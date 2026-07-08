import subprocess, re, os

# Get translation pairs from all commits
commits = ["7934c0e", "2a93511", "b9a870e", "2bbbec7", "f338a25", "eb654e8"]

all_pairs = []
for c in commits:
    result = subprocess.run(
        f"git show {c} --diff-filter=M -- '*.py' 2>/dev/null | grep -E '^[-+].*(help=|description=)' | grep -vE '^[-+]{3}'",
        shell=True, capture_output=True, text=True, timeout=10
    )
    old = None
    for line in result.stdout.strip().split('\n'):
        if line.startswith('-'):
            old = line[1:].strip()
        elif line.startswith('+') and old:
            all_pairs.append((old.strip(), line[1:].strip()))
            old = None

# Deduplicate
from collections import OrderedDict
seen = OrderedDict()
for old, new in all_pairs:
    # Use just the text content as key (remove formatting)
    seen[old] = new

print(f"Total: {len(seen)} unique translation changes")

# Extract just the string values
def extract_value(s):
    m = re.search(r'"(.*?)"', s)
    return m.group(1) if m else None

# Group by target file
file_changes = {}
for old, new in seen.items():
    old_val = extract_value(old)
    if old_val and len(old_val) > 5:
        # Find which file contains this
        result = subprocess.run(
            f"grep -rl '{old_val}' ruslan_cli/ --include='*.py' 2>/dev/null | head -1",
            shell=True, capture_output=True, text=True, timeout=5
        )
        fname = result.stdout.strip()
        if fname:
            if fname not in file_changes:
                file_changes[fname] = []
            file_changes[fname].append((old_val, extract_value(new)))

print(f"\nFiles with changes: {len(file_changes)}")
for f, changes in sorted(file_changes.items()):
    print(f"  {f}: {len(changes)} changes")

# Apply changes
for fname, changes in file_changes.items():
    with open(fname, 'r') as f:
        content = f.read()
    
    applied = 0
    for old_val, new_val in changes:
        if new_val and old_val in content:
            content = content.replace(old_val, new_val)
            applied += 1
    
    if applied > 0:
        with open(fname, 'w') as f:
            f.write(content)
        print(f"  ✓ {fname}: {applied}/{len(changes)} changes applied")

print("\nDone!")
