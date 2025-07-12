#!/bin/bash
# Start the chaos theory experiments

echo "🌀 CHAOS THEORY IN AI EXPERIMENTS"
echo "================================="
echo ""

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Please run this from the chaos-theory-ai root directory"
    exit 1
fi

# Create necessary directories
mkdir -p results
mkdir -p analysis

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

# Run the master experiment
cd experiments
python3 run_all.py

# Return to root
cd ..

echo ""
echo "✅ Experiment launcher complete!"
echo "Check the results/ directory for outputs"
