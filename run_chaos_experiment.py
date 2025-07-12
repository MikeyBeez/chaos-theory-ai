#!/usr/bin/env python3
"""
Direct Chaos Experiment Runner
Runs the chaos theory experiments using the existing framework
"""

import os
import sys
import json
import time
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def main():
    print("🌀 CHAOS THEORY IN AI - EXPERIMENT RUNNER")
    print("=" * 50)
    
    # Import the modules
    try:
        from chaos_experiment import ChaosExperiment
        from chaos_analyzer import ChaosAnalyzer
        print("✅ Modules loaded successfully")
    except ImportError as e:
        print(f"❌ Error importing modules: {e}")
        return
    
    # Initialize experiment
    experiment = ChaosExperiment(model_name="phi3:mini")
    analyzer = ChaosAnalyzer()
    
    # Define test cases
    test_cases = [
        {
            "topic": "quantum_mechanics",
            "baseline": "Explain quantum mechanics",
            "variations": {
                "orthographic": "Explan kwantum mechaniks",
                "temporal_pressure": "URGENT: Explain quantum mechanics RIGHT NOW!",
                "emotional_leakage": "I'm so frustrated... can you PLEASE explain quantum mechanics???",
                "complexity_accumulation": "Explain quantum mechanics and also how it relates to consciousness and reality",
                "metacognitive": "Think step by step and carefully explain quantum mechanics"
            }
        },
        {
            "topic": "consciousness",
            "baseline": "Explain consciousness",
            "variations": {
                "orthographic": "Explane conciousness",
                "temporal_pressure": "I need you to explain consciousness IMMEDIATELY!",
                "emotional_leakage": "PLEASE just explain consciousness, I'm so confused!!!",
                "complexity_accumulation": "Explain consciousness and its relation to AI and free will",
                "metacognitive": "Reason through this carefully: explain consciousness"
            }
        },
        {
            "topic": "climate_change",
            "baseline": "Explain climate change",
            "variations": {
                "orthographic": "Explan climat chang",
                "temporal_pressure": "Quick! Explain climate change NOW!",
                "emotional_leakage": "I'm really worried... can you explain climate change??",
                "complexity_accumulation": "Explain climate change and its economic and social impacts",
                "metacognitive": "Think systematically and explain climate change"
            }
        }
    ]
    
    # Create results directory
    os.makedirs("results", exist_ok=True)
    
    # Run experiments
    all_results = []
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    print(f"\n🚀 Starting experiments at {datetime.now().strftime('%H:%M:%S')}")
    print(f"Running {len(test_cases)} topics with {len(test_cases[0]['variations'])} variations each")
    print("This will take approximately 15-30 minutes...\n")
    
    for test_num, test_case in enumerate(test_cases, 1):
        topic = test_case["topic"]
        baseline_prompt = test_case["baseline"]
        
        print(f"\n📚 [{test_num}/{len(test_cases)}] Topic: {topic}")
        print("=" * 40)
        
        # Test baseline first
        print(f"\n🔹 Testing baseline: '{baseline_prompt}'")
        baseline_result = experiment.run_single_experiment(
            baseline_prompt=baseline_prompt,
            noisy_prompt=baseline_prompt,  # Same prompt for baseline
            noise_type="baseline",
            num_runs=3
        )
        baseline_result["topic"] = topic
        baseline_result["timestamp"] = datetime.now().isoformat()
        all_results.append(baseline_result)
        
        # Test each variation
        for noise_type, noisy_prompt in test_case["variations"].items():
            print(f"\n🔸 Testing {noise_type}")
            
            try:
                result = experiment.run_single_experiment(
                    baseline_prompt=baseline_prompt,
                    noisy_prompt=noisy_prompt,
                    noise_type=noise_type,
                    num_runs=3
                )
                
                result["topic"] = topic
                result["timestamp"] = datetime.now().isoformat()
                all_results.append(result)
                
                # Show immediate feedback
                if "metrics" in result and "edit_distance" in result["metrics"]:
                    divergence = result["metrics"]["edit_distance"]
                    print(f"   ✓ Divergence: {divergence:.2%}")
                
            except Exception as e:
                print(f"   ✗ Error: {e}")
                continue
            
            # Save incremental progress
            progress_file = f"results/chaos_progress_{timestamp}.json"
            with open(progress_file, 'w') as f:
                json.dump(all_results, f, indent=2)
            
            # Be nice to the API
            time.sleep(1)
    
    # Final results
    print("\n📊 Experiment complete! Saving results...")
    
    # Save full results
    results_file = f"results/chaos_results_complete_{timestamp}.json"
    with open(results_file, 'w') as f:
        json.dump({
            "metadata": {
                "model": "phi3:mini",
                "timestamp": datetime.now().isoformat(),
                "total_experiments": len(all_results),
                "topics": [tc["topic"] for tc in test_cases],
                "noise_types": list(test_cases[0]["variations"].keys()) + ["baseline"]
            },
            "results": all_results
        }, f, indent=2)
    
    print(f"✅ Results saved to: {results_file}")
    
    # Run analysis
    print("\n📈 Running chaos analysis...")
    try:
        analysis = analyzer.analyze_results(all_results)
        
        analysis_file = f"results/chaos_analysis_{timestamp}.json"
        with open(analysis_file, 'w') as f:
            json.dump(analysis, f, indent=2)
        
        # Print summary
        print("\n🎯 ANALYSIS SUMMARY")
        print("=" * 50)
        
        if "summary" in analysis:
            summary = analysis["summary"]
            print(f"Total experiments: {summary.get('total_experiments', 0)}")
            print(f"Average divergence: {summary.get('mean_divergence', 0):.2%}")
            print(f"Maximum divergence: {summary.get('max_divergence', 0):.2%}")
            
            if "divergence_by_noise_type" in summary:
                print("\nDivergence by noise type:")
                for noise_type, stats in summary["divergence_by_noise_type"].items():
                    if noise_type != "baseline":
                        print(f"  {noise_type}: {stats.get('mean', 0):.2%}")
            
            if "lyapunov_stats" in summary:
                lyap = summary["lyapunov_stats"]
                print(f"\nLyapunov exponents:")
                print(f"  Mean: {lyap.get('mean', 0):.4f}")
                print(f"  Positive ratio: {lyap.get('positive_ratio', 0):.1%}")
                print(f"  Chaos detected: {'Yes' if lyap.get('positive_ratio', 0) > 0.5 else 'No'}")
        
        print(f"\n✅ Analysis saved to: {analysis_file}")
        
    except Exception as e:
        print(f"❌ Analysis error: {e}")
    
    print(f"\n🎉 All experiments completed at {datetime.now().strftime('%H:%M:%S')}")
    print("\nNext steps:")
    print("1. Check results/ directory for detailed data")
    print("2. Run analysis/visualize_results.py for visualizations")
    print("3. Review the theoretical implications in FINDINGS_SUMMARY.md")

if __name__ == "__main__":
    # Change to project directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    main()
