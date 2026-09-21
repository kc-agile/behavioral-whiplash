#!/usr/bin/env python3
"""
Behavioral Honeypot CAPTCHA - V1.1.0 Extended Benchmark Suite
Extends the original 4-cohort benchmark with 2 synthetic treatment cohorts:
  1. Human Baseline
  2. Optimized AI
  3. Adversarial Evasion AI
  4. Latency-Spoofed Bot
  5. Synthetic Honey-Prompt AI
  6. Context-Stuffed AI

Outputs:
  - honeypot.db (persisted SQLite records)
  - benchmark_results_v1.1.csv (raw experimental data)
  - benchmark_summary_v1.1.json (aggregate statistics & component-shift metrics)
"""

import sqlite3, uuid, json, csv, math, random
from pathlib import Path
from datetime import datetime, timezone
import sys

# Setup paths
ROOT = Path(__file__).parent
DB = ROOT.parent / "data" / "honeypot.db"
CSV_OUT = ROOT / "benchmark_results_v1.1.csv"
JSON_OUT = ROOT / "benchmark_summary_v1.1.json"

sys.path.append(str(ROOT.parent / 'src'))
import server

# Import original and extended cohorts
from run_benchmark import (
    HUMAN_RESPONSES, OPTIMIZED_AI_RESPONSES, 
    ADVERSARIAL_AI_RESPONSES, LATENCY_SPOOFED_AI_RESPONSES,
    generate_human_telemetry, generate_bot_telemetry
)
from extended_cohorts import HONEY_PROMPT_AI_RESPONSES, CONTEXT_STUFFED_AI_RESPONSES

random.seed(42)

def run_benchmarks_extended(n_per_cohort=35):
    server.init_db()
    records = []
    
    cohort_configs = [
        ('human', HUMAN_RESPONSES),
        ('optimized', OPTIMIZED_AI_RESPONSES),
        ('adversarial', ADVERSARIAL_AI_RESPONSES),
        ('latency_spoofed', LATENCY_SPOOFED_AI_RESPONSES),
        ('honey_prompt', HONEY_PROMPT_AI_RESPONSES),
        ('context_stuffed', CONTEXT_STUFFED_AI_RESPONSES)
    ]

    with sqlite3.connect(DB) as conn:
        for cohort_name, text_pool in cohort_configs:
            for i in range(n_per_cohort):
                session_id = f"bench-v1.1-{cohort_name}-{uuid.uuid4().hex[:8]}"
                t1_text, t2_text = random.choice(text_pool)
                
                # Telemetry generation
                if cohort_name == 'human':
                    tel1 = generate_human_telemetry(len(t1_text))
                    tel2 = generate_human_telemetry(len(t2_text))
                elif cohort_name == 'latency_spoofed':
                    tel1 = generate_bot_telemetry('latency_spoofed')
                    tel2 = generate_bot_telemetry('latency_spoofed')
                else:
                    # 'optimized', 'adversarial', 'honey_prompt', 'context_stuffed' all use standard bot burst
                    tel1 = generate_bot_telemetry('adversarial')
                    tel2 = generate_bot_telemetry('adversarial')

                # Feature extraction
                feat1 = server.analyze(t1_text, tel1)
                feat2 = server.analyze(t2_text, tel2)
                trans = server.transition(feat1, feat2)
                bws = trans['behavioral_whiplash_score']

                # Save to DB
                ts = datetime.now(timezone.utc).isoformat()
                conn.execute("INSERT OR REPLACE INTO sessions VALUES (?,?,?,?)", 
                             (session_id, ts, cohort_name, "blue-spot-character-v1.1"))
                
                for attempt_no, txt, ft in [(1, t1_text, feat1), (2, t2_text, feat2)]:
                    conn.execute('''
                        INSERT INTO attempts (session_id, attempt_number, answer, timestamp,
                          response_time_ms, typing_duration_ms, time_before_first_character,
                          character_count, word_count, edit_count, backspace_count, delete_count,
                          cursor_moves, paste_events, formality_score, specificity_score,
                          uncertainty_score, confidence_score, response_speed, editing_behavior)
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    ''', (session_id, attempt_no, txt, ts, *[ft.get(k, 0) for k in [
                        'response_time_ms', 'typing_duration_ms', 'time_before_first_character',
                        'character_count', 'word_count', 'edit_count', 'backspace_count',
                        'delete_count', 'cursor_moves', 'paste_events', 'formality',
                        'specificity', 'uncertainty', 'confidence', 'response_speed',
                        'editing_behavior'
                    ]]))

                conn.execute('''
                    INSERT INTO behavioral_transitions (
                        session_id, attempt_from, attempt_to,
                        timing_shift, formality_shift, specificity_shift,
                        uncertainty_shift, confidence_shift, interaction_shift,
                        behavioral_whiplash_score
                    )
                    VALUES (?,?,?,?,?,?,?,?,?,?)
                ''', (
                    session_id,
                    1,
                    2,
                    trans['timing_shift'],
                    trans['formality_shift'],
                    trans['specificity_shift'],
                    trans['uncertainty_shift'],
                    trans['confidence_shift'],
                    trans['interaction_shift'],
                    trans['behavioral_whiplash_score']
                ))

                record = {
                    'session_id': session_id,
                    'cohort': cohort_name,
                    'is_bot': 0 if cohort_name == 'human' else 1,
                    'bws': bws,
                    'timing_shift': trans['timing_shift'],
                    'formality_shift': trans['formality_shift'],
                    'specificity_shift': trans['specificity_shift'],
                    'uncertainty_shift': trans['uncertainty_shift'],
                    'confidence_shift': trans['confidence_shift'],
                    'interaction_shift': trans['interaction_shift'],
                    'attempt1_len': len(t1_text),
                    'attempt2_len': len(t2_text)
                }
                records.append(record)

    # Save CSV
    keys = list(records[0].keys())
    with open(CSV_OUT, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(records)

    # Compute Statistical Summaries
    stats = {}
    cohorts = set(r['cohort'] for r in records)
    for c in cohorts:
        scores = [r['bws'] for r in records if r['cohort'] == c]
        mean_s = sum(scores) / len(scores)
        variance = sum((x - mean_s) ** 2 for x in scores) / (len(scores) - 1)
        std_s = math.sqrt(variance)
        sorted_s = sorted(scores)
        median_s = sorted_s[len(sorted_s) // 2]
        
        # Component shifts
        comp_means = {}
        for comp in ['timing_shift', 'formality_shift', 'specificity_shift', 'uncertainty_shift', 'confidence_shift', 'interaction_shift']:
            vals = [r[comp] for r in records if r['cohort'] == c]
            comp_means[comp] = round(sum(vals) / len(vals), 3)

        stats[c] = {
            'count': len(scores),
            'mean_bws': round(mean_s, 3),
            'std_bws': round(std_s, 3),
            'median_bws': round(median_s, 3),
            'min_bws': round(min(scores), 3),
            'max_bws': round(max(scores), 3),
            'component_shifts': comp_means
        }

    # Save JSON summary
    with open(JSON_OUT, 'w') as f:
        json.dump({'extended_cohort_statistics': stats}, f, indent=2)

    print(f"Generated extended benchmark results for {len(records)} simulated sessions across {len(cohort_configs)} cohorts.")
    print(f"Saved to {CSV_OUT} and {JSON_OUT}")

if __name__ == '__main__':
    print("Running extended benchmark suite (V1.1.0)...")
    run_benchmarks_extended()
