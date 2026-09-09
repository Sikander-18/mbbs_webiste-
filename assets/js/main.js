// Stellar Science Hub & Educonsultancy - Main Client Interactions

document.addEventListener('DOMContentLoaded', () => {
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
    initForgeExperienceController();
    initHeroMarquee();
    initForgeCountries();
    initForgeDoctors();
});

// 17. Integrated destination story: the country marquee belongs to the
// existing Why Stellar editorial section instead of becoming a standalone page.
function initIntegratedDestinationStory() {
    const section = document.getElementById('why-stellar-book-section');
    if (!section || section.querySelector('.integrated-destination-story')) return;

    const destinationStory = document.createElement('div');
    destinationStory.className = 'integrated-destination-story';
    destinationStory.setAttribute('aria-labelledby', 'destination-story-title');
    destinationStory.innerHTML = `
        <div class="destination-story-intro">
            <div>
                <p class="destination-story-kicker"><span>02</span><i></i><span>THE RIGHT DESTINATION</span></p>
                <h3 id="destination-story-title">Your destination.<br><em>Your future.</em></h3>
            </div>
            <div class="destination-story-copy">
                <p>Choosing where you study medicine shapes how you learn, live and grow into a doctor. We bring the world's strongest medical destinations into one clear, doctor-led pathway.</p>
                <a class="destination-story-link" href="/universities">Explore affiliated universities <span>↗</span></a>
            </div>
        </div>

        <div class="destination-marquee" aria-label="Affiliated MBBS destinations">
            <div class="destination-marquee-fade destination-marquee-fade-left"></div>
            <div class="destination-marquee-fade destination-marquee-fade-right"></div>
            <div class="destination-marquee-track">
                <span>Russia <b>•</b></span><span>Georgia <b>•</b></span><span>Kazakhstan <b>•</b></span><span>Uzbekistan <b>•</b></span><span>Kyrgyzstan <b>•</b></span><span>Philippines <b>•</b></span><span>Serbia <b>•</b></span>
                <span aria-hidden="true">Russia <b>•</b></span><span aria-hidden="true">Georgia <b>•</b></span><span aria-hidden="true">Kazakhstan <b>•</b></span><span aria-hidden="true">Uzbekistan <b>•</b></span><span aria-hidden="true">Kyrgyzstan <b>•</b></span><span aria-hidden="true">Philippines <b>•</b></span><span aria-hidden="true">Serbia <b>•</b></span>
            </div>
        </div>

        <div class="destination-story-grid">
            <article class="destination-story-feature">
                <span class="destination-story-number">01</span>
                <h4>Advice that starts before the application.</h4>
                <p>From NEET eligibility and budget planning to university shortlisting, every recommendation is built around your future practice—not a commission.</p>
            </article>
            <article class="destination-story-feature">
                <span class="destination-story-number">02</span>
                <h4>Seven countries. One honest route.</h4>
                <p>Compare curriculum, clinical exposure, recognition, safety and student life with guidance from people who have walked the same halls.</p>
            </article>
            <article class="destination-story-feature destination-story-feature-accent">
                <span class="destination-story-number">03</span>
                <h4>Meet the place before you commit.</h4>
                <p>Use our university profiles to move from a country name to a clear, informed decision about where your medical journey begins.</p>
                <a class="destination-story-arrow" href="/universities" aria-label="View all universities">↗</a>
            </article>
        </div>

        <div class="destination-story-footer">
            <span>Doctor-led guidance · NMC-aware shortlisting · No pressure</span>
            <span class="destination-story-rule"></span>
            <span>Scroll to meet your destination</span>
        </div>
    `;

    section.appendChild(destinationStory);
    section.classList.add('has-integrated-destinations');

    const standaloneExplorer = document.getElementById('pinned-countries-section');
    if (standaloneExplorer) standaloneExplorer.setAttribute('aria-hidden', 'true');
}

// 1. Header scroll effect matching reference site
function initHeaderScroll() {
    const header = document.querySelector('header');
    if (!header) return;

    // Ensure accent line exists at top of header
    let accentLine = header.querySelector('#header-accent-line');
    if (!accentLine) {
        accentLine = document.createElement('div');
        accentLine.id = 'header-accent-line';
        accentLine.style.position = 'absolute';
        accentLine.style.top = '0';
        accentLine.style.left = '0';
        accentLine.style.right = '0';
        accentLine.style.height = '2px';
        accentLine.style.background = 'linear-gradient(to right, #00B8A9, #C9A45C)';
        accentLine.style.display = 'none';
        accentLine.style.zIndex = '10';
        header.prepend(accentLine);
    }

    const brandContainer = header.querySelector('a.mr-auto');
    const brandBadge = brandContainer ? brandContainer.querySelector('.brand-logo-badge') : null;
    const brandTitle = brandContainer ? brandContainer.querySelector('p:first-of-type') : null;
    const brandSub = brandContainer ? brandContainer.querySelector('p:last-of-type') : null;
    const navLinks = header.querySelectorAll('nav a');
    const counselingContainer = header.querySelector('.hidden.lg\\:flex.items-center');
    const toggleBtn = header.querySelector('button[aria-label="Toggle menu"]');

    let isScrolled = false;

    // Attach hover listeners for nav links
    navLinks.forEach(link => {
        link.addEventListener('mouseenter', () => {
            if (!link.dataset.active) {
                link.style.color = isScrolled ? '#00B8A9' : '#F5F3EE';
            }
        });
        link.addEventListener('mouseleave', () => {
            if (!link.dataset.active) {
                link.style.color = isScrolled ? '#9CA3AF' : 'rgba(255, 255, 255, 0.55)';
            }
        });
    });

    function onScroll() {
        const forgeStage = document.getElementById('forge-stage-experience');
        const isOverDarkHero = forgeStage 
            ? (window.scrollY < (forgeStage.offsetTop + forgeStage.offsetHeight - 80)) 
            : (window.scrollY < 2200);

        if (isOverDarkHero) {
            header.style.background = 'rgba(7, 17, 28, 0.88)';
            header.style.backdropFilter = 'blur(12px)';
            header.style.webkitBackdropFilter = 'blur(12px)';
            header.style.borderBottom = '1px solid rgba(255, 255, 255, 0.1)';
            header.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.4)';
            accentLine.style.display = 'block';

            if (brandContainer) brandContainer.style.borderRight = '1px solid rgba(255, 255, 255, 0.1)';
            if (brandTitle) brandTitle.style.color = 'white';
            if (brandSub) brandSub.style.color = '#00B8A9';
            if (brandBadge) {
                brandBadge.style.borderColor = 'rgba(255, 255, 255, 0.25)';
                brandBadge.style.boxShadow = '0 2px 6px rgba(0, 0, 0, 0.2)';
            }

            navLinks.forEach(link => {
                link.style.borderRight = '1px solid rgba(255, 255, 255, 0.08)';
                if (!link.dataset.active) {
                    link.style.color = 'rgba(255, 255, 255, 0.7)';
                }
            });

            if (counselingContainer) counselingContainer.style.borderLeft = '1px solid rgba(255, 255, 255, 0.1)';
            if (toggleBtn) {
                toggleBtn.style.color = 'white';
                toggleBtn.style.borderLeft = '1px solid rgba(255, 255, 255, 0.1)';
            }
        } else {
            header.style.background = 'rgba(13, 27, 42, 0.96)';
            header.style.backdropFilter = 'blur(12px)';
            header.style.webkitBackdropFilter = 'blur(12px)';
            header.style.borderBottom = '1px solid #243342';
            header.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.06)';
            accentLine.style.display = 'block';

            if (brandContainer) brandContainer.style.borderRight = '1px solid #243342';
            if (brandTitle) brandTitle.style.color = '#F5F3EE';
            if (brandSub) brandSub.style.color = '#00B8A9';
            if (brandBadge) {
                brandBadge.style.borderColor = '#E2E8F0';
                brandBadge.style.boxShadow = '0 1px 3px rgba(0, 0, 0, 0.08)';
            }

            navLinks.forEach(link => {
                link.style.borderRight = '1px solid #243342';
                if (!link.dataset.active) {
                    link.style.color = '#9CA3AF';
                }
            });

            if (counselingContainer) counselingContainer.style.borderLeft = '1px solid #243342';
            if (toggleBtn) {
                toggleBtn.style.color = '#F5F3EE';
                toggleBtn.style.borderLeft = '1px solid #243342';
            }
        }
    }

    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
}


// 2. Mobile Menu Toggle
function initMobileMenu() {
    const toggleBtn = document.querySelector('button[aria-label="Toggle menu"]');
    const mobileMenu = document.querySelector('.lg\\:hidden.transition-all.duration-300.overflow-hidden');
    if (!toggleBtn || !mobileMenu) return;

    let isOpen = false;

    toggleBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        isOpen = !isOpen;
        if (isOpen) {
            mobileMenu.style.maxHeight = '600px';
            mobileMenu.classList.remove('max-h-0');
            toggleBtn.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>`;
        } else {
            mobileMenu.style.maxHeight = '0px';
            mobileMenu.classList.add('max-h-0');
            toggleBtn.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="4" x2="20" y1="12" y2="12"></line><line x1="4" x2="20" y1="6" y2="6"></line><line x1="4" x2="20" y1="18" y2="18"></line></svg>`;
        }
    });

    document.addEventListener('click', (e) => {
        if (isOpen && !mobileMenu.contains(e.target) && !toggleBtn.contains(e.target)) {
            isOpen = false;
            mobileMenu.style.maxHeight = '0px';
            mobileMenu.classList.add('max-h-0');
            toggleBtn.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="4" x2="20" y1="12" y2="12"></line><line x1="4" x2="20" y1="6" y2="6"></line><line x1="4" x2="20" y1="18" y2="18"></line></svg>`;
        }
    });
}

// 3. Interactive FAQ Accordion
function initFaqAccordion() {
    // Find all FAQ question headers/containers
    const faqBlocks = document.querySelectorAll('details, [data-faq-item]');
    faqBlocks.forEach(block => {
        const summary = block.querySelector('summary, [data-faq-trigger]');
        if (summary) {
            summary.style.cursor = 'pointer';
        }
    });

    // Support accordion items that use buttons/headings
    const accordions = document.querySelectorAll('.faq-item, [class*="border-b"][class*="cursor-pointer"]');
    accordions.forEach(item => {
        const trigger = item.querySelector('button, h3, div');
        const content = item.querySelector('p, div.faq-content');
        if (trigger && content) {
            trigger.addEventListener('click', () => {
                const isExpanded = content.style.display !== 'none';
                content.style.display = isExpanded ? 'none' : 'block';
            });
        }
    });
}

// 4. Country Filters on /countries page
function initCountryFilters() {
    const filterButtons = document.querySelectorAll('button');
    if (!filterButtons.length) return;

    let selectedBudget = 'Any Budget';
    let selectedDuration = 'Any Duration';
    let selectedInternship = 'Any';

    const countryCards = document.querySelectorAll('a[href*="/countries/"]');

    filterButtons.forEach(btn => {
        const text = btn.textContent.trim();
        const parent = btn.parentElement;
        if (!parent) return;

        const rowLabel = parent.querySelector('span')?.textContent.trim();
        if (!rowLabel) return;

        if (['Budget', 'Duration', 'Internship'].includes(rowLabel)) {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                // Set active style on sibling buttons
                parent.querySelectorAll('button').forEach(b => {
                    b.style.background = '#FFFFFF';
                    b.style.color = '#6B7280';
                    b.style.borderColor = '#E8E8E8';
                });
                btn.style.background = '#00B8A9'; btn.style.color = '#07111C';
                btn.style.color = '#FFFFFF';
                btn.style.borderColor = '#00B8A9';

                if (rowLabel === 'Budget') selectedBudget = text;
                if (rowLabel === 'Duration') selectedDuration = text;
                if (rowLabel === 'Internship') selectedInternship = text;

                filterCountryCards();
            });
        }
    });

    function filterCountryCards() {
        countryCards.forEach(card => {
            const cardText = card.textContent.toLowerCase();
            let match = true;

            // Budget filter logic
            if (selectedBudget === 'Under ₹25L') {
                match = match && (cardText.includes('15l') || cardText.includes('17l') || cardText.includes('20l') || cardText.includes('22l'));
            } else if (selectedBudget === '₹25L – ₹40L') {
                match = match && (cardText.includes('25l') || cardText.includes('30l') || cardText.includes('33l') || cardText.includes('35l') || cardText.includes('36l'));
            } else if (selectedBudget === '₹40L+') {
                match = match && (cardText.includes('40l') || cardText.includes('45l'));
            }

            // Duration filter logic
            if (selectedDuration === '5 Years') {
                match = match && cardText.includes('5 years');
            } else if (selectedDuration === '5.5 Years') {
                match = match && (cardText.includes('5.5') || cardText.includes('5.8'));
            } else if (selectedDuration === '6 Years') {
                match = match && cardText.includes('6 years');
            }

            card.style.display = match ? '' : 'none';
        });
    }

    // Grid vs List view toggle
    const gridBtn = document.querySelector('button[title="Grid view"]');
    const listBtn = document.querySelector('button[title="List view"]');
    const container = document.querySelector('.sm\\:grid-cols-2.lg\\:grid-cols-4');

    if (gridBtn && listBtn && container) {
        gridBtn.addEventListener('click', () => {
            gridBtn.style.background = '#00B8A9'; gridBtn.style.color = '#07111C';
            gridBtn.style.color = '#FFFFFF';
            listBtn.style.background = '#FFFFFF';
            listBtn.style.color = '#9CA3AF';
            container.className = 'grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-px bg-[#E8E8E8]';
        });

        listBtn.addEventListener('click', () => {
            listBtn.style.background = '#00B8A9'; listBtn.style.color = '#07111C';
            listBtn.style.color = '#FFFFFF';
            gridBtn.style.background = '#FFFFFF';
            gridBtn.style.color = '#9CA3AF';
            container.className = 'grid grid-cols-1 gap-px bg-[#E8E8E8]';
        });
    }
}

// 5. Highlight active navbar link
function highlightActiveNavLink() {
    const currentPath = window.location.pathname.replace(/\/index\.html$/, '').replace(/\/$/, '') || '/';
    const navLinks = document.querySelectorAll('header nav a, .lg\\:hidden a');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (!href) return;
        const cleanHref = href.replace(/\/index\.html$/, '').replace(/\/$/, '') || '/';

        if (cleanHref === currentPath || (cleanHref !== '/' && currentPath.startsWith(cleanHref))) {
            const bar = link.querySelector('span');
            if (bar) bar.style.transform = 'scaleX(1)';
            link.style.color = '#00B8A9';
        }
    });
}


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

    const heroLine = document.querySelector('.glow-line-pulse') || document.querySelector('main section:first-of-type > div[style*="background:#00B8A9"]');
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
                    <span style="font-family:var(--font-inter);font-size:0.82rem;font-weight:600;color:#07111C;display:block">${u.name}</span>
                    <span style="font-family:var(--font-mono);font-size:0.6rem;color:#00B8A9;letter-spacing:0.08em;text-transform:uppercase">${u.country}</span>
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

// 12. Forge Automotive Style Unified Hero Stage Controller
function initForgeExperienceController() {
    const section = document.getElementById('forge-stage-experience');
    if (!section) return;

    const wingLeft = document.getElementById('gate-wing-left');
    const wingRight = document.getElementById('gate-wing-right');
    const campusScene = document.getElementById('stage-campus-scene');
    const scrollCue = document.getElementById('stage-scroll-cue');
    const darkVeil = document.getElementById('stage-dark-veil');
    const quoteLayer = document.getElementById('stage-quote-layer');
    const quoteContainer = document.getElementById('stage-quote-container');
    const apertureLayer = document.getElementById('stage-aperture-layer');
    const apertureFrame = document.getElementById('stage-aperture-frame');
    const header = document.querySelector('header');

    let ticking = false;

    function onScroll() {
        ticking = false;
        const rect = section.getBoundingClientRect();
        const scrollDistance = -rect.top;
        const maxScroll = section.offsetHeight - window.innerHeight;
        const progress = Math.min(Math.max(scrollDistance / (maxScroll > 0 ? maxScroll : 1), 0), 1);

        // Header visibility: hidden during cinematic stage experience, reveals once scrolling into page content
        if (header) {
            if (progress < 0.95) {
                header.classList.add('header-cinematic-hidden');
            } else {
                header.classList.remove('header-cinematic-hidden');
            }
        }

        // --- PHASE 1a: Fade Out Discreet Bottom Scroll Cue (0.00 to 0.08) ---
        if (scrollCue) {
            if (progress <= 0.08) {
                scrollCue.style.opacity = (1 - progress / 0.08).toFixed(3);
            } else {
                scrollCue.style.opacity = '0';
            }
        }

        // --- PHASE 1b: Realistic 3D Double Gate Opening (0.00 to 0.32) ---
        if (wingLeft && wingRight) {
            const gateProgress = Math.min(progress / 0.30, 1);
            // Smooth natural cubic easing
            const easedGate = gateProgress < 0.5 
                ? 4 * gateProgress * gateProgress * gateProgress 
                : 1 - Math.pow(-2 * gateProgress + 2, 3) / 2;

            const swingAngle = easedGate * 82; // degrees rotation around pillar hinges
            wingLeft.style.transform = `rotateY(-${swingAngle.toFixed(2)}deg)`;
            wingRight.style.transform = `rotateY(${swingAngle.toFixed(2)}deg)`;

            // Smoothly blend into perspective as gates swing fully open
            const gateOpacity = gateProgress > 0.72 
                ? Math.max(1 - (gateProgress - 0.72) / 0.28, 0).toFixed(3) 
                : '1';
            wingLeft.style.opacity = gateOpacity;
            wingRight.style.opacity = gateOpacity;
        }

        // --- PHASE 1c: Camera Dolly Push into University Courtyard (0.00 to 0.56) ---
        if (campusScene) {
            const dollyProgress = Math.min(progress / 0.56, 1);
            const cameraScale = 1 + dollyProgress * 0.14; // gentle, majestic 1.0 to 1.14 zoom
            campusScene.style.transform = `translate(-50%, -50%) scale(${cameraScale.toFixed(3)})`;
        }

        // --- PHASE 1d: No solid black veil — keep college image visible! ---
        if (darkVeil) {
            darkVeil.style.opacity = '0';
        }

        // --- PHASE 2: Quote Appears Directly on College Image after Gate Opens (0.20 to 0.56) ---
        if (quoteLayer) {
            if (progress < 0.20) {
                quoteLayer.style.opacity = '0';
                quoteLayer.style.pointerEvents = 'none';
            } else if (progress >= 0.20 && progress < 0.32) {
                // Fade in quote smoothly over the open collegiate courtyard
                const qIn = (progress - 0.20) / 0.12;
                quoteLayer.style.opacity = qIn.toFixed(3);
                if (quoteContainer) {
                    const transY = (1 - qIn) * 24;
                    quoteContainer.style.transform = `translateY(${transY.toFixed(1)}px)`;
                }
            } else if (progress >= 0.32 && progress <= 0.46) {
                // Hold quote static, prominent, and readable directly over the sunlit campus
                quoteLayer.style.opacity = '1';
                if (quoteContainer) quoteContainer.style.transform = 'translateY(0px)';
            } else if (progress > 0.46 && progress <= 0.56) {
                // Fade out quote gently before aperture opens
                const qOut = (progress - 0.46) / 0.10;
                quoteLayer.style.opacity = (1 - qOut).toFixed(3);
                if (quoteContainer) {
                    const transY = -qOut * 20;
                    quoteContainer.style.transform = `translateY(${transY.toFixed(1)}px)`;
                }
            } else {
                quoteLayer.style.opacity = '0';
                quoteLayer.style.pointerEvents = 'none';
            }
        }

        // --- PHASE 3: Center Box Opens & Expands to Reveal Brand Hero + Marquee (0.58 to 0.98) ---
        if (apertureLayer) {
            if (progress < 0.58) {
                apertureLayer.style.opacity = '0';
                apertureLayer.style.pointerEvents = 'none';
                apertureLayer.style.clipPath = 'inset(45% 42% 45% 42% round 16px)';
                if (apertureFrame) {
                    apertureFrame.style.opacity = '0';
                }
            } else {
                const boxProgress = Math.min((progress - 0.58) / 0.38, 1);
                const easedBox = boxProgress < 0.5 
                    ? 4 * Math.pow(boxProgress, 3) 
                    : 1 - Math.pow(-2 * boxProgress + 2, 3) / 2;

                apertureLayer.style.opacity = boxProgress < 0.06 ? (boxProgress / 0.06).toFixed(3) : '1';

                // Aperture inset clip: shrinks from 44% top/bottom and 40% left/right down to 0%
                const clipY = Math.max((1 - easedBox) * 44, 0).toFixed(2);
                const clipX = Math.max((1 - easedBox) * 40, 0).toFixed(2);
                const clipRadius = Math.max((1 - easedBox) * 16, 0).toFixed(1);
                apertureLayer.style.clipPath = `inset(${clipY}% ${clipX}% ${clipY}% ${clipX}% round ${clipRadius}px)`;

                // Subtle zoom of content from 0.94 to 1.00 as aperture opens
                const scaleVal = (0.94 + easedBox * 0.06).toFixed(3);
                apertureLayer.style.transform = `scale(${scaleVal})`;

                // Aperture glowing frame outline
                if (apertureFrame) {
                    if (progress < 0.92 && boxProgress < 0.85) {
                        const frameOpacity = boxProgress < 0.08 ? (boxProgress / 0.08) : Math.max(0, 1 - (boxProgress - 0.65) / 0.2);
                        apertureFrame.style.opacity = Math.max(0, Math.min(1, frameOpacity)).toFixed(2);
                        const frameW = (100 - clipX * 2).toFixed(2);
                        const frameH = (100 - clipY * 2).toFixed(2);
                        apertureFrame.style.width = `${frameW}%`;
                        apertureFrame.style.height = `${frameH}%`;
                        apertureFrame.style.borderRadius = `${clipRadius}px`;
                        const alpha = Math.max((1 - easedBox) * 0.6, 0).toFixed(2);
                        apertureFrame.style.borderColor = `rgba(0, 184, 169, ${alpha})`;
                        apertureFrame.style.boxShadow = `0 0 35px rgba(0, 184, 169, ${(alpha * 0.35).toFixed(2)}), 0 20px 60px rgba(0, 0, 0, ${(alpha * 1.5).toFixed(2)})`;
                    } else {
                        apertureFrame.style.opacity = '0';
                    }
                }

                if (boxProgress >= 0.85) {
                    apertureLayer.style.pointerEvents = 'auto';
                } else {
                    apertureLayer.style.pointerEvents = 'none';
                }

                if (progress >= 0.98) {
                    apertureLayer.style.clipPath = 'inset(0% 0% 0% 0% round 0px)';
                    apertureLayer.style.transform = 'scale(1)';
                }
            }
        }
    }

    window.addEventListener('scroll', () => {
        if (!ticking) {
            ticking = true;
            window.requestAnimationFrame(onScroll);
        }
    }, { passive: true });

    // Initial sync
    onScroll();
}

// 12b. Infinite Country Marquee Scroll-Speed Controller
function initHeroMarquee() {
    const track = document.getElementById('hero-marquee-track');
    if (!track) return;

    let lastScrollY = window.scrollY;
    let scrollTimeout = null;

    window.addEventListener('scroll', () => {
        const delta = Math.abs(window.scrollY - lastScrollY);
        lastScrollY = window.scrollY;

        if (delta > 4) {
            track.style.animationDuration = '13s';
            clearTimeout(scrollTimeout);
            scrollTimeout = setTimeout(() => {
                track.style.animationDuration = '28s';
            }, 300);
        }
    }, { passive: true });
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
                        ctaBtn.style.background = '#00B8A9';
                        ctaBtn.style.color = '#07111C';
                        ctaBtn.style.fontWeight = '700';
                    } else {
                        ctaBtn.style.background = '#00B8A9';
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
                btn.style.background = '#00B8A9'; btn.style.color = '#07111C';
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
