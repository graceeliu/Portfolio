#!/usr/bin/env python3
"""
check_assets.py — verifies every file the site links to actually exists in
assets/, and flags files in assets/ that nothing links to.

Run from the portfolio/ directory:  python3 check_assets.py
Worth running after adding files and before you deploy — a broken PDF link
is invisible until someone clicks it.
"""
import glob, os, re

# Links appear in two places:
#   1. HTML attributes:   href="../assets/file.pdf"
#   2. The WRITING data in index.html:   href: "assets/file.pdf"
PATTERNS = [
    r'href="([^"${}]*assets/[^"${}]+)"',      # HTML attribute
    r'href:\s*"([^"${}]*assets/[^"${}]+)"',   # JS object property
]

refs, missing, external = {}, [], 0

for f in sorted(glob.glob('**/*.html', recursive=True)):
    if f == 'preview.html':
        continue
    src = open(f, encoding='utf-8').read()
    src = re.sub(r'<!--.*?-->', '', src, flags=re.S)   # skip HTML comments
    src = re.sub(r'/\*.*?\*/', '', src, flags=re.S)    # skip JS block comments
    for pat in PATTERNS:
        for href in re.findall(pat, src):
            path = os.path.normpath(os.path.join(os.path.dirname(f), href))
            refs.setdefault(path, set()).add(f)
    external += len(re.findall(r'href=(?:"|:\s*")https?://', src))

print("Files the site links to:")
for path in sorted(refs):
    ok = os.path.exists(path)
    if not ok:
        missing.append(path)
    print(f"  {'ok     ' if ok else 'MISSING'}  {os.path.basename(path)}")

orphans = [a for a in sorted(glob.glob('assets/*'))
           if os.path.normpath(a) not in refs]
if orphans:
    print("\nIn assets/ but nothing links to them:")
    for a in orphans:
        print(f"  {a}")

print("\nPieces with no link yet:")
found = False
for f in sorted(glob.glob('**/*.html', recursive=True)):
    if f == 'preview.html':
        continue
    for i, line in enumerate(open(f, encoding='utf-8'), 1):
        if re.search(r'href:\s*null', line) or 'class="pending"' in line:
            title = re.search(r'title: "([^"]+)"', line)
            label = title.group(1) if title else line.strip()[:60]
            print(f"  {f}:{i}  {label}")
            found = True
if not found:
    print("  none")

print(f"\nExternal links: {external}")
print()
if missing:
    print(f"{len(missing)} file(s) missing from assets/:")
    for m in missing:
        print(f"  {os.path.basename(m)}")
else:
    print("All linked files present.")
