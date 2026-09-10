"""Install the approved seven-country university catalogue.

This is intentionally a targeted content migration: it replaces catalogue sections,
updates the matching country-page institution sections, removes retired internal
university routes, and refreshes the small canonical datasets used for audits.
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent

COUNTRIES = [
    {
        "slug": "uzbekistan",
        "name": "Uzbekistan",
        "flag": "🇺🇿",
        "network": "7 government institutes",
        "budget": "₹30–35 lakh",
        "institutions": [
            ("Tashkent State Medical University", "Tashkent", "https://admissions.tma.uz/en/"),
            ("Samarkand State Medical University", "Samarkand", "https://www.sammu.uz/en"),
            ("Andijan State Medical Institute", "Andijan", "https://adti.uz/en/"),
            ("Bukhara State Medical Institute named after Abu Ali ibn Sino", "Bukhara", "https://bsmi.uz/en/"),
            ("Fergana Medical Institute of Public Health", "Fergana", "https://www.fmioph.uz/"),
        ],
    },
    {
        "slug": "kyrgyzstan",
        "name": "Kyrgyzstan",
        "flag": "🇰🇬",
        "network": "5 government institutes",
        "budget": "₹30–35 lakh",
        "institutions": [
            ("I.K. Akhunbaev Kyrgyz State Medical Academy (KSMA)", "Bishkek", "https://ksma.edu.kg/en"),
            ("Osh State University – Faculty of Medicine", "Osh", "https://www.oshsu.kg/en/page/109"),
            ("Jalal-Abad State University named after B. Osmonov – Medical Faculty", "Jalal-Abad", "https://jasu.kg/"),
            ("Kyrgyz-Russian Slavic University named after B.N. Yeltsin – Faculty of Medicine", "Bishkek", "https://www.krsu.kg/en/medical_faculty"),
        ],
    },
    {
        "slug": "kazakhstan",
        "name": "Kazakhstan",
        "flag": "🇰🇿",
        "network": "10–12 government institutes",
        "budget": "₹30–35 lakh",
        "institutions": [
            ("Asfendiyarov Kazakh National Medical University (KazNMU)", "Almaty", "https://kaznmu.edu.kz/"),
            ("Medical University Astana", "Astana", "https://amu.edu.kz/"),
            ("Karaganda Medical University", "Karaganda", "https://qmu.edu.kz/"),
            ("Semey Medical University", "Semey", "https://smu.edu.kz/"),
            ("West Kazakhstan Marat Ospanov Medical University", "Aktobe", "https://zkmu.edu.kz/"),
        ],
    },
    {
        "slug": "russia",
        "name": "Russia",
        "flag": "🇷🇺",
        "network": "60+ government institutes · 10+ high-level tie-ups",
        "budget": "₹27–45 lakh",
        "institutions": [
            ("Sechenov University – First Moscow State Medical University", "Moscow", "https://www.sechenov.ru/eng/"),
            ("Pirogov Russian National Research Medical University", "Moscow", "https://pirogov-university.com/"),
            ("Pavlov First Saint Petersburg State Medical University", "Saint Petersburg", "https://www.en.1spbgmu.ru/"),
            ("Kazan State Medical University", "Kazan", "https://kgmu.kcn.ru/"),
            ("Tver State Medical University", "Tver", "https://tvgmu.ru/"),
        ],
    },
    {
        "slug": "bangladesh",
        "name": "Bangladesh",
        "flag": "🇧🇩",
        "network": "37 government institutes · 15+ high-level tie-ups",
        "budget": "₹32–45 lakh",
        "institutions": [
            ("Dhaka Medical College", "Dhaka", "https://dmc.gov.bd/"),
            ("Sir Salimullah Medical College", "Dhaka", "https://www.ssmcbd.net/"),
            ("Chittagong Medical College", "Chattogram", "https://cmc.gov.bd/"),
            ("Rajshahi Medical College", "Rajshahi", "http://rmc.gov.bd/"),
            ("Mymensingh Medical College", "Mymensingh", "http://mmc.gov.bd/"),
        ],
    },
    {
        "slug": "georgia",
        "name": "Georgia",
        "flag": "🇬🇪",
        "network": "4–5 government institutes · director consultation",
        "budget": "₹38–55 lakh",
        "institutions": [
            ("Tbilisi State Medical University (TSMU)", "Tbilisi", "https://tsmu.edu/ts/index.php?lang=en"),
            ("Ivane Javakhishvili Tbilisi State University (TSU)", "Tbilisi", "https://tsu.ge/en/programs/434"),
            ("Ilia State University", "Tbilisi", "https://iliauni.edu.ge/en/iliauni/AcademicDepartments/sainjinro-fakulteti-270/programebi-310/medicinis-programa"),
            ("Akaki Tsereteli State University", "Kutaisi", "https://atsu.edu.ge/"),
            ("Batumi Shota Rustaveli State University", "Batumi", "https://www.bsu.edu.ge/?lang=en"),
        ],
    },
    {
        "slug": "nepal",
        "name": "Nepal",
        "flag": "🇳🇵",
        "network": "8–9 government institutes",
        "budget": "₹57–80 lakh",
        "institutions": [
            ("Institute of Medicine (IOM), Tribhuvan University – Maharajgunj Medical Campus", "Kathmandu", "https://www.iom.edu.np/"),
            ("B.P. Koirala Institute of Health Sciences (BPKIHS)", "Dharan", "https://www.bpkihs.edu/"),
            ("Patan Academy of Health Sciences (PAHS)", "Lalitpur", "https://web.pahs.edu.np/"),
            ("Pokhara Academy of Health Sciences (PoAHS)", "Pokhara", "https://www.poahs.edu.np/"),
            ("Karnali Academy of Health Sciences (KAHS)", "Jumla", "https://www.kahs.edu.np/"),
        ],
    },
]


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def institution_card(name: str, city: str, country: str, url: str) -> str:
    label = f"Visit the official website for {name}"
    return (
        f'<a class="group block university-official-card" href="{esc(url)}" target="_blank" '
        f'rel="noopener noreferrer" aria-label="{esc(label)}" '
        'style="background:#FFFFFF;border:1px solid #E2E4E8;text-decoration:none;transition:border-color .2s ease,transform .2s ease,box-shadow .2s ease;padding:1.5rem;display:flex;flex-direction:column;gap:1rem;min-height:220px">'
        '<div style="display:flex;justify-content:space-between;align-items:flex-start;gap:1rem">'
        f'<h3 style="font-family:var(--font-display);font-size:clamp(1.05rem,1.5vw,1.25rem);font-weight:700;color:#0D0D0D;line-height:1.25;letter-spacing:-.015em;margin:0">{esc(name)}</h3>'
        '<span style="font-family:var(--font-mono);font-size:.52rem;line-height:1.2;letter-spacing:.1em;text-transform:uppercase;color:#283A27;border:1px solid rgba(40,58,39,.25);padding:.4rem .5rem;white-space:nowrap">Government / Public</span>'
        '</div>'
        f'<p style="font-family:var(--font-mono);font-size:.62rem;letter-spacing:.1em;text-transform:uppercase;color:#6B7280;margin:0">{esc(city)} · {esc(country)}</p>'
        '<div style="height:1px;background:#E8E8E8;margin-top:auto"></div>'
        '<span style="display:flex;align-items:center;justify-content:space-between;gap:.75rem;font-family:var(--font-mono);font-size:.64rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:#283A27">Visit official website'
        '<svg aria-hidden="true" fill="none" height="15" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" viewBox="0 0 24 24" width="15" xmlns="http://www.w3.org/2000/svg"><path d="M15 3h6v6"></path><path d="M10 14 21 3"></path><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path></svg>'
        '</span></a>'
    )


def catalogue_section() -> str:
    groups = []
    for country in COUNTRIES:
        cards = "".join(
            institution_card(name, city, country["name"], url)
            for name, city, url in country["institutions"]
        )
        count = len(country["institutions"])
        groups.append(
            '<div class="mb-14 university-country-group">'
            '<div style="display:flex;align-items:end;justify-content:space-between;gap:1.5rem;flex-wrap:wrap;margin-bottom:1.4rem;padding-bottom:1rem;border-bottom:1px solid #D9D9D4">'
            '<div>'
            f'<span style="font-family:var(--font-mono);font-size:.58rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#6B7280">{count:02d} featured institutions</span>'
            f'<h2 style="font-family:var(--font-display);font-size:clamp(1.8rem,3vw,2.75rem);font-weight:700;color:#322D29;letter-spacing:-.03em;line-height:1.05;margin:.4rem 0 0">{country["flag"]} {esc(country["name"])}</h2>'
            '</div>'
            f'<p style="font-family:var(--font-mono);font-size:.6rem;letter-spacing:.1em;text-transform:uppercase;color:#6B7280;margin:0">{esc(country["network"])} · {esc(country["budget"])}</p>'
            '</div>'
            f'<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">{cards}</div>'
            '</div>'
        )
    return (
        '<section class="section-padding university-catalogue" style="background:#F5F5F2">'
        '<div class="container-custom">'
        '<div style="display:grid;grid-template-columns:minmax(0,1fr) minmax(280px,.65fr);gap:2rem;align-items:end;margin-bottom:4rem">'
        '<div><span class="section-label"><span style="opacity:.35">01</span><span style="opacity:.35">—</span><span>University network</span></span>'
        '<h2 style="font-family:var(--font-display);font-size:clamp(2.4rem,5vw,5rem);font-weight:700;color:#322D29;letter-spacing:-.045em;line-height:.98;margin:.9rem 0 0">34 featured institutions.<br/><em style="font-weight:400">Seven countries.</em></h2></div>'
        '<p style="font-size:1rem;line-height:1.75;color:#6B7280;margin:0">Browse the government and public medical institutions currently featured by Stellar. Our wider consultancy network spans 60+ government institutions across these seven destinations. Use each card to continue directly to the institution’s official website.</p>'
        '</div>'
        + "".join(groups)
        + '</div></section>'
    )


def country_institutions_section(country: dict) -> str:
    cards = "".join(
        institution_card(name, city, country["name"], url)
        for name, city, url in country["institutions"]
    )
    return (
        '<section class="section-padding university-country-directory" style="background:#F5F5F2">'
        '<div class="container-custom">'
        '<div style="display:grid;grid-template-columns:minmax(0,1fr) minmax(280px,.7fr);gap:2rem;align-items:end;margin-bottom:2.5rem">'
        '<div><span class="section-label"><span style="opacity:.35">04</span><span style="opacity:.35">—</span><span>Partner institutions</span></span>'
        f'<h2 style="font-family:var(--font-display);font-size:clamp(2rem,4vw,3.75rem);font-weight:700;color:#322D29;letter-spacing:-.04em;line-height:1;margin:.8rem 0 0">Government medical institutions in {esc(country["name"])}</h2></div>'
        f'<p style="font-size:.95rem;line-height:1.7;color:#6B7280;margin:0">These {len(country["institutions"])} featured institutions are part of Stellar’s broader {esc(country["network"])} network. Open a card to review the institution on its official website.</p>'
        '</div>'
        f'<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">{cards}</div>'
        '</div></section>'
    )


def replace_nth_section(source: str, section_index: int, replacement: str) -> str:
    starts = [match.start() for match in re.finditer(r"<section\b", source, flags=re.I)]
    if section_index >= len(starts):
        raise ValueError(f"Section {section_index} not found; page has {len(starts)} sections")
    start = starts[section_index]
    end = source.find("</section>", start)
    if end < 0:
        raise ValueError("Section closing tag not found")
    end += len("</section>")
    return source[:start] + replacement + source[end:]


def replace_between(source: str, start_marker: str, end_marker: str, replacement: str) -> str:
    start = source.find(start_marker)
    end = source.find(end_marker, start + len(start_marker))
    if start < 0 or end < 0:
        raise ValueError(f"Could not find article markers: {start_marker!r}, {end_marker!r}")
    return source[:start] + replacement + source[end:]


def write_text(path: Path, value: str) -> None:
    path.write_text(value, encoding="utf-8")
    print(f"updated {path.relative_to(ROOT)}")


def update_university_pages() -> None:
    for relative in ("universities.html", "universities/index.html"):
        path = ROOT / relative
        source = path.read_text(encoding="utf-8")
        source = replace_nth_section(source, 1, catalogue_section())
        source = source.replace(">19+</p><p", ">34</p><p", 1)
        source = source.replace(">Universities</p></div><div", ">Featured Institutions</p></div><div", 1)
        source = re.sub(
            r"<title>.*?</title>",
            "<title>Government Medical Universities Abroad — Official Websites | Stellar Science Hub &amp; Educonsultancy</title>",
            source,
            count=1,
        )
        source = re.sub(
            r'<meta content="[^"]*" name="description"/>',
            '<meta content="Browse 34 featured government and public medical institutions across 7 countries, with direct links to every official university website." name="description"/>',
            source,
            count=1,
        )
        write_text(path, source)


def update_country_pages() -> None:
    for country in COUNTRIES:
        for relative in (
            f'countries/{country["slug"]}.html',
            f'countries/{country["slug"]}/index.html',
        ):
            path = ROOT / relative
            source = path.read_text(encoding="utf-8")
            source = replace_nth_section(source, 3, country_institutions_section(country))

            if country["slug"] in {"kazakhstan", "bangladesh", "nepal"}:
                source = source.replace("Al-Farabi: 51% FMGE Rate", "Government Institution Network")
                source = source.replace(
                    "Al-Farabi Kazakh National University (Top 200 globally) achieves ~51% FMGE pass rate — the highest in Kazakhstan and among the best in Central Asia.",
                    f'Stellar’s {country["name"]} counselling network focuses on government and public medical institutions, with official-site verification before application.',
                )
                source = source.replace(
                    "One of the most affordable NMC-approved destinations. Semey and Karaganda start from ₹15L total — among the lowest anywhere.",
                    f'Compare the overall programme and living budget for {country["name"]} during counselling; institution-specific costs are confirmed from current official documents.',
                )

            if country["slug"] in {"bangladesh", "nepal"}:
                name = country["name"]
                source = source.replace("Admission Timeline — Kazakhstan", f"Admission Timeline — {name}")
                source = source.replace("Life in Kazakhstan", f"Life in {name}")
                source = source.replace("FMGE/NExT Preparation from Kazakhstan", f"FMGE/NExT Preparation from {name}")
                source = source.replace("Ready to Study MBBS in Kazakhstan", f"Ready to Study MBBS in {name}")
                source = source.replace(
                    "Kazakhstani Tenge (KZT). Monthly expenses ~₹12,000–₹18,000.",
                    "Plan day-to-day expenses with a current, city-specific estimate during counselling.",
                )
                source = source.replace(
                    "Kazakhstan has the highest FMGE pass rates in Central Asia. Al-Farabi KazNU leads at ~51%, followed by Astana Medical University at ~35.9%. Our team doctors (Dr. Nishu Yadav and Dr. Lokesh Attri) graduated from Semey Medical University and cleared FMGE on their first attempt — proving that consistent preparation from Year 1 is the key, regardless of university.",
                    f"Students returning from {name} must follow the licensing rules applicable in India. Stellar builds exam planning and document checks into counselling from the beginning of the programme.",
                )
            write_text(path, source)


def refresh_country_schema_and_copied_details(only_slugs: set[str] | None = None) -> None:
    """Remove institution-specific FAQ claims and two inherited Kazakhstan blocks."""
    for country in COUNTRIES:
        if only_slugs is not None and country["slug"] not in only_slugs:
            continue
        schema = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": f"Where can I verify current medical institution information for {country['name']}?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "Use the official institution links in the featured university section and confirm current programme, eligibility, recognition, and admission information before payment.",
                    },
                },
                {
                    "@type": "Question",
                    "name": f"How many {country['name']} institutions are featured by Stellar?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": f"The website currently features {len(country['institutions'])} government or public institutions in {country['name']} as part of Stellar's wider consultancy network.",
                    },
                },
            ],
        }
        schema_tag = (
            '<script type="application/ld+json">'
            + json.dumps(schema, ensure_ascii=False, separators=(",", ":"))
            + "</script>"
        )

        for relative in (
            f'countries/{country["slug"]}.html',
            f'countries/{country["slug"]}/index.html',
        ):
            path = ROOT / relative
            source = path.read_text(encoding="utf-8")
            source, count = re.subn(
                r'<script type="application/ld\+json">.*?</script>',
                lambda _: schema_tag,
                source,
                count=1,
                flags=re.S,
            )
            if count != 1:
                raise ValueError(f"Expected one country FAQ schema in {relative}")

            source = source.replace("Tashkent Medical Academy", "Tashkent State Medical University")
            if country["slug"] == "kazakhstan":
                source = source.replace(
                    "Kazakhstan has the highest FMGE pass rates in Central Asia. Al-Farabi KazNU leads at ~51%, followed by Astana Medical University at ~35.9%. Our team doctors (Dr. Nishu Yadav and Dr. Lokesh Attri) graduated from Semey Medical University and cleared FMGE on their first attempt — proving that consistent preparation from Year 1 is the key, regardless of university.",
                    "Licensing outcomes depend on the student, current regulations, and sustained preparation—not a marketing percentage attached to a university. Stellar builds exam planning and document checks into counselling from the beginning of the programme.",
                )
                source = source.replace(
                    "Which Kazakhstan university has the best FMGE rate?",
                    "Where can I verify Kazakhstan institution details?",
                )
                source = source.replace(
                    "Al-Farabi Kazakh National University leads at ~51% FMGE pass rate. Astana Medical University is second at ~35.9%. KazNMU (Asfendiyarov) follows at ~27%. For budget options, Semey and Karaganda are solid at 21–25%.",
                    "Use the official links in the featured institution section and confirm current programme, eligibility, recognition, and admission information before payment.",
                )

            if country["slug"] in {"bangladesh", "nepal"}:
                main_end = source.index("</main>")
                main = source[:main_end]
                footer = source[main_end:]
                main = main.replace("Kazakhstan", country["name"])
                main = main.replace("🇰🇿", country["flag"], 1)
                main = main.replace("Best FMGE Rates in Central Asia", "Government Medical Education Network")
                main = main.replace("Travel to Almaty or Astana", f'Travel to the confirmed campus city in {country["name"]}')
                main = main.replace(
                    "Cold winters: Astana (−20°C to −30°C), Almaty (milder, −10°C to −15°C). Almaty is strongly preferred for climate-sensitive students.",
                    f"Climate and seasonal conditions vary by campus city in {country['name']}; prepare after your destination is confirmed.",
                )
                main = main.replace(
                    "Indian mess available near universities in Almaty and Astana. Indian community growing rapidly.",
                    "Food and accommodation options vary by campus; confirm current hostel and meal arrangements before admission.",
                )
                main = main.replace(
                    "Generally safe. Kazakh people are hospitable. Petty crime low.",
                    "Review current city- and campus-specific safety guidance before travel.",
                )
                main = main.replace(
                    "Modern transport in Almaty and Astana. Metro in Almaty. Affordable taxis everywhere.",
                    "Local transport options depend on the campus city and accommodation location.",
                )
                if country["slug"] == "bangladesh":
                    main = main.replace(">5 years</p>", ">5.5–6 years</p>", 1)
                    main = main.replace(">₹15L – ₹30L</p>", ">₹32L – ₹45L</p>", 1)
                else:
                    main = main.replace(">5 years</p>", ">5.5 years</p>", 1)
                    main = main.replace(">₹15L – ₹30L</p>", ">₹57L – ₹80L</p>", 1)
                source = main + footer

            write_text(path, source)


def update_blog_pages() -> None:
    russia_list = (
        '<h2>Featured Government / Public Institutions</h2>'
        '<p>Stellar’s current featured Russia list is:</p><ul>'
        '<li><a href="https://www.sechenov.ru/eng/" target="_blank" rel="noopener noreferrer"><strong>Sechenov University – First Moscow State Medical University</strong></a> — Moscow</li>'
        '<li><a href="https://pirogov-university.com/" target="_blank" rel="noopener noreferrer"><strong>Pirogov Russian National Research Medical University</strong></a> — Moscow</li>'
        '<li><a href="https://www.en.1spbgmu.ru/" target="_blank" rel="noopener noreferrer"><strong>Pavlov First Saint Petersburg State Medical University</strong></a> — Saint Petersburg</li>'
        '<li><a href="https://kgmu.kcn.ru/" target="_blank" rel="noopener noreferrer"><strong>Kazan State Medical University</strong></a> — Kazan</li>'
        '<li><a href="https://tvgmu.ru/" target="_blank" rel="noopener noreferrer"><strong>Tver State Medical University</strong></a> — Tver</li>'
        '</ul><p>Confirm current programme, eligibility, and recognition information on the linked official websites before applying.</p>'
    )
    georgia_list = (
        '<h2>Featured Government / Public Institutions</h2><ul>'
        '<li><a href="https://tsmu.edu/ts/index.php?lang=en" target="_blank" rel="noopener noreferrer"><strong>Tbilisi State Medical University (TSMU)</strong></a> — Tbilisi</li>'
        '<li><a href="https://tsu.ge/en/programs/434" target="_blank" rel="noopener noreferrer"><strong>Ivane Javakhishvili Tbilisi State University (TSU)</strong></a> — Tbilisi</li>'
        '<li><a href="https://iliauni.edu.ge/en/iliauni/AcademicDepartments/sainjinro-fakulteti-270/programebi-310/medicinis-programa" target="_blank" rel="noopener noreferrer"><strong>Ilia State University</strong></a> — Tbilisi</li>'
        '<li><a href="https://atsu.edu.ge/" target="_blank" rel="noopener noreferrer"><strong>Akaki Tsereteli State University</strong></a> — Kutaisi</li>'
        '<li><a href="https://www.bsu.edu.ge/?lang=en" target="_blank" rel="noopener noreferrer"><strong>Batumi Shota Rustaveli State University</strong></a> — Batumi</li>'
        '</ul><p>Use the official links above to review current programme and admission information.</p>'
    )
    kazakhstan_list = (
        '<h2>Featured Government / Public Institutions</h2><ul>'
        '<li><a href="https://kaznmu.edu.kz/" target="_blank" rel="noopener noreferrer"><strong>Asfendiyarov Kazakh National Medical University (KazNMU)</strong></a> — Almaty</li>'
        '<li><a href="https://amu.edu.kz/" target="_blank" rel="noopener noreferrer"><strong>Medical University Astana</strong></a> — Astana</li>'
        '<li><a href="https://qmu.edu.kz/" target="_blank" rel="noopener noreferrer"><strong>Karaganda Medical University</strong></a> — Karaganda</li>'
        '<li><a href="https://smu.edu.kz/" target="_blank" rel="noopener noreferrer"><strong>Semey Medical University</strong></a> — Semey</li>'
        '<li><a href="https://zkmu.edu.kz/" target="_blank" rel="noopener noreferrer"><strong>West Kazakhstan Marat Ospanov Medical University</strong></a> — Aktobe</li>'
        '</ul><p>Use the official links above to review current programme and admission information.</p>'
    )

    migrations = [
        (
            ["blog/top-nmc-approved-universities-russia.html", "blog/top-nmc-approved-universities-russia/index.html"],
            "<h2>Top Universities (Summary)</h2>",
            "<h2>Important Notes</h2>",
            russia_list,
            [
                ("Planning MBBS in Russia? Here's the definitive list of NMC-approved universities with fees, FMGE pass rates, and what makes each one stand out.", "Planning MBBS in Russia? Review Stellar’s current featured government and public medical institutions, then verify the latest programme information on each official website."),
                ("Climate:</strong> Russian winters are cold (−10°C to −30°C depending on city). Southern cities like Volgograd are warmer.", "Climate:</strong> Russian winters can be severe, and conditions vary considerably by city."),
            ],
        ),
        (
            ["blog/mbbs-in-georgia-complete-guide-2026.html", "blog/mbbs-in-georgia-complete-guide-2026/index.html"],
            "<h2>Top NMC-Approved Universities</h2>",
            "<h2>Fees and Living Costs</h2>",
            georgia_list,
            [],
        ),
        (
            ["blog/mbbs-in-kazakhstan-fees-universities-eligibility.html", "blog/mbbs-in-kazakhstan-fees-universities-eligibility/index.html"],
            "<h2>Top Universities</h2>",
            "<h2>Fee Structure (Approximate)</h2>",
            kazakhstan_list,
            [
                ("MBBS, Al-Farabi Kazakh National University", "MBBS, Kazakhstan"),
            ],
        ),
    ]
    for paths, start, end, block, replacements in migrations:
        for relative in paths:
            path = ROOT / relative
            source = path.read_text(encoding="utf-8")
            if start in source and end in source:
                source = replace_between(source, start, end, block)
            elif '<h2>Featured Government / Public Institutions</h2>' not in source:
                raise ValueError(f"Could not identify the university list in {relative}")
            for old, new in replacements:
                source = source.replace(old, new)
            if "top-nmc-approved-universities-russia" in relative:
                source = source.replace(
                    "Top 10 NMC-Approved Universities in Russia for Indian Students (2026)",
                    "Featured Government Medical Universities in Russia (2026)",
                )
            write_text(path, source)


def refresh_russia_blog_title() -> None:
    for relative in (
        "blog/top-nmc-approved-universities-russia.html",
        "blog/top-nmc-approved-universities-russia/index.html",
    ):
        path = ROOT / relative
        source = path.read_text(encoding="utf-8")
        source = source.replace(
            "Top 10 NMC-Approved Universities in Russia for Indian Students (2026)",
            "Featured Government Medical Universities in Russia (2026)",
        )
        write_text(path, source)


def update_datasets() -> None:
    records = []
    for country in COUNTRIES:
        for name, city, url in country["institutions"]:
            records.append(
                {
                    "name": name,
                    "city": city,
                    "country": country["name"],
                    "institution_type": "Government / Public",
                    "official_url": url,
                }
            )
    write_text(
        ROOT / "data/universities_structured.json",
        json.dumps(records, ensure_ascii=False, indent=2) + "\n",
    )

    country_records = [
        {
            "slug": country["slug"],
            "name": country["name"],
            "government_institute_network": country["network"],
            "budget_range": country["budget"],
            "featured_institutions": [name for name, _, _ in country["institutions"]],
        }
        for country in COUNTRIES
    ]
    write_text(
        ROOT / "data/countries_structured.json",
        json.dumps(country_records, ensure_ascii=False, indent=2) + "\n",
    )

    lines = [
        "# Featured Government / Public Medical Institutions",
        "",
        "- **URL:** https://stellarsciencehub.in/universities",
        "- **Scope:** 34 featured institutions across 7 countries",
        "- **Network:** 60+ government institutions overall",
        "- **Link policy:** Institution cards open official websites directly",
        "",
    ]
    for country in COUNTRIES:
        lines.extend([f'## {country["name"]}', ""])
        for name, city, url in country["institutions"]:
            lines.append(f"- [{name}]({url}) — {city}")
        lines.append("")
    write_text(ROOT / "data/core/universities_index.md", "\n".join(lines))

    countries_dir = ROOT / "data/countries"
    for old in countries_dir.glob("*.md"):
        old.unlink()
    for country in COUNTRIES:
        body = [
            f'# MBBS in {country["name"]}',
            "",
            f'- **URL:** https://stellarsciencehub.in/countries/{country["slug"]}',
            f'- **Government network:** {country["network"]}',
            f'- **Indicative country budget:** {country["budget"]}',
            "",
            "## Featured Institutions",
            "",
        ]
        body.extend(
            f"- [{name}]({url}) — {city}" for name, city, url in country["institutions"]
        )
        body.extend(["", "> Always confirm current programme, eligibility, recognition, and admission information on the institution’s official website.", ""])
        write_text(countries_dir / f'{country["slug"]}.md', "\n".join(body))


def remove_retired_routes_and_records() -> None:
    universities_root = (ROOT / "universities").resolve()
    for page in universities_root.glob("*.html"):
        if page.name != "index.html":
            page.unlink()
            print(f"removed {page.relative_to(ROOT)}")
    for child in universities_root.iterdir():
        if child.is_dir():
            index = child / "index.html"
            if index.exists():
                index.unlink()
                print(f"removed {index.relative_to(ROOT)}")
            if not any(child.iterdir()):
                child.rmdir()

    countries_root = (ROOT / "countries").resolve()
    for slug in ("philippines", "serbia"):
        page = countries_root / f"{slug}.html"
        nested = countries_root / slug / "index.html"
        for target in (page, nested):
            if target.exists():
                target.unlink()
                print(f"removed {target.relative_to(ROOT)}")
        folder = countries_root / slug
        if folder.exists() and not any(folder.iterdir()):
            folder.rmdir()

    university_data = ROOT / "data/universities"
    for record in university_data.glob("*.md"):
        record.unlink()
        print(f"removed {record.relative_to(ROOT)}")


def update_readme_and_verifier() -> None:
    readme = ROOT / "README.md"
    source = readme.read_text(encoding="utf-8")
    source = source.replace(
        "Featuring 7 country destinations, 19 NMC-approved medical universities, admissions guides,",
        "Featuring 7 country destinations, 34 featured government/public medical institutions with official-site links, admissions guides,",
    )
    source = source.replace(
        "48 exact clean routes across core pages, 7 country destinations, 19 university profiles, and 10 detailed medical guides.",
        "29 verified clean routes across core pages, 7 country destinations, and 10 detailed medical guides; individual university cards link to official institution websites.",
    )
    source = source.replace("To verify all 48 clean routes", "To verify all 29 clean routes")
    source = source.replace("├── countries/                   # 7 Country guides (/countries/...)", "├── countries/                   # 7 approved country guides (/countries/...)")
    source = source.replace("├── universities/                # 19 Medical university profiles (/universities/...)", "├── universities/                # University directory only; cards open official websites")
    write_text(readme, source)

    verifier = ROOT / "scripts/verify_routes.py"
    source = verifier.read_text(encoding="utf-8")
    start = source.index("ROUTES = [")
    end = source.index("\n]\n\nBASE_URL", start) + 2
    routes = [
        "/", "/countries", "/universities", "/process", "/eligibility", "/blog",
        "/faq", "/about", "/book", "/contact", "/privacy", "/disclaimer",
        "/countries/uzbekistan", "/countries/kyrgyzstan", "/countries/kazakhstan",
        "/countries/russia", "/countries/bangladesh", "/countries/georgia", "/countries/nepal",
        "/blog/mbbs-abroad-vs-private-medical-college-india-2026",
        "/blog/top-nmc-approved-universities-russia",
        "/blog/fmge-exam-what-it-is-how-to-prepare",
        "/blog/mbbs-in-georgia-complete-guide-2026",
        "/blog/mbbs-in-kazakhstan-fees-universities-eligibility",
        "/blog/how-to-get-nmc-eligibility-certificate",
        "/blog/life-as-indian-student-in-russia",
        "/blog/neet-score-required-for-mbbs-abroad",
        "/blog/mbbs-abroad-document-checklist",
        "/blog/why-fmge-pass-rate-matters-choosing-university",
    ]
    route_block = "ROUTES = [\n" + "".join(f'    "{route}",\n' for route in routes) + "]"
    source = source[:start] + route_block + source[end:]
    write_text(verifier, source)


def main() -> None:
    assert len(COUNTRIES) == 7
    assert sum(len(country["institutions"]) for country in COUNTRIES) == 34
    update_university_pages()
    update_country_pages()
    refresh_country_schema_and_copied_details()
    update_blog_pages()
    refresh_russia_blog_title()
    update_datasets()
    remove_retired_routes_and_records()
    update_readme_and_verifier()
    print("University catalogue migration complete: 7 countries, 34 featured institutions.")


if __name__ == "__main__":
    main()
