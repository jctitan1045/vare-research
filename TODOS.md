# TODOS — Vare Research

## Active

- [ ] **Delete orphaned single mood board images** — `design-sauna.jpg`, `design-yoga.jpg`, `design-restaurant.jpg`, `design-social.jpg`, `design-coworking.jpg` no longer used, still in repo.
- [ ] **Yelp scraper for physical wellness venues** — Othership Toronto, Remedy Place, HigherDOSE, Bathhouse NYC, Perspire Sauna, Medellín wellness/spa/yoga places, Bodytech Medellín, 108 Yoga Medellín
- [ ] **Google Maps reviews** — same targets. May need SerpAPI or Outscraper if scraping is blocked.
- [ ] **Drop data into NotebookLM** — once Yelp/Google data collected. Ask: emotional drivers, what people wish existed, why they leave premium clubs, how they describe themselves.
- [ ] **Update discovery script** — add 7 demographic questions to opening section (nationality, age, work, tenure, neighborhood, communities). Rebuild DOCX.
- [ ] **Community leader branch** — optional add-back to discovery script for participants who are community organizers.

## Backlog

- [ ] Run more discovery calls — target: 30+. Each call → add to dashboard.
- [ ] Reach out to Reggie (investor) and Brett (trainer) — referrals from Andrew.
- [ ] Competitive analysis: pull pricing pages for Othership, Remedy Place, Perspire — what does a founding membership look like?
- [ ] Build Call 2 script — brand reveal, space concept, founding membership offer.

## Done

- [x] **Retire Fathom auto-sync auto-injection (2 corruption incidents)** — cloud Action rewritten notify-only (`scripts/notify_new_calls.py` → GitHub issue), JS smoke-check (`scripts/validate_index.js`) added as a deploy gate, old `update_calls.py` deleted, local `vare-fathom-sync` task confirmed retired. **Pushed to `main` + verified running in Actions** (deploy gate logged 15 participants OK; notifier run returned new_count=0).
- [x] Gitignore local `.claude/` and the 31MB `PROP 01 VARÉ.pdf`.
- [x] Add Community Events + Practitioner Services verticals to product roadmap (7 total)
- [x] Cluster feature card gaps by theme (data restructured to {theme, text})
- [x] Organize quote wall by theme instead of person — 7 themes, 35 quotes
- [x] Replace single mood board image per section with 3-photo collage (15 AI images via Pollinations FLUX)
- [x] Replace D3 work type treemap with named cluster groups (readable at N=11)
- [x] Build research dashboard (index.html) — live at jctitan1045.github.io/vare-research
- [x] Load Andrew Topping's call data into dashboard
- [x] Add demographics section to dashboard
- [x] Add aggregate "Services in demand" chart
- [x] Per-call services with context notes
- [x] Top 3 quotes per participant
- [x] Build discovery script (Call 1, 30 min)
- [x] Build DOCX version of script
- [x] Build ranking slide (HTML, dark, screen-share ready)
- [x] Push to GitHub Pages (jctitan1045/vare-research)
- [x] Confirm Vare brand name
- [x] Confirm Fathom call naming convention
- [x] Pull 330 Othership App Store reviews
- [x] Pull 4,515 wellness App Store reviews (wide sweep)
