# Chaos Theory in AI Experiment

This experiment explores the concepts from "The Butterfly Effect in AI: Why Your Typos Make ChatGPT Think You're Either Einstein or a Toddler" by demonstrating how different types of noise in prompts create divergent responses in language models.

## Theory Background

The paper proposes that LLMs exhibit chaotic dynamics with measurable sensitivity to input perturbations. Key concepts:

### 1. **Lyapunov Exponent** (λ)
- Measures how fast nearby trajectories diverge in a dynamical system
- Formula: `λ = lim_{t→∞} (1/t) ln|dφᵗ(x₀)/dx|`
- Positive λ = chaotic behavior
- Negative λ = stable/converging behavior

### 2. **Kaplan-Yorke Dimension** (D_KY)
- Measures the fractal dimension of the attractor
- Formula: `D_KY = k + (Σᵢ₌₁ᵏ λᵢ)/|λₖ₊₁|`
- Higher dimension = more complex behavior patterns

### 3. **Attractor Basins**
Different noise types push the AI into different "personality modes":
- **Orthographic Noise** → Simplified explanation mode
- **Temporal Pressure** → Emergency/concise mode
- **Emotional Leakage** → Empathetic/therapy mode
- **Complexity Accumulation** → Professor mode
- **Metacognitive Markers** → Curated/engaging mode

## Experiment Structure

```
chaos_ai_experiment/
├── test_cases.json          # Baseline and noisy prompts
├── chaos_experiment.py      # Main experiment runner
├── chaos_analyzer.py        # Chaos theory analysis tools
├── run_experiment.py        # Simplified experiment runner
└── test_ollama.py          # Ollama connection tester
```

## Running the Experiment

### Prerequisites
1. Install Ollama: https://ollama.ai
2. Pull a model: `ollama pull phi3:mini`
3. Start Ollama: `ollama serve`
4. Install Python dependencies: `pip install requests numpy`

### Quick Test
```bash
# Test Ollama connection
python test_ollama.py

# Run simplified experiment
python run_experiment.py

# View chaos analysis demonstration
python chaos_analyzer.py
```

### Full Experiment
```bash
# Run complete experiment with all noise types
python chaos_experiment.py
```

This will:
1. Test 5 different noise types across 5 topics
2. Generate 3 responses per prompt for statistical validity
3. Calculate divergence metrics and proxy Lyapunov exponents
4. Measure attractor basin stability
5. Generate visualizations and summary statistics

## Interpreting Results

### Divergence Scale
- 0.0 = Identical responses
- 0.5 = Moderately different
- 1.0 = Completely different

### Lyapunov Exponent
- λ < 0: Stable (responses converge)
- 0 < λ < 0.5: Weakly chaotic
- 0.5 < λ < 1.0: Moderately chaotic
- λ > 1.0: Strongly chaotic

### Expected Patterns
Based on the paper's hypothesis:
- **Temporal Pressure**: Low λ (negative), responses converge to minimal
- **Orthographic Noise**: Moderate positive λ, shifts to simpler attractor
- **Emotional Leakage**: High λ, bifurcation between support/technical modes
- **Complexity Accumulation**: Low λ but high dimension, explores more of knowledge space

## Key Insights

The experiment demonstrates that:
1. Small prompt variations create measurably different response patterns
2. Different noise types activate distinct "behavioral attractors"
3. These dynamics can be quantified using chaos theory metrics
4. Understanding these patterns enables better prompt engineering

## Extensions

- Test with different models (GPT, Claude, Llama, etc.)
- Measure response time variations
- Analyze semantic embeddings for deeper divergence metrics
- Build adaptive systems that recognize and compensate for noise types

## References

- Original paper: "The Butterfly Effect in AI" by Micheal Bee
- Chaos Theory: Strogatz, S. H. (2015). Nonlinear dynamics and chaos
- Lyapunov Exponents: Wolf, A., et al. (1985). "Determining Lyapunov exponents from a time series"
