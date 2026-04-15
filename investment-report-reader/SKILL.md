---
name: investment-report-reader
description: Read and extract content from PDF investment reports — sell-side notes (GS/MS/JPM/UBS/Citi/BofA), 10-Ks, annual reports, fund factsheets, manager commentaries, and macro outlooks. Specialises in CHARTS, TABLES, and IMAGES that text-only extraction silently misses (most research charts are vector and invisible to pdfimages). Handles MULTI-REPORT TRIANGULATION when 2+ reports cover the same name, comparing forecasts, valuation methods, and surfacing coverage gaps. When the user has a company of interest and uploads sector or industry reports alongside company-specific notes, MINES the sector reports for company-specific tables and exhibits and treats them as direct evidence. Use whenever a PDF investment report is uploaded and the user wants to summarise, query, extract from, compare reports, or dig a company out of an industry note. Trigger phrases include "read this broker note", "summarise this 10-K", "what does this report say about X", "pull the price target", "compare these reports".
---

# Investment Report Reader

**Version: 3.3** — adds missing-report detection, the EPS/PT/spot three-way race diagnostic (Rule 13), broadens Rule 12 from framework-switch to definition-switch, lowers the sector-mining threshold to single-paragraph mentions, requires bull-case sanity-checks against prior-cycle peaks, requires unit-consistency checks across estimate trajectories, and adds the unstated-falsifier prompt to every playbook. See changelog at the end of this file.

A specialised PDF reading skill for investment research documents. Built on top of the public `pdf-reading` skill but tuned for the specific structure, vocabulary, and extraction targets of investment reports.

## When this skill applies

Trigger on any PDF that is:
- **Sell-side research** — broker notes, initiations, company updates, sector primers, strategy notes
- **Company filings** — annual reports, 10-K / 10-Q / 20-F, interim reports, prospectuses
- **Fund documents** — factsheets, monthly/quarterly commentaries, KIIDs, holdings reports
- **Buy-side internal research** — investment memos, IC papers, pitch books
- **Macro / strategy** — house view documents, outlook reports, central bank publications

If the PDF is one of these AND the user wants to read, summarise, query, or extract from it — use this skill.

## Core philosophy

Investment reports are **hybrid documents**. The thesis is in the prose, but the *evidence* is almost always in charts and tables — and most of those charts are vector graphics that `pdfimages` will silently miss. A naive `pdftotext` pass will extract the narrative and lose 60% of the value. This skill exists to make sure that doesn't happen.

The default workflow is therefore:
1. **Triage** the report (type, length, structure)
2. **Extract text** for narrative, thesis, ratings, targets
3. **Extract tables** programmatically for financials, forecasts, comps
4. **Rasterize key pages** so charts and visual exhibits can actually be read
5. **Synthesise** into the format the user asked for (or infer)

---

## Step 1 — Triage

Always start here. It takes ~5 seconds and determines everything else.

```bash
PDF=/mnt/user-data/uploads/report.pdf
pdfinfo "$PDF"                              # pages, size, metadata
pdftotext -f 1 -l 2 "$PDF" - | head -60     # cover + first page text
pdfimages -list "$PDF" | head -20           # raster image inventory
```

From the cover page text, identify:

| Signal | What to look for |
|---|---|
| **Report type** | "Equity Research", "Company Update", "Annual Report", "Factsheet", "Outlook" |
| **Issuer / author** | Goldman Sachs, Morgan Stanley, BG, Wellington, the company itself |
| **Subject** | Ticker, company name, fund name, theme |
| **Date** | Publication date — critical for staleness assessment |
| **Rating & target** (sell-side) | Buy/Hold/Sell, price target, prior target |
| **Length** | <10 pages = note; 10–40 = standard report; 40+ = deep dive / annual |

Based on the type, jump to the appropriate playbook below.

---

## Step 2 — Report-type playbooks

### Playbook A — Sell-side research note

Standard structure: cover (rating/target/thesis) → key charts → financial summary table → narrative → forecasts → risks → disclosures.

**Always extract from the cover page:**
- Ticker, rating, price target (current and prior), implied upside
- **Reference price AND its date** — sell-side notes are often priced 1–2 days before publication, and the implied upside in the headline can be stale by 5–15% on a volatile stock. Always surface the reference date alongside the price.
- Analyst name, publication date
- One-line thesis / "what's changed"

**Then extract:**
- The financial summary table (usually page 2 or last page before disclosures) — this has the analyst's full forecast model in compressed form
- Any chart with a forecast curve, price target waterfall, or scenario analysis — **rasterize these pages**
- The risks section (usually near the end, before disclosures)

**Always check for chart-vs-narrative contradictions.** Sell-side notes routinely include charts that quietly undermine the bull case in the prose — the most common case is a P/B or P/E history chart showing the stock at the top of its historical range while the text argues for "attractive valuation". When you find one, **call it out explicitly** in the output. This is where charts add the most analytical value and it's also the easiest thing to miss if you're only reading the text.

**Always run the unstated-falsifier prompt.** After extracting the thesis, write down in one sentence what specific, observable scenario would have to materialise for the thesis to be wrong — not "things get worse" but a concrete event. Then search the report for any acknowledgment of that scenario. If the report doesn't address its own falsifier, name the gap explicitly. This applies to any single report, not just Mode 5 stacks. See Rule 17.

**Always sanity-check any bull case against prior-cycle peaks.** Whenever the report contains a bull case, blue-sky case, or upside scenario, extract the implied peak-year gross margin, operating margin, and revenue. Compare against the same company's prior-cycle peak. Flag any bull case whose implied margins exceed prior-peak by more than ~10 points without an accompanying structural argument. See Rule 15.

**Skip:** disclosures, analyst certifications, regulatory boilerplate (typically the last 3–10 pages — check page count and stop early).

### Playbook B — Annual report / 10-K

Long (100–400 pages), highly structured. Don't read linearly.

**Priority sections (in order):**
1. **Letter to shareholders / Chairman's statement** — strategic narrative
2. **MD&A / Operating review** — segment performance, drivers, outlook language
3. **Risk factors** — for 10-Ks, the *new* or *expanded* risks vs prior year
4. **Financial statements** — IS, BS, CF (extract as tables)
5. **Selected notes** — segment reporting, revenue recognition, debt schedule, share count, SBC

Use the table of contents (usually pages 2–4) to jump directly. Rasterize any segment performance chart or strategy diagram in the front section.

### Playbook C — Fund factsheet / commentary

Short (2–8 pages) but dense with charts. Almost everything that matters is visual.

**Strategy:** rasterize every page. Extract:
- Top 10 holdings table
- Sector / geographic breakdown (usually pie or bar chart — must rasterize)
- Performance table (1M / 3M / YTD / 1Y / 3Y / 5Y / SI vs benchmark)
- Manager commentary prose (text extract is fine here)
- Fund metadata (AUM, inception, fees, ISIN)

### Playbook D — Macro / strategy / outlook

Heavily chart-driven. The prose is often just connective tissue between exhibits.

**Strategy:** identify chart-heavy pages from `pdfimages -list` (high image count) AND visually scan the contents page. Rasterize every page that contains a key exhibit. Extract the prose for context.

---

## Step 3 — Extraction toolkit

### Before you begin: check how the PDF arrived

The default workflow below assumes the PDF is on the filesystem and you reach for `pdfinfo`, `pdftotext`, `pdfplumber`, and `pdftoppm` in order. But there are two delivery modes and they have different costs:

- **Filesystem PDF** (`/mnt/user-data/uploads/foo.pdf`): use the full toolkit below. Rasterization of key pages is necessary to read vector charts.
- **In-context PDF** (passed as a `document` block with `media_type: application/pdf`): Claude already has both the text layer *and* the visual layer of the PDF. Charts, tables, and exhibits are visible directly without rasterization. The filesystem tools are still useful for extracting tables programmatically (when you want clean rows for downstream use) and for jumping to specific pages, but the cost-saving observation is that **rasterization is not required** — every page is already viewable.

Check which mode you're in before reaching for `pdftoppm`. If the PDF is in context, skip the rasterize step entirely and read the exhibits directly. If only some PDFs in a stack are in context and others are on the filesystem, treat them differently.

### Text — for narrative, thesis, commentary

```bash
# Layout-preserving (best for multi-column research notes)
pdftotext -layout "$PDF" /tmp/full.txt

# A specific page range
pdftotext -layout -f 5 -l 8 "$PDF" - 
```

### Tables — for financials, forecasts, holdings, comps

`pdfplumber` is the workhorse. Try it first; if the table is garbled (merged cells, rotated text, image-based), fall back to rasterizing the page and reading visually.

```python
import pdfplumber

with pdfplumber.open("/mnt/user-data/uploads/report.pdf") as pdf:
    page = pdf.pages[4]  # 0-indexed
    tables = page.extract_tables()
    for t in tables:
        for row in t:
            print(row)
```

Tuning hints when default extraction fails:
- `extract_tables(table_settings={"vertical_strategy": "text", "horizontal_strategy": "text"})` — for borderless tables (common in sell-side research)
- `table_settings={"vertical_strategy": "lines", "horizontal_strategy": "lines"}` — for ruled tables (common in 10-Ks)
- If still garbled → rasterize the page and read visually

### Charts and visual exhibits — rasterize the page

**This is the most important capability of the skill.** Investment reports are full of vector charts (matplotlib, Excel, Bloomberg exports) that `pdfimages` will NOT extract because they are PDF drawing operators, not image objects. The only reliable way to "read" them is to rasterize the whole page and look at it.

```bash
# Rasterize page 7 at 200 DPI (high enough to read axis labels and small print)
pdftoppm -jpeg -r 200 -f 7 -l 7 "$PDF" /tmp/page

# Find the actual filename (zero-padding depends on total page count)
ls /tmp/page-*.jpg
```

Then use the `view` tool on the resulting image. When reading the chart, pull out:
- **Title and subtitle** — what is being shown
- **Axes** — units, scale (linear/log), date range
- **Series** — what each line/bar represents, colour-coded legend
- **Key data points** — most recent value, peaks, troughs, inflection points
- **Annotations** — analyst arrows, callouts, shaded regions
- **Source** — almost always at the bottom in small print; matters for credibility

For multi-chart pages, describe each exhibit separately and number them (Exhibit 1, 2, …) the way the report does.

### Embedded raster images (logos, photos, screenshots)

```bash
pdfimages -list "$PDF"           # inventory first
pdfimages -png "$PDF" /tmp/img   # extract all
```

Filter by file size — anything <5KB is usually a decorative element or logo, not content.

### Cost-aware reading

Rasterized pages are expensive (~1,600 tokens each at 150 DPI, more at 200 DPI). For a 200-page annual report, do **not** rasterize everything. The triage step exists precisely so you can identify the 5–15 pages that actually matter and rasterize only those.

Rules of thumb:
- Sell-side note (10–20 pages): rasterize 3–6 pages (cover, key charts, summary table)
- Annual report (200 pages): rasterize 5–10 pages (strategy diagrams, segment charts)
- Factsheet (4 pages): rasterize all of them
- Macro outlook (50 pages): rasterize 8–15 pages (key exhibits)

**Lean toward the upper end of the budget when `pdfimages -list` returns zero raster images.** A report with no extractable images is, by definition, a report where every chart is vector — so every chart needs rasterization or it's invisible. Don't be stingy in this case; the alternative is silently missing the entire visual layer of the document. Conversely, if `pdfimages -list` shows many raster charts, you can lean toward the lower end and let `pdfimages -png` handle them directly.

---

## Step 4 — Output

Let the user's request determine the format. If they haven't specified, infer from context.

### Mode 1 — Quick targeted answer (default for Q&A)

Plain markdown reply in chat. Lead with the answer, cite the page number, quote a short fragment if needed for evidence (≤15 words, follow copyright rules).

> *"The price target was raised from $185 to $215 (page 1), driven by a 4% upward revision to FY26 EPS estimates (page 4, Exhibit 3)."*

### Mode 2 — Comprehensive summary (default if user says "summarise" or "read this report")

Markdown structure:
```
## [Report title] — [Issuer], [Date]

**Bottom line:** [1–2 sentence thesis]

**Key numbers:**
- Rating / target / upside (if sell-side)
- Top 3 financial metrics with prior comparison

**What's new / what changed:** [bullets]

**Thesis:** [3–5 bullets]

**Forecasts:** [table — extracted, not paraphrased]

**Charts worth knowing:** [exhibit-by-exhibit, page-numbered]

**Risks:** [bullets]

**My read:** [1 paragraph — only if the user asks for a view]
```

### Mode 3 — Data extraction for downstream model

Structured table or JSON the user can drop into Excel or feed into another skill. Always include source page numbers.

### Mode 4 — Word memo

If the user wants a formal write-up, hand off to the appropriate downstream skill:
- Investment thesis / company analysis → `bg-lens`
- Earnings print → `earnings-analysis`
- Valuation / model → `dcf-valuation`, `semi-dcf-modeler`, `biotech-dcf-modeler`
- Sector / theme → `thematic-investment-research`
- Competitive positioning → `competitive-analysis`

This skill's job is to get the data *out of the PDF*; the downstream skill's job is to write the memo.

### Mode 5 — Multi-report triangulation (≥2 reports on the same subject)

When the user uploads two or more reports covering the same company, fund, or theme, do **not** treat them as independent summaries. The whole point of having multiple reports is to find where they agree, where they disagree, and what each one sees that the other misses. Run the per-report extraction first, then build a comparison.

**When the stack is mixed — some reports are company-specific and some are sector/industry-level — the company-of-interest is still the protagonist.** Sector reports almost always contain company-specific exhibits, tables, and paragraphs that are just as valuable as the data in the direct company note. Mine them. See the sub-section below.

Output template:

```
# [Subject] — [House A] vs [House B] (vs [House C]…)

## Bottom line
[1–2 sentences: do they agree on the call? On the math?
 If a beat-vs-performance paradox exists, lead with it.]

## Headlines side by side
[Comparison table — rating, target, reference price (with date),
 implied upside, key forecasts year by year, valuation method]

## Event-anchored timeline
[Only when sequential reports are clearly driven by one or two
 discrete events — earnings prints, investor days, M&A announcements,
 guidance changes. Organise the reports as "Pre-event view / Post-event
 digestion / Post-event plus follow-up" rather than by calendar date.
 Omit this section entirely if no clear anchoring event exists.]

## Estimate-revision trajectory
[Required whenever ≥3 reports span >4 weeks. Small table showing how
 each key forecast line — revenue, EPS for the next 2 fiscal years,
 operating margin — evolved report by report. The pattern matters
 more than any individual number.]

## What the charts tell you that the text doesn't
[Per-report exhibit observations that change the read]

## Where they actually diverge
[Numbered list of substantive disagreements — earnings forecasts,
 valuation framework, risks flagged by one but not the other,
 catalysts, end-market assumptions]

## Coverage gap matrix
[Topic-by-report grid — see rules below]

## Risks (synthesized)
[Union of both risk sections]

## My read
[Which report to trust for what; what to verify before acting]
```

**Rules for the comparison:**

1. **Identical headline targets often hide different math.** If two houses land on the same price target via materially different earnings forecasts or valuation methods, that's the most important thing in the comparison — surface it first. Identical targets with different math usually mean reasonable analysts have stopped arguing at a price, which is itself useful information.

2. **Always cross-check consensus citations.** Sell-side notes quote consensus numbers, and two reports written days apart often cite *different* consensus figures because they're pulling from different vintages (Visible Alpha vs Bloomberg vs Refinitiv, different cut-off dates). Surface the discrepancy when it appears — it tells you which consensus the analyst is benchmarking against.

3. **Date-arbitrage the reference prices.** Two reports published the same day may use reference prices from different trading sessions (intraday vs prior close, different time zones). On a volatile stock this can produce a 5–15% gap in the headline "implied upside" for an identical price target. Flag it explicitly. Cite the older reference price and note that the upside number is stale.

4. **Catalogue what each house addresses that the others ignore.** This is often where the alpha is. If House A discusses a HBM4 redesign or an ADR catalyst or a China manufacturing issue and House B is silent, that's a real coverage gap — surface it as "House B readers will miss this".

5. **Don't average the forecasts.** Show the spread. Investors need to see the dispersion, not a synthetic midpoint.

6. **The beat-vs-performance paradox always leads.** If multi-report triangulation surfaces a contradiction between (a) earnings/pricing data showing a name has had the biggest beat in a peer group AND (b) relative-performance data showing the same name has been the worst-performing stock in that peer group, that contradiction is the single most important observation in the entire stack and must be surfaced **first** in the bottom line. Biggest beat plus worst performance is the visual proof of a de-rating thesis — the market is refusing to capitalise the new earnings level. Never bury this in the body. Lead with it.

7. **Brevity is not a downgrade signal.** Short notes (3–4 pages) from senior analysts often contain the punchline that 30-page deep dives bury under model output. When a brief note delivers a sharper analytical observation than a longer note, weight the observation by quality, not by page count. Specifically: if the short note diagnoses a paradox or names a risk that the long note ignores, the short note is the more valuable read on that topic — say so.

8. **Event-anchor the timeline, don't calendar-anchor it.** When sequential reports are clearly driven by one or two discrete events (earnings prints, investor days, M&A announcements, guidance changes, major equity investments), organise the comparison around the events, not the publication dates. The natural framing is "Pre-event view / Post-event digestion / Post-event plus follow-up meetings". This is especially important when one report predates the key event entirely — that report should be labelled as pre-event and its forecasts treated as a historical baseline, not a current view. To identify the anchoring event, look for language like "following the Investor Briefing", "post-OFC", "after the Q2 print", or dates clustered around a known company event. If no clear event drives the revisions, fall back to calendar ordering and skip this section in the output.

9. **Track multiple compression across sequential reports.** When estimates rise faster than price targets, the implied forward multiple falls — and that is diagnostic. Rising targets built on compressing multiples mean consensus is *catching up* to buyside positioning rather than getting incrementally more bullish on valuation. This has different implications for whether the stock can keep running: a re-rating has room; a catch-up has less. Always compute, for each report in a sequential stack, the implied forward multiple on the furthest-out EPS number the report models. If the multiple is compressing while the PT rises, flag this as "consensus catch-up, not re-rating" in the output. Conversely, if the multiple is expanding while EPS is stable, flag it as a genuine re-rating. This distinction is often the most important read on whether a move has legs.

10. **The stranded rating pattern.** When any report's price target is more than 30% away from the current spot price (in either direction) and that report is not the most recent in the stack, the rating is effectively untenable absent a refresh — surface this as a "stranded rating" and quantify the gap in dollars and percent. The output should state explicitly that any reader relying on the stranded report alone is looking at a historical artefact, and should carry a warning that the rating has not been reconciled with the new price. This is the inverse of the beat-vs-performance paradox (rule 6): instead of good results failing to move the stock, it is a sceptical analyst whose thesis has been mechanically invalidated by price action. Both patterns deserve equal billing and both must lead the bottom line when they occur. To operationalise: when extracting cover-page data per Playbook A, always compute the gap between the report's reference price and the most recent reference price available anywhere in the stack. Any gap exceeding 20% is a watch item; any gap exceeding 30% triggers the stranded-rating tag automatically.

11. **Forecast convergence to a named third party is consensus catch-up — credit whoever was right first.** When an analyst's forecast moves over multiple reports in the direction of (and toward) a publicly-stated number from a named third-party data provider — TrendForce, IDC, Gartner, Wood Mackenzie, IHS, Visible Alpha consensus, or a competing sell-side house — that is a forecast convergence pattern, distinct from but related to multiple compression (rule 9). Compression is about price catching up to estimates within one model; convergence is about estimates catching up to a number someone else printed earlier. Both are catch-up patterns and both have the same diagnostic implication: the easy money has been made by whoever set the right anchor first. To operationalise: in any sequential stack of ≥3 reports, scan for third-party forecasts cited by name. If a cited number from an early report sits roughly where the analyst's own number lands two or three reports later, surface this explicitly as "the analyst spent N weeks closing the gap to [provider]'s [date] number" and credit the provider in the bottom line. The reader should know who called it first. This rule pairs with rule 9: compression is the within-model version of catch-up, convergence is the cross-source version.

12. **Anchored headline with shifting definition — the within-house cousin of rule 1.** Rule 1 covers identical price targets across houses derived from materially different math. Rule 12 covers any headline number — price target, multiple, or otherwise — held constant across time within one house while its underlying definition changes. The classic case is the framework switch (P/B to P/E, DCF to comps, sum-of-parts to multiples). But the subtler and more common case is a **definition switch** within the same framework: the headline "11x" survives across reports while its EPS denominator silently moves from "FY27" to "FY26-29 average," or from peak-cycle to through-cycle, or from non-GAAP to GAAP, or from forward-year to two-year-forward. This is still a P/E in both reports, so a framework-only check misses it — but the *referent* of the headline has changed, which is the same revealed-preference behaviour as a full framework switch. To operationalise: in any sequential same-house stack, extract the PT-derivation language verbatim from each report's price-objective-basis section and diff it on **all four axes** — (a) framework label (P/E, EV/EBITDA, DCF, P/B), (b) EPS or denominator definition (which fiscal year, peak vs through-cycle, GAAP vs non-GAAP, diluted basis), (c) multiple level, and (d) EV vs equity basis. Any one of those four changing while the headline number stays constant fires the rule. Surface as "anchored headline with definition switch" and quote both derivations in the output, naming which axis moved. Treat the second definition as the analyst's revealed-preference rationalisation, not their model — the analyst found themselves needing the headline to land at a particular level and adjusted the math underneath until it did.

13. **Three-way race between EPS revisions, spot price, and price target — the trajectory shape diagnostic.** In any sequential same-house stack of ≥3 reports, compute three percentage changes from the first report to the last: (a) the change in the furthest-out EPS estimate, (b) the change in the spot/reference price, and (c) the change in the price target. The relative ordering of these three numbers is itself a diagnostic, distinct from multiple compression (Rule 9), forecast convergence (Rule 11), and the stranded rating (Rule 10) — though it interacts with all three. The shapes worth naming:
    - **PT > EPS > spot.** The analyst is getting more bullish faster than the model justifies and the market is lagging. Usually means the analyst is leading; the runway depends on whether the model catches the PT or the PT catches reality.
    - **EPS > PT > spot.** The analyst is upgrading the model faster than the PT — the multiple is compressing inside the analyst's own framework (Rule 9 fires) but the analyst hasn't yet capitulated to where the model takes them. The PT is doing partial catch-up.
    - **EPS > spot > PT.** The most diagnostically loaded shape: the model is being dragged up by reality and the analyst is chasing both. The PT is structurally behind. This is consensus catch-up to the buyside (Rule 9) **and** convergence to a third party (Rule 11) running simultaneously, and it usually means the easy money has already been made by whoever was right first. Often pairs with Rule 12's anchored-headline behaviour because the analyst needs an excuse to keep the math looking conservative while the dollar number doubles.
    - **spot > PT > EPS.** Stranded rating territory (Rule 10). The analyst hasn't refreshed; the model is behind both the PT and reality.
    - **EPS > spot ≈ PT.** Healthy. The analyst is pacing the model and the tape together; nothing is being chased.
    To operationalise: surface the three numbers as a single line in the trajectory section ("Over [date range]: EPS +X%, spot +Y%, PT +Z%") and name the shape. The shape diagnostic should appear before the multiple-compression and convergence diagnostics in the output, because it frames how to read them.

14. **Missing-report detection in sequential stacks.** Sequential same-house stacks frequently have holes — the user uploads the early report and the latest report but is missing the one in between where a key revision actually happened. The skill currently has no mechanism to detect this, and trajectory analysis (Rules 9, 11, 12, 13) silently treats the gap between two endpoints as if it were a smooth path. It is not. To operationalise: when triaging any sequential same-house stack, scan every report's ticker table, comp table, summary table, and headline for `OLD`, `Old`, strikethrough numbers, "(prev. $X)", "(was $Y)", "previously $Z", or any annotation indicating a prior value that does not correspond to a report in the stack. Each such annotation is a missing-report signal. List them explicitly in the trajectory section as "interim revision: [old] → [new], dated between [report N] and [report N+1], not in stack." This matters because (a) a single missing report can hide a methodology switch or estimate jump that happened in one shot, (b) the path between two endpoints determines whether a move was smooth catch-up or a stepwise capitulation, and (c) downstream Mode 5 diagnostics depend on knowing whether you're looking at a continuous trajectory or a reconstructed one. If the missing report is material (large estimate jump, framework switch, rating change), say so in the bottom line — the user should know what they don't have.

15. **Bull-case sanity check against prior-cycle peaks.** Bull cases and blue-sky scenarios are where analysts park their optical upside, and they are routinely the least stress-tested numbers in any report. A reader skimming a bull case anchors on the dollar PT, not the implied margin profile or revenue level. To operationalise: whenever a report includes a bull case, blue-sky case, upside scenario, or "what if" valuation, always extract three things from it explicitly — (a) implied gross margin at the peak year, (b) implied operating margin at the peak year, and (c) implied revenue at the peak year — and compare each against the same company's prior cycle peak. The prior-peak data is usually available in the same report's history exhibits, the company's own filings, or trivially Google-able. Flag any bull case whose implied margins exceed the prior-cycle peak by more than ~10 percentage points without an accompanying structural argument for why this cycle is structurally different (and that argument has to be more than "AI demand"). The bull case is allowed to be aggressive; what it's not allowed to be is unexamined. Surface as "bull case implies [X]% GM vs [Y]% prior peak — structural justification: [paraphrase, or 'none stated']" in the output.

16. **Unit and definition consistency check across estimate trajectories.** Large QoQ revisions in trajectory tables can be artefacts rather than upgrades. Between two reports, the same headline number can shift because of (a) a fiscal year basis change, (b) a segment scope change after a divestiture or acquisition, (c) a currency/FX assumption change, (d) a GAAP vs non-GAAP basis switch, (e) a diluted vs basic share count change, or (f) a definition of "core" that has been quietly broadened. None of these are upgrades; all of them look like upgrades in a side-by-side table. To operationalise: any line in a trajectory table where the change exceeds ~25% must be cross-checked against the report's own footnotes for scope, definition, and basis changes before being treated as a like-for-like revision. Add a one-line declaration to the trajectory section: "All numbers above are on consistent scope (segments, geography, FX, fiscal year, GAAP basis). Footnote any line where the basis changed." If you cannot verify consistency from the report itself, say so — flag the line as "basis not verified" rather than reporting a clean percentage move that may be optical.

17. **The unstated-falsifier prompt — what would make the analyst wrong?** Risks sections in sell-side notes are overwhelmingly boilerplate (cyclical risk, customer concentration, China exposure, regulatory). The actual thesis-killer — the specific scenario that, if it materialised, would invalidate the bull case — is almost never named, because naming it would undermine the report. The skill catches some of these via topic-specific pitfalls (Pitfall 13 for headline-vs-realised price, for example), but those only fire when the pattern matches a known template. There is no general mechanism for finding the unstated falsifier. To operationalise: after extracting the thesis from any report (or the consensus thesis from a Mode 5 stack), write down in one sentence what would have to happen for the thesis to be wrong — not "things get worse" but a specific, observable scenario. Then search the report for any acknowledgment of that scenario. If the report doesn't address its own falsifier, name the gap explicitly in the output as "Unstated falsifier: [scenario]. Not addressed in report." This forces the reader to do the work the analyst didn't, and it tends to surface exactly the risks that get repriced violently when they materialise. Apply this to every playbook, not just Mode 5 — a single sell-side note deserves the prompt as much as a stack does.

**Coverage gap matrix — always include in Mode 5 output.**

Build a small table with topics as rows and reports as columns. Fill cells with ✓ (covered substantively), partial (mentioned but not analysed), or — (not addressed). The matrix should surface, at a glance:
- Which risks/catalysts only one house flags
- Which topics every house wants from the next earnings call (these are the "want from call" rows)
- Where sector reports cover ground that company-specific reports ignore (the most common gap)

Example shape:

```
| Topic                          | GS Co  | JPM Co | BofA Sector |
|--------------------------------|:------:|:------:|:-----------:|
| Segment-by-segment build       |   ✓    | partial|     —       |
| HBM4 qualification status      |   ✓    |   ✓    |     ✓       |
| Labor strike risk (May 2026)   |   —    |   ✓    |     —       |
| China NAND supply overhang     |   —    |   —    |     ✓       |
| TCB / packaging back-end       |   —    |   —    |     ✓       |
```

Topics that show up as ✓ in only one column are the alpha — the things readers of the other reports will miss.

#### Mining sector / industry reports for company-specific data

When the user has a company of interest and the stack includes sector-level reports (BofA Memory Tech, GS Korean Tech, MS Global Semis, etc.), do not treat those sector reports as mere "context". Mine them.

**Procedure:**

1. **Search every sector report for the company name** and any obvious aliases (Samsung / SEC / Samsung Electronics / 005930.KS / Korea memory leader; SK Hynix / Hynix / 000660.KS).

2. **Identify every exhibit, table, and paragraph that names the company.** Sector reports almost always contain company-specific rows in their bottom-up tables (DRAM forecast comparison, capex by company, market share by company, valuation peer table) and sometimes a full company-dedicated exhibit (e.g. "SEC HBM earnings outlook" embedded in a sector deck). Extract all of them.

3. **Treat the company-specific data as direct evidence**, with one caveat: the data is anchored to the sector report's publication date, not the current date. If the sector report is materially older than the company-specific reports in the stack, the sector report's forecasts may be pre-revision and need to be flagged accordingly (see also rule 2 above on consensus vintage — the same logic applies to entire reports, not just consensus prints inside them).

4. **Label everything in the output as either "Direct" (from a company-specific report) or "Sector-mined" (from a sector report's company-specific row/exhibit).** This helps the reader calibrate confidence — sector-mined data is usually higher-quality than text inference but lower-quality than the latest direct report.

5. **The most valuable sector-mined data points are usually:** bottom-up earnings/ASP/margin forecasts by company, capex by company, market share by company, peer valuation tables, and any company-dedicated exhibit. Always surface the company-specific row from each of these tables.

6. **Cross-check sector-mined forecasts against direct-report forecasts.** Where they disagree, the gap itself is informative — large gaps usually indicate a major news event (earnings prelim, guidance change, sector rotation) between the two report dates.

7. **Lower the threshold: single-paragraph mentions count.** The procedure above is built around tables and exhibits, but the most valuable sector-mined data point is sometimes a single paragraph in a cross-house note that the company's own coverage hasn't picked up yet. Even a one- or two-paragraph mention is worth surfacing if it contains any of: a new product category, a partnership, a regulatory event, a customer win/loss, a guidance reference, a competitor disclosure that reframes the company's positioning, or a technical/architectural change that affects the company's TAM. The test is not "is there a table?" but "would the company-coverage analyst write differently if they'd read this paragraph?" If yes, mine it. Operationally: grep for the ticker and the company name across every non-coverage report in the stack, read every paragraph that contains either, and surface anything that meets the test above as a labelled "Sector-mined (paragraph)" item — distinguish from "Sector-mined (table/exhibit)" so the reader can calibrate confidence. Paragraph mentions are lower-confidence than table data but higher-signal than text inference, and they are routinely the only place where a strategically important development first appears in the stack.

#### Single-house sequential weekly series

Sometimes the stack is not "GS vs JPM vs MS on the same day" but "the same analyst on the same name across four weeks". The standard Mode 5 framing — consensus dispersion, coverage gaps, who's the bull and who's the bear — does not work cleanly here. There is only one voice, and the comparison is the analyst against their own prior self.

The framing for this case differs in three specific ways:

**1. The "second voice" is whichever data provider the analyst keeps citing.** Sequential weeklies almost always lean on a regular external data feed — TrendForce or DRAMeXchange for memory, IDC or Counterpoint for handsets, Wood Mackenzie or Rystad for energy, IHS Markit for autos, Bloomberg or FactSet for consensus. Treat that provider as a de facto second analyst in the comparison. If the provider's number leads and the analyst's number follows, that is a forecast convergence pattern (rule 11) and should be surfaced exactly as it would be in a cross-house stack. The provider deserves credit for whichever direction they called first.

**2. The estimate-revision trajectory is the centrepiece, not a side table.** In a cross-house stack the trajectory section (already required when ≥3 reports span >4 weeks) is one diagnostic among many. In a single-house weekly series it is *the* diagnostic — the entire value of having four reports instead of one is to see the analyst's number move. Always lead the body of the output with the trajectory table, before any valuation or risk discussion.

**3. The coverage gap matrix becomes a "what was top-of-mind that week" grid, not an alpha-finder.** In a cross-house stack, topics that show up in only one column are alpha (the analyst who covers something the others missed). In a single-house weekly stack, topics that show up in only one column are usually just whatever the analyst was reacting to that week — a TrendForce call, a competitor's earnings, an industry conference, a discrete corporate event. The matrix is still worth building because a reader of any single weekly will miss everything that appeared in the other three, but the framing should be "what a single-week reader misses", not "where the analyst has unique insight".

**A useful template for the single-house sequential case:**

```
# [Subject] — [House] weekly series, [Date range]

## Bottom line
[Lead with the overall trajectory: is this consensus catch-up, genuine
 re-rating, or capitulation to a price? Name the three-way race shape
 (Rule 13). If the analyst is chasing a third-party data provider, name
 the provider and the date they called it. If any reports are missing
 from the stack, say so here.]

## Missing-report check
[List any interim revisions evidenced by OLD/strikethrough/prev. tags
 that don't correspond to a report in the stack, with the implied
 dates. Flag whether the gap is material. See Rule 14.]

## Three-way race (EPS / spot / PT)
[One line: "Over [date range]: EPS +X%, spot +Y%, PT +Z%." Name the
 shape (PT>EPS>spot, EPS>spot>PT, etc.) and what it implies. This
 frames the rest of the analysis. See Rule 13.]

## Estimate-revision trajectory
[Required and central. One row per key forecast line, one column per
 report. Spot the direction; spot any methodology switches; spot any
 reversals. End with the consistency declaration: "All numbers above
 are on consistent scope (segments, geography, FX, fiscal year, GAAP
 basis)" — or footnote the lines where basis changed. See Rule 16.]

## Forecast convergence check
[Was there a third-party number cited in the early reports that the
 analyst's own number eventually moved toward? If yes, surface it
 with dates and the size of the gap closure. See Rule 11.]

## Headline-vs-realised divergence
[For commodity/cyclical names: is the report headlining a high-frequency
 benchmark price that diverges from the realised price the company
 actually books? If yes, this is the most important watchpoint.
 See Pitfall 13.]

## Anchored-headline check
[Did any headline number — PT or multiple — stay constant across reports
 while the underlying definition shifted (framework, EPS denominator,
 multiple level, EV vs equity)? Quote both derivations side by side.
 See Rule 12.]

## Bull-case sanity check
[For any bull case in the stack: implied peak GM%, OpM%, revenue.
 Compare each against prior-cycle peak. Flag anything more than ~10
 points above prior peak without a structural justification. See
 Rule 15.]

## Unstated falsifier
[One sentence: what specific scenario would make the thesis wrong?
 Then: does any report in the stack address it? If not, name the gap.
 See Rule 17.]

## Coverage gap matrix
[Topic-by-week grid, framed as "what a single-week reader misses".]

## Valuation-multiple trajectory
[For each report, the implied forward multiple on the furthest-out
 EPS the report models. Compression while PT rises = catch-up; expansion
 while EPS stable = re-rating. See Rule 9.]

## My read
[Which report to trust for the numbers, which for the risks the analyst
 has since dropped, and who outside the house called the direction first.]
```

---

## Common pitfalls

1. **Trusting `pdfimages` for charts.** It only extracts raster images. Vector charts (the majority in modern research) will be invisible. Always rasterize the page when charts matter. **If `pdfimages -list` returns zero, treat that as a red flag — every chart is vector and will be silently missed unless you rasterize.**
2. **Linear reading of long reports.** A 200-page annual report read page-by-page burns context for no benefit. Use the TOC and triage.
3. **Reading the disclosures.** The last 3–10 pages of any sell-side note are boilerplate. Stop early.
4. **Quoting verbatim.** Investment research is copyrighted. Paraphrase the thesis; quote ≤15 words and only when wording is load-bearing. Never reproduce charts as images in the response — describe them.
5. **Missing the date.** A report from 18 months ago may be entirely stale. Always surface the publication date in the summary. For sell-side notes, also surface the **reference price date** — it's often a day or two before publication and matters on volatile stocks.
6. **Ignoring footnotes.** "Excluding one-offs", "constant currency", "pro forma" — these footnotes change what the headline number actually means. When extracting numbers, pull the footnote with them.
7. **Cover-page rating drift.** Sell-side covers sometimes show the *new* rating prominently and the *prior* rating in small print. Always extract both.
8. **Treating consensus as a single number.** Different houses cite consensus from different vintages and providers (Visible Alpha, Bloomberg, Refinitiv, FactSet) with different cut-off dates. When comparing reports, two "consensus" figures that disagree don't mean one analyst is wrong — they usually mean different sources. Flag the discrepancy and name the source if possible.
9. **Missing chart-vs-narrative contradictions.** The most common case: a P/B or P/E history chart shows the stock at the top of its historical range while the prose argues for "attractive valuation". If a chart undermines the narrative, that's the most important thing on the page — call it out explicitly.
10. **Not flagging stale reference prices in multi-report comparisons.** Two reports published the same day on the same stock may use reference prices a full trading session apart. The headline upside % can differ by 10%+ for an identical price target. Always check the as-of date on every reference price.
11. **Missing the stranded rating.** When one report in a multi-report stack has a price target more than 30% away from the current spot and has not been refreshed, that report is effectively a historical document — its rating is mechanically invalid until the analyst revisits it. Failing to flag this loudly is the most common way a triangulation output misleads the reader. Always compute the PT-to-current-spot gap for every report in the stack, and lead with any stranded ratings in the bottom line. See Mode 5 rule 10.
12. **Treating rising price targets as uniform bullishness.** Two reports may both be raising PTs while doing very different things underneath. One may be re-rating the multiple on stable EPS (genuinely more bullish on valuation); the other may be keeping the multiple flat or compressing it while EPS estimates catch up to buyside (consensus catch-up). These have different implications for the stock's remaining runway. Always decompose a PT change into its EPS component and its multiple component before calling a report "more bullish". See Mode 5 rule 9.
13. **Headline-price vs realised-price divergence.** Many sell-side reports — especially in commodities, semis, energy, materials, and shipping — headline a high-frequency benchmark (spot DRAM, LME copper, WTI, Baltic Dry, NYMEX gas) while the underlying company's revenue tracks a slower-moving realised price (contract DRAM, producer realised, hedged book, long-term offtake). When the spot rolls over and the contract is still rising — or vice versa — the headline can point one direction while the company's reportable number points the other. Always cross-check: does the price chart on the cover match the price line that drives the model? If not, the headline is optical, not analytical. This pattern is most acute at cycle inflection points, which is precisely when getting the call right matters most.
14. **Anchored headline with shifting definition.** Within a single analyst's coverage over time, a headline number (PT or multiple) held constant across multiple reports while the underlying definition changes — framework label (P/B to P/E, DCF to comps), EPS denominator (FY27 to FY26-29 average, peak to through-cycle, GAAP to non-GAAP), multiple level, or EV vs equity basis — is almost always a sign the analyst has stopped arguing for the headline on its merits. The shift is rarely acknowledged in the prose. Always diff the price-objective-basis paragraphs verbatim across sequential same-house reports on all four axes; identical headline plus any one of those four axes changing equals an anchored-headline pattern. Treat the second definition as the analyst's revealed-preference rationalisation. See Mode 5 Rule 12.
15. **Missing reports in sequential stacks.** When the user uploads a sequential same-house stack, the most common quality problem is not what's in the reports but what's missing between them. An interim revision can hide a methodology switch or estimate jump that happened in one shot. Always scan every report's ticker table, comp table, and headline language for `OLD`, strikethrough numbers, "(prev. $X)", or "previously $Y" annotations. Each one is evidence of a report that exists but isn't in the stack. List them in the trajectory section as "interim revision: not in stack" so downstream diagnostics aren't silently treating a stepwise jump as a smooth catch-up. See Mode 5 Rule 14.
16. **Three-way race shape misreading.** Multiple compression (Pitfall 12), stranded ratings (Pitfall 11), and forecast convergence (Rule 11) are all special cases of a more general pattern: the relative ordering of EPS revisions, spot price moves, and PT changes over a sequential stack. Reading any one of them in isolation can mislead. Always compute all three percentage changes from the first report to the last and surface them as a single line. The shape — PT>EPS>spot, EPS>PT>spot, EPS>spot>PT, spot>PT>EPS, EPS>spot≈PT — tells you who's leading and who's chasing. See Mode 5 Rule 13.
17. **Unexamined bull cases.** Bull and blue-sky scenarios are routinely the least stress-tested numbers in any report. Implied peak gross margins frequently exceed prior-cycle peaks by 10+ points without any structural justification beyond "AI demand", and the dollar PT does the optical work while the underlying margins go unchecked. Always extract the peak-year GM%, OpM%, and revenue from any bull case and compare to prior-cycle peaks before treating the dollar number as meaningful. See Mode 5 Rule 15.
18. **Optical revisions from basis changes.** Large QoQ moves in trajectory tables are sometimes artefacts of fiscal year basis changes, segment scope changes after divestitures or acquisitions, FX assumption changes, GAAP-to-non-GAAP switches, or share count changes — not real upgrades. None of these look like artefacts in a side-by-side table; all of them look like upgrades. Any line where the change exceeds ~25% must be cross-checked against the report's own footnotes for basis consistency before being reported as a clean revision. See Mode 5 Rule 16.
19. **Unstated falsifiers and boilerplate risk sections.** The risks section in a sell-side note is overwhelmingly boilerplate (cyclical, customer concentration, China, regulatory). The actual thesis-killer — the specific scenario that would invalidate the bull case — is almost never named, because naming it would undermine the report. Always write down in one sentence what specific, observable scenario would have to materialise for the thesis to be wrong, then search the report for any acknowledgment of it. If the report doesn't address its own falsifier, name the gap explicitly. The unstated falsifier is usually exactly the risk that gets repriced violently when it materialises. See Rule 17.

---

## Reference: tool cheat sheet

| Task | Tool | One-liner |
|---|---|---|
| Inspect | `pdfinfo` | `pdfinfo file.pdf` |
| Image inventory | `pdfimages` | `pdfimages -list file.pdf` |
| Text (layout) | `pdftotext` | `pdftotext -layout file.pdf out.txt` |
| Text (Python) | `pdfplumber` | `page.extract_text()` |
| Tables | `pdfplumber` | `page.extract_tables()` |
| Rasterize page | `pdftoppm` | `pdftoppm -jpeg -r 200 -f N -l N file.pdf /tmp/p` |
| Extract images | `pdfimages` | `pdfimages -png file.pdf /tmp/img` |
| Attachments | `pdfdetach` | `pdfdetach -saveall -o /tmp/ file.pdf` |

For deeper PDF mechanics (OCR, encrypted PDFs, font issues), see `/mnt/skills/public/pdf-reading/SKILL.md`.

---

## Changelog

**v3.3 — adds seven improvements motivated by a four-report SNDK stack** (Bernstein Jan 14, Bernstein Jan 26, JPM Feb 26, Bernstein Apr 9, 2026) in which Bernstein raised FY27 EPS by 173% and the price target by 116% over twelve weeks while the FY27 multiple compressed from 11.0x to 8.7x; the headline "11x" survived all three Bernstein reports while its EPS denominator silently shifted from FY27 to FY26-29 average; the JPM cross-house note contained a single two-paragraph mention of an HBF partnership that the Bernstein coverage never picked up; and Bernstein's blue-sky case carried an 86.7% gross margin without any comparison to prior-cycle peaks.

- **Rule 12 broadened from framework-switch to definition-switch.** The original Rule 12 caught only full valuation-framework switches (P/B to P/E, DCF to comps). The SNDK stack showed the subtler and more common version: same framework (P/E in both reports) but the EPS denominator silently shifted from FY27 to FY26-29 through-cycle average, while the headline "11x" stayed verbatim. Rule 12 now requires diffing the price-objective-basis paragraphs on four axes — framework label, denominator definition, multiple level, and EV vs equity basis. Pitfall 14 updated to match.
- **New Rule 13 — Three-way race between EPS, spot, and PT.** A general framing that subsumes multiple compression (Rule 9), forecast convergence (Rule 11), and stranded ratings (Rule 10). Compute the percentage change in the furthest-out EPS, the spot/reference price, and the PT from the first to the last report in a sequential stack; the relative ordering is itself a diagnostic. Five named shapes, each with a different implication for runway. Required as a single line in the trajectory section, framed before the other diagnostics. Pitfall 16 added.
- **New Rule 14 — Missing-report detection.** Sequential stacks frequently have holes. Scan every report's ticker table, comp table, and headline for `OLD`, strikethrough, or "previously $X" annotations; each is evidence of an interim revision not in the stack. Required check during triage. List interim revisions explicitly so trajectory analysis (Rules 9, 11, 12, 13) doesn't silently treat the gap between two endpoints as a smooth path. Pitfall 15 added.
- **New Rule 15 — Bull-case sanity check against prior-cycle peaks.** Bull cases are the least stress-tested numbers in any report; readers anchor on the dollar PT and skip the implied margin profile. Always extract implied peak-year GM%, OpM%, and revenue from any bull case and compare to prior-cycle peaks. Flag any bull case more than ~10 points above prior-peak without a structural justification. Wired into Playbook A so it fires on single reports too. Pitfall 17 added.
- **New Rule 16 — Unit and definition consistency check across trajectories.** Large QoQ revisions in trajectory tables can be artefacts of fiscal year basis, segment scope, FX, or GAAP basis changes rather than real upgrades. Any line moving more than ~25% must be cross-checked against the report's own footnotes for basis consistency before being treated as like-for-like. Required declaration in the trajectory section. Pitfall 18 added.
- **New Rule 17 — Unstated-falsifier prompt.** Risks sections are overwhelmingly boilerplate; the actual thesis-killer is almost never named. After extracting the thesis, write down the specific observable scenario that would invalidate it and search the report for any acknowledgment. Apply to every playbook, not just Mode 5 — wired into Playbook A. Pitfall 19 added.
- **Sector-mining threshold lowered to single-paragraph mentions.** The original sector-mining procedure assumed tables and exhibits. The SNDK stack showed that the most strategically important data point — the JPM HBF partnership — appeared as a two-paragraph mention with no table. New step 7 in the sector-mining procedure: even one- or two-paragraph mentions are worth surfacing if they contain a new product category, partnership, regulatory event, customer win/loss, guidance reference, competitor reframing, or technical/architectural change. The test is "would the company-coverage analyst write differently if they'd read this paragraph?"
- **Mode 5 sequential output template updated** with sections for missing-report check, three-way race, anchored-headline check (replacing anchored-target check), bull-case sanity check, unstated falsifier, and a basis-consistency declaration in the trajectory section.

**v3.2 — adds five improvements motivated by a four-report single-house sequential stack** (BofA Global Memory Tech weeklies, Jan–Apr 2026) in which the analyst spent 13 weeks closing the gap to a TrendForce forecast cited in their own February note, raised a price target by 18% while compressing the implied multiple from 7.4x to 4.3x, kept a separate coverage stock at the same target across two reports while switching the valuation framework from P/B to P/E, and headlined a spot-price series that had been rolling over for three weeks while their contract-price forecast was still rising.

- **New Mode 5 sub-section: Single-house sequential weekly series.** A separate framing for when the stack is one analyst over time rather than multiple analysts in a snapshot. The estimate-revision trajectory becomes the centrepiece; the coverage gap matrix becomes "what a single-week reader misses"; the third-party data provider becomes the de facto second voice. Includes its own output template.
- **Rule 11 — Forecast convergence to a named third party.** When an analyst's number moves over multiple reports toward a publicly-stated forecast from TrendForce, IDC, Wood Mackenzie, etc., that is consensus catch-up to a third party — distinct from the within-model multiple compression of rule 9 — and the third party deserves credit for calling it first. Operationalised as a scan-for-named-providers step in any ≥3 report sequential stack.
- **Rule 12 — Anchored target with shifting methodology.** The within-house cousin of rule 1 (identical cross-house targets with different math). When a single analyst keeps a price target constant across reports but switches the valuation framework, that is almost always capitulation to a price level rather than a model output. Operationalised as a verbatim diff of price-objective-basis paragraphs in sequential same-house reports.
- **Pitfall 13 — Headline-price vs realised-price divergence.** Reports headline high-frequency benchmarks (spot DRAM, LME copper, WTI, Baltic Dry) while underlying revenue tracks slower realised prices (contract DRAM, producer realised, hedged book). At cycle inflection points the two can point opposite directions. Always cross-check the cover chart against the model's price assumption.
- **Pitfall 14 — Anchored target with shifting methodology.** Pitfall sibling of rule 12.
- **Step 3 — In-context PDF handling.** When PDFs arrive as `document` blocks with `media_type: application/pdf` rather than filesystem paths, the visual layer is already available without rasterization. New subsection at the top of Step 3 distinguishes the two delivery modes and notes that `pdftoppm` is not needed in the in-context case.

**v3.1 — adds three rules to Mode 5 (multi-report triangulation)**, motivated by a three-report LITE stack (UBS Feb 3, MS Mar 18, JPM Apr 9) in which the stock roughly doubled over ten weeks, FY28 EPS estimates moved from $8.54 to $30.50, and one report's price target ended up 76% below spot without being refreshed.

- **Rule 8 — Event-anchored timelines.** When sequential reports are driven by one or two discrete events, organise the comparison around the events, not publication dates. Added a corresponding "Event-anchored timeline" section to the Mode 5 output template.
- **Rule 9 — Multiple-compression tracking.** Rising targets built on compressing multiples are consensus catch-up, not re-rating; the distinction matters for whether a move has legs. Added as a required decomposition of any PT change.
- **Rule 10 — The stranded rating pattern.** When a report's price target is more than 30% away from current spot and hasn't been refreshed, the rating is a historical artefact. Trigger a "stranded rating" tag automatically; lead the bottom line with it when it occurs. This is the inverse of the beat-vs-performance paradox and deserves equal billing.
- Added an "Estimate-revision trajectory" section to the Mode 5 output template, required when ≥3 reports span >4 weeks.
- Added pitfalls 11 (stranded rating) and 12 (uniform-bullishness fallacy) to support the new rules.

**v3.0 and earlier** — base skill (sell-side playbook, 10-K playbook, factsheet playbook, multi-report triangulation foundations, sector report mining, chart-vs-narrative contradiction surfacing, beat-vs-performance paradox).
