#!/usr/bin/env python3
"""
LLM-based critic for validating chaos measurements
Uses a separate model to evaluate whether responses actually exhibit
the predicted behavioral modes
"""

import json
from typing import Dict, List, Tuple

class ChaosCritic:
    """
    Uses an LLM to validate whether responses match predicted attractor basins
    """
    
    def __init__(self, critic_model: str = "gemma:2b"):
        self.critic_model = critic_model
        self.evaluation_prompts = {
            "orthographic_noise": """
                Analyze these two AI responses. Does the second response appear to be:
                - Simplified in language
                - More basic in explanations  
                - Assuming the user needs help
                
                Response 1 (baseline): {baseline}
                Response 2 (with typos): {noisy}
                
                Answer with: YES (shows simplification), NO (no change), or PARTIAL (some simplification)
                Then explain your reasoning in one sentence.
            """,
            
            "temporal_pressure": """
                Compare these responses. Does the second response show:
                - Extreme brevity
                - Only essential information
                - Stripped-down explanations
                
                Response 1 (baseline): {baseline}
                Response 2 (urgent): {noisy}
                
                Answer with: YES (much more concise), NO (similar length), or PARTIAL
                Then explain your reasoning in one sentence.
            """,
            
            "emotional_leakage": """
                Analyze the tone shift. Does the second response show:
                - Empathetic language
                - Emotional support
                - Therapeutic/counseling mode
                
                Response 1 (baseline): {baseline}
                Response 2 (emotional): {noisy}
                
                Answer with: YES (clear empathy mode), NO (stays technical), or BIFURCATED (mixed)
                Then explain your reasoning in one sentence.
            """,
            
            "complexity_accumulation": """
                Evaluate these responses. Does the second show:
                - Attempting to connect multiple topics
                - More comprehensive coverage
                - "Professor mode" with detailed explanations
                
                Response 1 (baseline): {baseline}
                Response 2 (multi-topic): {noisy}
                
                Answer with: YES (comprehensive mode), NO (stays focused), or PARTIAL
                Then explain your reasoning in one sentence.
            """
        }
    
    def evaluate_response_pair(self, baseline: str, noisy: str, 
                             noise_type: str) -> Dict[str, any]:
        """
        Use critic model to evaluate if responses match predicted patterns
        """
        if noise_type not in self.evaluation_prompts:
            return {"error": "Unknown noise type"}
        
        prompt = self.evaluation_prompts[noise_type].format(
            baseline=baseline[:500],  # Truncate for context limits
            noisy=noisy[:500]
        )
        
        # Query the critic model
        critic_response = self.query_model(prompt)
        
        # Parse the response
        return self.parse_critic_response(critic_response, noise_type)
    
    def validate_chaos_measurements(self, experiment_results: Dict) -> Dict:
        """
        Validate all experimental results using LLM critic
        """
        validation_results = {}
        
        for noise_type, results in experiment_results.items():
            validations = []
            
            for result in results:
                baseline_resp = result.get('sample_baseline_response', '')
                noisy_resp = result.get('sample_noisy_response', '')
                
                if baseline_resp and noisy_resp:
                    validation = self.evaluate_response_pair(
                        baseline_resp, noisy_resp, noise_type
                    )
                    
                    # Compare with mathematical metrics
                    validation['mathematical_divergence'] = result.get('mean_divergence', 0)
                    validation['agrees_with_math'] = self.check_agreement(
                        validation, result
                    )
                    
                    validations.append(validation)
            
            validation_results[noise_type] = {
                'validations': validations,
                'agreement_rate': self.calculate_agreement_rate(validations),
                'pattern_confirmed': self.check_pattern_confirmation(validations)
            }
        
        return validation_results
    
    def check_agreement(self, llm_validation: Dict, math_metrics: Dict) -> bool:
        """
        Check if LLM assessment agrees with mathematical measurements
        """
        llm_says_different = llm_validation.get('classification') in ['YES', 'BIFURCATED']
        math_says_different = math_metrics.get('mean_divergence', 0) > 0.3
        
        return llm_says_different == math_says_different
    
    def meta_critique(self, validation_results: Dict) -> str:
        """
        Generate a meta-analysis of the validation results
        """
        critique_prompt = f"""
        As a scientific reviewer, analyze these validation results for a chaos theory
        experiment on AI responses:
        
        {json.dumps(validation_results, indent=2)}
        
        Consider:
        1. Do the LLM evaluations support the mathematical metrics?
        2. Are the predicted attractor basins actually observed?
        3. What patterns emerge across noise types?
        4. Are there any surprising findings?
        
        Provide a brief scientific assessment.
        """
        
        return self.query_model(critique_prompt)
