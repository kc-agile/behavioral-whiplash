# Behavioral Whiplash: Open-Source Behavioral Honeypot & Telemetry Suite (v1.0.0)

A research testbed and non-invasive telemetry suite for evaluating multi-turn LLM agent evasion and behavioral and linguistic discontinuities in human verification challenges.

Accompanies the research paper:  
**"Behavioral Whiplash: An Open-Source Behavioral Honeypot and Keystroke Telemetry Suite for Exposing LLM Agent Discontinuities in Multi-Turn Verification"** (Targeted for *F1000Research Software Tool Articles*).

---

## Quick Start

### 1. Run the Local Research Server
Start the local server (zero external dependencies required):
```powershell
python server.py
```
Open **http://localhost:8000** in your browser.

### 2. Live Gemini API Integration (Optional)
The server defaults to calibrated offline benchmark responses. If you have a Google AI Studio API key, you can enable live generative AI calls:
```powershell
$env:GEMINI_API_KEY = "your-api-key"
$env:GEMINI_MODEL = "gemini-flash-lite-latest"
python server.py
```

### 3. Run Automated Empirical Benchmarks
Generate reproducible evaluation cohorts ($N=140$ trials across Synthetic Human Baseline, Optimized AI, Adversarial Humanized AI, and Latency-Spoofed Bots):
```powershell
python run_benchmark.py
```
Outputs:
- `honeypot.db`: SQLite database storing sessions, attempts, and transition metrics.
- `benchmark_results.csv`: Flat tabular dataset for statistical analysis.
- `benchmark_summary.json`: Summary statistics, cohort means, and ROC-AUC classification results.

---

## Repository Structure

```
├── server.py                 # Lightweight Python 3 HTTP server & linguistic analysis engine
├── index.html                # Client interface (Login demo, Honeypot challenge, Dashboard, Simulator)
├── app.js                    # Client-side telemetry capture & live analytics loader
├── style.css                 # Clean, responsive research UI styling
├── run_benchmark.py          # Automated multi-cohort empirical benchmark harness
├── honeypot.db               # Embedded SQLite research database
├── data/
│   ├── benchmark_results.csv # Raw empirical benchmark dataset (N=140)
│   └── benchmark_summary.json# Aggregate statistical metrics & ROC performance
└── paper/
    ├── paper_draft.md        # Full submission-ready F1000Research Software Tool Article
    ├── main.tex              # Compile-ready LaTeX manuscript
    ├── references.bib        # BibTeX bibliography
    └── DATA_DICTIONARY.md    # FAIR-compliant dataset codebook & database schema
```

---

## Core Concept: Behavioral Whiplash Score (BWS)

Instead of relying on single-shot trivia or easily spoofed visual puzzles, Behavioral Whiplash evaluates **transition divergence** across a two-turn ambiguous behavioral honeypot.

For each submission, the engine extracts a 6-dimensional normalized vector:
$$\mathbf{b} = (\tau, f, s, u, c, \kappa)$$
- $\tau$: Response Velocity (bounded by 60s ceiling)
- $f$: Formality & Register Elevation
- $s$: Specificity & Informational Density
- $u$: Epistemic Uncertainty & Hedging Markers
- $c$: Syntactic Confidence
- $\kappa$: Interactive Keystroke Revision Ratio

The **Behavioral Whiplash Score (BWS)** is the composite mean:
$$\text{BWS} = \frac{1}{6} \sum_{i=1}^{6} |\mathbf{b}_1 - \mathbf{b}_2|$$

### Key Empirical Findings
1. **Semantic Whiplash:** Adversarial LLMs attempting to sound like casual humans in Turn 2 produce an abrupt register collapse ($\Delta f = 0.619$ vs. human $0.049$), yielding an **ROC-AUC of 0.943**.
2. **Interactional Rigidity:** Non-steered bots exhibit zero epistemic modulation ($\Delta u = 0.0$) and zero interactive keystroke revisions ($\Delta \kappa = 0.0$).
3. **Composite Detector:** A dual-regime rule combining Semantic Whiplash and Interactional Rigidity achieved **100% classification accuracy** on the $N=140$ synthetic benchmark cohorts. This result should not be interpreted as an estimate of real-world human/bot detection accuracy; the benchmark cohorts are simulated.

---

## Privacy & Security Guarantees
- **No Keystroke Logging:** Raw text input is analyzed for aggregate metrics only; individual keyup/keydown timing logs and passwords are never recorded or stored.
- **Zero PII:** No user accounts, credentials, or personal tracking tokens are used.
- **Harmless Fictional Vignette:** The scenario uses an overtly fictional cartoon ailment to prevent real-world medical misinformation.

---

## License
Distributed under the **MIT License**. Dataset distributed under **CC-BY 4.0**.
