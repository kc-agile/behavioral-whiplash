# Data Dictionary & FAIR Compliance Guide
**Project:** Behavioral Whiplash CAPTCHA  
**License:** Creative Commons Attribution 4.0 International (CC-BY 4.0)

## Dataset Files
1. `benchmark_results.csv`: Flat tabular file containing individual benchmark sessions.
2. `benchmark_summary.json`: Aggregated statistics, cohort metrics, and ROC-AUC evaluation outputs.
3. `honeypot.db`: Relational SQLite database with full session schemas.

---

## Variable Codebook (`benchmark_results.csv`)

| Field Name | Type | Unit / Range | Description |
| :--- | :--- | :--- | :--- |
| `session_id` | String (UUID) | Unique string | Unique session identifier for each multi-turn challenge trial. |
| `cohort` | String | Categorical | Cohort label: `human`, `optimized`, `adversarial`, or `latency_spoofed`. |
| `is_bot` | Integer | {0, 1} | Binary ground truth label (0 = Human, 1 = Automated Bot). |
| `bws` | Float | [0.0, 1.0] | Behavioral Whiplash Score (arithmetic mean of the 6 shift dimensions). |
| `timing_shift` | Float | [0.0, 1.0] | Absolute divergence in response velocity $\Delta \tau$. |
| `formality_shift` | Float | [0.0, 1.0] | Absolute divergence in linguistic formality register $\Delta f$. |
| `specificity_shift` | Float | [0.0, 1.0] | Absolute divergence in lexical specificity and information density $\Delta s$. |
| `uncertainty_shift` | Float | [0.0, 1.0] | Absolute divergence in epistemic uncertainty/hedging markers $\Delta u$. |
| `confidence_shift` | Float | [0.0, 1.0] | Absolute divergence in syntactic and semantic confidence $\Delta c$. |
| `interaction_shift` | Float | [0.0, 1.0] | Absolute divergence in keystroke editing behavior ratio $\Delta \kappa$. |
| `attempt1_len` | Integer | Characters | Length in characters of Attempt 1 response text. |
| `attempt2_len` | Integer | Characters | Length in characters of Attempt 2 response text. |

---

## SQLite Relational Schema (`honeypot.db`)

### Table `sessions`
- `id` (TEXT, PRIMARY KEY): Unique session UUID.
- `created_at` (TEXT): ISO 8601 UTC timestamp.
- `participant_type` (TEXT): Cohort identifier (`human`, `optimized`, `adversarial`, `latency_spoofed`).
- `challenge_id` (TEXT): Identifier of the cognitive challenge scenario.

### Table `attempts`
- `id` (INTEGER, PRIMARY KEY): Autoincrementing attempt record ID.
- `session_id` (TEXT): Foreign key to `sessions.id`.
- `attempt_number` (INTEGER): Attempt turn number (1 or 2).
- `answer` (TEXT): Free-text response submitted by user/agent.
- `timestamp` (TEXT): ISO 8601 UTC timestamp.
- `response_time_ms` (INTEGER): Total duration from display to submission in milliseconds.
- `typing_duration_ms` (INTEGER): Active typing duration from first character in milliseconds.
- `time_before_first_character` (INTEGER): Pre-first-character cognitive hesitation in milliseconds.
- `character_count` (INTEGER): Raw character count.
- `word_count` (INTEGER): Word count.
- `edit_count` (INTEGER): Printable key edit actions.
- `backspace_count` (INTEGER): Backspace keystroke count.
- `delete_count` (INTEGER): Delete keystroke count.
- `cursor_moves` (INTEGER): Cursor arrow / navigation key event count.
- `paste_events` (INTEGER): DOM paste event count.
- `formality_score` (REAL): Formality score $f \in [0, 1]$.
- `specificity_score` (REAL): Specificity score $s \in [0, 1]$.
- `uncertainty_score` (REAL): Uncertainty score $u \in [0, 1]$.
- `confidence_score` (REAL): Confidence score $c \in [0, 1]$.
- `response_speed` (REAL): Normalized speed $\tau \in [0, 1]$.
- `editing_behavior` (REAL): Editing ratio $\kappa \in [0, 1]$.

### Table `behavioral_transitions`
- `id` (INTEGER, PRIMARY KEY): Transition ID.
- `session_id` (TEXT): Foreign key to `sessions.id`.
- `attempt_from` (INTEGER): Source attempt (1).
- `attempt_to` (INTEGER): Target attempt (2).
- `timing_shift` (REAL): $\Delta \tau$.
- `formality_shift` (REAL): $\Delta f$.
- `specificity_shift` (REAL): $\Delta s$.
- `uncertainty_shift` (REAL): $\Delta u$.
- `confidence_shift` (REAL): $\Delta c$.
- `interaction_shift` (REAL): $\Delta \kappa$.
- `behavioral_whiplash_score` (REAL): BWS composite score.
