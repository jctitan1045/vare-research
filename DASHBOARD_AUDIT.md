# Dashboard Audit — Improvement Roadmap

Best-practice + correctness review of the Waha research dashboard (started 2026-07-09). Checked items are done and live.

## A. Correctness (fix these)
- [x] **A1 — Price field mixed currencies.** Audited all 16 against their own notes + spend. Three un-converted expats (Andrew, Sebastian, Alex) were in USD → converted ×4 to COP-thousands. Colombians (Juliana/Isabella/JP Madrid/Isabel) and already-converted expats (Adam/Brett/Laurel/Armin/Ali/Zach/Jonas) left as-is. All `priceCeiling`/`priceGoodDeal` now COP-thousands; Price-calibration chart re-buckets correctly (1/3/3/7). Day-pass ranges untouched. *Done 2026-07-09.*
- [x] **A2 — "16 calls" was inaccurate.** It's 16 participants across 15 recordings (one joint call). Badge, exec summary, stat chip, market-landscape note, and pipeline recommendation now say "participants" (with "across N calls" where useful). *Done 2026-07-09.*
- [x] **A3 — Supply-side blended into demand aggregates.** Fixed via the segment filter (D13): Consumers (8) vs Supply-side (8) isolates demand from supply so instructor WTP/spend/rankings no longer pollute the consumer aggregates. *Done 2026-07-09.*
- [ ] **A4 — Near-duplicate roadmap features.** "Social" and "Community events" categories double-represent themed events / free intro events. Merge or de-dupe.

## B. Research best-practices
- [ ] **B5 — Sample bias not disclosed.** Add a "how to read this / sample composition" note (warm-network + expat skew).
- [x] **B6 — WTP is stated + anchored.** Added a "What they already pay" section: per-participant monthly spend across the bundled categories (revealed preference), median/range/% stats, and a stated-vs-revealed callout. Exec WTP chip reframed to "stated WTP · median already spends ~620k." *Done 2026-07-09.*
- [ ] **B7 — Small-sample features read as signal.** Mark n≤2 features as "low-sample / emerging."
- [ ] **B8 — No evidence weighting / commitment funnel.** Add an Interested → Call-2 → Waitlist → Deposit funnel.

## C. Accessibility & UX
- [x] **C9 — Accessibility gaps.** Section headers are now real `<button>`s (`aria-expanded`/`aria-controls`, native keyboard, focus ring) inside `role="heading" aria-level="2"`; section bodies are `role="region"` labelled by their heading; added a page `<h1>` and made the TOC a `<nav aria-label>`. `aria-expanded` stays in sync on toggle / expand-all / anchor-open. *Done 2026-07-09.*
- [ ] **C10 — No "last updated" date.** Add a "data as of …" stamp.
- [ ] **C11 — No print/PDF handling.** Print stylesheet that force-expands all sections.
- [ ] **C12 — Collapsed-by-default trade-off.** Consider defaulting Moat + Market open.

## D. Bigger enhancements (maybe / later)
- [x] **D13 — Segment filter.** "View data for" chips (All / Consumers / Supply-side / Locals / Expats) in the research section; re-renders the data + roadmap views (`ACTIVE` set) while curated strategy sections stay full. render() made re-runnable (Chart.js destroy + Leaflet re-init guard). *Done 2026-07-09.*
- [x] **D14 — Dedicated supply-side view.** New "Supply side — instructors & community partners" section: `supply` field on the 8 supply-side participants (single-source), rendered as cards (Offers / Audience / Collaboration model / Needs) + an intro capturing the recurring per-head-fee-then-50/50 model. In the TOC + collapsible. *Done 2026-07-09.*
- [ ] **D15 — Objections/dealbreakers view + theme-saturation curve.**
