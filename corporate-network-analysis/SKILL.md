---
name: corporate-network-analysis
description: Systematic framework for analyzing corporate networks to generate investment alpha. Use when analyzing supplier-customer relationships, director interlocks, executive networks, insider holdings patterns, or identifying M&A signals through board connections. Triggers on supply chain analysis, customer momentum, board interlock, director network, connected party analysis, relationship mapping, or network-based investment research.
---

# Corporate Network Analysis

Exploit slow information diffusion through supply chain relationships and director interlocks to identify predictable stock returns. Academic research shows customer momentum yields ~150bps monthly alpha; board centrality generates ~4.68% annual risk-adjusted returns.

## Core Investment Theses

1. **Supply Chain Momentum**: When a customer gets a big order, upstream suppliers benefit with a lag (40% of shock diffuses over subsequent months)
2. **Director Interlock Signals**: Shared board members facilitate information flow, M&A activity, and strategic alignment
3. **Cross-Holding Synergies**: Executives/directors with positions in multiple companies may orchestrate beneficial strategic moves

## Workflow

### Phase 1: Identify Target Company Networks

```
1. Map supplier-customer relationships (>5% revenue materiality)
2. Identify board members and their other directorships
3. Track executive cross-company positions
4. Document insider holdings across connected firms
```

### Phase 2: Data Collection

Use free data sources in this priority order:

| Relationship Type | Primary Source | How to Access |
|-------------------|----------------|---------------|
| Suppliers/Customers | SEC 10-K Item 1/7 | EDGAR full-text search |
| Board Members | DEF 14A Proxy | EDGAR company filings |
| Insider Transactions | Form 3/4/5 | EDGAR insider filings |
| Beneficial Ownership | Schedule 13D/13G | EDGAR ownership filings |
| Institutional Holdings | Form 13F | EDGAR quarterly filings |

See `references/sec-data-guide.md` for detailed extraction procedures.

### Phase 3: Network Construction

Build network graphs connecting companies through:
- Customer-supplier links (weighted by revenue %)
- Shared directors (first-degree: direct; second-degree: shared third board)
- Executive overlaps
- Cross-insider holdings

Calculate centrality metrics:
- **Degree**: Number of direct connections
- **Betweenness**: Importance in information flow paths
- **Closeness**: Speed of information propagation

See `references/network-metrics.md` for calculation methods.

### Phase 4: Signal Generation

**Customer Momentum Signal**:
```
1. Calculate weighted 12-month returns of major customers
2. Rank universe by customer momentum
3. Long top quintile, short bottom quintile
4. Optimal: 4th-layer relationships (less crowded)
```

**Board Connection Signals**:
- New shared director between firms → potential M&A signal
- Director clustered buying across positions → information signal
- High centrality + adverse event → watch for network contagion

See `references/signal-generation.md` for detailed procedures.

### Phase 5: Due Diligence Checklist

Before acting on network signals, verify:
- [ ] Relationship confirmed via multiple sources
- [ ] Revenue materiality >5%
- [ ] Network position shows high centrality
- [ ] Relationship stable (duration >2 years)
- [ ] Information asymmetry present (limited analyst coverage)
- [ ] Sufficient liquidity for execution
- [ ] No MNPI exposure risk

### Phase 6: Compliance Review

**Permissible**:
- All public SEC filings (10-K, DEF 14A, Form 4, 13D, 13F)
- Public earnings calls and press releases
- Mosaic theory: combining immaterial public info

**Prohibited**:
- Material non-public information from any source
- Shadow trading: using MNPI about Company A to trade Company B

See `references/compliance-guide.md` for legal boundaries.

## Output Templates

When completing analysis, produce:

1. **Network Map**: Visual or tabular representation of company relationships
2. **Signal Summary**: Ranked opportunities with confidence scores
3. **Due Diligence Notes**: Verification status for each relationship
4. **Risk Factors**: Data quality issues, concentration risks, compliance flags

## Key Academic References

- Cohen & Frazzini (2008): Customer-supplier momentum, 1.37-1.55% monthly alpha
- Ali & Hirshleifer (2020): Shared analyst coverage unifies spillover effects
- Larcker, So & Wang (2013): Board centrality predicts returns
- Cai & Sevilir (2012): Board connections in M&A transactions

See `references/academic-papers.md` for full bibliography.

## Data Quality Considerations

- SEC disclosures only capture >10% revenue customers
- Companies may strategically withhold customer names
- Board data has survivorship bias (failed firms disappear)
- Post-publication alpha decay affects well-known signals
- Multi-source verification essential for high-confidence signals
