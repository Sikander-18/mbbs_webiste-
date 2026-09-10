# Stellar Science Hub & Educonsultancy — MBBS Abroad Platform

A high-performance, responsive multi-page web platform for **Stellar Science Hub & Educonsultancy** — a doctor-led overseas medical education advisory based in Mira Road, Mumbai.

Featuring 7 country destinations, 34 featured government/public medical institutions with official-site links, admissions guides, an interactive budget calculator, and custom motion choreography inspired by **[Forge Automotive](https://forgeautomotive.co.uk/)**.

---

## Key Features

1. **Forge Automotive-Style Signature Animations**:
   - **University Gate Entrance Hero**: 3D perspective campus entrance with wrought-iron gate doors that swing open on scroll as the camera moves into the campus facade.
   - **Atmospheric Thesis Quote**: High-impact editorial statement screen: *"We Don't Just Process Admissions. We Build Future Doctors."*
   - **3D Medical Compendium / Book Opening**: Perspective journal revealing the founding standard and the 4 core pillars of NMC compliance.
   - **Pinned Split Country Explorer**: 50/50 sticky screen layout with live crossfading destination specs across Russia, Georgia, Kazakhstan, and Uzbekistan.
   - **Staged Doctor Counselors Showcase**: Interactive doctor counselor portfolio with credentials, FMGE scores, bios, and direct WhatsApp consultations.
2. **Interactive MBBS Budget Calculator**: Real-time slider (₹15L - ₹45L+) providing tuition fees, hostel costs, duration, and matching NMC-approved universities with direct WhatsApp pre-filled inquiry.
3. **Verified Real Photo Gallery**: Lightbox modal showcasing real campus photos and student batches.
4. **Complete Admissions Infrastructure**:
   - 29 verified clean routes across core pages, 7 country destinations, and 10 detailed medical guides; individual university cards link to official institution websites.
   - 100% NMC Gazette and WDOMS directory compliant.
   - Direct counselor WhatsApp integration (`+91 90047 75531`).

---

## Quick Start

### 1. Run the Local Development Server
Launch the multi-threaded Python preview server with clean URL handling and custom 404 routing:

```bash
python server.py
```
*Or using npm:*
```bash
npm run dev
```

Visit the website at: **`http://localhost:3000`**

### 2. Static Preview (`npx serve`)
```bash
npm run serve
```

### 3. Run Route & Concurrency Verification
To verify all 29 clean routes and status codes:
```bash
npm test
```
*Or directly:*
```bash
python scripts/verify_routes.py
```

---

## Project Structure

```
.
├── index.html                   # Homepage with Forge Automotive motion architecture
├── 404.html                     # Branded 404 Page Not Found
│
├── about/                       # About Us (/about)
├── blog/                        # 10 Medical advisory articles (/blog/...)
├── book/                        # 1-on-1 Doctor Call Booking (/book)
├── contact/                     # Contact & Location with Google Map (/contact)
├── countries/                   # 7 approved country guides (/countries/...)
├── eligibility/                 # NMC Eligibility regulations (/eligibility)
├── faq/                         # Comprehensive FAQ directory (/faq)
├── process/                     # 6-Step Admission Journey (/process)
├── universities/                # University directory only; cards open official websites
│
├── assets/
│   ├── css/
│   │   └── style.css            # Consolidated design system tokens, 3D perspective & styles
│   ├── js/
│   │   └── main.js              # Motion engine, gate entrance, pinned explorer & tab controllers
│   └── images/                  # Doctor portraits, campus gates, and university media
│
├── data/                        # Structured content datasets
├── scripts/
│   ├── apply_forge_experience.py # Automated animation builder script
│   ├── install_animations.py     # Base animation installer
│   ├── update_branding_and_purge.py # Branding & purge utility
│   └── verify_routes.py          # 48-route test suite
├── server.py                    # Multi-threaded clean URL development server
├── package.json
└── README.md
```

---

## License & Credits
- **Client**: Stellar Science Hub & Educonsultancy
- **Lead Counselors**: Dr. Nishu Yadav, Dr. Lokesh Attri, Dr. Bindu Tyagi
- **Website**: [stellarsciencehub.in](https://stellarsciencehub.in)
