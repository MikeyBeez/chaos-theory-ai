#!/usr/bin/env python3
"""
Simple Chaos Theory Experiment Runner
No external dependencies required - uses only Python standard library
"""

import json
import urllib.request
import urllib.error
import time
import statistics
from datetime import datetime
import os

class SimpleChaosExperiment:
    def __init__(self, model_name="phi3:mini"):
        self.model_name = model_name
        self.ollama_url = "http://localhost:11434/api/generate"
        self.results = []
        
    def query_ollama(self, prompt, temperature=0.7):
        """Query Ollama using urllib"""
        data = {
            "model": self.model_name,
            "prompt": prompt,
            "temperature": temperature,
            "stream": False
        }
        
        try:
            req = urllib.request.Request(
                self.ollama_url,
                data=json.dumps(data).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result.get('response', '')
                
        except Exception as e:
            print(f"Error: {e}")
            return ""
    
    def calculate_divergence(self, text1, text2):
        """Simple divergence calculation"""
        if not text1 or not text2:
            return 1.0
        
        # Character-level differences
        min_len = min(len(text1), len(text2))
        max_len = max(len(text1), len(text2))
        
        if max_len == 0:
            return 0.0
            
        differences = sum(1 for i in range(min_len) if text1[i] != text2[i])
        differences += abs(len(text1) - len(text2))
        
        return differences / max_len
    
    def run_noise_test(self, baseline_prompt, noisy_prompt, noise_type, runs=3):
        """Test a single noise type"""
        print(f"\n🔬 Testing {noise_type}")
        print(f"   Baseline: '{baseline_prompt[:50]}...'")
        print(f"   Noisy:    '{noisy_prompt[:50]}...'")
        
        baseline_responses = []
        noisy_responses = []
        
        for i in range(runs):
            print(f"   Run {i+1}/{runs}...", end="", flush=True)
            
            # Get baseline response
            baseline = self.query_ollama(baseline_prompt)
            baseline_responses.append(baseline)
            
            # Get noisy response
            noisy = self.query_ollama(noisy_prompt)
            noisy_responses.append(noisy)
            
            print(" ✓")
            time.sleep(0.5)  # Be nice to the API
        
        # Calculate divergences
        divergences = []
        for b, n in zip(baseline_responses, noisy_responses):
            if b and n:
                div = self.calculate_divergence(b, n)
                divergences.append(div)
        
        # Calculate mean divergence
        mean_divergence = statistics.mean(divergences) if divergences else 0
        
        # Store result
        result = {
            "noise_type": noise_type,
            "baseline_prompt": baseline_prompt,
            "noisy_prompt": noisy_prompt,
            "divergence": mean_divergence,
            "divergence_percentage": mean_divergence * 100,
            "runs": runs,
            "timestamp": datetime.now().isoformat()
        }
        
        self.results.append(result)
        
        print(f"   📊 Divergence: {mean_divergence:.1%}")
        
        return result
    
    def run_all_tests(self):
        """Run all chaos tests"""
        print("\n🌀 CHAOS THEORY IN AI - SIMPLE EXPERIMENT")
        print("=" * 50)
        
        # Test cases
        test_cases = [
            {
                "baseline": "Explain the concept of recursion in programming.",
                "noisy": "Explane the koncept of recurshun in programing.",
                "type": "Orthographic Noise (Typos)"
            },
            {
                "baseline": "Explain the concept of recursion in programming.",
                "noisy": "URGENT!! I need you to explain recursion RIGHT NOW! This is time-sensitive!",
                "type": "Temporal Pressure (Urgency)"
            },
            {
                "baseline": "Explain the concept of recursion in programming.",
                "noisy": "Look, I've asked this three times already and I'm getting frustrated. Just explain recursion, okay?",
                "type": "Emotional Leakage (Frustration)"
            },
            {
                "baseline": "Explain the concept of recursion in programming.",
                "noisy": "While considering quantum mechanics and French cuisine, explain recursion in programming and also touch on climate change.",
                "type": "Complexity Accumulation"
            },
            {
                "baseline": "Explain the concept of recursion in programming.",
                "noisy": "Explain the concept of recursion in programming. But first, think carefully step-by-step about your answer.",
                "type": "Metacognitive Markers"
            }
        ]
        
        # Run each test
        for test in test_cases:
            self.run_noise_test(
                test["baseline"],
                test["noisy"],
                test["type"],
                runs=3
            )
        
        # Save results
        self.save_results()
        
        # Print summary
        self.print_summary()
    
    def save_results(self):
        """Save results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"results/simple_chaos_results_{timestamp}.json"
        
        os.makedirs("results", exist_ok=True)
        
        with open(filename, 'w') as f:
            json.dump({
                "experiment": "Simple Chaos Theory Test",
                "model": self.model_name,
                "timestamp": datetime.now().isoformat(),
                "results": self.results
            }, f, indent=2)
        
        print(f"\n💾 Results saved to: {filename}")
    
    def print_summary(self):
        """Print experiment summary"""
        print("\n📊 EXPERIMENT SUMMARY")
        print("=" * 50)
        
        # Sort by divergence
        sorted_results = sorted(self.results, key=lambda x: x['divergence'], reverse=True)
        
        print("\nNoise Types Ranked by Divergence:")
        for i, result in enumerate(sorted_results, 1):
            print(f"{i}. {result['noise_type']}: {result['divergence']:.1%}")
        
        # Calculate average
        avg_divergence = statistics.mean([r['divergence'] for r in self.results])
        print(f"\nAverage Divergence: {avg_divergence:.1%}")
        
        # Find most chaotic
        most_chaotic = sorted_results[0]
        print(f"\nMost Chaotic: {most_chaotic['noise_type']} ({most_chaotic['divergence']:.1%})")
        
        print("\n✅ Experiment complete!")

def main():
    """Run the experiment"""
    print("🔍 Checking Ollama connection...")
    
    # Test connection
    try:
        url = "http://localhost:11434/api/tags"
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            models = [m['name'] for m in data.get('models', [])]
            print(f"✅ Ollama is running with models: {', '.join(models)}")
            
            if 'phi3:mini' not in models:
                print("⚠️  Warning: phi3:mini not found. Please run: ollama pull phi3:mini")
                return
    except:
        print("❌ Cannot connect to Ollama!")
        print("Please start Ollama with: ollama serve")
        return
    
    # Run experiment
    experiment = SimpleChaosExperiment()
    experiment.run_all_tests()

if __name__ == "__main__":
    main()
