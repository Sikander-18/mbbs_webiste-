import glob, re, os, sys
sys.stdout.reconfigure(encoding='utf-8')

html_files = sorted(glob.glob('**/*.html', recursive=True))
print(f'Starting batch conversion across {len(html_files)} HTML files...')

# Ordered replacements (from most specific compound rules to general fallbacks)
ordered_replacements = [
    # 1. Specific Hero sections & Overlays
    ('<section class="relative overflow-hidden" style="background:#00B8A9;color:#07111C;padding-top:7rem">',
     '<section class="relative overflow-hidden" style="background:#12130F;color:#F7F5EE;padding-top:7rem">'),
    ('style="background:#00B8A9;color:#07111C;padding-top:7rem"',
     'style="background:#12130F;color:#F7F5EE;padding-top:7rem"'),
    ('style="background:#00B8A9;color:#07111C;padding-top:7rem;padding-bottom:4rem;position:relative;overflow:hidden"',
     'style="background:#12130F;color:#F7F5EE;padding-top:7rem;padding-bottom:4rem;position:relative;overflow:hidden"'),
    ('style="background:#00B8A9;color:#07111C;padding-top:7rem;padding-bottom:5rem;position:relative;overflow:hidden"',
     'style="background:#12130F;color:#F7F5EE;padding-top:7rem;padding-bottom:5rem;position:relative;overflow:hidden"'),
    ('style="background:#00B8A9;color:#07111C;padding:clamp(4rem,7vw,6rem) 0;position:relative;overflow:hidden"',
     'style="background:#12130F;color:#F7F5EE;padding:clamp(4rem,7vw,6rem) 0;position:relative;overflow:hidden"'),
    ('style="background:#00B8A9;color:#07111C;position:relative;overflow:hidden"',
     'style="background:#12130F;color:#F7F5EE;position:relative;overflow:hidden"'),
    ('style="background:linear-gradient(180deg, rgba(0,51,102,0.92) 0%, rgba(0,51,102,0.85) 100%)"',
     'style="background:linear-gradient(180deg, rgba(18,19,15,0.94) 0%, rgba(18,19,15,0.88) 100%)"'),
    ('background:linear-gradient(180deg, rgba(0,51,102,0.92) 0%, rgba(0,51,102,0.85) 100%)',
     'background:linear-gradient(180deg, rgba(18,19,15,0.94) 0%, rgba(18,19,15,0.88) 100%)'),
    ('linear-gradient(105deg, #003366 35%, rgba(0,51,102,0.92) 55%, rgba(0,51,102,0.6) 80%, rgba(0,51,102,0.3) 100%)',
     'linear-gradient(105deg, #12130F 35%, rgba(18,19,15,0.94) 55%, rgba(18,19,15,0.6) 80%, rgba(18,19,15,0.3) 100%)'),
    ('linear-gradient(to top, rgba(0,51,102,0.8) 0%, rgba(0,51,102,0.2) 60%, transparent 100%)',
     'linear-gradient(to top, rgba(18,19,15,0.85) 0%, rgba(18,19,15,0.2) 60%, transparent 100%)'),
    ('linear-gradient(to top, #003366, transparent)',
     'linear-gradient(to top, #12130F, transparent)'),

    # 2. Left accents & Gold highlights
    ('style="width:3px;background:#00C5A3"', 'style="width:3px;background:#C9A45C"'),
    ('border-left:3px solid #00C5A3;', 'border-left:3px solid #C9A45C;'),
    ('border-left:3px solid #00C5A3"', 'border-left:3px solid #C9A45C"'),
    ('border:3px solid #00C5A3', 'border:3px solid #C9A45C'),
    ('border:2px solid #00C5A3', 'border:2px solid #C9A45C'),
    ('height:2px;background:#00B8A9;transform:scaleX(0)', 'height:2px;background:#C9A45C;transform:scaleX(0)'),
    ('width:32px;height:2px;background:#00B8A9;', 'width:32px;height:2px;background:#C9A45C;'),
    ('border-left:2px solid #00B8A9;', 'border-left:2px solid #C9A45C;'),
    ('border-left:2px solid #00B8A9"', 'border-left:2px solid #C9A45C"'),

    # 3. Specific Buttons, CTA boxes, Tables
    ('style="background:#00B8A9;color:#07111C;color:#FFFFFF"',
     'style="background:#283A27;color:#F7F5EE"'),
    ('style="background:#00B8A9;border:1px solid #00B8A9;color:#07111C;font-weight:700;box-shadow:0 4px 20px rgba(0,184,169,0.4);"',
     'style="background:#283A27;border:1px solid #283A27;color:#F7F5EE;font-weight:700;box-shadow:0 4px 20px rgba(40,58,39,0.4);"'),
    ('style="background:#00B8A9;color:#07111C;border:1px solid #004488;padding:2.5rem"',
     'style="background:#283A27;color:#F7F5EE;border:1px solid rgba(255,255,255,0.15);padding:2.5rem"'),
    ('style="background:#00B8A9;color:#07111C;border:1px solid rgba(255,255,255,0.1);padding:2rem;height:fit-content"',
     'style="background:#283A27;color:#F7F5EE;border:1px solid rgba(255,255,255,0.15);padding:2rem;height:fit-content"'),
    ('background:#00B8A9;color:#07111C;border:1px solid #00B8A9;',
     'background:#283A27;color:#F7F5EE;border:1px solid #283A27;'),
    ('background:#00B8A9;color:#07111C;border:1px solid #00B8A9"',
     'background:#283A27;color:#F7F5EE;border:1px solid #283A27"'),
    ('background:#00B8A9;color:#07111C;',
     'background:#283A27;color:#F7F5EE;'),
    ('background:#00B8A9;color:#07111C"',
     'background:#283A27;color:#F7F5EE"'),
    ('color:#07111C;background:#00B8A9;border:1px solid #00D2C1;padding:4px 10px',
     'color:#F7F5EE;background:#283A27;border:1px solid #385237;padding:4px 10px'),
    ('color:#07111C;background:#00B8A9;border:1px solid #00D2C1;padding:3px 8px;flex-shrink:0',
     'color:#F7F5EE;background:#283A27;border:1px solid #385237;padding:3px 8px;flex-shrink:0'),
    ('style="background:#00B8A9;border:1px solid #00D2C1"',
     'style="background:#283A27;border:1px solid #385237"'),
    ('background:#00B8A9;border:1px solid #00D2C1',
     'background:#283A27;border:1px solid #385237'),

    # 4. Chips, Badges & Highlights
    ('style="border:1px solid #00B8A9;background:rgba(0,197,163,0.08);padding:10px 16px"',
     'style="border:1px solid rgba(40,58,39,0.3);background:#EBF2EA;padding:10px 16px"'),
    ('border:1px solid #00B8A9;background:rgba(0,197,163,0.08)',
     'border:1px solid rgba(40,58,39,0.3);background:#EBF2EA'),
    ('background:rgba(0,197,163,0.08)', 'background:#EBF2EA'),
    ('background:rgba(0,197,163,0.6)', 'background:rgba(40,58,39,0.6)'),
    ('background:rgba(0,184,169,0.12)', 'background:#EBF2EA'),
    ('background:rgba(0,184,169,0.15)', 'background:#EBF2EA'),
    ('rgba(0,184,169,0.4)', 'rgba(40,58,39,0.35)'),
    ('rgba(0,184,169,0.2)', 'rgba(40,58,39,0.2)'),
    ('rgba(0,184,169,0.1)', 'rgba(201,164,92,0.1)'),
    ('rgba(0,184,169,0.25)', 'rgba(40,58,39,0.25)'),
    ('rgba(0,184,169,0.3)', 'rgba(40,58,39,0.3)'),
    ('rgba(0,197,163,0.08)', 'rgba(40,58,39,0.08)'),
    ('rgba(0,197,163,0.12)', 'rgba(40,58,39,0.12)'),
    ('rgba(0,197,163,0.18)', 'rgba(40,58,39,0.2)'),
    ('rgba(0,197,163,0.01)', 'rgba(40,58,39,0.02)'),
    ('rgba(0,197,163,0.5)', 'rgba(40,58,39,0.5)'),

    # 5. Blue / Navy items
    ('group-hover:text-[#003366]', 'group-hover:text-[#283A27]'),
    ('border-bottom:2px solid #003366', 'border-bottom:2px solid #283A27'),
    ('style="background:#003366"', 'style="background:#12130F"'),
    ('background:#003366;', 'background:#12130F;'),
    ('background:#003366"', 'background:#12130F"'),

    # 6. Footers & borders
    ('footer style="background:#07111C;border-top:4px solid #00B8A9"',
     'footer style="background:#12130F;border-top:4px solid #283A27"'),
    ('border-top:4px solid #00B8A9', 'border-top:4px solid #283A27'),
    ('border:1px solid #00B8A9', 'border:1px solid #283A27'),
    ('border-left-color:#00B8A9', 'border-left-color:#283A27'),

    # 7. General Base Replacements
    ('background:#00B8A9;', 'background:#283A27;'),
    ('background:#00B8A9"', 'background:#283A27"'),
    ('background:#07111C;', 'background:#12130F;'),
    ('background:#07111C"', 'background:#12130F"'),
    ('color:#00B8A9;', 'color:#283A27;'),
    ('color:#00B8A9"', 'color:#283A27"'),
    ('color:#07111C;', 'color:#181915;'),
    ('color:#07111C"', 'color:#181915"'),
    ('color:#07111C<', 'color:#181915<'),
    ('#00D2C1', '#385237'),
    ('#00C5A3', '#C9A45C'),
    ('#003366', '#181915'),
    ('#00B8A9', '#283A27'),
    ('#07111C', '#12130F')
]

modified_count = 0
total_replacements = 0

for fpath in html_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = content
    file_changes = 0
    for old, new in ordered_replacements:
        if old in new_content:
            count = new_content.count(old)
            new_content = new_content.replace(old, new)
            file_changes += count

    if file_changes > 0:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        modified_count += 1
        total_replacements += file_changes
        # Print progress periodically
        if modified_count % 10 == 0 or modified_count == 1:
            print(f'[{modified_count}/96] {fpath}: {file_changes} replacements applied.')

print(f'\nBATCH COMPLETED: {modified_count} files modified with {total_replacements} total replacements.')
