(function () {
    function installWordmark() {
        document.querySelectorAll('header .logo a, .footer-brand-v2 a').forEach((anchor) => {
            if (!anchor.querySelector('img')) return;
            anchor.classList.add('soulcont-wordmark');
            anchor.setAttribute('aria-label', 'SoulCont - pagina inicial');
            anchor.innerHTML = '<span>SOUL</span><strong>CONT</strong>';
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
                        <img src="/assets/img/soulcont/vitor-rodrigues-perfil-3x4.webp" alt="Vitor Rodrigues de Lima, contador responsável da SoulCont" width="720" height="960">
                        <figcaption class="soulcont-team-hero__caption">Vitor Rodrigues de Lima<span>Contador responsável · CRC SP353836</span></figcaption>
                    </figure>
                    <figure class="soulcont-team-hero__person">
                        <img src="/assets/img/soulcont/leonardo-silva-retrato-3x4.webp" alt="Leonardo Silva de Sousa, contador responsável da SoulCont" width="720" height="960">
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
                <img src="/assets/img/soulcont/leonardo-silva-retrato-3x4.webp" alt="Leonardo Silva de Sousa">
                <div>
                    <strong>Leonardo Silva de Sousa</strong>
                    <span>Contador responsável · Registro profissional: CRCCE 024206/O5</span>
                    <p class="copy-muted">Atendimento próximo e orientação prática, em pé de igualdade com Vitor, para que cada cliente saiba qual é o próximo passo.</p>
                </div>
            </div>`);
    }

    function installSecondWhatsApp() {
        document.querySelectorAll('.footer-group-v2 .wa-link-inline').forEach((link) => {
            const list = link.closest('ul');
            if (!list || list.querySelector('a[href*="5588921791670"]')) return;

            const item = document.createElement('li');
            item.innerHTML = '<a class="wa-link-inline" href="https://wa.me/5588921791670?text=Ola%2C%20quero%20falar%20com%20a%20SoulCont." target="_blank" rel="noopener noreferrer">WhatsApp Leonardo: (88) 92179-1670</a>';
            link.closest('li')?.insertAdjacentElement('afterend', item);
        });
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
        installSecondWhatsApp();
        initEditorialReveals();
        initFaqBehavior();
        initHeaderState();
    });
}());
