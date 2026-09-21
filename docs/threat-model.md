# Threat Model: AI Evasion Capabilities

This document outlines the threat model for the **Behavioral Whiplash** proof-of-concept, detailing the specific AI evasion tactics we anticipate and how the two-turn context-pivoting honeypot mitigates them.

## The Adversary

The primary adversaries modeled in this system are autonomous agents or bot scripts powered by Large Language Models (LLMs). The goal of the adversary is to successfully complete a multi-turn interaction (e.g., a medical triage form or customer support chat) while appearing completely human, thereby bypassing traditional bot detection mechanisms.

## Attack Vectors & Evasion Profiles

We categorize evasion attempts into three distinct profiles, representing varying levels of sophistication.

### 1. The Optimized Bot
- **Capability:** The agent focuses entirely on task completion and accuracy. It leverages an LLM to generate high-quality, formal responses.
- **Evasion Tactic:** None. It relies on the assumption that valid content is sufficient to pass checks.
- **Vulnerability:** **Interactional Rigidity.** It answers instantaneously (sub-second) with highly clinical language and zero keystroke edits, immediately failing telemetry checks.

### 2. The Latency-Spoofed Bot
- **Capability:** The agent is aware of basic timing-based bot detection. 
- **Evasion Tactic:** It introduces artificial delays (e.g., sleeping for 5-8 seconds) before pasting the LLM's response into the input field to mimic human reading and typing time.
- **Vulnerability:** **Interactional Rigidity.** While the total duration appears human, the internal telemetry (typing duration vs. total time, edit count, backspaces) is completely synthetic. Humans do not hesitate for 8 seconds and then instantaneously input 50 words without a single typo.

### 3. The Adversarial Evasion AI
- **Capability:** The agent is highly sophisticated. It utilizes advanced system prompts designed to mimic human conversational markers (e.g., "use lowercase," "use slang," "express doubt"). 
- **Evasion Tactic:** It attempts to spoof both the semantic tone of a human and (theoretically) the keystroke dynamics. 
- **Vulnerability:** **Behavioral/Linguistic Discontinuity (Semantic Whiplash).** The two-turn honeypot exploits the LLM's inherent statelessness and instruction-following bias. When presented with a hidden, context-altering honey-prompt in Turn 2, the adversarial AI's instructions force it to abruptly pivot its persona to comply. This sudden, massive delta in linguistic formality between Turn 1 and Turn 2 (Semantic Whiplash) exposes its synthetic nature.

## The "Whiplash Dilemma"

The core of our threat mitigation strategy is forcing the adversary into a lose-lose scenario:

1. **Option A:** The adversary instructs the LLM to strictly adhere to a consistent persona regardless of new context. 
   - *Result:* It ignores the honey-prompt, failing the Turing test by demonstrating a lack of contextual awareness.
2. **Option B:** The adversary instructs the LLM to adapt to new context dynamically.
   - *Result:* It complies with the extreme honey-prompt, triggering a massive behavioral discontinuity (Whiplash) that is easily detected.

By shifting the defense from static image recognition (traditional CAPTCHA) to dynamic, multi-turn behavioral analysis, we drastically increase the cost and complexity of building an evasive agent.
