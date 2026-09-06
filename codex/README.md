# Academic Writing Agents for Codex

The Codex version includes the same 30 writing principles and 12 specialist
roles as the Claude Code plugin. It uses Codex project instructions (`AGENTS.md`),
available host tools, and optional parallel workers. It also works sequentially
when subagents are unavailable. No Claude installation, Claude model, or MCP
server is required.

## Install the skill

Clone this fork and copy the complete skill directory into Codex's user skill
directory. The commands below refuse to replace an existing `academic` skill;
if one is already installed, compare or back it up before replacing it.

macOS / Linux:

```bash
git clone https://github.com/chughtapan/academic-writing-agents.git
cd academic-writing-agents
mkdir -p "$HOME/.agents/skills"
test ! -e "$HOME/.agents/skills/academic" && \
  cp -R codex/academic-writing-agents/skills/academic "$HOME/.agents/skills/academic"
```

Windows PowerShell:

```powershell
git clone https://github.com/chughtapan/academic-writing-agents.git
Set-Location academic-writing-agents
$skills = Join-Path $HOME '.agents/skills'
New-Item -ItemType Directory -Force -Path $skills | Out-Null
$destination = Join-Path $skills 'academic'
if (Test-Path $destination) {
    throw "An academic skill already exists at $destination"
}
Copy-Item -Recurse 'codex/academic-writing-agents/skills/academic' $destination
```

For a project-only installation, copy the same complete `academic` directory to
`<manuscript-project>/.agents/skills/academic` instead. Copying only `SKILL.md`
would omit its required references. The installed folder is self-contained and
does not depend on the checkout remaining at its original location.

Start a new Codex session in your manuscript project and invoke:

```text
$academic review my introduction in sections/introduction.tex
$academic polish the abstract while preserving claims and citations
$academic audit references.bib for missing fields and published versions
$academic survey recent work on test-time adaptation from 2024 onward
$academic check figure layout in main.pdf
```

The skill also supports automatic selection for academic writing requests.
See the [official skill discovery documentation](https://learn.chatgpt.com/docs/build-skills)
for supported installation locations.

## Plugin package

`academic-writing-agents/` is also a complete Codex plugin root, ready to include
as a plugin source in a Codex marketplace or import through a host that supports
local plugins:

```text
academic-writing-agents/
  .codex-plugin/plugin.json
  skills/academic/
    SKILL.md
    agents/openai.yaml
    references/
      principles/academic-writing.md
      agents/                       # All 12 role references
```

The root `.claude-plugin/` and `marketplace.json` in the repository belong to
Claude Code. Use the nested `codex/academic-writing-agents/` directory for Codex
plugin packaging. The direct skill installation above works without configuring
a marketplace. See [OpenAI's plugin packaging documentation](https://developers.openai.com/plugins/build/plugins).

## Behavior and requirements

- The 12 specialist descriptions are role references loaded on demand. They do
  not register custom agent types or change your Codex model configuration.
- Reviews return findings; drafting, polishing, and fix requests authorize the
  corresponding manuscript edits. Subagents receive scoped tasks, and editors
  work on separate files or run in sequence.
- Research and publication checks need web access. API authentication and
  availability depend on the provider; missing access is reported as a coverage
  gap. Literature survey examples are not a promise of exhaustive retrieval.
- LaTeX compilation needs your project's build tools. A visual layout check
  also needs PDF or image viewing capabilities. Unavailable checks are reported.
- Substantial review reports are saved under the manuscript's `.review/` unless
  the user requests no writes. Incremental reviews use content hashes, including
  uncommitted changes, and refresh time-sensitive research checks.

## Maintaining the shared references

Edit the canonical definitions under the repository's `agents/` and
`principles/`, then regenerate the Codex copies from the repository root:

```bash
python3 scripts/sync_codex_references.py
python3 scripts/sync_codex_references.py --check
```

The dependency-free Python script removes Claude-only frontmatter and adapts
project instruction and tool references. Keep Codex orchestration changes in
`codex/academic-writing-agents/skills/academic/SKILL.md`. Review generated changes
when updating upstream definitions; generation checks freshness, not behavior.
Python is only needed for maintenance, not for installing the skill.
