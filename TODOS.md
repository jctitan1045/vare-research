# TODOS — Waha Research

## Next

- [ ] **Build "Decisions & next moves" section** (actionability #1) — surface price / site / Phase-1 build / anchor instructors / GTM as owned decisions with status chips, under the exec summary. *The single next move.*
- [ ] **Calibrate the launch Gantt to a real target open date** — `LAUNCH_PLAN` in `index.html` currently assumes ~Q1–Q2 2027; needs Jordan's actual target / lease + build timelines.
- [ ] **Add real venue + model photos** — drop JPGs into `assets/venues/<slug>.jpg` and `assets/models/<slug>.jpg` (owned/licensed only). See USER_GUIDE.

## Soon

- [ ] **Hot-leads / founding-members list** (actionability #2) — ranked follow-up list of strong-match, high-WTP, already-spending participants.
- [ ] **C11 — print/PDF stylesheet** — force-expand all sections + light background for a clean investor PDF export.
- [ ] **D15 — objections / dealbreakers view** (+ theme-saturation curve) — the risk register.
- [ ] **B7 — low-sample markers** — tag n≤2 roadmap features as "emerging."
- [ ] **Finish the price prose sweep** — narrative COP/USD mentions in gap/notes text (verbatim quotes stay unchanged).
- [ ] **"Where they live" map polish** — apply the same fit-all + count-label treatment used on the "where they want it" map.
- [ ] **Maps Embed API key** (Jordan creates) → wire photo-forward `place` embeds on venue/model banners.
- [ ] **Review the WAHA Brand Book with Lorenzo → consolidated feedback to Nick** (from the Jul 15 BRANDBOOK call: 70 pages, modular `WAHA + Symbol + "Club"` logo system, Jungle Green / Sunrise Yellow / Beige palette).
- [ ] **Run more discovery calls — 22 of 30 done, 8 to go.** Each research call → add to `DATA.participants` + `AVATARS` (see USER_GUIDE for the gotchas).
- [ ] Reach out to Reggie (investor) and Brett (trainer) — referrals from Andrew.

## Someday

- [ ] Delete orphaned mood-board images (`design-sauna.jpg`, etc.) if still in the repo.
- [ ] Yelp scraper for physical wellness venues (Othership Toronto, Remedy Place, HigherDOSE, Bathhouse NYC, Perspire; Medellín spa/yoga, Bodytech, 108 Yoga).
- [ ] Google Maps reviews — same targets (may need SerpAPI / Outscraper).
- [ ] Drop collected review data into NotebookLM — emotional drivers, what people wish existed, why they leave premium clubs.
- [ ] Update discovery script — 7 demographic Qs in opening; rebuild DOCX. Optional community-leader branch.
- [ ] Competitive pricing pages (Othership, Remedy Place, Perspire) → design the founding-membership offer.
- [ ] Build Call 2 script — brand reveal, space concept, founding membership offer.
- [ ] Optional cosmetic: rename repo/Pages URL `vare-research` → `waha` (breaks current link).

## Done

- [x] **Added 6 research participants from the Jul 14–16 calls (2026-07-16)** — 16 → **22 participants**: Thierry Muller (17), Alain Alisca (18), Laisvidas "Lais" Karvelis (19), Niko Bo (20, supply-side facilitator), Emilis Karvelis (21, Lais's brother), Gabe Krebs (22). Each with a transcript-grounded participant object + `AVATARS` persona. Segments now Consumers 13 / Supply 9 / Locals 5 / Expats 17.
- [x] **Dashboard actionability + UX overhaul (2026-07-14)** — folded avatars into ICP click-through w/ Strong/Partial/Loose match ranking; per-section "what this tells us" takeaways; WTP consolidated; Market+Moat merged into "Where we win"; prices standardized COP-primary + USD; location map fit-all + count bubbles; market landscape re-imagined as per-venue photo cards + tap-to-expand Google Maps embeds; moat pyramid → stat strip + comparison matrix; North Star models built out as rich cards; launch **Gantt** + Now/Next/Later phase-tagged kanban; removed design-prompts, "Who's in this research" heading, and People-pipeline; fixed avatar handle + `[object Object]` profile quotes. (See WORKBENCH + DASHBOARD_AUDIT.)
- [x] Audit items A1–A4, actionability moves 1/B/2/3/C, C10, C12, D13, D14 (see `DASHBOARD_AUDIT.md`).
- [x] Retire Fathom auto-sync auto-injection (notify-only + deploy smoke-check gate).
- [x] Gitignore local `.claude/` and the 31MB `PROP 01 VARÉ.pdf`.
- [x] Add Community Events + Practitioner Services verticals to product roadmap (7 total).
- [x] Cluster feature-card gaps by theme; organize quote wall by theme (7 themes, 35 quotes).
- [x] Build research dashboard (index.html) — live at jctitan1045.github.io/vare-research.
- [x] Build discovery script (Call 1) + DOCX + ranking slide; confirm Waha brand + Fathom naming.
- [x] Pull 330 Othership + 4,515 wellness App Store reviews.
