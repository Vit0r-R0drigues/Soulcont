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
                <span class="soulcont-team-hero__label">Pessoas por tras dos numeros</span>
                <div class="soulcont-team-hero__photos">
                    <figure class="soulcont-team-hero__person">
                        <img src="/assets/img/soulcont/vitor-rodrigues-hero.webp" alt="Vitor Rodrigues de Lima, contador responsavel da SoulCont">
                        <figcaption class="soulcont-team-hero__caption">Vitor Rodrigues de Lima<span>Contador responsavel · CRC SP353836</span></figcaption>
                    </figure>
                    <figure class="soulcont-team-hero__person">
                        <img src="/assets/img/soulcont/leonardo-silva-hero.webp" alt="Leonardo Silva de Sousa, profissional da SoulCont">
                        <figcaption class="soulcont-team-hero__caption">Leonardo Silva de Sousa<span>Contador · CRCCE 024206/O5</span></figcaption>
                    </figure>
                </div>
                <p class="soulcont-team-hero__copy">Uma equipe presente para conectar rotina contabil, tributos e decisao empresarial com clareza.</p>
            </div>`;
    }

    function installLeonardoProfile() {
        if (document.body.dataset.page !== 'about') return;

        const profile = document.querySelector('.responsible-card .founder-profile');
        if (!profile || document.querySelector('.soulcont-team-member')) return;

        profile.insertAdjacentHTML('afterend', `
            <div class="founder-profile soulcont-team-member">
                <img src="/assets/img/soulcont/leonardo-silva-retrato-3x4.webp" alt="Leonardo Silva de Sousa">
                <div>
                    <strong>Leonardo Silva de Sousa</strong>
                    <span>Contador · CRCCE 024206/O5</span>
                    <p class="copy-muted">Atendimento proximo e orientacao pratica para que cada cliente saiba qual e o proximo passo.</p>
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

    document.addEventListener('DOMContentLoaded', () => {
        installWordmark();
        installHomePortraits();
        installLeonardoProfile();
        installSecondWhatsApp();
    });
}());
