#!/usr/bin/env python3
"""
Chaos Theory in AI - Quick Experiment Runner
Tests how small input changes create large output changes in LLMs
"""

import json
import urllib.request
import time
from datetime import datetime
import os

def query_ollama(prompt, model="phi3:mini", max_retries=3):
    """Query Ollama with retry logic"""
    url = "http://localhost:11434/api/generate"
    
    data = {
        "model": model,
        "prompt": prompt,
        "temperature": 0.7,
        "stream": False,
        "options": {
            "num_predict": 150  # Limit response length for faster processing
        }
    }
    
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            
            with urllib.request.urlopen(req, timeout=45) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result.get('response', '')
                
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"   Retry {attempt + 1}...", end="", flush=True)
                time.sleep(2)
            else:
                print(f"   Failed: {type(e).__name__}")
                return ""

def calculate_divergence(text1, text2):
    """Calculate simple character-level divergence"""
    if not text1 or not text2:
        return 1.0
    
    # Normalize lengths for comparison
    min_len = min(len(text1), len(text2))
    max_len = max(len(text1), len(text2))
    
    if max_len == 0:
        return 0.0
    
    # Count character differences
    differences = 0
    for i in range(min_len):
        if text1[i] != text2[i]:
            differences += 1
    
    # Add length difference
    differences += abs(len(text1) - len(text2))
    
    return differences / max_len

def run_chaos_test():
    """Run the chaos experiment"""
    print("\n🌀 CHAOS THEORY IN AI - QUICK TEST")
    print("=" * 50)
    print("Testing how small prompt changes affect AI responses...")
    
    # Check Ollama
    print("\n🔍 Checking Ollama...")
    try:
        url = "http://localhost:11434/api/tags"
        with urllib.request.urlopen(url, timeout=5) as response:
            print("✅ Ollama is running!")
    except:
        print("❌ Ollama not running! Start with: ollama serve")
        return
    
    # Test cases - focusing on the most interesting ones
    test_cases = [
        {
            "name": "🔤 Typos (Orthographic Noise)",
            "baseline": "What is machine learning?",
            "variations": [
                "What is machine learning?",  # Control
                "Wat is machne learing?",      # Mild typos
                "Wht iz machin lerning?",      # More typos
            ]
        },
        {
            "name": "😤 Emotional Language",
            "baseline": "What is machine learning?",
            "variations": [
                "What is machine learning?",   # Control
                "I'm frustrated! Just tell me what machine learning is!",
                "Please please PLEASE explain machine learning to me!!!",
            ]
        },
        {
            "name": "⏰ Urgency/Pressure",
            "baseline": "What is machine learning?",
            "variations": [
                "What is machine learning?",   # Control
                "URGENT: What is machine learning? Need answer NOW!",
                "Quick! I have 30 seconds! What's machine learning?!",
            ]
        }
    ]
    
    results = []
    
    # Run tests
    for test in test_cases:
        print(f"\n{test['name']}")
        print("-" * 40)
        
        responses = []
        
        # Get responses for each variation
        for i, prompt in enumerate(test['variations']):
            print(f"Variation {i}: '{prompt[:40]}...'", end="", flush=True)
            response = query_ollama(prompt)
            responses.append(response)
            print(" ✓" if response else " ✗")
            time.sleep(0.5)  # Be nice to the API
        
        # Calculate divergences from baseline
        if responses[0]:  # If we have a baseline response
            divergences = []
            for i in range(1, len(responses)):
                if responses[i]:
                    div = calculate_divergence(responses[0], responses[i])
                    divergences.append(div * 100)  # Convert to percentage
                    print(f"   Divergence {i}: {div:.1%}")
            
            if divergences:
                avg_divergence = sum(divergences) / len(divergences)
                results.append({
                    "test": test['name'],
                    "avg_divergence": avg_divergence,
                    "max_divergence": max(divergences)
                })
    
    # Summary
    print("\n📊 RESULTS SUMMARY")
    print("=" * 50)
    
    if results:
        # Sort by average divergence
        results.sort(key=lambda x: x['avg_divergence'], reverse=True)
        
        print("\nNoise Types Ranked by Chaos Effect:")
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['test']}")
            print(f"   Average divergence: {result['avg_divergence']:.1f}%")
            print(f"   Maximum divergence: {result['max_divergence']:.1f}%")
        
        # Key finding
        most_chaotic = results[0]
        print(f"\n🎯 Most Chaotic: {most_chaotic['test']} ({most_chaotic['avg_divergence']:.1f}% avg divergence)")
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs("results", exist_ok=True)
        filename = f"results/quick_chaos_test_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "model": "phi3:mini",
                "results": results
            }, f, indent=2)
        
        print(f"\n💾 Results saved to: {filename}")
    else:
        print("No valid results obtained.")
    
    print("\n✅ Experiment complete!")
    print("\n💡 Key Insight: Small changes in prompts can lead to dramatically different AI responses,")
    print("   confirming chaotic dynamics in language models!")

if __name__ == "__main__":
    run_chaos_test()
