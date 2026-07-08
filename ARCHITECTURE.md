# ARCHITECTURE — Vare Research

## What this project is

Market research infrastructure for the Vare Wellness Center (Medellín). Tracks customer discovery calls and competitive intelligence. Shared with business partner Lorenzo via live GitHub Pages URL.

---

## Dashboard (index.html)

**Live URL:** https://jctitan1045.github.io/vare-research/
**Repo:** https://github.com/jctitan1045/vare-research
**Hosting:** GitHub Pages — auto-deploys on push to main. No build step.

**Data model:** All participant data lives in a single `DATA.participants` JS array at the top of `index.html`. Adding a new call = adding one object to the array. All charts and cards render dynamically from this array.

**Participant object shape:**
```js
{
  id, name, date, fathomUrl,
  nationality, age, workType, workDetail,
  tenure, neighborhood, community, source,
  wellnessNote,
  rankingTop3, primaryDraw, socialMode,
  monthlySpend: { "Place": amountCOP },
  priceGoodDeal, priceCeiling, dayPassRange,
  replaceVsAdd,
  competitorsStayed, competitorsLeft,
  locationPull,
  call2, referrals,
  services: [{ name, note }],   // what they want + why
  quotes: ["...", "...", "..."], // top 3 verbatim
  gaps: [{ tag, text }]
}
```

**Sections rendered:**
1. Demographics — 4 metric cards + 5 bar charts (nationality, work type, tenure, neighborhood, community)
2. Aggregate "Services in demand" — horizontal bar chart, sorted by frequency across all calls
3. Per-call profile cards — ranking top 3, spend, price calibration, competitors, services with notes, 3 quotes
4. Gap section — aggregated across all calls
5. Patterns to watch

**Dependencies:** Chart.js 4.4.1 via cdnjs CDN. No build tools, no npm, no framework.

---

## Discovery Script

**Files:**
- `Vare_Discovery_Script_Call1.md` — source of truth (markdown)
- `Vare_Discovery_Script_Call1.docx` — formatted Word version for printing / sharing
- `Vare_Ranking_Slide.html` — dark HTML slide for screen sharing during calls

**Call flow (30 min):**
1. Opening (1 min) — permission + Fathom start
2. Ranking (2 min) — show slide, get top 2-3 picks
3. Life mapping (7 min) — current habits, named places, spend, why they choose/leave
4. Location (2 min) — neighborhood map slide
5. Gap diagnostic (8 min) — what would make it an easy yes/no, $100 hypothetical
6. Soft close (2 min) — permission for Call 2, referrals
7. Buffer (6 min)

**Call 1 rule:** Pure discovery. No concept reveal. No brand. No hard ask.
**Call 2:** Brand reveal, space concept, founding membership offer.

---

## Research Data (competitive intelligence)

**Location:** `/Users/jordancarroll/Downloads/`

| File | Contents |
|------|----------|
| `wellness_wide_reviews.json` | 4,515 App Store reviews (Othership, Equinox, Life Time, Soho House, SmartFit CO, Bodytech CO, etc.) |
| `wellness_wide_reviews_notebooklm.txt` | Same — formatted for NotebookLM upload |
| `othership_reviews.json` | Othership-only (330 reviews) |

**Note:** These are App Store reviews. Next step is Yelp/Google reviews for physical venue experiences.

---

## Fathom Integration (NOTIFY-ONLY as of 2026-07-07)

- Call naming convention: **"Wellness Center Market Research Call"**
- **Adding a call is manual + verified.** Pull the transcript (Fathom MCP or fathom.video), add one object to `DATA.participants` in `index.html`, push. No automation edits the file — the old auto-injector corrupted the live site twice and was retired.
- **`scripts/notify_new_calls.py`** (cloud `update-calls.yml`, daily `0 4 * * *` + manual dispatch): detects research calls in Fathom not yet on the dashboard (guest from `calendar_invitees`/title, loose-matched against `id:N, name:"…"`), and opens/updates a GitHub issue. Needs only `FATHOM_API_KEY`. Never writes `index.html`, never commits. `scripts/notify_skip.txt` lists calls to ignore (e.g. failed calls).
- **`scripts/validate_index.js`** — JS smoke-check that evals the `const DATA` block and asserts participant/id/shape validity. Runs as a **required gate in `deploy-pages.yml`** before every Pages deploy, so a broken DATA block can never ship. Run locally with `node scripts/validate_index.js`.
- Retired duplicate: the Claude Code scheduled task `vare-fathom-sync` (now under `~/.claude/scheduled-tasks-retired/`) did the same auto-add job — do not re-enable.
