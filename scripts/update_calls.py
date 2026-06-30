#!/usr/bin/env python3
"""
Daily Fathom → dashboard sync.

Finds any "Wellness Center Market Research Call" meetings from the past 48 hours,
uses Claude to extract a participant object, and appends it to DATA.participants
in index.html if the participant isn't already present.

Required env vars:
  FATHOM_API_KEY       — from fathom.video/settings/api
  ANTHROPIC_API_KEY    — from console.anthropic.com
"""

import os, re, json, sys, datetime
import urllib.request, urllib.error

FATHOM_API_KEY    = os.environ["FATHOM_API_KEY"]
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
CALL_NAME_MATCH   = "Wellness Center Market Research Call"
INDEX_HTML        = os.path.join(os.path.dirname(__file__), "..", "index.html")

PARTICIPANT_SCHEMA = """\
{
  id,           // next integer (auto-assigned by script)
  name,         // "First Last"
  date,         // "Jun 30, 2026"
  fathomUrl,    // direct link to recording
  nationality,  // "Canadian" / "American" / etc.
  age,          // number or null
  workType,     // "Entrepreneur" / "Remote employee" / etc.
  workDetail,   // one-line description
  tenure,       // "1-3yrs" / "7yrs on/off" / etc.
  neighborhood, // "Poblado" / "Laureles" / etc.
  community,    // "Men of Mastery" / "Run Club" / etc.
  source,       // how Jordan knows them
  wellnessNote, // brief wellness background
  rankingTop3,  // ["Food","Mental reset","Movement"]
  primaryDraw,  // one-line summary of what would pull them in
  socialMode,   // "Solo" / "Small group" / "Community"
  monthlySpend, // { "Place name": amountInCOP_thousands }
  priceGoodDeal,// number (COP thousands/month that feels like a deal)
  priceCeiling, // number (max they'd pay COP thousands/month)
  dayPassRange, // [min, max] or null
  replaceVsAdd, // "Replace" / "Add-on" / "Replace + consolidate"
  competitorsStayed, // ["name", ...]  places they currently use
  competitorsLeft,   // ["name", ...]  places they dropped
  locationPull, // "Poblado" / "Laureles" / etc.
  call2,        // true/false — did they give Call 2 permission?
  referrals,    // ["Name (role)", ...]
  services: [{ name, note }],  // services they want, with why
  quotes: ["...", "...", "..."],// top 3 verbatim quotes
  gaps: [{ tag, text }]        // what stands between them and a yes
}
"""

EXTRACTION_PROMPT = """\
You are extracting market research data from a wellness center discovery call transcript.

Return ONLY a single valid JavaScript object literal (no variable declaration, no markdown fences, no extra text) that matches this schema exactly:

{schema}

Rules:
- Use null for any field you cannot determine from the transcript.
- For monthlySpend, express amounts in COP thousands (e.g., 350 means 350,000 COP).
- For priceGoodDeal and priceCeiling, also use COP thousands.
- Keep quotes verbatim from the transcript.
- For gaps, use a short tag like "Proof" / "Quality" / "Location" and a one-sentence text.
- Do NOT add the id field — the script will assign it.
- Do NOT add the fathomUrl field — the script will set it.

Transcript:
---
{transcript}
---
""".format(schema=PARTICIPANT_SCHEMA, transcript="{transcript}")


def fathom_request(path, params=None):
    url = f"https://api.fathom.video/v1{path}"
    if params:
        query = "&".join(f"{k}={v}" for k, v in params.items())
        url = f"{url}?{query}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {FATHOM_API_KEY}"})
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())


def anthropic_extract(transcript, url):
    prompt = EXTRACTION_PROMPT.replace("{transcript}", transcript[:40000])
    payload = json.dumps({
        "model": "claude-sonnet-4-6",
        "max_tokens": 4096,
        "messages": [{"role": "user", "content": prompt}]
    }).encode()
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
    )
    with urllib.request.urlopen(req) as r:
        resp = json.loads(r.read())
    raw = resp["content"][0]["text"].strip()
    # Strip any accidental markdown fences
    raw = re.sub(r"^```[a-z]*\n?", "", raw)
    raw = re.sub(r"\n?```$", "", raw)
    return raw.strip()


def get_existing_names(html):
    """Extract names already in DATA.participants to avoid duplicates."""
    return set(re.findall(r'name:\s*["\']([^"\']+)["\']', html))


def get_next_id(html):
    ids = list(map(int, re.findall(r'\bid:\s*(\d+)', html)))
    return max(ids) + 1 if ids else 1


def inject_participant(html, obj_literal, next_id, fathom_url, recording_date):
    # Add the id and fathomUrl that the LLM was told to omit
    obj_with_meta = (
        f"  {{\n"
        f"    id:{next_id},\n"
        f"    date:\"{recording_date}\",\n"
        f"    fathomUrl:\"{fathom_url}\",\n"
        + "\n".join("    " + line for line in obj_literal.splitlines()
                    if not re.match(r'\s*(id|date|fathomUrl)\s*:', line))
        + "\n  }"
    )

    # Insert before the closing ]; of DATA.participants
    pattern = r'(const DATA\s*=\s*\{[^}]*participants\s*:\s*\[)(.*?)(\]\s*\})'
    def replacer(m):
        existing = m.group(2).rstrip()
        sep = ",\n" if existing else ""
        return m.group(1) + existing + sep + "\n" + obj_with_meta + "\n" + m.group(3)

    new_html, count = re.subn(pattern, replacer, html, count=1, flags=re.DOTALL)
    if count == 0:
        raise RuntimeError("Could not find DATA.participants array in index.html")
    return new_html


def format_date(iso_str):
    """Convert '2026-06-30T...' to 'Jun 30, 2026'."""
    d = datetime.datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
    return d.strftime("%b %-d, %Y")


def main():
    cutoff = (datetime.datetime.utcnow() - datetime.timedelta(hours=48)).isoformat() + "Z"

    print("Fetching recent Fathom meetings...")
    try:
        data = fathom_request("/meetings", {"limit": 50})
    except urllib.error.HTTPError as e:
        print(f"Fathom API error: {e.code} {e.reason}")
        sys.exit(1)

    meetings = data.get("data") or data.get("meetings") or []
    research_calls = [
        m for m in meetings
        if CALL_NAME_MATCH.lower() in (m.get("title") or m.get("name") or "").lower()
        and (m.get("started_at") or m.get("created_at") or "") >= cutoff
    ]

    if not research_calls:
        print("No new research calls found in the past 48 hours.")
        return

    with open(INDEX_HTML, "r") as f:
        html = f.read()

    existing_names = get_existing_names(html)
    changed = False

    for meeting in research_calls:
        mid = meeting.get("id") or meeting.get("recording_id")
        title = meeting.get("title") or meeting.get("name") or ""
        started = meeting.get("started_at") or meeting.get("created_at") or ""
        recording_url = meeting.get("share_url") or meeting.get("url") or f"https://fathom.video/calls/{mid}"

        print(f"Processing: {title} ({started[:10]})")

        # Get transcript
        try:
            tx_data = fathom_request(f"/meetings/{mid}/transcript")
        except urllib.error.HTTPError as e:
            print(f"  Could not fetch transcript: {e.code} — skipping")
            continue

        transcript_text = tx_data.get("transcript") or tx_data.get("text") or ""
        if not transcript_text:
            utterances = tx_data.get("utterances") or tx_data.get("segments") or []
            transcript_text = "\n".join(
                f"{u.get('speaker','')}: {u.get('text','')}" for u in utterances
            )

        if not transcript_text.strip():
            print("  Empty transcript — skipping")
            continue

        # Extract participant object via Claude
        print("  Extracting participant data via Claude...")
        try:
            obj_literal = anthropic_extract(transcript_text, recording_url)
        except Exception as e:
            print(f"  Claude extraction failed: {e} — skipping")
            continue

        # Check for duplicate (match on name field inside the extracted object)
        name_match = re.search(r'name\s*:\s*["\']([^"\']+)["\']', obj_literal)
        extracted_name = name_match.group(1) if name_match else None
        if extracted_name and extracted_name in existing_names:
            print(f"  {extracted_name} already in dashboard — skipping")
            continue

        next_id = get_next_id(html)
        recording_date = format_date(started) if started else "Unknown"

        html = inject_participant(html, obj_literal, next_id, recording_url, recording_date)
        existing_names.add(extracted_name or "")
        changed = True
        print(f"  Added participant #{next_id}: {extracted_name}")

    if changed:
        with open(INDEX_HTML, "w") as f:
            f.write(html)
        print("index.html updated.")
    else:
        print("No changes made.")


if __name__ == "__main__":
    main()
