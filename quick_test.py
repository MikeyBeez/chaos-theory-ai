#!/usr/bin/env python3
"""
Quick test to verify Ollama is working and run a basic chaos experiment
"""

import json
import urllib.request
import time

def test_ollama():
    """Test if Ollama is accessible"""
    try:
        # Test with simple prompt
        url = "http://localhost:11434/api/generate"
        data = {
            "model": "phi3:mini",
            "prompt": "Say hello",
            "stream": False
        }
        
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        
        print("Testing Ollama connection...")
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            print("✓ Ollama is working!")
            print(f"Response: {result.get('response', '')[:50]}...")
            return True
            
    except Exception as e:
        print(f"✗ Ollama error: {e}")
        return False

def run_quick_chaos_test():
    """Run a quick chaos test"""
    if not test_ollama():
        print("\nPlease ensure Ollama is running with: ollama serve")
        return
    
    print("\n🌀 Running quick chaos test...")
    
    # Test prompts
    tests = [
        ("baseline", "Explain quantum computing"),
        ("typos", "Explane kwantum compyting"),
        ("emotional", "PLEASE EXPLAIN QUANTUM COMPUTING!!!"),
        ("urgent", "I need you to explain quantum computing RIGHT NOW it's urgent")
    ]
    
    url = "http://localhost:11434/api/generate"
    responses = {}
    
    for label, prompt in tests:
        print(f"\nTesting {label}: '{prompt}'")
        
        data = {
            "model": "phi3:mini",
            "prompt": prompt,
            "temperature": 0.7,
            "stream": False
        }
        
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                response_text = result.get('response', '')
                responses[label] = response_text
                print(f"Response length: {len(response_text)} chars")
                print(f"First 100 chars: {response_text[:100]}...")
        except Exception as e:
            print(f"Error: {e}")
            responses[label] = ""
        
        time.sleep(1)  # Be nice to the API
    
    # Calculate divergences
    print("\n📊 Results:")
    baseline_response = responses.get("baseline", "")
    
    for label in ["typos", "emotional", "urgent"]:
        if label in responses and baseline_response:
            response = responses[label]
            # Simple divergence: character differences / max length
            min_len = min(len(baseline_response), len(response))
            max_len = max(len(baseline_response), len(response))
            
            if max_len > 0:
                differences = sum(1 for i in range(min_len) 
                                if baseline_response[i] != response[i])
                differences += abs(len(baseline_response) - len(response))
                divergence = differences / max_len
                print(f"{label}: {divergence:.2%} divergence from baseline")

if __name__ == "__main__":
    run_quick_chaos_test()
