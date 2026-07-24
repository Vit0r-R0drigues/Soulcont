document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-reviews-carousel]').forEach((carousel) => {
        const viewport = carousel.querySelector('[data-reviews-viewport]');
        const track = carousel.querySelector('.reviews-carousel__track');
        const previousButton = carousel.querySelector('[data-reviews-prev]');
        const autoplayButton = carousel.querySelector('[data-reviews-toggle]');
        const nextButton = carousel.querySelector('[data-reviews-next]');

        if (!viewport || !track || !previousButton || !autoplayButton || !nextButton) {
            return;
        }

        const reducedMotionQuery = window.matchMedia
            ? window.matchMedia('(prefers-reduced-motion: reduce)')
            : null;
        const autoplayDelay = 6500;
        let autoplayTimer = null;
        let autoplayPaused = !!reducedMotionQuery?.matches;
        let focusWithinCarousel = false;

        const updateControls = () => {
            const maximumScroll = Math.max(0, viewport.scrollWidth - viewport.clientWidth);
            previousButton.disabled = viewport.scrollLeft <= 2;
            nextButton.disabled = viewport.scrollLeft >= maximumScroll - 2;
        };

        const moveCarousel = (direction) => {
            const firstCard = track.querySelector('.review-card');
            if (!firstCard) {
                return;
            }

            const trackStyles = window.getComputedStyle(track);
            const gap = Number.parseFloat(trackStyles.columnGap || trackStyles.gap || '0');
            const cardWidth = firstCard.getBoundingClientRect().width;

            viewport.scrollBy({
                left: direction * (cardWidth + gap),
                behavior: reducedMotionQuery?.matches ? 'auto' : 'smooth'
            });
        };

        const stopAutoplay = () => {
            if (autoplayTimer !== null) {
                window.clearTimeout(autoplayTimer);
                autoplayTimer = null;
            }
        };

        const updateAutoplayButton = () => {
            const buttonIcon = autoplayButton.querySelector('span');
            autoplayButton.setAttribute('aria-pressed', String(autoplayPaused));
            autoplayButton.setAttribute(
                'aria-label',
                autoplayPaused ? 'Retomar rotação automática' : 'Pausar rotação automática'
            );

            if (buttonIcon) {
                buttonIcon.textContent = autoplayPaused ? '▶' : 'Ⅱ';
            }
        };

        const advanceAutomatically = () => {
            const maximumScroll = Math.max(0, viewport.scrollWidth - viewport.clientWidth);
            const behavior = reducedMotionQuery?.matches ? 'auto' : 'smooth';

            if (viewport.scrollLeft >= maximumScroll - 2) {
                viewport.scrollTo({ left: 0, behavior });
            } else {
                moveCarousel(1);
            }
        };

        const scheduleAutoplay = () => {
            stopAutoplay();

            if (autoplayPaused || focusWithinCarousel || document.hidden) {
                return;
            }

            autoplayTimer = window.setTimeout(() => {
                advanceAutomatically();
                scheduleAutoplay();
            }, autoplayDelay);
        };

        previousButton.addEventListener('click', () => {
            moveCarousel(-1);
            scheduleAutoplay();
        });
        nextButton.addEventListener('click', () => {
            moveCarousel(1);
            scheduleAutoplay();
        });
        autoplayButton.addEventListener('click', () => {
            autoplayPaused = !autoplayPaused;
            updateAutoplayButton();
            scheduleAutoplay();
        });
        viewport.addEventListener('scroll', updateControls, { passive: true });
        viewport.addEventListener('pointerdown', stopAutoplay);
        viewport.addEventListener('pointerup', scheduleAutoplay);
        viewport.addEventListener('pointercancel', scheduleAutoplay);
        carousel.addEventListener('focusin', () => {
            focusWithinCarousel = true;
            stopAutoplay();
        });
        carousel.addEventListener('focusout', (event) => {
            if (event.relatedTarget && carousel.contains(event.relatedTarget)) {
                return;
            }

            focusWithinCarousel = false;
            scheduleAutoplay();
        });
        document.addEventListener('visibilitychange', scheduleAutoplay);
        window.addEventListener('resize', updateControls);

        if (typeof reducedMotionQuery?.addEventListener === 'function') {
            reducedMotionQuery.addEventListener('change', (event) => {
                autoplayPaused = event.matches;
                updateAutoplayButton();
                scheduleAutoplay();
            });
        }

        updateControls();
        updateAutoplayButton();
        scheduleAutoplay();
    });

    if (!window.VLMotion) {
        return;
    }

    const motion = window.VLMotion;
    const page = document.body?.dataset.page || '';

    motion.applyRootState();
    motion.initTapFeedback();
    motion.initSwapValues();

    const revealConfigs = [
        '.page-hero > *',
        '.detail-hero > *',
        '.section-heading',
        '.final-cta-panel > *',
        '.responsible-card > *',
        '.contact-form-panel > *',
        { container: '.grid-2, .grid-3, .process-grid, .faq-grid-v2, .fit-grid, .contact-grid-v2, .service-overview-grid, .audience-grid, .services-home-grid, .trust-metric-row, .hero-proof-band', itemSelector: ':scope > *', step: 70 },
        { container: '.faq-details', itemSelector: ':scope > details', step: 70 },
        { container: '.service-anchor-row', itemSelector: ':scope > a', step: 48, baseDelay: 90 },
        { container: '.request-options', itemSelector: ':scope > *', step: 70 }
    ];

    if (page === 'home') {
        revealConfigs.push(
            '.hero-visual-card > *',
            { container: '.hero-direct-links, .audience-track-list, .audience-callout-actions, .proof-support-list', itemSelector: ':scope > *', step: 70 },
            '.proof-support-header > *',
            { container: '.audience-layout', itemSelector: ':scope > *', step: 110 },
            '.audience-fusion-panel .section-heading',
            '.services-home-panel .section-heading',
            '.dre-section .section-heading',
            { container: '.dre-layout', itemSelector: ':scope > *', step: 120 },
            '.dre-footnote'
        );
    }

    if (page === 'ir-2026') {
        revealConfigs.push('.hero', '.intro-card', '.quiz-shell', '.faq-shell');
    }

    motion.markRevealTargets(revealConfigs);
    motion.initRevealTargets();
    motion.initCountUps();
    motion.initParallaxScene();
    motion.initDreSection();
    motion.initTaxHero();
    motion.initFormEnhancements();
    motion.initIr2026Enhancements();

    if (page === 'home') {
        const homeFloat = document.querySelector('.whatsapp-float');
        const homeHero = document.querySelector('.hero-home-premium');
        const heroProofBand = document.querySelector('.hero-proof-band');
        const audiencePanel = document.querySelector('.audience-fusion-panel');
        const mobileFloatQuery = window.matchMedia('(max-width: 640px)');

        const syncHomeFloat = () => {
            if (!homeFloat || !homeHero) {
                return;
            }

            const thresholdAnchor = mobileFloatQuery.matches
                ? (audiencePanel || heroProofBand || homeHero)
                : (heroProofBand || homeHero);
            const threshold = thresholdAnchor.offsetTop + thresholdAnchor.offsetHeight - Math.min(window.innerHeight * 0.18, 120);
            const shouldShow = !mobileFloatQuery.matches || window.scrollY > threshold;
            document.body.classList.toggle('home-float-active', shouldShow);
        };

        syncHomeFloat();
        window.addEventListener('scroll', syncHomeFloat, { passive: true });
        window.addEventListener('resize', syncHomeFloat);

        if (typeof mobileFloatQuery.addEventListener === 'function') {
            mobileFloatQuery.addEventListener('change', syncHomeFloat);
        } else if (typeof mobileFloatQuery.addListener === 'function') {
            mobileFloatQuery.addListener(syncHomeFloat);
        }
    }
});
