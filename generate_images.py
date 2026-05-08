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
