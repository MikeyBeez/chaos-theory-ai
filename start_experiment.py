#!/usr/bin/env python3
"""
Direct experiment executor - Run this to start the chaos experiments
"""

import subprocess
import sys
import os
import time

def main():
    print("🌀 INITIATING CHAOS THEORY IN AI EXPERIMENTS")
    print("=" * 50)
    print()
    
    # Check if we're in the project directory
    if not os.path.exists("package.json"):
        print("❌ Please run this from the chaos-theory-ai directory")
        return
    
    print("📋 Pre-flight checks:")
    print("  • Python version:", sys.version.split()[0])
    print("  • Working directory:", os.getcwd())
    
    # Install requirements if needed
    print("\n📦 Checking Python dependencies...")
    try:
        import requests
        import numpy
        print("  ✅ Core dependencies available")
    except ImportError:
        print("  ⚠️  Installing dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Instructions for Ollama
    print("\n🤖 Ollama Setup:")
    print("  Before running experiments, ensure Ollama is running:")
    print("  1. Open a new terminal")
    print("  2. Run: ollama serve")
    print("  3. In another terminal, run: ollama pull phi3:mini")
    print()
    
    input("Press Enter when Ollama is ready (or Ctrl+C to cancel)...")
    
    # Run the experiment
    print("\n🚀 Starting experiments...")
    os.chdir("experiments")
    
    try:
        result = subprocess.run([sys.executable, "run_all.py"], 
                              capture_output=False, 
                              text=True)
        
        if result.returncode == 0:
            print("\n✅ Experiments completed successfully!")
        else:
            print("\n❌ Experiments encountered an error")
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Experiments interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    os.chdir("..")
    
    print("\n📊 Results location: ./results/")
    print("📝 Report location: ./EXPERIMENT_REPORT.md")

if __name__ == "__main__":
    main()
