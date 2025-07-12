# 🌀 Chaos Theory in AI - Experiment Guide

## Quick Start

### 1. Prerequisites

First, ensure you have Ollama installed and running:

```bash
# Install Ollama (if not already installed)
# Visit: https://ollama.ai

# Start Ollama server (in a separate terminal)
ollama serve

# Pull the model we'll use (in another terminal)
ollama pull phi3:mini
```

### 2. Install Python Dependencies

```bash
# From the project root directory
pip install -r requirements.txt
```

### 3. Run the Experiments

**Option A: Interactive Runner (Recommended)**
```bash
python start_experiment.py
```

**Option B: Direct Execution**
```bash
cd experiments
python run_all.py
```

**Option C: Shell Script**
```bash
./run_experiments.sh
```

## What the Experiments Do

1. **Connection Test**: Verifies Ollama is running
2. **Mini Experiment**: Quick test with 3 noise types
3. **Full Experiment**: Comprehensive test of all 6 noise categories
4. **Analysis**: Calculates chaos metrics (Lyapunov exponents, etc.)
5. **Visualization**: Creates plots of attractor basins

## Understanding the Results

### Key Metrics

- **Divergence**: How different responses are (0 = identical, 1 = completely different)
- **Lyapunov Exponent**: Sensitivity to input changes (negative = stable, positive = chaotic)
- **Attractor Shift**: How much the response "personality" changes
- **Kaplan-Yorke Dimension**: Complexity of response space

### Expected Patterns

1. **Temporal Pressure** ("hurry ASAP") → Negative λ, minimal responses
2. **Orthographic Noise** (typos) → Positive λ, simplified explanations
3. **Emotional Leakage** ("I'm frustrated") → High λ, empathetic mode
4. **Complexity Accumulation** (multi-topic) → Low λ, high dimension

## Viewing Results

After running experiments:

```bash
# View summary report
cat EXPERIMENT_REPORT.md

# Visualize results (requires matplotlib)
cd analysis
python visualize_results.py

# Check raw data
ls results/
```

## Troubleshooting

### "Cannot connect to Ollama"
- Ensure `ollama serve` is running
- Check it's on port 11434: `curl http://localhost:11434/api/tags`

### "No module named 'requests'"
- Run: `pip install -r requirements.txt`

### "Model not found"
- Pull the model: `ollama pull phi3:mini`

## Next Steps

1. **Try Different Models**
   - Edit `model_name` in scripts
   - Try: `gemma:2b`, `llama3.2:latest`, etc.

2. **Test Your Own Noise Types**
   - Edit `experiments/test_cases.json`
   - Add new categories and prompts

3. **Analyze Specific Patterns**
   - Use the analysis tools to dig deeper
   - Create custom visualizations

## The Science

This experiment demonstrates that AI language models exhibit:
- **Sensitive dependence on initial conditions** (chaos theory)
- **Multiple stable states** (attractor basins)
- **Measurable dynamics** (Lyapunov exponents)

Small changes in how you phrase a prompt can push the AI into completely different behavioral modes - like the butterfly effect!

## Contributing

Found interesting patterns? Want to add new experiments? PRs welcome!

---

*"Tiny variations... vastly different outcomes."*
