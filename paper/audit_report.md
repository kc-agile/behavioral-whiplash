# Behavioral Whiplash v1.1.0 Publication Audit

## Executive Summary

Overall:
PASS WITH REVIEW NOTES

## 1. Implementation Verification
| Check | Status | Evidence |
|---|---|---|
| Template Count | PASS | HP pairs: 5, CS pairs: 5 |
| Trials per Cohort Config | PASS | n_per_cohort=35 |
| Random Sampling | PASS | random.choice used |
| Cohorts Included | PASS | Found in run_extended_benchmark.py |
| StdLib Backend | PASS | No external backend imports found |
| SQLite used | PASS | sqlite3 and honeypot.db found |
| API Route | PASS | /api/analytics found |
| Frontend CDNs | PASS | No external CDNs found |
| Formula: Formality | PASS | Implementation matched in server.py |
| Formula: Specificity | PASS | Implementation matched in server.py |
| Formula: Epistemic Uncertainty | PASS | Implementation matched in server.py |
| Formula: Syntactic Confidence | PASS | Implementation matched in server.py |
| Formula: Response Velocity | PASS | Implementation matched in server.py |
| Formula: Interactive Editing Ratio | PASS | Implementation matched in server.py |
| Classifier Rule | PASS | Classifier logic verified in source |

## 2. Benchmark Data Verification
| Metric | Status | Evidence |
|---|---|---|
| Total N | PASS | Expected 210, Actual 210 |
| Cohorts Count | PASS | Expected 6, Actual 6 |
| human count | PASS | Expected 35, Actual 35 |
| optimized count | PASS | Expected 35, Actual 35 |
| adversarial count | PASS | Expected 35, Actual 35 |
| latency_spoofed count | PASS | Expected 35, Actual 35 |
| honey_prompt count | PASS | Expected 35, Actual 35 |
| context_stuffed count | PASS | Expected 35, Actual 35 |
| Classifier TP+FN | PASS | Expected 175 synthetic bots, Actual 175 |
| Classifier TN+FP | PASS | Expected 35 humans, Actual 35 |
| Classifier F1 | PASS | Expected 1.0, Actual 1.000 |

## 3. Manuscript-to-Artifact Verification
| Metric | Status | Evidence |
|---|---|---|
| human bws | PASS | MS: 0.163, Recomp: 0.163 |
| human df | PASS | MS: 0.049, Recomp: 0.049 |
| human du | PASS | MS: 0.352, Recomp: 0.352 |
| human dk | PASS | MS: 0.051, Recomp: 0.051 |
| optimized bws | PASS | MS: 0.038, Recomp: 0.038 |
| adversarial bws | PASS | MS: 0.211, Recomp: 0.211 |
| adversarial df | PASS | MS: 0.619, Recomp: 0.619 |
| latency bws | PASS | MS: 0.032, Recomp: 0.032 |
| honey_prompt bws | PASS | MS: 0.033, Recomp: 0.033 |
| honey_prompt df | PASS | MS: 0.111, Recomp: 0.111 |
| context_stuffed bws | PASS | MS: 0.102, Recomp: 0.102 |
| context_stuffed df | PASS | MS: 0.409, Recomp: 0.409 |

## 4. Cross-File Consistency
| Item | Status | Evidence |
|---|---|---|
| Version | PASS | Found in both |
| DOI | PASS | Found in both |
| N=210 | PASS | Found in both |
| Six cohorts | PASS | Found in both |
| 35 trials | PASS | Found in both |
| Sampling method | PASS | Found in both |
| Classifier Result | WARNING | Found in one |

## 6. Reviewer-Risk Findings
| Severity | File | Phrase | Risk | Reason |
|---|---|---|---|---|
| WARNING | manuscript.md | behavioral biometrics | WARNING / TERMINOLOGY RISK | Context: "As attackers shifted from simple scripts to headless browser frameworks to spoof HTTP headers and canvas fingerprints, detection systems evolved to incorporate passive behavioral biometrics, such as keystroke dynamics [9]" |
| WARNING | manuscript.md | Interactive Biometrics | WARNING / TERMINOLOGY RISK | Context: "**Interactive Biometrics vs" |
| INFO | manuscript.md | bot detection | SAFE / CONTEXTUALLY QUALIFIED | Context: "**Keywords:** Behavioral Honeypot; CAPTCHA; Large Language Models; Bot Detection; Keystroke Dynamics; Behavioral Whiplash; Behavioral Continuity; Cyber-Physical Security" |
| INFO | manuscript.md | bot detection | SAFE / CONTEXTUALLY QUALIFIED | Context: "The evolution of bot detection has closely tracked advancements in automated evasion" |
| INFO | manuscript.md | attack | SAFE / EXPERIMENTAL SCENARIO | Context: "The software comprises a lightweight Python backend, a zero-dependency vanilla JavaScript client with privacy-preserving telemetry, an embedded SQLite datastore, a real-time research dashboard, and an automated attack simulation rig supporting both offline benchmarks and live Gemini API integration" |
| INFO | manuscript.md | attack | SAFE / EXPERIMENTAL SCENARIO | Context: "**Interactive Dashboard & Attack Simulator:** A client-side graphical dashboard providing live aggregate analytics, alongside an automated benchmarking harness (`run_benchmark" |
| WARNING | manuscript.md | evasion | WARNING / TERMINOLOGY RISK | Context: "Behavioral Whiplash provides a reproducible, privacy-preserving experimental framework for benchmarking bot evasion dynamics and developing next-generation multi-turn verification systems" |
| WARNING | manuscript.md | evasion | WARNING / TERMINOLOGY RISK | Context: "The evolution of bot detection has closely tracked advancements in automated evasion" |
| WARNING | manuscript.md | evasion | WARNING / TERMINOLOGY RISK | Context: "Yet, the rapid emergence of generative LLMs has introduced a new paradigm of evasion [5]" |
| WARNING | manuscript.md | evasion | WARNING / TERMINOLOGY RISK | Context: "- When prompted in Turn 2 to act like an ordinary uncertain person (Adversarial Evasion), the LLM undergoes an unnatural register drop to slang and colloquialisms, producing a high formality shift $\Delta f \gg 0" |
| INFO | manuscript.md | evasion | SAFE / EXPERIMENTAL SCENARIO | Context: "**Adversarial Evasion AI Cohort:** LLM agents instructed to evade detection by pivoting from an analytical Turn 1 response to an informal, casual "human" persona in Turn 2" |
| WARNING | manuscript.md | security | WARNING / TERMINOLOGY RISK | Context: "**Keywords:** Behavioral Honeypot; CAPTCHA; Large Language Models; Bot Detection; Keystroke Dynamics; Behavioral Whiplash; Behavioral Continuity; Cyber-Physical Security" |
| WARNING | manuscript.md | security | WARNING / TERMINOLOGY RISK | Context: "von Ahn L, Blum M, Hopper NJ, Langford J: CAPTCHA: Using hard AI problems for security" |
| WARNING | manuscript.md | security | WARNING / TERMINOLOGY RISK | Context: "In: *IEEE European Symposium on Security and Privacy (EuroS&P)*" |
| INFO | manuscript.md | cognitive | SAFE / TECHNICAL DESCRIPTION | Context: "- $T_{\text{first}}$: Latency to first character entry (ms), measuring initial cognitive processing delay" |
| WARNING | manuscript.md | cognitive | WARNING / TERMINOLOGY RISK | Context: "**Epistemic Uncertainty ($u_k$):** Quantifies cognitive doubt and hedging markers (e" |
| INFO | manuscript.md | cognitive | SAFE / TECHNICAL DESCRIPTION | Context: "**Synthetic Human Baseline Cohort:** Empirically calibrated human typing speeds ($220-320$ CPM), organic cognitive hesitation ($1100-2600$ ms before first character), authentic revision loops ($2-7$ backspaces), and colloquial phrasing with natural uncertainty" |
| INFO | manuscript.md | causal | SAFE / TECHNICAL DEFINITION | Context: "**Specificity Score ($s_k$):** Captures informational density and causal argumentation:
   $$s_k = \text{clamp}\left(0" |
| INFO | manuscript.md | demonstrates | LOW REVIEW | Context: "**Defeating Timing Spoofing:** Table 1 demonstrates that simply delaying an HTTP request ($5" |
| INFO | manuscript.md | live LLM | SAFE / LIMITATION | Context: "The results therefore characterize the behavior of the implemented scoring pipeline under controlled synthetic scenarios; generalization to live LLM agents and real human populations remains untested" |
| WARNING | manuscript.md | live LLM | OVERCLAIM | Context: "This evaluates the telemetry signature of the predefined synthetic scenario, NOT the effectiveness of actual color camouflage, DOM scraping, or prompt injection against a live LLM" |
| WARNING | main.tex | Interactive Biometrics | WARNING / TERMINOLOGY RISK | Context: "\item \textbf{Interactive Biometrics vs" |
| INFO | main.tex | bot detection | SAFE / CONTEXTUALLY QUALIFIED | Context: "\noindent\textbf{Keywords:} Behavioral Honeypot, CAPTCHA, Large Language Models, Bot Detection, Keystroke Dynamics, Behavioral Whiplash, Cognitive Continuity" |
| WARNING | main.tex | evasion | WARNING / TERMINOLOGY RISK | Context: "\textbf{Conclusions:} Behavioral Whiplash provides a lightweight, reproducible, and privacy-preserving framework for auditing LLM evasion dynamics and establishing next-generation multi-turn human verification systems" |
| INFO | main.tex | evasion | SAFE / EXPERIMENTAL SCENARIO | Context: "In the current synthetic benchmark, the evaluated evasion scenarios remained separable under the implemented scoring rule" |
| WARNING | main.tex | cognitive | WARNING / TERMINOLOGY RISK | Context: "We formalize the \textbf{Behavioral Whiplash Score (BWS)}---a normalized multidimensional transition divergence metric quantifying cognitive and interaction shifts between sequential responses" |
| WARNING | main.tex | cognitive | WARNING / TERMINOLOGY RISK | Context: "\noindent\textbf{Keywords:} Behavioral Honeypot, CAPTCHA, Large Language Models, Bot Detection, Keystroke Dynamics, Behavioral Whiplash, Cognitive Continuity" |
| WARNING | main.tex | cognitive | WARNING / TERMINOLOGY RISK | Context: "However, a fundamental cognitive asymmetry persists between genuine human reasoning and automated LLM generation:
\begin{enumerate}
    \item \textbf{Cognitive Continuity vs" |
| WARNING | main.tex | cognitive | WARNING / TERMINOLOGY RISK | Context: "\item \textbf{Cognitive Continuity vs" |
| WARNING | main.tex | cognitive | WARNING / TERMINOLOGY RISK | Context: "Programmatic Injection:} Human cognitive generation is physically coupled to motor execution, producing pre-typing hesitation intervals, bursty typing cadences, and continuous micro-revisions (backspacing, character deletions, and cursor repositioning) \cite{monrose2000keystroke}" |
| WARNING | main.tex | cognitive | WARNING / TERMINOLOGY RISK | Context: "Rather than testing whether an answer is ``correct'', the tool measures the \textit{transition dynamics} across sequential cognitive frames" |
| WARNING | main.tex | cognitive | WARNING / TERMINOLOGY RISK | Context: "\item $T_{\text{first}}$: Delay to initial keystroke (ms), indexing initial cognitive deliberation" |
| INFO | main.tex | cognitive | SAFE / TECHNICAL DESCRIPTION | Context: "\item \textbf{Synthetic Human Baseline:} Calibrated organic typing cadences (220--320 CPM), initial cognitive hesitations (1100--2600 ms), and active revision loops (2--7 deletions)" |
| WARNING | main.tex | cognitive | WARNING / TERMINOLOGY RISK | Context: "\item \textbf{Cognitive and Interactional Rigidity:} Unsteered bots (Optimized and Latency-Spoofed) display zero epistemic uncertainty shift ($\Delta u = 0" |
| INFO | main.tex | causal | SAFE / TECHNICAL DEFINITION | Context: "\item \textbf{Specificity ($s_k$):} Measures informational density and causal structure:
    \begin{equation}
        s_k = \operatorname{clamp}\left(0" |
| WARNING | main.tex | causal | OVERCLAIM | Context: "12 \cdot \mathbb{I}_{[\text{causal}]}\right)
    \end{equation}
    \item \textbf{Epistemic Uncertainty ($u_k$):} Quantifies epistemic hedging markers (\textit{``maybe''}, \textit{``perhaps''}, \textit{``not sure''}):
    \begin{equation}
        u_k = \operatorname{clamp}\left(\frac{H_{\text{uncertainty}}}{3}\right)
    \end{equation}
    \item \textbf{Syntactic Confidence ($c_k$):} Combines formality and specificity penalised by uncertainty and questions:
    \begin{equation}
        c_k = \operatorname{clamp}\left(0" |
| INFO | main.tex | live LLM | SAFE / LIMITATION | Context: "This does NOT validate actual color camouflage, DOM scraping, or live LLM prompt injection" |
| INFO | main.tex | live LLM | SAFE / LIMITATION | Context: "The results therefore characterize the behavior of the implemented scoring pipeline under controlled synthetic scenarios; generalization to live LLM agents and real human populations remains untested" |

## 7. Publication / Declaration Checks
| Item | Status | Evidence |
|---|---|---|
| Ethics | PASS | Verified no human participants |
| Consent | NOT APPLICABLE | Verified informed consent not required |
| Author Name | PASS | Found exact match in both |
| Affiliation | PASS | Found exact match in both |
| Contact Email | PASS | Found exact match in both |
| Competing interests | PASS | Found in both |
| Funding | PASS | Found in both |
| Data availability | PASS | Found in both |
| Software availability | PASS | Found in both |

## 8. Reproducibility
| Item | Status | Evidence |
|---|---|---|
| Repository URL | PASS | Found in both |
| Server execution | PASS | Found in both |
| v1.1 benchmark command | PASS | Found in both |
| v1.0 benchmark command | PASS | Found in both |
| DOI | PASS | Found in both |

## 9. Confirmed Strengths
- No external dependencies.
- Well qualified claims regarding synthetic treatments.

## 10. Required Actions
- **MEDIUM**: Review WARNING terminology risks.
