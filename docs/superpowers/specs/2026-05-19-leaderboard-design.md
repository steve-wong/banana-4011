# Leaderboard Design

## Overview

Replace the end screen with a leaderboard screen shown after every game. Players can post their score to a community leaderboard (Supabase) or view their personal best history (localStorage). Participation is always optional — skip is one tap away.

---

## Screen Flow

`endGame()` calls `showLeaderboard()` instead of showing `#end-screen`. The `#end-screen` div is removed and replaced by `#leaderboard-screen`.

Full screen order: Start → Game → Leaderboard (→ Start on Play Again, or Home)

---

## Layout

### Header
- "Banana 4011" title + "Game over" subtitle
- Large score (e.g. "140")
- Stats line: "8/10 correct · best streak 5"

### Tabs
- **Community** | **Personal best** — tab strip below stats
- Active tab determined by `plu_lb_default` localStorage value (defaults to "community")
- Switching tabs is always available ad-hoc; does not change the default

### Leaderboard table
- Columns: rank (#), name, score
- Top 10 rows, then "…" separator, then the player's own row at the bottom
- Community tab: player's row shows "— not submitted" (greyed) until they post
- Personal best tab: player's current game row is highlighted at its rank among their history

### Bottom section (Community tab)
1. **Post row:** `[name input] [Post score] [Home]`
2. **Skip link:** "skip leaderboard" (centered, subtle)
3. **Play Again** (full-width hero button)

After posting: the Post score button is replaced by a brief "✓ Posted" confirmation (1.5 s), then the row settles to static name text + small "edit" link + Home button. Clicking edit re-enables the name field and Post button so the player can correct their name and re-submit.

**Personal best tab:** No post row shown. Just Play Again + Home.

---

## Name Management

- Display name stored in `localStorage` under `plu_player_name`
- Pre-filled from storage on load; editable inline before posting
- Persists across games — user sets it once

---

## Personal Best (Local)

- Each completed game appends to `localStorage` under `plu_score_history`
- Entry shape: `{ score, correct, total, streak, date }` (ISO date string)
- Capped at 50 entries (oldest dropped when full)
- Tab shows top 10 by score desc; current game's row highlighted
- Migration: on first load, if `plu_best` exists and `plu_score_history` does not, seed history with `{ score: plu_best, correct: null, total: null, streak: null, date: today }`
- Start screen high score continues to work — reads `Math.max(...plu_score_history.map(e => e.score))`

---

## Community Tab (Supabase)

### Table: `scores`

| column | type | notes |
|---|---|---|
| `id` | uuid | PK, auto-generated |
| `name` | text | display name |
| `score` | int | final score |
| `correct` | int | correct answers |
| `total` | int | rounds played |
| `streak` | int | best streak this game |
| `created_at` | timestamptz | auto |

Row Level Security: anon role can SELECT and INSERT; no UPDATE or DELETE.

### On screen load
Fetch top 10 rows ordered by `score desc` — shown immediately, no auth required.

### On Post score
1. INSERT the player's row
2. Re-fetch top 10
3. Query rank: `SELECT COUNT(*) FROM scores WHERE score > :playerScore` → rank = count + 1
4. Update the player's own row in the table with their name and rank

### Error handling
On any Supabase fetch/insert failure, show an inline error message chosen randomly from:
- "The leaderboard has gone bananas 🍌 — [retry]"
- "Score submission got lost in the produce aisle — [try again]"

Skip remains functional regardless of network state. Personal best tab is unaffected by Supabase errors.

### Credentials
Supabase project URL and anon key stored as constants at the top of `index.html`'s `<script>` block (not in `config.js`). Supabase JS SDK loaded via CDN `<script>` tag.

---

## Settings Integration

New "Leaderboard" section added to the settings screen with one control:

- **Default tab:** toggle "Community" / "Personal best"
- Stored in `localStorage` under `plu_lb_default`
- Defaults to "community" if unset

---

## Files Changed

| File | Change |
|---|---|
| `index.html` | Add `#leaderboard-screen` div; add leaderboard JS (show/hide, fetch, post, tab toggle, name management, score history); update `endGame()` to call `showLeaderboard()`; add Supabase SDK script tag and credentials constants; add leaderboard default setting to settings screen |
| `style.css` | Add leaderboard screen styles |
| `config.js` | No changes needed — Supabase credentials go in `index.html` |
