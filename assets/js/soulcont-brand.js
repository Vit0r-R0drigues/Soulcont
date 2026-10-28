(function () {
    function installWordmark() {
        document.querySelectorAll('header .logo a, .footer-brand-v2 a').forEach((anchor) => {
            if (!anchor.querySelector('img')) return;
            anchor.classList.add('soulcont-wordmark');
            anchor.setAttribute('aria-label', 'SoulCont - pagina inicial');
            anchor.innerHTML = '<img class="soulcont-wordmark__mark" src="/assets/img/soulcont/brand-mark-growth-transparent.png?v=1" alt="" width="26" height="32" aria-hidden="true"><span>SOUL</span><strong>CONT</strong>';
        });
    }

    function installHomePortraits() {
        if (!document.body.classList.contains('home-page')) return;

        const card = document.querySelector('.hero-visual-card');
        if (!card) return;

        card.innerHTML = `
            <div class="soulcont-team-hero">
                <span class="soulcont-team-hero__label">Pessoas por trás dos números</span>
                <div class="soulcont-team-hero__photos">
                    <figure class="soulcont-team-hero__person">
                        <img src="/assets/img/soulcont/vitor-rodrigues-perfil-3x4.webp?v=2" alt="Vitor Rodrigues de Lima, contador responsável da SoulCont" width="720" height="960">
                        <figcaption class="soulcont-team-hero__caption">Vitor Rodrigues de Lima<span>Contador responsável · CRC SP353836</span></figcaption>
                    </figure>
                    <figure class="soulcont-team-hero__person">
                        <img src="/assets/img/soulcont/leonardo-silva-retrato-real-640w.webp" alt="Leonardo Silva de Sousa, contador da SoulCont, no escritório" width="640" height="853">
                        <figcaption class="soulcont-team-hero__caption">Leonardo Silva de Sousa<span>Contador responsável · CRCCE 024206/O5</span></figcaption>
                    </figure>
                </div>
                <p class="soulcont-team-hero__copy">Dois contadores responsáveis para conectar rotina, tributos e decisões empresariais com clareza.</p>
            </div>`;
    }

    function installLeonardoProfile() {
        if (document.body.dataset.page !== 'about' && document.body.dataset.page !== 'home') return;

        const profile = document.querySelector('.responsible-card .founder-profile');
        if (!profile || document.querySelector('.soulcont-team-member')) return;

        profile.insertAdjacentHTML('afterend', `
            <div class="founder-profile soulcont-team-member">
                <img src="/assets/img/soulcont/leonardo-silva-retrato-real-640w.webp" alt="Leonardo Silva de Sousa no escritório da SoulCont" width="640" height="853" loading="lazy" decoding="async">
                <div>
                    <strong>Leonardo Silva de Sousa</strong>
                    <span>Contador responsável · Registro profissional: CRCCE 024206/O5</span>
                    <p class="copy-muted">Atendimento próximo e orientação prática, em pé de igualdade com Vitor, para que cada cliente saiba qual é o próximo passo.</p>
                </div>
            </div>`);
    }

    function initEditorialReveals() {
        const reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        const candidates = document.querySelectorAll(
            '.section-block .section-panel, .section-block .soulcont-feature-story, .section-block .final-cta-panel, .section-block .proof-strip'
        );

        candidates.forEach((element, index) => {
            if (element.closest('.hero-section')) return;
            element.classList.add('soul-reveal');
            element.style.setProperty('--soul-reveal-delay', `${Math.min(index % 3, 2) * 70}ms`);
        });

        if (reduceMotion || !('IntersectionObserver' in window)) {
            candidates.forEach((element) => element.classList.add('is-visible'));
            return;
        }

        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) return;
                entry.target.classList.add('is-visible');
                observer.unobserve(entry.target);
            });
        }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });

        candidates.forEach((element) => observer.observe(element));
    }

    function initFaqBehavior() {
        document.querySelectorAll('.soulcont-faq__grid, .faq-details').forEach((group) => {
            const items = Array.from(group.querySelectorAll('details'));
            items.forEach((item) => {
                const summary = item.querySelector('summary');
                if (!summary) return;

                summary.setAttribute('aria-expanded', String(item.open));
                item.addEventListener('toggle', () => {
                    summary.setAttribute('aria-expanded', String(item.open));
                    if (!item.open) return;
                    items.forEach((other) => {
                        if (other !== item) other.open = false;
                    });
                });
            });
        });
    }

    const WHATSAPP_CONTACTS = {
        ce: { number: '5588921791670', label: 'Ceará', phone: '(88) 92179-1670' },
        sp: { number: '5511916539680', label: 'São Paulo', phone: '(11) 91653-9680' }
    };

    const WHATSAPP_ICON = '<svg class="wa-dock__icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M12 2.5a9.5 9.5 0 0 0-8.2 14.3L2.5 21.5l4.8-1.3A9.5 9.5 0 1 0 12 2.5Z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M8.6 7.6c.3-.6.6-.6.9-.6h.6c.2 0 .4 0 .6.5l.8 1.9c.1.2.1.4 0 .6l-.6.8c-.1.2-.1.4 0 .6.7 1.2 1.6 2.1 2.8 2.7.2.1.4.1.6-.1l.8-.9c.2-.2.4-.2.6-.1l1.9.9c.3.1.4.3.4.5 0 .5-.2 1.3-.8 1.7-.6.4-1.4.6-2.4.3a10.6 10.6 0 0 1-6.1-5.4c-.5-1-.4-2.3.2-2.9Z" fill="currentColor"/></svg>';

    function buildWhatsAppUrl(contact) {
        const text = `Olá! Vim pelo site da SoulCont e quero conversar sobre minha empresa.\n\nPágina: ${document.title}`;
        return `https://wa.me/${contact.number}?text=${encodeURIComponent(text)}`;
    }

    function buildWhatsAppLink(contact, label) {
        const link = document.createElement('a');
        link.href = buildWhatsAppUrl(contact);
        link.target = '_blank';
        link.rel = 'noopener noreferrer';
        link.dataset.directWhatsapp = 'true';
        link.dataset.trackPosition = 'whatsapp_dock';
        link.innerHTML = label;
        return link;
    }

    // Fixed WhatsApp access on every page: direct to the regional number when the
    // page declares one (data-whatsapp-region), otherwise an inline choice between
    // Ceará and São Paulo instead of sending the visitor to the contact page.
    function installWhatsAppDock() {
        if (document.querySelector('.wa-dock')) return;
        document.querySelectorAll('.whatsapp-float').forEach((legacy) => legacy.remove());

        const region = WHATSAPP_CONTACTS[document.body.dataset.whatsappRegion];
        const dock = document.createElement('div');
        dock.className = 'wa-dock';

        if (region) {
            const direct = buildWhatsAppLink(region, `${WHATSAPP_ICON}<span>Falar no WhatsApp</span>`);
            direct.className = 'wa-dock__button';
            dock.appendChild(direct);
            document.body.appendChild(dock);
            return;
        }

        const toggle = document.createElement('button');
        toggle.type = 'button';
        toggle.className = 'wa-dock__button';
        toggle.setAttribute('aria-expanded', 'false');
        toggle.setAttribute('aria-controls', 'wa-dock-panel');
        toggle.innerHTML = `${WHATSAPP_ICON}<span>Falar no WhatsApp</span>`;

        const panel = document.createElement('div');
        panel.className = 'wa-dock__panel';
        panel.id = 'wa-dock-panel';
        panel.hidden = true;
        panel.innerHTML = '<p class="wa-dock__title">Escolha o atendimento</p>';
        Object.values(WHATSAPP_CONTACTS).forEach((contact) => {
            const option = buildWhatsAppLink(contact, `<strong>${contact.label}</strong><span>${contact.phone}</span>`);
            option.className = 'wa-dock__option';
            panel.appendChild(option);
        });

        const setOpen = (open) => {
            panel.hidden = !open;
            toggle.setAttribute('aria-expanded', String(open));
        };

        toggle.addEventListener('click', () => setOpen(panel.hidden));
        document.addEventListener('click', (event) => {
            if (!dock.contains(event.target)) setOpen(false);
        });
        document.addEventListener('keydown', (event) => {
            if (event.key === 'Escape') setOpen(false);
        });

        dock.append(panel, toggle);
        document.body.appendChild(dock);
    }

    function initHeaderState() {
        const header = document.querySelector('header');
        if (!header) return;

        const update = () => header.classList.toggle('scrolled', window.scrollY > 16);
        update();
        window.addEventListener('scroll', update, { passive: true });
    }

    document.addEventListener('DOMContentLoaded', () => {
        installWordmark();
        installHomePortraits();
        installLeonardoProfile();
        installWhatsAppDock();
        initEditorialReveals();
        initFaqBehavior();
        initHeaderState();
    });
}());
