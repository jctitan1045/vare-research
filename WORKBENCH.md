# WORKBENCH — Vare Research

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
- `/Users/jordancarroll/Projects/vare-research/index.html` — live dashboard (GitHub Pages)
- `/Users/jordancarroll/Downloads/Vare_Discovery_Script_Call1.md` — discovery script
- `/Users/jordancarroll/Downloads/Vare_Discovery_Script_Call1.docx` — formatted DOCX
- `/Users/jordancarroll/Downloads/Vare_Ranking_Slide.html` — screen share slide

**Still open from this session:**
- Add 7 demographic questions to discovery script and rebuild DOCX
- Community leader branch (removed per user request, offered to add back as optional section)
