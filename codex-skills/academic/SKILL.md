---
name: academic
description: >-
  Review, draft, polish, and research academic papers and thesis chapters using
  30 writing principles and 12 specialist roles. Use for manuscript review,
  research positioning, literature surveys, bibliography audits, and LaTeX
  figures or layout.
---

# Academic Writing for Codex

Coordinate academic writing work using the bundled principles and specialist
roles. Invoke explicitly with `$academic <task>`, or select this skill when the
user requests academic writing help.

## Load context

1. Read [the writing principles](../../codex-references/principles/academic-writing.md).
   Resolve every bundled reference relative to this `SKILL.md`, regardless of
   the manuscript's working directory. If a required reference is missing,
   report the missing file and the resulting limitation; do not imply it was
   applied.
2. Follow the manuscript project's applicable `AGENTS.md` instructions. Read
   its writing conventions, relevant macros, adjacent sections, bibliography,
   and build instructions as needed. Preserve the author's voice and explicit
   preferences over the bundled defaults.
3. Identify the requested files, audience, and outcome from the conversation.
   Ask only for missing information that affects the work. For a new draft,
   establish the central insight, supporting evidence, and surrounding context.
4. Check `.review/` for earlier findings on this scope. Use those as context;
   verify the current files before treating an earlier finding as still valid.

## Select specialist roles

Read only the role references relevant to the task. Each role is also available
as a directly invokable plugin skill (for example, `$writing-reviewer` or
`$prose-polisher`). These roles do not require separate model configurations.

| Role | Reference | Scope |
| --- | --- | --- |
| Consistency checker | [consistency-checker](../../codex-references/agents/consistency-checker.md) | Terminology, cross-references, structure, figure/text agreement |
| Logic reviewer | [logic-reviewer](../../codex-references/agents/logic-reviewer.md) | Argument flow, transitions, narrative gaps |
| Technical reviewer | [technical-reviewer](../../codex-references/agents/technical-reviewer.md) | Mathematics, methodology, results, technical citations |
| Writing reviewer | [writing-reviewer](../../codex-references/agents/writing-reviewer.md) | Clarity, concision, grammar, tone; reports findings |
| LaTeX layout auditor | [latex-layout-auditor](../../codex-references/agents/latex-layout-auditor.md) | Compiled PDF layout, floats, sizing, alignment |
| Bibliography auditor | [bibliography-auditor](../../codex-references/agents/bibliography-auditor.md) | Citation metadata, publication status, capitalization, venues |
| Research analyst | [research-analyst](../../codex-references/agents/research-analyst.md) | Related work, novelty, positioning, research gaps |
| Brainstormer | [brainstormer](../../codex-references/agents/brainstormer.md) | Alternative framings, connections, research directions |
| Paper crawler | [paper-crawler](../../codex-references/agents/paper-crawler.md) | Collect, deduplicate, and classify literature |
| Prose polisher | [prose-polisher](../../codex-references/agents/prose-polisher.md) | Edit expression while preserving claims and citations |
| Section drafter | [section-drafter](../../codex-references/agents/section-drafter.md) | Draft sections, transitions, captions, abstracts |
| LaTeX figure specialist | [latex-figure-specialist](../../codex-references/agents/latex-figure-specialist.md) | Create or adjust TikZ/pgfplots figures and placement |

For a general chapter review, use consistency, logic, technical, writing, and
bibliography roles; add layout review when a compiled PDF is available. For
polishing, diagnose with the writing role, then apply the prose role. For a
literature survey, collect sources before research analysis. For a submission
check, review the manuscript, bibliography, and rendered layout, then verify any
requested fixes. Use a single role or work directly for a small task.

## Coordinate work in Codex

Briefly state the chosen roles and scope, then proceed with the authorized task.
When subagent tools are available and delegation is permitted, use them for
independent specialist reviews. Give each worker:

- The absolute path to its bundled role reference and principles, or their full
  contents if it cannot access those files.
- The manuscript paths, relevant project instructions, and the specific question
  to answer.
- A clear instruction to return findings without editing manuscript files for
  review, audit, research, and brainstorming roles.
- For action roles, the relevant review findings and exclusive ownership of the
  files they may edit. Sequence workers that need to change the same file.

Use agent types actually exposed by the host; do not pass a role filename as an
invented `subagent_type`. Respect the available concurrency limit and queue
remaining roles. Use the session's model selection. When delegation is
unavailable or disallowed, perform the same role passes sequentially yourself
and describe the result as a sequential review.

Use the host's available file-reading, search, editing, web, and image/PDF tools.
Role instructions describe capabilities, not permission grants. A missing tool
does not justify claiming its check succeeded. For layout review, inspect the
rendered PDF or page images; source inspection alone cannot confirm alignment
or float placement. Use the project's build command when available and report
compilation or rendering tools that are missing.

## Evidence and edits

Research and bibliography checks need retrieved sources. Open and verify primary
sources before claiming a citation, publication status, novelty comparison, or
paper result is confirmed. Include links and distinguish source evidence from
inference. If web access is unavailable, restrict conclusions to supplied
material and label verification gaps. Never invent references, measurements,
experimental outcomes, or supporting claims to complete a draft.

For paper collection, use the user's venue and year bounds. If none are given,
state a reasonable range based on the current date. Check the current DBLP and
OpenAlex documentation before using their APIs: authentication, response fields,
pagination, and limits can change. Follow the current API contract over dated
examples in the role reference. If a service is unavailable or credentials are
missing, report the coverage gap and use accessible sources. Label a truncated
or partial survey. Preserve existing result files when choosing output paths.

Review requests produce findings without changing the manuscript. A request to
draft, polish, or fix already authorizes those edits: diagnose first and complete
the requested work without another approval round. Ask when a missing scientific
claim or a substantive author decision prevents a sound edit. Pass concrete
review findings to action roles and verify changed passages, references, and
figures afterward.

## Synthesis and persistence

Merge duplicate findings and prioritize them as Critical, Important, or Minor.
Each finding should identify a file and line or PDF page, the problem, its
supporting evidence, a relevant principle when applicable, and a concrete fix.
Resolve disagreements where evidence permits; otherwise explain the uncertainty.
Adapt the output for drafts, brainstorming, and literature surveys.

Persist substantial reviews to `.review/YYYY-MM-DD-<scope>.md` in the manuscript
project, using a new suffix if that file already exists. If the user requested no
file writes, return the review in the response. Record the reviewed paths,
content hashes (including relevant context files), review scope, findings, and
verification limits. Reuse a prior review only when its scope and file hashes
still match, including uncommitted edits; otherwise review the affected files
and their dependencies. Missing hashes require a fresh comparison or review.
Do not use file dates as proof of unchanged content. Refresh time-sensitive
literature checks even when manuscript files have not changed.

Finish with the findings or changes, verification performed, and any remaining
author decisions or incomplete checks. Do not claim independent reviewers or
successful compilation unless those actually ran.
