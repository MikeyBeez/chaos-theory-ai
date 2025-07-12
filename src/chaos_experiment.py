#!/usr/bin/env python3
"""
Chaos Theory in AI: Measuring response divergence in LLMs
Based on "The Butterfly Effect in AI" paper concepts
"""

import json
import requests
import numpy as np
from typing import List, Dict, Tuple, Optional
import time
from datetime import datetime
import hashlib
from difflib import SequenceMatcher
import re
from collections import defaultdict

class ChaosExperiment:
    def __init__(self, model_name: str = "phi3:mini", ollama_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.ollama_url = ollama_url
        self.results = defaultdict(list)
        
    def query_ollama(self, prompt: str, temperature: float = 0.7) -> str:
        """Query Ollama API and return response"""
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "temperature": temperature,
                    "stream": False
                },
                timeout=30
            )
            response.raise_for_status()
            return response.json()["response"]
        except Exception as e:
            print(f"Error querying Ollama: {e}")
            return ""
    
    def calculate_edit_distance(self, s1: str, s2: str) -> float:
        """Calculate normalized edit distance between two strings"""
        return 1 - SequenceMatcher(None, s1, s2).ratio()
    
    def extract_features(self, response: str) -> Dict[str, float]:
        """Extract features from a response for comparison"""
        features = {
            "length": len(response),
            "word_count": len(response.split()),
            "sentence_count": len(re.split(r'[.!?]+', response)),
            "avg_word_length": np.mean([len(w) for w in response.split()]) if response else 0,
            "complexity_score": len(set(response.split())) / len(response.split()) if response else 0,  # Vocabulary diversity
            "punctuation_ratio": sum(1 for c in response if c in '.,!?;:') / len(response) if response else 0,
            "uppercase_ratio": sum(1 for c in response if c.isupper()) / len(response) if response else 0,
        }
        return features
    
    def calculate_divergence(self, response1: str, response2: str) -> Dict[str, float]:
        """Calculate various divergence metrics between two responses"""
        # Text similarity
        edit_distance = self.calculate_edit_distance(response1, response2)
        
        # Feature-based divergence
        features1 = self.extract_features(response1)
        features2 = self.extract_features(response2)
        
        feature_divergence = {}
        for key in features1:
            if features1[key] > 0 or features2[key] > 0:
                feature_divergence[key] = abs(features1[key] - features2[key]) / max(features1[key], features2[key])
        
        # Calculate proxy Lyapunov exponent
        # λ_proxy = log(response_divergence / prompt_divergence)
        # For identical prompts, we use a small epsilon to avoid division by zero
        proxy_lyapunov = np.log(edit_distance + 0.001) / np.log(0.001)
        
        return {
            "edit_distance": edit_distance,
            "proxy_lyapunov": proxy_lyapunov,
            "feature_divergence": feature_divergence,
            "mean_feature_divergence": np.mean(list(feature_divergence.values()))
        }
    
    def run_single_experiment(self, baseline_prompt: str, noisy_prompt: str, 
                            noise_type: str, num_runs: int = 3) -> Dict:
        """Run experiment comparing baseline and noisy prompt responses"""
        print(f"\nTesting: {noise_type}")
        print(f"Baseline: '{baseline_prompt}'")
        print(f"Noisy: '{noisy_prompt}'")
        
        baseline_responses = []
        noisy_responses = []
        
        # Generate multiple responses for statistical validity
        for i in range(num_runs):
            print(f"  Run {i+1}/{num_runs}...", end="", flush=True)
            baseline_responses.append(self.query_ollama(baseline_prompt))
            noisy_responses.append(self.query_ollama(noisy_prompt))
            print(" ✓")
            time.sleep(0.5)  # Be nice to the API
        
        # Calculate divergences
        divergences = []
        for br, nr in zip(baseline_responses, noisy_responses):
            if br and nr:  # Only if both responses are valid
                div = self.calculate_divergence(br, nr)
                divergences.append(div)
        
        # Calculate attractor basin stability (variance within same prompt type)
        baseline_stability = []
        noisy_stability = []
        
        for i in range(len(baseline_responses)):
            for j in range(i+1, len(baseline_responses)):
                if baseline_responses[i] and baseline_responses[j]:
                    baseline_stability.append(
                        self.calculate_edit_distance(baseline_responses[i], baseline_responses[j])
                    )
                if noisy_responses[i] and noisy_responses[j]:
                    noisy_stability.append(
                        self.calculate_edit_distance(noisy_responses[i], noisy_responses[j])
                    )
        
        result = {
            "baseline_prompt": baseline_prompt,
            "noisy_prompt": noisy_prompt,
            "noise_type": noise_type,
            "divergences": divergences,
            "mean_divergence": np.mean([d["edit_distance"] for d in divergences]) if divergences else 0,
            "mean_proxy_lyapunov": np.mean([d["proxy_lyapunov"] for d in divergences]) if divergences else 0,
            "baseline_stability": np.mean(baseline_stability) if baseline_stability else 0,
            "noisy_stability": np.mean(noisy_stability) if noisy_stability else 0,
            "sample_baseline_response": baseline_responses[0][:200] + "..." if baseline_responses[0] else "",
            "sample_noisy_response": noisy_responses[0][:200] + "..." if noisy_responses[0] else "",
            "timestamp": datetime.now().isoformat()
        }
        
        return result
    
    def run_full_experiment(self, test_cases_file: str = "test_cases.json") -> None:
        """Run the full experiment across all noise types"""
        # Load test cases
        with open(test_cases_file, 'r') as f:
            test_cases = json.load(f)
        
        baseline_prompts = test_cases["baseline"]["prompts"]
        
        # Run experiments for each noise type
        for noise_type, noise_data in test_cases.items():
            if noise_type == "baseline":
                continue
                
            noise_prompts = noise_data["prompts"]
            
            for baseline_prompt, noisy_prompt in zip(baseline_prompts, noise_prompts):
                result = self.run_single_experiment(
                    baseline_prompt, noisy_prompt, noise_type, num_runs=3
                )
                self.results[noise_type].append(result)
                
                # Save intermediate results
                self.save_results(f"chaos_results_{self.model_name.replace(':', '_')}.json")
        
        # Calculate summary statistics
        self.calculate_summary_stats()
    
    def calculate_summary_stats(self) -> None:
        """Calculate summary statistics across all experiments"""
        summary = {}
        
        for noise_type, experiments in self.results.items():
            divergences = [exp["mean_divergence"] for exp in experiments]
            lyapunovs = [exp["mean_proxy_lyapunov"] for exp in experiments]
            baseline_stabilities = [exp["baseline_stability"] for exp in experiments]
            noisy_stabilities = [exp["noisy_stability"] for exp in experiments]
            
            summary[noise_type] = {
                "mean_divergence": np.mean(divergences),
                "std_divergence": np.std(divergences),
                "mean_proxy_lyapunov": np.mean(lyapunovs),
                "std_proxy_lyapunov": np.std(lyapunovs),
                "mean_baseline_stability": np.mean(baseline_stabilities),
                "mean_noisy_stability": np.mean(noisy_stabilities),
                "attractor_shift": np.mean(noisy_stabilities) - np.mean(baseline_stabilities),
                "num_experiments": len(experiments)
            }
        
        self.summary = summary
        
        # Save summary
        with open(f"chaos_summary_{self.model_name.replace(':', '_')}.json", 'w') as f:
            json.dump(summary, f, indent=2)
        
        # Print summary
        print("\n" + "="*60)
        print("CHAOS EXPERIMENT SUMMARY")
        print("="*60)
        
        for noise_type, stats in summary.items():
            print(f"\n{noise_type.upper()}:")
            print(f"  Mean Divergence: {stats['mean_divergence']:.4f} (±{stats['std_divergence']:.4f})")
            print(f"  Proxy Lyapunov: {stats['mean_proxy_lyapunov']:.4f} (±{stats['std_proxy_lyapunov']:.4f})")
            print(f"  Baseline Stability: {stats['mean_baseline_stability']:.4f}")
            print(f"  Noisy Stability: {stats['mean_noisy_stability']:.4f}")
            print(f"  Attractor Shift: {stats['attractor_shift']:.4f}")
    
    def save_results(self, filename: str) -> None:
        """Save results to JSON file"""
        with open(filename, 'w') as f:
            json.dump(dict(self.results), f, indent=2)
    
    def visualize_results(self) -> None:
        """Create a simple text visualization of results"""
        if not hasattr(self, 'summary'):
            self.calculate_summary_stats()
        
        print("\n" + "="*60)
        print("CHAOS VISUALIZATION (Text-based)")
        print("="*60)
        
        # Sort noise types by mean divergence
        sorted_noise = sorted(self.summary.items(), key=lambda x: x[1]['mean_divergence'])
        
        print("\nDivergence Scale (0.0 = identical, 1.0 = completely different):")
        print("-" * 50)
        
        for noise_type, stats in sorted_noise:
            divergence = stats['mean_divergence']
            bar_length = int(divergence * 40)
            bar = "█" * bar_length + "░" * (40 - bar_length)
            print(f"{noise_type:25} [{bar}] {divergence:.3f}")
        
        print("\nProxy Lyapunov Exponents (higher = more chaotic):")
        print("-" * 50)
        
        sorted_lyapunov = sorted(self.summary.items(), key=lambda x: x[1]['mean_proxy_lyapunov'])
        for noise_type, stats in sorted_lyapunov:
            lyapunov = stats['mean_proxy_lyapunov']
            # Normalize to 0-1 range for visualization (assuming max ~10)
            normalized = min(lyapunov / 10, 1.0)
            bar_length = int(normalized * 40)
            bar = "▓" * bar_length + "░" * (40 - bar_length)
            print(f"{noise_type:25} [{bar}] {lyapunov:.3f}")

if __name__ == "__main__":
    # Initialize experiment
    print("🔬 CHAOS THEORY IN AI EXPERIMENT")
    print("================================")
    
    # You can change the model here
    model = "phi3:mini"  # Options: phi3:mini, gemma:2b, llama3.2:latest, etc.
    
    print(f"Model: {model}")
    print(f"Starting at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run experiment
    experiment = ChaosExperiment(model_name=model)
    experiment.run_full_experiment()
    
    # Visualize results
    experiment.visualize_results()
    
    print(f"\n✅ Experiment complete at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Results saved to: chaos_results_{model.replace(':', '_')}.json")
    print(f"Summary saved to: chaos_summary_{model.replace(':', '_')}.json")
