# Valuation Methods Reference

## Valuation Philosophy for Thematic Investing

### Core Principles

1. **Multi-methodology**: No single approach captures all value dimensions
2. **Scenario-weighted**: Incorporate probability distributions, not point estimates
3. **Theme-specific metrics**: Use KPIs relevant to specific value drivers
4. **Margin of safety**: Demand upside even in base case for forecast uncertainty

### Methodology Selection Matrix

| Company Profile | Primary Method | Secondary Methods |
|----------------|----------------|-------------------|
| Profitable, stable growth | DCF | EV/EBITDA, P/E |
| High-growth, profitable | DCF, PEG | EV/Revenue growth-adjusted |
| High-growth, unprofitable | EV/Revenue | LTV/CAC, Rule of 40 |
| Pipeline-driven (biotech) | rNPV | Sum-of-parts |
| Conglomerate with theme segment | Sum-of-parts | SOTP + theme premium |
| Asset-heavy | EV/EBITDA, NAV | Replacement cost |
| Subscription/SaaS | LTV/CAC, EV/ARR | Rule of 40 |

## DCF Valuation Framework

### Revenue Projection Methodology

**Step 1: TAM Linkage**
- Start with theme-level TAM from structural analysis
- Define SAM based on company's addressable portion
- Project market share trajectory

**Step 2: Segment-by-Segment Build**

| Segment | TAM ($) | SAM ($) | Share % | Revenue ($) |
|---------|---------|---------|---------|-------------|
| Core Theme | | | | |
| Adjacent | | | | |
| Legacy | | | | |
| **Total** | | | | |

**Step 3: Growth Rate Validation**

| Check | Your Estimate | Benchmark |
|-------|---------------|-----------|
| Implied TAM penetration | | <30% Y5 reasonable |
| vs. Historical CAGR | | Within 2x historical |
| vs. Consensus | | Document variance |
| vs. Guidance | | Explain delta |

### Margin Evolution Framework

**Gross Margin Drivers**

| Driver | Current | Target | Bridge |
|--------|---------|--------|--------|
| Product mix | | | |
| Scale efficiencies | | | |
| Input costs | | | |
| Pricing | | | |
| **Gross Margin** | | | |

**Operating Margin Path**

| Metric | Current | Y+3 | Y+5 | Mature | Driver |
|--------|---------|-----|-----|--------|--------|
| Gross Margin | | | | | |
| R&D % | | | | | Scale leverage |
| S&M % | | | | | Channel maturity |
| G&A % | | | | | Fixed cost leverage |
| **Operating Margin** | | | | | |

**Margin Benchmarks by Stage**

| Stage | Gross Margin | Op Margin | FCF Margin |
|-------|-------------|-----------|------------|
| Early Growth | 40-60% | Negative | Negative |
| Scaling | 50-70% | 0-15% | 0-10% |
| Mature Growth | 60-80% | 15-25% | 10-20% |
| Dominant | 70%+ | 25%+ | 20%+ |

### WACC Construction

**Cost of Equity**

```
Cost of Equity = Risk-Free Rate + Beta × Equity Risk Premium + Size Premium + Company Premium
```

| Component | Value | Source |
|-----------|-------|--------|
| Risk-Free Rate | | 10Y Treasury |
| Equity Risk Premium | | 4.5-6.0% typical |
| Beta | | 2Y weekly vs. S&P 500 |
| Size Premium | | Duff & Phelps |
| Company Premium | | Execution/theme risk |
| **Cost of Equity** | | |

**Beta Considerations for Thematic Companies**

| Issue | Solution |
|-------|----------|
| Historical beta may be stale | Use implied beta from peers |
| Theme not yet reflected | Adjust toward theme peer median |
| High volatility | Consider fundamental beta |
| Low trading volume | Use industry beta |

**WACC Calculation**

| Component | Weight | Cost | Contribution |
|-----------|--------|------|--------------|
| Equity | | | |
| Debt | | | |
| **WACC** | 100% | | |

### Terminal Value Approaches

**Perpetuity Growth Method**

```
Terminal Value = FCF(n+1) / (WACC - g)
```

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Terminal FCF | | Normalized |
| Terminal Growth | | 2-3% typical |
| Implied TV/EBITDA | | Cross-check |

**Exit Multiple Method**

```
Terminal Value = EBITDA(n) × Exit Multiple
```

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Terminal EBITDA | | |
| Exit Multiple | | Mature peer median |
| Implied Perpetual Growth | | Cross-check |

**Terminal Value Checks**

| Check | Value | Acceptable Range |
|-------|-------|------------------|
| TV as % of Enterprise Value | | <70% preferred |
| Implied TV/EBITDA | | 6-12x typical |
| Implied Perpetual Growth | | 1-3% |
| TV/Revenue | | Industry benchmark |

### DCF Output Template

| Scenario | Revenue Y5 | EBITDA Y5 | FCF Y5 | WACC | TV | PV(TV) | PV(FCF) | EV | Per Share |
|----------|-----------|-----------|--------|------|----|----|----|----|-----------|
| Bull | | | | | | | | | |
| Base | | | | | | | | | |
| Bear | | | | | | | | | |

**Probability-Weighted Value**

| Scenario | Probability | Value | Contribution |
|----------|-------------|-------|--------------|
| Bull | 25% | | |
| Base | 55% | | |
| Bear | 20% | | |
| **Expected Value** | 100% | | |

## Relative Valuation Framework

### Peer Selection Principles

1. **Thematic Peers**: Similar theme exposure regardless of sector
2. **Business Model Peers**: Similar operating models
3. **Growth Stage Peers**: Companies at similar maturity
4. **Traditional Peers**: GICS-based for reality check

### Comparable Analysis Template

| Company | EV/Rev | EV/EBITDA | P/E | EV/FCF | Rev Gr | Margin |
|---------|--------|-----------|-----|--------|--------|--------|
| Peer 1 | | | | | | |
| Peer 2 | | | | | | |
| Peer 3 | | | | | | |
| Peer 4 | | | | | | |
| Peer 5 | | | | | | |
| **Median** | | | | | | |
| **Mean** | | | | | | |
| **Target** | | | | | | |
| Premium/(Discount) | | | | | | |

### Multiple Adjustments

**Growth-Adjusted Multiples**

| Metric | Formula | Use Case |
|--------|---------|----------|
| PEG | P/E ÷ EPS Growth | Growth comparisons |
| EV/EBITDA/Growth | Multiple ÷ EBITDA Growth | Operating comparisons |
| Rule of 40 | Revenue Growth + FCF Margin | SaaS evaluation |

**Quality Adjustments**

| Factor | Premium | Discount |
|--------|---------|----------|
| Market Leadership | +10-20% | |
| Recurring Revenue | +10-15% | |
| Margin Superiority | +5-15% | |
| Leverage | | -5-15% |
| Customer Concentration | | -5-10% |
| Governance Concerns | | -5-15% |

## Reverse DCF Analysis

### Methodology

**Purpose**: Determine what growth/margins are implied by current price

**Process**:
1. Start with current share price
2. Assume reasonable WACC and terminal growth
3. Assume target margin profile
4. Solve for implied revenue CAGR

### Reverse DCF Template

| Assumption | Value |
|------------|-------|
| Current Share Price | |
| Shares Outstanding | |
| Net Debt | |
| **Implied Enterprise Value** | |
| | |
| Assumed WACC | |
| Assumed Terminal Growth | |
| Assumed Terminal Margin | |
| | |
| **Implied Revenue CAGR** | |
| Consensus Revenue CAGR | |
| **Gap** | |

### Interpretation Guide

| Implied vs. Your Estimate | Interpretation |
|---------------------------|----------------|
| Implied << Your Est | Undervalued (bullish) |
| Implied ≈ Your Est | Fairly valued |
| Implied >> Your Est | Overvalued (bearish) |

## Sum-of-Parts Valuation

### When to Use
- Diversified companies with separable theme exposure
- Conglomerates with distinct business units
- Companies with valuable minority stakes

### SOTP Template

| Segment | Metric | Multiple | Value | % of Total |
|---------|--------|----------|-------|------------|
| Theme Segment | EBITDA | 15x | | |
| Legacy Segment | EBITDA | 8x | | |
| Investment Stake | | | | |
| Corporate Costs | | | | |
| Net Debt | | | | |
| **Total Equity Value** | | | | |
| Per Share | | | | |

### Conglomerate Discount Considerations

| Factor | Discount | Rationale |
|--------|----------|-----------|
| Management distraction | 5-10% | Suboptimal focus |
| Capital misallocation | 5-15% | Cross-subsidization |
| Transparency | 5-10% | Segment opacity |
| No discount | 0% | Synergies justify |

## Valuation Integration

### Target Price Construction

**Step 1: Gather Methodologies**

| Method | Value | Weight | Contribution |
|--------|-------|--------|--------------|
| DCF (Prob-Weighted) | | 40% | |
| Comparable Analysis | | 30% | |
| Sum-of-Parts | | 20% | |
| Precedent Transactions | | 10% | |
| **Blended Target** | | 100% | |

**Step 2: Establish Ranges**

| Scenario | Low | Base | High |
|----------|-----|------|------|
| DCF | | | |
| Comps | | | |
| SOTP | | | |
| **Range** | | | |

**Step 3: Set Price Target**

| Conviction Level | Target Setting |
|------------------|----------------|
| High | Base case value |
| Medium | Conservative of range |
| Low | Lower quartile |

### Sensitivity Analysis

**Two-Variable Sensitivity (WACC vs. Terminal Growth)**

|  | g=1% | g=2% | g=3% |
|--|------|------|------|
| WACC=8% | | | |
| WACC=9% | | | |
| WACC=10% | | | |
| WACC=11% | | | |

**Scenario Sensitivity**

| Variable | -20% | Base | +20% | Value Impact |
|----------|------|------|------|--------------|
| Revenue Growth | | | | |
| Terminal Margin | | | | |
| Multiple | | | | |
