# PLU Filter Settings Screen — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a settings screen where the player selects which PLU items appear in game rounds, persisted to localStorage.

**Architecture:** New `#settings-screen` div in `index.html`, a `category` field added to each `produce.js` entry, and a module-level `activePRODUCE` array derived from the saved filter at game start. Distractors are drawn from the active pool only.

**Tech Stack:** Vanilla JS, HTML, CSS — no build step, no dependencies.

---

## PLU → Category reference table

Use this table when adding `category` fields in Task 1.

| Category | PLU codes |
|---|---|
| Apples | 3507, 3616, 4131, 4135, 4017, 3283, 4130, 3486 |
| Avocados | 4225, 94046 |
| Banana | 4011 |
| Berries | 3329, 4275 |
| Citrus | 4289, 4053, 4048, 3632, 4012, 3129 |
| Dragon Fruit | 3319, 3040 |
| Grapes | 4022 |
| Kiwi | 3279 |
| Mangoes | 4959, 4312 |
| Melons | 4050, 4326, 4329, 95369, 4332, 4032, 3421 |
| Stone Fruit | 4378, 4044 |
| Pears | 4408, 4409, 4413, 4416, 4417, 4425 |
| Pineapple | 4430 |
| Specialty Fruit | 3127, 4428, 3112 |
| Tomatoes | 4087, 4799 |
| Cruciferous & Greens | 3082, 3083, 4070 |
| Roots & Bulbs | 4562, 4608, 4662 |
| Onions | 4082, 4166, 4663, 4093 |
| Peppers | 4065, 3121, 4688, 4689, 4693 |
| Potatoes | 4727, 4073, 4072, 4817, 3288 |
| Squash & Eggplant | 4750, 4759, 4776, 94782, 4081, 94067 |
| Cucumbers | 4062, 4593, 94593 |
| Other Vegetables | 4762, 4080, 4077 |

---

## Task 1: Add `category` field to produce.js

**Files:**
- Modify: `produce.js`

- [ ] **Step 1: Add `category` to every entry**

Using the table above, add `category: "..."` to each object in `PRODUCE_DATA`. The field should go after `plu`, before `name`. Example for the first three entries:

```js
{
  plu: "3507",
  category: "Apples",
  name: "Cosmic Crisp Apple",
  // ...
},
{
  plu: "3616",
  category: "Apples",
  name: "Envy Apple",
  // ...
},
{
  plu: "4225",
  category: "Avocados",
  name: "Hass Avocado",
  // ...
},
```

Apply this pattern to all 78 entries. Use the reference table above to look up each PLU's category.

- [ ] **Step 2: Verify count in browser console**

Open `index.html` in a browser. In the console, run:

```js
const cats = [...new Set(PRODUCE_DATA.map(p => p.category))];
console.log('Categories:', cats.length, cats);
console.log('Missing category:', PRODUCE_DATA.filter(p => !p.category).map(p => p.plu));
```

Expected: 23 categories, empty missing-category array.

- [ ] **Step 3: Commit**

```bash
git add produce.js
git commit -m "Add category field to all 78 produce entries"
```

---

## Task 2: Add settings screen HTML to index.html

**Files:**
- Modify: `index.html`

- [ ] **Step 1: Add gear icon button to start screen**

Find the existing `<button class="btn" onclick="startGame()">Start Game</button>` in `#start-screen`. Add an `id="start-btn"` attribute to it (needed later for the guard). Also add a gear button in the top-right corner of the start screen. Insert after the opening `<div id="start-screen" class="screen active">` tag:

```html
<div id="start-screen" class="screen active">
  <button class="gear-btn" onclick="showSettings()" aria-label="Settings">⚙</button>
```

And update the Start Game button to have an id:

```html
<button class="btn" id="start-btn" onclick="startGame()">Start Game</button>
```

- [ ] **Step 2: Add settings screen div**

After the closing `</div>` of `#end-screen` and before `</div>` that closes `#app`, insert:

```html
  <!-- SETTINGS SCREEN -->
  <div id="settings-screen" class="screen">
    <div class="settings-header">
      <button class="back-btn" onclick="showStart()">← Back</button>
      <h2 class="settings-title">Settings</h2>
    </div>

    <div class="settings-section">
      <div class="settings-section-header">
        <span class="settings-section-title">PLU Filter</span>
        <div class="select-all-wrap">
          <button class="text-btn" onclick="selectAllFilter(true)">Select All</button>
          <span class="divider">·</span>
          <button class="text-btn" onclick="selectAllFilter(false)">Deselect All</button>
        </div>
      </div>
      <div id="filter-warning" class="filter-warning" style="display:none">
        Select at least 4 items to play
      </div>
      <div id="settings-list" class="settings-list"></div>
    </div>

    <button class="btn settings-done-btn" onclick="showStart()">Done</button>
  </div>
```

- [ ] **Step 3: Verify HTML parses**

Open `index.html` in a browser. No console errors. The page shows the start screen as before. Clicking ⚙ shows a blank settings screen (no CSS yet, plain layout). Clicking Back returns to start screen.

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "Add settings screen HTML and gear button"
```

---

## Task 3: Add settings screen CSS to style.css

**Files:**
- Modify: `style.css`

- [ ] **Step 1: Add all settings screen styles**

Append the following to the end of `style.css`:

```css
/* Settings screen */
#settings-screen {
  padding: 20px 0 100px;
  text-align: left;
}

.gear-btn {
  position: absolute;
  top: 20px;
  right: 20px;
  background: none;
  border: none;
  font-size: 1.4rem;
  color: #555;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 8px;
  transition: color 0.15s, background 0.15s;
  line-height: 1;
}
.gear-btn:hover { color: #aaa; background: #16213e; }

.settings-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 24px;
}

.back-btn {
  background: none;
  border: none;
  color: #aaa;
  font-size: 0.9rem;
  cursor: pointer;
  padding: 6px 10px;
  border-radius: 8px;
  transition: color 0.15s, background 0.15s;
}
.back-btn:hover { color: #eee; background: #16213e; }

.settings-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: #eee;
  margin: 0;
}

.settings-section {
  background: #16213e;
  border-radius: 16px;
  padding: 16px;
  margin-bottom: 20px;
}

.settings-section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.settings-section-title {
  font-size: 0.85rem;
  font-weight: 700;
  color: #aaa;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.select-all-wrap {
  display: flex;
  align-items: center;
  gap: 6px;
}

.text-btn {
  background: none;
  border: none;
  color: #6c5ce7;
  font-size: 0.8rem;
  cursor: pointer;
  padding: 2px 4px;
  border-radius: 4px;
}
.text-btn:hover { color: #a29bfe; }

.divider { color: #555; font-size: 0.8rem; }

.filter-warning {
  background: rgba(214, 48, 49, 0.12);
  border: 1px solid rgba(214, 48, 49, 0.4);
  color: #ff7675;
  font-size: 0.8rem;
  border-radius: 8px;
  padding: 8px 12px;
  margin-bottom: 12px;
}

.settings-list {
  max-height: 400px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

/* Category group */
.settings-group {
  border-radius: 10px;
  overflow: hidden;
}

.group-header {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  background: #1e2a50;
  cursor: pointer;
  user-select: none;
  border-radius: 10px;
}
.group-header:hover { background: #243060; }

.group-name {
  flex: 1;
  font-size: 0.9rem;
  font-weight: 600;
  color: #eee;
}

.group-count {
  font-size: 0.75rem;
  color: #666;
  background: #16213e;
  padding: 1px 7px;
  border-radius: 999px;
}

.group-items {
  display: flex;
  flex-direction: column;
  padding: 4px 0 4px 12px;
}

.item-row {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 7px 12px 7px 0;
  cursor: pointer;
  user-select: none;
  border-radius: 8px;
  transition: background 0.1s;
}
.item-row:hover { background: rgba(255,255,255,0.04); }

.item-emoji { font-size: 1.1rem; min-width: 24px; text-align: center; }

.item-name {
  flex: 1;
  font-size: 0.85rem;
  color: #ccc;
}

.item-plu {
  font-size: 0.75rem;
  font-weight: 700;
  color: #555;
  letter-spacing: 1px;
  font-family: monospace;
}

/* Checkbox styling */
.group-header input[type=checkbox],
.item-row input[type=checkbox] {
  width: 16px;
  height: 16px;
  accent-color: #6c5ce7;
  cursor: pointer;
  flex-shrink: 0;
}

.settings-done-btn {
  width: 100%;
  margin-top: 4px;
}

/* Make start screen relative so gear btn positions correctly */
#start-screen { position: relative; }
```

- [ ] **Step 2: Verify visually**

Open `index.html`. The start screen should show a ⚙ button in the top-right. Clicking it should show a styled settings screen with the "PLU Filter" section (list still empty — JS in next task). Back/Done should return to start screen.

- [ ] **Step 3: Commit**

```bash
git add style.css
git commit -m "Add settings screen CSS"
```

---

## Task 4: Add settings screen JS to index.html

**Files:**
- Modify: `index.html` (the `<script>` section)

- [ ] **Step 1: Add helper functions**

Inside the `<script>` block, after the existing `let highScore = ...` line, add:

```js
function showSettings() {
  buildSettingsScreen();
  showScreen('settings-screen');
}

function buildSettingsScreen() {
  const saved = JSON.parse(localStorage.getItem('plu_filter') || 'null');
  const activePLUs = saved ? new Set(saved) : new Set(PRODUCE.map(p => p.plu));

  const categories = {};
  PRODUCE.forEach(p => {
    if (!categories[p.category]) categories[p.category] = [];
    categories[p.category].push(p);
  });

  const container = document.getElementById('settings-list');
  container.innerHTML = '';

  Object.entries(categories).forEach(([cat, items]) => {
    const allChecked = items.every(p => activePLUs.has(p.plu));
    const someChecked = items.some(p => activePLUs.has(p.plu));

    const group = document.createElement('div');
    group.className = 'settings-group';
    group.innerHTML = `
      <label class="group-header">
        <input type="checkbox" class="group-check" ${allChecked ? 'checked' : ''}>
        <span class="group-name">${cat}</span>
        <span class="group-count">${items.length}</span>
      </label>
      <div class="group-items">
        ${items.map(p => `
          <label class="item-row">
            <input type="checkbox" class="item-check" data-plu="${p.plu}" ${activePLUs.has(p.plu) ? 'checked' : ''}>
            <span class="item-emoji">${p.emoji}</span>
            <span class="item-name">${p.name}</span>
            <span class="item-plu">${p.plu}</span>
          </label>
        `).join('')}
      </div>
    `;

    const groupCb = group.querySelector('.group-check');
    if (someChecked && !allChecked) groupCb.indeterminate = true;

    groupCb.addEventListener('change', () => {
      group.querySelectorAll('.item-check').forEach(ic => ic.checked = groupCb.checked);
      groupCb.indeterminate = false;
      onFilterChange();
    });

    group.querySelectorAll('.item-check').forEach(cb => {
      cb.addEventListener('change', () => {
        const allCbs = group.querySelectorAll('.item-check');
        const checked = [...allCbs].filter(c => c.checked).length;
        groupCb.checked = checked === allCbs.length;
        groupCb.indeterminate = checked > 0 && checked < allCbs.length;
        onFilterChange();
      });
    });

    container.appendChild(group);
  });

  updateStartGuard();
}

function onFilterChange() {
  const plus = [...document.querySelectorAll('.item-check:checked')].map(cb => cb.dataset.plu);
  localStorage.setItem('plu_filter', JSON.stringify(plus));
  updateStartGuard();
}

function updateStartGuard() {
  const saved = JSON.parse(localStorage.getItem('plu_filter') || 'null');
  const count = saved ? saved.length : PRODUCE.length;
  const btn = document.getElementById('start-btn');
  const warning = document.getElementById('filter-warning');
  btn.disabled = count < 4;
  warning.style.display = count < 4 ? 'block' : 'none';
}

function selectAllFilter(checked) {
  document.querySelectorAll('.item-check').forEach(cb => cb.checked = checked);
  document.querySelectorAll('.group-check').forEach(cb => {
    cb.checked = checked;
    cb.indeterminate = false;
  });
  onFilterChange();
}
```

- [ ] **Step 2: Call `updateStartGuard()` on page load**

Find the existing `init()` function call at the bottom of the script, or the first code that runs on page load. Add `updateStartGuard();` there. If there's no init function, add it just before the `showStart()` call:

```js
updateStartGuard();
showStart();
```

If the script ends with standalone calls like `showStart();`, insert `updateStartGuard();` on the line before it.

- [ ] **Step 3: Verify settings screen works**

Open `index.html`. Click ⚙:
- All 78 items should be visible, grouped by category (23 groups).
- Checking/unchecking items should save to localStorage immediately.
- Deselecting all items should show the red warning banner and disable Start Game.
- Selecting 4+ items should hide the warning and re-enable Start Game.
- Group checkbox should show indeterminate state (dash) when partially checked.
- Refreshing the page should preserve the selection.

In the browser console, verify:
```js
JSON.parse(localStorage.getItem('plu_filter')).length  // returns number of checked items
```

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "Add settings screen JS: filter builder, localStorage persistence, start guard"
```

---

## Task 5: Update game logic to use active PLU filter

**Files:**
- Modify: `index.html` (the `<script>` section)

- [ ] **Step 1: Add `activePRODUCE` module-level variable**

Find the existing module-level variables block (near `let score = 0; let streak = 0;` etc.). Add:

```js
let activePRODUCE = [];
```

- [ ] **Step 2: Set `activePRODUCE` at game start**

Find the `startGame()` function. After the `TIMER_MS = ...` line and before `score = 0;`, add:

```js
const saved = JSON.parse(localStorage.getItem('plu_filter') || 'null');
activePRODUCE = (saved && saved.length >= 4)
  ? PRODUCE.filter(p => saved.includes(p.plu))
  : [...PRODUCE];
```

- [ ] **Step 3: Update `nextRound()` to use `activePRODUCE`**

In `nextRound()`, find this block:

```js
// Pick a random item not used yet
let available = PRODUCE.map((_, i) => i).filter(i => !usedIndices.includes(i));
if (available.length === 0) { usedIndices = []; available = PRODUCE.map((_, i) => i); }
const idx = available[Math.floor(Math.random() * available.length)];
usedIndices.push(idx);
currentItem = PRODUCE[idx];
```

Replace it with:

```js
// Pick a random item not used yet
let available = activePRODUCE.map((_, i) => i).filter(i => !usedIndices.includes(i));
if (available.length === 0) { usedIndices = []; available = activePRODUCE.map((_, i) => i); }
const idx = available[Math.floor(Math.random() * available.length)];
usedIndices.push(idx);
currentItem = activePRODUCE[idx];
```

- [ ] **Step 4: Update distractor generation to use `activePRODUCE`**

In `nextRound()`, find:

```js
const distractors = shuffle(allPLUs.filter(p => p !== currentItem.plu)).slice(0, 3);
```

Replace with:

```js
const activePLUs = activePRODUCE.map(p => p.plu);
const distractors = shuffle(activePLUs.filter(p => p !== currentItem.plu)).slice(0, 3);
```

- [ ] **Step 5: Verify full game flow**

Open `index.html`. Test these scenarios:

**Scenario A — default (all items active):**
Click Start Game. Play 10 rounds. All rounds should work normally.

**Scenario B — small selection:**
Go to Settings. Deselect All, then select only the 8 Apples. Click Done. Start Game. Play 10 rounds — you should only see apple items, and all 8 should appear before any repeats. All 4 choice buttons should be apple PLUs.

**Scenario C — exactly 4 items:**
Go to Settings. Deselect All, then check exactly 4 items. Start Game. Each round, the 4 choice buttons should show exactly those 4 PLUs.

**Scenario D — fewer than 4 items:**
Go to Settings. Deselect until only 3 items remain. The Start Game button should be disabled with the warning banner visible. You should not be able to start a game.

- [ ] **Step 6: Commit**

```bash
git add index.html
git commit -m "Wire PLU filter into game: activePRODUCE, round selection, distractors"
```

---

## Task 6: Push to GitHub

- [ ] **Push all commits**

```bash
git push
```

Expected: all 5 commits pushed to `origin main` with no errors.
