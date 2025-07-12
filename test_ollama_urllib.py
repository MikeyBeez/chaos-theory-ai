#!/usr/bin/env python3
"""Quick test to verify Ollama connection using urllib"""

import urllib.request
import json

def test_ollama():
    url = "http://localhost:11434/api/generate"
    
    print("Testing Ollama connection...")
    
    # Simple test prompt
    test_data = {
        "model": "phi3:mini",
        "prompt": "Hello, please respond with a single sentence.",
        "temperature": 0.7,
        "stream": False
    }
    
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(test_data).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            print("✅ Ollama is working!")
            print(f"Response: {result.get('response', 'No response')[:100]}...")
            return True
            
    except urllib.error.URLError as e:
        print("❌ Cannot connect to Ollama. Is it running on port 11434?")
        print(f"Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    if test_ollama():
        print("\nOllama is ready for experiments!")
    else:
        print("\nPlease ensure Ollama is running with: ollama serve")
