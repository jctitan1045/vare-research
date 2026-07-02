#!/usr/bin/env python3
"""
Generates mood board images for each Varé space using the DALL-E 3 API.
Images are saved to assets/moodboards/{space_id}.png and committed to the repo.

Usage:
  OPENAI_API_KEY=sk-... python scripts/generate_moodboards.py

Or run via GitHub Actions (see .github/workflows/generate-moodboards.yml).
"""

import os, sys, time, json
import urllib.request, urllib.error

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("Error: OPENAI_API_KEY environment variable not set.")
    sys.exit(1)

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "moodboards")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Prompts derived from research — keep in sync with DESIGN_PROMPTS in index.html
SPACES = [
    {
        "id": "wellness",
        "label": "Sauna + Cold Plunge",
        "prompt": (
            "A boutique wellness spa interior in Medellín, Colombia. Cedar wood sauna walls "
            "with soft amber lighting visible through a glass panel. An adjacent natural stone "
            "cold plunge pool surrounded by lush tropical plants — palms, ferns, climbing vines. "
            "A covered outdoor terrace with hanging plants. No people. Warm, private, body-safe "
            "atmosphere. Dark, intimate, and calming. Architectural Digest editorial photography style."
        )
    },
    {
        "id": "yoga",
        "label": "Yoga Studio",
        "prompt": (
            "A spacious yoga studio in a tropical Colombian wellness club. Warm oak hardwood floors. "
            "Large arched open windows with soft morning light filtering through tropical palms and "
            "ferns outside. Ceiling fans overhead. Yoga mats, blocks, and straps stored neatly at "
            "the walls. 20-30 person capacity. Warm, airy, community-oriented atmosphere. No people. "
            "Editorial interior photography style, safe and welcoming energy."
        )
    },
    {
        "id": "restaurant",
        "label": "Restaurant & Herbal Bar",
        "prompt": (
            "A health-focused restaurant and herbal bar interior in Medellín, Colombia. Colorful "
            "macro bowls and fresh ingredients displayed on a clean counter. A herbal drinks bar "
            "with adaptogen elixirs, ceremonial cacao, and functional drinks in apothecary-style "
            "bottles on wooden shelves. Natural wood furniture, tropical plants, warm light through "
            "large windows. Clean, bright, inviting. No people. Editorial food photography style."
        )
    },
    {
        "id": "social",
        "label": "Social & Event Space",
        "prompt": (
            "A flexible community event space in a Medellín wellness club. Warm wood floors. "
            "Floor cushions and movable rattan chairs arranged in small intimate circles. Exposed "
            "wood beam ceiling. Lush tropical plants throughout. Open archways leading to a terrace "
            "with natural light. Soft warm evening lighting. No people. Designed for community "
            "gathering — circle formats, not rows. Architectural photography style."
        )
    },
    {
        "id": "coworking",
        "label": "Co-working Zone",
        "prompt": (
            "A warm boutique co-working café in Medellín, Colombia. Individual work tables with "
            "warm amber lighting and comfortable seating. Lush tropical plants and hanging ferns "
            "throughout. High ceilings with natural skylight. A herbal coffee and drinks bar "
            "visible in the background. Quiet, familiar, third-home atmosphere — calm, not trendy. "
            "No people. Editorial interior photography style."
        )
    }
]


def generate_image(prompt, label):
    payload = json.dumps({
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,
        "size": "1792x1024",
        "quality": "standard",
        "response_format": "url"
    }).encode()

    req = urllib.request.Request(
        "https://api.openai.com/v1/images/generations",
        data=payload,
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        resp = json.loads(r.read())

    return resp["data"][0]["url"]


def download_image(url, path):
    with urllib.request.urlopen(url, timeout=30) as r:
        with open(path, "wb") as f:
            f.write(r.read())


def main():
    print(f"Generating {len(SPACES)} mood board images via DALL-E 3...\n")
    results = []

    for i, space in enumerate(SPACES):
        out_path = os.path.join(OUTPUT_DIR, f"{space['id']}.png")
        print(f"[{i+1}/{len(SPACES)}] {space['label']}...")

        try:
            image_url = generate_image(space["prompt"], space["label"])
            download_image(image_url, out_path)
            print(f"  ✓ Saved to assets/moodboards/{space['id']}.png")
            results.append({"id": space["id"], "status": "ok"})
        except Exception as e:
            print(f"  ✗ Failed: {e}")
            results.append({"id": space["id"], "status": "error", "error": str(e)})

        # Respect DALL-E 3 rate limit (5 images/min on tier 1)
        if i < len(SPACES) - 1:
            time.sleep(13)

    ok = sum(1 for r in results if r["status"] == "ok")
    print(f"\nDone: {ok}/{len(SPACES)} images generated.")

    if ok < len(SPACES):
        sys.exit(1)


if __name__ == "__main__":
    main()
