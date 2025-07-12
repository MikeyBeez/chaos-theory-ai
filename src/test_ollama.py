#!/usr/bin/env python3
"""Quick test to verify Ollama connection"""

import requests
import json

def test_ollama():
    url = "http://localhost:11434/api/generate"
    
    print("Testing Ollama connection...")
    
    # Simple test prompt
    test_prompt = "Hello, please respond with a single sentence."
    
    try:
        response = requests.post(
            url,
            json={
                "model": "phi3:mini",
                "prompt": test_prompt,
                "temperature": 0.7,
                "stream": False
            },
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Ollama is working!")
            print(f"Response: {result.get('response', 'No response')[:100]}...")
            return True
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            print(response.text)
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Ollama. Is it running on port 11434?")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    if test_ollama():
        print("\nOllama is ready for experiments!")
        print("You can now run: python chaos_experiment.py")
    else:
        print("\nPlease ensure Ollama is running with: ollama serve")
