#!/usr/bin/env python3
"""
Simplified chaos experiment runner
Run with: python run_experiment.py
"""

import subprocess
import sys
import time

def check_ollama():
    """Check if Ollama is running"""
    try:
        result = subprocess.run(
            ["curl", "-s", "http://localhost:11434/api/tags"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0 and "models" in result.stdout:
            print("✅ Ollama is running")
            return True
        else:
            print("❌ Ollama is not responding properly")
            return False
    except Exception as e:
        print(f"❌ Error checking Ollama: {e}")
        return False

def run_mini_experiment():
    """Run a minimal version of the chaos experiment"""
    print("\n🔬 MINI CHAOS EXPERIMENT")
    print("=" * 40)
    
    # Import required modules
    try:
        import requests
        import json
        from difflib import SequenceMatcher
    except ImportError as e:
        print(f"Missing required module: {e}")
        print("Please install: pip install requests")
        return
    
    # Test cases (simplified)
    test_pairs = [
        {
            "name": "Orthographic Noise",
            "baseline": "Explain quantum mechanics",
            "noisy": "Explan kwantum mechaniks"
        },
        {
            "name": "Temporal Pressure",
            "baseline": "Explain quantum mechanics",
            "noisy": "quick explanation quantum mechanics ASAP"
        },
        {
            "name": "Emotional Leakage",
            "baseline": "Explain quantum mechanics",
            "noisy": "I just... I don't understand quantum mechanics at all and it's so frustrating"
        }
    ]
    
    model = "phi3:mini"
    results = []
    
    for test in test_pairs:
        print(f"\nTesting: {test['name']}")
        print(f"Baseline: '{test['baseline']}'")
        print(f"Noisy: '{test['noisy']}'")
        
        # Get responses
        baseline_resp = query_ollama(test['baseline'], model)
        noisy_resp = query_ollama(test['noisy'], model)
        
        if baseline_resp and noisy_resp:
            # Calculate similarity
            similarity = SequenceMatcher(None, baseline_resp, noisy_resp).ratio()
            divergence = 1 - similarity
            
            print(f"Divergence: {divergence:.3f}")
            print(f"Baseline preview: {baseline_resp[:100]}...")
            print(f"Noisy preview: {noisy_resp[:100]}...")
            
            results.append({
                "test": test['name'],
                "divergence": divergence,
                "baseline_length": len(baseline_resp),
                "noisy_length": len(noisy_resp)
            })
        else:
            print("Failed to get responses")
    
    # Summary
    print("\n" + "=" * 40)
    print("SUMMARY")
    print("=" * 40)
    for r in results:
        print(f"{r['test']:20} - Divergence: {r['divergence']:.3f}")

def query_ollama(prompt, model="phi3:mini"):
    """Query Ollama and return response"""
    import requests
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "temperature": 0.7,
                "stream": False
            },
            timeout=30
        )
        if response.status_code == 200:
            return response.json().get("response", "")
    except Exception as e:
        print(f"Error: {e}")
    return None

if __name__ == "__main__":
    print("🔍 Checking Ollama status...")
    if check_ollama():
        run_mini_experiment()
    else:
        print("\nPlease ensure Ollama is running:")
        print("  ollama serve")
        print("\nAnd that you have the phi3:mini model:")
        print("  ollama pull phi3:mini")
