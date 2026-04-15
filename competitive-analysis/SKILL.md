---
name: competitive-analysis
description: Comprehensive framework for analyzing company competitiveness across 11 dimensions (market position, moat, Porter's Five Forces, value chain, strategy, innovation, operations, financials, vulnerabilities, forward indicators, geopolitical supply chain resilience). Use when asked to assess competitive positioning, evaluate competitive advantages, analyze industry dynamics, compare companies competitively, assess moat sustainability, build investment theses based on competitive strength, evaluate supply chain resilience, assess geopolitical risk exposure, analyze friend-shoring/nearshoring advantage, or evaluate domestic supply chain as competitive moat. Produces institutional-quality analysis with visual infographic summary and detailed section-by-section assessment.
---

# Competitive Analysis Framework

## Overview

This skill provides a systematic 11-section framework for analyzing company competitiveness, producing institutional-quality investment research. The framework incorporates geopolitical supply chain resilience as a distinct competitive dimension, reflecting the 2026 environment where domestic/friend-shored supply chains represent meaningful competitive advantages. The output consists of a one-page visual infographic summary followed by detailed analytical sections.

## Workflow

### Step 1: Information Gathering

Collect necessary information about the company and industry:
- Company name, ticker symbol, and business description
- Recent financial filings (10-K, 10-Q, investor presentations)
- Industry reports and competitive landscape data
- Customer/supplier relationships and dependencies
- Management commentary and strategic initiatives

If the user provides specific documents or filings, prioritize those. Otherwise, use web_search to gather current information.

### Step 2: Create the One-Page Infographic Summary

**CRITICAL: Create the infographic FIRST before the detailed analysis sections.**

The infographic provides a visual at-a-glance summary of all 11 competitive dimensions using a PowerPoint slide. Create using the pptx skill with this structure:

**Layout:**
- **Header**: Company name, ticker, date, "Competitive Position Analysis"
- **Central visual**: Competitive strength radar chart or scorecard showing ratings (1-10) for each of the 11 dimensions
- **Key metrics panel**: 4-5 most critical metrics (market share, ROIC, moat rating, supply chain resilience score, competitive score)
- **Color coding**: Green (strong), yellow (neutral), red (weak)
- **Bottom summary**: Overall competitiveness score (1-10) and one-sentence investment implication

**Visual elements to include:**
- Radar/spider chart showing 11-dimension scores
- Small icon or indicator for moat rating (None/Narrow/Wide)
- Traffic light indicators for key risk areas
- Supply chain geographic exposure mini-map or flag indicators
- Mini chart showing market share trend or margin trajectory
- Compact competitive positioning matrix (if applicable)

**Design principles:**
- Professional, clean layout suitable for investment presentations
- High information density but uncluttered
- Instantly communicates competitive strength/weakness
- Use institutional color scheme (blues, grays, accent colors)

After creating the infographic, present it to the user FIRST, then proceed with detailed sections.

### Step 3: Conduct 11-Section Competitive Analysis

Perform comprehensive analysis across all 11 dimensions. For each section, provide:
- Current assessment with quantitative metrics where available
- Trend analysis (improving/stable/deteriorating)
- Peer benchmarking
- Key strengths and vulnerabilities
- Investment implications

The 11 sections are detailed in the references file. Load `references/analysis_framework.md` for complete methodology.

### Step 4: Generate Executive Summary & Investment Implications

After completing all sections, synthesize findings into:
- **Competitiveness Score**: 1-10 overall rating with justification
- **Moat Rating**: None/Narrow/Wide with durability assessment (5/10/15+ years)
- **Top 3 Competitive Advantages**: Ranked by strength and sustainability
- **Top 3 Vulnerabilities**: Ranked by severity and probability
- **Investment Implications**:
  - Valuation multiple support (justify premium/discount)
  - Growth sustainability assessment
  - Downside risk scenarios
  - Recommended action (buy/hold/sell with price target context)

### Step 5: Format & Present Output

**Output structure:**
1. **Page 1**: One-page infographic summary (PowerPoint slide)
2. **Pages 2+**: Detailed analysis document (Word document or markdown)
   - Executive Summary (1 page)
   - Section 1: Market Structure & Positioning
   - Section 2: Competitive Moat Assessment
   - Section 3: Porter's Five Forces
   - Section 4: Value Chain & Cost Position
   - Section 5: Strategic Positioning
   - Section 6: Innovation & Adaptability
   - Section 7: Operational Competitiveness
   - Section 8: Financial Competitiveness
   - Section 9: Vulnerability Analysis
   - Section 10: Forward-Looking Indicators
   - Section 11: Geopolitical Supply Chain Resilience
   - Appendices (data tables, peer comparisons, geographic exposure maps)

Use professional formatting consistent with investment research reports.

## Key Analysis Principles

**Objectivity**: Present balanced view with both strengths and weaknesses. Avoid confirmation bias.

**Quantification**: Use specific metrics and peer benchmarks wherever possible. Avoid vague qualitative statements.

**Forward-looking**: Focus on sustainability and trajectory, not just current state. Consider disruption risks.

**Investment lens**: Always tie competitive analysis to investment implications (valuation, growth, risk).

**Evidence-based**: Ground assessments in concrete data points from filings, industry reports, and observable metrics.

**Geopolitical awareness**: In sustained high-geopolitical-risk environments (2026+), treat supply chain geographic positioning as a first-order competitive factor. Domestic/friend-shored supply chains may justify valuation premiums; concentrated exposure to high-risk geographies should be treated as material risk.

## Common Triggers

Use this skill when users ask to:
- "Analyze [Company]'s competitive position"
- "Assess [Company]'s competitive advantages"
- "What is [Company]'s moat?"
- "Compare [Company A] vs [Company B] competitively"
- "Evaluate [Industry] competitive dynamics"
- "Is [Company]'s competitive position sustainable?"
- "Build investment thesis based on competitive strength"
- "Assess [Company]'s supply chain resilience"
- "Evaluate geopolitical risk exposure for [Company]"
- "Does [Company] have a friend-shoring/nearshoring advantage?"
- "How exposed is [Company] to China/Taiwan supply chain risk?"
- "Is domestic supply chain a competitive advantage for [Company]?"
- "Compare supply chain security of [Company A] vs [Company B]"
- "What is [Company]'s reshoring strategy?"

## References

Detailed analytical methodologies for each of the 11 sections are available in:
- `references/analysis_framework.md` - Complete framework with metrics, questions, peer benchmarking guidance, and geopolitical supply chain resilience assessment methodology
