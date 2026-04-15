---
name: supply-chain-pass-through
description: Map listed-equity beneficiaries of a secular trend across the supply chain, then substantiate each with earnings call evidence (backlog, book-to-bill, guide raises, Q&A admissions, mix shifts). Decomposes multi-mechanism themes into sub-themes, flags cost-bearer nodes, subtracts captive capacity, and classifies each node as value captor, volume taker, optionality, or cost bearer. Use when asked "who benefits from X", "supply chain beneficiaries", "pass-through analysis", "thematic basket", "pick and shovel", "trace this trend", "map the value chain", "which companies are exposed to", or any request starting from a macro driver and asking for downstream equity beneficiaries. Also triggers on "substantiate with earnings calls" or checking whether a company actually captures benefit vs merely transits volume. Pairs with bg-lens for single-name deep dives and earnings-analysis for individual prints.
---

# Supply Chain Pass-Through (v2)

## Purpose

Given a secular trend, produce a mechanically-derived chain of listed beneficiaries and substantiate each link with concrete earnings evidence. The output is a thesis-grade thematic map that a PM can defend in an IC — not a vague "themes we like" list.

The skill's value is as much in what it **refuses to include** as in what it recommends. Naive baskets are always bigger than correct ones; the pass-through analysis is an anti-bullshit filter on thematic investing.

## Core principles

### 1. Two meanings of pass-through

- **Trend pass-through**: how the driver mechanically reaches each layer of the chain.
- **Value pass-through**: whether a company *captures* the benefit or merely *transits* it to customers or input suppliers.

Nodes with high trend pass-through and low value capture are the canonical trap. Flag every node on both axes.

### 2. Single-mechanism gate (new in v2)

A trend must have a single causal mechanism to be analysed as one theme. Bundles of several mechanisms that share a marketing label (e.g. "edge AI", "quantum computing", "metaverse") must be **decomposed into sub-themes** before any chain is built. This is Phase 0 below.

### 3. Default skepticism at the L1 platform/originator layer (new in v2)

Across every test of this skill, the "pick and shovel" layer has beaten the "platform/originator" layer on value capture. Shovels beat platforms. Originators face customer power (governments, payers, hyperscalers), supplier power (CDMOs, foundries, specialty inputs), and IP/patent cliffs that pickers and shovellers don't. Start Phase 4 evidence review at the L2/L3 layer; work back to L1 only after the shovels are mapped.

### 4. End users are cost bearers, not beneficiaries (new in v2)

If a node's cost of goods rises with the trend, it is a **cost bearer**, not a beneficiary, regardless of whether its revenue grows. EV OEMs in a rare-earth thesis, auto OEMs in a chip shortage thesis, PC OEMs in a memory upcycle thesis — these are all cost bearers. Flag and exclude from the basket. Growth ≠ benefit.

## When to use vs adjacent skills

- **This skill**: "Who benefits from X and how do I prove it?" Start from a trend, end with a defended chain.
- **thematic-investment-research**: Top-down theme construction, sizing, and portfolio build. Broader scope.
- **bg-lens**: Single-name deep-dive on a high-conviction beneficiary surfaced by this skill.
- **earnings-analysis**: The latest print for one company. This skill uses transcripts as evidence but doesn't produce a full earnings memo.
- **competitive-analysis**: Used inside this skill for any node where value-capture is uncertain.
- **regime-map**: Use after this skill to stress-test the surviving basket against multiple world states.

---

## Workflow

Work through these phases in order. Each phase is gated — don't advance until the prior one has produced a defensible output. **If Phase 0 fails, do not proceed to a single-basket analysis — decompose and run Phase 1 separately for each sub-theme.**

### Phase 0 — Theme decomposition gate (new in v2)

Before building any chain, answer these three questions:

1. **Does the trend have a single causal mechanism?** (E.g., "NA power demand growth driven by AI datacenter load" = yes. "Edge AI" = no, because it bundles physical AI, server companion chips, consumer PC NPUs, and on-device smartphone AI — four different mechanisms.)
2. **Are the sub-drivers positively correlated or negatively correlated?** Cloud vs edge inference compete for a fixed workload budget and are negatively correlated. If you find negative correlation inside a "theme", it's not a theme.
3. **Do the sub-themes share the same customer base?** If the customers are different (hyperscalers vs auto OEMs vs consumer PC buyers), the "theme" is actually several themes.

If **any** answer is "no" or "multiple", decompose. Produce a sub-theme table that looks like this:

```
Sub-theme      | Mechanism              | Binding constraint | Status
A              | ...                    | ...                | evidence-positive
B              | ...                    | ...                | evidence-mixed
C              | ...                    | ...                | already-falsified
D              | ...                    | ...                | no-listed-pure-play
```

Then run Phase 1 onward separately for each **investable** sub-theme (i.e. drop the falsified and no-pure-play rows from further analysis but keep them in the output so the reader sees why they were excluded).

**Sub-theme status values** (mandatory field):
- **evidence-positive**: Earnings evidence supports the sub-theme; proceed to full analysis.
- **evidence-negative**: Sub-theme is plausible but earnings evidence is absent or weak; watchlist only, do not build basket.
- **evidence-mixed**: Earnings evidence is contradictory; proceed with heavy caveats.
- **already-falsified**: A previously-credible sub-theme has failed (e.g. Copilot+ PCs in 2024–2025). Exclude from basket by default; include only if a new and specific mechanism is identified.
- **no-listed-pure-play**: The sub-theme exists but cannot be expressed in listed equities (e.g. on-device phone GenAI where all beneficiaries are captive OEMs). Exclude from basket.

### Phase 1 — Articulate the trend as a mechanism, not a narrative

For each surviving sub-theme, state it as a **causal mechanism** with a quantifiable driver, not a slogan.

Deliverable for Phase 1:

- **One-sentence driver statement** with magnitude and timeframe.
- **Physical/economic mechanism**: the actual chain of events that must occur.
- **Binding constraint**: where is the bottleneck? That's where pricing power lives. If no binding constraint exists, note it explicitly — this is a weaker thesis setup.
- **Structural event subphase** (new in v2) — mandatory. Check and document recent:
  - M&A (e.g. Novo–Catalent, Dec 2024)
  - Government intervention (e.g. DoW–MP Materials, July 2025)
  - Regulatory shocks (e.g. China heavy rare earth export controls, April 2025)
  - IP cliffs / patent expiries (e.g. semaglutide in Canada/Brazil, 2026)
  - Price floors or ceilings (e.g. MP's $110/kg DoW floor)
  - Captive capacity events (e.g. Novo buying Catalent's fill-finish sites)
  - Competitive exits (e.g. a Western competitor leaving the market)
  - Category rebrands in management commentary (e.g. "edge AI" → "physical AI" across AMBA and LSCC in 2025)
- **Bifurcated / regional pricing check** (new in v2): Does the same product trade at meaningfully different prices in different geographies or channels? If yes, which tier do listed beneficiaries access? This is material — a single-price assumption can silently misstate economics by multiples (see rare earth heavy REEs: Chinese vs Western price premium of 264–276%).
- **Falsifiability test**: what observables would kill this thesis? Specify numerical thresholds, not moods.

Skip to Phase 2 only when the mechanism is specific enough that a sceptic could disagree on facts.

### Phase 2 — Build the physical/economic chain

Map the chain layer-by-layer from driver to end-point. Standard layers:

| Layer | Definition | Typical exposure type |
|---|---|---|
| **L1 — Primary** | Direct provider of the thing the trend demands | Revenue line ~100% exposed |
| **L2 — Pick-and-shovel** | Upstream components/inputs that L1 needs to scale | Segment-level exposure |
| **L3 — Enablers** | Adjacent infrastructure co-required in parallel | Product-line exposure |
| **L4 — Second-order** | Derivative beneficiaries (services, real estate, logistics, specialty labour) | Indirect/operating leverage |

For each layer, write a one-line causal sentence linking it back to Phase 1. If you can't write that sentence cleanly, the layer doesn't belong.

**Chain collapse check (new in v2).** If L1, L2, and L3 names are vertically integrating into each other (e.g. MP Materials mining + separating + magnet-making; the rare earth chain collapses into three integrated pure-plays), treat them as a single integrated layer and concentrate the basket accordingly. Don't split integrated players into multiple buckets.

**Captive capacity subtraction (new in v2).** If a node was on the merchant market but has been bought by a downstream consumer (Catalent → Novo), subtract that capacity from the merchant pool count. The node still exists and still produces, but it is no longer available to other customers. Flag explicitly — naive chain maps silently include captive capacity.

**Cost-bearer flagging (new in v2).** At L4 / end-user, ask: "does the trend make inputs more expensive for this node?" If yes, flag as cost bearer and exclude from the basket, even if the company is growing for other reasons. Examples: EV OEMs in a rare-earth thesis, defense primes in a metals thesis, PC OEMs in a memory upcycle. Growth ≠ benefit.

### Phase 3 — Populate candidates at each layer

For each layer, list 3–8 listed candidates. Prefer pure-plays over diversified names; note % revenue exposure. Use `places_search` / `web_search` / `conversation_search` for unfamiliar subsectors. Screen candidates against three filters:

1. **Liquidity filter**: market cap and ADV large enough to be investable (default $2bn / $20m ADV unless specified).
2. **Pure-play filter**: ≥25% of revenue exposed, OR a discrete reportable segment.
3. **Listing filter**: tradeable on a venue the user can access (flag ADRs and non-US listings).

Cut anything that fails all three. Keep names that fail one but offer unique exposure (flagged).

### Phase 4 — Product-level exposure mapping per candidate

Work **from L2/L3 inward** (default skepticism at L1). For each surviving candidate, decompose revenue to the product/segment level and identify which lines actually touch the trend. Output a small table per name:

```
Company: Eaton (ETN)
Segment                  | % Rev | Trend exposure
Electrical Americas      |  50%  | HIGH — data centre, grid reinforcement
Electrical Global        |  25%  | MEDIUM
Aerospace                |  15%  | NONE
Vehicle                  |   6%  | NONE
eMobility                |   4%  | MEDIUM (2nd order)
                                → Weighted theme exposure: ~55–60%
```

Source from 10-K segment disclosures, investor day materials, and the most recent earnings deck. If you can't source it, say so — don't estimate blind.

**Critical caveat for diversified names (new in v2).** If only part of a company's revenue touches the trend (e.g. Lattice Semiconductor: Industrial & Automotive ~30% is edge AI; Communications & Computing ~64% is datacenter), your basket sizing should reflect only the *exposed* portion. Do not credit the full company to the thesis. Include an explicit "theme-exposed revenue" line.

### Phase 5 — Earnings evidence hunt

For each candidate, pull the last **2–4 earnings calls** and extract concrete evidence of the trend landing. Use `web_search` for transcripts; `web_fetch` for specific pages; Daloopa MCP where available for structured historicals.

**Evidence hierarchy (strongest to weakest):**

1. **Hard order-book data**: backlog $, book-to-bill >1.0, multi-year capacity sold out, pricing increases accepted.
2. **Guidance raises explicitly attributed to the trend** in prepared remarks.
3. **Quantified mix shift** (new v2: promoted weight). This includes:
   - Customer mix shift (e.g. "data centre went from 10% to 25% of orders")
   - **Mix broadening** (e.g. STVN's 40% increase in non-GLP-1 customers ordering premium syringes) — this is the strongest form of mix evidence because it shows capex earns beyond the initial theme.
   - **Category rebrand in management language** (new v2: Tier 3 signal). When multiple companies rebrand a category — e.g. "edge AI" → "physical AI" across AMBA, LSCC, NVDA in 2025 — that is an industry admission that the old narrative failed and the real demand is narrower. Treat as substantive evidence.
4. **Q&A admissions** — often the best signal because unrehearsed. Analysts probe weak points; management responses under pressure are high-information.
5. **Prepared-remarks narrative claims** (weakest — marketing).

Demand at least **two items from tiers 1–4** per company. Prepared-remarks narrative alone is unsubstantiated.

Capture evidence in this format:

```
ETN — Q2 2026 call (Jul 2026)
[T1] Backlog: Electrical Americas backlog +32% YoY, record
[T1] Book-to-bill: 1.15x in Electrical Americas
[T2] Guide: FY26 organic raised 200bps, CFO cited data centre orders
[T4] Q&A (analyst: Nigel Coe, Wolfe): asked about backlog durability;
     CFO said "visibility now extends into 2028 on large projects"
→ Substantiation: STRONG
```

If evidence is thin, stale (>4 months), or missing, say so. Do not fabricate. Note which calls are unavailable and proceed with what you have.

**Competitive share-shift check (new v2).** At the L1 originator/platform layer, explicitly check for **competitive share shift data** — it's often a better signal than either company's own guidance. In GLP-1, the Lilly-vs-Novo 60.5%/39.5% incretin share was the cleanest evidence that Novo was losing despite its own volume growth.

### Phase 6 — Value capture test

For every node with strong trend pass-through, run a one-paragraph value-capture check:

- **Customer power**: concentration of customer base; top-3 concentration above ~40% is a yellow flag.
- **Supplier power**: dependence on constrained upstream inputs.
- **Substitution**: can the customer bypass this node (in-source, redesign)?
- **Pricing evidence**: prices actually rising, or volume at flat margin? Check gross margin trajectory.
- **Competitive structure**: duopoly/oligopoly captures value; fragmented markets dissipate it.

**Contractual vs structural value capture (new in v2).** These are different things and should be graded differently:

- **Contractual value capture**: legally guaranteed by a specific agreement (e.g. MP Materials' DoW Price Protection Agreement, $140m/year minimum EBITDA, 100% offtake). Very strong — survives competitive threats that would break structural moats. Rare.
- **Structural value capture**: derives from oligopoly, switching costs, IP, or regulatory moats (e.g. WST elastomer closures, STVN Nexa syringes, PLTR Maven POR). Strong in equilibrium, vulnerable to structural shocks (IP cliffs, regulatory changes, new entrants).
- **Positional value capture**: temporary advantage from being first-to-market, having spare capacity, or holding inventory. Weakest — erodes quickly.

Grade each captor explicitly on which type.

**Classify each node:**
- **Value captor** (strong trend pass-through + strong value capture) — thesis candidate.
- **Volume taker** (strong trend pass-through + weak value capture) — avoid, or short the narrative.
- **Optionality** (weak current pass-through + strong structural position) — watchlist.
- **Cost bearer** (trend raises input costs for this node) — exclude from basket. (New in v2.)

### Phase 7 — Output: the pass-through memo

Produce a Word document using the `ib-report-formatting` skill, or python-docx directly if you already know the conventions. Structure:

1. **Executive summary** with headline conclusion
2. **Phase 0 decomposition** (if the theme had multiple mechanisms) — show the rejected sub-themes so the reader understands why
3. **Trend mechanism** (Phase 1 output, ½ page)
4. **Structural events subphase** (Phase 1) — explicit list of recent M&A, government intervention, pricing regime changes, category rebrands
5. **Chain map** (Phase 2 table + optional diagram via `alphaear-logic-visualizer`; note chain-collapse and captive-capacity observations)
6. **Candidate universe** (Phase 3 table)
7. **Per-company evidence pages** (Phases 4–6, one page per company): exposure table, evidence extract, value capture verdict incl. type (contractual/structural/positional), cost-bearer flag where applicable
8. **Portfolio-shape summary**: which 5–8 names carry the thesis, how weight reflects the binding constraint, regime framing at the node level
9. **Falsification watchlist**: 3–5 observables from Phase 1 plus company-level red flags. Numerical thresholds, not moods.

Filename convention: `SCPT_<trend-short>_<YYYYMMDD>.docx`

---

## Evidence standards (non-negotiable)

- **Every quantitative claim must be sourced** to a specific call, date, or filing.
- **Distinguish orders from revenue**. Orders/backlog are forward-looking; revenue is already priced in.
- **Watch for language inflation**. "Strong" and "robust" are not evidence. Numbers, backlog statements, and guidance raises are.
- **Flag stale evidence**. If the last relevant earnings call is >4 months old, say so.
- **Flag missing evidence explicitly**. An empty evidence box is more useful than fabricated colour.
- **Flag category rebrands**. When management changes category language (e.g. "edge AI" → "physical AI"), treat as a Tier 3 signal and note which companies have adopted the new language.
- **Use competitive share-shift data** at the L1 layer. It's more informative than either company's own narrative.

## Common failure modes to avoid

1. **Treating a bundle as a theme.** Failing Phase 0 is the most common failure. "Edge AI", "quantum computing", "metaverse", "agentic AI" — decompose before analysing.
2. **Layer inflation.** Adding L4/L5 names to grow the list. If you can't write a one-sentence causal link, drop the node.
3. **Narrative accumulation bias.** Treating three prepared-remarks quotes as stronger than one Q&A admission. It's the reverse.
4. **Ignoring the value-capture leg.** Producing a chain where every node is a "buy". That's almost never true.
5. **Linear best/base/worst scenarios at the chain level.** Each node's modal outcome is driven by its own mechanism. Frame node-level outcomes regime-by-regime.
6. **Over-diversification tax.** Including a name with 5% theme exposure because the parent is well-known. The exposure needs to move the P&L.
7. **Currency/listing blind spot.** European, Australian, Japanese, and Korean beneficiaries are often the cleanest plays but need explicit flagging.
8. **Double-counting diversified names** (new v2). Lattice is ~30% edge AI and ~64% datacenter. Crediting full-company metrics to the edge thesis silently overweights the sleeve. Use theme-exposed revenue only.
9. **Missing captive capacity** (new v2). Catalent still produces, but only for Novo. Subtract from merchant pool.
10. **Failing to flag cost bearers** (new v2). Auto OEMs and defense primes in rare earths are cost bearers, not beneficiaries. Growth ≠ benefit.
11. **Single-price assumption in bifurcated markets** (new v2). Rare earth Western prices are 3–5x Chinese. Assume one global price at your peril.
12. **Mistaking marketing rebrands for growth** (new v2). When "AI PCs" became 55% of forecast shipments but only 5% of actual purchases driven by consumer demand, that's forced adoption via silicon roadmap, not pull.

## Worked mini-examples (calibration)

**Example 1: simple chain with clear binding constraint (rare earth magnets, April 2026)**

- Phase 0: single mechanism ✓ (Chinese export controls + Western reshoring)
- Phase 1 binding constraint: Western heavy rare earth separation capacity
- Phase 1 structural events: DoW–MP deal (July 2025), China export controls (April 2025), Lynas first commercial HRE production (May 2025), Apple $500m partnership (Oct 2025)
- Phase 1 bifurcated pricing: Dy $226/kg China vs $850/kg Europe (+276% premium)
- Phase 2 chain collapse: MP, Lynas, Energy Fuels all integrating L1+L2 — treat as single integrated layer
- Phase 4 cost bearers: Tesla, Ford, GM, defense primes excluded
- Phase 6 contractual captor: MP Materials (DoW $110/kg floor, $140m/year minimum EBITDA) — contractual capture
- Output: 3-name concentrated basket

**Example 2: failed Phase 0, theme decomposition required ("edge AI inference")**

- Phase 0: **FAILS** single-mechanism gate. Decompose:
  - Physical AI (embedded vision) — evidence-positive → run Phase 1+
  - Server companion chips — evidence-positive but datacenter, not edge → flag category mis-label
  - Consumer PC NPUs (Copilot+) — **already-falsified** (2.3% of Q1 2025 shipments) → exclude
  - Phone on-device GenAI — **no-listed-pure-play** (captive to Apple/Samsung) → exclude
- Phase 1 for physical AI: binding constraint is low-power SoC design; category rebrand "edge AI" → "physical AI" across AMBA, LSCC management
- Output: 2-name concentrated basket (AMBA + partial LSCC I&A segment only)

**Example 3: value capture broken at originator ("GLP-1", April 2026)**

- Phase 0: single mechanism ✓
- Phase 1 structural events: Novo–Catalent captivization (Dec 2024); semaglutide patent cliff in Canada/Brazil 2026; MFN pricing deal
- Phase 2 captive capacity: Catalent subtracted from merchant fill-finish pool
- Phase 4 competitive share shift: Lilly 60.5% / Novo 39.5% US incretin share
- Phase 6: Novo flagged as **volume taker** despite highest theme exposure (FY26 guide: -5% to -13% CER sales growth). WST, STVN, Bachem flagged as **structural value captors**.
- Output: shovel-heavy basket with zero weight on highest-exposure originator

---

## The one-liner

**Decompose → mechanism → structural events → chain → product → transcript → value capture (contractual / structural / positional) → memo.** Refuse single baskets for multi-mechanism themes. Exclude cost bearers. Subtract captive capacity. Rank mix-shift evidence above prepared remarks. Default skeptical on L1.
