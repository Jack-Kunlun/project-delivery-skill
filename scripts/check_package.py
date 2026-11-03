#!/usr/bin/env python3
"""Check distributed documentation/navigation without running product suites."""
from pathlib import Path
import re

def require(condition, message):
    if not condition:
        raise RuntimeError(message)
from urllib.parse import unquote, urlsplit
root = Path(__file__).resolve().parents[1]
paths = [root / 'README.md', root / 'README.zh-CN.md', *(root / 'skills').rglob('*.md'), *(root / 'docs/zh-CN').rglob('*.md')]
paths = [p for p in paths if p.name != 'PROJECT.md']
guidance = (root / 'AGENTS.md').read_text()
require('acceptance_gate.py complete --root . --task ID' in guidance, 'Package validation failed')
require('`audit --root .`' in guidance and '`.delivery/gate.json`' in guidance, 'Package validation failed')
require('Register new tasks in the existing ledger/config' in guidance, 'Package validation failed')
require((root / '.delivery/gate.json').is_file(), 'Package validation failed')
links = 0
for p in paths:
    s = p.read_text()
    rel = p.relative_to(root).as_posix()
    require('/Users/' not in s and '/private/tmp' not in s, rel)
    require(len(re.findall('^```', s, re.M)) % 2 == 0, rel)
    if rel.startswith('skills/'):
        require(not re.search('[一-\u9fff]', s), rel)
    body = re.sub('^```[^\\n]*\\n.*?^```\\s*$', '', s, flags=re.M | re.S)
    zh = rel == 'README.zh-CN.md' or rel.startswith('docs/zh-CN/')
    for (label, target) in re.findall('\\[([^\\]]+)\\]\\(([^)]+)\\)', body):
        if urlsplit(target).scheme:
            continue
        dest = (p.parent / unquote(target.split('#', 1)[0])).resolve()
        require(dest.is_relative_to(root) and dest.is_file(), (rel, target))
        d = dest.relative_to(root).as_posix()
        dz = d == 'README.zh-CN.md' or d.startswith('docs/zh-CN/')
        if zh != dz:
            require('英文' in label or label == 'English' if zh else '中文' in label or 'Chinese' in label or 'zh-CN' in label, (rel, label))
        links += 1
    width = None
    for line in body.splitlines():
        if line.startswith('|'):
            n = len(line.split('|'))
            width = n if width is None else width
            require(n == width, (rel, line))
        else:
            width = None
runtime = root / 'skills/project-delivery'
require([p.name for p in runtime.glob('SKILL.md')] == ['SKILL.md'], 'Package validation failed')
require('name: project-delivery\n' in (runtime / 'SKILL.md').read_text(), 'Package validation failed')
require(not (root / 'docs/zh-CN/guide.md').read_text().startswith('---'), 'Package validation failed')
refs = {p.name for p in (runtime / 'references').glob('*.md')}
require(refs == {p.name for p in (root / 'docs/zh-CN/references').glob('*.md')}, 'Package validation failed')
for name in refs:
    a = (runtime / 'references' / name).read_text()
    b = (root / 'docs/zh-CN/references' / name).read_text()
    for pattern in ['^#{1,6} ', '^\\|', '^\\d+\\. ']:
        require(len(re.findall(pattern, a, re.M)) == len(re.findall(pattern, b, re.M)), (name, pattern))
blocks = lambda p: re.findall('^```sh\\n(.*?)^```', p.read_text(), re.M | re.S)
require(blocks(root / 'README.md') == blocks(root / 'README.zh-CN.md'), 'Package validation failed')
print(f'PASS: {len(paths)} documentation pages, {links} local links, {len(refs)} paired references; runtime language and installation snippets checked')
