import os
import re
from bs4 import BeautifulSoup

def apply_forge_experience():
    # 1. Update style.css with Forge-style animations if not already present
    with open('assets/css/style.css', 'r', encoding='utf-8') as f:
        css = f.read()

    forge_css = '''
/* ========================================================
   FORGE AUTOMOTIVE HOMEPAGE MOTION STYLES
   ======================================================== */

@keyframes mouseScroll {
    0% { transform: translateY(0); opacity: 1; }
    100% { transform: translateY(12px); opacity: 0; }
}

/* Gate Entrance Perspective */
.gate-hero-pinned {
    perspective: 1200px;
}

#gate-door-left, #gate-door-right {
    transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.2s ease;
}

#campus-facade {
    transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

/* 3D Medical Book Opening */
.medical-book-wrap {
    transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.6s ease;
    transform-style: preserve-3d;
}

.medical-book-wrap:hover {
    transform: translateY(-5px) rotateX(2deg);
    box-shadow: 0 35px 80px rgba(0,0,0,0.7), 0 0 50px rgba(0,197,163,0.25);
}

/* Pinned Country Explorer */
@media (max-width: 1023px) {
    .pinned-countries-sticky {
        position: relative !important;
        height: auto !important;
        flex-direction: column !important;
    }
    .pinned-country-left, .pinned-country-right {
        width: 100% !important;
    }
    .pinned-country-right {
        height: 380px !important;
    }
    .pinned-countries-track {
        min-height: auto !important;
    }
}
'''

    if 'FORGE AUTOMOTIVE HOMEPAGE MOTION STYLES' not in css:
        with open('assets/css/style.css', 'a', encoding='utf-8') as f:
            f.write(forge_css)
        print("assets/css/style.css updated with Forge styles.")

    # 2. Build the new homepage HTML sections
    hero_and_quote_and_book = '''
<!-- STAGE 1: University Gate & College Entrance (Forge Hero Benchmark) -->
<section id="gate-hero-section" class="gate-hero-pinned" style="position:relative;min-height:180vh;background:#040711;">
  <div id="gate-sticky-frame" style="position:sticky;top:0;height:100vh;width:100%;overflow:hidden;display:flex;align-items:center;justify-content:center;">
    <div id="campus-facade" style="position:absolute;inset:0;background-image:url('/assets/images/campus_entrance.png');background-size:cover;background-position:center;will-change:transform;transform-origin:center 60%;">
      <div style="position:absolute;inset:0;background:radial-gradient(circle at center, rgba(4,7,17,0.15) 0%, rgba(4,7,17,0.65) 70%, rgba(4,7,17,0.95) 100%);"></div>
    </div>

    <div id="gate-doors-wrap" style="position:absolute;inset:0;pointer-events:none;display:flex;perspective:1200px;z-index:20;">
      <div id="gate-door-left" style="width:50%;height:100%;background:linear-gradient(to right, rgba(5,8,16,0.96) 0%, rgba(8,12,24,0.85) 85%, rgba(0,197,163,0.3) 100%);border-right:3px solid #00C5A3;transform-origin:left center;will-change:transform,opacity;position:relative;display:flex;align-items:center;justify-content:flex-end;">
        <svg viewBox="0 0 400 800" style="height:85%;opacity:0.38;position:absolute;right:0;" fill="none" stroke="#00C5A3" stroke-width="2">
          <path d="M400,50 C250,50 150,150 150,300 L150,750 M400,120 C280,120 200,200 200,320 L200,750 M400,200 C320,200 250,260 250,350 L250,750"/>
          <circle cx="280" cy="200" r="15" fill="none"/>
          <circle cx="340" cy="140" r="15" fill="none"/>
          <line x1="50" y1="400" x2="400" y2="400"/>
          <line x1="50" y1="600" x2="400" y2="600"/>
          <line x1="100" y1="100" x2="100" y2="750"/>
        </svg>
        <div style="margin-right:24px;width:68px;height:68px;border-radius:50%;border:2px solid #00C5A3;display:flex;align-items:center;justify-content:center;background:rgba(0,197,163,0.12);backdrop-filter:blur(6px);box-shadow:0 0 25px rgba(0,197,163,0.3);">
          <span style="font-family:var(--font-mono);font-size:0.75rem;font-weight:700;color:#00C5A3;letter-spacing:0.1em;">STELLAR</span>
        </div>
      </div>

      <div id="gate-door-right" style="width:50%;height:100%;background:linear-gradient(to left, rgba(5,8,16,0.96) 0%, rgba(8,12,24,0.85) 85%, rgba(0,197,163,0.3) 100%);border-left:3px solid #00C5A3;transform-origin:right center;will-change:transform,opacity;position:relative;display:flex;align-items:center;justify-content:flex-start;">
        <svg viewBox="0 0 400 800" style="height:85%;opacity:0.38;position:absolute;left:0;transform:scaleX(-1);" fill="none" stroke="#00C5A3" stroke-width="2">
          <path d="M400,50 C250,50 150,150 150,300 L150,750 M400,120 C280,120 200,200 200,320 L200,750 M400,200 C320,200 250,260 250,350 L250,750"/>
          <circle cx="280" cy="200" r="15" fill="none"/>
          <circle cx="340" cy="140" r="15" fill="none"/>
          <line x1="50" y1="400" x2="400" y2="400"/>
          <line x1="50" y1="600" x2="400" y2="600"/>
          <line x1="100" y1="100" x2="100" y2="750"/>
        </svg>
        <div style="margin-left:24px;width:68px;height:68px;border-radius:50%;border:2px solid #00C5A3;display:flex;align-items:center;justify-content:center;background:rgba(0,197,163,0.12);backdrop-filter:blur(6px);box-shadow:0 0 25px rgba(0,197,163,0.3);">
          <span style="font-family:var(--font-mono);font-size:0.75rem;font-weight:700;color:#00C5A3;letter-spacing:0.1em;">ACADEMY</span>
        </div>
      </div>
    </div>

    <div id="hero-entrance-content" style="position:relative;z-index:25;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:5rem 1.5rem 3rem;max-width:960px;transition:opacity 0.3s ease, transform 0.3s ease;">
      <div style="display:inline-flex;align-items:center;gap:10px;padding:6px 16px;background:rgba(0,197,163,0.12);border:1px solid rgba(0,197,163,0.35);border-radius:30px;margin-bottom:1.75rem;backdrop-filter:blur(8px);">
        <span style="width:7px;height:7px;border-radius:50%;background:#00C5A3;box-shadow:0 0 10px #00C5A3;"></span>
        <span style="font-family:var(--font-mono);font-size:0.62rem;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:#00C5A3;">NMC Compliant Admissions 2026</span>
      </div>

      <h1 style="font-family:var(--font-display);font-size:clamp(2.75rem, 6.5vw, 5.5rem);line-height:0.95;letter-spacing:-0.03em;color:#FFFFFF;margin:0 0 1.25rem;max-width:960px;">
        For the Doctors. <br>
        <span style="color:#00C5A3;font-style:italic;">By the Doctors.</span>
      </h1>

      <p style="color:rgba(255,255,255,0.75);font-size:clamp(0.95rem, 1.3vw, 1.15rem);max-width:560px;line-height:1.75;margin:0 auto 2.5rem;font-family:var(--font-inter);">
        Doctor-led guidance for NMC-approved medical academies across Russia, Georgia, Kazakhstan & Uzbekistan. Free consultation.
      </p>

      <div style="display:flex;flex-wrap:wrap;gap:1rem;justify-content:center;margin-bottom:3rem;">
        <a href="https://wa.me/919004775531?text=Hi%20Stellar%20Science%20Hub,%20I%20want%20to%20consult%20with%20a%20doctor%20regarding%20MBBS%20Abroad." target="_blank" rel="noopener noreferrer" class="btn-surgical btn-magnetic" style="display:inline-flex;align-items:center;gap:10px;padding:14px 28px;font-size:0.75rem;">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-phone"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
          Talk to a Doctor Counselor
        </a>
        <a href="#budget-calculator" class="btn-outline-white btn-magnetic" style="display:inline-flex;align-items:center;gap:10px;padding:14px 28px;font-size:0.75rem;">
          Calculate Your Budget ↓
        </a>
      </div>

      <div style="display:flex;gap:0.75rem;flex-wrap:wrap;justify-content:center;">
        <span style="font-family:var(--font-mono);font-size:0.53rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:#00C5A3;border:1px solid rgba(0,197,163,0.3);padding:4px 10px;background:rgba(0,0,0,0.4);">NMC Approved ✓</span>
        <span style="font-family:var(--font-mono);font-size:0.53rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:#00C5A3;border:1px solid rgba(0,197,163,0.3);padding:4px 10px;background:rgba(0,0,0,0.4);">WDOMS Listed ✓</span>
        <span style="font-family:var(--font-mono);font-size:0.53rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:#00C5A3;border:1px solid rgba(0,197,163,0.3);padding:4px 10px;background:rgba(0,0,0,0.4);">Doctor-Led ✓</span>
        <span style="font-family:var(--font-mono);font-size:0.53rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:#00C5A3;border:1px solid rgba(0,197,163,0.3);padding:4px 10px;background:rgba(0,0,0,0.4);">Zero Capitation ✓</span>
      </div>

      <div style="margin-top:2.5rem;display:flex;flex-direction:column;align-items:center;gap:6px;opacity:0.8;">
        <span style="font-family:var(--font-mono);font-size:0.52rem;letter-spacing:0.2em;text-transform:uppercase;color:white;">Scroll To Open Gate &bull; Enter Campus</span>
        <div style="width:18px;height:28px;border:2px solid rgba(0,197,163,0.6);border-radius:12px;display:flex;justify-content:center;padding-top:4px;">
          <div style="width:3px;height:6px;background:#00C5A3;border-radius:2px;animation:mouseScroll 1.5s infinite;"></div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- STAGE 2: Atmospheric Thesis Quote Screen (Forge Image 2 Style) -->
<section id="thesis-quote-section" style="background:#060911;min-height:85vh;display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden;border-bottom:1px solid rgba(255,255,255,0.06);padding:5rem 1.5rem;">
  <div style="position:absolute;inset:0;background:radial-gradient(circle at 50% 50%, rgba(0,197,163,0.08) 0%, transparent 70%);pointer-events:none;"></div>
  <div class="container-custom" style="position:relative;z-index:5;text-align:center;max-width:960px;">
    <div style="width:64px;height:64px;margin:0 auto 2.5rem;border-radius:50%;background:rgba(0,197,163,0.08);border:1px solid rgba(0,197,163,0.3);display:flex;align-items:center;justify-content:center;box-shadow:0 0 25px rgba(0,197,163,0.15);">
      <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#00C5A3" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 2v20M8 5c1 0 2 1 2 3s-1 3-2 3c-1 0-2-1-2-3s1-3 2-3zM16 5c-1 0-2 1-2 3s1 3 2 3c1 0 2-1 2-3s-1-3-2-3zM6 13c1.5 0 3 1.5 3 3.5S7.5 20 6 20s-3-1.5-3-3.5S4.5 13 6 13zM18 13c-1.5 0-3 1.5-3 3.5S16.5 20 18 20s3-1.5 3-3.5S19.5 13 18 13z"/>
      </svg>
    </div>

    <h2 style="font-family:var(--font-display);font-size:clamp(2.5rem, 5.5vw, 4.5rem);line-height:1.02;letter-spacing:-0.035em;color:#FFFFFF;margin-bottom:2rem;">
      We Don't Just Process Admissions.<br>
      <span style="color:#00C5A3;font-style:italic;">We Build Future Doctors.</span>
    </h2>

    <div style="width:60px;height:2px;background:linear-gradient(to right, transparent, #00C5A3, transparent);margin:0 auto 2rem;"></div>

    <p style="font-family:var(--font-mono);font-size:clamp(0.68rem, 1.1vw, 0.82rem);font-weight:700;letter-spacing:0.2em;text-transform:uppercase;color:rgba(255,255,255,0.6);margin:0 auto;max-width:640px;line-height:1.8;">
      Doctor-Led Guidance &bull; 100% NMC Gazette Compliant &bull; Zero Capitation Fees
    </p>
  </div>
</section>

<!-- STAGE 3: "01 Why Stellar Science Hub" — 3D Book Opening Animation -->
<section id="why-stellar-book-section" style="background:#090E1A;padding:clamp(5rem, 8vw, 7rem) 0;border-bottom:1px solid rgba(255,255,255,0.06);position:relative;overflow:hidden;">
  <div class="container-custom">
    <div style="display:flex;align-items:flex-end;justify-content:space-between;flex-wrap:wrap;gap:1.5rem;margin-bottom:3.5rem;padding-bottom:1.5rem;border-bottom:1px solid rgba(255,255,255,0.08);">
      <div>
        <p style="font-family:var(--font-mono);font-size:0.58rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:#00C5A3;margin-bottom:0.75rem;display:flex;align-items:center;gap:0.75rem;">
          <span style="opacity:0.4;">01</span><span style="opacity:0.4;">—</span><span>Why Stellar Science Hub & Educonsultancy</span>
        </p>
        <h2 style="font-family:var(--font-display);font-size:clamp(2.25rem, 4.5vw, 3.75rem);line-height:1;letter-spacing:-0.03em;color:#FFFFFF;">
          The Doctor-Led <em style="font-style:italic;color:#00C5A3;">Compendium</em>
        </h2>
      </div>
      <p style="color:rgba(255,255,255,0.6);font-size:0.875rem;max-width:420px;line-height:1.7;border-left:2px solid #00C5A3;padding-left:1.25rem;">
        Inside the walls of medical school, decisions are critical. Here is our ethical charter for every aspiring medical student.
      </p>
    </div>

    <div class="book-3d-scene" style="perspective:1600px;display:flex;justify-content:center;align-items:center;margin:2rem 0;">
      <div id="medical-book" class="medical-book-wrap" style="width:100%;max-width:1100px;background:#FFFFFF;border-radius:8px;box-shadow:0 30px 70px rgba(0,0,0,0.6), 0 0 40px rgba(0,197,163,0.15);overflow:hidden;border:1px solid rgba(255,255,255,0.2);display:grid;grid-template-columns:1fr;position:relative;">
        <div class="grid grid-cols-1 md:grid-cols-2" style="min-height:500px;">
          <div style="background:#FAFBFD;padding:clamp(2rem, 4vw, 3.5rem);border-right:1px solid #E2E8F0;display:flex;flex-direction:column;justify-content:space-between;position:relative;">
            <div>
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:2rem;padding-bottom:0.75rem;border-bottom:1px solid #E2E8F0;">
                <span style="font-family:var(--font-mono);font-size:0.55rem;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:#00C5A3;">CHAPTER 01 &bull; THE STANDARD</span>
                <span style="font-family:var(--font-mono);font-size:0.55rem;color:#94A3B8;">PAGE 04</span>
              </div>
              <h3 style="font-family:var(--font-display);font-size:clamp(1.5rem, 2.4vw, 2.25rem);line-height:1.1;color:#003366;letter-spacing:-0.02em;margin-bottom:1.25rem;">
                Counselors who have <em style="font-style:italic;color:#00C5A3;">walked these exact halls.</em>
              </h3>
              <p style="font-family:var(--font-inter);font-size:0.92rem;line-height:1.8;color:#475569;margin-bottom:1.5rem;">
                Most overseas consultancies are commercial booking agents who have never stepped foot into a foreign dissection hall or hospital ward. Every counselor at Stellar holds an active foreign medical MBBS degree and has successfully cleared the FMGE licensing exam.
              </p>
            </div>
            <div style="display:flex;gap:8px;flex-wrap:wrap;padding-top:1.25rem;border-top:1px dashed #CBD5E1;">
              <span style="font-family:var(--font-mono);font-size:0.55rem;font-weight:700;background:#E6FAF6;color:#00856E;padding:5px 10px;border-radius:4px;">NMC GAZETTE COMPLIANT</span>
              <span style="font-family:var(--font-mono);font-size:0.55rem;font-weight:700;background:#EBF3FA;color:#003366;padding:5px 10px;border-radius:4px;">WDOMS DIRECTORY LISTED</span>
            </div>
          </div>

          <div style="background:#FFFFFF;padding:clamp(2rem, 4vw, 3.5rem);display:flex;flex-direction:column;justify-content:space-between;">
            <div>
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1.5rem;padding-bottom:0.75rem;border-bottom:1px solid #E2E8F0;">
                <span style="font-family:var(--font-mono);font-size:0.55rem;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:#00C5A3;">CHAPTER 02 &bull; THE 4 PILLARS</span>
                <span style="font-family:var(--font-mono);font-size:0.55rem;color:#94A3B8;">PAGE 05</span>
              </div>
              
              <div style="display:flex;flex-direction:column;gap:1.25rem;">
                <div style="display:flex;gap:14px;align-items:flex-start;">
                  <span style="font-family:var(--font-mono);font-size:0.68rem;font-weight:700;color:#00C5A3;background:#E6FAF6;width:24px;height:24px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;">01</span>
                  <div>
                    <h4 style="font-family:var(--font-display);font-size:1.05rem;color:#0F172A;margin:0 0 3px;">Full Practice Rights in India</h4>
                    <p style="font-size:0.8rem;color:#64748B;line-height:1.5;margin:0;">54+ months curriculum in English + 12 months clinical internship satisfying all NMC rules.</p>
                  </div>
                </div>

                <div style="display:flex;gap:14px;align-items:flex-start;">
                  <span style="font-family:var(--font-mono);font-size:0.68rem;font-weight:700;color:#00C5A3;background:#E6FAF6;width:24px;height:24px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;">02</span>
                  <div>
                    <h4 style="font-family:var(--font-display);font-size:1.05rem;color:#0F172A;margin:0 0 3px;">Direct University Alliances</h4>
                    <p style="font-size:0.8rem;color:#64748B;line-height:1.5;margin:0;">Zero middleman fees. Direct university application letters and transparent official fee accounts.</p>
                  </div>
                </div>

                <div style="display:flex;gap:14px;align-items:flex-start;">
                  <span style="font-family:var(--font-mono);font-size:0.68rem;font-weight:700;color:#00C5A3;background:#E6FAF6;width:24px;height:24px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;">03</span>
                  <div>
                    <h4 style="font-family:var(--font-display);font-size:1.05rem;color:#0F172A;margin:0 0 3px;">FMGE Roadmap from Day One</h4>
                    <p style="font-size:0.8rem;color:#64748B;line-height:1.5;margin:0;">We give you year-wise coaching materials and test series before you board your flight.</p>
                  </div>
                </div>

                <div style="display:flex;gap:14px;align-items:flex-start;">
                  <span style="font-family:var(--font-mono);font-size:0.68rem;font-weight:700;color:#00C5A3;background:#E6FAF6;width:24px;height:24px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;">04</span>
                  <div>
                    <h4 style="font-family:var(--font-display);font-size:1.05rem;color:#0F172A;margin:0 0 3px;">On-Ground Campus Support</h4>
                    <p style="font-size:0.8rem;color:#64748B;line-height:1.5;margin:0;">Indian mess food, separate girls/boys hostel assistance, airport pickup, and local SIM setup.</p>
                  </div>
                </div>
              </div>
            </div>

            <div style="padding-top:1.5rem;display:flex;justify-content:flex-end;">
              <a href="/about" class="btn-outline" style="font-size:0.65rem;padding:8px 18px;">Read Full Founding Story &rarr;</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
'''

    pinned_countries_html = '''
<!-- STAGE 4: Pinned Split Countries Explorer (Forge Image 3 - Wheels Style) -->
<section id="pinned-countries-section" style="background:#0D111A;position:relative;border-bottom:1px solid rgba(255,255,255,0.08);">
  <div class="pinned-countries-track" style="min-height:300vh;position:relative;">
    <div class="pinned-countries-sticky" style="position:sticky;top:72px;height:calc(100vh - 72px);overflow:hidden;display:flex;align-items:stretch;">
      <div class="pinned-country-left" style="width:50%;background:#0A0E17;border-right:1px solid rgba(255,255,255,0.08);padding:clamp(2rem, 5vw, 4.5rem);display:flex;flex-direction:column;justify-content:center;position:relative;z-index:10;">
        <div id="country-dynamic-content">
          <p id="country-index" style="font-family:var(--font-mono);font-size:0.62rem;font-weight:700;letter-spacing:0.2em;text-transform:uppercase;color:#00C5A3;margin-bottom:1.5rem;">
            DESTINATION 01 / 04
          </p>
          <h2 id="country-title" style="font-family:var(--font-display);font-size:clamp(2.75rem, 5vw, 4.5rem);line-height:1;letter-spacing:-0.03em;color:#FFFFFF;margin-bottom:1.25rem;">
            Russia
          </h2>
          <p id="country-desc" style="color:rgba(255,255,255,0.65);font-size:clamp(0.95rem, 1.2vw, 1.0625rem);line-height:1.75;max-width:480px;margin-bottom:2rem;font-family:var(--font-inter);">
            World-renowned government medical academies with 200+ years of history, English-medium curriculum, high FMGE pass rates, and subsidized tuition fees.
          </p>
          
          <div id="country-specs" style="display:flex;flex-direction:column;gap:0.75rem;margin-bottom:2.5rem;padding:1.25rem;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:6px;max-width:460px;">
            <div style="display:flex;justify-content:space-between;border-bottom:1px solid rgba(255,255,255,0.06);padding-bottom:0.4rem;">
              <span style="font-family:var(--font-mono);font-size:0.6rem;color:#94A3B8;text-transform:uppercase;">Estimated Budget:</span>
              <span id="country-spec-budget" style="font-family:var(--font-mono);font-size:0.72rem;font-weight:700;color:#00C5A3;">₹20L – ₹35L (Total 6-Yr)</span>
            </div>
            <div style="display:flex;justify-content:space-between;border-bottom:1px solid rgba(255,255,255,0.06);padding-bottom:0.4rem;">
              <span style="font-family:var(--font-mono);font-size:0.6rem;color:#94A3B8;text-transform:uppercase;">Duration:</span>
              <span id="country-spec-duration" style="font-family:var(--font-mono);font-size:0.72rem;font-weight:700;color:white;">5.8 Years with Internship</span>
            </div>
            <div style="display:flex;justify-content:space-between;">
              <span style="font-family:var(--font-mono);font-size:0.6rem;color:#94A3B8;text-transform:uppercase;">NMC Recognition:</span>
              <span id="country-spec-recog" style="font-family:var(--font-mono);font-size:0.72rem;font-weight:700;color:#00C5A3;">100% Compliant</span>
            </div>
          </div>

          <div id="country-cta-container">
            <a id="country-cta-btn" href="/countries/russia" class="btn-surgical btn-magnetic" style="display:inline-flex;align-items:center;gap:10px;padding:12px 26px;font-size:0.7rem;">
              Explore Russia Universities &rarr;
            </a>
          </div>
        </div>
      </div>

      <div class="pinned-country-right" style="width:50%;position:relative;overflow:hidden;background:#050811;">
        <div id="country-img-container" style="position:absolute;inset:0;">
          <img id="country-img" src="https://images.unsplash.com/photo-1513326738677-b964603b136d?w=1200&q=85" alt="MBBS in Russia" style="width:100%;height:100%;object-fit:cover;transition:opacity 0.5s ease, transform 0.8s cubic-bezier(0.16,1,0.3,1);"/>
          <div style="position:absolute;inset:0;background:linear-gradient(to right, #0A0E17 0%, transparent 20%), linear-gradient(to top, rgba(5,8,17,0.7) 0%, transparent 30%);"></div>
        </div>
      </div>
    </div>
  </div>
</section>
'''

    pinned_doctors_html = '''
<!-- STAGE 5: Staged Doctor Counselors Showcase (Forge Image 4 - 02/03 Insight Style) -->
<section id="pinned-doctors-section" style="background:#060A12;padding:clamp(5rem, 8vw, 7rem) 0;position:relative;border-bottom:1px solid rgba(255,255,255,0.08);overflow:hidden;">
  <div style="position:absolute;inset:0;background:radial-gradient(circle at 70% 30%, rgba(0,197,163,0.06) 0%, transparent 60%);pointer-events:none;"></div>
  
  <div class="container-custom" style="position:relative;z-index:5;">
    <div style="margin-bottom:3.5rem;padding-bottom:1.5rem;border-bottom:1px solid rgba(255,255,255,0.08);display:flex;align-items:flex-end;justify-content:space-between;flex-wrap:wrap;gap:1.5rem;">
      <div>
        <p style="font-family:var(--font-mono);font-size:0.58rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:#00C5A3;margin-bottom:0.75rem;display:flex;align-items:center;gap:0.75rem;">
          <span>03</span><span style="opacity:0.4;">—</span><span>Our Doctor Counselors</span>
        </p>
        <h2 style="font-family:var(--font-display);font-size:clamp(2.25rem, 4.5vw, 3.75rem);line-height:1;letter-spacing:-0.03em;color:#FFFFFF;">
          Doctors Who Have <em style="font-style:italic;color:#00C5A3;">Lived It</em>
        </h2>
      </div>
      <p style="color:rgba(255,255,255,0.55);font-size:0.875rem;max-width:400px;line-height:1.7;border-left:2px solid #00C5A3;padding-left:1.25rem;">
        Direct guidance from practicing and licensed doctors who graduated from top medical universities abroad.
      </p>
    </div>

    <div id="doctor-staged-wrapper" class="grid grid-cols-1 lg:grid-cols-12 gap-10 items-center" style="min-height:480px;background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:clamp(1.5rem, 3vw, 3rem);backdrop-filter:blur(10px);">
      <div class="lg:col-span-5" style="display:flex;justify-content:center;">
        <div id="doctor-frame-card" style="width:100%;max-width:360px;aspect-ratio:3/4;border-radius:8px;border:3px solid rgba(0,197,163,0.4);overflow:hidden;box-shadow:0 25px 50px rgba(0,0,0,0.6), 0 0 30px rgba(0,197,163,0.15);position:relative;transition:all 0.5s cubic-bezier(0.16,1,0.3,1);">
          <img id="doctor-img" src="/assets/images/nishu_yadav.jpg" alt="Dr. Nishu Yadav" style="width:100%;height:100%;object-fit:cover;display:block;transition:all 0.5s ease;"/>
          <div style="position:absolute;bottom:0;left:0;right:0;padding:1rem;background:linear-gradient(to top, rgba(0,0,0,0.85) 0%, transparent 100%);">
            <span id="doctor-status-badge" style="font-family:var(--font-mono);font-size:0.55rem;font-weight:700;color:#00C5A3;background:rgba(0,197,163,0.15);padding:4px 8px;border-radius:4px;">AVAILABLE FOR CONSULTATION</span>
          </div>
        </div>
      </div>

      <div class="lg:col-span-7" style="display:flex;flex-direction:column;justify-content:center;">
        <div style="display:flex;align-items:center;gap:1.5rem;margin-bottom:1.5rem;">
          <div id="doc-step-indicator" style="font-family:var(--font-mono);font-size:1.15rem;font-weight:700;color:#00C5A3;letter-spacing:0.1em;">
            01 <span style="opacity:0.4;color:white;">/ 04</span>
          </div>
          <div style="display:flex;gap:6px;">
            <button class="doc-tab-btn active" data-doc="0" style="width:32px;height:4px;background:#00C5A3;border:none;border-radius:2px;cursor:pointer;"></button>
            <button class="doc-tab-btn" data-doc="1" style="width:32px;height:4px;background:rgba(255,255,255,0.2);border:none;border-radius:2px;cursor:pointer;"></button>
            <button class="doc-tab-btn" data-doc="2" style="width:32px;height:4px;background:rgba(255,255,255,0.2);border:none;border-radius:2px;cursor:pointer;"></button>
            <button class="doc-tab-btn" data-doc="3" style="width:32px;height:4px;background:rgba(255,255,255,0.2);border:none;border-radius:2px;cursor:pointer;"></button>
          </div>
        </div>

        <h3 id="doctor-name" style="font-family:var(--font-display);font-size:clamp(2rem, 3.8vw, 3.25rem);line-height:1.05;color:#FFFFFF;letter-spacing:-0.03em;margin-bottom:0.5rem;">
          Dr. Nishu Yadav
        </h3>

        <p id="doctor-role" style="font-family:var(--font-mono);font-size:0.68rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:#00C5A3;margin-bottom:1.25rem;">
          Founder & Lead Counselor &bull; MBBS (Semey Medical University, Kazakhstan)
        </p>

        <p id="doctor-bio" style="font-family:var(--font-inter);font-size:0.95rem;line-height:1.8;color:rgba(255,255,255,0.7);margin-bottom:2rem;max-width:540px;">
          Dr. Nishu completed his medical education across Ukraine and Kazakhstan, gaining diverse international clinical exposure. He cleared the FMGE on his very first attempt. His mission is to simplify your journey and support aspiring doctors at every step.
        </p>

        <div style="display:flex;gap:1rem;flex-wrap:wrap;align-items:center;">
          <a id="doctor-cta-btn" href="https://wa.me/919004775531?text=Hi%20Dr.%20Nishu,%20I%20want%20to%20consult%20regarding%20MBBS%20Abroad." target="_blank" rel="noopener noreferrer" class="btn-surgical btn-magnetic" style="padding:12px 24px;font-size:0.7rem;">
            Consult With Dr. Nishu via WhatsApp &rarr;
          </a>
          <div style="display:flex;gap:8px;">
            <button id="doc-prev-btn" style="width:40px;height:40px;border-radius:50%;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.15);color:white;cursor:pointer;display:flex;align-items:center;justify-content:center;">&larr;</button>
            <button id="doc-next-btn" style="width:40px;height:40px;border-radius:50%;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.15);color:white;cursor:pointer;display:flex;align-items:center;justify-content:center;">&rarr;</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
'''

    # Parse index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    main = soup.find('main')
    if not main:
        print("Error: <main> tag not found")
        return

    sections = main.find_all('section', recursive=False)
    
    # Identify existing kept sections
    calc_sec = None
    gallery_sec = None
    stories_sec = None
    video_sec = None
    faq_sec = None
    cta_sec = None

    for s in sections:
        sec_id = s.get('id')
        sec_text = s.get_text()
        if sec_id == 'budget-calculator':
            calc_sec = s
        elif 'A Glimpse Into The Stellar Experience' in sec_text:
            gallery_sec = s
        elif 'Real students.' in sec_text:
            # Polish numbering to 04
            wm = s.find('div', style=lambda st: st and 'opacity:0.03' in st)
            if wm and wm.string in ('06', '6'):
                wm.string = '04'
            lbl = s.find('p', style=lambda st: st and 'Student Stories' in st)
            if lbl:
                for span in lbl.find_all('span'):
                    if span.string in ('06', '6'):
                        span.string = '04'
            stories_sec = s
        elif 'Hear it from the' in sec_text:
            video_sec = s
        elif 'Questions we hear' in sec_text or ('FAQ' in sec_text and ('07' in sec_text or '05' in sec_text)):
            # Polish numbering to 05
            wm = s.find('div', style=lambda st: st and 'opacity:0.04' in st)
            if wm and wm.string in ('07', '7'):
                wm.string = '05'
            lbl = s.find('p', style=lambda st: st and 'FAQ' in st)
            if lbl:
                for span in lbl.find_all('span'):
                    if span.string in ('07', '7'):
                        span.string = '05'
            faq_sec = s
        elif 'Ready?' in sec_text or 'Free Counseling' in sec_text:
            cta_sec = s

    # Convert new section HTML strings into soup objects
    stage1_2_3_soup = BeautifulSoup(hero_and_quote_and_book, 'html.parser')
    stage4_soup = BeautifulSoup(pinned_countries_html, 'html.parser')
    stage5_soup = BeautifulSoup(pinned_doctors_html, 'html.parser')

    # Clear <main> and re-append in the exact requested sequence
    main.clear()

    # Append Stage 1 (Gate), Stage 2 (Quote), Stage 3 (3D Book)
    for el in stage1_2_3_soup.children:
        if el.name:
            main.append(el)

    # Append Stage 4 (Pinned Countries)
    for el in stage4_soup.children:
        if el.name:
            main.append(el)

    # Append Stage 5 (Staged Doctor Counselors)
    for el in stage5_soup.children:
        if el.name:
            main.append(el)

    # Append Budget Calculator
    if calc_sec:
        main.append(calc_sec)

    # Append Gallery
    if gallery_sec:
        main.append(gallery_sec)

    # Append Student Stories
    if stories_sec:
        main.append(stories_sec)

    # Append Video Explainer
    if video_sec:
        main.append(video_sec)

    # Append FAQ
    if faq_sec:
        main.append(faq_sec)

    # Append Ready CTA
    if cta_sec:
        main.append(cta_sec)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print("index.html successfully reconstructed with Forge animation architecture!")

    # 3. Add Forge Interactive Controller to assets/js/main.js
    forge_js = '''

// 12. Forge Automotive Gate Entrance & Campus Zoom Controller
function initForgeGate() {
    const heroSection = document.getElementById('gate-hero-section');
    const gateLeft = document.getElementById('gate-door-left');
    const gateRight = document.getElementById('gate-door-right');
    const campusBg = document.getElementById('campus-facade');
    const heroContent = document.getElementById('hero-entrance-content');
    if (!heroSection || !gateLeft || !gateRight) return;

    let ticking = false;
    function updateGate() {
        ticking = false;
        const rect = heroSection.getBoundingClientRect();
        const scrollDistance = -rect.top;
        const maxScroll = heroSection.offsetHeight - window.innerHeight;
        const progress = Math.min(Math.max(scrollDistance / (maxScroll > 0 ? maxScroll : window.innerHeight), 0), 1);

        // Rotate gate doors open
        const angle = progress * 92;
        const translateX = progress * 40;
        gateLeft.style.transform = `rotateY(-${angle}deg) translateX(-${translateX}%)`;
        gateRight.style.transform = `rotateY(${angle}deg) translateX(${translateX}%)`;
        gateLeft.style.opacity = `${Math.max(1 - progress * 1.1, 0)}`;
        gateRight.style.opacity = `${Math.max(1 - progress * 1.1, 0)}`;

        // Zoom into campus facade
        if (campusBg) {
            const scale = 1 + progress * 0.45;
            campusBg.style.transform = `scale(${scale})`;
        }

        // Fade hero title text slightly as gate opens
        if (heroContent) {
            heroContent.style.opacity = `${Math.max(1 - progress * 1.6, 0)}`;
            heroContent.style.transform = `scale(${1 + progress * 0.1}) translateY(-${progress * 40}px)`;
        }
    }

    window.addEventListener('scroll', () => {
        if (!ticking) {
            ticking = true;
            window.requestAnimationFrame(updateGate);
        }
    }, { passive: true });
    updateGate();
}

// 13. Pinned Split Country Explorer Controller (Forge Image 3 - Wheels Style)
function initForgeCountries() {
    const section = document.getElementById('pinned-countries-section');
    if (!section) return;

    const countryData = [
        {
            index: "DESTINATION 01 / 04",
            title: "Russia",
            desc: "World-renowned government medical academies with 200+ years of history, English-medium curriculum, high FMGE pass rates, and subsidized tuition fees.",
            budget: "₹20L – ₹35L (Total 6-Yr)",
            duration: "5.8 Years with Internship",
            recog: "100% NMC Compliant",
            img: "https://images.unsplash.com/photo-1513326738677-b964603b136d?w=1200&q=85",
            ctaText: "Explore Russia Universities →",
            ctaHref: "/countries/russia"
        },
        {
            index: "DESTINATION 02 / 04",
            title: "Georgia",
            desc: "European-standard clinical education, 100% English medium from day one, safe student-friendly cities, and world-class simulation hospitals.",
            budget: "₹30L – ₹45L (Total 6-Yr)",
            duration: "6.0 Years (European ECTS)",
            recog: "WHO & WFME Recognized",
            img: "https://images.unsplash.com/photo-1565008447742-97f6f38c985c?w=1200&q=85",
            ctaText: "Explore Georgia Universities →",
            ctaHref: "/countries/georgia"
        },
        {
            index: "DESTINATION 03 / 04",
            title: "Kazakhstan",
            desc: "Direct alumni mentorship from our founders. Top national universities like Semey and Al-Farabi offering high clinical patient loads and low cost of living.",
            budget: "₹18L – ₹26L (Total 5.8-Yr)",
            duration: "5.8 Years (NMC Validated)",
            recog: "Highest First-Attempt FMGE Rate",
            img: "https://images.unsplash.com/photo-1558588942-930faae5a389?w=1200&q=85",
            ctaText: "Explore Kazakhstan Universities →",
            ctaHref: "/countries/kazakhstan"
        },
        {
            index: "DESTINATION 04 / 04",
            title: "Uzbekistan",
            desc: "Centrally located government institutions like Tashkent Medical Academy with affordable living costs, high clinical patient exposure, and strong doctor mentors.",
            budget: "₹16L – ₹22L (Total 5.8-Yr)",
            duration: "5.8 Years with Clinical Training",
            recog: "NMC Gazette Listed",
            img: "https://images.unsplash.com/photo-1596484552834-6a58f850e0a1?w=1200&q=85",
            ctaText: "Explore Uzbekistan Universities →",
            ctaHref: "/countries/uzbekistan"
        },
        {
            index: "AND 3 MORE DESTINATIONS",
            title: "All 7 Countries",
            desc: "We also guide eligible students to top NMC-recognized medical universities in Kyrgyzstan, Philippines, and Serbia tailored to your exact budget.",
            budget: "₹15L – ₹45L Across 7 Nations",
            duration: "Fully NMC & WHO Compliant",
            recog: "Practice Rights in India",
            img: "https://images.unsplash.com/photo-1562774053-701939374585?w=1200&q=85",
            ctaText: "Tap to know more →",
            ctaHref: "/universities"
        }
    ];

    const idxEl = document.getElementById('country-index');
    const titleEl = document.getElementById('country-title');
    const descEl = document.getElementById('country-desc');
    const budgetEl = document.getElementById('country-spec-budget');
    const durEl = document.getElementById('country-spec-duration');
    const recogEl = document.getElementById('country-spec-recog');
    const ctaBtn = document.getElementById('country-cta-btn');
    const imgEl = document.getElementById('country-img');

    let currentIndex = -1;
    let ticking = false;

    function updateCountryScroll() {
        ticking = false;
        const rect = section.getBoundingClientRect();
        const sectionHeight = section.offsetHeight;
        const scrolledIntoSection = -rect.top;

        if (scrolledIntoSection >= 0 && scrolledIntoSection <= sectionHeight) {
            const fraction = scrolledIntoSection / (sectionHeight - window.innerHeight);
            const totalSlides = countryData.length;
            const slideIndex = Math.min(Math.floor(fraction * totalSlides), totalSlides - 1);

            if (slideIndex !== currentIndex && slideIndex >= 0) {
                currentIndex = slideIndex;
                const d = countryData[slideIndex];

                if (idxEl) idxEl.textContent = d.index;
                if (titleEl) titleEl.textContent = d.title;
                if (descEl) descEl.textContent = d.desc;
                if (budgetEl) budgetEl.textContent = d.budget;
                if (durEl) durEl.textContent = d.duration;
                if (recogEl) recogEl.textContent = d.recog;
                if (ctaBtn) {
                    ctaBtn.textContent = d.ctaText;
                    ctaBtn.href = d.ctaHref;
                    if (slideIndex === totalSlides - 1) {
                        ctaBtn.style.background = '#00C5A3';
                        ctaBtn.style.color = '#003366';
                        ctaBtn.style.fontWeight = '700';
                    } else {
                        ctaBtn.style.background = '#003366';
                        ctaBtn.style.color = '#FFFFFF';
                    }
                }
                if (imgEl && imgEl.src !== d.img) {
                    imgEl.style.opacity = '0.3';
                    imgEl.style.transform = 'scale(1.06)';
                    setTimeout(() => {
                        imgEl.src = d.img;
                        imgEl.alt = 'MBBS in ' + d.title;
                        imgEl.style.opacity = '1';
                        imgEl.style.transform = 'scale(1)';
                    }, 180);
                }
            }
        }
    }

    window.addEventListener('scroll', () => {
        if (!ticking) {
            ticking = true;
            window.requestAnimationFrame(updateCountryScroll);
        }
    }, { passive: true });
    updateCountryScroll();
}

// 14. Staged Doctor Counselors Controller (Forge Image 4 - Insight Style)
function initForgeDoctors() {
    const doctors = [
        {
            name: "Dr. Nishu Yadav",
            role: "Founder & Lead Counselor • MBBS (Semey Medical University, Kazakhstan)",
            bio: "Dr. Nishu completed his medical education across Ukraine and Kazakhstan, gaining diverse international clinical exposure. He cleared the FMGE on his very first attempt. His mission is providing practical, experience-based support to aspiring doctors.",
            img: "/assets/images/nishu_yadav.jpg",
            whatsapp: "https://wa.me/919004775531?text=Hi%20Dr.%20Nishu,%20I%20want%20to%20consult%20regarding%20MBBS%20Abroad."
        },
        {
            name: "Dr. Lokesh Attri",
            role: "Co-Founder & FMG Counselor • MBBS (Semey Medical University, Kazakhstan)",
            bio: "Dr. Lokesh completed his medical degree with extensive hospital clinical exposure and cleared FMGE on his first attempt with an impressive score of 210. He actively mentors medical aspirants on subject-wise university preparation.",
            img: "/assets/images/lokesh_attri.jpg",
            whatsapp: "https://wa.me/919004775531?text=Hi%20Dr.%20Lokesh,%20I%20want%20to%20consult%20regarding%20MBBS%20Abroad."
        },
        {
            name: "Dr. Bindu Tyagi",
            role: "Co-Founder & Overseas Counselor • MBBS (Ternopil National Medical University)",
            bio: "Dr. Bindu graduated with clinical honors and mentors students on European curriculum navigation, hostel safety, clinical rounds, and year-by-year NMC compliance.",
            img: "/assets/images/bindu_tyagi.jpg",
            whatsapp: "https://wa.me/919004775531?text=Hi%20Dr.%20Bindu,%20I%20want%20to%20consult%20regarding%20MBBS%20Abroad."
        },
        {
            name: "Dr. Vikram Singh",
            role: "Senior Academic Director • MBBS, MD (Pediatrics)",
            bio: "With over a decade of clinical practice and overseas medical education advisory, Dr. Vikram oversees our rigorous university vetting process and post-arrival student welfare programs.",
            img: "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=400&q=80",
            whatsapp: "https://wa.me/919004775531?text=Hi%20Dr.%20Vikram,%20I%20want%20to%20consult%20regarding%20MBBS%20Abroad."
        }
    ];

    let currentDoc = 0;
    const nameEl = document.getElementById('doctor-name');
    const roleEl = document.getElementById('doctor-role');
    const bioEl = document.getElementById('doctor-bio');
    const imgEl = document.getElementById('doctor-img');
    const ctaBtn = document.getElementById('doctor-cta-btn');
    const indicatorEl = document.getElementById('doc-step-indicator');
    const tabBtns = document.querySelectorAll('.doc-tab-btn');
    const prevBtn = document.getElementById('doc-prev-btn');
    const nextBtn = document.getElementById('doc-next-btn');

    function renderDoc(index) {
        if (index < 0) index = doctors.length - 1;
        if (index >= doctors.length) index = 0;
        currentDoc = index;
        const d = doctors[index];

        if (nameEl) nameEl.textContent = d.name;
        if (roleEl) roleEl.textContent = d.role;
        if (bioEl) bioEl.textContent = d.bio;
        if (ctaBtn) {
            ctaBtn.href = d.whatsapp;
            ctaBtn.textContent = `Consult With ${d.name} via WhatsApp →`;
        }
        if (indicatorEl) {
            indicatorEl.innerHTML = `0${index + 1} <span style="opacity:0.4;color:white;">/ 04</span>`;
        }

        if (imgEl && imgEl.src !== d.img) {
            imgEl.style.opacity = '0.3';
            imgEl.style.transform = 'scale(0.96)';
            setTimeout(() => {
                imgEl.src = d.img;
                imgEl.alt = d.name;
                imgEl.style.opacity = '1';
                imgEl.style.transform = 'scale(1)';
            }, 180);
        }

        tabBtns.forEach((btn, i) => {
            if (i === index) {
                btn.style.background = '#00C5A3';
                btn.classList.add('active');
            } else {
                btn.style.background = 'rgba(255,255,255,0.2)';
                btn.classList.remove('active');
            }
        });
    }

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const idx = parseInt(btn.dataset.doc, 10);
            renderDoc(idx);
        });
    });

    if (prevBtn) prevBtn.addEventListener('click', () => renderDoc(currentDoc - 1));
    if (nextBtn) nextBtn.addEventListener('click', () => renderDoc(currentDoc + 1));
}
'''

    with open('assets/js/main.js', 'r', encoding='utf-8') as f:
        js = f.read()

    # Update initializers
    if 'initForgeGate();' not in js:
        js = js.replace('initScrollReveals();', 'initScrollReveals();\n    initForgeGate();\n    initForgeCountries();\n    initForgeDoctors();')

    if 'function initForgeGate' not in js:
        js += forge_js

    with open('assets/js/main.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("assets/js/main.js updated with Forge interactive handlers.")

    # 4. Upgrade server.py to ThreadedTCPServer
    server_code = '''import http.server
import socketserver
import os
import mimetypes

PORT = 3000

mimetypes.init()
mimetypes.add_type('font/woff2', '.woff2')
mimetypes.add_type('text/css', '.css')
mimetypes.add_type('application/javascript', '.js')

class CleanURLHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Keep local preview in sync while static experience is iterated
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

    def send_error_404(self):
        not_found_file = os.path.join(os.getcwd(), '404.html')
        if os.path.isfile(not_found_file):
            self.send_response(404)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            with open(not_found_file, 'rb') as f:
                content = f.read()
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_error(404, "File not found")

    def do_GET(self):
        # Handle /_next/image queries
        if self.path.startswith('/_next/image'):
            import urllib.parse
            parsed = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed.query)
            if 'url' in params:
                img_url = params['url'][0]
                if img_url.startswith('http'):
                    self.send_response(302)
                    self.send_header('Location', img_url)
                    self.end_headers()
                    return
                elif img_url.startswith('/images/'):
                    self.path = img_url
                    return super().do_GET()

        clean_url = self.path.split('?')[0].split('#')[0]

        # Exact file match on disk
        local_path = self.translate_path(clean_url)
        if os.path.isfile(local_path):
            return super().do_GET()

        # Handle privacy and disclaimer (styled reference 404)
        norm_path = clean_url.strip('/')
        if norm_path in ['privacy', 'disclaimer']:
            target_html = os.path.join(os.getcwd(), f"{norm_path}.html")
            if os.path.isfile(target_html):
                self.send_response(404)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                with open(target_html, 'rb') as f:
                    content = f.read()
                self.send_header('Content-Length', str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return
            else:
                return self.send_error_404()

        # Clean URLs without trailing slash: e.g. /countries -> countries.html or countries/index.html
        if norm_path:
            cand_html = os.path.join(os.getcwd(), (norm_path + '.html').replace('/', os.sep))
            cand_idx = os.path.join(os.getcwd(), norm_path.replace('/', os.sep), 'index.html')

            if os.path.isfile(cand_html):
                self.path = '/' + norm_path + '.html'
                return super().do_GET()
            elif os.path.isfile(cand_idx):
                self.path = '/' + norm_path + '/index.html'
                return super().do_GET()
        elif clean_url in ['/', '']:
            if os.path.isfile(os.path.join(os.getcwd(), 'index.html')):
                self.path = '/index.html'
                return super().do_GET()

        # Route not found -> branded 404 page
        return self.send_error_404()

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True

if __name__ == '__main__':
    with ThreadedTCPServer(("", PORT), CleanURLHandler) as httpd:
        print(f"Server serving clean URLs and branded 404 on port {PORT} (Multi-threaded)")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
'''
    with open('server.py', 'w', encoding='utf-8') as f:
        f.write(server_code)
    print("server.py upgraded with ThreadedTCPServer for concurrent, non-blocking requests.")

if __name__ == '__main__':
    apply_forge_experience()
