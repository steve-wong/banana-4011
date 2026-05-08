# AI-Generated Produce Images — Design Spec

**Date:** 2026-05-08  
**Status:** Approved

## Goal

Generate photo-realistic AI images of all 78 produce items in the game and display them in the produce card, replacing the emoji. Each image shows a single item of the given produce. A fine-print "AI generated" label appears beneath each image.

## Image Generation

**Service:** Pollinations.ai — free, no API key, no signup required. Uses the Flux model.

**Script:** `generate_images.py` at the project root.

**Prompt template per item:**
```
single {name} ({variety}), photorealistic, white background, grocery store produce photography, no text
```

**URL format:**
```
https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=512&nologo=true
```

**Behavior:**
- Reads `produce.js` to extract `plu`, `name`, and `variety` for each item
- Downloads images sequentially (avoids rate limits)
- Saves each image to `images/{plu}.jpg`
- Skips items where the file already exists (safe to re-run)
- In sample mode (`--sample`), generates only the first 5 items and exits

**Output:** 78 JPEG files in `images/`, one per produce item, named by PLU code.

## Game UI Changes (`index.html`)

The produce card gains an `<img>` element above the name, and the emoji is hidden by default.

**Card structure after change:**
```
<img class="produce-img" src="images/{plu}.jpg" onerror="fallback">
<p class="ai-label">AI generated</p>
[produce name]
[produce hint]
[emoji — hidden, shown only as onerror fallback]
```

**Fallback behavior:** If the image fails to load, `onerror` hides the `<img>` and the `<p class="ai-label">`, and shows the emoji span instead.

## CSS Changes (`style.css`)

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

## JavaScript Changes (`index.html` script)

In `nextRound()`, when setting up a new round:
- Set `<img src="images/{currentItem.plu}.jpg">` on the produce image element
- Hide the AI label initially (it shows when the image loads successfully)
- Keep emoji hidden; only show via the `onerror` fallback

## Out of Scope

- Regenerating images with different prompts (script is re-runnable, skip existing files)
- Hosting images remotely
- Organic variants (94xxx PLUs share the same display image as their conventional counterpart — organic items reuse the conventional PLU image)
