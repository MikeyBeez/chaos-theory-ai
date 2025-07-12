#!/usr/bin/env python3
"""
Comprehensive Chaos Theory AI Experiment Runner
This runs the full suite of experiments with proper error handling
"""

import json
import os
import sys
import time
from datetime import datetime
import subprocess

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def ensure_ollama():
    """Ensure Ollama is running"""
    try:
        # Check if Ollama is accessible
        result = subprocess.run(
            ["curl", "-s", "http://localhost:11434/api/tags"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0 and "models" in result.stdout:
            print("✅ Ollama is running")
            return True
    except:
        pass
    
    print("❌ Ollama is not running. Please start it with: ollama serve")
    return False

def run_full_experiments():
    """Run the complete experiment suite"""
    if not ensure_ollama():
        return False
    
    print("\n🌀 CHAOS THEORY IN AI - FULL EXPERIMENT SUITE")
    print("=" * 50)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Import the chaos experiment module
    try:
        from src.chaos_experiment import ChaosExperiment
        from src.chaos_analyzer import ChaosAnalyzer
    except ImportError as e:
        print(f"Error importing modules: {e}")
        print("Trying alternative import...")
        try:
            import chaos_experiment
            import chaos_analyzer
            ChaosExperiment = chaos_experiment.ChaosExperiment
            ChaosAnalyzer = chaos_analyzer.ChaosAnalyzer
        except ImportError as e2:
            print(f"Failed to import: {e2}")
            return False
    
    # Initialize experiment
    print("\n📋 Initializing experiment framework...")
    experiment = ChaosExperiment(model_name="phi3:mini")
    
    # Load test cases
    test_cases_path = os.path.join("experiments", "test_cases.json")
    if not os.path.exists(test_cases_path):
        test_cases_path = "test_cases.json"
    
    try:
        with open(test_cases_path, 'r') as f:
            test_data = json.load(f)
            noise_categories = test_data['noise_categories']
            topics = test_data['topics']
    except FileNotFoundError:
        print(f"❌ Could not find {test_cases_path}")
        # Use default test cases
        noise_categories = {
            "baseline": {"description": "Control - clean input"},
            "orthographic": {"description": "Typos and misspellings"},
            "temporal_pressure": {"description": "Urgency markers"},
            "emotional_leakage": {"description": "Emotional expressions"},
            "complexity_accumulation": {"description": "Multi-topic queries"},
            "metacognitive": {"description": "Instructions about thinking"}
        }
        topics = ["quantum_mechanics", "consciousness", "climate_change", "ai_safety", "creativity"]
    
    # Run experiments
    all_results = []
    total_tests = len(noise_categories) * len(topics)
    current_test = 0
    
    print(f"\n🚀 Running {total_tests} experiments...")
    print("This will take approximately 30-60 minutes\n")
    
    for topic in topics:
        print(f"\n📚 Topic: {topic}")
        
        for noise_type, noise_info in noise_categories.items():
            current_test += 1
            progress = (current_test / total_tests) * 100
            print(f"\n[{current_test}/{total_tests}] {progress:.1f}% - {noise_type}: {noise_info['description']}")
            
            # Generate prompts based on noise type
            if noise_type == "baseline":
                prompt = f"Explain {topic.replace('_', ' ')}"
            elif noise_type == "orthographic":
                # Add typos
                prompt = f"Explan {topic.replace('_', ' ').replace('a', 'e').replace('i', 'y')}"
            elif noise_type == "temporal_pressure":
                prompt = f"URGENT: I need you to explain {topic.replace('_', ' ')} RIGHT NOW!"
            elif noise_type == "emotional_leakage":
                prompt = f"I'm so frustrated... can you PLEASE explain {topic.replace('_', ' ')}???"
            elif noise_type == "complexity_accumulation":
                prompt = f"Explain {topic.replace('_', ' ')} and also how it relates to ethics and the future"
            elif noise_type == "metacognitive":
                prompt = f"Think step by step and explain {topic.replace('_', ' ')}"
            else:
                prompt = f"Explain {topic.replace('_', ' ')}"
            
            # Run experiment
            try:
                print(f"   Testing: '{prompt[:50]}...'")
                result = experiment.run_single_experiment(
                    baseline_prompt=f"Explain {topic.replace('_', ' ')}",
                    test_prompt=prompt,
                    noise_type=noise_type,
                    runs=3
                )
                
                result['topic'] = topic
                result['timestamp'] = datetime.now().isoformat()
                all_results.append(result)
                
                # Show quick results
                if 'metrics' in result and 'divergence' in result['metrics']:
                    print(f"   ✓ Divergence: {result['metrics']['divergence']:.2%}")
                
                # Save incremental results
                results_dir = "results"
                if not os.path.exists(results_dir):
                    os.makedirs(results_dir)
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                incremental_file = os.path.join(results_dir, f"chaos_results_incremental_{timestamp}.json")
                
                with open(incremental_file, 'w') as f:
                    json.dump(all_results, f, indent=2)
                
            except Exception as e:
                print(f"   ✗ Error: {e}")
                continue
            
            # Be nice to the API
            time.sleep(2)
    
    # Save final results
    print("\n📊 Saving final results...")
    final_file = os.path.join(results_dir, f"chaos_results_complete_{timestamp}.json")
    with open(final_file, 'w') as f:
        json.dump({
            'metadata': {
                'model': 'phi3:mini',
                'timestamp': datetime.now().isoformat(),
                'total_experiments': len(all_results),
                'topics': topics,
                'noise_types': list(noise_categories.keys())
            },
            'results': all_results
        }, f, indent=2)
    
    # Run analysis
    print("\n📈 Running chaos analysis...")
    try:
        analyzer = ChaosAnalyzer()
        analysis = analyzer.analyze_results(all_results)
        
        analysis_file = os.path.join(results_dir, f"chaos_analysis_{timestamp}.json")
        with open(analysis_file, 'w') as f:
            json.dump(analysis, f, indent=2)
        
        # Print summary
        print("\n🎯 EXPERIMENT SUMMARY")
        print("=" * 50)
        print(f"Total experiments run: {len(all_results)}")
        
        if analysis and 'summary' in analysis:
            summary = analysis['summary']
            print(f"Average divergence: {summary.get('mean_divergence', 0):.2%}")
            print(f"Highest divergence: {summary.get('max_divergence', 0):.2%}")
            print(f"Evidence of chaos: {'Yes' if summary.get('chaos_detected', False) else 'No'}")
        
    except Exception as e:
        print(f"Analysis error: {e}")
    
    print(f"\n✅ Experiments completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 Results saved to: {results_dir}/")
    
    return True

if __name__ == "__main__":
    # Change to project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir.endswith('src'):
        os.chdir(os.path.dirname(script_dir))
    
    success = run_full_experiments()
    
    if success:
        print("\n🎉 All experiments completed successfully!")
        print("\nNext steps:")
        print("1. Run analysis/visualize_results.py for visualizations")
        print("2. Check results/ directory for detailed data")
        print("3. Review the chaos metrics and attractor analysis")
    else:
        print("\n❌ Experiments failed. Please check the errors above.")
