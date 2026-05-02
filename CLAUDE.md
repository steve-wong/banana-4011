# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Git workflow

Commit and push to GitHub after every meaningful change so work is never lost. Use specific, descriptive commit messages that explain what changed and why.

```
git add index.html
git commit -m "Short description of what and why"
git push
```

The remote is `origin` on GitHub (`steve-wong/banana-4011`).

## Running the game

Open `index.html` directly in a browser — no build step, no server required. For live development, any static file server works:

```
python3 -m http.server
npx serve .
```

## Architecture

The entire game is a single self-contained file (`index.html`) with no dependencies, split into three sections:

- **`<style>`** — all CSS, organized by component with comments (`/* Scorebar */`, `/* Timer bar */`, etc.)
- **`<body>`** — three screen divs (`#start-screen`, `#game-screen`, `#end-screen`), only one visible at a time via the `.screen` / `.screen.active` class toggle
- **`<script>`** — all game logic as plain JS functions with module-level state variables

### Screen flow

`showStart()` → `startGame()` → `nextRound()` (loops `TOTAL_ROUNDS` times) → `endGame()`

Each round: `nextRound()` picks a random `PRODUCE` item, builds 4 choice buttons (1 correct + 3 shuffled distractors from `allPLUs`), then calls `startTimer()`. Answer handling branches to either `handleAnswer()` or `handleTimeout()`, both of which call `setTimeout(nextRound, 1800)` to advance.

### Config file (`config.js`)

All game settings live in `config.js` as the global `CONFIG` object. Add any new settings here — never hardcode game parameters in `index.html`.

```js
CONFIG.totalRounds      // number of rounds per game
CONFIG.timerDefault     // starting slider value in seconds
CONFIG.timerMin         // slider minimum in seconds
CONFIG.timerMax         // slider maximum in seconds
CONFIG.pointsCorrect    // base points per correct answer
CONFIG.streakBonus      // bonus points per answer when on a streak
CONFIG.streakThreshold  // streak length required to earn the bonus
CONFIG.reviewMs         // ms to display the correct answer before advancing to the next round
```

### Key state

| Variable | Purpose |
|---|---|
| `PRODUCE` | Alias for `PRODUCE_DATA` from `produce.js` — 30 items: `{ plu, name, variety, emoji, fact, quality, memoryTip }` |
| `TIMER_MS` | Set from the slider at game start (1–10 s) |
| `usedIndices` | Tracks which `PRODUCE` items have appeared this game to avoid repeats |
| `answered` | Guard flag — prevents double-processing clicks and timer expiry |
| `currentItem` | The `PRODUCE` entry for the active round |

### Scoring

- 10 pts per correct answer (`POINTS_CORRECT`)
- +5 pt streak bonus (`STREAK_BONUS`) when current streak ≥ 3
- High score persisted in `localStorage` under key `plu_best`

### PLU data file (`produce.js`)

All produce data lives in `produce.js` as the global `PRODUCE_DATA` array. Each entry schema:

```js
{
  plu: "4011",        // IFPS-assigned code
  name: "Banana",     // display name
  variety: "...",     // variety/sub-type shown in-game as a hint
  emoji: "🍌",        // visual representation
  fact: "...",        // revealed after each round
  quality: "...",     // how to distinguish from similar varieties, or quality indicators
  memoryTip: "...",   // mnemonic for remembering this PLU
}
```

`index.html` loads `produce.js` via `<script src="produce.js">` before its own script, so `PRODUCE_DATA` is available as a global.

### PLU code conventions

- 4-digit codes starting with `3` or `4` = conventional produce
- Prefix `9` = organic equivalent (e.g. organic banana = 94011)
- All PLUs in `PRODUCE_DATA` are real IFPS-assigned codes — verify against the IFPS lookup before adding new items
