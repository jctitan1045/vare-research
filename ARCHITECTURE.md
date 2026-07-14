# ARCHITECTURE — Waha Research

## What this project is

Market research infrastructure for the Waha Wellness Center (Medellín). Tracks customer discovery calls and competitive intelligence. Shared with business partner Lorenzo via live GitHub Pages URL.

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
  monthlySpend: { "Place": amountCOP },     // values in "k" (thousands COP)
  priceGoodDeal, priceCeiling, dayPassRange, // all in "k"
  replaceVsAdd,
  competitorsStayed, competitorsLeft,
  locationPull,
  call2, referrals,
  supply: { type, offers, audience, model, needs }, // supply-side participants only
  featureVotes: ["<feature string>", ...],  // drives the roadmap kanban tally
  icps: [{ n:"<ICP name>", m:3|2|1 }],       // which ICP(s) + match tier (3 Strong/2 Partial/1 Loose)
  services: [{ name, note }],                // what they want + why
  quotes: [{ theme, text }],                 // verbatim, rendered with theme as label
  gaps: [{ tag, text }]
}
```

Other top-level data blocks in `index.html`: `AVATARS` (one persona per participant, surfaced inside the ICP click-through — not a standalone section), `ICPS`, `MOAT`, `MARKET_LANDSCAPE` (competitors + north-star `models`), `PRODUCT_PRIORITIES` (roadmap kanban), `LAUNCH_PLAN` (the Gantt), `SECTION_TAKEAWAYS`, `OPEN_BY_DEFAULT`.

**Currency:** COP is primary, USD in parens (~1 USD = 4,000 COP). Helper `money(k)` / `USD(k)=k/4` — values stored in "k" (thousands COP).

**Sections rendered (top→bottom):** exec summary → demographics block (led by "View data for" segment chips: All/Consumers/Supply/Locals/Expats) → Ideal Client Profiles (cards + avatar/profile click-through) → Where they want it (Leaflet map, fit-all + count bubbles) → What they'll pay (stated vs revealed) → **Where we win** (venue photo cards w/ Google Maps embeds → moat stat-strip + comparison matrix → north-star model cards) → **Product roadmap** (launch Gantt + Now/Next/Later feature kanban) → Supply side → What they said (quote wall). Collapsible sections (WAI-ARIA disclosure); core-story ones open by default.

**Segment filter:** `ACTIVE` global + `render()` is re-runnable (Chart.js `destroy` loop + Leaflet re-init guard) so chips re-render the data views.

**Photos:** venue/model cards load `assets/venues/<slug>.jpg` / `assets/models/<slug>.jpg` with a branded emoji placeholder + `onerror` fallback; banner taps expand a keyless Google Maps `output=embed` iframe (lazy). A future Maps *Embed API* key would swap these to photo-forward `place` embeds.

**Dependencies:** Chart.js 4.4.1 + Leaflet (CARTO tiles) via CDN; Google Maps `output=embed` iframes (no key). No build tools, no npm, no framework.

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
