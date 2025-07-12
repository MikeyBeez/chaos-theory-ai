#!/usr/bin/env python3
"""
Chaos Theory Analysis for AI Responses
Demonstrates concepts from "The Butterfly Effect in AI" paper
"""

import json
import numpy as np
from typing import Dict, List, Tuple
import math

class ChaosTheoryAnalyzer:
    """Analyze AI responses using chaos theory metrics"""
    
    def __init__(self):
        self.results = {}
        
    def calculate_lyapunov_proxy(self, baseline_response: str, noisy_response: str, 
                                prompt_distance: float = 0.1) -> float:
        """
        Calculate proxy Lyapunov exponent
        λ_proxy = (1/t) * ln(|response_divergence| / |prompt_divergence|)
        
        Since we're comparing single responses, t=1
        """
        from difflib import SequenceMatcher
        
        # Calculate response divergence (edit distance)
        response_similarity = SequenceMatcher(None, baseline_response, noisy_response).ratio()
        response_divergence = 1 - response_similarity
        
        # Avoid log(0)
        if response_divergence < 0.001:
            response_divergence = 0.001
            
        # Calculate proxy Lyapunov
        # prompt_distance represents how different the prompts are
        lyapunov = math.log(response_divergence / prompt_distance)
        
        return lyapunov
    
    def calculate_kaplan_yorke_dimension(self, lyapunov_exponents: List[float]) -> float:
        """
        Calculate Kaplan-Yorke dimension
        D_KY = k + (Σᵢ₌₁ᵏ λᵢ) / |λₖ₊₁|
        
        where k is the largest integer such that Σᵢ₌₁ᵏ λᵢ ≥ 0
        """
        # Sort exponents in descending order
        sorted_exponents = sorted(lyapunov_exponents, reverse=True)
        
        # Find k
        cumsum = 0
        k = 0
        for i, exp in enumerate(sorted_exponents):
            cumsum += exp
            if cumsum >= 0:
                k = i + 1
            else:
                break
        
        if k == 0 or k >= len(sorted_exponents):
            return float(k)
        
        # Calculate dimension
        sum_positive = sum(sorted_exponents[:k])
        d_ky = k + (sum_positive / abs(sorted_exponents[k]))
        
        return d_ky
    
    def analyze_attractor_basins(self, responses: List[str]) -> Dict:
        """
        Analyze the stability of attractor basins by measuring
        variance in responses to the same prompt type
        """
        from difflib import SequenceMatcher
        
        if len(responses) < 2:
            return {"stability": 1.0, "variance": 0.0}
        
        # Calculate pairwise similarities
        similarities = []
        for i in range(len(responses)):
            for j in range(i + 1, len(responses)):
                sim = SequenceMatcher(None, responses[i], responses[j]).ratio()
                similarities.append(sim)
        
        mean_similarity = np.mean(similarities)
        variance = np.var(similarities)
        
        return {
            "stability": mean_similarity,
            "variance": variance,
            "attractor_strength": 1 - variance  # Higher = stronger attractor
        }
    
    def measure_response_complexity(self, response: str) -> Dict:
        """
        Measure various complexity metrics of a response
        Related to the Kaplan-Yorke dimension concept
        """
        words = response.split()
        sentences = response.split('.')
        
        # Vocabulary diversity (unique words / total words)
        vocab_diversity = len(set(words)) / len(words) if words else 0
        
        # Sentence complexity (words per sentence)
        avg_sentence_length = len(words) / len(sentences) if sentences else 0
        
        # Information density (characters per word)
        avg_word_length = len(response) / len(words) if words else 0
        
        # Punctuation complexity
        punctuation_density = sum(1 for c in response if c in '.,!?;:()[]{}') / len(response) if response else 0
        
        return {
            "vocab_diversity": vocab_diversity,
            "avg_sentence_length": avg_sentence_length,
            "avg_word_length": avg_word_length,
            "punctuation_density": punctuation_density,
            "complexity_score": vocab_diversity * avg_sentence_length * 0.1  # Combined metric
        }
    
    def analyze_noise_effects(self, test_results: Dict) -> Dict:
        """
        Comprehensive analysis of how different noise types affect AI behavior
        """
        analysis = {}
        
        for noise_type, results in test_results.items():
            if not results:
                continue
                
            # Extract metrics
            divergences = [r.get('divergence', 0) for r in results]
            lyapunovs = [r.get('lyapunov', 0) for r in results]
            complexities = [r.get('complexity', {}).get('complexity_score', 0) for r in results]
            
            analysis[noise_type] = {
                "mean_divergence": np.mean(divergences),
                "std_divergence": np.std(divergences),
                "mean_lyapunov": np.mean(lyapunovs),
                "mean_complexity": np.mean(complexities),
                "chaos_classification": self._classify_chaos_level(np.mean(lyapunovs))
            }
        
        return analysis
    
    def _classify_chaos_level(self, lyapunov: float) -> str:
        """Classify the chaos level based on Lyapunov exponent"""
        if lyapunov < 0:
            return "Stable (Converging)"
        elif lyapunov < 0.5:
            return "Weakly Chaotic"
        elif lyapunov < 1.0:
            return "Moderately Chaotic"
        else:
            return "Strongly Chaotic"
    
    def generate_report(self, test_results: Dict) -> str:
        """Generate a comprehensive report of the chaos analysis"""
        report = []
        report.append("="*60)
        report.append("CHAOS THEORY ANALYSIS OF AI RESPONSES")
        report.append("="*60)
        report.append("")
        
        # Analyze each noise type
        analysis = self.analyze_noise_effects(test_results)
        
        # Sort by mean Lyapunov exponent
        sorted_types = sorted(analysis.items(), key=lambda x: x[1]['mean_lyapunov'])
        
        report.append("NOISE TYPE ANALYSIS (sorted by chaos level):")
        report.append("-"*50)
        
        for noise_type, metrics in sorted_types:
            report.append(f"\n{noise_type.upper()}:")
            report.append(f"  Chaos Classification: {metrics['chaos_classification']}")
            report.append(f"  Mean Lyapunov Exponent: {metrics['mean_lyapunov']:.3f}")
            report.append(f"  Mean Divergence: {metrics['mean_divergence']:.3f} (±{metrics['std_divergence']:.3f})")
            report.append(f"  Mean Complexity: {metrics['mean_complexity']:.3f}")
        
        # Visual representation
        report.append("\n" + "="*60)
        report.append("CHAOS SPECTRUM VISUALIZATION")
        report.append("="*60)
        report.append("\nLow Chaos ←→ High Chaos")
        report.append("-"*50)
        
        for noise_type, metrics in sorted_types:
            lyapunov = metrics['mean_lyapunov']
            # Normalize to 0-1 range for visualization
            normalized = min(max((lyapunov + 2) / 4, 0), 1)  # Map [-2, 2] to [0, 1]
            bar_length = int(normalized * 40)
            bar = "▓" * bar_length + "░" * (40 - bar_length)
            report.append(f"{noise_type:25} [{bar}]")
        
        # Key insights
        report.append("\n" + "="*60)
        report.append("KEY INSIGHTS")
        report.append("="*60)
        
        # Find most and least chaotic
        most_chaotic = sorted_types[-1]
        least_chaotic = sorted_types[0]
        
        report.append(f"\n• Most Chaotic: {most_chaotic[0]} (λ = {most_chaotic[1]['mean_lyapunov']:.3f})")
        report.append(f"• Most Stable: {least_chaotic[0]} (λ = {least_chaotic[1]['mean_lyapunov']:.3f})")
        
        # Calculate Kaplan-Yorke dimension estimate
        all_lyapunovs = [m['mean_lyapunov'] for _, m in analysis.items()]
        if all_lyapunovs:
            ky_dimension = self.calculate_kaplan_yorke_dimension(all_lyapunovs)
            report.append(f"\n• Estimated Kaplan-Yorke Dimension: {ky_dimension:.2f}")
            report.append("  (Higher dimension = more complex response patterns)")
        
        return "\n".join(report)

# Example usage function
def demonstrate_chaos_analysis():
    """Demonstrate the chaos theory analysis with example data"""
    
    # Example test results (would come from actual Ollama experiments)
    example_results = {
        "orthographic_noise": [
            {
                "divergence": 0.45,
                "lyapunov": 0.8,
                "complexity": {"complexity_score": 0.3}
            },
            {
                "divergence": 0.52,
                "lyapunov": 0.9,
                "complexity": {"complexity_score": 0.28}
            }
        ],
        "temporal_pressure": [
            {
                "divergence": 0.38,
                "lyapunov": -0.2,
                "complexity": {"complexity_score": 0.15}
            },
            {
                "divergence": 0.35,
                "lyapunov": -0.1,
                "complexity": {"complexity_score": 0.18}
            }
        ],
        "emotional_leakage": [
            {
                "divergence": 0.65,
                "lyapunov": 1.2,
                "complexity": {"complexity_score": 0.45}
            },
            {
                "divergence": 0.58,
                "lyapunov": 1.1,
                "complexity": {"complexity_score": 0.42}
            }
        ],
        "complexity_accumulation": [
            {
                "divergence": 0.72,
                "lyapunov": 0.3,
                "complexity": {"complexity_score": 0.68}
            },
            {
                "divergence": 0.68,
                "lyapunov": 0.4,
                "complexity": {"complexity_score": 0.65}
            }
        ]
    }
    
    # Create analyzer and generate report
    analyzer = ChaosTheoryAnalyzer()
    report = analyzer.generate_report(example_results)
    
    print(report)
    
    # Save report
    with open("chaos_analysis_report.txt", "w") as f:
        f.write(report)
    
    print("\n\nReport saved to: chaos_analysis_report.txt")

if __name__ == "__main__":
    print("🌀 Chaos Theory Analyzer for AI Responses")
    print("Based on 'The Butterfly Effect in AI' concepts\n")
    
    demonstrate_chaos_analysis()
