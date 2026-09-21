# Reproducibility Guide

This document provides instructions on how to reproduce the benchmark data and statistical findings presented in the Behavioral Whiplash research repository.

## The Synthetic Human Baseline

**Crucial Note on Ethics and Data:** 
As detailed in the manuscript, this proof-of-concept relies entirely on a **Synthetic Human Baseline**. **No real human participants were involved in generating this data.** 

The human cohort data is generated using a mathematically calibrated telemetry function (`generate_human_telemetry` in `benchmark/run_benchmark.py`) that simulates organic human typing patterns, including:
- Typing speeds between 220-320 CPM (Characters Per Minute).
- Pre-typing hesitation (1000-2500ms).
- Organic edit and backspace injection (simulating typos and corrections).

## Reproducing the Benchmark Results

The benchmark suite generates 140 trials across four distinct cohorts (35 trials each). The script is seeded (`random.seed(42)`) to ensure absolute reproducibility.

### Prerequisites
Ensure you have Python 3.8+ installed. The benchmark relies solely on standard library modules (e.g., `sqlite3`, `json`, `csv`, `math`). No external pip dependencies are required for the benchmark script itself.

### Execution

1. Navigate to the root directory of the repository in your terminal.
2. Execute the benchmark script:
   ```bash
   python benchmark/run_benchmark.py
   ```

### Verifying Outputs

Running the script will completely regenerate the baseline data and output three artifacts:

1. **`data/honeypot.db`**: A SQLite database containing the raw session telemetry, individual attempt data, and calculated transition scores.
2. **`benchmark/benchmark_results.csv`**: A flattened CSV export of the database, providing a tabular view of the behavioral whiplash scores and component shifts for every trial.
3. **`benchmark/benchmark_summary.json`**: A JSON payload containing the aggregate statistics, standard deviations, and the final ROC-AUC performance metrics for the composite detector.

### Validating Claims

You can validate the primary claims of the manuscript by reviewing the console output or the `benchmark_summary.json`:
- **Adversarial Whiplash Detection:** The Formality Shift ROC-AUC should read 0.943.
- **Composite Detector Accuracy:** The combination of Semantic Whiplash and Interactional Rigidity detection should yield an accuracy of 100.0%. 

*Note: The 100% detection rate is a result of the constrained parameters of this proof-of-concept simulator. Real-world deployment would exhibit varying accuracy depending on the sophistication of the live adversaries and organic human noise.*
