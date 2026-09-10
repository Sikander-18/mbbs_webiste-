// Stellar Science Hub & Educonsultancy - Main Client Interactions

document.addEventListener('DOMContentLoaded', () => {
    initRafiqProfileSection();
    initHeaderScroll();
    initMobileMenu();
    initFaqAccordion();
    initCountryFilters();
    initCountryBannerStack();
    highlightActiveNavLink();
    initKineticHero();
    initStatCounters();
    initMagneticButtons();
    initGalleryLightbox();
    initScrollReveals();
    initForgeExperienceController();
    initHeroMarquee();
    initBookExperience();
    initForgeCountries();
    initForgeDoctors();
});

// Homepage profile copy beside the featured video.
function initRafiqProfileSection() {
    const video = document.querySelector('iframe[src*="youtube.com/embed/dQw4w9WgXcQ"]');
    const section = video?.closest('section');
    const heading = section?.querySelector('h2');
    const description = section?.querySelector('h2 + div + p');

    if (!heading || !description) return;

    heading.textContent = 'Rafiq Sir';
    description.textContent = 'With a career dedicated to guiding students toward the right medical education opportunities, Rafiq Sir brings over a decade of experience in the MBBS abroad counselling space. He completed his B.Sc. in 1997 and later pursued an LLB, completed in 2026. While Stellar Educonsultancy was officially established in 2024, his work in the field began more than 10 years ago, during which he has successfully guided and placed 1,200+ students in medical universities abroad. His experience is built on understanding students’ aspirations, choosing the right destinations, and helping families navigate the journey with confidence.';
}

// Countries page: scroll-driven editorial banner stack.
function initCountryBannerStack() {
    const section = document.getElementById('filter');
    const firstCard = section?.querySelector('a.group');
    const stack = firstCard?.parentElement;
    if (!section || !stack) return;

    const cards = Array.from(stack.children).filter(child => child.matches('a.group'));
    if (cards.length < 2) return;

    section.classList.add('country-stack-section');
    stack.classList.add('country-banner-stack');

    const sectionHeading = section.querySelector('h2');
    if (sectionHeading) {
        sectionHeading.innerHTML = sectionHeading.innerHTML.replace('All 8 destinations', 'All 7 destinations');
    }

    cards.forEach((card, index) => {
        card.classList.add('country-banner-card');
        card.style.setProperty('--stack-order', index);
        card.style.setProperty('--stack-z', index + 1);

        const sequence = document.createElement('span');
        sequence.className = 'country-banner-sequence';
        sequence.textContent = `${String(index + 1).padStart(2, '0')} / ${String(cards.length).padStart(2, '0')}`;
        sequence.setAttribute('aria-hidden', 'true');
        card.appendChild(sequence);
    });

    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    let ticking = false;

    const updateStack = () => {
        ticking = false;
        const visibleCards = cards.filter(card => window.getComputedStyle(card).display !== 'none');
        const compact = window.innerWidth < 768;
        const baseTop = compact ? 76 : 88;
        const step = compact ? 7 : 13;

        visibleCards.forEach((card, index) => {
            card.style.setProperty('--stack-top', `${baseTop + (index * step)}px`);
            card.style.setProperty('--stack-z', index + 1);

            if (reduceMotion) return;

            const nextCard = visibleCards[index + 1];
            if (!nextCard) {
                card.style.setProperty('--stack-scale', '1');
                card.style.setProperty('--stack-brightness', '1');
                return;
            }

            const nextTop = nextCard.getBoundingClientRect().top;
            const animationStart = window.innerHeight * 0.88;
            const animationDistance = window.innerHeight * 0.7;
            const progress = Math.max(0, Math.min(1, (animationStart - nextTop) / animationDistance));
            card.style.setProperty('--stack-scale', (1 - (progress * (compact ? 0.018 : 0.032))).toFixed(4));
            card.style.setProperty('--stack-brightness', (1 - (progress * 0.28)).toFixed(4));
        });
    };

    const requestUpdate = () => {
        if (ticking) return;
        ticking = true;
        window.requestAnimationFrame(updateStack);
    };

    if (!reduceMotion) {
        window.addEventListener('scroll', requestUpdate, { passive: true });
        window.addEventListener('resize', requestUpdate, { passive: true });
    }

    const filterObserver = new MutationObserver(requestUpdate);
    cards.forEach(card => filterObserver.observe(card, { attributes: true, attributeFilter: ['style', 'class'] }));
    updateStack();
}

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
                <span>Uzbekistan <b>•</b></span><span>Kyrgyzstan <b>•</b></span><span>Kazakhstan <b>•</b></span><span>Russia <b>•</b></span><span>Bangladesh <b>•</b></span><span>Georgia <b>•</b></span><span>Nepal <b>•</b></span>
                <span aria-hidden="true">Uzbekistan <b>•</b></span><span aria-hidden="true">Kyrgyzstan <b>•</b></span><span aria-hidden="true">Kazakhstan <b>•</b></span><span aria-hidden="true">Russia <b>•</b></span><span aria-hidden="true">Bangladesh <b>•</b></span><span aria-hidden="true">Georgia <b>•</b></span><span aria-hidden="true">Nepal <b>•</b></span>
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
        accentLine.style.background = 'linear-gradient(to right, #283A27, #C9A45C)';
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
                link.style.color = isScrolled ? '#283A27' : '#F7F5EE';
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
            if (brandSub) brandSub.style.color = '#C9A45C';
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
            if (brandSub) brandSub.style.color = '#C9A45C';
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
    const canHover = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const closeTimers = new WeakMap();

    document.querySelectorAll('details').forEach(block => {
        const summary = block.querySelector(':scope > summary');
        const answer = summary?.nextElementSibling;
        if (!summary || !answer) return;

        block.classList.add('faq-hover-item');
        summary.style.cursor = 'pointer';
        summary.setAttribute('aria-expanded', String(block.open));

        block.addEventListener('toggle', () => {
            summary.setAttribute('aria-expanded', String(block.open));
            if (block.open && !reduceMotion && typeof answer.animate === 'function') {
                answer.animate(
                    [
                        { opacity: 0, transform: 'translateY(-7px)' },
                        { opacity: 1, transform: 'translateY(0)' }
                    ],
                    { duration: 220, easing: 'cubic-bezier(0.22, 1, 0.36, 1)' }
                );
            }
        });

        if (!canHover) return;

        block.addEventListener('mouseenter', () => {
            window.clearTimeout(closeTimers.get(block));
            block.open = true;
        });

        block.addEventListener('mouseleave', () => {
            const timer = window.setTimeout(() => {
                if (!block.contains(document.activeElement)) block.open = false;
            }, 140);
            closeTimers.set(block, timer);
        });

        // Pointer users get hover-first behaviour. Keyboard activation continues
        // to use the native details control, and touch devices retain tap-to-open.
        summary.addEventListener('click', event => {
            if (event.detail > 0) {
                event.preventDefault();
                block.open = true;
            }
        });
    });

    // Support any non-details FAQ components that may be added later.
    document.querySelectorAll('[data-faq-item]').forEach(item => {
        const trigger = item.querySelector('[data-faq-trigger]');
        const content = item.querySelector('[data-faq-content]');
        if (!trigger || !content) return;

        const setExpanded = expanded => {
            item.classList.toggle('is-open', expanded);
            trigger.setAttribute('aria-expanded', String(expanded));
            content.hidden = !expanded;
        };

        trigger.addEventListener('click', () => setExpanded(content.hidden));
        if (canHover) {
            item.addEventListener('mouseenter', () => setExpanded(true));
            item.addEventListener('mouseleave', () => setExpanded(false));
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

    const filterSection = document.getElementById('filter');
    const countryCards = filterSection
        ? filterSection.querySelectorAll('a.group')
        : document.querySelectorAll('a[href*="/countries/"]');

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
                btn.style.background = '#283A27'; btn.style.color = '#F7F5EE';
                btn.style.color = '#FFFFFF';
                btn.style.borderColor = '#283A27';

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
            const budgetMatch = cardText.match(/₹\s*(\d+)[^\d]+(\d+)/);
            const budgetMin = budgetMatch ? Number(budgetMatch[1]) : null;
            const budgetMax = budgetMatch ? Number(budgetMatch[2]) : null;

            if (selectedBudget === 'Under ₹25L') {
                match = match && budgetMin !== null && budgetMin < 25;
            } else if (selectedBudget === '₹25L – ₹40L') {
                match = match && budgetMin !== null && budgetMin >= 25 && budgetMin <= 40;
            } else if (selectedBudget === '₹40L+') {
                match = match && budgetMax !== null && budgetMax >= 40;
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
            gridBtn.style.background = '#283A27'; gridBtn.style.color = '#F7F5EE';
            gridBtn.style.color = '#FFFFFF';
            listBtn.style.background = '#FFFFFF';
            listBtn.style.color = '#9CA3AF';
            container.className = 'grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-px bg-[#E8E8E8]';
        });

        listBtn.addEventListener('click', () => {
            listBtn.style.background = '#283A27'; listBtn.style.color = '#F7F5EE';
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
            link.style.color = '#283A27';
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

    const heroLine = document.querySelector('.glow-line-pulse') || document.querySelector('main section:first-of-type > div[style*="background:#283A27"]');
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

// 13. Scroll-open Doctor-Led Compendium
function initBookExperience() {
    const section = document.getElementById('why-stellar-book-section');
    const sticky = section ? section.querySelector('.book-story__sticky') : null;
    const book = document.getElementById('medical-book');
    if (!section || !sticky || !book) return;

    const leftPage = book.querySelector('.medical-book-page-left');
    const rightPage = book.querySelector('.medical-book-page-right');
    const header = section.querySelector('.book-story__header');
    const pageContent = book.querySelectorAll('.medical-book-page-left > *, .medical-book-page-right > *');

    const progress = document.createElement('div');
    progress.className = 'book-story__progress';
    progress.innerHTML = '<span></span><small>Scroll to open</small>';
    sticky.appendChild(progress);

    if (typeof gsap === 'undefined' || typeof ScrollTrigger === 'undefined') return;
    gsap.registerPlugin(ScrollTrigger);

    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        section.classList.add('book-story--open');
        progress.hidden = true;
        return;
    }

    const mm = gsap.matchMedia();

    mm.add('(min-width: 768px)', () => {
        gsap.set(book, {
            scale: 0.56,
            y: 105,
            rotationX: 15,
            transformPerspective: 1800,
            transformOrigin: '50% 72%'
        });
        gsap.set(leftPage, {
            rotationY: 86,
            transformOrigin: '100% 50%',
            filter: 'brightness(0.42)'
        });
        gsap.set(rightPage, {
            rotationY: -86,
            transformOrigin: '0% 50%',
            filter: 'brightness(0.42)'
        });
        gsap.set(pageContent, { opacity: 0, y: 18 });
        gsap.set(header, { opacity: 0.35, y: 26 });

        const tl = gsap.timeline({
            scrollTrigger: {
                trigger: section,
                start: 'top top',
                end: '+=3000',
                pin: sticky,
                scrub: 1.15,
                anticipatePin: 1,
                invalidateOnRefresh: true
            },
            onUpdate: () => {
                section.style.setProperty('--book-progress', `${(tl.progress() * 100).toFixed(2)}%`);
                progress.querySelector('small').textContent = tl.progress() > 0.82 ? 'Chapter open' : 'Scroll to open';
            }
        });

        tl.to(header, { opacity: 1, y: 0, duration: 0.9, ease: 'power2.out' }, 0)
          .to(book, { scale: 0.72, y: 30, rotationX: 10, duration: 1.1, ease: 'power2.out' }, 0)
          .to(leftPage, { rotationY: 0, filter: 'brightness(1)', duration: 2.8, ease: 'power2.inOut' }, 0.75)
          .to(rightPage, { rotationY: 0, filter: 'brightness(1)', duration: 2.8, ease: 'power2.inOut' }, 0.75)
          .to(book, { scale: 1, y: 0, rotationX: 0, duration: 2.2, ease: 'power2.out' }, 1.2)
          .to(pageContent, { opacity: 1, y: 0, duration: 1.1, stagger: 0.08, ease: 'power2.out' }, 2.65)
          .to(book, { y: -8, duration: 1.15, ease: 'none' }, 3.75)
          .to({}, { duration: 0.8 });

        return () => {
            tl.kill();
            section.style.removeProperty('--book-progress');
        };
    });

    mm.add('(max-width: 767px)', () => {
        gsap.set(book, { scale: 0.88, y: 70, clipPath: 'inset(0 48% 0 48% round 8px)' });
        gsap.set(pageContent, { opacity: 0, y: 14 });

        const tl = gsap.timeline({
            scrollTrigger: {
                trigger: section,
                start: 'top top',
                end: '+=1450',
                pin: sticky,
                scrub: 0.9,
                anticipatePin: 1,
                invalidateOnRefresh: true
            },
            onUpdate: () => {
                section.style.setProperty('--book-progress', `${(tl.progress() * 100).toFixed(2)}%`);
            }
        });

        tl.to(book, { clipPath: 'inset(0 0% 0 0% round 8px)', scale: 1, y: 0, duration: 2.2, ease: 'power2.inOut' })
          .to(pageContent, { opacity: 1, y: 0, duration: 0.9, stagger: 0.06, ease: 'power2.out' }, 1.3)
          .to({}, { duration: 0.7 });

        return () => tl.kill();
    });
}

// 14. Pinned destination story
function initForgeCountries() {
    const section = document.getElementById('pinned-countries-section');
    if (!section) return;

    const countryData = [
        {
            index: "DESTINATION 01 / 07",
            title: "Uzbekistan",
            desc: "Access to 7 government medical institutes within Stellar's 60+ college network, with structured guidance from selection through admission.",
            institutes: "7 government institutes",
            budget: "₹30–35 lakh",
            tieups: "Government-only network",
            img: "/assets/images/countries/uzbekistan-campus.jpg",
            ctaText: "View affiliated universities",
            ctaHref: "/universities"
        },
        {
            index: "DESTINATION 02 / 07",
            title: "Kyrgyzstan",
            desc: "Five government medical institutes offering an accessible MBBS pathway, supported by transparent counselling and end-to-end admission guidance.",
            institutes: "5 government institutes",
            budget: "₹30–35 lakh",
            tieups: "Government-only network",
            img: "/assets/images/countries/kyrgyzstan-campus.jpg",
            ctaText: "View affiliated universities",
            ctaHref: "/universities"
        },
        {
            index: "DESTINATION 03 / 07",
            title: "Kazakhstan",
            desc: "A broad choice of 10–12 government medical institutes, paired with practical counselling on university fit, budget, and student readiness.",
            institutes: "10–12 government institutes",
            budget: "₹30–35 lakh",
            tieups: "Government-only network",
            img: "/assets/images/countries/kazakhstan-campus.jpg",
            ctaText: "View affiliated universities",
            ctaHref: "/universities"
        },
        {
            index: "DESTINATION 04 / 07",
            title: "Russia",
            desc: "Stellar's largest government-college ecosystem, including 10+ high-level institutional tie-ups and options across established medical education hubs.",
            institutes: "60+ government institutes",
            budget: "₹27–45 lakh",
            tieups: "10+ high-level tie-ups",
            img: "/assets/images/countries/russia-campus.jpg",
            ctaText: "View affiliated universities",
            ctaHref: "/universities"
        },
        {
            index: "DESTINATION 05 / 07",
            title: "Bangladesh",
            desc: "A substantial network of 37 government medical institutes, including 15+ high-level tie-ups and a familiar South Asian academic environment.",
            institutes: "37 government institutes",
            budget: "₹32–45 lakh",
            tieups: "15+ high-level tie-ups",
            img: "/assets/images/countries/bangladesh-campus.jpg",
            ctaText: "View affiliated universities",
            ctaHref: "/universities"
        },
        {
            index: "DESTINATION 06 / 07",
            title: "Georgia",
            desc: "A focused selection of 4–5 government medical institutes with counselling that explains the destination, estimated cost, and institutional fit clearly.",
            institutes: "4–5 government institutes",
            budget: "₹38–55 lakh",
            tieups: "Government-only network",
            img: "/assets/images/countries/georgia-campus.jpg",
            ctaText: "View affiliated universities",
            ctaHref: "/universities"
        },
        {
            index: "DESTINATION 07 / 07",
            title: "Nepal",
            desc: "Eight to nine government medical institutes with close cultural proximity to India and personalised guidance for students and families.",
            institutes: "8–9 government institutes",
            budget: "₹57–80 lakh",
            tieups: "Government-only network",
            img: "/assets/images/countries/nepal-campus.webp",
            ctaText: "View affiliated universities",
            ctaHref: "/universities"
        }
    ];

    const panesHost = document.getElementById('country-story-panes');
    const visualsHost = document.getElementById('country-story-visuals');
    const progressHost = document.getElementById('country-story-progress');
    const ambientHost = section.querySelector('.countries-story__ambient');
    const visualIndex = document.getElementById('country-visual-index');
    if (!panesHost || !visualsHost || !progressHost || !ambientHost) return;

    panesHost.innerHTML = countryData.map((country, index) => `
        <article class="country-story-pane${index === 0 ? ' active' : ''}" data-country="${index}">
            <p class="country-story-pane__index">${country.index}</p>
            <h2 class="country-story-pane__title"${index === 0 ? ' id="countries-story-title"' : ''}>${country.title}</h2>
            <p class="country-story-pane__description">${country.desc}</p>
            <dl class="country-story-pane__specs">
                <div><dt>Government institutes</dt><dd>${country.institutes}</dd></div>
                <div><dt>Estimated total budget</dt><dd>${country.budget}</dd></div>
                <div><dt>Institutional access</dt><dd>${country.tieups}</dd></div>
            </dl>
            <a class="country-story-pane__cta" href="${country.ctaHref}">${country.ctaText}<span aria-hidden="true">↗</span></a>
        </article>
    `).join('');

    const shade = visualsHost.querySelector('.countries-story__visual-shade');
    countryData.forEach((country, index) => {
        const layer = document.createElement('div');
        layer.className = `country-story-image${index === 0 ? ' active' : ''}`;
        layer.dataset.country = index;
        layer.innerHTML = `<img src="${country.img}" alt="Government medical education campus in ${country.title}" loading="${index === 0 ? 'eager' : 'lazy'}">`;
        visualsHost.insertBefore(layer, shade);

        const ambient = document.createElement('div');
        ambient.className = `country-story-ambient${index === 0 ? ' active' : ''}`;
        ambient.style.backgroundImage = `url('${country.img}')`;
        ambientHost.appendChild(ambient);

        const button = document.createElement('button');
        button.type = 'button';
        button.className = `country-story-progress-dot${index === 0 ? ' active' : ''}`;
        button.dataset.country = index;
        button.setAttribute('aria-label', `Show ${country.title}`);
        progressHost.appendChild(button);

        const preload = new Image();
        preload.src = country.img;
    });

    const panes = Array.from(panesHost.querySelectorAll('.country-story-pane'));
    const images = Array.from(visualsHost.querySelectorAll('.country-story-image'));
    const ambientLayers = Array.from(ambientHost.querySelectorAll('.country-story-ambient'));
    const dots = Array.from(progressHost.querySelectorAll('.country-story-progress-dot'));
    const railFill = document.getElementById('country-story-rail-fill');

    const setActiveCountry = (index) => {
        dots.forEach((dot, dotIndex) => dot.classList.toggle('active', dotIndex === index));
        if (visualIndex) visualIndex.textContent = `${String(index + 1).padStart(2, '0')} / ${String(countryData.length).padStart(2, '0')}`;
    };

    if (typeof gsap === 'undefined' || typeof ScrollTrigger === 'undefined' || window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        setActiveCountry(0);
        return;
    }

    gsap.registerPlugin(ScrollTrigger);
    const mm = gsap.matchMedia();

    const buildTimeline = (isDesktop) => {
        gsap.set(panes, { autoAlpha: 0, y: 34, pointerEvents: 'none' });
        gsap.set(panes[0], { autoAlpha: 1, y: 0, pointerEvents: 'auto' });
        gsap.set(images, { autoAlpha: 0, scale: 1.08, clipPath: isDesktop ? 'inset(0 50% 0 50%)' : 'inset(50% 0 50% 0)' });
        gsap.set(images[0], { autoAlpha: 1, scale: 1, clipPath: 'inset(0 0% 0 0%)', zIndex: 2 });
        gsap.set(ambientLayers, { autoAlpha: 0 });
        gsap.set(ambientLayers[0], { autoAlpha: 0.34 });

        const tl = gsap.timeline({
            scrollTrigger: {
                trigger: section,
                start: 'top top',
                end: isDesktop ? '+=8400' : '+=5600',
                pin: section.querySelector('.countries-story__sticky'),
                scrub: isDesktop ? 1.2 : 0.9,
                anticipatePin: 1,
                invalidateOnRefresh: true,
                snap: {
                    snapTo: 1 / (countryData.length - 1),
                    duration: { min: 0.18, max: 0.5 },
                    delay: 0.12,
                    ease: 'power2.out'
                }
            },
            onUpdate: () => {
                const activeIndex = Math.min(countryData.length - 1, Math.round(tl.progress() * (countryData.length - 1)));
                setActiveCountry(activeIndex);
                if (railFill) railFill.style.width = `${(tl.progress() * 100).toFixed(2)}%`;
            }
        });

        let cursor = 0;
        tl.to(images[0].querySelector('img'), { scale: 1.035, duration: 1.45, ease: 'none' }, cursor);
        cursor += 1.45;

        for (let index = 1; index < countryData.length; index += 1) {
            const previousPane = panes[index - 1];
            const nextPane = panes[index];
            const previousImage = images[index - 1];
            const nextImage = images[index];

            tl.to(previousPane, { autoAlpha: 0, y: -28, duration: 0.42, ease: 'power2.in', pointerEvents: 'none' }, cursor)
              .to(previousImage, { autoAlpha: 0.18, scale: 1.07, duration: 0.75, ease: 'power2.inOut' }, cursor)
              .to(ambientLayers[index - 1], { autoAlpha: 0, duration: 0.75, ease: 'power1.inOut' }, cursor)
              .set(nextImage, { zIndex: index + 2, autoAlpha: 1 }, cursor)
              .to(nextImage, { clipPath: 'inset(0 0% 0 0%)', scale: 1, duration: 0.92, ease: 'power2.inOut' }, cursor)
              .to(nextPane, { autoAlpha: 1, y: 0, duration: 0.62, ease: 'power2.out', pointerEvents: 'auto' }, cursor + 0.28)
              .to(ambientLayers[index], { autoAlpha: 0.34, duration: 0.8, ease: 'power1.inOut' }, cursor + 0.15);

            cursor += 0.95;
            tl.to(nextImage.querySelector('img'), { scale: 1.035, duration: 1.35, ease: 'none' }, cursor);
            cursor += 1.35;
        }

        tl.to({}, { duration: 0.7 });

        dots.forEach((dot, index) => {
            dot.onclick = () => {
                const trigger = tl.scrollTrigger;
                if (!trigger) return;
                const destination = trigger.start + (index / (countryData.length - 1)) * (trigger.end - trigger.start);
                window.scrollTo({ top: destination, behavior: 'smooth' });
            };
        });

        return () => tl.kill();
    };

    mm.add('(min-width: 900px)', () => buildTimeline(true));
    mm.add('(max-width: 899px)', () => buildTimeline(false));
}

// 15. Pinned Editorial Doctor Counselors Controller
function initForgeDoctors() {
    const section = document.getElementById('pinned-doctors-section');
    if (!section) return;

    if (typeof gsap === 'undefined' || typeof ScrollTrigger === 'undefined') {
        console.warn('GSAP or ScrollTrigger not loaded; falling back.');
        return;
    }

    gsap.registerPlugin(ScrollTrigger);

    const panes = Array.from(section.querySelectorAll('.doctor-pane'));
    const photoLayers = Array.from(section.querySelectorAll('.doctor-photo-layer'));
    const ambientLayers = Array.from(section.querySelectorAll('.doctors-ambient-layer'));
    const pills = Array.from(section.querySelectorAll('.doctors-story__progress-pill'));
    const badgeEl = document.getElementById('doctor-badge-status');

    if (!panes.length || !photoLayers.length) return;

    const doctorCount = panes.length;
    const doctorBadges = [
        "AVAILABLE FOR CONSULTATION",
        "AVAILABLE FOR CONSULTATION",
        "AVAILABLE FOR CONSULTATION",
        "SENIOR ACADEMIC DIRECTOR"
    ];

    // Preload all doctor imagery before scrub begins
    const doctorImageSources = [
        '/assets/images/nishu_yadav.jpg',
        '/assets/images/lokesh_attri.jpg',
        '/assets/images/bindu_tyagi.jpg',
        'https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=800&q=80'
    ];
    doctorImageSources.forEach(src => {
        const img = new Image();
        img.src = src;
    });

    // Reduced motion preference: static presentation
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        panes.forEach((p, i) => {
            p.style.position = 'relative';
            p.style.opacity = '1';
            p.style.pointerEvents = 'auto';
        });
        photoLayers.forEach((layer, i) => {
            layer.style.position = 'relative';
            layer.style.opacity = '1';
        });
        return;
    }

    // Master doctor transition builder
    function addDoctorTransition(tl, startTime, fromIdx, toIdx, duration, isDesktop) {
        const fromPane = panes[fromIdx];
        const toPane = panes[toIdx];
        const fromPhoto = photoLayers[fromIdx];
        const toPhoto = photoLayers[toIdx];
        const fromImg = fromPhoto ? fromPhoto.querySelector('.doctor-photo-img') : null;
        const toImg = toPhoto ? toPhoto.querySelector('.doctor-photo-img') : null;

        // --- Photo Layers Transition ---
        if (fromPhoto) {
            // Outgoing photo drifts subtly and fades
            tl.to(fromPhoto, {
                scale: 1.04,
                opacity: 0,
                duration: duration * 0.85,
                ease: "power2.inOut"
            }, startTime);
            if (fromImg) {
                tl.to(fromImg, {
                    scale: 1.03,
                    duration: duration,
                    ease: "power1.out"
                }, startTime);
            }
        }

        if (toPhoto) {
            // Incoming photo is brought above (zIndex: 2)
            tl.set(toPhoto, { zIndex: 2, opacity: 1 }, startTime);

            if (isDesktop) {
                // Signature Forge center-outward curtain reveal:
                // Begins as a 0-width slit in exact center (50% left, 50% right)
                // Opens smoothly outward to full frame (0% left, 0% right)
                tl.fromTo(toPhoto, {
                    clipPath: "inset(0% 50% 0% 50%)",
                    scale: 1.08
                }, {
                    clipPath: "inset(0% 0% 0% 0%)",
                    scale: 1.0,
                    duration: duration,
                    ease: "power2.inOut"
                }, startTime);
            } else {
                // Mobile optimized: smooth crossfade + gentle scale settling
                tl.fromTo(toPhoto, {
                    opacity: 0,
                    scale: 1.06
                }, {
                    opacity: 1,
                    scale: 1.0,
                    duration: duration,
                    ease: "power2.out"
                }, startTime);
            }

            if (toImg) {
                tl.fromTo(toImg, {
                    scale: 1.06
                }, {
                    scale: 1.0,
                    duration: duration,
                    ease: "power2.out"
                }, startTime);
            }
        }

        // --- Typography & Editorial Pane Transition ---
        if (fromPane) {
            const fIndex = fromPane.querySelector('.doctor-pane__index');
            const fLabel = fromPane.querySelector('.doctor-pane__label');
            const fName = fromPane.querySelector('.doctor-pane__name');
            const fRole = fromPane.querySelector('.doctor-pane__role');
            const fBio = fromPane.querySelector('.doctor-pane__bio');
            const fCta = fromPane.querySelector('.doctor-pane__cta');

            // Staggered exit upward
            tl.to([fIndex, fLabel], { y: -24, opacity: 0, duration: duration * 0.35, ease: "power2.in" }, startTime);
            tl.to(fName, { y: -65, opacity: 0, duration: duration * 0.45, ease: "power2.in" }, startTime + duration * 0.08);
            tl.to(fRole, { y: -30, opacity: 0, duration: duration * 0.4, ease: "power2.in" }, startTime + duration * 0.12);
            tl.to(fBio, { y: -28, opacity: 0, duration: duration * 0.45, ease: "power2.in" }, startTime + duration * 0.16);
            tl.to(fCta, { y: -20, opacity: 0, duration: duration * 0.35, ease: "power2.in" }, startTime + duration * 0.2);

            tl.set(fromPane, { pointerEvents: "none", opacity: 0 }, startTime + duration * 0.6);
        }

        if (toPane) {
            const tIndex = toPane.querySelector('.doctor-pane__index');
            const tLabel = toPane.querySelector('.doctor-pane__label');
            const tName = toPane.querySelector('.doctor-pane__name');
            const tRole = toPane.querySelector('.doctor-pane__role');
            const tBio = toPane.querySelector('.doctor-pane__bio');
            const tCta = toPane.querySelector('.doctor-pane__cta');

            tl.set(toPane, { opacity: 1 }, startTime + duration * 0.25);
            tl.set(toPane, { pointerEvents: "auto" }, startTime + duration * 0.6);

            // Staggered entry from below
            tl.fromTo([tIndex, tLabel], { y: 24, opacity: 0 }, { y: 0, opacity: 1, duration: duration * 0.45, ease: "power2.out" }, startTime + duration * 0.3);
            tl.fromTo(tName, { y: 65, opacity: 0 }, { y: 0, opacity: 1, duration: duration * 0.55, ease: "power2.out" }, startTime + duration * 0.38);
            tl.fromTo(tRole, { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: duration * 0.48, ease: "power2.out" }, startTime + duration * 0.44);
            tl.fromTo(tBio, { y: 28, opacity: 0 }, { y: 0, opacity: 1, duration: duration * 0.5, ease: "power2.out" }, startTime + duration * 0.48);
            tl.fromTo(tCta, { y: 20, opacity: 0 }, { y: 0, opacity: 1, duration: duration * 0.45, ease: "power2.out" }, startTime + duration * 0.52);
        }

        // --- Ambient Backdrop Transition ---
        if (ambientLayers[fromIdx]) {
            tl.to(ambientLayers[fromIdx], { opacity: 0, duration: duration * 0.8, ease: "power1.inOut" }, startTime);
        }
        if (ambientLayers[toIdx]) {
            tl.to(ambientLayers[toIdx], { opacity: 0.5, duration: duration * 0.8, ease: "power1.inOut" }, startTime + duration * 0.2);
        }
    }

    const mm = gsap.matchMedia();

    // ========================================================
    // DESKTOP / TABLET LANDSCAPE (>= 1024px)
    // ========================================================
    mm.add("(min-width: 1024px)", () => {
        // Initial setup
        panes.forEach((pane, i) => {
            const isFirst = i === 0;
            gsap.set(pane, { opacity: isFirst ? 1 : 0, pointerEvents: isFirst ? "auto" : "none" });
            const idxEl = pane.querySelector('.doctor-pane__index');
            const labelEl = pane.querySelector('.doctor-pane__label');
            const nameEl = pane.querySelector('.doctor-pane__name');
            const roleEl = pane.querySelector('.doctor-pane__role');
            const bioEl = pane.querySelector('.doctor-pane__bio');
            const ctaEl = pane.querySelector('.doctor-pane__cta');

            if (isFirst) {
                gsap.set([idxEl, labelEl, nameEl, roleEl, bioEl, ctaEl], { y: 0, opacity: 1 });
            } else {
                gsap.set([idxEl, labelEl], { y: 24, opacity: 0 });
                gsap.set(nameEl, { y: 65, opacity: 0 });
                gsap.set(roleEl, { y: 30, opacity: 0 });
                gsap.set(bioEl, { y: 28, opacity: 0 });
                gsap.set(ctaEl, { y: 20, opacity: 0 });
            }
        });

        photoLayers.forEach((layer, i) => {
            const img = layer.querySelector('.doctor-photo-img');
            if (i === 0) {
                gsap.set(layer, { opacity: 1, scale: 1.0, clipPath: "inset(0% 0% 0% 0%)", zIndex: 1 });
                if (img) gsap.set(img, { scale: 1.0 });
            } else {
                gsap.set(layer, { opacity: 0, scale: 1.08, clipPath: "inset(0% 50% 0% 50%)", zIndex: 0 });
                if (img) gsap.set(img, { scale: 1.0 });
            }
        });

        ambientLayers.forEach((amb, i) => {
            gsap.set(amb, { opacity: i === 0 ? 0.5 : 0 });
        });

        pills.forEach((p, i) => {
            if (i === 0) p.classList.add('active');
            else p.classList.remove('active');
        });

        if (badgeEl) badgeEl.textContent = doctorBadges[0];

        // Master Timeline: 60% Hold, 40% Transition, Scrub: 1
        const tl = gsap.timeline({
            scrollTrigger: {
                trigger: section,
                start: "top top",
                end: "+=6200",
                pin: true,
                scrub: 1.15,
                anticipatePin: 1,
                invalidateOnRefresh: true,
                snap: {
                    snapTo: 1 / 3,
                    duration: { min: 0.18, max: 0.5 },
                    delay: 0.12,
                    ease: "power2.out"
                }
            },
            onUpdate: () => {
                const curTime = tl.time();
                let activeDoc = 0;
                if (curTime >= 7.3) activeDoc = 3;
                else if (curTime >= 4.7) activeDoc = 2;
                else if (curTime >= 2.1) activeDoc = 1;
                else activeDoc = 0;

                pills.forEach((p, k) => {
                    if (k === activeDoc) p.classList.add('active');
                    else p.classList.remove('active');
                });

                if (badgeEl && doctorBadges[activeDoc]) {
                    badgeEl.textContent = doctorBadges[activeDoc];
                }
            }
        });

        const HOLD = 1.6;
        const TRANS = 1.0;

        // Scene 0: Dr. Nishu Yadav Hold (t: 0 -> 1.6)
        const img0 = photoLayers[0].querySelector('.doctor-photo-img');
        if (img0) {
            tl.to(img0, { scale: 1.025, duration: HOLD, ease: "none" }, 0);
        }

        // Transition 0 -> 1 (t: 1.6 -> 2.6)
        addDoctorTransition(tl, 1.6, 0, 1, TRANS, true);

        // Scene 1: Dr. Lokesh Attri Hold (t: 2.6 -> 4.2)
        const img1 = photoLayers[1].querySelector('.doctor-photo-img');
        if (img1) {
            tl.to(img1, { scale: 1.025, duration: HOLD, ease: "none" }, 2.6);
        }

        // Transition 1 -> 2 (t: 4.2 -> 5.2)
        addDoctorTransition(tl, 4.2, 1, 2, TRANS, true);

        // Scene 2: Dr. Bindu Tyagi Hold (t: 5.2 -> 6.8)
        const img2 = photoLayers[2].querySelector('.doctor-photo-img');
        if (img2) {
            tl.to(img2, { scale: 1.025, duration: HOLD, ease: "none" }, 5.2);
        }

        // Transition 2 -> 3 (t: 6.8 -> 7.8)
        addDoctorTransition(tl, 6.8, 2, 3, TRANS, true);

        // Scene 3: Dr. Vikram Singh Hold (t: 7.8 -> 9.4)
        const img3 = photoLayers[3].querySelector('.doctor-photo-img');
        if (img3) {
            tl.to(img3, { scale: 1.025, duration: HOLD, ease: "none" }, 7.8);
        }

        // Outro buffer before unpin (t: 9.4 -> 9.8)
        tl.to(photoLayers[3], { scale: 1.02, duration: 0.4, ease: "none" }, 9.4);

        // Pill click jumps to precise hold centers
        const pillTargets = [0.8 / 9.8, 3.4 / 9.8, 6.0 / 9.8, 8.6 / 9.8];
        pills.forEach((btn, idx) => {
            btn.onclick = (e) => {
                e.preventDefault();
                const st = tl.scrollTrigger;
                if (st) {
                    const targetScroll = st.start + pillTargets[idx] * (st.end - st.start);
                    window.scrollTo({ top: targetScroll, behavior: 'smooth' });
                }
            };
        });

        return () => {
            tl.kill();
        };
    });

    // ========================================================
    // MOBILE / TABLET PORTRAIT (< 1024px)
    // ========================================================
    mm.add("(max-width: 1023px)", () => {
        // Initial setup for mobile
        panes.forEach((pane, i) => {
            const isFirst = i === 0;
            gsap.set(pane, { opacity: isFirst ? 1 : 0, pointerEvents: isFirst ? "auto" : "none" });
            const allKids = pane.children;
            if (isFirst) {
                gsap.set(allKids, { y: 0, opacity: 1 });
            } else {
                gsap.set(allKids, { y: 20, opacity: 0 });
            }
        });

        photoLayers.forEach((layer, i) => {
            if (i === 0) {
                gsap.set(layer, { opacity: 1, scale: 1.0, zIndex: 1 });
            } else {
                gsap.set(layer, { opacity: 0, scale: 1.06, zIndex: 0 });
            }
        });

        ambientLayers.forEach((amb, i) => {
            gsap.set(amb, { opacity: i === 0 ? 0.4 : 0 });
        });

        pills.forEach((p, i) => {
            if (i === 0) p.classList.add('active');
            else p.classList.remove('active');
        });

        if (badgeEl) badgeEl.textContent = doctorBadges[0];

        const tl = gsap.timeline({
            scrollTrigger: {
                trigger: section,
                start: "top top",
                end: "+=4000",
                pin: true,
                scrub: 1,
                anticipatePin: 1,
                invalidateOnRefresh: true,
                snap: {
                    snapTo: 1 / 3,
                    duration: { min: 0.16, max: 0.42 },
                    delay: 0.1,
                    ease: "power2.out"
                }
            },
            onUpdate: () => {
                const curTime = tl.time();
                let activeDoc = 0;
                if (curTime >= 5.6) activeDoc = 3;
                else if (curTime >= 3.6) activeDoc = 2;
                else if (curTime >= 1.6) activeDoc = 1;
                else activeDoc = 0;

                pills.forEach((p, k) => {
                    if (k === activeDoc) p.classList.add('active');
                    else p.classList.remove('active');
                });

                if (badgeEl && doctorBadges[activeDoc]) {
                    badgeEl.textContent = doctorBadges[activeDoc];
                }
            }
        });

        const HOLD = 1.2;
        const TRANS = 0.8;

        // Transitions for mobile
        addDoctorTransition(tl, 1.2, 0, 1, TRANS, false);
        addDoctorTransition(tl, 3.2, 1, 2, TRANS, false);
        addDoctorTransition(tl, 5.2, 2, 3, TRANS, false);
        tl.to({}, { duration: 1.0 }, 6.0); // final hold

        return () => {
            tl.kill();
        };
    });
}
