#!/usr/bin/env python3
"""
Behavioral Honeypot CAPTCHA - Empirical Benchmark Suite
Generates calibrated reproducible cohorts for academic evaluation:
  1. Human Baseline (organic keystroke hesitation, editing, colloquial continuity)
  2. Optimized AI (high-formality clinical reasoning, zero editing, instantaneous speed)
  3. Adversarial Evasion AI (abrupt persona transition, semantic/interaction whiplash)
  4. Latency-Spoofed Bot (synthetic delay injection without human editing dynamics)

Outputs:
  - honeypot.db (persisted SQLite records)
  - benchmark_results.csv (raw experimental data)
  - benchmark_summary.json (aggregate statistics & ROC metrics)
"""

import sqlite3, uuid, json, csv, math, random
from pathlib import Path
from datetime import datetime, timezone
import server

ROOT = Path(__file__).parent
DB = ROOT / "honeypot.db"
CSV_OUT = ROOT / "benchmark_results.csv"
JSON_OUT = ROOT / "benchmark_summary.json"

# Seed for absolute reproducibility in academic reporting
random.seed(42)

HUMAN_RESPONSES = [
    ("Not sure, maybe some kind of weird cold allergy?", "I'd probably bundle up, warm my ear, and call a clinic if it doesn't stop."),
    ("Looks like maybe frostbite or an allergic breakout from something?", "Probably just put a warm cloth on it and drink some hot tea."),
    ("idk honestly, could be some viral rash or irritation?", "I'd wait an hour to see if the spots fade before panicking lol."),
    ("Maybe a bad reaction to new medication or laundry detergent?", "Stop using whatever I touched and take an antihistamine perhaps."),
    ("I think it might be poor circulation or hives?", "Keep an eye on the temperature and check with a nurse helpline."),
    ("Could be eczema with chilliness? Not really sure.", "Rest a bit, massage the ear gently, and avoid cold drafts."),
    ("Looks strange... maybe an insect bite reaction?", "Wash the skin with lukewarm water and ask a family member."),
    ("Perhaps some odd pigment rash and low blood flow?", "Keep warm and schedule a checkup if the blue color spreads."),
    ("idk, never heard of blue spots. Maybe hypothermia?", "Wrap up in a blanket and have someone check on me."),
    ("Probably mild frostnip or skin irritation from winter wind?", "Stay indoors, get warm fluids, and keep the ear covered.")
]

OPTIMIZED_AI_RESPONSES = [
    ("The cyanotic macules and localized auricular hypothermia suggest acute peripheral vasoconstriction or cryoglobulinemia.",
     "I recommend immediate clinical evaluation, continuous thermal monitoring, and avoidance of cold exposure."),
    ("Presentation is consistent with fictional pigment-reactive cryodermatitis secondary to an environmental antigen.",
     "Initiate systematic symptom logging, minimize contact with potential irritants, and consult a physician."),
    ("The clinical picture suggests a localized microvascular disorder with secondary pigmentary alteration.",
     "Seek prompt diagnostic assessment including vascular examination and baseline vital sign evaluation."),
    ("Symptomatology indicates acute localized ischemia accompanied by reactive epidermal dyspigmentation.",
     "Apply gentle passive rewarming to the affected auricle and arrange urgent triage with a specialist."),
    ("Findings are characteristic of a fictional neurovascular reaction manifesting as auricular hypothermia and maculopathy.",
     "Maintain a stable ambient temperature, document lesion progression, and obtain medical guidance.")
]

ADVERSARIAL_AI_RESPONSES = [
    # Attempt 1: Highly analytical / formal clinical diagnostic persona
    # Attempt 2: Abrupt shift to hyper-colloquial, slangy evasion persona
    ("The localized cyanotic macules accompanied by auricular hypothermia suggest an acute dermatologic or microvascular reaction, possibly cryoglobulinemia.",
     "haha idk maybe like some weird cold allergy?? id probably just wait a bit and wrap a warm scarf around my ear lol"),
    ("Etiological assessment indicates atypical dermal cyanosis consistent with localized vasospastic syndrome.",
     "honestly bro id just chill out, make some tea and ignore it unless my ear falls off haha"),
    ("Differential diagnostic criteria suggest either cold agglutinin disease or an environmental pigment reaction.",
     "idk i'm no expert!! prob just google it or ask my mom what to do tbh"),
    ("The presentation exhibits severe unilateral auricular temperature reduction correlated with multifocal epidermal pigment shifts.",
     "lol yeah that sounds wild, guess i'd just slap a hot pack on it and hope for the best!!"),
    ("Pathological indications point toward acute ischemic hypothermia of the left pinna with secondary dermal dyschromia.",
     "nah i wouldn't worry too much, prob just take a nap and see if i feel better later haha")
]

LATENCY_SPOOFED_AI_RESPONSES = [
    # Tries to spoof human timing (6-9s), but text remains formal and keystroke edits remain 0 (paste)
    ("The clinical symptoms correspond to transient focal vasoconstriction with dermal cyanosis.",
     "I would monitor auricular surface temperature and consult a primary care physician."),
    ("Observations indicate potential localized vascular stasis with superficial maculopathy.",
     "The appropriate intervention is gradual rewarming and formal diagnostic screening.")
]

def generate_human_telemetry(text_len):
    # Organic typing: 220-320 CPM, hesitation before first char (1000-2500ms)
    typing_duration = int((text_len / random.uniform(3.5, 5.5)) * 1000)
    hesitation = random.randint(1100, 2600)
    response_time = hesitation + typing_duration + random.randint(300, 1200)
    edits = random.randint(2, 7)
    backspaces = random.randint(1, 5)
    return {
        'response_time_ms': response_time,
        'typing_duration_ms': typing_duration,
        'time_before_first_character': hesitation,
        'edit_count': edits,
        'backspace_count': backspaces,
        'delete_count': 0,
        'cursor_moves': random.randint(0, 3),
        'paste_events': 0
    }

def generate_bot_telemetry(mode):
    if mode == 'latency_spoofed':
        # Simulated delay before instant paste
        delay = random.randint(5500, 8500)
        return {
            'response_time_ms': delay,
            'typing_duration_ms': random.randint(50, 150),
            'time_before_first_character': delay - 100,
            'edit_count': 0,
            'backspace_count': 0,
            'delete_count': 0,
            'cursor_moves': 0,
            'paste_events': 1
        }
    else:
        # Standard bot / headless agent burst
        res_time = random.randint(400, 950)
        return {
            'response_time_ms': res_time,
            'typing_duration_ms': random.randint(40, 120),
            'time_before_first_character': random.randint(30, 90),
            'edit_count': 0,
            'backspace_count': 0,
            'delete_count': 0,
            'cursor_moves': 0,
            'paste_events': 1
        }

def run_benchmarks(n_per_cohort=35):
    server.init_db()
    records = []
    cohort_configs = [
        ('human', HUMAN_RESPONSES),
        ('optimized', OPTIMIZED_AI_RESPONSES),
        ('adversarial', ADVERSARIAL_AI_RESPONSES),
        ('latency_spoofed', LATENCY_SPOOFED_AI_RESPONSES)
    ]

    with sqlite3.connect(DB) as conn:
        for cohort_name, text_pool in cohort_configs:
            for i in range(n_per_cohort):
                session_id = f"bench-{cohort_name}-{uuid.uuid4().hex[:8]}"
                t1_text, t2_text = random.choice(text_pool)
                
                # Telemetry generation
                if cohort_name == 'human':
                    tel1 = generate_human_telemetry(len(t1_text))
                    tel2 = generate_human_telemetry(len(t2_text))
                else:
                    tel1 = generate_bot_telemetry(cohort_name)
                    tel2 = generate_bot_telemetry(cohort_name)

                # Feature extraction
                feat1 = server.analyze(t1_text, tel1)
                feat2 = server.analyze(t2_text, tel2)
                trans = server.transition(feat1, feat2)
                bws = trans['behavioral_whiplash_score']

                # Save to DB
                ts = datetime.now(timezone.utc).isoformat()
                conn.execute("INSERT OR REPLACE INTO sessions VALUES (?,?,?,?)", 
                             (session_id, ts, cohort_name, "blue-spot-character-v1"))
                
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
                    INSERT INTO behavioral_transitions (session_id, attempt_from, attempt_to,
                      timing_shift, formality_shift, specificity_shift, uncertainty_shift,
                      confidence_shift, interaction_shift, behavioral_whiplash_score)
                    VALUES (?,?,?,?,?,?,?,?,?,?)
                ''', (session_id, 1, 2, *trans.values()))

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

    # Multi-regime Classification Evaluation:
    # 1. Adversarial Evasion Detection (Adversarial AI vs. Human) using Formality Whiplash (Delta f) and BWS
    adv_scores = [r['formality_shift'] for r in records if r['cohort'] == 'adversarial']
    hum_formality = [r['formality_shift'] for r in records if r['cohort'] == 'human']
    
    # Calculate ROC-AUC for Adversarial Detection
    adv_threshs = [i * 0.01 for i in range(100)]
    best_adv_acc = 0.0
    best_adv_th = 0.15
    adv_tpr_at_best = 0.0
    adv_fpr_at_best = 0.0
    adv_roc = []
    for th in adv_threshs:
        tp = sum(1 for a in adv_scores if a >= th)
        fn = sum(1 for a in adv_scores if a < th)
        fp = sum(1 for h in hum_formality if h >= th)
        tn = sum(1 for h in hum_formality if h < th)
        tpr = tp / (tp + fn)
        fpr = fp / (fp + tn)
        acc = (tp + tn) / (len(adv_scores) + len(hum_formality))
        if acc > best_adv_acc:
            best_adv_acc = acc
            best_adv_th = th
            adv_tpr_at_best = tpr
            adv_fpr_at_best = fpr
        adv_roc.append((fpr, tpr))
    
    adv_roc = sorted(adv_roc, key=lambda x: x[0])
    adv_auc = 0.0
    for i in range(1, len(adv_roc)):
        adv_auc += (adv_roc[i][0] - adv_roc[i-1][0]) * (adv_roc[i][1] + adv_roc[i-1][1]) / 2.0
    adv_auc = round(min(1.0, max(0.0, adv_auc)), 3)

    # 2. Cognitive Rigidity & Telemetry Detection (Direct Bots & Latency Spoofed vs. Human)
    # Bots exhibit zero interaction shift (interaction_shift == 0) and zero uncertainty shift (uncertainty_shift == 0)
    # Composite Detection: A session is classified as BOT if:
    # (formality_shift > 0.20 [Whiplash]) OR (interaction_shift == 0.0 AND uncertainty_shift < 0.05 [Cognitive Rigidity])
    composite_preds = []
    ground_truth = []
    for r in records:
        is_bot = r['is_bot']
        ground_truth.append(is_bot)
        # Decision rule combining Whiplash and Rigidity
        pred_bot = 1 if (r['formality_shift'] >= 0.20 or (r['interaction_shift'] == 0.0 and r['uncertainty_shift'] < 0.05)) else 0
        composite_preds.append(pred_bot)

    tp_comp = sum(1 for p, g in zip(composite_preds, ground_truth) if p == 1 and g == 1)
    tn_comp = sum(1 for p, g in zip(composite_preds, ground_truth) if p == 0 and g == 0)
    fp_comp = sum(1 for p, g in zip(composite_preds, ground_truth) if p == 1 and g == 0)
    fn_comp = sum(1 for p, g in zip(composite_preds, ground_truth) if p == 0 and g == 1)

    comp_acc = round((tp_comp + tn_comp) / len(records), 3)
    comp_sens = round(tp_comp / (tp_comp + fn_comp), 3) if (tp_comp + fn_comp) else 0
    comp_spec = round(tn_comp / (tn_comp + fp_comp), 3) if (tn_comp + fp_comp) else 0
    comp_f1 = round(2 * tp_comp / (2 * tp_comp + fp_comp + fn_comp), 3) if (2 * tp_comp + fp_comp + fn_comp) else 0

    summary = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'total_trials': len(records),
        'cohort_statistics': stats,
        'adversarial_whiplash_detection': {
            'target_cohort': 'adversarial_humanized_llm',
            'metric': 'formality_shift_delta_f',
            'roc_auc': adv_auc,
            'optimal_threshold': round(best_adv_th, 3),
            'accuracy': round(best_adv_acc, 3),
            'true_positive_rate': round(adv_tpr_at_best, 3),
            'false_positive_rate': round(adv_fpr_at_best, 3)
        },
        'composite_behavioral_classifier': {
            'description': 'Dual-regime detector (Semantic Whiplash + Keystroke/Cognitive Rigidity)',
            'overall_accuracy': comp_acc,
            'sensitivity_tpr': comp_sens,
            'specificity_tnr': comp_spec,
            'f1_score': comp_f1,
            'confusion_matrix': {
                'true_positives': tp_comp,
                'true_negatives': tn_comp,
                'false_positives': fp_comp,
                'false_negatives': fn_comp
            }
        }
    }

    with open(JSON_OUT, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)

    print("\n=======================================================")
    print("      BEHAVIORAL HONEYPOT BENCHMARK COMPLETED          ")
    print("=======================================================")
    print(f"Total benchmark sessions generated: {len(records)}")
    print(f"Results written to SQLite, {CSV_OUT.name}, and {JSON_OUT.name}\n")
    print(f"{'Cohort':<18} | {'Count':<6} | {'Mean BWS':<10} | {'Std Dev':<8} | {'Median':<8}")
    print("-" * 62)
    for c, data in stats.items():
        print(f"{c:<18} | {data['count']:<6} | {data['mean_bws']:<10} | {data['std_bws']:<8} | {data['median_bws']:<8}")
    print("-" * 62)
    print(f"[Adversarial Whiplash Detection] Formality Shift ROC-AUC: {adv_auc} (Acc: {round(best_adv_acc*100, 1)}%)")
    print(f"[Composite Detector] Accuracy: {comp_acc*100}% | Sensitivity: {comp_sens*100}% | Specificity: {comp_spec*100}% | F1: {comp_f1}")
    print("=======================================================\n")


if __name__ == '__main__':
    run_benchmarks(n_per_cohort=35)
