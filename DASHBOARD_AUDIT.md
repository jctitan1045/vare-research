# Dashboard Audit — Improvement Roadmap

Best-practice + correctness review of the Waha research dashboard (started 2026-07-09). Checked items are done and live.

## A. Correctness (fix these)
- [ ] **A1 — Price field mixes currencies.** `priceCeiling`/`priceGoodDeal` jumble USD and COP-thousands in one field, so the Price-calibration chart mis-buckets. Normalize to COP-thousands; audit all participants.
- [x] **A2 — "16 calls" was inaccurate.** It's 16 participants across 15 recordings (one joint call). Badge, exec summary, stat chip, market-landscape note, and pipeline recommendation now say "participants" (with "across N calls" where useful). *Done 2026-07-09.*
- [ ] **A3 — Supply-side blended into demand aggregates.** 8 of 16 are instructors/community-builders; their WTP + rankings distort consumer aggregates. Segment or caveat.
- [ ] **A4 — Near-duplicate roadmap features.** "Social" and "Community events" categories double-represent themed events / free intro events. Merge or de-dupe.

## B. Research best-practices
- [ ] **B5 — Sample bias not disclosed.** Add a "how to read this / sample composition" note (warm-network + expat skew).
- [x] **B6 — WTP is stated + anchored.** Added a "What they already pay" section: per-participant monthly spend across the bundled categories (revealed preference), median/range/% stats, and a stated-vs-revealed callout. Exec WTP chip reframed to "stated WTP · median already spends ~620k." *Done 2026-07-09.*
- [ ] **B7 — Small-sample features read as signal.** Mark n≤2 features as "low-sample / emerging."
- [ ] **B8 — No evidence weighting / commitment funnel.** Add an Interested → Call-2 → Waitlist → Deposit funnel.

## C. Accessibility & UX
- [ ] **C9 — Accessibility gaps.** Collapsible headers are `<div>`s (no role/aria/keyboard); zero semantic headings. Make headers real buttons + promote to headings.
- [ ] **C10 — No "last updated" date.** Add a "data as of …" stamp.
- [ ] **C11 — No print/PDF handling.** Print stylesheet that force-expands all sections.
- [ ] **C12 — Collapsed-by-default trade-off.** Consider defaulting Moat + Market open.

## D. Bigger enhancements (maybe / later)
- [ ] **D13 — Segment filter** (locals/expats · consumer/instructor · WTP tier).
- [ ] **D14 — Dedicated supply-side view** (instructor rates, collaboration models, audiences).
- [ ] **D15 — Objections/dealbreakers view + theme-saturation curve.**
