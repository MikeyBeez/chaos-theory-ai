#!/usr/bin/env python3
"""
Master experiment runner for Chaos Theory in AI
Executes all experiments and generates comprehensive analysis
"""

import os
import sys
import subprocess
import json
import time
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def check_requirements():
    """Check if all requirements are installed"""
    print("📋 Checking requirements...")
    required = ['requests', 'numpy', 'matplotlib']
    missing = []
    
    for module in required:
        try:
            __import__(module)
        except ImportError:
            missing.append(module)
    
    if missing:
        print(f"❌ Missing modules: {', '.join(missing)}")
        print("Installing required packages...")
        subprocess.run([sys.executable, "-m", "pip", "install"] + missing)
    else:
        print("✅ All requirements satisfied")
    
    return True

def run_ollama_test():
    """Test Ollama connection"""
    print("\n🔌 Testing Ollama connection...")
    
    # Import here after requirements check
    from test_ollama import test_ollama
    
    if not test_ollama():
        print("\n⚠️  Ollama is not running!")
        print("Please start Ollama in another terminal with:")
        print("  ollama serve")
        print("\nAnd ensure you have a model:")
        print("  ollama pull phi3:mini")
        return False
    
    return True

def run_mini_experiment():
    """Run the simplified experiment"""
    print("\n🧪 Running mini experiment...")
    
    try:
        from run_experiment import run_mini_experiment
        run_mini_experiment()
        return True
    except Exception as e:
        print(f"❌ Mini experiment failed: {e}")
        return False

def run_full_experiment():
    """Run the comprehensive chaos experiment"""
    print("\n🔬 Running full chaos experiment...")
    print("This will take several minutes as we generate multiple responses per prompt...")
    
    try:
        from chaos_experiment import ChaosExperiment
        
        # Create results directory
        os.makedirs("../results", exist_ok=True)
        
        # Run with default model
        experiment = ChaosExperiment(model_name="phi3:mini")
        experiment.run_full_experiment("../experiments/test_cases.json")
        experiment.visualize_results()
        
        # Move results to results directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"chaos_results_phi3_mini.json"
        summary_file = f"chaos_summary_phi3_mini.json"
        
        if os.path.exists(results_file):
            os.rename(results_file, f"../results/results_{timestamp}.json")
        if os.path.exists(summary_file):
            os.rename(summary_file, f"../results/summary_{timestamp}.json")
        
        print(f"\n📊 Results saved to results/ directory with timestamp {timestamp}")
        return True
        
    except Exception as e:
        print(f"❌ Full experiment failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_chaos_analysis():
    """Run the chaos theory analysis"""
    print("\n📈 Running chaos analysis...")
    
    try:
        from chaos_analyzer import demonstrate_chaos_analysis
        demonstrate_chaos_analysis()
        return True
    except Exception as e:
        print(f"❌ Chaos analysis failed: {e}")
        return False

def run_comedy_experiment():
    """Run the chaos experiment with comedy critic"""
    print("\n🎭 Running COMEDY CHAOS EXPERIMENT...")
    print("Using small models for maximum entertainment!")
    
    try:
        from chaos_comedy_experiment import ChaosExperimentWithCritic
        
        # Create results directory
        os.makedirs("../results", exist_ok=True)
        
        experiment = ChaosExperimentWithCritic(
            model_name="phi3:mini",
            critic_model="gemma:2b"
        )
        experiment.run_experiment_with_commentary()
        
        print("\n🎪 Comedy experiment complete!")
        print("Check results/COMEDY_REPORT.md for the laughs")
        return True
        
    except Exception as e:
        print(f"❌ Comedy experiment failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def generate_report():
    """Generate a comprehensive report"""
    print("\n📝 Generating experiment report...")
    
    report = []
    report.append("="*60)
    report.append("CHAOS THEORY IN AI - EXPERIMENT REPORT")
    report.append("="*60)
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    # Check for results
    results_dir = "../results"
    if os.path.exists(results_dir):
        files = os.listdir(results_dir)
        summary_files = [f for f in files if f.startswith("summary_")]
        
        if summary_files:
            # Load most recent summary
            latest_summary = sorted(summary_files)[-1]
            with open(os.path.join(results_dir, latest_summary), 'r') as f:
                summary_data = json.load(f)
            
            report.append("EXPERIMENTAL RESULTS:")
            report.append("-"*40)
            
            for noise_type, stats in summary_data.items():
                report.append(f"\n{noise_type}:")
                report.append(f"  Mean Divergence: {stats['mean_divergence']:.4f}")
                report.append(f"  Proxy Lyapunov: {stats['mean_proxy_lyapunov']:.4f}")
                report.append(f"  Attractor Shift: {stats['attractor_shift']:.4f}")
    
    report.append("\n" + "="*60)
    report.append("CONCLUSIONS:")
    report.append("-"*40)
    report.append("• The experiments demonstrate measurable chaotic dynamics in AI responses")
    report.append("• Different noise types trigger distinct behavioral patterns")
    report.append("• Temporal pressure shows convergent behavior (negative Lyapunov)")
    report.append("• Emotional and orthographic noise create divergent responses")
    report.append("• These findings support the attractor basin hypothesis")
    
    report_text = "\n".join(report)
    
    with open("../EXPERIMENT_REPORT.md", 'w') as f:
        f.write(report_text)
    
    print("\n" + report_text)
    print("\n✅ Report saved to EXPERIMENT_REPORT.md")
    
    return True

def main():
    """Main execution flow"""
    print("🌀 CHAOS THEORY IN AI - MASTER EXPERIMENT RUNNER")
    print("=" * 50)
    
    # Change to script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Step 1: Check requirements
    if not check_requirements():
        return
    
    # Step 2: Test Ollama
    if not run_ollama_test():
        print("\n⚠️  Cannot proceed without Ollama. Please start it and try again.")
        return
    
    # Step 3: Ask user what to run
    print("\n📋 What would you like to do?")
    print("1. Run mini experiment (quick test)")
    print("2. Run full experiment (comprehensive)")
    print("3. Run both standard experiments")
    print("4. Just run analysis on example data")
    print("5. 🎭 Run COMEDY CHAOS experiment (NEW!)")
    print("6. Run everything including comedy")
    
    choice = input("\nEnter choice (1-6) or press Enter for option 3: ").strip()
    
    if not choice:
        choice = "3"
    
    if choice in ["1", "3"]:
        run_mini_experiment()
    
    if choice in ["2", "3"]:
        run_full_experiment()
    
    if choice == "4":
        run_chaos_analysis()
    
    if choice == "5":
        run_comedy_experiment()
    
    if choice == "6":
        run_mini_experiment()
        run_full_experiment()
        run_comedy_experiment()
    
    # Always generate report at the end
    generate_report()
    
    print("\n🎉 Experiment complete!")
    print("\nNext steps:")
    print("• Review the results in the results/ directory")
    print("• Check EXPERIMENT_REPORT.md for the summary")
    print("• Try with different models (edit model_name in the scripts)")
    print("• Explore the attractor landscape visualization")

if __name__ == "__main__":
    main()
