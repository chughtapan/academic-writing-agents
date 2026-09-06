#!/usr/bin/env python3
"""Bundle portable Codex references from the shared Claude agent sources."""

import argparse
import pathlib


_ROOT = pathlib.Path(__file__).resolve().parents[1]
_BUNDLE = pathlib.Path(
    'codex/academic-writing-agents/skills/academic/references'
)
_REPLACEMENTS = (
    ('.claude/CLAUDE.md', 'AGENTS.md'),
    ('CLAUDE.md', 'AGENTS.md'),
    ('using the Edit tool', "using the host's editing tools"),
    ('`curl` or `WebFetch`', "`curl` or the host's web tools"),
    ('Invoke via `/orchestrate` or directly as a subagent.',
     'Invoke through `$academic` using this role.'),
)


def references(root: pathlib.Path) -> dict[pathlib.Path, str]:
    """Return self-contained reference paths and their Codex-adapted contents."""
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
        result[pathlib.Path('agents') / source.name] = body
    result[pathlib.Path('principles/academic-writing.md')] = (
        (root / 'principles/academic-writing.md').read_text(encoding='utf-8')
    )
    for path, content in result.items():
        for old, new in _REPLACEMENTS:
            content = content.replace(old, new)
        result[path] = content
    return result


def main() -> int:
    """Write bundled references, or check their freshness without writing."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true',
                        help='fail if bundled references are missing or stale')
    args = parser.parse_args()
    bundle = _ROOT / _BUNDLE
    expected = references(_ROOT)
    stale = []
    for relative, content in expected.items():
        target = bundle / relative
        if args.check:
            if (not target.is_file()
                    or target.read_text(encoding='utf-8') != content):
                stale.append(str(relative))
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding='utf-8')
    extras = set(bundle.rglob('*.md')) - {bundle / p for p in expected}
    stale.extend(str(path.relative_to(bundle)) for path in sorted(extras))
    if stale:
        print('Stale or unexpected Codex references: ' + ', '.join(stale))
        print('Run scripts/sync_codex_references.py; remove obsolete references.')
        return 1
    print(f'{len(expected)} Codex references '
          + ('are current.' if args.check else 'written.'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
