# Chaos Theory in AI Research Project

> Exploring the butterfly effect in artificial intelligence: How small input perturbations create divergent behavioral modes in language models.

## Overview

This project implements empirical tests of chaos theory concepts in AI systems, based on "The Butterfly Effect in AI" paper. We investigate whether language models exhibit measurable chaotic dynamics and distinct attractor basins triggered by different types of input noise.

## Key Research Questions

1. **Do LLMs exhibit chaotic dynamics?** Can we measure sensitivity to initial conditions using proxy Lyapunov exponents?

2. **Are there distinct behavioral attractors?** Do different noise types consistently trigger different response modes?

3. **What is the dimensionality of AI behavior?** Can we estimate the Kaplan-Yorke dimension of response spaces?

4. **How does chaos vary across models?** Do different architectures have different chaos signatures?

## Project Structure

```
chaos-theory-ai/
├── src/                    # Core implementation
│   ├── chaos_experiment.py # Main experiment runner
│   ├── chaos_analyzer.py   # Analysis tools
│   ├── run_experiment.py   # Simplified runner
│   └── test_ollama.py      # Connection tester
├── experiments/            # Test data and configs
│   └── test_cases.json     # Noise type examples
├── docs/                   # Documentation
│   ├── README.md          # Detailed guide
│   └── theory.md          # Mathematical background
├── results/               # Experiment outputs
└── analysis/              # Jupyter notebooks
```

## Quick Start

### Prerequisites

1. **Install Ollama**: https://ollama.ai
2. **Pull a model**: 
   ```bash
   ollama pull phi3:mini
   ```
3. **Start Ollama**:
   ```bash
   ollama serve
   ```
4. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Run Experiments

```bash
# Test connection
npm run test:ollama

# Run mini experiment (quick test)
npm run experiment:mini

# Run full experiment (all noise types)
npm run experiment:full

# Analyze results
npm run analyze
```

## Noise Taxonomy

We test 6 categories of prompt perturbations:

### 1. **Orthographic Noise** 
- Example: "Explan kwantum mechaniks"
- Hypothesis: Triggers simplified explanation mode
- Expected: Moderate positive Lyapunov exponent

### 2. **Temporal Pressure**
- Example: "quick explanation ASAP"  
- Hypothesis: Converges to minimal response
- Expected: Negative Lyapunov exponent

### 3. **Emotional Leakage**
- Example: "I'm so frustrated, help me understand..."
- Hypothesis: Bifurcation between empathy/technical modes
- Expected: High Lyapunov, multiple attractors

### 4. **Complexity Accumulation**
- Example: "Explain X and Y and Z and how they relate..."
- Hypothesis: High-dimensional response space
- Expected: Low Lyapunov, high Kaplan-Yorke dimension

### 5. **Metacognitive Markers**
- Example: "Explain (but make it interesting)"
- Hypothesis: Curated/filtered responses
- Expected: Strange attractors with irregular orbits

### 6. **Stream of Consciousness**
- Example: Rambling, unstructured thoughts
- Hypothesis: Mirror-like behavioral adaptation
- Expected: Variable dynamics

## Theoretical Framework

### Lyapunov Exponent (λ)
Measures divergence rate of nearby trajectories:
```
λ = lim_{t→∞} (1/t) ln|dφᵗ(x₀)/dx|
```

### Kaplan-Yorke Dimension (D_KY)
Estimates fractal dimension of attractor:
```
D_KY = k + (Σᵢ₌₁ᵏ λᵢ)/|λₖ₊₁|
```

### Proxy Measurements
Since we can't compute exact values for LLMs, we use:
- Edit distance for divergence
- Response features for complexity
- Multiple runs for statistical validity

## Contributing

This is active research! Contributions welcome:
- Test with different models
- Propose new noise categories  
- Improve measurement techniques
- Analyze results across scales

## Citations

- Original concept: "The Butterfly Effect in AI" by Micheal Bee
- Chaos theory: Strogatz (2015), "Nonlinear Dynamics and Chaos"
- Lyapunov exponents: Wolf et al. (1985)

## License

MIT - See LICENSE file

---

*"Tiny variations... vastly different outcomes." - Ian Malcolm*
