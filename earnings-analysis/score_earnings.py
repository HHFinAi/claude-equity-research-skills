#!/usr/bin/env python3
"""
Earnings Quality Scorer v1.4.1 — validates parsed earnings data and flags risks.

v1.4.1 refinements:
1. Whisper overrun regime branch: handles the "beat-maintain-negative reaction"
   pattern where a headline beat at low or medium stock elevation draws a
   negative reaction because narrow-band whisper expectations on a specific
   key metric were not met. Previously fell through to "unknown" regime.
2. Growth capex mode threshold adjustment: adds optional capex-to-revenue
   ratio input and lowers revenue growth threshold from 20% to 15%. Companies
   with high capex intensity (>25% of revenue) are now classified as
   GROWTH_CAPEX_MODE regardless of revenue growth rate, capturing cases
   like Microsoft's $37.5B quarterly capex on 17% revenue growth.

v1.4 refinements (retained):
1. Year-over-year gross margin deterioration check: flags structural margin
   compression visible on an annual basis even when QoQ is not severe enough
   to trigger the existing margin pressure flag.
2. Regulatory overhang red flag category: adds doj_investigation,
   sec_investigation, antitrust_review, regulatory_enforcement_action, and
   doj_settlement_risk as distinct red flag keys with appropriate penalties.
3. Operating margin input: adds explicit operating margin change inputs
   (QoQ and YoY) to capture earnings quality dynamics in high-gross-margin
   businesses (pharma, software) where the real action is at the OPM level.
4. One-time beat direction split: separates one_time_favourable (beat
   flattered by non-recurring positive) from one_time_unfavourable (current
   period depressed by non-recurring negative). Retains legacy 'one_time'
   mapping to one_time_favourable for backward compatibility.

Cosmetic fix: PROBLEMATIC_QUARTER now correctly receives the
WITH_CRITICAL_FLAGS suffix when critical flags are present, resolving the
minor labelling inconsistency identified during the Novo Nordisk test.

v1.3.1 changes (retained):
- Base verdict computed from composite score without critical flag gating
- Critical flag downgrade modifier with preserved base verdict context

v1.3 changes (retained):
- Core segment GM gap input
- Multi-period stock context with expectations elevation classifier

v1.2 changes (retained):
- YoY trend suppression on QoQ margin noise
- Stock reaction overlay with expectations regime classifier
- GAAP/non-GAAP operating margin gap detection

v1.1 changes (retained):
- OCF/NI primary cash metric, FCF/NI secondary
- Guidance raise magnitude buckets
- Peak cycle risk flag
- Beat driver persistence scoring
- Extreme beat magnitude flag
"""

import argparse
import json
from typing import Dict, List, Any


# ---------------------------------------------------------------------------
# Stock Context Classifier
# ---------------------------------------------------------------------------

def classify_expectations_elevation(
    stock_1y_return_pct: float,
    stock_return_from_low_pct: float,
    stock_drawdown_from_high_pct: float
) -> Dict[str, Any]:
    """Classify market expectations elevation based on stock history."""
    recent_momentum = 0
    if stock_1y_return_pct > 150:
        recent_momentum = 3
    elif stock_1y_return_pct > 75:
        recent_momentum = 2
    elif stock_1y_return_pct > 30:
        recent_momentum = 1

    rally_maturity = 0
    if stock_return_from_low_pct > 400:
        rally_maturity = 3
    elif stock_return_from_low_pct > 200:
        rally_maturity = 2
    elif stock_return_from_low_pct > 100:
        rally_maturity = 1

    cushion_erosion = 0
    if stock_drawdown_from_high_pct < 5:
        cushion_erosion = 3
    elif stock_drawdown_from_high_pct < 15:
        cushion_erosion = 2
    elif stock_drawdown_from_high_pct < 30:
        cushion_erosion = 1

    total = recent_momentum + rally_maturity + cushion_erosion

    if total >= 7:
        elevation = "extreme"
        narrative = (
            "Expectations extreme: stock has rallied hard recently, is mature "
            "in its multi-period move, and sits near all-time highs. Any "
            "disappointment relative to the whisper will draw outsized punishment."
        )
    elif total >= 5:
        elevation = "high"
        narrative = (
            "Expectations elevated: market has priced in meaningful success. "
            "Beating consensus is no longer sufficient — the bar is now the "
            "whisper or better."
        )
    elif total >= 3:
        elevation = "medium"
        narrative = (
            "Expectations balanced: market is neither overly optimistic nor "
            "pessimistic. Straightforward beat/miss dynamics apply."
        )
    else:
        elevation = "low"
        narrative = (
            "Expectations depressed: the stock carries limited pricing of "
            "good outcomes. Positive surprises will have leveraged upside."
        )

    return {
        "elevation": elevation,
        "total_score": total,
        "narrative": narrative,
        "breakdown": {
            "recent_momentum": recent_momentum,
            "rally_maturity": rally_maturity,
            "cushion_erosion": cushion_erosion
        }
    }


# ---------------------------------------------------------------------------
# Layer 1: Beat Quality (v1.4 with OPM input, YoY margin check, beat driver split)
# ---------------------------------------------------------------------------

def score_beat_quality(
    revenue_beat_pct: float,
    eps_beat_pct: float,
    guidance_change: str,
    guidance_raise_magnitude: str,
    gross_margin_change_bps: float,
    gross_margin_change_yoy_bps: float,
    gross_margin_vs_5y_percentile: float,
    core_segment_gm_gap_pp: float,
    beat_driver: str,
    operating_margin_change_qoq_bps: float,
    operating_margin_change_yoy_bps: float
) -> Dict[str, Any]:
    """Score beat quality with v1.4 operating margin, YoY margin, and beat
    driver refinements."""
    score = 0
    flags = []

    # ---- Revenue beat ----
    if revenue_beat_pct > 10:
        score += 4
    elif revenue_beat_pct > 3:
        score += 3
    elif revenue_beat_pct > 1:
        score += 2
    elif revenue_beat_pct > 0:
        score += 1
    elif revenue_beat_pct > -1:
        score += 0
    elif revenue_beat_pct > -3:
        score -= 1
    else:
        score -= 2

    # ---- EPS beat ----
    if eps_beat_pct > 15:
        score += 4
    elif eps_beat_pct > 5:
        score += 3
    elif eps_beat_pct > 2:
        score += 2
    elif eps_beat_pct > 0:
        score += 1
    elif eps_beat_pct > -2:
        score += 0
    else:
        score -= 2

    # ---- Extreme beat magnitude flag ----
    if revenue_beat_pct > 15 or eps_beat_pct > 20:
        flags.append(
            f"EXTREME_BEAT: Revenue beat {revenue_beat_pct:.0f}% / EPS beat "
            f"{eps_beat_pct:.0f}% — model-breaking magnitude. Investigate "
            "whether this is sustainable outperformance or peak-cycle pricing."
        )

    # ---- Guidance scoring ----
    if guidance_change == "raised":
        magnitude_scores = {"modest": 2, "meaningful": 4, "massive": 6}
        score += magnitude_scores.get(guidance_raise_magnitude, 2)
        if guidance_raise_magnitude == "massive":
            flags.append(
                "GUIDANCE_MASSIVE_RAISE: Guide >15% above consensus — "
                "expect broad analyst revisions; also consider whether this "
                "marks a cycle peak where the next revision will be downward."
            )
    elif guidance_change == "raised_narrowed":
        score += 2
    elif guidance_change == "maintained":
        score += 0
    elif guidance_change == "narrowed_lowered":
        score -= 2
    elif guidance_change == "lowered":
        cut_scores = {"modest": -2, "meaningful": -4, "massive": -6}
        score += cut_scores.get(guidance_raise_magnitude, -3)
    elif guidance_change == "withdrawn":
        score -= 4
        flags.append("GUIDANCE_WITHDRAWN: Guidance withdrawn — major uncertainty signal")
    elif guidance_change == "initiated":
        score += 1

    # ---- Core segment GM gap ----
    core_segment_premium = False
    if core_segment_gm_gap_pp > 8:
        score += 1
        core_segment_premium = True
        flags.append(
            f"CORE_SEGMENT_PREMIUM: Core segment GM runs {core_segment_gm_gap_pp:.0f}pp "
            "above consolidated. Headline margin materially understates the "
            "quality of the underlying business."
        )
    elif core_segment_gm_gap_pp > 3:
        flags.append(
            f"CORE_SEGMENT_HIGHER: Core segment GM {core_segment_gm_gap_pp:.0f}pp "
            "above consolidated. Modest positive context for margin reading."
        )
    elif core_segment_gm_gap_pp < -5:
        score -= 1
        flags.append(
            f"CORE_SEGMENT_DRAG: Core segment GM runs {abs(core_segment_gm_gap_pp):.0f}pp "
            "BELOW consolidated. The core business is worse than the headline suggests."
        )

    # ---- QoQ gross margin with YoY suppression + core segment awareness ----
    if gross_margin_change_bps < -200:
        if gross_margin_change_yoy_bps > 0 or core_segment_premium:
            flags.append(
                f"QOQ_MARGIN_NOISE: {gross_margin_change_bps:.0f}bps QoQ GM "
                f"decline but YoY trend is +{gross_margin_change_yoy_bps:.0f}bps"
                + (" and core segment running at premium" if core_segment_premium else "")
                + " — likely mix-quarter noise, not structural compression."
            )
            score -= 1 if not core_segment_premium else 0
        else:
            score -= 2
            flags.append(
                f"GROSS_MARGIN_COMPRESSION: {gross_margin_change_bps:.0f}bps QoQ "
                f"decline WITH YoY trend also weak ({gross_margin_change_yoy_bps:+.0f}bps) — "
                "structural margin erosion concern"
            )
    elif gross_margin_change_bps < -100:
        if gross_margin_change_yoy_bps > 50 or core_segment_premium:
            flags.append(
                f"QOQ_MARGIN_NOISE: {gross_margin_change_bps:.0f}bps QoQ GM "
                f"dip suppressed — YoY trend positive or core segment at premium."
            )
        else:
            score -= 1
            flags.append(
                "MARGIN_PRESSURE: 100-200bps QoQ gross margin decline "
                "not offset by YoY improvement"
            )

    # ---- v1.4: Year-over-year gross margin deterioration check ----
    # Catches structural margin compression visible on an annual basis.
    # Particularly important for businesses where QoQ is noisy but the
    # annual trend has clearly turned.
    if gross_margin_change_yoy_bps < -400:
        score -= 2
        flags.append(
            f"YOY_MARGIN_DETERIORATION_SEVERE: Gross margin down "
            f"{gross_margin_change_yoy_bps:.0f}bps year-over-year. Structural "
            "margin compression on annual basis — investigate input cost, "
            "mix shift, competitive pricing, or regulatory pricing pressure."
        )
    elif gross_margin_change_yoy_bps < -200:
        score -= 1
        flags.append(
            f"YOY_MARGIN_DETERIORATION: Gross margin down "
            f"{gross_margin_change_yoy_bps:.0f}bps year-over-year. Annual "
            "margin trend has turned negative — verify whether drivers "
            "are structural or transitory."
        )

    # ---- v1.4: Operating margin check ----
    # Critical for high-gross-margin businesses (pharma, software, luxury)
    # where the real earnings quality story is at the OPM level, not GM.
    # OPM compression without GM compression signals operating deleverage,
    # pricing pressure below the gross margin line, or opex ramp.
    opm_divergence = (
        operating_margin_change_qoq_bps < -100
        and gross_margin_change_bps > -50
    )

    if operating_margin_change_yoy_bps < -500:
        score -= 2
        flags.append(
            f"OPM_DETERIORATION_SEVERE: Operating margin down "
            f"{operating_margin_change_yoy_bps:.0f}bps year-over-year. "
            "Structural operating deleverage — for high-GM businesses, "
            "this is often where the real story lives."
        )
    elif operating_margin_change_yoy_bps < -250:
        score -= 1
        flags.append(
            f"OPM_DETERIORATION: Operating margin down "
            f"{operating_margin_change_yoy_bps:.0f}bps year-over-year. "
            "Annual operating leverage turning negative."
        )

    if opm_divergence:
        score -= 1
        flags.append(
            f"OPM_GM_DIVERGENCE: OPM compressing "
            f"({operating_margin_change_qoq_bps:.0f}bps QoQ) while GM is "
            "stable or improving. Issue is below the gross margin line — "
            "investigate opex growth, pricing on fixed-cost leverage, or "
            "below-the-line items."
        )

    # ---- Peak cycle risk ----
    if gross_margin_vs_5y_percentile >= 90:
        flags.append(
            f"PEAK_CYCLE_RISK: Gross margin at {gross_margin_vs_5y_percentile:.0f}th "
            "percentile of 5-year history. Reversion risk elevated."
        )

    # ---- v1.4: Beat driver with split for one-time direction ----
    driver_adjustments = {
        "volume": 1,
        "mix": 0,
        "pricing": -1,
        "one_time_favourable": -3,
        "one_time_unfavourable": 1,
        # Legacy compatibility: treat bare 'one_time' as 'favourable'
        "one_time": -3,
        "fx": -1,
        "unknown": 0
    }
    score += driver_adjustments.get(beat_driver, 0)

    if beat_driver == "pricing" and (revenue_beat_pct > 5 or gross_margin_change_bps > 500):
        flags.append(
            "PRICING_DRIVEN_BEAT: Beat is overwhelmingly pricing-driven. "
            "In cyclical industries, pricing beats have shorter half-lives "
            "than volume beats."
        )
    if beat_driver in ("one_time_favourable", "one_time"):
        flags.append(
            "ONE_TIME_FAVOURABLE_BEAT: Current period flattered by "
            "non-recurring positive item — do not extrapolate into forward "
            "estimates. Underlying trajectory is worse than headline."
        )
    if beat_driver == "one_time_unfavourable":
        flags.append(
            "ONE_TIME_UNFAVOURABLE: Current period depressed by non-recurring "
            "negative item. Headline understates underlying earnings power; "
            "normalised results would be materially stronger."
        )

    # ---- Contradiction checks ----
    if revenue_beat_pct > 0 and guidance_change in ("lowered", "narrowed_lowered", "withdrawn"):
        score -= 2
        flags.append("BEAT_AND_CUT: Revenue beat with guidance cut — classic pull-forward signal")

    if eps_beat_pct > 2 and revenue_beat_pct <= 0:
        flags.append(
            "EPS_QUALITY: EPS beat without revenue beat — check tax rate, "
            "below-the-line items, and buyback contribution"
        )

    return {"beat_quality_score": score, "flags": flags, "core_segment_premium": core_segment_premium}


# ---------------------------------------------------------------------------
# Layer 2: Operational Health
# ---------------------------------------------------------------------------

def score_operational_health(
    ocf_conversion: float,
    fcf_conversion: float,
    dso_change_days: float,
    inventory_growth_pct: float,
    revenue_growth_pct: float,
    gaap_nongaap_op_margin_gap_pp: float,
    capex_to_revenue_ratio: float = 0
) -> Dict[str, Any]:
    score = 0
    flags = []

    if ocf_conversion > 1.1:
        score += 3
    elif ocf_conversion > 0.9:
        score += 2
    elif ocf_conversion > 0.75:
        score += 1
    elif ocf_conversion > 0.6:
        score += 0
    elif ocf_conversion > 0.4:
        score -= 1
        flags.append(f"OCF_QUALITY: OCF/NI at {ocf_conversion:.2f} — earnings quality concern")
    else:
        score -= 3
        flags.append(f"LOW_OCF: OCF/NI below 0.40 ({ocf_conversion:.2f}) — serious earnings quality concern")

    if fcf_conversion < 0.5 and ocf_conversion > 0.75:
        # v1.4.1: Lowered revenue growth threshold to 15% and added
        # capex-intensity check to correctly classify companies with
        # large absolute capex programmes as growth capex mode rather
        # than as FCF weakness concerns.
        sustained_growth = revenue_growth_pct > 15
        high_capex_intensity = capex_to_revenue_ratio > 25
        if sustained_growth or high_capex_intensity:
            driver = []
            if sustained_growth:
                driver.append(f"revenue growing {revenue_growth_pct:.0f}%")
            if high_capex_intensity:
                driver.append(f"capex at {capex_to_revenue_ratio:.0f}% of revenue")
            driver_text = " and ".join(driver)
            flags.append(
                f"GROWTH_CAPEX_MODE: FCF conversion low ({fcf_conversion:.2f}) "
                f"but OCF healthy ({ocf_conversion:.2f}) with {driver_text} — "
                "capex funding growth or infrastructure build-out"
            )
        else:
            score -= 1
            flags.append(
                f"FCF_WEAKNESS: FCF/NI at {fcf_conversion:.2f} without "
                "offsetting revenue growth or capex-intensive investment cycle"
            )

    if dso_change_days > 10:
        score -= 2
        flags.append("DSO_SPIKE: DSO increased >10 days QoQ — revenue recognition or collections risk")
    elif dso_change_days > 5:
        score -= 1
        flags.append("DSO_RISING: DSO increased 5-10 days QoQ — monitor collections")
    elif dso_change_days < -5:
        score += 1

    inv_rev_spread = inventory_growth_pct - revenue_growth_pct
    if inv_rev_spread > 15:
        score -= 2
        flags.append(f"INVENTORY_BUILD: Inventory growing {inv_rev_spread:.0f}pp faster than revenue")
    elif inv_rev_spread > 5:
        score -= 1
        flags.append(f"INVENTORY_WATCH: Inventory growing {inv_rev_spread:.0f}pp faster than revenue")
    elif inv_rev_spread < -10:
        score += 1

    if gaap_nongaap_op_margin_gap_pp > 25:
        score -= 2
        flags.append(
            f"GAAP_NONGAAP_GAP_EXTREME: Operating margin gap of "
            f"{gaap_nongaap_op_margin_gap_pp:.0f}pp. Investigate whether "
            "excluded items are truly one-time."
        )
    elif gaap_nongaap_op_margin_gap_pp > 15:
        score -= 1
        flags.append(
            f"GAAP_NONGAAP_GAP: Operating margin gap of "
            f"{gaap_nongaap_op_margin_gap_pp:.0f}pp. Notable but not extreme."
        )

    return {"operational_health_score": score, "flags": flags}


# ---------------------------------------------------------------------------
# Layer 3: Management Signals + Stock Reaction (v1.4 with regulatory flags)
# ---------------------------------------------------------------------------

def score_management_signals(
    management_tone: str,
    red_flags: List[str],
    stock_reaction: str,
    revenue_beat_pct: float,
    eps_beat_pct: float,
    guidance_change: str,
    expectations_elevation: str
) -> Dict[str, Any]:
    score = 0
    flags = []
    expectations_regime = "unknown"

    tone_scores = {
        "bullish": 2, "confident": 1, "neutral": 0,
        "cautious": -1, "defensive": -2, "evasive": -3
    }
    score += tone_scores.get(management_tone, 0)

    # v1.4: Expanded red flag library with regulatory overhang category
    red_flag_penalties = {
        "cfo_departure": (-3, "CFO_DEPARTURE: CFO leaving — governance red flag"),
        "auditor_change": (-3, "AUDITOR_CHANGE: Auditor change — governance concern"),
        "new_non_gaap_adjustments": (-2, "NEW_NON_GAAP: New non-GAAP adjustments — potential earnings management"),
        "guidance_metric_dropped": (-2, "METRIC_DROPPED: Previously guided metric no longer guided"),
        "guidance_cut_with_beat": (-2, "BEAT_AND_CUT: Beat current quarter but cut forward"),
        "restatement": (-4, "RESTATEMENT: Financial restatement — material accounting issue"),
        "buyback_with_debt_and_declining_roic": (-2, "DESTRUCTIVE_BUYBACK: Debt-funded buybacks with declining ROIC"),
        "insider_selling_spike": (-1, "INSIDER_SELLING: Elevated insider selling around earnings"),
        "segment_restructuring": (-1, "SEGMENT_CHANGE: Segment restructuring may obscure trends"),
        "deferred_revenue_decline": (-1, "DEFERRED_REV_DECLINE: Deferred revenue declining — forward demand weakening"),
        # v1.4 additions: regulatory overhang category
        "doj_investigation": (-2, "DOJ_INVESTIGATION: Active DOJ investigation — forward risk from exogenous legal outcomes can produce surprises independent of operating execution"),
        "sec_investigation": (-2, "SEC_INVESTIGATION: Active SEC investigation — accounting or disclosure review risk"),
        "antitrust_review": (-2, "ANTITRUST_REVIEW: Active antitrust review — structural remedy risk"),
        "regulatory_enforcement_action": (-3, "REGULATORY_ENFORCEMENT: Active regulatory enforcement action — specific penalties or structural remedies possible"),
        "doj_settlement_risk": (-1, "DOJ_SETTLEMENT_RISK: Settlement discussions or consent decree risk disclosed"),
        "executive_departure_senior": (-2, "EXECUTIVE_DEPARTURE: Senior executive (non-CFO) departure — leadership transition risk")
    }

    for flag_key in red_flags:
        if flag_key in red_flag_penalties:
            penalty, message = red_flag_penalties[flag_key]
            score += penalty
            flags.append(message)
        else:
            flags.append(f"CUSTOM_FLAG: {flag_key}")

    # Expectations regime classification (unchanged from v1.3)
    headline_beat = (revenue_beat_pct > 0 and eps_beat_pct > 0)
    headline_miss = (revenue_beat_pct < 0 or eps_beat_pct < 0)
    raised = (guidance_change in ("raised", "raised_narrowed"))
    lowered = (guidance_change in ("lowered", "narrowed_lowered", "withdrawn"))
    elevated = expectations_elevation in ("high", "extreme")

    # v1.4.1: Deteriorating regime is checked FIRST for any negative reaction
    # paired with a guidance cut, because the cut is the dominant forward
    # signal regardless of whether the current quarter's headline was a beat
    # or miss. This ensures beat-and-cut cases (like Novo Nordisk) are
    # classified correctly rather than falling into whisper_overrun.
    if stock_reaction == "negative" and lowered:
        expectations_regime = "deteriorating"
        flags.append(
            "DETERIORATING_REGIME: Miss/cut + negative reaction. Expectations "
            "may still be ahead of reality — further downside risk if the "
            "next print doesn't beat the reset."
        )

    elif stock_reaction == "negative" and headline_beat:
        if raised:
            flags.append(
                "EXPECTATIONS_BAR_RISING: Stock reacted negatively to a "
                "beat-and-raise quarter. Forward risk/reward has asymmetrically worsened."
            )
            expectations_regime = "overrun"
            score -= 1
            if expectations_elevation == "extreme":
                score -= 1
                flags.append(
                    "ELEVATION_EXTREME: Stock history shows extreme expectations "
                    "elevation. The negative reaction is not a buy-the-dip opportunity."
                )
        elif elevated:
            flags.append(
                f"HOT_STOCK_MODEST_BEAT: Stock at {expectations_elevation} "
                "expectations elevation reacted negatively to a beat."
            )
            expectations_regime = "overrun"
            score -= 1
        else:
            # Negative reaction to a beat at low or medium stock elevation
            # with maintained guidance. Narrow-band whisper expectations on
            # a specific key metric were elevated even though the broader
            # multi-period stock setup was not.
            flags.append(
                "WHISPER_OVERRUN: Headline beat consensus but disappointed "
                "narrow-band whisper expectations on a specific key metric. "
                "Forward risk/reward has shifted modestly negative but the "
                "broader setup remains intact — not a thesis-breaking reaction."
            )
            expectations_regime = "whisper_overrun"
            score -= 1

    elif stock_reaction == "positive" and headline_miss:
        flags.append(
            "EXPECTATIONS_BAR_LOW: Stock rallied despite headline miss — "
            "expectations had been reset lower than reported results."
        )
        expectations_regime = "depressed"
        score += 1

    elif stock_reaction == "positive" and headline_beat and raised:
        expectations_regime = "constructive"
        if expectations_elevation == "low":
            flags.append(
                "ASYMMETRIC_UPSIDE: Beat-and-raise into depressed expectations. "
                "Positive surprises have leveraged upside from this regime."
            )
            score += 1

    elif stock_reaction == "flat" and headline_beat:
        expectations_regime = "balanced"

    return {
        "management_signal_score": score,
        "expectations_regime": expectations_regime,
        "flags": flags
    }


# ---------------------------------------------------------------------------
# Composite Verdict (v1.4 with PROBLEMATIC_QUARTER critical flag fix)
# ---------------------------------------------------------------------------

def compute_composite(beat_result, ops_result, mgmt_result, elevation_result):
    """Compute final verdict with v1.4 critical flag labelling fix."""
    total = (
        beat_result["beat_quality_score"]
        + ops_result["operational_health_score"]
        + mgmt_result["management_signal_score"]
    )

    all_flags = beat_result["flags"] + ops_result["flags"] + mgmt_result["flags"]

    critical_flags = [f for f in all_flags if any(
        k in f for k in [
            "CFO_DEPARTURE", "AUDITOR_CHANGE", "RESTATEMENT",
            "BEAT_AND_CUT", "DESTRUCTIVE_BUYBACK", "LOW_OCF",
            "GAAP_NONGAAP_GAP_EXTREME", "REGULATORY_ENFORCEMENT"
        ]
    )]

    peak_cycle = any("PEAK_CYCLE_RISK" in f for f in all_flags)
    expectations_overrun = mgmt_result.get("expectations_regime") == "overrun"

    # Compute base verdict from score alone
    if total >= 9:
        base_verdict = "STRONG_QUARTER"
        base_detail = "Clean beat with quality indicators confirming. Thesis-confirming quarter."
    elif total >= 4:
        base_verdict = "SOLID_QUARTER"
        base_detail = "Decent quarter with no major red flags. Thesis maintained."
    elif total >= 0:
        base_verdict = "MIXED_QUARTER"
        base_detail = "Mixed signals. Further diagnosis needed."
    elif total >= -4:
        base_verdict = "WEAK_QUARTER"
        base_detail = "Below expectations or quality concerns present."
    else:
        base_verdict = "PROBLEMATIC_QUARTER"
        base_detail = "Material miss and/or serious red flags. Thesis may be impaired."

    verdict = base_verdict
    verdict_detail = base_detail

    # v1.4: Critical flag handling with PROBLEMATIC_QUARTER fix
    if len(critical_flags) > 0:
        downgrade_map = {
            "STRONG_QUARTER": "MIXED_QUARTER_WITH_CRITICAL_FLAGS",
            "SOLID_QUARTER": "MIXED_QUARTER_WITH_CRITICAL_FLAGS",
            "MIXED_QUARTER": "MIXED_QUARTER_WITH_CRITICAL_FLAGS",
            "WEAK_QUARTER": "WEAK_QUARTER_WITH_CRITICAL_FLAGS",
            "PROBLEMATIC_QUARTER": "PROBLEMATIC_QUARTER_WITH_CRITICAL_FLAGS"
        }
        verdict = downgrade_map.get(base_verdict, base_verdict)

        flag_summary = "; ".join([f.split(":")[0] for f in critical_flags])

        if base_verdict == "PROBLEMATIC_QUARTER":
            verdict_detail = (
                f"Composite score of {total} (base: PROBLEMATIC_QUARTER) "
                f"confirmed by {len(critical_flags)} critical flag(s): {flag_summary}. "
                "Multiple independent signals point to a materially impaired quarter."
            )
        else:
            verdict_detail = (
                f"Composite score of {total} (base: {base_verdict}) downgraded "
                f"due to {len(critical_flags)} critical flag(s): {flag_summary}. "
                "Governance/quality issues must be resolved before the base "
                "verdict is meaningful."
            )

        if peak_cycle:
            verdict_detail += " Additional context: peak cycle risk also triggered."
        if expectations_overrun:
            verdict_detail += (
                f" Additional context: expectations overrun at "
                f"{elevation_result['elevation']} elevation."
            )

    else:
        if peak_cycle and verdict in ("STRONG_QUARTER", "SOLID_QUARTER"):
            verdict = verdict + "_AT_PEAK"
            verdict_detail += (
                " NOTE: Peak cycle risk flag triggered — results are strong but "
                "reversion risk is elevated."
            )

        if expectations_overrun and (verdict.startswith("STRONG") or verdict.startswith("SOLID")):
            if "EXPECTATIONS_OVERRUN" not in verdict:
                verdict = verdict + "_EXPECTATIONS_OVERRUN"
                verdict_detail += (
                    f" NOTE: Expectations overrun detected at {elevation_result['elevation']} "
                    "elevation — fundamentals are strong but market has priced in execution."
                )

    # Output recommendation
    if "WITH_CRITICAL_FLAGS" in verdict:
        output_recommendation = "FULL_MEMO + RISK_MAP (critical flag investigation required)"
    elif verdict == "PROBLEMATIC_QUARTER":
        output_recommendation = "FULL_MEMO + RISK_MAP"
    elif verdict == "WEAK_QUARTER":
        output_recommendation = "FULL_MEMO + RISK_MAP"
    elif "AT_PEAK" in verdict:
        output_recommendation = "FULL_MEMO + RISK_MAP (peak cycle analysis required)"
    elif "EXPECTATIONS_OVERRUN" in verdict:
        output_recommendation = "FULL_MEMO (expectations analysis — position sizing focus)"
    elif verdict == "STRONG_QUARTER":
        output_recommendation = "ONE_PAGE_SHEET"
    else:
        output_recommendation = "FULL_MEMO"

    return {
        "composite_score": total,
        "verdict": verdict,
        "verdict_detail": verdict_detail,
        "output_recommendation": output_recommendation,
        "total_flags": len(all_flags),
        "critical_flags": len(critical_flags),
        "peak_cycle_triggered": peak_cycle,
        "expectations_regime": mgmt_result.get("expectations_regime", "unknown"),
        "expectations_elevation": elevation_result["elevation"],
        "all_flags": all_flags,
        "breakdown": {
            "beat_quality": beat_result["beat_quality_score"],
            "operational_health": ops_result["operational_health_score"],
            "management_signals": mgmt_result["management_signal_score"]
        }
    }


def main():
    p = argparse.ArgumentParser(description="Earnings Quality Scorer v1.4.1")
    p.add_argument("--ticker", required=True)
    p.add_argument("--quarter", required=True)

    # Beat inputs
    p.add_argument("--revenue-beat-pct", type=float, default=0)
    p.add_argument("--eps-beat-pct", type=float, default=0)
    p.add_argument("--guidance-change", default="maintained",
                   choices=["raised", "raised_narrowed", "maintained",
                            "narrowed_lowered", "lowered", "withdrawn",
                            "initiated", "not_provided"])
    p.add_argument("--guidance-raise-magnitude", default="modest",
                   choices=["modest", "meaningful", "massive"])
    p.add_argument("--gross-margin-change-bps", type=float, default=0)
    p.add_argument("--gross-margin-change-yoy-bps", type=float, default=0)
    p.add_argument("--gross-margin-vs-5y-percentile", type=float, default=50)
    p.add_argument("--core-segment-gm-gap-pp", type=float, default=0)
    p.add_argument("--beat-driver", default="unknown",
                   choices=["volume", "mix", "pricing",
                            "one_time_favourable", "one_time_unfavourable",
                            "one_time",  # legacy
                            "fx", "unknown"])

    # v1.4: Operating margin inputs
    p.add_argument("--operating-margin-change-qoq-bps", type=float, default=0,
                   help="QoQ operating margin change in bps")
    p.add_argument("--operating-margin-change-yoy-bps", type=float, default=0,
                   help="YoY operating margin change in bps")

    # Operational
    p.add_argument("--ocf-conversion", type=float, default=1.0)
    p.add_argument("--fcf-conversion", type=float, default=1.0)
    p.add_argument("--dso-change-days", type=float, default=0)
    p.add_argument("--inventory-growth-pct", type=float, default=0)
    p.add_argument("--revenue-growth-pct", type=float, default=0)
    p.add_argument("--gaap-nongaap-op-margin-gap-pp", type=float, default=0)
    p.add_argument("--capex-to-revenue-ratio", type=float, default=0,
                   help="Capex as percent of revenue (for growth capex mode detection)")

    # Management + market
    p.add_argument("--management-tone", default="neutral",
                   choices=["bullish", "confident", "neutral",
                            "cautious", "defensive", "evasive"])
    p.add_argument("--stock-reaction", default="flat",
                   choices=["positive", "flat", "negative"])
    p.add_argument("--stock-1y-return-pct", type=float, default=0)
    p.add_argument("--stock-return-from-low-pct", type=float, default=0)
    p.add_argument("--stock-drawdown-from-high-pct", type=float, default=50)
    p.add_argument("--red-flags", default="[]")

    args = p.parse_args()
    red_flags = json.loads(args.red_flags)

    elevation = classify_expectations_elevation(
        args.stock_1y_return_pct,
        args.stock_return_from_low_pct,
        args.stock_drawdown_from_high_pct
    )

    beat = score_beat_quality(
        args.revenue_beat_pct, args.eps_beat_pct,
        args.guidance_change, args.guidance_raise_magnitude,
        args.gross_margin_change_bps, args.gross_margin_change_yoy_bps,
        args.gross_margin_vs_5y_percentile, args.core_segment_gm_gap_pp,
        args.beat_driver,
        args.operating_margin_change_qoq_bps,
        args.operating_margin_change_yoy_bps
    )
    ops = score_operational_health(
        args.ocf_conversion, args.fcf_conversion,
        args.dso_change_days, args.inventory_growth_pct, args.revenue_growth_pct,
        args.gaap_nongaap_op_margin_gap_pp,
        args.capex_to_revenue_ratio
    )
    mgmt = score_management_signals(
        args.management_tone, red_flags,
        args.stock_reaction, args.revenue_beat_pct, args.eps_beat_pct,
        args.guidance_change, elevation["elevation"]
    )
    composite = compute_composite(beat, ops, mgmt, elevation)

    print(json.dumps({
        "ticker": args.ticker,
        "quarter": args.quarter,
        "version": "1.4.1",
        "composite": composite,
        "expectations_elevation": elevation,
        "beat_quality": beat,
        "operational_health": ops,
        "management_signals": mgmt
    }, indent=2))


if __name__ == "__main__":
    main()
