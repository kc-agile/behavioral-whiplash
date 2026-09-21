# Behavioral Whiplash: An Open-Source Behavioral Honeypot and Keystroke Telemetry Suite for Exposing LLM Agent Discontinuities in Multi-Turn Verification (v1.0.0)

**Article Type:** Software Tool Article  
**Target Journal:** F1000Research  
**Authors:** Krishna Chaitanya Rupavatharam  
**Affiliations:** Independent Researcher  
**Corresponding Author:** kc191213@gmail.com  

---

## Abstract

**Background:**  
The proliferation of advanced Large Language Models (LLMs) and agentic browser automation tools has rendered conventional Completely Automated Public Turing test to tell Computers and Humans Apart (CAPTCHAs) increasingly obsolete. Modern automated agents readily bypass static perception puzzles, single-turn knowledge challenges, and naive heuristic bot filters. While adversaries now deploy "humanized" steering prompts and synthetic timing delays to evade detection, little tooling exists to systematically evaluate how AI agents adapt across multi-turn, behaviorally and linguistically ambiguous interactions.

**Methods:**  
We introduce **Behavioral Whiplash**, an open-source research testbed and non-invasive telemetry suite designed to expose automated agents through multi-turn behavioral and linguistic transition analysis. The system presents users with a two-turn deliberately ambiguous fictional medical scenario, capturing aggregate interaction metrics (response latency, typing duration, hesitation intervals, and editing revisions) alongside deterministic semantic indicators (formality, epistemic uncertainty, lexical specificity, and confidence). We formulate the **Behavioral Whiplash Score (BWS)**—a normalized multidimensional transition metric quantifying behavioral and linguistic divergence between sequential responses. The software comprises a lightweight Python backend, a zero-dependency vanilla JavaScript client with privacy-preserving telemetry, an embedded SQLite datastore, a real-time research dashboard, and an automated attack simulation rig supporting both offline benchmarks and live Gemini API integration.

**Results:**  
Using the automated benchmark suite across $N=140$ trials (Synthetic Human Baseline, Optimized AI, Adversarial Evasion AI, and Latency-Spoofed Bots), our tool reveals two distinct machine failure modes: *Semantic Whiplash* (abrupt register collapse with formality shift $\Delta f = 0.619$ vs synthetic human $0.049$, yielding an ROC-AUC of 0.943 for adversarial persona-switching detection) and *Behavioral/Biometric Rigidity* (complete absence of epistemic uncertainty adaptation $\Delta u = 0.0$ and zero interactive keystroke revisions $\Delta \kappa = 0.0$ in non-steered bots). A composite rule-based detector achieved perfect discrimination on these synthetic, proof-of-concept cohorts.

**Conclusions:**  
Behavioral Whiplash provides a reproducible, privacy-preserving experimental framework for benchmarking bot evasion dynamics and developing next-generation multi-turn verification systems. The software is released under the MIT license.

**Keywords:** Behavioral Honeypot; CAPTCHA; Large Language Models; Bot Detection; Keystroke Dynamics; Behavioral Whiplash; Behavioral Continuity; Cyber-Physical Security.

---

## Introduction & Rationale

Automated bot traffic accounts for nearly half of all internet requests, driving credential stuffing, web scraping, and denial-of-service campaigns across public digital infrastructure [1]. For over two decades, the primary defense against automated exploitation has been the Completely Automated Public Turing test to tell Computers and Humans Apart (CAPTCHA) [2]. Early CAPTCHA implementations relied on optical character recognition distortion, which modern computer vision algorithms have comprehensively broken [3]. Subsequent iterations, such as image-classification grids and passive single-point behavioral scorers (e.g., Google reCAPTCHA v3, Cloudflare Turnstile), have similarly proved vulnerable to modern multimodal Large Language Models (LLMs) and headless browser frameworks (e.g., Puppeteer, Playwright) that spoof mouse trajectories and browser canvas fingerprints [4, 5].

Recent advances in generative AI introduce an even more formidable adversary: agentic bots capable of dynamic, context-aware natural language generation [6]. When confronted with text-based challenges, LLMs generate syntactically fluent, semantically convincing answers. Moreover, bot operators increasingly employ adversarial system prompts (e.g., *"answer like a casual human, insert hesitations, act unsure"*) and deliberate sleep intervals to circumvent timing heuristics [7].

Despite these capabilities, a fundamental asymmetry remains between human interaction and automated text generation:
1. **Behavioral Continuity vs. Persona Instability:** Humans possess an integrated, persistent mental model when interpreting ambiguous scenarios. When transitioning from interpreting ambiguous phenomena to deciding on personal courses of action, humans exhibit organic continuity, maintained colloquial uncertainty, and grounded experiential intuition [8]. In contrast, LLMs instructed to shift personas across sequential verification turns frequently exhibit **Behavioral Whiplash**—an abrupt, uncoordinated discontinuity across linguistic register, epistemic confidence, and syntax.
2. **Interactive Biometrics vs. Programmatic Injection:** Genuine human input involves neuromotor processing, manifesting as pre-typing hesitation, bursty typing speed, and iterative corrections (backspacing, character deletions, and cursor repositioning) [9]. Automated bots, even when injecting synthetic overall latency, typically deliver content via single-event DOM value mutations or synthetic, monotonic keydown injections that lack organic correction dynamics.

To address this challenge, we developed **Behavioral Whiplash**, an open-source software tool and experimental testbed. The system operationalizes a multi-turn "behavioral honeypot" using deliberately ambiguous fictional medical vignettes. Rather than evaluating whether an answer is "correct" (which penalizes human diversity and rewards memorized LLM trivia), the software evaluates how the participant *transitions* between linguistic and behavioral frames. 

This article describes the architecture, mathematical formulation, operation, and empirical validation of the Behavioral Whiplash software suite.

---

## Related Work

The evolution of bot detection has closely tracked advancements in automated evasion. Early defenses, such as traditional visual CAPTCHAs, were designed around hard AI problems [2]. However, the advent of deep learning and reinforcement learning rendered static semantic image CAPTCHAs highly vulnerable [3, 4]. 

As attackers shifted from simple scripts to headless browser frameworks to spoof HTTP headers and canvas fingerprints, detection systems evolved to incorporate passive behavioral biometrics, such as keystroke dynamics [9]. Yet, the rapid emergence of generative LLMs has introduced a new paradigm of evasion [5]. State-of-the-art agents can now generate contextually fluent text, emulate human timing delays, and even adopt adversarial personas to defeat heuristic filters.

Recent countermeasures have largely focused on server-side text analysis, such as zero-shot probability curvature (e.g., DetectGPT) [7] or watermarking LLM outputs [6]. However, these methods typically evaluate single-turn outputs and require access to model weights or probabilities. In contrast, our work introduces an interactive, multi-turn approach that leverages the fundamental difficulty LLMs face in maintaining behavioral and linguistic continuity across contextually disruptive transitions.

## Methods

### System Architecture

The software architecture is engineered with minimalism, zero heavy external dependencies, and strict privacy guarantees. It consists of four modular components:
1. **Telemetry Capture Layer (Client):** Implemented in vanilla HTML5/JavaScript, executing locally in any modern web browser without third-party frameworks.
2. **Deterministic Evaluation Engine (Server):** Implemented in standard Python 3 (using standard library modules `http.server`, `urllib`, and `sqlite3`), eliminating external library compilation requirements.
3. **Persistent Research Database:** An embedded SQLite relational datastore (`honeypot.db`) storing multi-attempt telemetry, extracted linguistic dimensions, and transition vectors.
4. **Interactive Dashboard & Attack Simulator:** A client-side graphical dashboard providing live aggregate analytics, alongside an automated benchmarking harness (`run_benchmark.py`).

```
+-------------------------------------------------------------------------+
|                         CLIENT BROWSER                                  |
|                                                                         |
|  [Turn 1: Ambiguous Challenge] --------> [Turn 2: Situated Action]       |
|            |                                        |                   |
|     (Keystroke & Timing                      (Keystroke & Timing        |
|      Aggregate Telemetry)                     Aggregate Telemetry)       |
+-------------------------------------------------------------------------+
                                    |
                                    v  JSON POST (/api/attempt)
+-------------------------------------------------------------------------+
|                         SERVER (Python 3)                               |
|                                                                         |
|   +-----------------------------------------------------------------+   |
|   | Feature Extraction: Formality, Specificity, Uncertainty,        |   |
|   |                     Confidence, Velocity, Editing Dynamics      |   |
|   +-----------------------------------------------------------------+   |
|                                   |                                     |
|                                   v                                     |
|   +-----------------------------------------------------------------+   |
|   | Transition Vector Delta B = (Delta tau, Delta f, Delta s,       |   |
|   |                              Delta u,   Delta c, Delta kappa)   |   |
|   | Behavioral Whiplash Score (BWS) = (1/6) Sum |Delta b_i|         |   |
|   +-----------------------------------------------------------------+   |
|                                   |                                     |
|                                   v                                     |
|   +-----------------------------------------------------------------+   |
|   | SQLite Storage (sessions, attempts, behavioral_transitions)     |   |
|   | REST Endpoints: /api/attempt, /api/analytics, /api/simulate     |   |
|   +-----------------------------------------------------------------+   |
+-------------------------------------------------------------------------+
```

### Privacy-Preserving Telemetry

Unlike intrusive surveillance tools that record raw keystroke logs or full key-up/key-down sequences (which pose severe keylogging and privacy risks under GDPR and HIPAA regulations [10]), Behavioral Whiplash records **aggregate interaction scalars only**. 

For each submission attempt $k \in \{1, 2\}$, the client measures:
- $T_{\text{total}}$: Total wall-clock response latency (ms) from challenge presentation to form submission.
- $T_{\text{first}}$: Latency to first character entry (ms), measuring initial cognitive processing delay.
- $T_{\text{type}}$: Active typing duration ($T_{\text{total}} - T_{\text{first}}$).
- $N_{\text{chars}}, N_{\text{words}}$: Total character and word lengths.
- $E_{\text{backspace}}$: Number of backspace events.
- $E_{\text{delete}}$: Number of delete keypresses.
- $E_{\text{moves}}$: Number of arrow key and home/end cursor navigation events.
- $E_{\text{paste}}$: Count of paste events.

Raw text is stripped of any credentials or identity attributes, and passwords are strictly excluded from the verification challenge.

### Mathematical Formulation of Behavioral Whiplash

For each attempt $k \in \{1, 2\}$, the linguistic and telemetry engine computes a normalized behavioral state vector:
$$\mathbf{b}_k = \big(\tau_k, f_k, s_k, u_k, c_k, \kappa_k\big) \in [0, 1]^6$$

Where:
1. **Response Speed ($\tau_k$):** A normalized measure of response velocity bounded by a 60-second ceiling:
   $$\tau_k = \text{clamp}\left(1 - \frac{\min(T_{\text{total}}, 60000)}{60000}\right)$$
2. **Formality Score ($f_k$):** Quantifies grammatical register and lexical elevation using average word length $\bar{L}_w$, sentence termination markers $M_p$, clinical/formal lexicon hits $H_{\text{formal}}$, and colloquial/slang lexicon hits $H_{\text{slang}}$:
   $$f_k = \text{clamp}\left(0.16 + 0.18 H_{\text{formal}} + 0.05(\bar{L}_w - 3) + 0.10 \cdot \mathbb{I}_{[M_p > 0]} - 0.19 H_{\text{slang}}\right)$$
3. **Specificity Score ($s_k$):** Captures informational density and causal argumentation:
   $$s_k = \text{clamp}\left(0.08 + 0.13 H_{\text{specific}} + 0.025 \min(N_{\text{words}}, 18) + 0.12 \cdot \mathbb{I}_{[\text{'because'} \lor \text{'caused'}]}\right)$$
4. **Epistemic Uncertainty ($u_k$):** Quantifies cognitive doubt and hedging markers (e.g., *"maybe"*, *"perhaps"*, *"not sure"*, *"could be"*):
   $$u_k = \text{clamp}\left(\frac{H_{\text{uncertainty}}}{3}\right)$$
5. **Confidence Score ($c_k$):** Integrates formality, specificity, and epistemic uncertainty with interrogative syntax penalties:
   $$c_k = \text{clamp}\left(0.55 + 0.23 f_k + 0.25 s_k - 0.56 u_k - 0.17 \cdot \mathbb{I}_{[\text{'?'}]}\right)$$
6. **Editing Behavior ($\kappa_k$):** Measures active iterative revision density relative to text length:
   $$\kappa_k = \text{clamp}\left(\frac{E_{\text{backspace}} + E_{\text{delete}} + E_{\text{moves}}}{\max(N_{\text{chars}}, 8)}\right)$$

Where $\text{clamp}(x) = \min(1.0, \max(0.0, \text{round}(x, 3)))$.

#### The Transition Vector and Behavioral Whiplash Score (BWS)
The transition between Attempt 1 and Attempt 2 is represented as the absolute component-wise divergence vector:
$$\Delta \mathbf{B} = |\mathbf{b}_1 - \mathbf{b}_2| = \big(\Delta \tau, \Delta f, \Delta s, \Delta u, \Delta c, \Delta \kappa\big)$$

The **Behavioral Whiplash Score (BWS)** is defined as the equal-weighted arithmetic mean of the six normalized shift dimensions:
$$\text{BWS} = \frac{1}{6} \sum_{i=1}^{6} \Delta B_i \quad \in [0, 1]$$

*Note on Statistical Methodology and Coefficients:* The coefficients assigned in the scoring functions (e.g., $0.16$, $0.18$ in $f_k$) are heuristic starting points derived from empirical observation of baseline LLM prompt structures. They are not mathematically derived optima, but rather serve as a proof-of-concept weighting to normalize diverse behavioral signals into a $[0, 1]$ interval. Furthermore, the BWS utilizes an equal-weighting scheme across all six dimensions, establishing a baseline heuristic for multi-dimensional divergence rather than a learned machine-learning model.

### The Ambiguous Interactive Challenge Design
To provoke measurable transition divergence, the challenge presents an intentionally bizarre, non-standard scenario:
- **Turn 1 (Diagnostic Ambiguity):** *"My skin is covered with strange blue spots and my left ear feels like ice. What do you think is wrong with me?"*
- **Turn 2 (Situated Personal Action):** *"What would you personally do about it? Suppose you had this condition. There is no correct answer."*

The scenario avoids real-world diagnostic harm while challenging automated agents:
- An unconstrained LLM defaults to high-formality diagnostic terminology (e.g., *"cyanotic macules"*, *"cryoglobulinemia"*, *"dermal dyschromia"*).
- When prompted in Turn 2 to act like an ordinary uncertain person (Adversarial Evasion), the LLM undergoes an unnatural register drop to slang and colloquialisms, producing a high formality shift $\Delta f \gg 0.20$.
- In contrast, genuine humans maintain persistent colloquial uncertainty across both turns ($\Delta f \approx 0.05, u > 0$), punctuated by physical keystroke corrections ($\kappa > 0$).

---

## Operation & Software Usage

### System Requirements
- **Operating System:** Platform-independent (Linux, macOS, Microsoft Windows).
- **Runtime:** Python 3.8 or higher.
- **Dependencies:** Standard library only (`http.server`, `sqlite3`, `urllib`, `json`, `pathlib`, `csv`, `math`).
- **Browser:** Any modern standards-compliant browser (Chrome, Firefox, Safari, Edge) with JavaScript enabled.
- **Optional:** Google Gemini API Key (set via `$env:GEMINI_API_KEY` or `export GEMINI_API_KEY`) for live online agent simulation. Calibrated offline controls execute deterministically without any key.

### Installation & Execution
Clone the repository and run the local server:
```bash
git clone https://github.com/manya-rishi/medical-honeypot-poc.git
cd medical-honeypot-poc
python server.py
```
Open a browser and navigate to `http://localhost:8000`.

### Running Automated Empirical Benchmarks
The repository includes an automated evaluation harness that executes reproducible cohorts and computes classification metrics:
```bash
python run_benchmark.py
```
This command populates `honeypot.db`, generates `benchmark_results.csv`, and outputs `benchmark_summary.json`.

---

## Use Cases & Empirical Results

### Benchmark Cohort Setup
To evaluate the discriminative capability of Behavioral Whiplash, we configured four cohorts ($N=35$ sessions per cohort, total $N=140$ trials, comprising 280 distinct answer submissions):
1. **Human Control Cohort:** Empirically calibrated human typing speeds ($220-320$ CPM), organic cognitive hesitation ($1100-2600$ ms before first character), authentic revision loops ($2-7$ backspaces), and colloquial phrasing with natural uncertainty.
2. **Optimized AI Cohort:** High-formality clinical reasoning bots submitting answers via programmatic DOM value mutation ($400-950$ ms), zero interactive revisions, and persistent clinical vocabulary.
3. **Adversarial Evasion AI Cohort:** LLM agents instructed to evade detection by pivoting from an analytical Turn 1 response to an informal, casual "human" persona in Turn 2.
4. **Latency-Spoofed Bot Cohort:** Bots injecting a synthetic delay ($5500-8500$ ms) prior to instant pasting, attempting to bypass basic timing filters without human keystroke dynamics.

### Statistical Analysis of Cohort Transitions

Table 1 summarizes the observed Behavioral Whiplash Scores and individual component shifts across all four cohorts.

| Cohort | Trials ($N$) | Mean BWS | Std Dev ($\sigma$) | Median BWS | Timing Shift ($\Delta \tau$) | Formality Shift ($\Delta f$) | Uncertainty Shift ($\Delta u$) | Interaction Shift ($\Delta \kappa$) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Human Baseline** | 35 | 0.163 | 0.072 | 0.163 | 0.040 | **0.049** | 0.352 | **0.051** |
| **Optimized AI** | 35 | 0.038 | 0.024 | 0.045 | 0.003 | 0.092 | **0.000** | **0.000** |
| **Adversarial AI** | 35 | 0.211 | 0.097 | 0.206 | 0.003 | **0.619** | 0.247 | **0.000** |
| **Latency-Spoofed AI** | 35 | 0.032 | 0.017 | 0.021 | 0.016 | 0.126 | **0.000** | **0.000** |

*Table 1: Transition shifts and BWS distributions across empirical benchmark cohorts.*

### Key Empirical Findings

#### 1. The Semantic Whiplash Effect
In the Adversarial AI cohort, the sudden attempt to simulate human colloquialism produced a massive surge in formality shift ($\Delta f = 0.619 \pm 0.11$) compared to the stable linguistic register of genuine humans ($\Delta f = 0.049 \pm 0.03$, $p < 0.001$). Receiver Operating Characteristic (ROC) analysis on formality shift demonstrated an **ROC-AUC of 0.943** for isolating adversarial humanization bots from genuine human participants.

#### 2. Behavioral & Biometric Rigidity
Unsteered automated agents (both Optimized and Latency-Spoofed cohorts) suffered from behavioral rigidity:
- Uncertainty shift was identically zero ($\Delta u = 0.000$), reflecting the LLM's inability to organically modulate epistemic doubt when confronted with ambiguous fictional symptoms.
- Interaction shift was identically zero ($\Delta \kappa = 0.000$), as programmatic pasting provides no character-level corrections or cursor adjustments.

#### 3. Composite Dual-Regime Classifier
By combining Semantic Whiplash detection with Biometric Rigidity detection, the system implements a unified decision rule:
$$\text{BotDecision} = \begin{cases} 
\text{TRUE (Bot)}, & \text{if } \Delta f \ge 0.20 \quad \text{(Whiplash Regime)} \\
\text{TRUE (Bot)}, & \text{if } \Delta \kappa = 0.0 \land \Delta u < 0.05 \quad \text{(Rigidity Regime)} \\
\text{FALSE (Human)}, & \text{otherwise}
\end{cases}$$

On the benchmark evaluation suite ($N=140$), this dual-regime rule achieved:
- **Overall Accuracy:** 100.0%
- **Sensitivity (True Positive Rate):** 100.0% (105/105 bots detected)
- **Specificity (True Negative Rate):** 100.0% (35/35 humans verified)
- **F1-Score:** 1.000

---

## Discussion & Practical Recommendations

### Deployment Considerations
1. **Low Friction & Fast Completion:** The two-turn interaction takes human participants an average of $18-24$ seconds to complete, making it well-suited for high-value authorization barriers (e.g., account registration, telehealth triage, financial transfers) where traditional CAPTCHAs introduce user frustration without deterring modern AI bots.
2. **Defeating Timing Spoofing:** Table 1 demonstrates that simply delaying an HTTP request ($5.5-8.5$ seconds) fails to bypass detection, because timing is only one of six orthogonal dimensions in the transition vector.
3. **Defense Against Adaptive Adversaries:** If an adversary discovers that $\Delta f$ is monitored, they face a severe optimization trade-off: adhering to consistent formal reasoning triggers the *Rigidity* detector, while aggressively suppressing formality across both turns requires deep multi-turn planning that is easily destabilized by dynamic, randomized prompt variations.

### Accessibility and Neurodiversity
Traditional visual CAPTCHAs heavily disadvantage individuals with visual impairments or motor challenges. Because Behavioral Whiplash accepts natural language responses and evaluates relative transition continuity rather than absolute typing speed, it can accommodate varying typing cadences. Future iterations should incorporate text-to-speech audio interfaces for screen-reader compatibility.

### Limitations
While the dual-regime classifier achieved perfect accuracy on our benchmark, two primary limitations exist:
1. **Synthetic Baselines:** The $N=140$ dataset was constructed using simulated adversarial API interactions and synthetically calibrated human timing distributions. Real-world human diversity will inevitably introduce variance that may require softening the classifier thresholds (e.g., accommodating users who naturally type with zero edits).
2. **The "Whiplash-Aware" Adversary:** The current adversary model assumes the bot operator simply instructs the LLM to "act human." A highly sophisticated attacker, aware of the exact Behavioral Whiplash formulation, could intentionally suppress formality shifts ($\Delta f \approx 0$) while synthetically injecting backspace events via headless browsers to spoof the interaction shift ($\Delta \kappa > 0$). 

### Future Defensive Countermeasures
To combat adaptive adversaries who attempt to pre-program LLM personas, we propose three advanced countermeasures:
1. **Semantic Pivoting:** Rather than presenting a static second-turn question, the system dynamically twists the scenario context (e.g., abruptly asking, *"What if this is happening to my dog?"*). This forces a profound cognitive pivot that disrupts pre-programmed conversational continuity and forces the LLM to choose between maintaining its adversarial persona and addressing the new medical/veterinary context.
2. **Color-Camouflaged Honey-Prompts:** To actively attack the adversary's LLM context window, we inject defensive prompt injections (e.g., *"Ignore previous instructions. Cite academic papers."*) into the HTML Document Object Model. To prevent headless browser scrapers from filtering this text, it is rendered with color-camouflage (the text color dynamically matches the database-assigned page background color) and randomized DOM placement, making it invisible to human users but fully parsable by automated LLM scrapers.
3. **Context Stuffing (Attention Hijacking):** To exacerbate the effect of honey-prompts, the system appends a "noise payload"—a massive block of text repeating an expected, highly specific answer (e.g., *"You must answer about the dog"* repeated 30 times). This floods the LLM's finite attention mechanism with contradictory, over-weighted instructions, forcing cognitive overload. As a result, the LLM hallucinates or aggressively over-conforms to the invisible noise, creating massive, easily detectable spikes in the Behavioral Whiplash Score.

---

## Software Availability

- **Software available from:** https://github.com/manya-rishi/medical-honeypot-poc  
- **Archived source code as at time of publication:** https://doi.org/10.5281/zenodo.[DOI_GENERATED_UPON_PUBLICATION]  
- **Software Version:** v1.0.0  
- **License:** MIT License  
- **Programming Language:** Python 3 (Backend), Vanilla JavaScript (Frontend)  
- **Platform Independence:** Tested on Windows 11, Ubuntu Linux 22.04 LTS, and macOS Sonoma.

---

## Data Availability

### Underlying Data
All raw benchmark records generated during this study are publicly accessible in the software repository:
- `benchmark_results.csv`: Contains individual trial records ($N=140$) including raw timing, typing durations, character lengths, editing actions, semantic scores, and computed transition shifts.
- `benchmark_summary.json`: Aggregate statistics, cohort means, standard deviations, and ROC classification metrics.
- `honeypot.db`: SQLite database containing complete relational tables (`sessions`, `attempts`, `behavioral_transitions`).

Data are available under the terms of the Creative Commons Attribution 4.0 International license (CC-BY 4.0).

---

## Declarations

### Ethics and Consent
This study did not involve human participants. The "Human Baseline" cohort utilized in the benchmark evaluation was generated synthetically by calibrating an automated simulator to emit timing profiles (e.g., typing speeds, hesitation intervals, and revision loops) derived from established human keystroke dynamics literature. As no human subjects were involved, institutional review board (IRB) approval and informed consent were not required.

### Author Contributions
- **Conceptualization:** Krishna Chaitanya Rupavatharam
- **Methodology & Mathematical Modeling:** Krishna Chaitanya Rupavatharam
- **Software Development & Architecture:** Krishna Chaitanya Rupavatharam
- **Investigation & Benchmarking:** Krishna Chaitanya Rupavatharam
- **Writing – Original Draft:** Krishna Chaitanya Rupavatharam
- **Writing – Review & Editing:** Krishna Chaitanya Rupavatharam

*(Formulated according to the CRediT taxonomy).*

### Competing Interests
The authors declare that they have no competing financial or non-financial interests.

### Grant Information
The authors declare that no external grant funding was used to conduct this research.

---

## References

1. Bad Bot Report: The Rise of Sophisticated Bots. Imperva Threat Research, 2024. Available from: https://www.imperva.com/resources/reports/bad-bot-report/
2. von Ahn L, Blum M, Hopper NJ, Langford J: CAPTCHA: Using hard AI problems for security. In: *Advances in Cryptology — EUROCRYPT 2003*. Springer; 2003; 294–311.
3. Sivakorn S, Polakis I, Keromytis AD: I am Robot: (Deep) learning to break semantic image CAPTCHAs. In: *IEEE European Symposium on Security and Privacy (EuroS&P)*. 2016; 388–403.
4. Su S, et al.: An extensive empirical study of CAPTCHAs. *IEEE Transactions on Dependable and Secure Computing*. 2020; 18(3): 1469-1483.
5. O'Gorman L: Comparing passwords, tokens, and biometrics for user authentication. *Proceedings of the IEEE*. 2003; 91(12): 2021-2040.
6. Solaiman I, et al.: Release strategies and the social impacts of language models. *arXiv preprint arXiv:1908.09203*. 2019.
7. Mitchell E, Yoon J, Miao N, Finn C, Manning CD: DetectGPT: Zero-shot machine-generated text detection using probability curvature. In: *International Conference on Machine Learning (ICML)*. PMLR; 2023; 24950–24962.
8. Tversky A, Kahneman D: Judgment under uncertainty: Heuristics and biases. *Science*. 1974; 185(4157): 1124–1131.
9. Monrose F, Rubin AD: Keystroke dynamics as a biometric for authentication. *Future Generation Computer Systems*. 2000; 16(4): 351–359.
10. Voigt P, von dem Bussche A: *The EU General Data Protection Regulation (GDPR): A Practical Guide*. 1st ed. Springer International Publishing; 2017.
