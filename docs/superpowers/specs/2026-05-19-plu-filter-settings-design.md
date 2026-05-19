# PLU Filter Settings Screen

**Date:** 2026-05-19
**Status:** Approved

## Overview

Add a settings screen where the player can select which PLU items appear in game rounds. At least 90% of selected items must appear across a game's rounds; repeats are allowed if necessary.

## Data layer

Add a `category` string field to every entry in `produce.js`, matching the existing section comment headers (e.g. `"Apples"`, `"Citrus"`, `"Berries"`, `"Tropical"`, `"Melons"`, etc.).

```js
{
  plu: "4011",
  name: "Banana",
  category: "Tropical",
  // ... existing fields unchanged
}
```

No changes to `config.js`.

## Settings screen

### Entry point

A gear icon button (⚙) in the top-right corner of the start screen. Calls `showScreen('settings-screen')`.

### Layout

- **Header:** "Settings" label + "Back" button (returns to start screen via `showStart()`)
- **PLU Filter section:**
  - Global "Select All" / "Deselect All" toggle
  - Items grouped by `category`, rendered as collapsible groups
  - Each group has a group-level checkbox (checks/unchecks all items in the group)
  - Each item row: emoji + name + PLU code + individual checkbox
- **Warning banner:** shown when fewer than 4 items are checked — "Select at least 4 items to play"
- **Done button:** sticky at bottom, returns to start screen

### Start screen guard

The "Start Game" button is disabled (greyed out) when the active filter has fewer than 4 items. Re-enabled as soon as ≥4 are checked.

## Game logic

### Active item set

At game start (`startGame()`), read `plu_filter` from localStorage. If absent or empty, treat all PLUs as active. Build `activePRODUCE` — the filtered subset of `PRODUCE`.

```js
let activePRODUCE = [];  // module-level, set in startGame()

function startGame() {
  const saved = JSON.parse(localStorage.getItem('plu_filter') || 'null');
  activePRODUCE = saved ? PRODUCE.filter(p => saved.includes(p.plu)) : [...PRODUCE];
  // ... rest of existing startGame logic
}
```

### Round selection

`nextRound()` draws from `activePRODUCE` instead of `PRODUCE`. The existing `usedIndices` exhaustion logic is unchanged — once all active items have appeared, the pool resets. This guarantees all selected items appear before any repeats (satisfying the ≥90% requirement for any game length ≤ item count).

### Distractors

Distractor PLUs are drawn from `activePRODUCE`'s PLU list (not the global `allPLUs`). When active pool has exactly 4 items, all 4 appear as choices every round.

## Persistence

| localStorage key | Type | Notes |
|---|---|---|
| `plu_best` | number | Existing — unchanged |
| `plu_filter` | JSON array of PLU strings | New. Absent = all active |

Selection is written to `plu_filter` immediately on any checkbox change (no explicit "Save" step).

## Files changed

| File | Change |
|---|---|
| `produce.js` | Add `category` field to all 78 entries |
| `index.html` | New `#settings-screen` div, gear button on start screen, filter logic in JS |
| `style.css` | Settings screen layout, category group styles, checkbox styles |
