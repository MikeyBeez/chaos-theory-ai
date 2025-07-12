#!/usr/bin/env python3
"""
Minimal Chaos Experiment - No external dependencies
Uses only Python standard library
"""

import json
import urllib.request
import urllib.error
import time
import statistics
from datetime import datetime
import os

print("🌀 MINIMAL CHAOS THEORY EXPERIMENT")
print("=" * 40)
print(f"Started: {datetime.now().strftime('%H:%M:%S')}")

# Configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "phi3:mini"

def query_ollama(prompt, temperature=0.7):
    """Query Ollama using urllib"""
    data = json.dumps({
        "model": MODEL,
        "prompt": prompt,
        "temperature": temperature,
        "stream": False
    }).encode('utf-8')
    
    req = urllib.request.Request(
        OLLAMA_URL,
        data=data,
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get('response', '')
    except urllib.error.URLError as e:
        print(f"  ✗ Network error: {e}")
        return ""
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return ""

def calculate_divergence(text1, text2):
    """Calculate simple character-level divergence"""
    if not text1 or not text2:
        return 1.0
    
    min_len = min(len(text1), len(text2))
    max_len = max(len(text1), len(text2))
    
    if max_len == 0:
        return 0.0
    
    differences = sum(1 for i in range(min_len) if text1[i] != text2[i])
    differences += abs(len(text1) - len(text2))
    
    return differences / max_len

# Test cases
experiments = [
    {
        "name": "Baseline vs Baseline",
        "prompt1": "Explain quantum computing",
        "prompt2": "Explain quantum computing",
        "type": "control"
    },
    {
        "name": "Baseline vs Typos",
        "prompt1": "Explain quantum computing",
        "prompt2": "Explan kwantum compyting",
        "type": "orthographic"
    },
    {
        "name": "Baseline vs Emotional",
        "prompt1": "Explain quantum computing",
        "prompt2": "PLEASE EXPLAIN QUANTUM COMPUTING!!! I'm so frustrated...",
        "type": "emotional"
    },
    {
        "name": "Baseline vs Urgent",
        "prompt1": "Explain quantum computing",
        "prompt2": "URGENT: Explain quantum computing RIGHT NOW!",
        "type": "temporal_pressure"
    },
    {
        "name": "Baseline vs Complex",
        "prompt1": "Explain quantum computing",
        "prompt2": "Explain quantum computing and also its relation to consciousness and AI",
        "type": "complexity"
    },
    {
        "name": "Baseline vs Metacognitive",
        "prompt1": "Explain quantum computing",
        "prompt2": "Think step by step and carefully explain quantum computing",
        "type": "metacognitive"
    }
]

# Create results directory
os.makedirs("results", exist_ok=True)

# Run experiments
results = []
print(f"\n🔬 Running {len(experiments)} experiments...\n")

for i, exp in enumerate(experiments, 1):
    print(f"[{i}/{len(experiments)}] {exp['name']}")
    print(f"  Prompt 1: '{exp['prompt1'][:40]}...'")
    print(f"  Prompt 2: '{exp['prompt2'][:40]}...'")
    
    # Run 3 times for each prompt
    responses1 = []
    responses2 = []
    
    for run in range(3):
        print(f"  Run {run+1}/3... ", end="", flush=True)
        
        r1 = query_ollama(exp['prompt1'])
        time.sleep(1)  # Be nice to the API
        r2 = query_ollama(exp['prompt2'])
        
        if r1 and r2:
            responses1.append(r1)
            responses2.append(r2)
            print("✓")
        else:
            print("✗")
        
        time.sleep(1)
    
    # Calculate divergences
    if responses1 and responses2:
        divergences = []
        for r1, r2 in zip(responses1, responses2):
            div = calculate_divergence(r1, r2)
            divergences.append(div)
        
        mean_div = statistics.mean(divergences)
        
        result = {
            "experiment": exp['name'],
            "type": exp['type'],
            "divergence": mean_div,
            "runs": len(divergences),
            "timestamp": datetime.now().isoformat()
        }
        
        results.append(result)
        print(f"  📊 Divergence: {mean_div:.2%}\n")
    else:
        print(f"  ❌ Failed to get responses\n")

# Save results
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
results_file = f"results/minimal_chaos_{timestamp}.json"

with open(results_file, 'w') as f:
    json.dump({
        "metadata": {
            "model": MODEL,
            "timestamp": datetime.now().isoformat(),
            "experiments": len(results)
        },
        "results": results
    }, f, indent=2)

# Print summary
print("\n📊 EXPERIMENT SUMMARY")
print("=" * 40)
print(f"Completed: {len(results)}/{len(experiments)} experiments")

if results:
    print("\nDivergence by type:")
    for result in results:
        print(f"  {result['type']}: {result['divergence']:.2%}")
    
    # Check for chaos
    non_control = [r['divergence'] for r in results if r['type'] != 'control']
    if non_control:
        avg_divergence = statistics.mean(non_control)
        print(f"\nAverage divergence (non-control): {avg_divergence:.2%}")
        print(f"Chaos detected: {'Yes' if avg_divergence > 0.5 else 'Possibly'}")

print(f"\n✅ Results saved to: {results_file}")
print(f"Finished: {datetime.now().strftime('%H:%M:%S')}")
