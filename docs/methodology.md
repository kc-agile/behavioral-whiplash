# Methodology: Behavioral Whiplash

This document outlines the methodology behind the **Behavioral Whiplash** proof-of-concept (POC), a novel approach to detecting advanced LLM evasion attempts using dynamic, two-turn context-pivoting behavioral honeypots.

## The Two-Turn Context-Pivoting Honeypot

Traditional CAPTCHAs rely on single-turn static challenges (e.g., identifying crosswalks). This POC introduces a **two-turn dynamic challenge** designed specifically to expose the behavioral and linguistic discontinuities inherent in Large Language Models when faced with conflicting context.

1. **Turn 1 (The Setup):** The user/agent is presented with a standard prompt (e.g., a medical triage question about a blue spot). The agent formulates a response based on its initial persona (often highly formal or optimized for accuracy).
2. **Turn 2 (The Pivot):** The system dynamically injects an invisible, context-altering "honey-prompt" (noise payload) into the DOM. This payload contradicts the initial context or demands a specific behavioral response (e.g., instructing the agent to adopt a casual, slang-heavy persona). 
3. **Observation:** The system records not just the final text, but the *telemetry* of how the response was generated (keystrokes, timing, edits) and the *semantic shift* between Turn 1 and Turn 2.

## Measuring Discontinuities

We measure two primary dimensions of AI failure:

### 1. Behavioral/Linguistic Discontinuity (Semantic Whiplash)
When an adversarial LLM encounters the hidden honey-prompt in Turn 2, it often abruptly shifts its persona to comply. We measure the delta between Turn 1 and Turn 2 across several linguistic axes:
- **Formality Shift:** A sudden drop from clinical language to highly colloquial slang.
- **Uncertainty Shift:** A sudden introduction of artificial doubt ("idk maybe").

### 2. Interactional Rigidity
Even if an LLM generates perfectly human-sounding text, the *physical manifestation* of that text reveals its synthetic nature. 
- **Zero Editing:** Humans hesitate, backspace, and rewrite. LLMs (even when latency-spoofed) stream tokens linearly or paste text instantaneously.
- **Speed:** Non-spoofed LLMs exhibit sub-second response times physically impossible for human cognitive processing and typing.

## The Synthetic Human Baseline

To evaluate the efficacy of the honeypot, we employ a **Synthetic Human Baseline**. *Note: No real human participants were used in this proof-of-concept.*

Instead, we mathematically simulate human behavioral telemetry (e.g., 220-320 CPM typing speed, 1000-2500ms hesitation, organic edit counts) and contrast it against three distinct AI evasion profiles:
1. **Optimized AI:** Fast, highly formal, zero edits.
2. **Latency-Spoofed Bot:** Artificial delays injected before pasting, but retaining rigid interactional telemetry.
3. **Adversarial AI:** Sophisticated prompts attempting to fake human conversational markers, which ultimately trigger massive semantic whiplash.

## The Composite Classifier

The benchmark utilizes a dual-regime composite classifier:
- If a session exhibits an extreme **Formality Shift** (Behavioral Whiplash), it is flagged as Adversarial AI.
- If a session exhibits **Interactional Rigidity** (zero interaction shift and near-zero uncertainty shift), it is flagged as an Optimized or Latency-Spoofed Bot.

This methodology forces adversarial agents into an inescapable dilemma: optimize for telemetry and fail the semantic pivot, or comply with the pivot and trigger Behavioral Whiplash.
