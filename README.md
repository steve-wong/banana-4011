# 🍌 Banana 4011 — The PLU Code Quiz Game

> _Can you tell your 4011 from your 4384? Your Fuji from your Gala? Your jicama from your... wait, what even is jicama?_

**Banana 4011** is a fast-paced produce guessing game for anyone who's ever stood at a register and stared blankly at a pile of mystery fruit. Pick the right PLU code before the timer runs out, build streaks, and climb the leaderboard.

🎮 **[Play now →](https://steve-wong.github.io/banana-4011/)**

---

## Who's this for?

**New cashiers in training** — There's no shame in looking up a PLU. But imagine the confidence of just *knowing* that bananas are 4011, that Roma tomatoes are 4087, or that the weird lumpy thing the customer swears is "just a squash" is actually a chayote (4761). A few rounds a day and you'll be flying through the keypad.

**Veteran cashiers** — Think you've seen it all? Put your speed to the test. The timer goes down to 1 second. Yes, really.

**Curious humans** — Ever wonder what the difference between a Fuyu and a Hachiya persimmon is? Or how to tell conventional from organic just by the PLU number? You'll pick up little gems of produce knowledge after every round whether you get the answer right or not.

---

## How to play

1. A produce item appears — name, variety, emoji, and a photo
2. Four PLU codes show up as choices
3. Pick the right one before the timer hits zero
4. Correct answers earn **10 points** — string together 3 or more in a row for a **+5 streak bonus** per answer
5. After each round you'll see the correct code plus a fun fact about the item
6. After 10 rounds, your score is posted to the leaderboard

---

## Features

- **78 produce items** spanning fruits, vegetables, herbs, and things you'll need to Google
- **Adjustable timer** — 1 to 10 seconds (settings page)
- **Streak bonuses** to reward hot hands
- **Fun facts and memory tips** after every round to help the codes actually stick
- **Community leaderboard** — see how you stack up against other players
- **Personal best tracking** — your high score is saved locally

---

## The secret to organic PLUs

Conventional PLUs are 4 digits starting with `3` or `4`. Organic? Just slap a `9` in front. Organic banana = **94011**. Once you know the trick, half the codes become free points.

---

## Running locally

No build step, no dependencies — just open `index.html` in a browser. For live reloading during development:

```bash
python3 -m http.server
# or
npx serve .
```

---

## Contributing

Spot a wrong PLU? Know a better memory tip for a tricky code? PRs welcome. All produce data lives in `produce.js` — each entry has a PLU, name, variety, emoji, fun fact, quality notes, and a memory tip.

---

_4011. Always 4011._
