import os
import re

def install_animations():
    # 1. Update assets/js/main.js
    with open('assets/js/main.js', 'r', encoding='utf-8') as f:
        js_content = f.read()

    new_initializers = '''document.addEventListener('DOMContentLoaded', () => {
    initHeaderScroll();
    initMobileMenu();
    initFaqAccordion();
    initCountryFilters();
    highlightActiveNavLink();
    initKineticHero();
    initStatCounters();
    initBudgetCalculator();
    initMagneticButtons();
    initGalleryLightbox();
    initScrollReveals();
});'''

    js_content = re.sub(r'document\.addEventListener\(\'DOMContentLoaded\'[\s\S]*?\}\);', new_initializers, js_content, count=1)

    motion_code = '''

// 6. Kinetic Hero Typography & Atmosphere (Forge & Peryton Benchmark)
function initKineticHero() {
    const heroH1s = document.querySelectorAll('main section:first-of-type h1');
    heroH1s.forEach((h1, i) => {
        if (!h1.querySelector('.clip-reveal-wrap')) {
            const inner = h1.innerHTML;
            h1.innerHTML = `<span class="clip-reveal-wrap"><span class="clip-reveal-text delay-${i+1}">${inner}</span></span>`;
        }
    });

    const heroP = document.querySelector('main section:first-of-type p[style*="max-width:420px"]');
    if (heroP && !heroP.classList.contains('blur-focus-reveal')) {
        heroP.classList.add('blur-focus-reveal');
    }

    const heroLine = document.querySelector('main section:first-of-type > div[style*="background:#00C5A3"]');
    if (heroLine && !heroLine.classList.contains('glow-line-pulse')) {
        heroLine.classList.add('glow-line-pulse');
    }
}

// 7. Scroll-Triggered Animated Metric Counters (Peryton Benchmark)
function initStatCounters() {
    const statCards = document.querySelectorAll('section div > p[style*="font-size:clamp(1.5rem"], section div > p[style*="font-size:1.25rem"]');
    if (!statCards.length) return;

    const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const el = entry.target;
                const originalText = el.textContent.trim();
                
                let target = 0;
                let suffix = '';
                if (originalText.includes('L+')) {
                    target = parseFloat(originalText);
                    suffix = 'L+';
                } else if (originalText.includes('K')) {
                    target = parseFloat(originalText);
                    suffix = 'K';
                } else if (originalText.includes('%')) {
                    target = parseFloat(originalText);
                    suffix = '%';
                } else if (originalText.includes('+')) {
                    target = parseFloat(originalText);
                    suffix = '+';
                } else {
                    target = parseFloat(originalText);
                    suffix = '';
                }

                if (!isNaN(target) && target > 0) {
                    const duration = 1600;
                    const startTime = performance.now();

                    function updateNumber(now) {
                        const elapsed = now - startTime;
                        const progress = Math.min(elapsed / duration, 1);
                        const ease = 1 - Math.pow(1 - progress, 3);
                        const current = Math.floor(ease * target);

                        el.textContent = current + suffix;

                        if (progress < 1) {
                            requestAnimationFrame(updateNumber);
                        } else {
                            el.textContent = originalText;
                        }
                    }

                    requestAnimationFrame(updateNumber);
                }
                obs.unobserve(el);
            }
        });
    }, { threshold: 0.2 });

    statCards.forEach(card => observer.observe(card));
}

// 8. Interactive MBBS Budget & Cost Calculator Widget
function initBudgetCalculator() {
    const slider = document.getElementById('budget-calc-slider');
    if (!slider) return;

    const budgetDisplay = document.getElementById('budget-calc-val');
    const tuitionDisplay = document.getElementById('calc-tuition-val');
    const hostelDisplay = document.getElementById('calc-hostel-val');
    const durationDisplay = document.getElementById('calc-duration-val');
    const uniList = document.getElementById('calc-uni-list');
    const ctaBtn = document.getElementById('calc-whatsapp-cta');

    const universityDatabase = [
        { name: 'Kazan State Medical University', country: 'Russia', minBudget: 28, maxBudget: 35, tuition: '₹4,20,000 / yr', hostel: '₹65,000 / yr' },
        { name: 'Volgograd State Medical University', country: 'Russia', minBudget: 24, maxBudget: 32, tuition: '₹3,80,000 / yr', hostel: '₹60,000 / yr' },
        { name: 'Omsk State Medical University', country: 'Russia', minBudget: 22, maxBudget: 28, tuition: '₹3,40,000 / yr', hostel: '₹55,000 / yr' },
        { name: 'Al-Farabi Kazakh National University', country: 'Kazakhstan', minBudget: 20, maxBudget: 26, tuition: '₹3,20,000 / yr', hostel: '₹70,000 / yr' },
        { name: 'Astana Medical University', country: 'Kazakhstan', minBudget: 22, maxBudget: 28, tuition: '₹3,50,000 / yr', hostel: '₹75,000 / yr' },
        { name: 'Semey Medical University', country: 'Kazakhstan', minBudget: 18, maxBudget: 24, tuition: '₹2,80,000 / yr', hostel: '₹60,000 / yr' },
        { name: 'Tashkent Medical Academy', country: 'Uzbekistan', minBudget: 16, maxBudget: 22, tuition: '₹2,50,000 / yr', hostel: '₹50,000 / yr' },
        { name: 'Kyrgyz State Medical Academy', country: 'Kyrgyzstan', minBudget: 15, maxBudget: 20, tuition: '₹2,30,000 / yr', hostel: '₹45,000 / yr' },
        { name: 'David Tvildiani Medical University', country: 'Georgia', minBudget: 32, maxBudget: 42, tuition: '₹5,80,000 / yr', hostel: '₹90,000 / yr' },
        { name: 'Tbilisi State Medical University', country: 'Georgia', minBudget: 35, maxBudget: 45, tuition: '₹6,20,000 / yr', hostel: '₹95,000 / yr' },
        { name: 'University of Perpetual Help', country: 'Philippines', minBudget: 25, maxBudget: 32, tuition: '₹3,60,000 / yr', hostel: '₹80,000 / yr' },
        { name: 'University of Kragujevac', country: 'Serbia', minBudget: 30, maxBudget: 38, tuition: '₹4,90,000 / yr', hostel: '₹85,000 / yr' }
    ];

    function updateCalculator() {
        const val = parseInt(slider.value, 10);
        if (budgetDisplay) budgetDisplay.textContent = `₹${val} Lakhs`;

        const yearlyTotal = Math.round((val * 100000) / 5.8);
        const estTuition = Math.round(yearlyTotal * 0.78 / 1000) * 1000;
        const estHostel = Math.round(yearlyTotal * 0.22 / 1000) * 1000;

        if (tuitionDisplay) tuitionDisplay.textContent = `₹${(estTuition).toLocaleString('en-IN')} / yr`;
        if (hostelDisplay) hostelDisplay.textContent = `₹${(estHostel).toLocaleString('en-IN')} / yr`;
        if (durationDisplay) durationDisplay.textContent = val >= 32 ? '6.0 Years (European ECTS)' : '5.8 Years (NMC Compliant)';

        const matched = universityDatabase.filter(u => val >= (u.minBudget - 2) && val <= (u.maxBudget + 4));
        if (uniList) {
            uniList.innerHTML = '';
            matched.slice(0, 4).forEach(u => {
                const tag = document.createElement('div');
                tag.style.cssText = 'display:flex;align-items:center;justify-content:space-between;padding:10px 14px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:6px;transition:all 0.2s;';
                tag.innerHTML = `<div>
                    <span style="font-family:var(--font-inter);font-size:0.82rem;font-weight:600;color:#003366;display:block">${u.name}</span>
                    <span style="font-family:var(--font-mono);font-size:0.6rem;color:#00C5A3;letter-spacing:0.08em;text-transform:uppercase">${u.country}</span>
                </div>
                <div style="text-align:right">
                    <span style="font-family:var(--font-mono);font-size:0.75rem;font-weight:700;color:#0A0A0A">₹${u.minBudget}L – ₹${u.maxBudget}L</span>
                    <span style="display:block;font-size:0.55rem;color:#9CA3AF">All-inclusive est.</span>
                </div>`;
                uniList.appendChild(tag);
            });
        }

        if (ctaBtn) {
            const encodedMsg = encodeURIComponent(`Hi Stellar Science Hub, I used your website budget calculator for an MBBS abroad budget of ₹${val} Lakhs. Can you suggest the best NMC-approved universities and detailed fee breakdown?`);
            ctaBtn.href = `https://wa.me/919004775531?text=${encodedMsg}`;
            ctaBtn.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-message-circle"><path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/></svg> Get Verified Universities for ₹${val}L via WhatsApp`;
        }
    }

    slider.addEventListener('input', updateCalculator);
    updateCalculator();
}

// 9. Magnetic Proximity Pull on Desktop CTAs (Forge Benchmark)
function initMagneticButtons() {
    if (!window.matchMedia('(hover: hover) and (pointer: fine)').matches) return;

    const buttons = document.querySelectorAll('.btn-teal, .btn-surgical, .btn-magnetic');
    buttons.forEach(btn => {
        btn.addEventListener('mousemove', (e) => {
            const rect = btn.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;
            btn.style.transform = `translate(${x * 0.18}px, ${y * 0.18}px)`;
        });

        btn.addEventListener('mouseleave', () => {
            btn.style.transform = 'translate(0px, 0px)';
        });
    });
}

// 10. Lightbox Modal for Real Student & Campus Photos
function initGalleryLightbox() {
    let lightbox = document.getElementById('stellar-lightbox');
    if (!lightbox) {
        lightbox = document.createElement('div');
        lightbox.id = 'stellar-lightbox';
        lightbox.className = 'modal-lightbox-backdrop';
        lightbox.innerHTML = `
            <div class="modal-lightbox-content" style="position:relative;background:#000;">
                <button id="lightbox-close" style="position:absolute;top:12px;right:12px;background:rgba(0,0,0,0.75);border:1px solid rgba(255,255,255,0.3);color:white;width:36px;height:36px;border-radius:50%;cursor:pointer;display:flex;align-items:center;justify-content:center;z-index:20">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                </button>
                <img id="lightbox-img" src="" alt="Stellar Experience" style="max-height:80vh;max-width:90vw;display:block;object-fit:contain;border-radius:6px"/>
                <div id="lightbox-caption" style="padding:12px 16px;background:rgba(0,10,25,0.95);color:white;font-family:var(--font-inter);font-size:0.85rem;border-top:1px solid rgba(255,255,255,0.1)"></div>
            </div>
        `;
        document.body.appendChild(lightbox);

        lightbox.addEventListener('click', (e) => {
            if (e.target === lightbox || e.target.closest('#lightbox-close')) {
                lightbox.classList.remove('active');
            }
        });

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && lightbox.classList.contains('active')) {
                lightbox.classList.remove('active');
            }
        });
    }

    const galleryImages = document.querySelectorAll('section img[src*="stellar_"], section img[src*="alfa_"]');
    galleryImages.forEach(img => {
        img.style.cursor = 'zoom-in';
        img.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            const lightboxImg = document.getElementById('lightbox-img');
            const lightboxCaption = document.getElementById('lightbox-caption');
            if (lightboxImg) lightboxImg.src = img.src;
            if (lightboxCaption) lightboxCaption.textContent = img.alt || 'Stellar Science Hub Medical Community';
            lightbox.classList.add('active');
        });
    });
}

// 11. Scroll-Triggered Reveal System
function initScrollReveals() {
    const revealTargets = document.querySelectorAll('main section > div.container-custom');
    if (!revealTargets.length) return;

    const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                obs.unobserve(entry.target);
            }
        });
    }, { threshold: 0.08 });

    revealTargets.forEach(el => {
        if (!el.classList.contains('motion-fade-up')) {
            el.classList.add('motion-fade-up');
        }
        observer.observe(el);
    });
}
'''

    with open('assets/js/main.js', 'w', encoding='utf-8') as f:
        f.write(js_content + motion_code)
    print("assets/js/main.js updated with motion engine.")

    # 2. Inject Interactive Budget Calculator into index.html and countries.html
    calc_html = '''
<!-- Interactive MBBS Budget & Cost Calculator Section (Forge & Peryton Spec) -->
<section id="budget-calculator" style="background:#001F3F;padding:clamp(4rem, 6vw, 5.5rem) 0;border-bottom:1px solid rgba(255,255,255,0.08);position:relative;overflow:hidden">
  <div style="position:absolute;top:-50px;right:-50px;width:300px;height:300px;background:radial-gradient(circle, rgba(0,197,163,0.12) 0%, transparent 70%);border-radius:50%;pointer-events:none"></div>
  <div class="container-custom" style="position:relative;z-index:2">
    <div style="display:flex;align-items:flex-end;justify-content:space-between;flex-wrap:wrap;gap:1.5rem;margin-bottom:2.5rem;padding-bottom:1.5rem;border-bottom:1px solid rgba(255,255,255,0.08)">
      <div>
        <p style="font-family:var(--font-mono);font-size:0.58rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:#00C5A3;margin-bottom:0.75rem;display:flex;align-items:center;gap:0.75rem">
          <span>Interactive Planner</span><span style="opacity:0.4">—</span><span>Live Cost & Eligibility Estimator</span>
        </p>
        <h2 style="font-family:var(--font-display);font-size:clamp(2rem, 3.8vw, 3.25rem);line-height:1;letter-spacing:-0.03em;color:#FFFFFF">
          Calculate Your Total <em style="font-style:italic;color:#00C5A3">MBBS Budget</em>
        </h2>
      </div>
      <p style="color:rgba(255,255,255,0.6);font-size:0.875rem;max-width:380px;line-height:1.6;border-left:2px solid rgba(0,197,163,0.4);padding-left:1.25rem">
        Drag the slider to your planned budget to see matching NMC-approved universities, realistic tuition breakdown, and hostel expenses.
      </p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-stretch">
      <div class="lg:col-span-7" style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.1);padding:clamp(1.5rem, 3vw, 2.5rem);border-radius:8px;backdrop-filter:blur(8px);display:flex;flex-direction:column;justify-content:space-between">
        <div>
          <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:1.25rem">
            <span style="font-family:var(--font-mono);font-size:0.65rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:rgba(255,255,255,0.6)">Your Target Total Budget</span>
            <span id="budget-calc-val" style="font-family:var(--font-display);font-size:2.25rem;font-weight:700;color:#00C5A3;line-height:1">₹28 Lakhs</span>
          </div>

          <div style="margin-bottom:2rem">
            <input type="range" id="budget-calc-slider" class="calc-slider" min="15" max="45" value="28" step="1"/>
            <div style="display:flex;justify-content:space-between;font-family:var(--font-mono);font-size:0.55rem;color:rgba(255,255,255,0.4);margin-top:8px;text-transform:uppercase">
              <span>₹15L (Min.)</span>
              <span>₹25L</span>
              <span>₹35L</span>
              <span>₹45L+ (European)</span>
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3" style="margin-bottom:1.5rem">
            <div style="background:rgba(0,0,0,0.3);border:1px solid rgba(255,255,255,0.08);padding:1rem;border-radius:6px">
              <p style="font-family:var(--font-mono);font-size:0.52rem;color:rgba(255,255,255,0.5);text-transform:uppercase;letter-spacing:0.1em;margin-bottom:4px">Est. Tuition Fee</p>
              <p id="calc-tuition-val" style="font-family:var(--font-mono);font-size:1.15rem;font-weight:700;color:#FFFFFF;line-height:1.2">₹3,75,000 / yr</p>
            </div>
            <div style="background:rgba(0,0,0,0.3);border:1px solid rgba(255,255,255,0.08);padding:1rem;border-radius:6px">
              <p style="font-family:var(--font-mono);font-size:0.52rem;color:rgba(255,255,255,0.5);text-transform:uppercase;letter-spacing:0.1em;margin-bottom:4px">Hostel & Mess</p>
              <p id="calc-hostel-val" style="font-family:var(--font-mono);font-size:1.15rem;font-weight:700;color:#FFFFFF;line-height:1.2">₹1,05,000 / yr</p>
            </div>
            <div style="background:rgba(0,0,0,0.3);border:1px solid rgba(255,255,255,0.08);padding:1rem;border-radius:6px">
              <p style="font-family:var(--font-mono);font-size:0.52rem;color:rgba(255,255,255,0.5);text-transform:uppercase;letter-spacing:0.1em;margin-bottom:4px">Course Duration</p>
              <p id="calc-duration-val" style="font-family:var(--font-mono);font-size:0.88rem;font-weight:700;color:#00C5A3;line-height:1.2">5.8 Years (NMC)</p>
            </div>
          </div>
        </div>

        <div style="padding-top:1rem;border-top:1px solid rgba(255,255,255,0.08)">
          <p style="font-size:0.75rem;color:rgba(255,255,255,0.5);margin-bottom:0">
            * Covers full 5-6 year tuition, government university hostel accommodation, and Indian mess food. Zero donation or capitation fees.
          </p>
        </div>
      </div>

      <div class="lg:col-span-5" style="background:#FFFFFF;padding:clamp(1.5rem, 3vw, 2.25rem);border-radius:8px;box-shadow:0 15px 30px rgba(0,0,0,0.25);display:flex;flex-direction:column;justify-content:space-between">
        <div>
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:1rem;padding-bottom:0.75rem;border-bottom:1px solid #E2E8F0">
            <span style="font-family:var(--font-mono);font-size:0.6rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:#003366">Matching NMC Universities</span>
            <span style="font-family:var(--font-mono);font-size:0.55rem;color:#00C5A3;font-weight:700">WDOMS Listed ✓</span>
          </div>

          <div id="calc-uni-list" style="display:flex;flex-direction:column;gap:0.6rem;margin-bottom:1.5rem">
          </div>
        </div>

        <div>
          <a id="calc-whatsapp-cta" href="https://wa.me/919004775531" target="_blank" rel="noopener noreferrer" class="btn-surgical btn-magnetic" style="display:flex;align-items:center;justify-content:center;gap:8px;width:100%;text-align:center;padding:12px 18px;font-size:0.7rem">
            Get Verified Universities for ₹28L via WhatsApp
          </a>
        </div>
      </div>
    </div>
  </div>
</section>
'''

    for fn in ['index.html', 'countries.html', 'countries/index.html']:
        if not os.path.exists(fn):
            continue
        with open(fn, 'r', encoding='utf-8') as f:
            content = f.read()

        if 'id="budget-calculator"' in content:
            continue

        # For index.html: place before Section 03
        if 'Our Difference' in content:
            idx_diff = content.find('Our Difference')
            sec_start = content.rfind('<section', 0, idx_diff)
            content = content[:sec_start] + calc_html + content[sec_start:]
        else:
            # Place before footer
            idx_footer = content.find('<footer')
            if idx_footer != -1:
                content = content[:idx_footer] + calc_html + content[idx_footer:]

        with open(fn, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Injected budget calculator into {fn}")

if __name__ == '__main__':
    install_animations()
