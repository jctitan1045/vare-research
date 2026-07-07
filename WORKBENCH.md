# WORKBENCH — Vare Research

---

## Session: 2026-07-07 | Killed the auto-inject Fathom sync (2nd corruption) → notify-only + deploy smoke-check

**Focus:** Root-cause and fix the recurring Actions corruption of index.html.

**What happened:**
- 2nd corruption confirmed: cloud Action commit `8b73f4a` "Auto: add Jul 7 call" grabbed the WRONG call (re-added Armin Shafee, already id:12) AND spliced a quoted-key JSON object *into Andrew Topping's (id:1) `gaps` array* — a syntax error that blanks the whole live dashboard. Same class of bug as the 2026-07-03 incident (ids 12–15).
- Root causes in the old `scripts/update_calls.py`: (1) `inject_participant()` regex `(.*?)(\]\s*\})` is non-greedy and matched the FIRST `]}` (end of participant 1's gaps + object), splicing the new record inside id:1 instead of at the array end; (2) it wrapped the LLM's quoted-key JSON (`{ "name":... }`) inside its own `{ id, date, fathomUrl, ... }`, producing a nested unkeyed `{` = invalid JS; (3) name-dedup was unreliable. Parsing/editing live JS with regex is inherently fragile.
- **[DECISION] Retired auto-injection entirely** (WORKBENCH had leaned "keep cloud Action"; two corruptions overruled that). No process auto-edits index.html anymore. Manual add is what correctly shipped both Jul 7 calls anyway.
- Rewrote the cloud Action as **notify-only**: `.github/workflows/update-calls.yml` → `scripts/notify_new_calls.py` detects Fathom research calls not yet on the dashboard (guest name from `calendar_invitees` / title, loose-matched against `id:N, name:"..."`) and opens/updates a GitHub issue. Only needs `FATHOM_API_KEY`; no Anthropic, no commit, no file writes. Verified live: correctly saw ids 12/14/15 as present.
- Added `scripts/notify_skip.txt` (Jonas Arequipa / call 731099771 = the known failed Jul 2 call) so intentionally-excluded calls don't nag daily.
- Added **JS smoke-check** `scripts/validate_index.js` — evals the `const DATA` block in a VM and asserts participants/ids/shape. Verified it PASSES on current index.html and FAILS on the corrupt `8b73f4a` blob. Wired as a **required gate in `deploy-pages.yml`** before upload, so no broken DATA block (manual or automated) can ever deploy.
- Deleted the dangerous `scripts/update_calls.py`. Added `.gitignore` (ephemeral `fathom_new_calls.md`, `.DS_Store`).
- Local duplicate `vare-fathom-sync` scheduled task was **already** out of the active dir (now `~/.claude/scheduled-tasks-retired/`); added a prominent RETIRED banner to its SKILL.md so it's never re-enabled.

**Files touched:**
- `scripts/notify_new_calls.py` (new), `scripts/validate_index.js` (new), `scripts/notify_skip.txt` (new)
- `scripts/update_calls.py` (deleted)
- `.github/workflows/update-calls.yml` (notify-only rewrite), `.github/workflows/deploy-pages.yml` (smoke-check gate)
- `.gitignore` (new)
- `~/.claude/scheduled-tasks-retired/vare-fathom-sync/SKILL.md` (RETIRED banner — external to repo)

**Still open / NEXT:**
- **Not committed/pushed** — changes are in the working tree. Review, then push to `main`; the notify-only Action and the deploy gate only take effect once on GitHub. Pushing also runs the smoke-check on the current (valid) index.html.
- Optional: prune unreferenced original mood-board images (`design-sauna.jpg`, etc.) per 2026-07-03 note.

---

## Session: 2026-07-05 | Repo moved to hub (logged from consolidation session)

**Focus:** Local folder consolidation. Logged here from the consolidation session because the working vare session did not write its own close entry.

**What happened:**
- Repo moved locally from `~/Projects/vare-research` → `~/Claude Code/vare-research` as part of consolidating all of Jordan's projects under one hub (`~/Claude Code/`).
- GitHub remote (`jctitan1045/vare-research`), branches, GitHub Pages deploy, and the `update-calls` Actions workflow are all UNCHANGED — cloud runs from the repo, not the local folder. Work from the new path going forward.
- Updated the hardcoded old path in the `vare-fathom-sync` Claude Code scheduled task (`~/.claude/scheduled-tasks/vare-fathom-sync/SKILL.md`) to the new location, and quoted its `cd` command (the new path contains a space).

**Still open:**
- [DECISION NEEDED] The `vare-fathom-sync` Claude task and the cloud `update-calls.py` Action do the identical Fathom→participant→push job. The 2026-07-03 entry records an `[INCIDENT]` where the Actions sync injected malformed JS and broke participants id:12–15 — so this duplication has already caused corruption. Recommend retiring one (keep the cloud Action).
- Untracked in the folder after move: `.claude/`, `.DS_Store`, `PROP 01 VARÉ.pdf` — triage/commit or gitignore as appropriate.

**Files touched:**
- No repo file content changed here (path fix was in the external scheduled-task SKILL.md, not this repo).

---

## Session: 2026-07-03 | Dashboard Polish — Collages, Quote Clusters, Roadmap, Work Type

**Focus:** Dashboard visual improvements and content depth

**What happened:**
- Added 2 new product roadmap verticals: Community Events & Practitioner Services (7 total)
- Restructured all `gaps` arrays from flat strings to `{theme, text}` objects — now cluster visually by tag inside each feature card
- Restructured all `quotes` arrays from flat strings to `{theme, text}` objects — 35 quotes across 11 participants assigned to 7 themes
- Rebuilt `renderQuoteWall()` to group by theme (not person) using `THEME_ORDER` — themes: Space feel & atmosphere, The gap in Medellín, Community & belonging, Recovery & reset, All-in-one vision, Barriers & friction, Movement & wellness identity
- Replaced design section's single AI image per space with a 3-photo collage from different quote-derived prompts (15 images total via Pollinations.ai FLUX, downloaded as static assets)
- Replaced D3 treemap for work type with named cluster groups — pill badges with initials + first name, color-coded by category
- [INCIDENT] GitHub Actions Fathom sync (commit 971cee9) injected malformed JS inside Andrew Topping's `gaps` array — broken participants id:12–15 (Jonas failed call + duplicates). Fixed and force-redeployed.
- [INCIDENT] GitHub Pages deploy failed transiently ("Deployment failed, try again later") — resolved by pushing empty commit to re-trigger

**Files touched:**
- `/Users/jordancarroll/Claude Code/vare-research/index.html` — all changes
- `design-sauna-[1-3].jpg`, `design-yoga-[1-3].jpg`, `design-restaurant-[1-3].jpg`, `design-social-[1-3].jpg`, `design-cowork-[1-3].jpg` — 15 new AI mood board images

**Path move logged:**
- OLD: `/Users/jordancarroll/Projects/vare-research/`
- NEW: `/Users/jordancarroll/Claude Code/vare-research/`
- GitHub remote, Pages deploy, Actions — all unchanged

**Still open:**
- Fathom auto-sync bot needs a syntax validator before it commits — it keeps injecting broken JS. Consider adding a pre-commit check in the workflow or disabling the bot entirely until the schema is fixed.
- The old `design-sauna.jpg`, `design-yoga.jpg`, `design-restaurant.jpg`, `design-social.jpg`, `design-coworking.jpg` (original single images) are still in the repo but no longer referenced — can be deleted to save space.

**Next session start:**
Continue from `~/Claude Code/vare-research/` (new path). Dashboard is live and clean at jctitan1045.github.io/vare-research.

---

## Session: 2026-06-27 | Market Research Scraping

**Focus:** Customer discovery — sourcing review data from physical wellness venues

**What happened:**
- Attempted Reddit scraping (r/sauna, r/medellin, r/biohacking, r/coldplunge, r/digitalnomad, Othership threads) — blocked by Reddit's 403 lockdown post-2023 API changes
- Attempted Reddit OAuth API via old.reddit.com/prefs/apps — blocked by Reddit's new Responsible Builder Policy review requirement
- [DECISION] Pivoted to App Store reviews as proxy — pulled 4,515 reviews across: Othership (booking + breathwork), Perspire Sauna, Remedy Place, Life Time, Soho House, Equinox, Wim Hof, Mindbody, SmartFit (CO/BR/MX), Bodytech (CO)
- [DECISION] User correctly redirected: App Store is the wrong source. Physical location reviews (Yelp, Google) are the target. Session ended before completing this pivot.

**Still open:**
- Yelp scraper for physical locations: Othership Toronto, Remedy Place NYC/LA, HigherDOSE NYC, Bathhouse NYC/Brooklyn, Perspire Sauna locations, wellness centers in Medellín
- Google Maps reviews (harder — likely needs Places API or SerpAPI)
- Drop collected data into NotebookLM and run emotional driver analysis
- Ask NotebookLM: "What do people say they wish existed?" / "Why do people leave premium wellness clubs?" / "What language do they use to describe themselves?"

**Files touched:**
- `/Users/jordancarroll/Downloads/wellness_wide_reviews.json` — 4,515 App Store reviews (pivot away from these)
- `/Users/jordancarroll/Downloads/wellness_wide_reviews_notebooklm.txt` — same, formatted for NotebookLM
- `/Users/jordancarroll/Downloads/othership_reviews.json` — Othership-only first pass
- `/Users/jordancarroll/Downloads/othership_reviews_notebooklm.txt` — same
- `/tmp/wide_review_scraper.py` — App Store scraper script
- `/tmp/review_scraper.py` — Othership-only scraper script

**Next session start:**
Build a Yelp scraper targeting physical wellness locations. Key targets:
- Othership (Toronto) — yelp.com/biz/othership-toronto
- Remedy Place (NYC + LA)
- HigherDOSE (NYC infrared sauna)
- Bathhouse (Brooklyn)
- Perspire Sauna (multiple US locations)
- Medellín wellness/spa: search Yelp + Google for "wellness center Medellín", "spa Medellín", "sauna Medellín"
- Bodytech Medellín (specific locations)
- 108 Yoga Medellín (Andrew's reference)

If Yelp blocks: fall back to SerpAPI ($50/mo) or Outscraper for Google reviews.

---

## Session: 2026-06-25/26 | Dashboard + Discovery Script Build

**Focus:** Build market research infrastructure from scratch

**What happened:**
- Built customer discovery script (Call 1, 30 min, pure discovery — no concept reveal)
- [DECISION] No brand/concept reveal on Call 1 — brand not ready. Call 2 = reveal.
- [DECISION] Ranking section moved to first in call flow
- Created DOCX version of script with teal callout boxes, ranking items, capture table
- Created dark HTML ranking slide for screen sharing (Vare_Ranking_Slide.html)
- Built live research dashboard (index.html) — data-driven, Chart.js, GitHub Pages
- Loaded Andrew Topping's call data (Jun 25): 19 services with context notes, demographics, 3 quotes, gap tags, price calibration, competitors, referrals
- [DECISION] Services stored as {name, note} objects (not just keyword tags) — richer context
- Added demographics section: 4 metric cards + 5 bar charts (nationality, work type, tenure, neighborhood, community)
- Added aggregate "Services in demand" chart — horizontal bar, sorted by frequency across all calls
- [DECISION] GitHub Pages for all hosting (not Netlify Drop — expires). Repo: github.com/jctitan1045/vare-research
- Fathom call naming convention confirmed: "Wellness Center Market Research Call"

**Files touched:**
- `/Users/jordancarroll/Claude Code/vare-research/index.html` — live dashboard (GitHub Pages)
- `/Users/jordancarroll/Downloads/Vare_Discovery_Script_Call1.md` — discovery script
- `/Users/jordancarroll/Downloads/Vare_Discovery_Script_Call1.docx` — formatted DOCX
- `/Users/jordancarroll/Downloads/Vare_Ranking_Slide.html` — screen share slide

**Still open from this session:**
- Add 7 demographic questions to discovery script and rebuild DOCX
- Community leader branch (removed per user request, offered to add back as optional section)
