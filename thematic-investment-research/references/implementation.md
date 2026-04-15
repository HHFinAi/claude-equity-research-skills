# Implementation Reference

## Position Sizing Framework

### Conviction-Based Sizing Matrix

| Conviction Level | Base Size | Criteria | Max Size |
|------------------|-----------|----------|----------|
| **High** | 4-5% | Deep dive complete; multiple valuation support; clear catalysts; strong thesis | 6% |
| **Medium** | 2-3% | Fundamental work complete; some uncertainty on timing/execution | 4% |
| **Speculative** | 1-1.5% | High potential but significant risks; option-like payoff; early stage | 2% |
| **Watch List** | 0% | Interesting but valuation or thesis not yet compelling | 0% |

### Risk-Adjusted Sizing Formula

```
Adjusted Size = Base Size × Volatility Adj × Liquidity Adj × Correlation Adj × Conviction Adj
```

**Adjustment Factors:**

| Factor | Condition | Adjustment |
|--------|-----------|------------|
| **Volatility** | Beta >1.5 | 0.75x |
| | Beta 1.0-1.5 | 1.0x |
| | Beta <1.0 | 1.1x |
| **Liquidity** | ADV <$10M | 0.5x |
| | ADV $10-50M | 0.75x |
| | ADV >$50M | 1.0x |
| **Correlation** | High correlation to existing | 0.75x |
| | Low correlation | 1.0x |
| **Conviction** | Near thesis killer | 0.5x |
| | Crowding elevated | 0.75x |

### Portfolio Construction Rules

| Rule | Limit | Rationale |
|------|-------|-----------|
| Single Position | ≤6% | Diversification |
| Theme Total | ≤25% | Theme concentration |
| Pure-Play Total | ≤15% | Pure-play risk |
| Illiquid (<$20M ADV) | ≤10% | Liquidity risk |
| Top 3 Positions | ≤15% | Position concentration |

### Position Count Guidelines

| Portfolio Size | Thematic Positions | Per-Position Target |
|----------------|-------------------|---------------------|
| <$100M | 8-12 | 2-4% avg |
| $100M-500M | 12-18 | 2-3% avg |
| >$500M | 15-25 | 1.5-2.5% avg |

## Entry Execution Framework

### Entry Timing Considerations

| Factor | Assessment | Implication |
|--------|------------|-------------|
| **Catalyst Proximity** | Near-term catalyst? | Accelerate if positive catalyst approaching |
| **Valuation** | Discount to target? | Larger initial position if cheap |
| **Technical** | Support/resistance? | Consider technical levels for entry |
| **Sentiment** | Crowded/unloved? | Larger if unloved; smaller if crowded |
| **Market Regime** | Risk-on/off? | More aggressive in risk-on |
| **Liquidity** | Normal conditions? | Avoid thin markets, earnings |

### Staged Entry Protocol

**Rationale**: Manages timing risk; allows thesis validation; averages entry price

| Stage | Size | Trigger | Purpose |
|-------|------|---------|---------|
| **Initial** | 40-50% | Thesis validated; basic work complete | Establish core exposure |
| **Second** | 30-40% | Positive confirmation; catalyst progress | Build on conviction |
| **Final** | 10-30% | Clear catalyst; technical setup | Complete position |

**Confirmation Signals for Second Stage:**
- Earnings beat with positive guidance
- Key product/customer win
- Favorable regulatory development
- Peer group re-rating
- Technical breakout

**Trigger Events for Final Stage:**
- Major catalyst 1-2 months away
- Valuation at/below entry target
- Technical support holds
- Sentiment reset after pullback

### Entry Decision Tree

```
1. Is thesis validated?
   No → Stay on watch list
   Yes → Proceed to Step 2

2. Is current price attractive?
   >10% above target → Wait
   Within 10% of target → Consider entry
   Below target → Proceed to Step 3

3. Are near-term catalysts positive or negative?
   Negative catalyst imminent → Wait for resolution
   Neutral/Positive → Proceed to Step 4

4. Is market environment favorable?
   Severe risk-off → Reduce size or wait
   Normal/Risk-on → Proceed to Step 5

5. Execute entry based on conviction level and sizing rules
```

## Monitoring Framework

### Theme-Level Monitoring

| Indicator Category | Metrics | Frequency | Source |
|-------------------|---------|-----------|--------|
| **Adoption** | Penetration rate, unit volumes | Monthly/Quarterly | Industry data |
| **Economics** | Pricing trends, cost curves | Quarterly | Company disclosures |
| **Competition** | New entrants, M&A, share shifts | Ongoing | News, filings |
| **Policy** | Legislation, regulatory actions | Ongoing | Government sources |
| **Sentiment** | ETF flows, coverage count | Monthly | Fund data, research |

### Company-Level Monitoring

| Category | Metrics | Timing |
|----------|---------|--------|
| **Earnings** | Revenue, margins, guidance | Quarterly |
| **Operational KPIs** | Theme-specific metrics | Quarterly+ |
| **Strategic** | M&A, partnerships, pivots | Ongoing |
| **Competitive** | Win/loss, share data | Quarterly |
| **Valuation** | Multiple vs. peers, implied growth | Weekly |
| **Technical** | Price levels, momentum | Daily/Weekly |

### Monitoring Dashboard Template

| Metric | Current | Prior | Trend | Alert | Action |
|--------|---------|-------|-------|-------|--------|
| **Theme KPIs** | | | | | |
| Adoption rate | | | | | |
| Cost per unit | | | | | |
| Policy support | | | | | |
| **Company KPIs** | | | | | |
| Revenue growth | | | | | |
| Margin trend | | | | | |
| Market share | | | | | |
| **Valuation** | | | | | |
| EV/Revenue | | | | | |
| vs. peer median | | | | | |
| vs. history | | | | | |

### Alert Thresholds

| Indicator | Yellow Alert | Red Alert | Action |
|-----------|-------------|-----------|--------|
| Theme adoption | -10% vs. plan | -25% vs. plan | Review thesis |
| Company revenue | Miss guidance | Miss 2 consecutive | Consider trim |
| Market share | -200bps YoY | -500bps YoY | Reassess position |
| Valuation | >75th percentile | >90th percentile | Consider trim |
| Thesis killer | Approaching | Breached | Exit per protocol |

## Rebalancing Framework

### Rebalancing Triggers

| Trigger Type | Condition | Action |
|--------------|-----------|--------|
| **Position Drift** | >1.5x target weight | Trim to target |
| | <0.5x target weight | Evaluate adding |
| **Conviction Change** | Upgraded | Increase to new target |
| | Downgraded | Reduce to new target |
| **Relative Value** | Better opportunity | Rotate capital |
| **Risk Limits** | Limit breached | Reduce to compliance |
| **Time-Based** | Quarterly | Review all positions |

### Rebalancing Decision Matrix

| Position Performance | Thesis Status | Action |
|---------------------|---------------|--------|
| Outperformed, overweight | Unchanged | Trim to target |
| Outperformed, overweight | Strengthened | Allow modest overweight |
| Underperformed, underweight | Unchanged | Add to target |
| Underperformed, underweight | Weakened | Reassess; may exit |

## Exit Criteria Framework

### Exit Decision Types

| Exit Type | Definition | Typical Action |
|-----------|------------|----------------|
| **Target Achieved** | Price reaches target; thesis reflected | Trim 50-100% |
| **Thesis Broken** | Fundamental assumption invalidated | Exit 100% |
| **Better Opportunity** | Superior risk/reward available | Rotate |
| **Theme Maturation** | Theme becomes consensus | Systematic reduction |
| **Risk Management** | Position/portfolio limits | Trim to compliance |
| **Stop Loss** | Price-based trigger | Per pre-defined rules |

### Exit Decision Tree

```
1. Has thesis killer been triggered?
   Yes → Exit 100% immediately
   No → Proceed to Step 2

2. Has price target been achieved?
   Yes → Trim 50-75%; reassess target
   No → Proceed to Step 3

3. Has conviction changed?
   Downgraded → Reduce position
   Unchanged → Proceed to Step 4
   Upgraded → Consider adding

4. Is better opportunity available?
   Yes → Consider rotation
   No → Proceed to Step 5

5. Are risk limits breached?
   Yes → Trim to compliance
   No → Hold position; continue monitoring
```

### Stop Loss Framework

| Stop Type | Methodology | Application |
|-----------|-------------|-------------|
| **Absolute** | Fixed % below entry | Speculative positions |
| **Trailing** | % below highest price | Momentum captures |
| **Fundamental** | Thesis killer trigger | All positions |
| **Time-Based** | No progress by date | Catalyst-dependent |

**Stop Loss Guidelines:**

| Position Type | Stop Type | Level |
|---------------|-----------|-------|
| High Conviction | Fundamental only | Thesis killer |
| Medium Conviction | Fundamental + Absolute | 25-30% |
| Speculative | All types | 15-20% |

## Review Cadence

### Position Review (Post-Earnings + Monthly)

**Checklist:**
- [ ] Results vs. expectations
- [ ] Guidance changes
- [ ] Thesis progression/regression
- [ ] Valuation update
- [ ] Position size appropriate
- [ ] Alerts triggered

### Theme Review (Quarterly)

**Checklist:**
- [ ] Theme adoption metrics
- [ ] Competitive dynamics changes
- [ ] Regulatory developments
- [ ] TAM estimate revisions
- [ ] Hype cycle progression
- [ ] Crowding indicators

### Universe Refresh (Semi-Annual)

**Checklist:**
- [ ] New screening run
- [ ] IPO/listing additions
- [ ] Removal candidates
- [ ] Exposure category updates
- [ ] Peer group revisions

### Full Research Update (Annual)

**Checklist:**
- [ ] Complete thesis revalidation
- [ ] Updated market sizing
- [ ] Refreshed financial models
- [ ] New valuation targets
- [ ] Risk reassessment
- [ ] Report publication

## Performance Attribution

### Attribution Framework

| Level | Metrics | Frequency |
|-------|---------|-----------|
| **Theme** | Theme return vs. benchmark | Quarterly |
| **Selection** | Stock selection within theme | Quarterly |
| **Sizing** | Contribution from position sizing | Quarterly |
| **Timing** | Entry/exit timing impact | Semi-annual |

### Performance Review Template

| Period | Theme Return | Benchmark | Alpha | Attribution |
|--------|-------------|-----------|-------|-------------|
| MTD | | | | |
| QTD | | | | |
| YTD | | | | |
| Since Inception | | | | |

**Attribution Breakdown:**

| Source | Contribution | Commentary |
|--------|-------------|------------|
| Theme exposure | | |
| Stock selection | | |
| Position sizing | | |
| Timing | | |
| **Total Alpha** | | |
