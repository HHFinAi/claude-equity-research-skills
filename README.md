# 📊 Claude Equity Research Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Claude](https://img.shields.io/badge/Built%20for-Claude-orange.svg)](https://claude.ai)
[![Skills](https://img.shields.io/badge/Skills-7-blue.svg)](#-the-skills)

> **Institutional-quality equity research skills for Claude AI — systematizing the fundamental analysis playbook from buy-side investing into reusable, AI-executable frameworks.**

Seven composable skills that let Claude reason like a long-only fundamental analyst: classify growth, map competitive moats, parse earnings, trace supply chains, diagnose director networks, validate investment themes, and read broker research.

---

## 📋 Table of Contents

- [Why This Exists](#-why-this-exists)
- [The Skills](#-the-skills)
- [How Skills Work](#-how-skills-work)
- [Installation](#-installation)
- [Usage Examples](#-usage-examples)
- [Skill Composition Patterns](#-skill-composition-patterns)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Why This Exists

Most AI "investment analysis" prompts are shallow — they produce sell-side pastiche. These skills are different: each one encodes a specific, battle-tested research methodology used at buy-side shops, broken down into structured layers with explicit scoring, evidence requirements, and output schemas.

Built by someone with ~8 years in healthcare equity research and sustainability investing (The Global Fund, Baillie Gifford), these skills reflect how professional investors actually work — not what ChatGPT thinks investors do.

### What you get

- **Opinionated frameworks** — each skill takes a methodological stance (7 Powers + Greenwald + Thorndike for growth; Porter + value chain + geopolitical resilience for competitive analysis; etc.)
- **Mechanical scoring engines** — repeatable grading rubrics, not vibes
- **Evidence-first outputs** — every claim traced to filings, calls, or price action
- **Word-document deliverables** — institutional-quality memos, not chat responses
- **Composable** — chain them together for end-to-end thesis construction

---

## 🧰 The Skills

| Skill | Purpose | Typical Output |
|---|---|---|
| **growth-stock-analysis** | Evaluate high-growth equities using competitive moat theory, technology adoption dynamics, narrative economics, management quality, and platform strategy | Long-form thesis memo |
| **earnings-analysis** | Institutional post-print analysis with 4-layer framework (Parse → Compare → Diagnose → Decide) and mechanical scoring across beat quality, operational health, and management signals | One-page earnings sheet, full memo, or trade note |
| **competitive-analysis** | 11-dimension competitive assessment covering Porter's Five Forces, value chain, moat sustainability, geopolitical supply chain resilience, and forward indicators | Visual infographic + detailed section-by-section analysis |
| **corporate-network-analysis** | Map supplier-customer relationships, director interlocks, and executive networks to identify M&A signals and customer momentum | Relationship map + alpha hypothesis |
| **supply-chain-pass-through** | Decompose secular trends into sub-themes and map listed-equity beneficiaries across the value chain, substantiated with earnings call evidence | Thematic basket with beneficiary classification (value captor / volume taker / optionality / cost bearer) |
| **thematic-investment-research** | End-to-end methodology for theme validation, value chain mapping, universe construction, deep dives, and portfolio implementation | Full thematic research report |
| **investment-report-reader** | Parse PDF broker notes (GS/MS/JPM/UBS/Citi/BofA), 10-Ks, fund factsheets, with multi-report triangulation and chart/table extraction | Structured summary + extracted exhibits |

---

## 🔧 How Skills Work

Claude Skills are Markdown-based instruction bundles that Claude loads on-demand when their trigger conditions are met. Each skill lives in its own directory with:

```
skill-name/
├── SKILL.md              # The skill definition (required)
├── references/           # Supporting methodology docs
├── scripts/              # Optional executable helpers
└── assets/               # Templates, examples, images
```

When you install these skills into Claude (Desktop, Code, or API), Claude reads the description field in each `SKILL.md` and decides when to trigger the skill based on your query. No manual invocation needed.

**Learn more about skills:** [Anthropic Skills Documentation](https://docs.claude.com/en/docs/build-with-claude/skills)

---

## 📦 Installation

### Option 1: Claude Desktop / Claude Code

1. Clone this repository:
   ```bash
   git clone https://github.com/YOUR-USERNAME/claude-equity-research-skills.git
   ```

2. Copy the skill directories you want into your Claude skills folder:
   - **Claude Code**: `~/.claude/skills/`
   - **Claude Desktop**: Settings → Skills → Import

3. Restart Claude. The skills will activate automatically based on your queries.

### Option 2: Individual Skill

You don't need all seven. Grab just the ones you want:

```bash
# Example: just the earnings analysis skill
curl -L https://github.com/YOUR-USERNAME/claude-equity-research-skills/archive/main.tar.gz | \
  tar xz --strip=1 claude-equity-research-skills-main/earnings-analysis
```

### Option 3: Claude API

Reference the `SKILL.md` content directly in your system prompt, or use Anthropic's skills feature when available.

---

## 💡 Usage Examples

Once installed, just ask Claude in natural language. The skills trigger automatically.

### Earnings Analysis
> *"Analyze NVDA's Q3 FY26 earnings — I want the full post-print memo with scoring."*

Claude parses the release, compares against consensus and prior guide, runs the mechanical scoring engine (beat quality / operational health / management signals), and produces a scored Word memo with a one-page earnings sheet.

### Competitive Analysis
> *"Run a competitive analysis on ASML — I'm especially interested in the geopolitical supply chain resilience dimension given China export controls."*

Claude walks through all 11 dimensions with emphasis on supply chain resilience, outputs a visual infographic plus a full written assessment.

### Supply Chain Pass-Through
> *"AI capex is booming. Who actually captures the economics across the optical and memory value chains?"*

Claude decomposes the theme into sub-mechanisms, maps beneficiaries node-by-node, classifies each (value captor vs. volume taker), and substantiates with earnings call evidence (backlog, book-to-bill, guide raises).

### Investment Report Reader
> *"I've uploaded three sell-side notes on Viking Therapeutics. Triangulate the forecasts and flag coverage gaps."*

Claude compares price targets, valuation methodologies, and consensus estimates across reports, surfaces disagreements, and extracts charts/tables the text-only reader would miss.

### Thematic Investment Research
> *"Build me a thematic research package on AI-in-drug-discovery for 2026 — European listed names preferred."*

Claude runs the full workflow: theme validation → value chain mapping → universe construction → screening → company deep dives → portfolio implementation.

---

## 🔗 Skill Composition Patterns

These skills are designed to compose. Common chains:

**Single-name thesis construction:**
```
investment-report-reader → competitive-analysis → growth-stock-analysis
```
*Read what the Street thinks → pressure-test competitive position → build your own growth thesis.*

**Thematic basket construction:**
```
thematic-investment-research → supply-chain-pass-through → competitive-analysis (per name)
```
*Validate the theme → map beneficiaries → confirm moat at each node.*

**Post-earnings reassessment:**
```
earnings-analysis → corporate-network-analysis → competitive-analysis
```
*Diagnose the print → check for insider/network signals → re-score the moat.*

---
How to Use This Skill

In Claude.ai (recommended starting point)

This is the simplest way to get started. No terminal or coding experience is required. There are two approaches, depending on whether you want the skill available everywhere or only within a specific project.

Option A: Install account-wide via Customize (recommended)

This makes the skill available in all your conversations and in Cowork.

Download this repository as a ZIP file (on the repository's main page, click the green Code button, then Download ZIP).

Open claude.ai. In the left sidebar, click Customize (the toolbox icon), then go to Skills.

Click the + button, then + Create skill, and upload the ZIP file.

The skill will appear in your Skills list. Make sure its toggle is turned on.

Start any conversation and ask Claude to review your writing. For example:

Review the writing quality of my manuscript. Here is the Introduction section:

[paste your text]
Claude will recognize that the request matches the skill, load it, and produce a structured review report with specific findings and suggested revisions. You can also upload your manuscript as a PDF or paste individual sections.

Note: The ZIP file must contain the skill folder at the root level. If your ZIP contains sciwrite/SKILL.md (not just a loose SKILL.md), you're set.
Option B: Add to a specific Project's knowledge base

If you prefer to limit the skill to a particular project (for example, a project dedicated to a specific manuscript):

Download the SKILL.md file from this repository.
Open or create a Project in Claude.ai.
In the Project's knowledge base, click Add content and upload the SKILL.md file.
Start a conversation inside that Project and ask Claude to review your writing.
This approach keeps the skill scoped to one project, which is useful if you are working on multiple manuscripts with different conventions.

In Claude Code (terminal agent)

Place SKILL.md in .claude/skills/manuscript-review/ inside your manuscript project directory, then launch Claude Code and ask for a review. See HOW-TO-USE.md for full setup instructions, example prompts, and tips for each review mode.

In Claude's Cowork (desktop agent)

If you installed the skill account-wide via Customize (Option A above), it is already available in Cowork—no additional setup needed.

If you prefer to work with the file directly, you can also place the SKILL.md file in the folder you point Cowork at (or in a subfolder). Then ask Cowork to review a manuscript file in that same folder:

Review the writing quality of the manuscript draft in this folder.
In ChatGPT

Because OpenAI has adopted the Agent Skills standard, you can use this skill in ChatGPT through a Custom GPT:

Open the SKILL.md file and copy its full contents (everything below the closing --- of the header).
Go to chat.openai.com, click your profile icon, then My GPTs → Create a GPT.
In the Configure tab, paste the contents of the skill into the Instructions field. You may also want to add the YAML header's description text at the top so the GPT knows when to apply these instructions.
Name the GPT something like "SciWrite Reviewer" and save it.
Open the GPT and paste your manuscript text.
The output format and reasoning will follow the same structure as in Claude.

In Google Gemini

Gemini does not yet natively support the SKILL.md format, but you can achieve a similar result using a Gem (Gemini's equivalent of a custom assistant):

Open gemini.google.com and navigate to Gems (in the left sidebar, or via the Gem manager).
Create a new Gem. In the instructions field, paste the full body of the SKILL.md file (everything after the YAML header).
Save the Gem and open a conversation with it.
Paste your manuscript text and ask for a writing review.
General approach for any AI tool

If your preferred AI tool is not listed above, the pattern is the same:

Find the tool's mechanism for persistent instructions (custom assistants, system prompts, project instructions, or similar).
Paste the contents of SKILL.md into that mechanism.
Provide your manuscript text and ask for a review.
The skill is plain Markdown with no dependencies on any specific platform. It works wherever you can give an AI tool a block of instructions to follow.

Tips for Getting Good Results

Provide enough text for context. A single isolated sentence is hard to review for keyword consistency or logical flow. A full section or chapter gives the skill enough material to identify patterns—repeated nominalizations, inconsistent terminology, or structural problems that span multiple paragraphs.

Specify the review mode if you have a specific need. If you already know your weakness is passive voice, ask for a targeted review rather than a full pass. This produces faster, more focused feedback.

Use the interactive mode for learning. The paragraph-by-paragraph mode shows before/after revisions with explanations — useful for building long-term writing habits, not just fixing a single draft.

Review the output critically. The skill produces well-structured editorial feedback, but your domain expertise is the final quality check. Occasionally a "smothered verb" that the skill flags is actually the standard term in your field (e.g., "polymerization" is not a nominalization that needs fixing). Use your judgment.

Iterate. If a suggested revision changes your intended meaning, tell the AI why and ask it to try again. The skill's structured reasoning means the AI can explain why it flagged a particular sentence, which makes it easy to have a productive back-and-forth.




## 🤝 Contributing

Skills are opinionated by design — but they can always be sharpened. If you spot a gap in methodology, a missing scoring dimension, or a better reference framework:

1. Fork the repo
2. Create a feature branch (`git checkout -b improve-earnings-scoring`)
3. Commit your changes with clear reasoning in the message
4. Open a pull request describing *why* the change improves the skill

Contributions especially welcome in:
- Sector-specific extensions (semis, biotech, financials, energy)
- Non-US market adaptations (European disclosure norms, Japan, EM)
- Scoring engine refinements backed by empirical evidence
- Reference methodology additions (academic papers, practitioner books)

---

## ⚠️ Disclaimer

These skills are for research, educational, and analytical purposes only. They are **not** investment advice. The scoring engines, frameworks, and outputs reflect opinionated methodologies and are not guaranteed to predict market outcomes. Do your own work. Consult a licensed advisor before making investment decisions. Past frameworks do not guarantee future alpha.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details. Use them, fork them, adapt them, ship them in your own workflows.

---

## 🙏 Acknowledgments

Methodological debts owed to:
- **Baillie Gifford** — for the LTGG / 10Q / Stewardship research culture
- **Michael Porter, Bruce Greenwald, Hamilton Helmer** — competitive strategy foundations
- **Peter Thiel, Geoffrey Moore, William Thorndike** — platform and capital allocation lenses
- **Aswath Damodaran** — valuation discipline
- **Anthropic** — for building Claude and the Skills framework

---

*Built by a buy-side analyst who got tired of re-typing the same frameworks.*
