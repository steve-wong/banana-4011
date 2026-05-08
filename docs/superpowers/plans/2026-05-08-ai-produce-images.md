# AI-Generated Produce Images Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate photo-realistic AI images for all 78 produce items via Pollinations.ai and display them in the produce card, replacing the emoji.

**Architecture:** A Python script reads produce.js, builds rich prompts from `name`+`variety`, fetches images from Pollinations.ai sequentially, and saves them as `images/{plu}.jpg`. The game's produce card gets an `<img>` element that loads the local file, with the emoji kept as an `onerror` fallback. An "AI generated" fine-print label sits below each image.

**Tech Stack:** Python 3 (stdlib only — `urllib`, `re`, `argparse`), Pollinations.ai Flux model (free, no key), vanilla JS/HTML/CSS.

---

### Task 1: Write the image generation script

**Files:**
- Create: `generate_images.py`

- [ ] **Step 1: Create `generate_images.py`**

```python
#!/usr/bin/env python3
"""Download AI-generated produce images from Pollinations.ai."""

import re
import argparse
import urllib.request
import urllib.parse
import time
import os
import sys

def parse_produce(js_path="produce.js"):
    with open(js_path) as f:
        content = f.read()
    entries = []
    # Split on object boundaries — each entry starts after a {
    blocks = re.split(r'\{(?=\s*\n?\s*plu:)', content)
    for block in blocks:
        plu = re.search(r'plu:\s*"([^"]+)"', block)
        name = re.search(r'name:\s*"([^"]+)"', block)
        variety = re.search(r'variety:\s*"([^"]+)"', block)
        if plu and name and variety:
            entries.append({
                "plu": plu.group(1),
                "name": name.group(1),
                "variety": variety.group(1),
            })
    return entries

def image_url(name, variety):
    prompt = f"single {name} ({variety}), photorealistic, white background, grocery store produce photography, no text"
    encoded = urllib.parse.quote(prompt)
    return f"https://image.pollinations.ai/prompt/{encoded}?width=512&height=512&nologo=true&model=flux"

def download(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = resp.read()
    with open(dest, "wb") as f:
        f.write(data)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample", action="store_true", help="Generate first 5 items only")
    parser.add_argument("--produce-js", default="produce.js")
    parser.add_argument("--out-dir", default="images")
    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    items = parse_produce(args.produce_js)
    if args.sample:
        items = items[:5]

    total = len(items)
    for i, item in enumerate(items, 1):
        dest = os.path.join(args.out_dir, f"{item['plu']}.jpg")
        if os.path.exists(dest):
            print(f"[{i}/{total}] {item['plu']} — skipped (exists)")
            continue
        url = image_url(item["name"], item["variety"])
        print(f"[{i}/{total}] {item['plu']} {item['name']} ... ", end="", flush=True)
        try:
            download(url, dest)
            print("ok")
        except Exception as e:
            print(f"FAILED: {e}", file=sys.stderr)
        if i < total:
            time.sleep(0.5)  # be polite to the free service

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run sample generation (5 images)**

Run from the project root (same directory as `produce.js`):

```bash
python3 generate_images.py --sample
```

Expected output (5 lines like):
```
[1/5] 3507 Cosmic Crisp Apple ... ok
[2/5] 3616 Envy Apple ... ok
[3/5] 4131 Fuji Apple ... ok
[4/5] 4135 Gala Apple ... ok
[5/5] 4017 Granny Smith Apple ... ok
```

Then confirm the files exist:
```bash
ls -lh images/ | head -10
```

Expected: 5 `.jpg` files, each 30–200 KB.

Open a few in Preview/Finder to visually verify the quality looks right (single produce item, white/clean background).

- [ ] **Step 3: Commit the script**

```bash
git add generate_images.py
git commit -m "Add Pollinations.ai image generation script"
```

---

### Task 2: Add CSS for produce image and AI label

**Files:**
- Modify: `style.css` — add `.produce-img` and `.ai-label`, update `.produce-emoji` default

- [ ] **Step 1: Open `style.css` and locate the `.produce-emoji` block (around line 137)**

It currently reads:
```css
.produce-emoji {
  font-size: 7rem;
  line-height: 1;
  display: block;
  margin-bottom: 14px;
}
```

Change `display: block` to `display: none` so the emoji is hidden by default and only appears as a fallback:
```css
.produce-emoji {
  font-size: 7rem;
  line-height: 1;
  display: none;
  margin-bottom: 14px;
}
```

- [ ] **Step 2: Add the new classes directly after `.produce-emoji`**

```css
.produce-img {
  width: 200px;
  height: 200px;
  object-fit: cover;
  border-radius: 12px;
  display: block;
  margin: 0 auto 4px;
}

.ai-label {
  font-size: 0.6rem;
  color: #aaa;
  font-style: italic;
  text-align: center;
  margin: 0 0 8px;
}
```

- [ ] **Step 3: Commit**

```bash
git add style.css
git commit -m "Add produce-img and ai-label CSS classes"
```

---

### Task 3: Update produce card HTML in `index.html`

**Files:**
- Modify: `index.html` — add `<img>` and `<p class="ai-label">` to the produce card

- [ ] **Step 1: Locate the produce card block (around line 109–114)**

It currently reads:
```html
<div class="produce-card" id="produce-card">
  <span class="produce-emoji" id="produce-emoji-fallback"></span>
  <div class="produce-name" id="produce-name">Banana</div>
  <div class="produce-hint" id="produce-hint">Yellow, conventional</div>

</div>
```

Replace it with:
```html
<div class="produce-card" id="produce-card">
  <img class="produce-img" id="produce-img" src="" alt="">
  <p class="ai-label" id="ai-label">AI generated</p>
  <span class="produce-emoji" id="produce-emoji-fallback"></span>
  <div class="produce-name" id="produce-name">Banana</div>
  <div class="produce-hint" id="produce-hint">Yellow, conventional</div>
</div>
```

- [ ] **Step 2: Commit**

```bash
git add index.html
git commit -m "Add produce image and AI generated label to produce card HTML"
```

---

### Task 4: Update `nextRound()` JS to load the image

**Files:**
- Modify: `index.html` — update the "Display produce" section of `nextRound()` (around line 265–268)

- [ ] **Step 1: Locate the "Display produce" lines in `nextRound()`**

They currently read:
```js
  // Display produce
  document.getElementById('produce-emoji-fallback').textContent = currentItem.emoji;
  document.getElementById('produce-name').textContent = currentItem.name;
  document.getElementById('produce-hint').textContent = currentItem.variety;
```

Replace with:
```js
  // Display produce
  const produceImg = document.getElementById('produce-img');
  const aiLabel = document.getElementById('ai-label');
  const emojiEl = document.getElementById('produce-emoji-fallback');

  emojiEl.textContent = currentItem.emoji;
  emojiEl.style.display = 'none';
  produceImg.style.display = 'block';
  aiLabel.style.display = 'block';
  produceImg.src = `images/${currentItem.plu}.jpg`;
  produceImg.onerror = function() {
    produceImg.style.display = 'none';
    aiLabel.style.display = 'none';
    emojiEl.style.display = 'inline';
  };

  document.getElementById('produce-name').textContent = currentItem.name;
  document.getElementById('produce-hint').textContent = currentItem.variety;
```

- [ ] **Step 2: Open `index.html` in a browser and play a round**

Verify:
- The produce photo appears in the card
- "AI generated" fine-print is visible below the image
- The emoji is NOT visible when the image loads
- Clicking a correct/wrong answer still works normally
- After each round, the next produce photo loads correctly

To test the fallback: temporarily rename one image file (e.g. `images/3507.jpg` → `images/3507.jpg.bak`), reload, and play until that produce appears — the emoji should show instead. Restore the file afterward.

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "Wire produce image src and emoji fallback in nextRound()"
```

---

### Task 5: Generate all 78 images and push

**Files:**
- Populate: `images/` directory with 78 `.jpg` files

- [ ] **Step 1: Run the full image generation**

```bash
python3 generate_images.py
```

This takes ~5–10 minutes. Watch for any `FAILED` lines in the output. If any fail, re-run the script — it skips already-downloaded files, so it will only retry the failures.

- [ ] **Step 2: Verify all 78 images are present**

```bash
ls images/*.jpg | wc -l
```

Expected: `78`

```bash
ls -lh images/*.jpg | sort -k5 -h | head -5
```

Check no file is suspiciously small (under 5 KB would indicate a failed/empty download).

- [ ] **Step 3: Spot-check a few images in browser**

Open `index.html` in a browser and play several rounds. Confirm images load and display cleanly for varied produce types (apples, citrus, root vegetables, etc.).

- [ ] **Step 4: Commit and push**

```bash
git add images/
git commit -m "Add 78 AI-generated produce photos via Pollinations.ai"
git push
```
