# USER GUIDE — Waha Research

## Adding a new discovery call to the dashboard

1. Pull the transcript from Fathom (name it "Wellness Center Market Research Call")
2. Open `/Users/jordancarroll/Claude Code/vare-research/index.html`
3. Add a new object to `DATA.participants` array — copy the Andrew object as a template
4. Fill in all fields from the transcript
5. (Optional but recommended) Sanity-check before pushing: `node scripts/validate_index.js` — catches any typo that would break the whole dashboard
6. Push to GitHub: `cd /Users/jordancarroll/Claude Code/vare-research && git add index.html && git commit -m "Add [name] call" && git push`
7. Dashboard live URL updates automatically: https://jctitan1045.github.io/vare-research/ — the deploy re-runs the same smoke-check and will refuse to publish a broken `DATA` block

**Heads up on new calls:** a daily GitHub Action checks Fathom and opens a GitHub issue when a research call isn't on the dashboard yet, so you don't have to remember. It only notifies — it never edits the dashboard. To silence a call you're intentionally skipping (e.g. a failed one), add its guest name or Fathom call-id to `scripts/notify_skip.txt`.

## Running a discovery call

1. Open `Vare_Discovery_Script_Call1.docx` (printed or on second screen)
2. Open `Vare_Ranking_Slide.html` in browser — share screen when you hit the Ranking section
3. Start Fathom recording after the opening exchange
4. Follow timing: Opening 1min → Ranking 2min → Life mapping 7min → Location 2min → Gap diagnostic 8min → Soft close 2min
5. Fill capture table immediately after the call

## Key rules for Call 1

- No concept reveal — don't describe what you're building
- No brand name — just "I'm working on something in this space"
- No hard ask — the $100 question is hypothetical, not a real ask
- Goal: get Call 2 permission + referrals

## Sharing the dashboard

Live URL: **https://jctitan1045.github.io/vare-research/**
Share directly with Lorenzo or anyone else. Always up to date.

## Files reference

| File | Where |
|------|-------|
| Live dashboard | https://jctitan1045.github.io/vare-research/ |
| Dashboard source | `/Users/jordancarroll/Claude Code/vare-research/index.html` |
| Discovery script (DOCX) | `/Users/jordancarroll/Downloads/Vare_Discovery_Script_Call1.docx` |
| Ranking slide | `/Users/jordancarroll/Downloads/Vare_Ranking_Slide.html` |
| Othership reviews | `/Users/jordancarroll/Downloads/othership_reviews_notebooklm.txt` |
| Wide wellness reviews | `/Users/jordancarroll/Downloads/wellness_wide_reviews_notebooklm.txt` |
