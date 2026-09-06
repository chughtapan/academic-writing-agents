#!/usr/bin/env python3
"""Synchronize Codex specialist skills and shared references."""

import argparse
import json
import pathlib
import re


_ROOT = pathlib.Path(__file__).resolve().parents[1]
_BUNDLE = pathlib.Path('codex-references')
_SKILLS = pathlib.Path('codex-skills')
_REPLACEMENTS = (
    ('.claude/CLAUDE.md', 'AGENTS.md'),
    ('CLAUDE.md', 'AGENTS.md'),
    ('using the Edit tool', "using the host's editing tools"),
    ('`curl` or `WebFetch`', "`curl` or the host's web tools"),
    ('Invoke via `/orchestrate` or directly as a subagent.',
     'Invoke through `$academic` using this role.'),
)


def references(root: pathlib.Path) -> dict[pathlib.Path, str]:
    """Return generated plugin paths and their Codex-adapted contents."""
    sources = sorted((root / 'agents').glob('*.md'))
    if not sources:
        raise ValueError('No agent definitions found')
    result = {}
    for source in sources:
        content = source.read_text(encoding='utf-8')
        if not content.startswith('---\n') or '\n---\n' not in content[4:]:
            raise ValueError(f'Missing agent frontmatter: {source}')
        # Claude tool allowlists and model names are not Codex role settings.
        body = content.split('\n---\n', 1)[1].lstrip()
        result[_BUNDLE / 'agents' / source.name] = body
        header = content.split('\n---\n', 1)[0]
        description = re.search(r'^description: (.+)$', header, re.MULTILINE)
        if description is None or description[1].startswith(('>', '|')):
            raise ValueError(f'Expected a one-line description: {source}')
        result.update(specialist_skill(source.stem, description[1]))
    result[_BUNDLE / 'principles/academic-writing.md'] = (
        (root / 'principles/academic-writing.md').read_text(encoding='utf-8')
    )
    for path, content in result.items():
        for old, new in _REPLACEMENTS:
            content = content.replace(old, new)
        result[path] = content
    return result


def specialist_skill(name: str, description: str) -> dict[pathlib.Path, str]:
    """Build a directly invokable specialist with shared plugin resources."""
    title = name.replace('-', ' ').title().replace('Latex', 'LaTeX')
    skill = f'''---
name: {name}
description: {json.dumps(description)}
---

# {title}

Apply this specialist to the user's academic writing request. Before starting,
read these bundled resources, resolving paths relative to this `SKILL.md`:

1. [Codex specialist workflow](../../codex-references/specialist-workflow.md)
2. [Writing principles](../../codex-references/principles/academic-writing.md)
3. [{title} role](../../codex-references/agents/{name}.md)

Follow the shared workflow when adapting the role to the current host and
available tools. Work directly on this role's scope; use `$academic` when the
user wants a coordinated review across several specialties.
'''
    interface = {
        'display_name': title,
        'short_description': f'{title} for academic manuscripts',
        'default_prompt': f'Use ${name} to help with my academic manuscript.',
    }
    metadata = 'interface:\n' + ''.join(
        f'  {key}: {json.dumps(value)}\n' for key, value in interface.items()
    )
    return {
        _SKILLS / name / 'SKILL.md': skill,
        _SKILLS / name / 'agents/openai.yaml': metadata,
    }


def main() -> int:
    """Write bundled references, or check their freshness without writing."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true',
                        help='fail if bundled references are missing or stale')
    args = parser.parse_args()
    expected = references(_ROOT)
    stale = []
    for relative, content in expected.items():
        target = _ROOT / relative
        if args.check:
            if (not target.is_file()
                    or target.read_text(encoding='utf-8') != content):
                stale.append(str(relative))
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding='utf-8')
    managed = set((_ROOT / _BUNDLE / 'agents').glob('*.md'))
    managed.update((_ROOT / _BUNDLE / 'principles').glob('*.md'))
    for path in (_ROOT / _SKILLS).iterdir():
        if path.is_dir() and path.name != 'academic':
            managed.update(child for child in path.rglob('*') if child.is_file())
    extras = managed - {_ROOT / path for path in expected}
    stale.extend(str(path.relative_to(_ROOT)) for path in sorted(extras))
    if stale:
        print('Stale or unexpected generated Codex files: ' + ', '.join(stale))
        print('Run scripts/sync_codex_references.py; remove obsolete files.')
        return 1
    print(f'{len(expected)} generated Codex files '
          + ('are current.' if args.check else 'written.'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
