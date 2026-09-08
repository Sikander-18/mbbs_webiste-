import os
import re

def update_brand_and_purge():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    html_files = []
    all_files = []
    
    for root, dirs, files in os.walk(repo_root):
        if any(p in root for p in ['.git', 'node_modules', '.system_generated', '__pycache__']):
            continue
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            fp = os.path.join(root, file)
            if ext == '.html':
                html_files.append(fp)
            if ext in ['.html', '.js', '.css', '.json', '.md', '.txt']:
                all_files.append(fp)

    print(f"Found {len(html_files)} HTML files and {len(all_files)} total files.")

    # 1. Update Header Brand Link in HTML files
    old_brand_pattern = re.compile(
        r'<a class="flex items-center gap-3 mr-auto"[^>]*>.*?</a>',
        re.DOTALL
    )

    new_brand_html = (
        '<a class="flex items-center gap-3 mr-auto" href="/" style="padding-right:2rem;border-right:1px solid rgba(255,255,255,0.1);text-decoration:none">'
        '<div class="brand-logo-badge" style="background:#FFFFFF;padding:5px 9px;border-radius:5px;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 6px rgba(0,0,0,0.2);border:1px solid rgba(255,255,255,0.25);flex-shrink:0">'
        '<img alt="Stellar Science Hub & Educonsultancy Logo" src="/assets/images/stellar_logo.png" style="height:26px;width:auto;max-width:110px;object-fit:contain;display:block"/>'
        '</div>'
        '<div>'
        '<p class="brand-title" style="font-family:var(--font-display);font-size:clamp(1rem, 1.35vw, 1.25rem);font-weight:700;color:white;line-height:1.15;letter-spacing:-0.01em;transition:color 0.4s;white-space:nowrap">Stellar Science Hub & Educonsultancy</p>'
        '<p class="brand-sub" style="font-family:var(--font-mono);font-size:0.62rem;font-weight:700;letter-spacing:0.2em;text-transform:uppercase;color:#00C5A3;margin-top:3px;transition:color 0.4s">MBBS ABROAD</p>'
        '</div>'
        '</a>'
    )

    # 2. Update Footer Brand Block in HTML files
    old_footer_pattern = re.compile(
        r'<div class="flex items-center gap-3 mb-5"><div style="width:48px;height:48px;flex-shrink:0;position:relative"><img alt="Stellar Science Hub & Educonsultancy"[^>]*>.*?</div><div><p style="font-family:var\(--font-display\)[^>]*>Stellar Science Hub & Educonsultancy</p><p style="font-family:var\(--font-mono\)[^>]*>.*?</p></div></div>',
        re.DOTALL
    )

    new_footer_brand_html = (
        '<div class="flex items-center gap-3 mb-5">'
        '<div class="brand-logo-badge" style="background:#FFFFFF;padding:5px 9px;border-radius:5px;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 6px rgba(0,0,0,0.2);border:1px solid rgba(255,255,255,0.25);flex-shrink:0">'
        '<img alt="Stellar Science Hub & Educonsultancy Logo" src="/assets/images/stellar_logo.png" style="height:26px;width:auto;max-width:110px;object-fit:contain;display:block"/>'
        '</div>'
        '<div>'
        '<p style="font-family:var(--font-display);font-size:clamp(1rem, 1.35vw, 1.25rem);font-weight:700;color:white;line-height:1.15;letter-spacing:-0.01em">Stellar Science Hub & Educonsultancy</p>'
        '<p style="font-family:var(--font-mono);font-size:0.62rem;font-weight:700;letter-spacing:0.2em;text-transform:uppercase;color:#00C5A3;margin-top:3px">MBBS ABROAD</p>'
        '</div>'
        '</div>'
    )

    header_updated = 0
    footer_updated = 0

    for fp in html_files:
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()

        new_content = old_brand_pattern.sub(new_brand_html, content)
        if new_content != content:
            header_updated += 1
            content = new_content

        new_content = old_footer_pattern.sub(new_footer_brand_html, content)
        if new_content != content:
            footer_updated += 1
            content = new_content

        with open(fp, 'w', encoding='utf-8') as f:
            f.write(content)

    print(f"Updated header branding in {header_updated} HTML files.")
    print(f"Updated footer branding in {footer_updated} HTML files.")

    # 3. Purge "worldwise" across all files
    replacements = [
        ("https://worldwiseducation.in", "https://stellarsciencehub.in"),
        ("http://worldwiseducation.in", "https://stellarsciencehub.in"),
        ("worldwiseducation.in", "stellarsciencehub.in"),
        ("Worldwise Education", "Stellar Science Hub & Educonsultancy"),
        ("worldwise education", "stellar science hub & educonsultancy"),
        ("WORLDWISE EDUCATION", "STELLAR SCIENCE HUB & EDUCONSULTANCY"),
        ("world.wiseeducation", "stellarsciencehub"),
        ("Worldwise", "Stellar Science Hub"),
        ("worldwise", "stellarsciencehub"),
        ("WORLDWISE", "STELLAR SCIENCE HUB")
    ]

    purged_files = 0
    total_replacements = 0

    for fp in all_files:
        if os.path.basename(fp) == 'update_branding_and_purge.py':
            continue
        try:
            with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            modified = False
            file_rep_count = 0
            for old_str, new_str in replacements:
                if old_str in content:
                    cnt = content.count(old_str)
                    content = content.replace(old_str, new_str)
                    file_rep_count += cnt
                    modified = True

            if modified:
                with open(fp, 'w', encoding='utf-8') as f:
                    f.write(content)
                purged_files += 1
                total_replacements += file_rep_count
        except Exception as e:
            print(f"Error processing {fp}: {e}")

    print(f"Purged worldwise in {purged_files} files with {total_replacements} total replacements.")

if __name__ == '__main__':
    update_brand_and_purge()
