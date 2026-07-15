class MobileMenu {
    static instance = null;

    constructor() {
        if (MobileMenu.instance) {
            return MobileMenu.instance;
        }

        this.header = document.querySelector('header, .site-header');
        this.menuBtn = document.getElementById('btn-mobile');
        this.navMenu = document.querySelector('header nav, .site-header nav');

        if (!this.header || !this.navMenu) {
            return;
        }

        if (!this.menuBtn) {
            this.createMenuButton();
        }

        this.toggleMenu = this.toggleMenu.bind(this);
        this.handleDocumentClick = this.handleDocumentClick.bind(this);
        this.handleLinkClick = this.handleLinkClick.bind(this);
        this.handleEscape = this.handleEscape.bind(this);
        this.handleFocusTrap = this.handleFocusTrap.bind(this);

        this.init();
        MobileMenu.instance = this;
    }

    createMenuButton() {
        const menuMobile = document.createElement('div');
        menuMobile.className = 'menu-mobile';
        menuMobile.innerHTML = `
            <button class="menu-toggle" aria-label="Abrir menu" aria-expanded="false" id="btn-mobile">
                <span class="menu-toggle-glyph" aria-hidden="true">&#9776;</span>
            </button>
        `;

        this.header.appendChild(menuMobile);
        this.menuBtn = menuMobile.querySelector('#btn-mobile');
    }

    init() {
        if (!this.menuBtn) {
            return;
        }

        this.setButtonGlyph(false);
        this.ensureAccessibleStructure();
        this.menuBtn.addEventListener('click', this.toggleMenu);
        document.addEventListener('click', this.handleDocumentClick);
        document.addEventListener('keydown', this.handleEscape);
        document.addEventListener('keydown', this.handleFocusTrap);

        this.navMenu.querySelectorAll('a').forEach((link) => {
            link.addEventListener('click', this.handleLinkClick);
        });
    }

    ensureAccessibleStructure() {
        if (!this.navMenu.id) {
            this.navMenu.id = 'navegacao-principal';
        }

        this.menuBtn.setAttribute('aria-controls', this.navMenu.id);

        const main = document.querySelector('main');
        if (main && !main.id) {
            main.id = 'conteudo-principal';
        }

        if (main && !document.querySelector('.skip-link')) {
            const skipLink = document.createElement('a');
            skipLink.className = 'skip-link';
            skipLink.href = `#${main.id}`;
            skipLink.textContent = 'Pular para o conteúdo principal';
            document.body.prepend(skipLink);
        }
    }

    toggleMenu(event) {
        if (event) {
            event.stopPropagation();
        }

        const isActive = this.navMenu.classList.toggle('active');
        this.menuBtn.classList.toggle('active', isActive);

        this.setButtonGlyph(isActive);

        this.menuBtn.setAttribute('aria-expanded', String(isActive));
        document.body.style.overflow = isActive ? 'hidden' : '';
        this.setBackgroundInert(isActive);

        if (isActive) {
            const firstLink = this.navMenu.querySelector('a');
            firstLink?.focus();
        }
    }

    closeMenu(restoreFocus = true) {
        if (!this.navMenu.classList.contains('active')) {
            return;
        }

        this.navMenu.classList.remove('active');
        this.menuBtn?.classList.remove('active');
        this.setButtonGlyph(false);
        this.menuBtn?.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
        this.setBackgroundInert(false);

        if (restoreFocus) {
            this.menuBtn?.focus();
        }
    }

    setBackgroundInert(isInert) {
        document.querySelectorAll('main, footer, .social-icons, .whatsapp-float').forEach((element) => {
            if ('inert' in element) {
                element.inert = isInert;
            }
            element.toggleAttribute('aria-hidden', isInert);
        });
    }

    setButtonGlyph(isActive) {
        if (!this.menuBtn) {
            return;
        }

        let glyph = this.menuBtn.querySelector('.menu-toggle-glyph');
        if (!glyph) {
            glyph = document.createElement('span');
            glyph.className = 'menu-toggle-glyph';
            glyph.setAttribute('aria-hidden', 'true');
            this.menuBtn.innerHTML = '';
            this.menuBtn.appendChild(glyph);
        }

        glyph.innerHTML = isActive ? '&times;' : '&#9776;';
    }

    handleDocumentClick(event) {
        if (!this.navMenu.classList.contains('active')) {
            return;
        }

        const clickedInsideMenu = event.target.closest('nav');
        const clickedToggle = event.target.closest('.menu-mobile');

        if (!clickedInsideMenu && !clickedToggle) {
            this.closeMenu();
        }
    }

    handleLinkClick() {
        this.closeMenu();
    }

    handleEscape(event) {
        if (event.key === 'Escape') {
            this.closeMenu();
        }
    }

    handleFocusTrap(event) {
        if (event.key !== 'Tab' || !this.navMenu.classList.contains('active')) {
            return;
        }

        const focusable = Array.from(this.navMenu.querySelectorAll('a, button, [tabindex]:not([tabindex="-1"])'))
            .filter((element) => !element.hasAttribute('disabled'));

        if (focusable.length === 0) {
            event.preventDefault();
            this.menuBtn?.focus();
            return;
        }

        const first = focusable[0];
        const last = focusable[focusable.length - 1];

        if (event.shiftKey && document.activeElement === first) {
            event.preventDefault();
            last.focus();
        } else if (!event.shiftKey && document.activeElement === last) {
            event.preventDefault();
            first.focus();
        }
    }

    destroy() {
        this.closeMenu();

        if (this.menuBtn) {
            this.menuBtn.removeEventListener('click', this.toggleMenu);
        }

        document.removeEventListener('click', this.handleDocumentClick);
        document.removeEventListener('keydown', this.handleEscape);
        document.removeEventListener('keydown', this.handleFocusTrap);

        this.navMenu?.querySelectorAll('a').forEach((link) => {
            link.removeEventListener('click', this.handleLinkClick);
        });

        MobileMenu.instance = null;
    }
}

function initMobileMenu() {
    if (window.innerWidth <= 768) {
        if (!MobileMenu.instance) {
            new MobileMenu();
        }
    } else if (MobileMenu.instance) {
        MobileMenu.instance.destroy();
    }
}

function ensureGlobalAccessibility() {
    const navMenu = document.querySelector('header nav, .site-header nav');
    const menuBtn = document.getElementById('btn-mobile');
    const main = document.querySelector('main');

    if (navMenu && !navMenu.id) {
        navMenu.id = 'navegacao-principal';
    }

    if (menuBtn && navMenu) {
        menuBtn.setAttribute('aria-controls', navMenu.id);
    }

    if (main && !main.id) {
        main.id = 'conteudo-principal';
    }

    if (main && !document.querySelector('.skip-link')) {
        const skipLink = document.createElement('a');
        skipLink.className = 'skip-link';
        skipLink.href = `#${main.id}`;
        skipLink.textContent = 'Pular para o conteúdo principal';
        document.body.prepend(skipLink);
    }
}

function setLogoLink() {
    const logoLink = document.querySelector('header .logo a, .site-header .brand');
    if (logoLink) {
        logoLink.setAttribute('href', '/index.html');
    }
}

function markActiveLinks() {
    const currentPage = document.body.dataset.page;
    const menuLinks = document.querySelectorAll('.menu a[data-nav], .header-nav a[data-nav]');

    menuLinks.forEach((link) => {
        const linkPage = link.dataset.nav || '';
        const isActive = currentPage ? currentPage === linkPage : false;
        link.classList.toggle('active', isActive);
        if (isActive) {
            link.setAttribute('aria-current', 'page');
        } else {
            link.removeAttribute('aria-current');
        }
    });
}

function enhanceExternalLinks() {
    document.querySelectorAll('a[target="_blank"]').forEach((link) => {
        const relValues = new Set((link.getAttribute('rel') || '').split(/\s+/).filter(Boolean));
        relValues.add('noopener');
        relValues.add('noreferrer');
        link.setAttribute('rel', Array.from(relValues).join(' '));
    });
}

function routeGenericWhatsAppLinks() {
    const chooserUrl = '/HTML/contatos.html#escolher-whatsapp';
    const directContactPattern = /vitor|leonardo|são paulo|ceará|\(11\)|\(88\)|91653|92179/i;

    document.querySelectorAll('a[href*="wa.me/"]').forEach((link) => {
        const context = `${link.textContent || ''} ${link.getAttribute('title') || ''} ${link.getAttribute('aria-label') || ''}`;

        if (directContactPattern.test(context)) {
            return;
        }

        link.href = chooserUrl;
        link.removeAttribute('target');
        link.removeAttribute('rel');
        link.setAttribute('aria-label', 'Escolher WhatsApp da SoulCont');
        link.setAttribute('title', 'Escolher WhatsApp da SoulCont');
    });
}

function tagDirectWhatsAppLinks() {
    const originLine = 'Origem: Site SoulCont (soulcontt.com.br)';

    document.querySelectorAll('a[href*="wa.me/"]').forEach((link) => {
        const url = new URL(link.href);
        const existingText = url.searchParams.get('text') || 'Olá! Quero falar com a SoulCont.';

        if (existingText.includes('Origem: Site SoulCont')) {
            return;
        }

        url.searchParams.set('text', `${existingText}\n\n${originLine}\nPágina: ${document.title}`);
        link.href = url.toString();
    });
}

function initHeaderScroll() {
    const header = document.querySelector('header');

    if (!header) {
        return;
    }

    const onScroll = () => {
        header.classList.toggle('scrolled', window.scrollY > 40);
    };

    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
}

function initCalculatorHeader() {
    if (!document.querySelector('.calculadora-page')) {
        return;
    }

    const header = document.querySelector('header');
    const calculadora = document.querySelector('.calculadora-container');

    if (!header || !calculadora) {
        return;
    }

    const updateOverlap = () => {
        const headerRect = header.getBoundingClientRect();
        const calcRect = calculadora.getBoundingClientRect();
        header.classList.toggle('transparent', headerRect.bottom > calcRect.top);
    };

    window.addEventListener('scroll', updateOverlap, { passive: true });
    window.addEventListener('resize', updateOverlap);
    updateOverlap();
}

let resizeTimeout = null;

window.addEventListener('resize', () => {
    window.clearTimeout(resizeTimeout);
    resizeTimeout = window.setTimeout(initMobileMenu, 180);
});

document.addEventListener('DOMContentLoaded', () => {
    ensureGlobalAccessibility();
    initMobileMenu();
    setLogoLink();
    markActiveLinks();
    routeGenericWhatsAppLinks();
    tagDirectWhatsAppLinks();
    enhanceExternalLinks();
    initHeaderScroll();
    initCalculatorHeader();
});
