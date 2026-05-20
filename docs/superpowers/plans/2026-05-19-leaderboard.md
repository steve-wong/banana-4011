# Leaderboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the end screen with a leaderboard showing community scores (Supabase) and personal best history (localStorage), with optional score posting.

**Architecture:** Add `#leaderboard-screen` (replacing `#end-screen`) with CSS in `style.css` and JS in `index.html`'s script block. `endGame()` calls `showLeaderboard()` which records the game, renders the active tab, and shows the screen. Supabase JS SDK loaded via CDN; credentials stored as constants at the top of the script block.

**Tech Stack:** Vanilla HTML/CSS/JS, Supabase JS SDK v2 (CDN), localStorage

---

## File Map

| File | Change |
|---|---|
| `index.html` | Remove `#end-screen`; add `#leaderboard-screen` HTML; add Supabase CDN `<script>` tag; add all leaderboard JS |
| `style.css` | Append leaderboard + settings toggle styles |

---

### Task 1: Add `#leaderboard-screen` HTML

**Files:**
- Modify: `index.html:132-142` (replace `#end-screen` block)

- [ ] **Step 1: Replace `#end-screen` with `#leaderboard-screen`**

In `index.html`, remove the entire `<!-- END SCREEN -->` block (lines 132–142) and replace with:

```html
  <!-- LEADERBOARD SCREEN -->
  <div id="leaderboard-screen" class="screen">
    <h1>Banana 4011</h1>
    <p class="tagline">Game over</p>
    <div class="lb-score" id="lb-score">0</div>
    <div class="lb-stats" id="lb-stats"></div>

    <div class="lb-tabs">
      <button class="lb-tab" id="tab-community" onclick="switchLbTab('community')">Community</button>
      <button class="lb-tab" id="tab-personal" onclick="switchLbTab('personal')">Personal best</button>
    </div>

    <div class="lb-table-wrap">
      <div class="lb-table-header">
        <span class="lb-col-rank">#</span>
        <span class="lb-col-name">Name</span>
        <span class="lb-col-score">Score</span>
      </div>
      <div id="lb-rows"></div>
      <div class="lb-error" id="lb-error" style="display:none"></div>
    </div>

    <div id="lb-post-area" class="lb-post-area">
      <div class="lb-post-row" id="lb-post-row">
        <input type="text" id="lb-name-input" class="lb-name-input" placeholder="Your name" maxlength="20">
        <button class="lb-post-btn" id="lb-post-btn" onclick="postScore()">Post score</button>
        <button class="btn secondary lb-home-btn" onclick="showStart()">Home</button>
      </div>
      <div class="lb-skip-wrap" id="lb-skip-wrap">
        <button class="text-btn" onclick="skipLeaderboard()">skip leaderboard</button>
      </div>
    </div>

    <button class="btn lb-play-btn" onclick="startGame()">Play Again</button>
  </div>
```

- [ ] **Step 2: Verify no console errors**

Open `index.html` in a browser. The leaderboard screen is hidden (not `.active`) — no JS errors should appear in the console.

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "Add #leaderboard-screen HTML, remove #end-screen"
```

---

### Task 2: Add leaderboard CSS

**Files:**
- Modify: `style.css` (append after line 668)

- [ ] **Step 1: Append leaderboard styles**

Append to the end of `style.css`:

```css
/* Leaderboard screen */
body.lb-open {
  align-items: flex-start;
  overflow-y: auto;
  overflow-x: hidden;
}

#leaderboard-screen {
  padding: 20px 0 32px;
  text-align: center;
}

.lb-score {
  font-size: 4rem;
  font-weight: 900;
  background: linear-gradient(135deg, #f9ca24, #f0932b);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 12px 0 4px;
}

.lb-stats {
  color: #aaa;
  font-size: 0.85rem;
  margin-bottom: 20px;
}

/* Tabs */
.lb-tabs {
  display: flex;
  border-radius: 10px;
  overflow: hidden;
  border: 1px solid #2d3561;
  margin-bottom: 12px;
}

.lb-tab {
  flex: 1;
  padding: 8px;
  background: none;
  border: none;
  color: #555;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
}

.lb-tab.active {
  background: #6c5ce7;
  color: #fff;
}

.lb-tab:hover:not(.active) {
  background: #16213e;
  color: #aaa;
}

/* Table */
.lb-table-wrap {
  background: #16213e;
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 12px;
  text-align: left;
}

.lb-table-header {
  display: flex;
  padding: 6px 12px;
  border-bottom: 1px solid #2d3561;
  color: #555;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.lb-row {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  border-bottom: 1px solid #1a1a2e;
  font-size: 0.85rem;
}

.lb-row:last-child { border-bottom: none; }

.lb-row.player {
  background: rgba(108, 92, 231, 0.15);
  border: 1px solid rgba(108, 92, 231, 0.3);
  color: #a29bfe;
}

.lb-row.unsubmitted { color: #555; }

.lb-row.sep {
  color: #555;
  font-size: 0.75rem;
  padding: 4px 12px;
}

.lb-col-rank {
  width: 28px;
  flex-shrink: 0;
  font-weight: 700;
}

.lb-col-name {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.lb-col-score {
  text-align: right;
  min-width: 44px;
  font-weight: 700;
}

/* Gold/silver/bronze for top 3 community rows */
.lb-row:nth-child(1) .lb-col-rank { color: #f9ca24; }
.lb-row:nth-child(2) .lb-col-rank { color: #aaa; }
.lb-row:nth-child(3) .lb-col-rank { color: #cd7f32; }
.lb-row.player .lb-col-rank { color: #a29bfe; }

.lb-error {
  padding: 10px 12px;
  color: #fdcb6e;
  font-size: 0.82rem;
  text-align: center;
}

.lb-error a {
  color: #a29bfe;
  cursor: pointer;
  text-decoration: underline;
}

/* Post area */
.lb-post-area { margin-bottom: 8px; }

.lb-post-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
}

.lb-name-input {
  flex: 1;
  background: #16213e;
  border: 1px solid #2d3561;
  border-radius: 8px;
  padding: 9px 12px;
  color: #f9ca24;
  font-size: 0.9rem;
  font-weight: 700;
  outline: none;
  transition: border-color 0.15s;
}

.lb-name-input:focus { border-color: #6c5ce7; }

.lb-post-btn {
  padding: 9px 14px;
  background: #16213e;
  border: 1px solid #00b894;
  border-radius: 20px;
  color: #00b894;
  font-size: 0.82rem;
  font-weight: 700;
  cursor: pointer;
  white-space: nowrap;
  transition: background 0.15s;
}

.lb-post-btn:hover:not(:disabled) { background: rgba(0, 184, 148, 0.12); }
.lb-post-btn:disabled { opacity: 0.4; cursor: default; }

.lb-home-btn {
  padding: 9px 14px !important;
  font-size: 0.82rem !important;
  white-space: nowrap;
}

.lb-skip-wrap {
  text-align: center;
  margin-bottom: 10px;
}

.lb-static-name {
  flex: 1;
  color: #f9ca24;
  font-weight: 700;
  font-size: 0.9rem;
  text-align: left;
  padding: 9px 0;
}

.lb-play-btn { width: 100%; }

/* Leaderboard settings toggle */
.lb-default-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 6px 0;
}

.lb-tab-toggle {
  display: flex;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #2d3561;
}

.lb-toggle-opt {
  padding: 5px 12px;
  background: none;
  border: none;
  color: #555;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
}

.lb-toggle-opt.active { background: #6c5ce7; color: #fff; }
.lb-toggle-opt:hover:not(.active) { background: #1e2a50; color: #aaa; }
```

- [ ] **Step 2: Verify no CSS parse errors**

Open `index.html` in a browser — no console errors. The start screen looks unchanged.

- [ ] **Step 3: Commit**

```bash
git add style.css
git commit -m "Add leaderboard screen CSS and settings toggle styles"
```

---

### Task 3: Core leaderboard JS — score history, `showLeaderboard()`, `endGame()` wiring

**Files:**
- Modify: `index.html` (script block)

- [ ] **Step 1: Add module-level variables**

In the `<script>` block, after `let activePLUs = [];` (around line 194), add:

```javascript
let correctCount = 0;
let currentGameEntryDate = null;
let lbActiveTab = 'community';
let lbPosted = false;
let lbPlayerRank = null;
let lbPlayerName = null;
```

- [ ] **Step 2: Track `correctCount` in `startGame()` and `handleAnswer()`**

In `startGame()`, after `streak = 0;`, add:

```javascript
  correctCount = 0;
```

In `handleAnswer()`, inside the `if (isCorrect) {` block, directly after `score += pts;`, add:

```javascript
    correctCount++;
```

- [ ] **Step 3: Add score history helpers**

Add these functions before `showSettings()`:

```javascript
function getScoreHistory() {
  const raw = localStorage.getItem('plu_score_history');
  if (raw) return JSON.parse(raw);
  const best = parseInt(localStorage.getItem('plu_best') || '0');
  if (best > 0) return [{ score: best, correct: null, total: null, streak: null, date: new Date(0).toISOString() }];
  return [];
}

function saveScoreHistory(history) {
  localStorage.setItem('plu_score_history', JSON.stringify(history));
}

function recordGame(s, correct, total, streak) {
  const history = getScoreHistory();
  const date = new Date().toISOString();
  currentGameEntryDate = date;
  history.push({ score: s, correct, total, streak, date });
  if (history.length > 50) history.splice(0, history.length - 50);
  saveScoreHistory(history);
  const best = history.reduce((m, e) => Math.max(m, e.score), 0);
  localStorage.setItem('plu_best', best);
}
```

- [ ] **Step 4: Add `showLeaderboard()` and tab helpers**

Add after `recordGame()`:

```javascript
function showLeaderboard() {
  lbPosted = false;
  lbPlayerRank = null;
  lbPlayerName = null;
  lbActiveTab = localStorage.getItem('plu_lb_default') || 'community';

  recordGame(score, correctCount, TOTAL_ROUNDS, bestStreak);

  const pct = score / (TOTAL_ROUNDS * POINTS_CORRECT);
  let grade = '';
  if (pct >= 0.9)      grade = '🏆 Produce master!';
  else if (pct >= 0.7) grade = '🌟 Seasoned cashier!';
  else if (pct >= 0.5) grade = '🛒 Getting the hang of it!';
  else if (pct >= 0.3) grade = '📦 Keep practicing!';
  else                 grade = '🍌 Stick to bananas for now!';

  document.getElementById('lb-score').textContent = score;
  document.getElementById('lb-stats').textContent =
    `${correctCount}/${TOTAL_ROUNDS} correct · best streak ${bestStreak} · ${grade}`;

  initPostArea();
  switchLbTab(lbActiveTab);

  document.body.classList.add('lb-open');
  showScreen('leaderboard-screen');
}

function switchLbTab(tab) {
  lbActiveTab = tab;
  document.getElementById('tab-community').classList.toggle('active', tab === 'community');
  document.getElementById('tab-personal').classList.toggle('active', tab === 'personal');
  document.getElementById('lb-post-area').style.display = tab === 'community' ? '' : 'none';
  if (tab === 'community') renderCommunityBoard();
  else renderPersonalBest();
}

function skipLeaderboard() {
  document.getElementById('lb-post-area').style.display = 'none';
}

function initPostArea() {
  lbPosted = false;
  const nameInput = document.getElementById('lb-name-input');
  const postBtn = document.getElementById('lb-post-btn');
  const postRow = document.getElementById('lb-post-row');

  const existing = postRow.querySelector('.lb-static-name');
  if (existing) existing.remove();
  nameInput.style.display = '';
  nameInput.disabled = false;
  nameInput.value = localStorage.getItem('plu_player_name') || '';
  postBtn.textContent = 'Post score';
  postBtn.disabled = false;
  postBtn.style.display = '';
  postBtn.onclick = postScore;

  document.getElementById('lb-skip-wrap').innerHTML =
    '<button class="text-btn" onclick="skipLeaderboard()">skip leaderboard</button>';
  document.getElementById('lb-post-area').style.display = '';
}

// Stubs — implemented in Tasks 5 and 6
function renderCommunityBoard() {
  document.getElementById('lb-rows').innerHTML =
    '<div class="lb-row unsubmitted" style="justify-content:center">Community leaderboard not yet configured</div>';
}

function renderPersonalBest() {
  document.getElementById('lb-rows').innerHTML =
    '<div class="lb-row unsubmitted" style="justify-content:center">Loading…</div>';
}

function postScore() {}
```

- [ ] **Step 5: Replace `endGame()` with a one-liner**

Replace the entire `endGame()` function (currently lines ~528–553) with:

```javascript
function endGame() {
  clearInterval(timerInterval);
  showLeaderboard();
}
```

- [ ] **Step 6: Update `showStart()` to remove `lb-open`**

Replace the existing `showStart()` function with:

```javascript
function showStart() {
  document.body.classList.remove('settings-open');
  document.body.classList.remove('lb-open');
  showScreen('start-screen');
  document.getElementById('fun-fact').textContent = randomFact();
}
```

- [ ] **Step 7: Update `startGame()` to remove `lb-open`**

At the very top of `startGame()`, before `TIMER_MS = ...`, add:

```javascript
  document.body.classList.remove('lb-open');
```

- [ ] **Step 8: Verify in browser**

Play a full game (10 rounds). After the last round, verify:
- Leaderboard screen appears (not the old end screen)
- Score, correct count, best streak, and grade all display correctly
- Both tabs are clickable — Community shows "not yet configured", Personal best shows "Loading…"
- "skip leaderboard" hides the post area; it does not reappear
- Play Again and Home both work correctly

- [ ] **Step 9: Commit**

```bash
git add index.html
git commit -m "Wire endGame() to leaderboard, add score history and tab scaffolding"
```

---

### Task 4: Personal best tab

**Files:**
- Modify: `index.html` (script block — replace `renderPersonalBest()` stub)

- [ ] **Step 1: Replace the `renderPersonalBest()` stub**

Find the stub `function renderPersonalBest() { ... }` added in Task 3 and replace it entirely with:

```javascript
function renderPersonalBest() {
  const history = getScoreHistory();
  const sorted = [...history].sort((a, b) => b.score - a.score);
  const top10 = sorted.slice(0, 10);
  const currentIdx = sorted.findIndex(e => e.date === currentGameEntryDate);
  const container = document.getElementById('lb-rows');
  container.innerHTML = '';

  if (sorted.length === 0) {
    container.innerHTML = '<div class="lb-row unsubmitted" style="justify-content:center">No games yet</div>';
    return;
  }

  top10.forEach((entry, i) => {
    const isCurrent = entry.date === currentGameEntryDate;
    const label = isCurrent
      ? 'You (now)'
      : entry.date === new Date(0).toISOString()
        ? 'Previous best'
        : new Date(entry.date).toLocaleDateString();
    const row = document.createElement('div');
    row.className = 'lb-row' + (isCurrent ? ' player' : '');
    row.innerHTML = `
      <span class="lb-col-rank">${i + 1}</span>
      <span class="lb-col-name">${label}</span>
      <span class="lb-col-score">${entry.score}</span>
    `;
    container.appendChild(row);
  });

  if (currentIdx >= 10) {
    const sep = document.createElement('div');
    sep.className = 'lb-row sep';
    sep.innerHTML = '<span class="lb-col-rank">…</span><span class="lb-col-name"></span><span class="lb-col-score"></span>';
    container.appendChild(sep);

    const entry = sorted[currentIdx];
    const row = document.createElement('div');
    row.className = 'lb-row player';
    row.innerHTML = `
      <span class="lb-col-rank">${currentIdx + 1}</span>
      <span class="lb-col-name">You (now)</span>
      <span class="lb-col-score">${entry.score}</span>
    `;
    container.appendChild(row);
  }
}
```

- [ ] **Step 2: Verify personal best tab**

Play two or more games. After each, switch to "Personal best". Verify:
- All previous scores appear, sorted highest first
- Each row shows a human-readable date (or "You (now)" for the current game)
- Current game's row is highlighted in purple
- If current game is outside top 10, it appears below the "…" separator with correct rank
- Switching tabs back and forth doesn't duplicate rows

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "Implement personal best tab with score history"
```

---

### Task 5: Supabase setup + community tab

**Files:**
- Modify: `index.html` (add CDN tag, constants, replace `renderCommunityBoard()` stub)

**Prerequisite — do this before writing any code:**

1. Go to [supabase.com](https://supabase.com), create a free account and a new project
2. In the SQL Editor, run:

```sql
CREATE TABLE scores (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  name text NOT NULL,
  score integer NOT NULL,
  correct integer,
  total integer,
  streak integer,
  created_at timestamptz DEFAULT now()
);

ALTER TABLE scores ENABLE ROW LEVEL SECURITY;

CREATE POLICY "allow anon read" ON scores
  FOR SELECT TO anon USING (true);

CREATE POLICY "allow anon insert" ON scores
  FOR INSERT TO anon WITH CHECK (true);
```

3. Go to **Project Settings → API**, copy the **Project URL** and **anon/public key**

- [ ] **Step 1: Add Supabase CDN script tag**

In `index.html`, before `<script src="config.js">`, add:

```html
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
```

- [ ] **Step 2: Add Supabase constants + client at the top of the script block**

At the very top of the `<script>` block (before `const PRODUCE = PRODUCE_DATA;`), add:

```javascript
const SUPABASE_URL = 'YOUR_SUPABASE_URL';
const SUPABASE_ANON_KEY = 'YOUR_SUPABASE_ANON_KEY';
const sbClient = supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
```

Replace `YOUR_SUPABASE_URL` and `YOUR_SUPABASE_ANON_KEY` with the values copied in the prerequisite step.

- [ ] **Step 3: Add error message helper and `escapeHtml()`**

Add these before `renderCommunityBoard()`:

```javascript
const LB_ERRORS = [
  'The leaderboard has gone bananas 🍌 — <a onclick="renderCommunityBoard()">retry</a>',
  'Score submission got lost in the produce aisle — <a onclick="renderCommunityBoard()">try again</a>',
];

function lbErrorMsg() {
  return LB_ERRORS[Math.floor(Math.random() * LB_ERRORS.length)];
}

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;')
    .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
```

- [ ] **Step 4: Replace the `renderCommunityBoard()` stub**

Find the stub `function renderCommunityBoard() { ... }` added in Task 3 and replace it entirely with:

```javascript
async function renderCommunityBoard() {
  const container = document.getElementById('lb-rows');
  const errEl = document.getElementById('lb-error');
  container.innerHTML = '<div class="lb-row unsubmitted" style="justify-content:center;color:#555">Loading…</div>';
  errEl.style.display = 'none';

  try {
    const { data, error } = await sbClient
      .from('scores')
      .select('name, score')
      .order('score', { ascending: false })
      .limit(10);
    if (error) throw error;
    renderCommunityRows(data);
  } catch {
    container.innerHTML = '';
    errEl.innerHTML = lbErrorMsg();
    errEl.style.display = 'block';
  }
}

function renderCommunityRows(rows) {
  const container = document.getElementById('lb-rows');
  container.innerHTML = '';

  if (!rows || rows.length === 0) {
    container.innerHTML =
      '<div class="lb-row unsubmitted" style="justify-content:center">No scores yet — be the first!</div>';
  } else {
    rows.forEach((row, i) => {
      const el = document.createElement('div');
      el.className = 'lb-row';
      el.innerHTML = `
        <span class="lb-col-rank">${i + 1}</span>
        <span class="lb-col-name">${escapeHtml(row.name)}</span>
        <span class="lb-col-score">${row.score}</span>
      `;
      container.appendChild(el);
    });
  }

  const sep = document.createElement('div');
  sep.className = 'lb-row sep';
  sep.innerHTML = '<span class="lb-col-rank">…</span><span class="lb-col-name"></span><span class="lb-col-score"></span>';
  container.appendChild(sep);

  const playerRow = document.createElement('div');
  if (lbPosted && lbPlayerRank !== null) {
    playerRow.className = 'lb-row player';
    playerRow.innerHTML = `
      <span class="lb-col-rank">${lbPlayerRank}</span>
      <span class="lb-col-name">${escapeHtml(lbPlayerName)} ← you</span>
      <span class="lb-col-score">${score}</span>
    `;
  } else {
    playerRow.className = 'lb-row player unsubmitted';
    playerRow.innerHTML = `
      <span class="lb-col-rank">—</span>
      <span class="lb-col-name">— not submitted</span>
      <span class="lb-col-score">—</span>
    `;
  }
  container.appendChild(playerRow);
}
```

- [ ] **Step 5: Verify community tab**

Play a game. On the Community tab:
- "Loading…" appears briefly, then top 10 rows render (or "No scores yet" if empty)
- "— not submitted" player row appears below the separator
- No 401/403 errors in the browser console (Supabase credentials are correct)
- Switching tabs back and forth reloads the board each time without errors

- [ ] **Step 6: Commit**

```bash
git add index.html
git commit -m "Add Supabase community leaderboard tab"
```

---

### Task 6: Post score flow

**Files:**
- Modify: `index.html` (script block — replace `postScore()` stub, add `showPostConfirmed()` and `enterEditMode()`)

- [ ] **Step 1: Replace the `postScore()` stub**

Find the stub `function postScore() {}` added in Task 3 and replace it with:

```javascript
async function postScore() {
  const nameInput = document.getElementById('lb-name-input');
  const postBtn = document.getElementById('lb-post-btn');
  const errEl = document.getElementById('lb-error');
  const name = nameInput.value.trim();
  if (!name) { nameInput.focus(); return; }

  localStorage.setItem('plu_player_name', name);
  postBtn.disabled = true;
  postBtn.textContent = 'Posting…';
  errEl.style.display = 'none';

  try {
    const { error: insertErr } = await sbClient.from('scores').insert({
      name,
      score,
      correct: correctCount,
      total: TOTAL_ROUNDS,
      streak: bestStreak,
    });
    if (insertErr) throw insertErr;

    const { count, error: rankErr } = await sbClient
      .from('scores')
      .select('*', { count: 'exact', head: true })
      .gt('score', score);
    if (rankErr) throw rankErr;

    lbPlayerName = name;
    lbPlayerRank = (count || 0) + 1;
    lbPosted = true;

    showPostConfirmed(name);
    await renderCommunityBoard();

  } catch {
    postBtn.disabled = false;
    postBtn.textContent = 'Post score';
    errEl.innerHTML = lbErrorMsg();
    errEl.style.display = 'block';
  }
}
```

- [ ] **Step 2: Add `showPostConfirmed()` and `enterEditMode()`**

Add these after `postScore()`:

```javascript
function showPostConfirmed(name) {
  const postRow = document.getElementById('lb-post-row');
  const nameInput = document.getElementById('lb-name-input');
  const postBtn = document.getElementById('lb-post-btn');

  nameInput.style.display = 'none';
  postBtn.textContent = '✓ Posted';

  const staticName = document.createElement('span');
  staticName.className = 'lb-static-name';
  staticName.textContent = name;
  postRow.insertBefore(staticName, nameInput);

  document.getElementById('lb-skip-wrap').innerHTML =
    '<button class="text-btn" onclick="enterEditMode()">edit name</button>';

  setTimeout(() => { postBtn.style.display = 'none'; }, 1500);
}

function enterEditMode() {
  const postRow = document.getElementById('lb-post-row');
  const nameInput = document.getElementById('lb-name-input');
  const postBtn = document.getElementById('lb-post-btn');
  const existing = postRow.querySelector('.lb-static-name');
  if (existing) existing.remove();

  nameInput.style.display = '';
  nameInput.disabled = false;
  postBtn.style.display = '';
  postBtn.textContent = 'Post score';
  postBtn.disabled = false;
  postBtn.onclick = postScore;

  lbPosted = false;
  lbPlayerRank = null;
  lbPlayerName = null;

  document.getElementById('lb-skip-wrap').innerHTML =
    '<button class="text-btn" onclick="skipLeaderboard()">skip leaderboard</button>';

  nameInput.focus();
  renderCommunityBoard();
}
```

- [ ] **Step 3: Verify post flow**

Play a game. On the leaderboard:
1. Enter a name and click **Post score** — verify "Posting…" appears, then "✓ Posted" for 1.5 s, then the button disappears
2. Name becomes static text; "edit name" link appears below
3. Community board refreshes: your row at the bottom shows your rank and "← you"
4. Click **edit name** — name field and Post button reappear
5. Change the name and post again — board refreshes with the new name
6. Post with an empty name — name field gets focus, nothing is submitted
7. Simulate offline (DevTools → Network → Offline) and try to post — verify a humorous error appears and the Post button re-enables

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "Add post score flow with name management and edit mode"
```

---

### Task 7: Settings — leaderboard default tab

**Files:**
- Modify: `index.html` (settings screen HTML + `buildSettingsScreen()` JS)

- [ ] **Step 1: Add Leaderboard section to `#settings-screen` HTML**

In `index.html`, inside `#settings-screen`, after the closing `</div>` of the PLU Filter settings section (just before `<button class="btn settings-done-btn"`), add:

```html
    <div class="settings-section">
      <div class="settings-section-header">
        <span class="settings-section-title">Leaderboard</span>
      </div>
      <div class="lb-default-row">
        <span class="item-name">Default tab</span>
        <div class="lb-tab-toggle">
          <button class="lb-toggle-opt" id="lbt-community" onclick="setLbDefault('community')">Community</button>
          <button class="lb-toggle-opt" id="lbt-personal" onclick="setLbDefault('personal')">Personal best</button>
        </div>
      </div>
    </div>
```

- [ ] **Step 2: Add `setLbDefault()` function**

Add after `selectAllFilter()`:

```javascript
function setLbDefault(val) {
  localStorage.setItem('plu_lb_default', val);
  document.getElementById('lbt-community').classList.toggle('active', val === 'community');
  document.getElementById('lbt-personal').classList.toggle('active', val === 'personal');
}
```

- [ ] **Step 3: Initialise the toggle in `buildSettingsScreen()`**

At the end of `buildSettingsScreen()`, just before the closing `}`, add:

```javascript
  const lbDefault = localStorage.getItem('plu_lb_default') || 'community';
  document.getElementById('lbt-community').classList.toggle('active', lbDefault === 'community');
  document.getElementById('lbt-personal').classList.toggle('active', lbDefault === 'personal');
```

- [ ] **Step 4: Verify in browser**

Open Settings. Verify:
- "Leaderboard" section appears below "PLU Filter"
- Community/Personal best toggle is visible; "Community" is active by default
- Clicking a toggle option highlights it immediately
- Closing and reopening Settings retains the selection
- Playing a game opens the leaderboard on whichever tab was set as default

- [ ] **Step 5: Commit and push**

```bash
git add index.html
git commit -m "Add leaderboard default tab setting"
git push
```
