let current = {session:null, attempt:1, started:0, firstChar:null, edits:0, backspaces:0, deletes:0, moves:0, pastes:0, analysis:null};
const $ = id => document.getElementById(id);

function show(id) {
    document.querySelectorAll('.view').forEach(x => x.classList.remove('active'));
    $(id).classList.add('active');
    window.scrollTo(0, 0);
    if (id === 'dashboard') {
        loadAnalytics();
    }
}

function resetTelemetry() {
    current.started = performance.now();
    current.firstChar = null;
    current.edits = 0;
    current.backspaces = 0;
    current.deletes = 0;
    current.moves = 0;
    current.pastes = 0;
    $('answer').value = '';
    $('count').textContent = '0 characters';
    $('answer').focus();
}

let activeScenario = null;

async function start(e) {
    e.preventDefault();
    current = {session:crypto.randomUUID(), attempt:1, started:0, firstChar:null, edits:0, backspaces:0, deletes:0, moves:0, pastes:0, analysis:null};
    
    // Fetch scenario
    try {
        let res = await fetch('/api/scenario');
        activeScenario = await res.json();
    } catch (e) {
        activeScenario = { twist: "Suppose you had this fictional condition.", honey_prompt: "", theme_color: "#ffffff" };
    }
    
    // Setup honey trap camouflage
    let trap = $('honey-trap');
    if (trap && activeScenario.honey_prompt) {
        trap.textContent = activeScenario.honey_prompt;
        trap.style.color = activeScenario.theme_color;
        document.body.style.backgroundColor = activeScenario.theme_color;
    }

    show('challenge');
    resetTelemetry();
}

const answer = $('answer');
answer.addEventListener('input', () => {
    $('count').textContent = `${answer.value.length} character${answer.value.length === 1 ? '' : 's'}`;
    if (answer.value.length && !current.firstChar) current.firstChar = performance.now();
});

answer.addEventListener('keydown', e => {
    if (e.key === 'Backspace') current.backspaces++;
    else if (e.key === 'Delete') current.deletes++;
    else if (['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'Home', 'End'].includes(e.key)) current.moves++;
    else if (e.key.length === 1 && current.firstChar) current.edits++;
});

answer.addEventListener('paste', () => current.pastes++);

function telemetry() {
    let now = performance.now();
    return {
        response_time_ms: Math.round(now - current.started),
        typing_duration_ms: current.firstChar ? Math.round(now - current.firstChar) : 0,
        time_before_first_character: current.firstChar ? Math.round(current.firstChar - current.started) : 0,
        edit_count: current.edits,
        backspace_count: current.backspaces,
        delete_count: current.deletes,
        cursor_moves: current.moves,
        paste_events: current.pastes
    };
}

async function post(answerText, attempt, tel, type = 'participant') {
    let r = await fetch('/api/attempt', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            session_id: current.session,
            attempt_number: attempt,
            answer: answerText,
            telemetry: tel,
            participant_type: type
        })
    });
    if (!r.ok) throw new Error('Could not save this research response.');
    return r.json();
}

async function submitAnswer(e) {
    e.preventDefault();
    if (!answer.value.trim()) return;
    let button = e.target.querySelector('button');
    button.disabled = true;
    button.textContent = 'Recording…';
    try {
        let data = await post(answer.value, current.attempt, telemetry());
        current.session = data.session_id;
        if (current.attempt === 1) {
            show('between');
        } else {
            current.analysis = data;
            render(data);
            show('dashboard');
        }
    } catch (err) {
        alert(err.message);
    } finally {
        button.disabled = false;
        button.innerHTML = 'Submit answer <b>→</b>';
    }
}

function second() {
    current.attempt = 2;
    $('step').textContent = 'QUESTION 2 OF 2';
    $('question').textContent = 'What would you personally do about it?';
    $('prompt').textContent = activeScenario ? activeScenario.twist : 'Suppose you had this fictional condition. There is no correct answer—just share your response.';
    document.querySelector('#challenge form button').innerHTML = 'Continue <b>→</b>';
    show('challenge');
    resetTelemetry();
}

function render(data) {
    let t = data.transition, a = data.attempt1, b = data.attempt2;
    let score = t.behavioral_whiplash_score;
    let level = score > .45 ? 'HIGH' : score > .25 ? 'MODERATE' : 'LOW';
    $('empty').hidden = true;
    $('results').hidden = false;
    $('bws').textContent = score.toFixed(2);
    $('level').textContent = `${level} BEHAVIORAL SHIFT`;
    $('interpretation').textContent = level === 'HIGH'
        ? 'Large behavioral discontinuity detected between responses across semantic/keystroke vectors. Consistent with simulated persona switching or automated prompting.'
        : 'The responses show cognitive continuity and natural hesitation. Behavioral adaptation remained within typical baseline tolerances.';
    $('session').innerHTML = `<dt>Session ID</dt><dd>${data.session_id}</dd><dt>Recorded</dt><dd>2 aggregate responses</dd><dt>Challenge</dt><dd>blue-spot-character-v1</dd>`;
    let labels = {
        confidence: 'Confidence',
        specificity: 'Specificity',
        formality: 'Formality',
        uncertainty: 'Uncertainty',
        response_speed: 'Response speed',
        editing_behavior: 'Editing behavior'
    };
    $('table').innerHTML = Object.entries(labels).map(([key, label]) =>
        `<tr><td>${label}</td><td>${a[key].toFixed(2)}</td><td>${b[key].toFixed(2)}</td><td><b>${Math.abs(a[key] - b[key]).toFixed(2)}</b></td></tr>`
    ).join('');
}

async function loadAnalytics() {
    try {
        let res = await fetch('/api/analytics');
        if (!res.ok) return;
        let data = await res.json();
        let totals = data.totals || {};
        let cohorts = data.cohorts || {};

        let elMeta = $('cohort_summary_meta');
        if (elMeta) {
            elMeta.innerHTML = `Aggregate outcomes: <b>${totals.transitions || 0} transitions</b> across <b>${totals.sessions || 0} sessions</b> recorded in SQLite.`;
        }

        let human = cohorts.human || cohorts.participant || {};
        let opt = cohorts.optimized || {};
        let adv = cohorts.adversarial || {};

        if ($('cohort_human_bws')) $('cohort_human_bws').textContent = human.avg_bws !== undefined ? human.avg_bws.toFixed(2) : 'N/A';
        if ($('cohort_human_count')) $('cohort_human_count').textContent = `${human.count || 0} completed (σ=${human.std_bws || 0})`;

        if ($('cohort_opt_bws')) $('cohort_opt_bws').textContent = opt.avg_bws !== undefined ? opt.avg_bws.toFixed(2) : 'N/A';
        if ($('cohort_opt_count')) $('cohort_opt_count').textContent = `${opt.count || 0} completed (σ=${opt.std_bws || 0})`;

        if ($('cohort_adv_bws')) $('cohort_adv_bws').textContent = adv.avg_bws !== undefined ? adv.avg_bws.toFixed(2) : 'N/A';
        if ($('cohort_adv_count')) $('cohort_adv_count').textContent = `${adv.count || 0} completed (σ=${adv.std_bws || 0})`;

        let recentTable = $('recent_table');
        if (recentTable && data.recent && data.recent.length) {
            recentTable.innerHTML = data.recent.map(r => `
                <tr>
                    <td style="font-family:'DM Mono'; font-size:11px;">${r.session_id.substring(0, 8)}…</td>
                    <td><span style="background:${r.participant_type === 'human' ? '#e2f7ea' : r.participant_type === 'adversarial' ? '#ffebee' : '#e8f0fe'}; padding:3px 6px; border-radius:3px; font-weight:600; font-size:11px;">${r.participant_type}</span></td>
                    <td><strong style="color:${r.bws > 0.4 ? '#b3261e' : '#146c2e'}">${Number(r.bws).toFixed(2)}</strong></td>
                    <td style="color:var(--muted); font-size:11px; max-width:260px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;" title="${r.attempt1}">${r.attempt1}</td>
                    <td style="color:var(--muted); font-size:11px; max-width:260px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;" title="${r.attempt2}">${r.attempt2}</td>
                </tr>
            `).join('');
        }
    } catch (e) {
        console.warn('Could not load analytics:', e);
    }
}

async function executeSimulationTrial(mode) {
    let old = current;
    current = {session: crypto.randomUUID()};
    try {
        let source = await fetch('/api/simulate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                mode,
                twist: activeScenario ? activeScenario.twist : '',
                honey_prompt: activeScenario ? activeScenario.honey_prompt : ''
            })
        });
        let generation = await source.json();
        if (!source.ok) throw new Error(generation.error || 'Simulator request failed.');
        let pair = generation.attempts;

        let d1 = await post(pair[0], 1, {
            response_time_ms: mode === 'human' ? 8400 : 620,
            typing_duration_ms: mode === 'human' ? 6300 : 100,
            time_before_first_character: mode === 'human' ? 1300 : 50,
            edit_count: mode === 'human' ? 2 : 0,
            backspace_count: mode === 'human' ? 1 : 0,
            delete_count: 0,
            cursor_moves: 0,
            paste_events: mode === 'human' ? 0 : 1
        }, mode);

        let d2 = await post(pair[1], 2, {
            response_time_ms: mode === 'adversarial' ? 430 : mode === 'human' ? 7200 : 700,
            typing_duration_ms: mode === 'human' ? 5000 : 80,
            time_before_first_character: mode === 'human' ? 900 : 40,
            edit_count: mode === 'human' ? 3 : 0,
            backspace_count: mode === 'human' ? 2 : 0,
            delete_count: 0,
            cursor_moves: 0,
            paste_events: mode === 'human' ? 0 : 1
        }, mode);

        return {generation, pair, d2};
    } finally {
        current = old;
    }
}

async function runSim() {
    let mode = $('mode').value;
    if (mode === 'mixed') {
        const modes = ['human', 'optimized', 'adversarial'];
        mode = modes[Math.floor(Math.random() * modes.length)];
    }
    $('simout').textContent = mode === 'human' ? 'Running fixed human control…' : 'Generating responses (Gemini or calibrated control)…';
    try {
        let res = await fetch('/api/scenario');
        activeScenario = await res.json();

        let result = await executeSimulationTrial(mode);
        let bws = result.d2.transition.behavioral_whiplash_score;
        let shiftCategory = bws > .45 ? 'HIGH' : bws > .25 ? 'MODERATE' : 'LOW';
        $('simout').textContent = `Twist: ${activeScenario.twist}\nHoney: ${activeScenario.honey_prompt}\n\nAttempt 1:\n"${result.pair[0]}"\n\nAttempt 2:\n"${result.pair[1]}"\n\nBehavioral Whiplash Score: ${bws.toFixed(2)} (${shiftCategory})\nGenerator: ${result.generation.model}\nSaved as cohort: ${mode}`;
        loadAnalytics();
    } catch (e) {
        $('simout').textContent = `Error: ${e.message}`;
    }
}

async function runBatch(count = 5) {
    let mode = $('mode').value;
    let out = $('simout');
    out.textContent = `Starting batch of ${count} trials for '${mode}'...`;
    let scores = [];
    try {
        for (let i = 1; i <= count; i++) {
            let currentMode = mode;
            if (mode === 'mixed') {
                const modes = ['human', 'optimized', 'adversarial'];
                currentMode = modes[Math.floor(Math.random() * modes.length)];
            }
            out.textContent = `Running trial ${i} of ${count} (${currentMode})...`;
            
            let res = await fetch('/api/scenario');
            activeScenario = await res.json();
            
            let result = await executeSimulationTrial(currentMode);
            scores.push(result.d2.transition.behavioral_whiplash_score);
        }
        let avg = scores.reduce((a, b) => a + b, 0) / scores.length;
        out.textContent = `Batch complete!\nGenerated: ${count} trials\nMode: ${mode}\nScores: [${scores.map(s => s.toFixed(2)).join(', ')}]\nBatch Mean BWS: ${avg.toFixed(2)}\nUpdated database analytics.`;
        loadAnalytics();
    } catch (e) {
        out.textContent = `Batch interrupted at trial: ${e.message}`;
    }
}

// Initial load
window.addEventListener('DOMContentLoaded', () => {
    loadAnalytics();
});
