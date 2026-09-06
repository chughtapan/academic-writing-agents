# Codex plugin installation

Academic Writing Agents is a Codex plugin with **13 skills**: the `$academic`
orchestrator and 12 directly invokable specialists. It includes the complete
writing principles, role references, and Plugin Directory metadata and icons.
Install the whole plugin through its repository marketplace.

## Install from GitHub

With a Codex CLI that supports `codex plugin`:

```bash
codex plugin marketplace add chughtapan/academic-writing-agents
codex plugin add academic-writing-agents@chughtapan-academic-writing-agents
```

Start a new Codex thread in your manuscript project. The plugin is available in
**Plugins**, and you can invoke its skills directly:

```text
$academic-writing-agents:academic review my introduction in sections/introduction.tex
$academic-writing-agents:writing-reviewer check the clarity of my abstract
$academic-writing-agents:prose-polisher polish the abstract while preserving claims
$academic-writing-agents:bibliography-auditor audit references.bib
$academic-writing-agents:paper-crawler survey test-time adaptation from 2024 onward
$academic-writing-agents:latex-layout-auditor check the figure layout in main.pdf
```

Skills support automatic selection when relevant. Installation uses the full
repository as the plugin source; there is no manual copying into a skills folder.

## Install from a local checkout

Choose this method instead when developing the plugin or using a local clone:

```bash
git clone https://github.com/chughtapan/academic-writing-agents.git
cd academic-writing-agents
codex plugin marketplace add .
codex plugin add academic-writing-agents@chughtapan-academic-writing-agents
```

These commands also work in PowerShell with Codex CLI and Git installed.
Keep the checkout available as the source for future local plugin updates.
Restart with a new thread after installing or updating the plugin.

Check installation:

```bash
codex plugin list --marketplace chughtapan-academic-writing-agents --json
```

If you previously copied the standalone `academic` skill from an earlier version
of this fork, move that old skill out of `~/.agents/skills`, `~/.codex/skills`, or
any project `.agents/skills` directory where you installed it. This avoids showing
both the old standalone skill and the plugin's orchestrator. Keep any local
customizations before moving it.

## Included skills

Codex namespaces installed skills as `academic-writing-agents:<skill-name>`.
The table uses short names for readability; select the plugin's namespaced entry
in the skill picker when other installed skills have the same short name.

| Skill | Purpose |
| --- | --- |
| `$academic` | Coordinate multiple specialists and synthesize their findings |
| `$consistency-checker` | Terminology, cross-references, structure, figure/text agreement |
| `$logic-reviewer` | Argument flow, transitions, narrative gaps |
| `$technical-reviewer` | Mathematics, methodology, results, technical citations |
| `$writing-reviewer` | Prose clarity, concision, grammar, tone |
| `$latex-layout-auditor` | Rendered PDF layout, floats, sizing, alignment |
| `$bibliography-auditor` | Citation metadata, publication status, capitalization, venues |
| `$research-analyst` | Related work, novelty, positioning, research gaps |
| `$brainstormer` | Alternative framings, connections, research directions |
| `$paper-crawler` | Collect, deduplicate, and classify literature |
| `$prose-polisher` | Edit expression while preserving claims and citations |
| `$section-drafter` | Draft sections, transitions, captions, abstracts |
| `$latex-figure-specialist` | Create or adjust TikZ/pgfplots figures and placement |

The orchestrator can delegate independent reviews when Codex exposes subagent
tools and permits delegation. It runs sequentially otherwise. Specialist skills
work directly on their own scope and use the session's model selection.

## Package layout

This follows the repository plugin and marketplace pattern used by
[Research Companion](https://github.com/andrehuang/research-companion):

```text
.codex-plugin/plugin.json          # Codex identity, skills path, and presentation
.agents/plugins/marketplace.json    # Codex repository marketplace
agents/openai.yaml                 # Plugin presentation metadata
assets/                            # Plugin icons
codex-skills/
  academic/                        # Orchestrator
  writing-reviewer/                # One of 12 specialist skills
  ...
codex-references/                   # Shared Codex workflow, roles, and principles
.claude-plugin/                     # Claude Code plugin and marketplace
skills/academic/                   # Claude Code orchestrator
agents/*.md                        # Canonical specialist definitions
principles/academic-writing.md      # Canonical principles
```

The Codex manifest selects `./codex-skills/`, so Codex loads the adapted skills.
The Claude Code plugin continues to use `skills/academic/` and `agents/*.md`.
Shared references are resolved relative to each installed instruction file, so
neither host depends on the author's filesystem paths.

## Requirements and behavior

- Follow the manuscript project's `AGENTS.md` and author preferences.
- Reviews return findings; drafting, polishing, and fix requests authorize their
  corresponding edits. Editors run on separate files or in sequence.
- Research and publication checks need web access. Missing API credentials or
  unavailable services are reported as coverage gaps.
- LaTeX compilation needs your project's build tools. Visual layout checks need
  a PDF or image viewer. Unavailable checks are reported.
- The orchestrator saves substantial reviews in the manuscript's `.review/`
  unless the user requests no writes. Incremental reviews use content hashes,
  including uncommitted changes, and refresh time-sensitive research checks.

## Maintenance

Edit canonical definitions under `agents/` and `principles/`, then synchronize
Codex references and specialist entrypoints from the repository root:

```bash
python3 scripts/sync_codex_references.py
python3 scripts/sync_codex_references.py --check
python3 -m unittest discover -s tests -v
```

Edit Codex orchestration in `codex-skills/academic/SKILL.md`, and shared
specialist behavior in `codex-references/specialist-workflow.md`. Generated role
references and specialist skills are checked for missing, stale, and obsolete
files. Python is needed for maintenance, not for plugin installation.

See [OpenAI's plugin packaging documentation](https://developers.openai.com/plugins/build/plugins)
and [skill documentation](https://learn.chatgpt.com/docs/build-skills).
