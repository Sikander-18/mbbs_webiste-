# Stellar Science Hub & Educonsultancy — MBBS Abroad Website

Production-ready static website for **Stellar Science Hub & Educonsultancy**, an MBBS-abroad education consultancy based in Mira Road, Mumbai.

The site includes a cinematic landing page, country guides, a university directory with official outbound links, admissions-process information, eligibility guidance, FAQs, booking/contact pages, and documentation for the animation references used during design.

## Key features

- **Cinematic homepage animation system**
  - Scroll-driven university gate entrance hero.
  - Campus quote transition.
  - 3D medical compendium/book section.
  - Pinned country explorer.
  - Doctor guidance showcase.
- **Country coverage**
  - Russia, Georgia, Kazakhstan, Uzbekistan, Kyrgyzstan, Bangladesh, and Nepal.
- **University directory**
  - Cards link directly to the official university websites.
  - Old individual university detail routes are not part of the current production site.
- **Conversion paths**
  - WhatsApp booking links.
  - Consultation CTAs.
  - Contact/location page.
- **Static route support**
  - Root `.html` files and matching `folder/index.html` files are intentionally kept so both direct-file and clean URLs work across local/dev hosting setups.

## Quick start

Run the local clean-URL development server:

```bash
python server.py
```

Or:

```bash
npm run dev
```

Visit:

```text
http://localhost:3000
```

## Verification

Run the route verification suite:

```bash
npm test
```

The test checks the 19 supported clean routes, including the branded 404 behavior for `/privacy` and `/disclaimer`.

There is currently no separate production build, lint, or type-check script because this project is a static HTML/CSS/JS site.

## Project structure

```text
.
├── index.html                  # Homepage with the main scroll animation sequence
├── 404.html                    # Branded 404 page
├── about.html / about/         # About route, direct and clean URL variants
├── blog.html / blog/           # Blog landing route
├── book.html / book/           # Consultation booking route
├── contact.html / contact/     # Contact route
├── countries.html / countries/ # Country index and 7 country detail routes
├── eligibility.html / eligibility/
├── faq.html / faq/
├── gallery.html / gallery/
├── process.html / process/
├── universities.html / universities/
├── assets/
│   ├── css/style.css           # Site design system, layout, responsive rules, animation styling
│   ├── js/main.js              # Site interactions and GSAP/ScrollTrigger animation logic
│   ├── js/vendor/              # Local GSAP vendor files
│   └── images/                 # Runtime image assets used by the website
├── images/                     # Compatibility logo assets used by `_next/image` metadata redirects
├── _next/static/media/         # Font assets referenced by exported HTML
├── docs/animation-references/  # Reference reports from Forge Automotive and Peryton Film
├── scripts/verify_routes.py    # Clean-route verification script
├── server.py                   # Local preview server with clean URL and `_next/image` handling
├── serve.json                  # Static-hosting preview config
└── package.json
```

## Notes for maintainers

- Keep `assets/js/main.js` and the animation-related CSS changes deliberate; the homepage book, country, and doctor sequences rely on coordinated GSAP timelines.
- Keep both route forms (`about.html` and `about/index.html`, etc.) unless the server and tests are changed together.
- Keep root `images/logo_512.png`; exported `_next/image` metadata URLs are routed to it by `server.py`.
