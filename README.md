# Equity research skills

Seven research workflows for fundamental equity analysis. These are explicit
methodologies, not empirically calibrated predictors of investment returns.

| Skill | Purpose |
|---|---|
| growth-stock-analysis | Growth thesis, competitive advantages and adoption |
| earnings-analysis | Post-print review with explicit data coverage and abstention |
| competitive-analysis | Competitive position and durability |
| corporate-network-analysis | Evidence-backed business relationships |
| supply-chain-pass-through | Map economic beneficiaries and cost bearers |
| thematic-investment-research | Theme validation and universe construction |
| investment-report-reader | Source extraction and multi-report comparison |

## Installation

The earnings component is now a **commit-pinned submodule** of the maintained
`HHFinAi/earnings-analysis` repository, not another independently edited copy.

```bash
git clone --recurse-submodules https://github.com/HHFinAi/claude-equity-research-skills.git
cd claude-equity-research-skills
# For an existing checkout:
git submodule update --init --recursive
python tools/build_bundle.py
```

Install the ZIPs produced under `dist/` in a compatible Agent Skills host. Each
contains `skill-name/SKILL.md` and its supporting files. CI also builds ZIP
artifacts after successful checks. GitHub's ordinary **Download ZIP does not
include submodule contents**; use a recursive clone or a successful CI bundle.
Before these maintenance changes are merged, check out the maintenance branch
with the same name used by the pull request, then initialize its submodules.

For hosts without native skills support, use the Markdown as a framework and
supply references and execution capabilities separately. Do not assume a copied
instruction grants file access, Python execution or automatic routing. Product UI
and model availability should be verified in the relevant vendor documentation.

## Research discipline

Preserve source IDs, reporting periods, units and data cutoffs. Separate facts,
inference, model changes and open questions. Consensus requires a dated
pre-release snapshot. Missing data is not zero; unavailable evidence must not be
invented. Regime labels and scores are heuristic interpretations, not calibrated
probabilities. Test disconfirming evidence and do not treat corporate connections
as evidence of an undisclosed transaction without independent support.

Start with source intake, then competitive/growth analysis. For quarterly
maintenance, run earnings review before changing valuation assumptions. Use only
public or appropriately authorized materials; do not put licensed research or
private portfolio information into public examples.

## Maintenance and validation

`python -m unittest discover -s tests -v`

`python -m unittest discover -s earnings-analysis/tests -v`

Update the pinned earnings commit through a reviewed PR after its upstream tests
pass. Do not use `git submodule update --remote` in installation or CI, which
would replace a reproducible pin with an unreviewed moving branch. Other skills
remain locally maintained in this repository; they have not all undergone an
analytical benchmark. Historical README content is retained in `docs/archive/`.

MIT; see [LICENSE](LICENSE). Research framework only, not investment advice.
