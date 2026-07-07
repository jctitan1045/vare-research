#!/usr/bin/env python3
"""
Fathom -> dashboard NOTIFIER (detect only, never mutate).

This replaces the old auto-injector (scripts/update_calls.py), which spliced
LLM-generated JS straight into index.html and corrupted the dashboard twice
(2026-07-03 broke ids 12-15; 2026-07-07 commit 8b73f4a re-added the wrong guest
and injected malformed JSON into another participant's `gaps` array, blanking the
whole site). We no longer auto-edit the dashboard. This script only *tells* Jordan
that a new research call exists so he can hand-add + verify it.

What it does:
  1. Pulls "Wellness Center Market Research Call" meetings from the last N days.
  2. Reads the guest name from each meeting (calendar invitees / title).
  3. Compares against the participant names already in index.html.
  4. Reports the un-added calls (date, guest, Fathom link) to stdout, to the
     GitHub Actions step summary, and to fathom_new_calls.md (issue body).
  5. Emits new_count via $GITHUB_OUTPUT so the workflow can open an issue.

It NEVER writes index.html and NEVER commits. Only FATHOM_API_KEY is required.
"""

import os, re, sys, json, datetime
import urllib.request, urllib.error, urllib.parse

FATHOM_API_KEY  = os.environ["FATHOM_API_KEY"]
CALL_NAME_MATCH = "wellness center market research call"
LOOKBACK_DAYS   = int(os.environ.get("LOOKBACK_DAYS", "7"))
INDEX_HTML      = os.path.join(os.path.dirname(__file__), "..", "index.html")
ISSUE_BODY_FILE = os.path.join(os.path.dirname(__file__), "..", "fathom_new_calls.md")
SKIP_FILE       = os.path.join(os.path.dirname(__file__), "notify_skip.txt")
# Jordan / the recorder — never treated as the "guest" of a research call.
OWNER_EMAILS    = {"jordan@jordanscarroll.com"}


def fathom_request(path, params=None):
    url = f"https://api.fathom.ai/external/v1{path}"
    if params:
        query = "&".join(f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items())
        url = f"{url}?{query}"
    req = urllib.request.Request(url, headers={"X-Api-Key": FATHOM_API_KEY})
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())


def load_skiplist():
    """Tokens (guest names or Fathom call-id substrings) to intentionally ignore,
    e.g. failed/aborted calls Jordan chose not to add. One per line, '#' comments."""
    tokens = []
    try:
        with open(SKIP_FILE) as f:
            for line in f:
                line = line.split("#", 1)[0].strip()
                if line:
                    tokens.append(line.lower())
    except FileNotFoundError:
        pass
    return tokens


def is_skipped(label, url, skiplist):
    hay = (label + " " + url).lower()
    return any(tok in hay for tok in skiplist)


def existing_participant_names(html):
    """Top-level participant names only (id:N, name:"..."), not nested service names."""
    return [m.strip() for m in re.findall(r'id:\s*\d+\s*,\s*name:\s*"([^"]+)"', html)]


def bogota_date(iso_str):
    """Format an ISO timestamp as 'Jul 7, 2026' in Colombia time (UTC-5, no DST)."""
    if not iso_str:
        return "Unknown date"
    try:
        dt = datetime.datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        dt = dt.astimezone(datetime.timezone(datetime.timedelta(hours=-5)))
        return dt.strftime("%b %-d, %Y")
    except ValueError:
        return iso_str[:10]


def guest_names(meeting):
    """Best-effort external guest name(s) for a research call."""
    names = []
    for inv in meeting.get("calendar_invitees") or []:
        email = (inv.get("email") or "").lower()
        if inv.get("is_external") and email not in OWNER_EMAILS and inv.get("name"):
            names.append(inv["name"].strip())
    if names:
        return names
    # Fallback: parse the guest out of the title, e.g.
    # "Wellness Center Market Research Call - Zach Cohen and Jordan Carroll"
    title = meeting.get("title") or meeting.get("meeting_title") or ""
    tail = re.split(r'[-–:]', title, maxsplit=1)
    if len(tail) == 2:
        people = re.split(r'\band\b|,|&|\+', tail[1])
        people = [p.strip() for p in people if p.strip() and "jordan" not in p.lower()]
        if people:
            return people
    return []


def name_already_present(guest, existing):
    """Loose match: dashboard uses labels like 'Juan Pablo (Duet Fitness)' while the
    invitee is 'Juan Pablo Madrid'. Match on shared first+last tokens, either direction.
    When unsure we report as NEW — over-notifying is safe; a human verifies."""
    g = guest.lower()
    g_core = re.sub(r"\(.*?\)", "", g).strip()
    for e in existing:
        el = e.lower()
        e_core = re.sub(r"\(.*?\)", "", el).strip()
        if g_core and (g_core in el or e_core in g or e_core == g_core):
            return True
        # first + last token overlap
        gt, et = g_core.split(), e_core.split()
        if gt and et and gt[0] == et[0] and (len(gt) < 2 or len(et) < 2 or gt[-1] == et[-1]):
            return True
    return False


def main():
    today = datetime.date.today()
    cutoff = f"{(today - datetime.timedelta(days=LOOKBACK_DAYS)).isoformat()}T00:00:00Z"
    before = f"{(today + datetime.timedelta(days=1)).isoformat()}T00:00:00Z"

    print(f"Fetching Fathom meetings {cutoff} .. {before}")
    try:
        data = fathom_request("/meetings", {"created_after": cutoff, "created_before": before})
    except urllib.error.HTTPError as e:
        print(f"Fathom API error: {e.code} {e.reason}", file=sys.stderr)
        sys.exit(1)

    items = data.get("items") if isinstance(data, dict) else data
    items = items or []
    research = [m for m in items
                if CALL_NAME_MATCH in ((m.get("title") or m.get("meeting_title") or "").lower())]
    print(f"Found {len(research)} research call(s) in window.")

    with open(INDEX_HTML) as f:
        existing = existing_participant_names(f.read())
    print(f"Dashboard currently has {len(existing)} participants.")
    skiplist = load_skiplist()

    new_calls = []
    for m in research:
        when = m.get("recording_start_time") or m.get("scheduled_start_time") or m.get("created_at")
        date = bogota_date(when)
        url = m.get("url") or m.get("share_url") or ""
        guests = guest_names(m) or ["(guest name not found — check the call)"]
        present = any(name_already_present(g, existing) for g in guests if "not found" not in g)
        label = " & ".join(guests)
        if present:
            status = "already in dashboard"
        elif is_skipped(label, url, skiplist):
            status = "skipped (notify_skip.txt)"
        else:
            status = "NOT in dashboard"
        print(f"  - {date} | {label} | {status} | {url}")
        if not present and not is_skipped(label, url, skiplist):
            new_calls.append({"date": date, "guest": label, "url": url})

    # ---- write outputs -------------------------------------------------
    lines = []
    if new_calls:
        lines.append(f"**{len(new_calls)} Fathom research call(s) not yet on the dashboard.**")
        lines.append("")
        lines.append("Add each one by hand to `DATA.participants` in `index.html` "
                     "(match the existing JS style: unquoted keys, quotes/gaps as "
                     "`{theme,text}` / `{tag,text}` objects, next sequential `id`). "
                     "Pushing runs the JS smoke-check before deploy.")
        lines.append("")
        for c in new_calls:
            lines.append(f"- **{c['date']} — {c['guest']}** · [Fathom recording]({c['url']})")
    else:
        lines.append("No un-added Fathom research calls. Dashboard is up to date. ✅")
    body = "\n".join(lines) + "\n"

    with open(ISSUE_BODY_FILE, "w") as f:
        f.write(body)

    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a") as f:
            f.write("## Fathom new-call check\n\n" + body)

    gh_out = os.environ.get("GITHUB_OUTPUT")
    if gh_out:
        with open(gh_out, "a") as f:
            f.write(f"new_count={len(new_calls)}\n")

    print(f"\nnew_count={len(new_calls)}")


if __name__ == "__main__":
    main()
