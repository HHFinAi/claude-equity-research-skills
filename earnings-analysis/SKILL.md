---
name: earnings-analysis
description: >-
  Institutional-quality earnings analysis for public equities. Parses 10-Qs,
  earnings releases, and call transcripts into a 4-layer framework (Parse →
  Compare → Diagnose → Decide), runs a mechanical scoring engine that produces
  a composite verdict across beat quality, operational health, and management
  signals, and outputs a one-page earnings sheet, full memo (Word doc), risk
  map, or trade note. Use when asked to analyse earnings, review quarterly
  results, parse a 10-Q, summarise an earnings call, assess earnings quality,
  evaluate beat/miss dynamics, diagnose guidance changes, or produce a
  post-print memo. Triggers include "what did [company] report", "how were
  earnings", "earnings surprise", "quarter review", "results analysis",
  "post-print analysis". Do NOT use for DCF models, long-term thesis work,
  technical analysis, or metals analysis — use the dedicated skills for those.
metadata:
  author: Ed
  version: 1.4.1
  tags:
    - earnings-analysis
    - equity-research
    - quarterly-results
    - financial-statements
    - earnings-call
    - 10-Q
    - investment-research
---

# Earnings Analysis: Institutional-Quality Quarterly Review Framework

## Overview

This skill transforms raw earnings materials (filings, releases, transcripts) into structured investment-grade analysis. It moves beyond simple beat/miss reporting to diagnose *why* results deviated, *what matters* for the forward thesis, and *what action* follows — the way a senior buyside analyst processes a quarter.

**Philosophy**: The market doesn't pay for knowing what happened. It pays for knowing what changed, whether it's repeatable, and what's mispriced. Every earnings analysis must answer: "So what? What do I do now?"

**Two-part architecture.** The skill is a four-layer analytical framework (Parse → Compare → Diagnose → Decide) anchored by a Python scoring engine at `scripts/score_earnings.py` that produces a mechanical composite verdict, flag inventory, and expectations regime classification. The scorer runs at the end of Step 2 and anchors the judgment work in Steps 3 and 4 — it is an input to the diagnosis, not a replacement for it.

## Input Types & Parsing Priority

The skill handles these inputs, in priority order:

| Input Type | What to Extract | How to Access |
|------------|----------------|---------------|
| **User-uploaded files** | Full filing/transcript content | Read from `/mnt/user-data/uploads/` using `pdf-reading` or `file-reading` skills |
| **Earnings release / 8-K** | Headline KPIs, segment data, guidance, non-GAAP reconciliation | Parse uploaded file or search web |
| **10-Q / 10-K filing** | Revenue detail, margin breakdown, balance sheet, cash flow, MD&A | Parse uploaded file or search web |
| **Earnings call transcript** | Management tone, forward commentary, Q&A signals, guidance language | Parse uploaded file or search web |
| **Consensus estimates** | Revenue, EPS, margin expectations, whisper numbers | Web search (Yahoo Finance, Visible Alpha, Seeking Alpha) |
| **Historical quarter data** | Sequential and YoY comparison base | Web search or user-provided |

If files are provided, always start there. If no files, use `web_search` to find the latest earnings materials. Aim for 5–8 searches to gather comprehensive data including consensus expectations and stock reaction context.

---

## Workflow

### Step 0: Input Triage

Before analysis begins, determine what materials are available:

1. Check `/mnt/user-data/uploads/` for uploaded files
2. If files exist, read them using the appropriate method (`/mnt/skills/public/pdf-reading/SKILL.md` for PDFs, `/mnt/skills/public/file-reading/SKILL.md` for other formats)
3. If no files, search for: `[Company] Q[X] [Year] earnings results`, `[Company] earnings call transcript Q[X] [Year]`, `[Company] consensus estimates`, `[Company] stock reaction earnings`
4. Identify the fiscal quarter and reporting date
5. Note what's available vs missing — missing inputs aren't fatal but affect analysis depth

**Validation gate — do not proceed until confirmed:**
- [ ] Company identified with ticker, sector, market cap
- [ ] Reporting quarter identified (fiscal quarter, calendar date)
- [ ] At least ONE primary source obtained (earnings release, filing, or transcript)
- [ ] Prior quarter and prior year baseline data located (or flagged as unavailable)

---

### Step 1: PARSE — Extract Structured Data

Extract data points systematically. Use `references/parsing-checklist.md` for sector-specific KPIs.

#### 1A. Financial KPIs

| Category | Metrics to Extract |
|----------|-------------------|
| **Revenue** | Total revenue, organic growth %, segment breakdown, geographic mix, recurring vs one-time, ASP vs volume decomposition |
| **Margins** | Gross margin, operating margin, EBITDA margin, net margin; GAAP vs non-GAAP reconciliation; SBC as % of revenue |
| **Earnings** | GAAP EPS, adjusted EPS, non-GAAP reconciliation items, share count, buyback contribution to EPS |
| **Cash Flow** | Operating cash flow, free cash flow, capex (growth vs maintenance), working capital, DSO/DIO/DPO trends |
| **Balance Sheet** | Cash, total debt, net debt, debt maturity profile, inventory, goodwill/intangibles, deferred revenue |

#### 1B. Forward Indicators

| Category | What to Extract |
|----------|----------------|
| **Guidance** | Revenue range, EPS range, margin guidance, capex plans, new metrics guided; compare to prior guidance (raised/maintained/lowered); note magnitude (modest/meaningful/massive) |
| **Backlog / Pipeline** | Order book, RPO, bookings, book-to-bill ratio |
| **Leading KPIs** | DAU/MAU, ARR/NRR, same-store sales, subscriber count, pipeline conversion — whatever is sector-relevant |

#### 1C. Management Language Signals

Parse the earnings call transcript (or MD&A section) for:

| Signal Type | What to Flag |
|-------------|-------------|
| **Confidence markers** | "Confident", "strong visibility", "accelerating", "ahead of plan", "raising" |
| **Hedging markers** | "Cautiously optimistic", "uncertain environment", "monitoring closely", "prudent" |
| **Deflection markers** | Pivoting away from questions, "we don't guide to that", avoiding previously guided specifics |
| **New language** | Terms appearing for the first time — often signals strategic pivots or emerging risks |
| **Tone shift** | Compared to prior quarter: is management more/less bullish on specific segments? |
| **Q&A tells** | Which topics drew most follow-ups? What did management dodge? What got a surprisingly detailed answer? |

#### 1D. Stock Context (for Scorer)

Collect data needed to classify expectations elevation:

- Trailing 12-month stock return (%)
- Percentage recovery from 52-week low (%)
- Current drawdown from all-time high (%)
- Stock reaction to the print (positive / flat / negative)

These inputs feed the expectations elevation classifier in the scoring engine, which determines how the market's reaction should be interpreted relative to the underlying fundamentals.

**Validation gate — do not proceed until confirmed:**
- [ ] Revenue, EPS, margin extracted (GAAP and non-GAAP where applicable, or flagged as unavailable)
- [ ] At least one forward indicator captured (guidance, backlog, or leading KPI, or flagged as unavailable)
- [ ] Management language scan completed (or flagged as "no transcript available")
- [ ] Stock context collected for scorer inputs (or flagged as unavailable — scorer will use neutral defaults)
- [ ] Data gaps explicitly noted for the diagnosis step

Missing inputs are not blockers. The scorer accepts partial input and applies neutral defaults for anything not passed. The cost of missing data is interpretive, not mechanical: list every assumed input in Step 3 so the reader knows which dimensions of the verdict rest on disclosed data versus defaults.

---

### Step 2: COMPARE — Multi-Horizon Benchmarking

Every extracted metric needs context. Raw numbers are meaningless without a reference frame.

#### 2A. Sequential (QoQ) Comparison

- Revenue growth trajectory: accelerating, stable, or decelerating?
- Margin expansion or compression vs prior quarter?
- Cash conversion trend?
- Guidance change: raised, maintained, or lowered vs prior quarter's guidance?

#### 2B. Year-over-Year (YoY) Comparison

- Organic revenue growth (exclude acquisitions, FX, one-offs)
- Margin change with driver attribution (mix shift, pricing, cost, scale)
- EPS growth decomposed into operational vs financial engineering (buybacks, tax rate, below-the-line items)

#### 2C. Versus Consensus

The market prices off expectations, not absolutes. This is the most important comparison.

| Metric | Reported | Consensus | Delta | Interpretation |
|--------|----------|-----------|-------|----------------|
| Revenue | | | | Beat/miss magnitude; quality of beat (one-time vs sustainable) |
| EPS | | | | Decompose: operational or below-the-line? |
| Guidance midpoint | | | | Forward expectations raised/lowered? |
| Key segment | | | | Where did the surprise come from? |

**Beat quality matters more than beat size.** A 2% revenue beat from pull-forward demand is worse than a 0.5% beat from new customer wins. Always diagnose the source. Also note whisper numbers where available — a beat that meets consensus but misses whisper will trade negatively.

#### 2D. Versus Peers

- Did the company outperform or underperform sector trends?
- Are margin differences structural or timing-driven?
- Is the company gaining or losing share?

#### 2E. Versus Valuation History

- Current forward P/E vs 5-year average
- EV/Revenue or EV/EBITDA relative to growth rate
- How has the market historically repriced this stock after similar quarters?

---

### Step 2.5: RUN THE SCORING ENGINE

Once Compare is substantially complete, invoke the scorer to produce a mechanical composite verdict that anchors Steps 3 and 4. The scorer is at `scripts/score_earnings.py`. Read `references/scoring-engine.md` first for the full input schema, verdict tiers, flag library, and sample invocation.

The scorer output gives you:
- Composite score (integer, typically -15 to +18)
- Base verdict tier (STRONG / SOLID / MIXED / WEAK / PROBLEMATIC)
- Verdict suffix modifiers where applicable (_AT_PEAK, _EXPECTATIONS_OVERRUN, _WITH_CRITICAL_FLAGS)
- Expectations regime (constructive / overrun / whisper_overrun / depressed / balanced / deteriorating)
- Expectations elevation (low / medium / high / extreme)
- Complete flag inventory with narrative text
- Output recommendation (which deliverables to produce)

Treat the scorer verdict as a hypothesis to be validated or overridden by the judgment work in Step 3. If you disagree with the scorer, explain why — the scorer catches mechanical patterns but can miss narrative, competitive, or regulatory context that matters for the investment thesis.

**Validation gate — do not proceed until confirmed:**
- [ ] QoQ and YoY comparison completed for revenue, margins, EPS (or flagged as unavailable for the missing periods)
- [ ] Consensus comparison completed where consensus is available (flag explicitly if no consensus could be located)
- [ ] Beat/miss quality diagnosed (operational vs one-time/financial engineering)
- [ ] Forward guidance compared to consensus expectations (or flagged as not provided / no consensus)
- [ ] Scoring engine invoked and output captured (partial inputs are acceptable; document assumed defaults)

---

### Step 3: DIAGNOSE — Explain What Changed and Why

This is the analytical core. Move from *what happened* to *why it happened* and *whether it persists*. Every scorer flag that fired must be addressed in the diagnosis.

#### 3A. Growth Diagnosis

- What drove the revenue delta? (volume, pricing, mix, FX, acquisitions, one-offs)
- Is the growth rate accelerating, stable, or decelerating? What's the second derivative?
- Are leading indicators (bookings, pipeline, DAU, ARR) confirming or diverging from reported growth?
- Is growth quality improving? (recurring > one-time, organic > acquired, high-margin > low-margin)

#### 3B. Margin Diagnosis

- Was margin change driven by gross margin or opex leverage?
- Gross margin drivers: input costs, pricing power, mix shift, scale
- Opex drivers: hiring pace, R&D investment, S&M efficiency, G&A leverage
- For high-GM businesses (pharma, software, luxury), operating margin trajectory matters more than gross margin — OPM compression without GM compression signals operating deleverage or opex ramp
- Is SBC growing faster than revenue?
- Is management guiding for margin expansion or reinvestment?

#### 3C. Cash Quality Diagnosis

- OCF/NI conversion — is earnings quality high? (OCF is more reliable than FCF for quality signal because it excludes capex noise)
- FCF/NI conversion — and is low FCF a quality concern or a growth capex mode signal?
- Working capital — is DSO rising (revenue recognition concern)? Is inventory building (demand risk)?
- Capex intensity — growth vs maintenance split; what's the return profile?

#### 3D. Balance Sheet Risk Diagnosis

- Net debt trajectory — improving or deteriorating?
- Debt maturity wall — any near-term refinancing risk?
- Goodwill/intangibles as % of total assets — impairment risk?
- Off-balance-sheet exposures (operating leases, unconsolidated entities, guarantees)

#### 3E. Narrative Shift Diagnosis

This is often the most alpha-generative layer.

- Has management's strategic narrative changed from prior quarters?
- Are there new buzzwords, new segment disclosures, or new metrics being emphasised?
- Has the investment thesis evolved? (growth story becoming a margin story, or vice versa)
- What did management stop talking about? (often more telling than what they started saying)
- Did the CEO/CFO tone shift between prepared remarks and Q&A?

**Validation gate — do not proceed until confirmed:**
- [ ] Growth, margin, and cash flow drivers each diagnosed with specific attribution
- [ ] Repeatability assessed for each major driver (one-time vs structural)
- [ ] Narrative shift (or continuity) identified with evidence
- [ ] Every scorer flag that fired has been addressed in the diagnosis
- [ ] At least one non-obvious insight surfaced beyond the headline beat/miss

---

### Step 4: DECIDE — Translate to Investment Action

The final layer converts diagnosis into actionable output.

#### 4A. The Verdict: What Changed

Summarise in 2–3 sentences:
- What is the single most important thing that changed this quarter?
- Does this change strengthen, weaken, or leave unchanged the prior investment thesis?
- Is this a thesis-confirming, thesis-evolving, or thesis-breaking quarter?

The scorer verdict is the mechanical anchor. Your written verdict should agree with it or explicitly explain why you're overriding it.

#### 4B. Scenario Framework

| Scenario | Description | Probability | Implied Valuation |
|----------|-------------|-------------|-------------------|
| **Bull** | What goes right from here — extrapolate positive trends | | |
| **Base** | Current trajectory continues — management delivers on guidance | | |
| **Bear** | What could go wrong — risks materialise, growth disappoints | | |

For each scenario, describe the revenue/margin trajectory, the key assumption, and rough valuation implications.

#### 4C. Repricing Path

- What would cause the street to revise estimates up or down?
- Is there a catalyst calendar ahead? (next quarter, product launch, regulatory decision, M&A)
- Is the stock likely to re-rate on this quarter, or is it a "show me" story?

#### 4D. Trade/Research Implications

| If Position | Action | Rationale |
|-------------|--------|-----------|
| **Long** | Add / Hold / Trim / Exit | Why? What changed for the position? |
| **Short** | Cover / Hold / Add | Why? Is the bear case weakening or strengthening? |
| **No position** | Initiate / Watchlist / Pass | Why? What would trigger a position? |

#### 4E. Risk Triggers & Invalidation

Identify 3–5 specific, measurable conditions that would invalidate the current view:
- e.g., "If organic growth falls below 5% for two consecutive quarters"
- e.g., "If gross margin drops below 60% excluding one-time charges"
- e.g., "If management lowers FY guidance by more than 5% at midpoint"

These should be concrete and monitorable, not vague risk factors.

---

## Scoring Engine Reference

The scoring engine at `scripts/score_earnings.py` produces the mechanical composite verdict that anchors Steps 3 and 4. Before invoking it, read `references/scoring-engine.md` for the complete input schema, the three scoring layers, the expectations elevation and regime classifiers, verdict tiers and routing, the critical-flag override, and the full flag library.

**Defaults handling.** All scorer inputs have sensible defaults, so partial invocation is fine when source materials are incomplete. Any input not passed is treated as neutral (no flag fires, no score impact). When proceeding with missing inputs, list them explicitly in the Diagnose step so the reader knows which dimensions of the score rest on assumed values rather than disclosed data.


## Output Deliverables

The scoring engine's `output_recommendation` drives which deliverables to produce. Always honour the routing unless the user explicitly requests something different.

### Output 1: One-Page Earnings Sheet

Default output for STRONG_QUARTER cases. A single-page summary as a Word document. Read `/mnt/skills/public/docx/SKILL.md` before building.

Structure:

```
┌─────────────────────────────────────────────────┐
│  [Company] (TICKER) — Q[X] FY[YYYY]            │
│  Sector | Market Cap | Report Date              │
├─────────────────────────────────────────────────┤
│  VERDICT: [Scorer tier] — [1-sentence summary] │
├────────────────────┬────────────────────────────┤
│  KEY METRICS       │  BEAT / MISS SCORECARD    │
│  Revenue: $X.Xbn   │  Rev: Beat/Miss by X%     │
│  Gross Margin: XX% │  EPS: Beat/Miss by $X.XX  │
│  Op Margin: XX%    │  Guide: Raised/Held/Cut   │
│  EPS: $X.XX        │  Quality: Vol/Mix/Price   │
│  FCF: $X.Xbn       │                            │
├────────────────────┴────────────────────────────┤
│  WHAT CHANGED (3 bullets max)                   │
├─────────────────────────────────────────────────┤
│  GROWTH DRIVERS    │  MARGIN DRIVERS           │
├─────────────────────────────────────────────────┤
│  MANAGEMENT TONE: [tone] — [evidence]          │
├─────────────────────────────────────────────────┤
│  SCENARIO TABLE (Bull / Base / Bear)            │
├─────────────────────────────────────────────────┤
│  ACTION: [position-specific]                    │
│  RISK TRIGGERS: [2-3 invalidation conditions]   │
└─────────────────────────────────────────────────┘
```

### Output 2: Full Earnings Memo

Default output for SOLID, MIXED, WEAK, and PROBLEMATIC cases, and for any strong case with an AT_PEAK or EXPECTATIONS_OVERRUN suffix. A 4–6 page Word document. Read `/mnt/skills/public/docx/SKILL.md` before building.

- **Page 1**: Cover + Verdict — scorer output, composite score, base tier, regime, elevation, and a 2-sentence summary
- **Page 2**: Parsed Financials — segment breakdown, GAAP/non-GAAP reconciliation, KPI table
- **Page 3**: Comparison Matrix — QoQ, YoY, vs consensus, vs peers (table format)
- **Page 4**: Diagnosis — growth, margin, cash, balance sheet, narrative shift; must address every flag that fired in the scorer
- **Page 5**: Decision Framework — scenarios, repricing path, action, risk triggers
- **Page 6**: Appendix — paraphrased management quotes, Q&A summary, data sources

**Formatting.** Navy (#1B2A4A) headers, accent blue (#2E75B6) highlights, light grey (#F5F5F5) alternating rows. Body text 10pt Arial. Tables with thin borders. Concise — every sentence must earn its place.

### Output 3: Risk Map

Produced whenever the scorer's output_recommendation includes "+ RISK_MAP". A structured risk assessment as a markdown table or React component:

| Risk Category | Specific Risk | Probability | Impact | Trend | Monitoring Metric |
|--------------|--------------|-------------|--------|-------|-------------------|
| Growth | Deceleration | Med/High/Low | High/Med/Low | ↑↓→ | Organic growth rate |
| Margin | Input cost pressure | ... | ... | ... | Gross margin % |
| Regulatory | DOJ investigation | ... | ... | ... | Court filings, settlement disclosures |

For critical-flag cases, include a dedicated row for each critical flag with a specific monitoring metric and an explicit invalidation condition.

### Output 4: Trade Note

Produced on user request in addition to the default deliverables. 3–5 paragraphs for a portfolio manager or trading desk:

- Line 1: Ticker, quarter, beat/miss summary
- Para 1: What happened (2–3 sentences, numbers only)
- Para 2: What matters (the diagnosis)
- Para 3: What to do (the action)
- Final line: Key risk trigger

---

## Sector-Specific Parsing Extensions

Different sectors require different KPIs. Read `references/parsing-checklist.md` for the full sector-specific extraction guide. Key examples:

| Sector | Additional KPIs |
|--------|----------------|
| **SaaS / Cloud** | ARR, NRR, RPO, customer count, DBNR, Rule of 40, CAC payback |
| **Semiconductors** | Revenue by end market, ASP trends, utilisation, inventory channel fill, design wins, HBM/AI mix |
| **Biotech / Pharma** | Pipeline updates, FDA milestones, Rx volumes, launch curves, patent cliffs, R&D productivity |
| **Banks / Financials** | NIM, loan growth, deposit costs, credit quality (NCO, NPL, reserves), CET1, fee income mix |
| **Consumer / Retail** | Same-store sales, traffic vs ticket, inventory turns, e-commerce mix, promotional activity |
| **Industrials** | Organic orders, book-to-bill, backlog, price vs volume, segment margin bridge |
| **REITs** | FFO/AFFO, occupancy, lease spreads, same-property NOI, development pipeline |
| **Energy** | Production volumes, realised prices, unit costs, reserves replacement, breakeven price |

---

## Process Discipline

1. **Layer sequence matters.** Don't skip to judgment before parsing, comparing, and running the scorer. The framework is designed to prevent premature conclusions.
2. **Every scorer flag must be addressed in the diagnosis.** A flag that fires without comment is a missed opportunity; a flag that fires and is explained away is an explicit analytical choice.
3. **Be opinionated but transparent.** The best buyside research takes a view. Don't hedge with "on the one hand / on the other hand" — make a call and state what would change your mind. If you override the scorer verdict, explain why.
4. **Time-stamp everything.** Earnings analysis is perishable. Always note the reporting date and when the analysis was produced.

---

## Quick Reference: The 4-Layer Summary

```
Layer 1: PARSE      → What happened? (Revenue, margins, EPS, cash, balance sheet, stock context)
Layer 2: COMPARE    → How does it stack up? (QoQ, YoY, vs consensus, vs peers, vs valuation)
          → Run scorer at end of Compare for mechanical verdict
Layer 3: DIAGNOSE   → Why did it happen? Is it repeatable? What shifted? Address every scorer flag.
Layer 4: DECIDE     → So what? What's the action? What would change my mind?
```

The one-page sheet is the minimum viable output for STRONG cases. The full memo is the default for everything else. Always end with a clear view and specific invalidation conditions.
