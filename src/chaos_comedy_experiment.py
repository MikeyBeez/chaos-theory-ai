#!/usr/bin/env python3
"""
Enhanced Chaos Experiment with Comedy Critic
Now with 100% more amusement and smaller models for maximum chaos
"""

import json
import requests
import numpy as np
from typing import List, Dict, Tuple, Optional
import time
from datetime import datetime
import re
from collections import defaultdict

class ChaosExperimentWithCritic:
    """
    The original experiment but now with comedy critic validation
    """
    
    def __init__(self, model_name: str = "phi3:mini", critic_model: str = "gemma:2b"):
        self.model_name = model_name
        self.critic_model = critic_model
        self.ollama_url = "http://localhost:11434"
        self.results = defaultdict(list)
        self.comedy_gold = []  # Store the funniest moments
        
    def run_experiment_with_commentary(self):
        """
        Run the chaos experiment with live comedy commentary
        """
        print("🎭 CHAOS EXPERIMENT: COMEDY EDITION")
        print(f"Starring: {self.model_name} (our chaos subject)")
        print(f"With special guest critic: {self.critic_model}")
        print("="*50)
        
        # Load test cases
        with open("../experiments/test_cases.json", 'r') as f:
            test_cases = json.load(f)
        
        for noise_type, data in test_cases.items():
            if noise_type == "baseline":
                continue
                
            print(f"\n🎬 SCENE: {noise_type.replace('_', ' ').upper()}")
            print("-" * 40)
            
            baseline_prompts = test_cases["baseline"]["prompts"]
            noisy_prompts = data["prompts"]
            
            for i, (baseline, noisy) in enumerate(zip(baseline_prompts, noisy_prompts)):
                print(f"\n🎯 Test {i+1}: {baseline[:30]}...")
                
                # Get responses
                baseline_resp = self.query_model(baseline, self.model_name)
                noisy_resp = self.query_model(noisy, self.model_name)
                
                # Get critic's hot take
                critic_commentary = self.get_critic_commentary(
                    baseline, noisy, baseline_resp, noisy_resp, noise_type
                )
                
                print(f"🤖 Baseline length: {len(baseline_resp)} chars")
                print(f"🤪 Noisy length: {len(noisy_resp)} chars")
                print(f"🎭 Critic says: {critic_commentary}")
                
                # Store funny moments
                if "LOL" in critic_commentary or "😂" in critic_commentary:
                    self.comedy_gold.append({
                        "noise_type": noise_type,
                        "prompt": noisy,
                        "response_preview": noisy_resp[:100] + "...",
                        "critic_comment": critic_commentary
                    })
                
                time.sleep(0.5)  # Dramatic pause
        
        # Generate the comedy report
        self.generate_comedy_report()
    
    def get_critic_commentary(self, baseline_prompt: str, noisy_prompt: str,
                            baseline_resp: str, noisy_resp: str, 
                            noise_type: str) -> str:
        """
        Get the critic's comedic take on the responses
        """
        prompts = {
            "orthographic_noise": f"""
                The human typed: "{noisy_prompt}"
                
                The AI responded with: "{noisy_resp[:200]}..."
                
                Compared to the clean version which said: "{baseline_resp[:200]}..."
                
                Rate the chaos (1-10) and give your funniest observation in one sentence.
                Use emojis if appropriate. Be honest if it's hilariously bad.
            """,
            
            "temporal_pressure": f"""
                Human said URGENTLY: "{noisy_prompt}"
                
                AI's "quick" response: "{noisy_resp[:200]}..."
                
                VS the leisurely version: "{baseline_resp[:200]}..."
                
                Did the AI actually hurry? Give a sarcastic review with chaos rating (1-10).
            """,
            
            "emotional_leakage": f"""
                Emotional human: "{noisy_prompt}"
                
                AI's response: "{noisy_resp[:200]}..."
                
                VS emotionless version: "{baseline_resp[:200]}..."
                
                Rate the emotional intelligence fail/win (1-10) and roast or praise accordingly.
            """,
            
            "complexity_accumulation": f"""
                Human's kitchen sink prompt: "{noisy_prompt}"
                
                AI tried to answer with: "{noisy_resp[:200]}..."
                
                Single topic version said: "{baseline_resp[:200]}..."
                
                Did the AI have a stroke? Rate the chaos (1-10) and comment on the word salad.
            """,
            
            "metacognitive_markers": f"""
                Human with special instructions: "{noisy_prompt}"
                
                AI's attempt: "{noisy_resp[:200]}..."
                
                Normal version: "{baseline_resp[:200]}..."
                
                Did the AI follow instructions or rebel? Chaos rating (1-10) + sassy comment.
            """
        }
        
        critic_prompt = prompts.get(noise_type, "Just roast this response.")
        
        try:
            response = self.query_model(critic_prompt, self.critic_model)
            return response[:200]  # Keep it snappy
        except:
            return "🤷 Critic.exe has stopped working"
    
    def query_model(self, prompt: str, model: str) -> str:
        """Query any model"""
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "temperature": 0.8,  # Higher temp for more chaos
                    "stream": False
                },
                timeout=30
            )
            return response.json().get("response", "")
        except:
            return "[Model had an existential crisis and refused to answer]"
    
    def generate_comedy_report(self):
        """
        Generate the final comedy report
        """
        report = [
            "\n" + "="*60,
            "🎭 CHAOS EXPERIMENT: THE COMEDY REPORT",
            "="*60,
            "",
            f"Test Subject: {self.model_name}",
            f"Critic: {self.critic_model}",
            f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            "🏆 HIGHLIGHTS FROM THE COMEDY GOLD COLLECTION:",
            "-" * 50
        ]
        
        if self.comedy_gold:
            for i, moment in enumerate(self.comedy_gold[:5], 1):
                report.extend([
                    f"\n{i}. {moment['noise_type'].replace('_', ' ').title()}",
                    f"   Prompt: {moment['prompt']}",
                    f"   Response: {moment['response_preview']}",
                    f"   Critic: {moment['critic_comment']}",
                    ""
                ])
        else:
            report.append("No comedy gold found. The models were suspiciously well-behaved.")
        
        report.extend([
            "\n🎪 CHAOS CIRCUS SUMMARY:",
            "-" * 50,
            f"Total experiments run: {len(self.results)}",
            f"Comedy gold moments: {len(self.comedy_gold)}",
            f"Critic breakdowns: {sum(1 for m in self.comedy_gold if '🤷' in m.get('critic_comment', ''))}",
            "",
            "📊 SCIENTIFIC CONCLUSION:",
            "The smaller the model, the bigger the chaos.",
            "The bigger the chaos, the bigger the laughs.",
            "Therefore: Small models = Big laughs. QED. 🎭",
            "",
            "Remember: We came for the chaos theory,",
            "          We stayed for the comedy show!"
        ])
        
        report_text = "\n".join(report)
        
        # Save the comedy report
        with open("../results/COMEDY_REPORT.md", 'w') as f:
            f.write(report_text)
        
        print(report_text)
        
        # Also save the raw comedy moments
        with open("../results/comedy_gold.json", 'w') as f:
            json.dump(self.comedy_gold, f, indent=2)

if __name__ == "__main__":
    print("🎪 Welcome to the Chaos Comedy Experiment!")
    print("Using small models for MAXIMUM CHAOS")
    print("")
    
    experiment = ChaosExperimentWithCritic(
        model_name="phi3:mini",  # Small model = Big chaos
        critic_model="gemma:2b"  # Another small model critiquing!
    )
    
    experiment.run_experiment_with_commentary()
    
    print("\n✨ The chaos has been measured, the comedy has been captured!")
    print("Check ../results/COMEDY_REPORT.md for the full experience")
