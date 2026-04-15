# Scoring Engine Reference

Read this file before invoking `scripts/score_earnings.py`. Covers the input schema, the three scoring layers, the expectations elevation and regime classifiers, verdict tiers and routing, the critical-flag override, and the complete flag library.

## Contents
1. Invocation & defaults handling
2. Input schema (beat quality, operational health, management signals)
3. Layer 1 — Beat quality
4. Layer 2 — Operational health
5. Layer 3 — Management signals
6. Expectations elevation classifier
7. Expectations regime classifier
8. Verdict tiers and routing
9. Critical flag override
10. Verdict-driven output routing
11. Flag library (beat quality, operational health, management signals, expectations regime)

---

The scoring engine at `scripts/score_earnings.py` converts parsed earnings data into a composite verdict across three analytical layers. Current version is v1.4.1, validated against nine distinct earnings cases spanning every major verdict tier from STRONG_QUARTER through PROBLEMATIC_QUARTER_WITH_CRITICAL_FLAGS and every defined expectations regime.

### Invocation

The scorer takes command-line arguments that mirror the data points extracted in Steps 1 and 2. Output is JSON. A representative invocation:

```bash
python scripts/score_earnings.py \
  --ticker "XYZ" --quarter "Q4 2025" \
  --revenue-beat-pct 1.5 --eps-beat-pct 3.0 \
  --guidance-change raised --guidance-raise-magnitude modest \
  --gross-margin-change-bps 50 --gross-margin-change-yoy-bps 100 \
  --gross-margin-vs-5y-percentile 60 \
  --core-segment-gm-gap-pp 0 --beat-driver volume \
  --operating-margin-change-qoq-bps 20 --operating-margin-change-yoy-bps 80 \
  --ocf-conversion 1.05 --fcf-conversion 0.85 \
  --dso-change-days 2 --inventory-growth-pct 10 --revenue-growth-pct 12 \
  --gaap-nongaap-op-margin-gap-pp 3 --capex-to-revenue-ratio 8 \
  --management-tone confident --stock-reaction positive \
  --stock-1y-return-pct 25 --stock-return-from-low-pct 60 --stock-drawdown-from-high-pct 10 \
  --red-flags '[]'
```

All inputs have sensible defaults so partial invocation is possible. Missing inputs should be explicitly noted in Step 3 so the reader understands which dimensions of the score are based on assumed values rather than disclosed data.

### Input Schema

**Beat quality inputs.** `revenue-beat-pct` and `eps-beat-pct` are signed percentage surprises versus consensus. `guidance-change` takes one of: `raised`, `raised_narrowed`, `maintained`, `narrowed_lowered`, `lowered`, `withdrawn`, `initiated`, `not_provided`. `guidance-raise-magnitude` (for both raises and cuts) takes `modest`, `meaningful`, or `massive`. `gross-margin-change-bps` is sequential, `gross-margin-change-yoy-bps` is annual. `gross-margin-vs-5y-percentile` is 0–100. `core-segment-gm-gap-pp` is the core segment's GM minus consolidated GM in percentage points. `beat-driver` takes `volume`, `mix`, `pricing`, `one_time_favourable`, `one_time_unfavourable`, `fx`, or `unknown` (legacy `one_time` maps to favourable). `operating-margin-change-qoq-bps` and `operating-margin-change-yoy-bps` capture operating-margin dynamics.

**Operational health inputs.** `ocf-conversion` is OCF/net income (primary cash quality metric). `fcf-conversion` is FCF/net income (secondary, interpreted alongside capex intensity). `dso-change-days` is sequential DSO change. `inventory-growth-pct` is YoY inventory growth, compared to `revenue-growth-pct`. `gaap-nongaap-op-margin-gap-pp` captures SBC/adjustment magnitude. `capex-to-revenue-ratio` (new in v1.4.1) enables growth-capex-mode detection for high-intensity investment cycles.

**Management signals inputs.** `management-tone` takes `bullish`, `confident`, `neutral`, `cautious`, `defensive`, or `evasive`. `stock-reaction` takes `positive`, `flat`, or `negative`. `stock-1y-return-pct`, `stock-return-from-low-pct`, and `stock-drawdown-from-high-pct` feed the expectations elevation classifier. `red-flags` is a JSON array of flag keys drawn from the library documented below — use the exact snake_case keys listed in the Flag Library.

### Layer 1: Beat Quality

Evaluates beat magnitude, guidance direction and magnitude, gross margin and operating margin dynamics, beat-driver persistence, and contradictions such as beat-and-cut. Rewards clean volume-driven beats with raised guidance and positive margin trends. Penalises pricing-driven beats, one-time favourable flatters, guidance cuts, margin compression (sequential or annual), and operating deleverage. Typical range: -8 to +10.

### Layer 2: Operational Health

Evaluates cash conversion, working capital discipline, and the GAAP/non-GAAP gap. OCF/NI is the primary cash quality metric because it excludes capex variability. FCF/NI enters through a growth-capex-mode check that distinguishes genuine FCF weakness from heavy investment cycles. As of v1.4.1, growth capex mode fires when FCF conversion is low AND OCF is healthy AND (revenue growth >15% OR capex-to-revenue ratio >25%). Typical range: -6 to +5.

### Layer 3: Management Signals

Evaluates management tone, governance and reporting red flags, the market reaction, and the interaction between reaction and expectations elevation. This layer also hosts the expectations regime classifier. Typical range: -8 to +3.

### Expectations Elevation Classifier

A 0–9 composite that measures how much optimism is priced into the stock heading into the print. Three independent sub-scores each 0–3:

- **Recent momentum** — trailing 12-month return (0 for <30%, 3 for >150%)
- **Rally maturity** — recovery from 52-week low (0 for <100%, 3 for >400%)
- **Cushion erosion** — drawdown from all-time high (0 for >30%, 3 for <5%)

The total maps to four tiers: **low** (0–2), **medium** (3–4), **high** (5–6), **extreme** (7–9). Elevation matters because it determines how the market's reaction should be interpreted. A beat that would normally be received positively can produce a negative reaction at extreme elevation because the whisper has moved ahead of consensus. Conversely, a miss at low elevation may produce a muted or positive reaction because expectations are already reset.

### Expectations Regime Classifier

Produces a single label summarising the relationship between the current print, forward guidance, market reaction, and expectations elevation. Seven regimes exist at v1.4.1:

| Regime | Pattern | Interpretation |
|--------|---------|----------------|
| **constructive** | Beat + raise + positive reaction | Clean thesis confirmation; asymmetric upside flag fires at low elevation |
| **overrun** | Beat-and-raise with negative reaction, or beat-without-raise at elevated stock | Whisper was ahead of guidance; forward risk/reward has asymmetrically worsened |
| **whisper_overrun** (v1.4.1) | Beat + maintained guidance + negative reaction at low/medium elevation | Narrow-band whisper disappointed on a specific key metric; reaction is real but not thesis-breaking |
| **depressed** | Headline miss with positive reaction | Expectations reset below reported results; leveraged upside regime |
| **balanced** | Beat + flat reaction | Market has neither revised up nor down |
| **deteriorating** | Negative reaction + guidance cut (regardless of current-quarter beat/miss) | Most severe regime; expectations may still be ahead of reality |
| **unknown** | No branch matches | Should not occur in practice at v1.4.1 |

**Branch precedence.** The deteriorating check runs first for any negative reaction combined with a guidance cut, ensuring that beat-and-cut cases (like Novo Nordisk Q4 2025) are classified as deteriorating rather than whisper_overrun.

### Verdict Tiers and Routing

The composite score is the sum of the three layer scores. Five base tiers:

| Tier | Score Range | Meaning |
|------|-------------|---------|
| **STRONG_QUARTER** | ≥ 9 | Clean beat with quality confirming; thesis-confirming |
| **SOLID_QUARTER** | 4 to 8 | Decent quarter, no major red flags; thesis maintained |
| **MIXED_QUARTER** | 0 to 3 | Mixed signals; further diagnosis required |
| **WEAK_QUARTER** | -4 to -1 | Below expectations or quality concerns present |
| **PROBLEMATIC_QUARTER** | ≤ -5 | Material miss and/or serious red flags; thesis may be impaired |

Three suffix modifiers can attach:

- **_AT_PEAK** — attaches to STRONG or SOLID when the peak cycle risk flag fired. Results are strong but mean reversion risk is elevated.
- **_EXPECTATIONS_OVERRUN** — attaches to STRONG or SOLID when the overrun regime is detected. Fundamentals are strong but market has priced in execution; the question shifts from direction to position sizing.
- **_WITH_CRITICAL_FLAGS** — attaches to any base tier when critical flags fire. STRONG, SOLID, and MIXED cases are downgraded to MIXED_QUARTER_WITH_CRITICAL_FLAGS. WEAK and PROBLEMATIC retain their base label with the suffix appended.

### Critical Flag Override

Eight flag keys are classified as critical and trigger the WITH_CRITICAL_FLAGS suffix regardless of the base composite score: **CFO_DEPARTURE**, **AUDITOR_CHANGE**, **RESTATEMENT**, **BEAT_AND_CUT**, **DESTRUCTIVE_BUYBACK**, **LOW_OCF**, **GAAP_NONGAAP_GAP_EXTREME**, and **REGULATORY_ENFORCEMENT**.

Critical flags apply as a downgrade modifier while the underlying composite score is preserved in the verdict detail text, so the reader sees both the mechanical score and the specific concern that caused the downgrade. When the base verdict is already PROBLEMATIC_QUARTER, the verdict detail reads "confirmed by" rather than "downgraded due to" because the critical flag is reinforcing rather than overriding the base classification.

### Verdict-Driven Output Routing

The scorer emits an `output_recommendation` that maps the verdict tier to deliverable types. This routing takes precedence over any default deliverable selection — produce what the scorer recommends unless the user explicitly requests something else.

| Verdict Tier | Output Recommendation |
|-------------|----------------------|
| STRONG_QUARTER | One-page earnings sheet |
| STRONG_QUARTER_AT_PEAK | Full memo + risk map (peak cycle focus) |
| STRONG_QUARTER_EXPECTATIONS_OVERRUN | Full memo (position sizing focus) |
| SOLID_QUARTER | Full memo |
| SOLID_QUARTER_AT_PEAK | Full memo + risk map (peak cycle focus) |
| SOLID_QUARTER_EXPECTATIONS_OVERRUN | Full memo (position sizing focus) |
| MIXED_QUARTER | Full memo |
| MIXED_QUARTER_WITH_CRITICAL_FLAGS | Full memo + risk map (critical flag investigation) |
| WEAK_QUARTER | Full memo + risk map |
| WEAK_QUARTER_WITH_CRITICAL_FLAGS | Full memo + risk map (critical flag investigation) |
| PROBLEMATIC_QUARTER | Full memo + risk map |
| PROBLEMATIC_QUARTER_WITH_CRITICAL_FLAGS | Full memo + risk map (critical flag investigation) |

The trade note is produced on user request in addition to any of the above.

---

## Flag Library Reference

The scoring engine maintains a structured library of flags that fire when specific conditions are detected. Each flag carries a score impact (which can be zero for narrative-only flags), a narrative text, and in some cases a classification as a critical flag. The Score column shows the direct impact on the layer score — flags marked "narrative" have zero score impact but appear in the output to inform the diagnosis.

Critical flags are marked with an asterisk.

### Beat Quality Layer

| Flag Name | Input Condition | Score | Purpose |
|-----------|----------------|-------|---------|
| EXTREME_BEAT | Revenue beat >15% or EPS beat >20% | narrative | Model-breaking magnitude — investigate sustainability vs peak cycle |
| GUIDANCE_MASSIVE_RAISE | Guide raised >15% above consensus | narrative | Expect broad analyst revisions; watch for peak cycle reversal |
| CORE_SEGMENT_PREMIUM | Core segment GM gap >8pp above consolidated | +1 | Headline margin understates core business quality |
| CORE_SEGMENT_HIGHER | Core segment GM gap 3–8pp above consolidated | narrative | Modest positive context for margin reading |
| CORE_SEGMENT_DRAG | Core segment GM gap <-5pp | -1 | Core business worse than headline suggests |
| QOQ_MARGIN_NOISE | QoQ GM decline suppressed by YoY positive or core premium | 0 or -1 | Mix-quarter noise, not structural compression |
| GROSS_MARGIN_COMPRESSION | QoQ GM decline >200bps with YoY trend also weak | -2 | Structural margin erosion |
| MARGIN_PRESSURE | QoQ GM decline 100–200bps not offset by YoY | -1 | Margin pressure without annual offset |
| YOY_MARGIN_DETERIORATION | YoY GM decline 200–400bps | -1 | Annual margin trend turned negative; verify structural vs transitory |
| YOY_MARGIN_DETERIORATION_SEVERE | YoY GM decline >400bps | -2 | Severe structural margin compression |
| OPM_DETERIORATION | YoY OPM decline 250–500bps | -1 | Annual operating leverage turning negative |
| OPM_DETERIORATION_SEVERE | YoY OPM decline >500bps | -2 | Structural operating deleverage; critical for high-GM businesses |
| OPM_GM_DIVERGENCE | OPM compressing QoQ (<-100bps) while GM stable (>-50bps) | -1 | Issue is below the gross margin line |
| PEAK_CYCLE_RISK | GM at 90th+ percentile of 5-year history | narrative | Mean reversion risk; triggers _AT_PEAK suffix |
| ONE_TIME_FAVOURABLE_BEAT | `beat-driver = one_time_favourable` | -3 | Current period flattered by non-recurring positive |
| ONE_TIME_UNFAVOURABLE | `beat-driver = one_time_unfavourable` | +1 | Current period depressed by non-recurring negative |
| PRICING_DRIVEN_BEAT | `beat-driver = pricing` with large surprise | narrative | Pricing beats have shorter half-lives than volume beats |
| BEAT_AND_CUT* | Revenue beat paired with guidance cut | -2 | Classic pull-forward signal; critical flag |
| EPS_QUALITY | EPS beat without revenue beat | narrative | Check tax rate, below-the-line items, buybacks |
| GUIDANCE_WITHDRAWN | `guidance-change = withdrawn` | -4 | Major uncertainty signal |

### Operational Health Layer

| Flag Name | Input Condition | Score | Purpose |
|-----------|----------------|-------|---------|
| LOW_OCF* | OCF/NI below 0.40 | -3 | Serious earnings quality concern; critical flag |
| OCF_QUALITY | OCF/NI 0.40 to 0.60 | -1 | Earnings quality concern |
| GROWTH_CAPEX_MODE | Low FCF + healthy OCF + (rev growth >15% OR capex/rev >25%) | narrative | Capex funding growth/infrastructure; not a quality concern |
| FCF_WEAKNESS | FCF/NI <0.5 without growth or capex offset | -1 | Cash conversion issue without clear explanation |
| DSO_SPIKE | DSO increased >10 days QoQ | -2 | Revenue recognition or collections risk |
| DSO_RISING | DSO increased 5–10 days QoQ | -1 | Monitor collections |
| INVENTORY_BUILD | Inventory growing >15pp faster than revenue | -2 | Demand risk, potential write-down |
| INVENTORY_WATCH | Inventory growing 5–15pp faster than revenue | -1 | Monitor inventory vs demand |
| GAAP_NONGAAP_GAP | Operating margin gap 15–25pp | -1 | Notable SBC/adjustment magnitude |
| GAAP_NONGAAP_GAP_EXTREME* | Operating margin gap >25pp | -2 | Investigate whether excluded items are truly one-time; critical flag |

### Management Signals Layer

Red flag keys in the table below are passed to the scorer via the `--red-flags` argument as a JSON array of snake_case strings. Example: `--red-flags '["cfo_departure","doj_investigation"]'`. Expectations regime flags are emitted automatically based on the stock reaction and guidance change inputs — you do not pass them in explicitly.

**Governance & quality red flags (pass via --red-flags):**

| Input Key | Output Flag | Score | Category |
|-----------|------------|-------|----------|
| `cfo_departure` | CFO_DEPARTURE* | -3 | Governance |
| `auditor_change` | AUDITOR_CHANGE* | -3 | Governance |
| `restatement` | RESTATEMENT* | -4 | Governance |
| `new_non_gaap_adjustments` | NEW_NON_GAAP | -2 | Quality |
| `guidance_metric_dropped` | METRIC_DROPPED | -2 | Quality |
| `guidance_cut_with_beat` | BEAT_AND_CUT | -2 | Quality (also auto-fires from beat/guidance combo) |
| `buyback_with_debt_and_declining_roic` | DESTRUCTIVE_BUYBACK* | -2 | Capital allocation |
| `insider_selling_spike` | INSIDER_SELLING | -1 | Insider behaviour |
| `segment_restructuring` | SEGMENT_CHANGE | -1 | Reporting |
| `deferred_revenue_decline` | DEFERRED_REV_DECLINE | -1 | Forward demand |

**Regulatory overhang red flags (pass via --red-flags):**

| Input Key | Output Flag | Score | Category |
|-----------|------------|-------|----------|
| `doj_investigation` | DOJ_INVESTIGATION | -2 | Regulatory overhang |
| `sec_investigation` | SEC_INVESTIGATION | -2 | Regulatory overhang |
| `antitrust_review` | ANTITRUST_REVIEW | -2 | Regulatory overhang |
| `regulatory_enforcement_action` | REGULATORY_ENFORCEMENT* | -3 | Regulatory overhang |
| `doj_settlement_risk` | DOJ_SETTLEMENT_RISK | -1 | Regulatory overhang |
| `executive_departure_senior` | EXECUTIVE_DEPARTURE | -2 | Leadership transition |

**Expectations regime flags (auto-fired, not passed in):**

| Output Flag | Condition | Score |
|------------|-----------|-------|
| EXPECTATIONS_BAR_RISING | Negative reaction to beat-and-raise | -1 |
| HOT_STOCK_MODEST_BEAT | Negative reaction to beat at elevated stock | -1 |
| WHISPER_OVERRUN | Negative reaction to beat at low/medium elevation without raise | -1 |
| EXPECTATIONS_BAR_LOW | Positive reaction to headline miss | +1 |
| ASYMMETRIC_UPSIDE | Beat-and-raise at low elevation with positive reaction | +1 |
| DETERIORATING_REGIME | Negative reaction paired with guidance cut | narrative |
| ELEVATION_EXTREME | Overrun pattern at extreme elevation (additional penalty) | -1 |

**Custom flags.** Any `red-flags` key not in the standard library will be passed through as `CUSTOM_FLAG: <key>` with no score impact, for cases where you need to note something outside the standard taxonomy.

---
