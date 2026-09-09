import glob, re, sys, os
sys.stdout.reconfigure(encoding='utf-8')

all_files = glob.glob('**/*', recursive=True)
scanned_files = [f for f in all_files if os.path.isfile(f) and f.endswith(('.html', '.css', '.js')) and 'node_modules' not in f and '.git' not in f and 'scripts' not in f]

print(f'Auditing {len(scanned_files)} production web files (.html, .css, .js)...')

targets = ['#00B8A9', '#07111C', '#00D2C1', '#00C5A3', 'rgba(0,184,169', 'rgba(0,197,163', '#003366']

residual = {}
for fpath in scanned_files:
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    for t in targets:
        matches = list(re.finditer(re.escape(t), content, re.IGNORECASE))
        if matches:
            residual.setdefault(fpath, {})[t] = len(matches)

if not residual:
    print('AUDIT PERFECT! ZERO old synthetic color instances found across all HTML, CSS, and JS files.')
else:
    print(f'Found residual colors in {len(residual)} files:')
    for fpath, items in residual.items():
        print(f'  {fpath}: {items}')
