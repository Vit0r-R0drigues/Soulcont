// Configuracao de cookies
const COOKIE_CONFIG = {
    expiryDays: 365,
    names: {
        consent: 'soulcont_cookie_consent',
        analytics: 'soulcont_analytics_cookies',
        marketing: 'soulcont_marketing_cookies'
    }
};

const ANALYTICS_CONFIG = {
    measurementId: 'G-V68TNXMWT5',
    scriptId: 'soulcont-analytics-script'
};

function getCookie(name) {
    const prefix = `${name}=`;
    const parts = document.cookie.split(';');
    for (const rawPart of parts) {
        const part = rawPart.trim();
        if (part.startsWith(prefix)) {
            return decodeURIComponent(part.substring(prefix.length));
        }
    }
    return null;
}

function setCookie(name, value, days = COOKIE_CONFIG.expiryDays) {
    const expires = new Date(Date.now() + days * 24 * 60 * 60 * 1000).toUTCString();
    const secure = window.location.protocol === 'https:' ? '; Secure' : '';
    document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires}; path=/; SameSite=Lax${secure}`;
}

function hideCookieBanner() {
    const banner = document.querySelector('.cookie-banner');
    if (!banner) return;
    banner.classList.remove('show');
    document.body.classList.remove('has-cookie-banner');
    setTimeout(() => banner.remove(), 300);
}

function closeCookieSettings() {
    const overlay = document.querySelector('.cookie-overlay');
    const settings = document.querySelector('.cookie-settings');

    if (overlay) overlay.classList.remove('show');
    if (settings) settings.classList.remove('show');

    setTimeout(() => {
        if (overlay) overlay.remove();
        if (settings) settings.remove();
    }, 300);
}

function showCookieBanner() {
    if (getCookie(COOKIE_CONFIG.names.consent) === 'true') return;
    if (document.querySelector('.cookie-banner')) return;

    const banner = document.createElement('div');
    banner.className = 'cookie-banner';
    banner.innerHTML = `
        <div class="cookie-content">
            <p>
                Utilizamos cookies para melhorar sua experiencia.
                Leia nossa <a href="/HTML/politica-de-privacidade.html" target="_blank" rel="noopener noreferrer">Politica de Privacidade</a>.
            </p>
            <div class="cookie-buttons">
                <button type="button" class="cookie-btn settings-btn" onclick="showCookieSettings()">Configurar Preferencias</button>
                <button type="button" class="cookie-btn settings-btn" onclick="rejectOptionalCookies()">Recusar Opcionais</button>
                <button type="button" class="cookie-btn accept-btn" onclick="acceptAllCookies()">Aceitar Todos</button>
            </div>
        </div>
    `;

    document.body.appendChild(banner);
    document.body.classList.add('has-cookie-banner');
    requestAnimationFrame(() => banner.classList.add('show'));
}

function showCookieSettings() {
    if (document.querySelector('.cookie-overlay') || document.querySelector('.cookie-settings')) return;

    const analyticsChecked = getCookie(COOKIE_CONFIG.names.analytics) === 'true';
    const marketingChecked = getCookie(COOKIE_CONFIG.names.marketing) === 'true';

    const overlay = document.createElement('div');
    overlay.className = 'cookie-overlay';

    const settings = document.createElement('div');
    settings.className = 'cookie-settings';
    settings.innerHTML = `
        <h3>Preferencias de Cookies</h3>
        <p class="cookie-description">Escolha quais cookies deseja permitir.</p>
        <div class="cookie-option">
            <div class="cookie-option-text">
                <label>Cookies Essenciais</label>
                <p>Necessarios para o funcionamento do site. Nao podem ser desativados.</p>
            </div>
            <label class="switch">
                <input type="checkbox" checked disabled>
                <span class="slider"></span>
            </label>
        </div>
        <div class="cookie-option">
            <div class="cookie-option-text">
                <label>Cookies Analiticos</label>
                <p>Ajudam a medir desempenho e melhorar a experiencia.</p>
            </div>
            <label class="switch">
                <input type="checkbox" id="analyticsCookies" ${analyticsChecked ? 'checked' : ''}>
                <span class="slider"></span>
            </label>
        </div>
        <div class="cookie-option">
            <div class="cookie-option-text">
                <label>Cookies de Marketing</label>
                <p>Usados para personalizacao de campanhas.</p>
            </div>
            <label class="switch">
                <input type="checkbox" id="marketingCookies" ${marketingChecked ? 'checked' : ''}>
                <span class="slider"></span>
            </label>
        </div>
        <div class="cookie-buttons">
            <button type="button" class="cookie-btn settings-btn" onclick="closeCookieSettings()">Cancelar</button>
            <button type="button" class="cookie-btn accept-btn" onclick="saveSettings()">Salvar Preferencias</button>
        </div>
    `;

    overlay.addEventListener('click', (event) => {
        if (event.target === overlay) {
            closeCookieSettings();
        }
    });

    document.body.appendChild(overlay);
    document.body.appendChild(settings);

    requestAnimationFrame(() => {
        overlay.classList.add('show');
        settings.classList.add('show');
    });
}

function acceptAllCookies() {
    setCookie(COOKIE_CONFIG.names.consent, 'true');
    setCookie(COOKIE_CONFIG.names.analytics, 'true');
    setCookie(COOKIE_CONFIG.names.marketing, 'true');
    closeCookieSettings();
    hideCookieBanner();
    initializeServices();
}

function rejectOptionalCookies() {
    setCookie(COOKIE_CONFIG.names.consent, 'true');
    setCookie(COOKIE_CONFIG.names.analytics, 'false');
    setCookie(COOKIE_CONFIG.names.marketing, 'false');
    closeCookieSettings();
    hideCookieBanner();
    updateGoogleConsent(false, false);
}

function saveSettings() {
    const analyticsEnabled = document.getElementById('analyticsCookies')?.checked ?? false;
    const marketingEnabled = document.getElementById('marketingCookies')?.checked ?? false;

    setCookie(COOKIE_CONFIG.names.consent, 'true');
    setCookie(COOKIE_CONFIG.names.analytics, String(analyticsEnabled));
    setCookie(COOKIE_CONFIG.names.marketing, String(marketingEnabled));

    closeCookieSettings();
    hideCookieBanner();
    updateGoogleConsent(analyticsEnabled, marketingEnabled);
    initializeServices();
}

function updateGoogleConsent(analyticsEnabled, marketingEnabled) {
    if (typeof window.gtag !== 'function') return;

    window.gtag('consent', 'update', {
        analytics_storage: analyticsEnabled ? 'granted' : 'denied',
        ad_storage: marketingEnabled ? 'granted' : 'denied',
        ad_user_data: marketingEnabled ? 'granted' : 'denied',
        ad_personalization: marketingEnabled ? 'granted' : 'denied'
    });
}

function trackAnalyticsEvent(eventName, parameters = {}) {
    if (getCookie(COOKIE_CONFIG.names.analytics) !== 'true') return;
    if (typeof window.gtag !== 'function') return;

    window.gtag('event', eventName, {
        page_path: window.location.pathname,
        ...parameters
    });
}

function getContactMethod(link) {
    const href = link.getAttribute('href') || '';
    if (/^tel:/i.test(href)) return 'telefone';
    if (/^mailto:/i.test(href)) return 'email';
    if (/wa\.me|api\.whatsapp\.com|whatsapp\.com/i.test(href)) return 'whatsapp';
    return null;
}

function getPageTrackingContext(element = null) {
    const cityMatch = window.location.pathname.match(/\/cidades\/([^/]+)\//i);
    const serviceMatch = window.location.pathname.match(/\/servicos\/([^/]+)\//i);
    const legacyServiceMatch = window.location.pathname.match(
        /\/HTML\/(abertura-de-empresa|troca-de-contador|diagnostico-tributario|contabilidade-prestadores-servico)\.html/i
    );
    const trackedElement = element instanceof HTMLElement ? element : null;
    const submittedCity = element instanceof HTMLFormElement
        ? element.elements.namedItem('cidade')?.value?.trim()
        : '';

    return {
        city: trackedElement?.dataset.trackCity
            || document.body.dataset.trackCity
            || submittedCity
            || cityMatch?.[1]
            || 'nao_informada',
        service: trackedElement?.dataset.trackService
            || document.body.dataset.trackService
            || serviceMatch?.[1]
            || legacyServiceMatch?.[1]
            || 'geral',
        page_type: document.body.dataset.pageType
            || (cityMatch ? 'cidade' : serviceMatch || legacyServiceMatch ? 'servico' : 'institucional')
    };
}

function initializeContactTracking() {
    if (window.soulcontContactTrackingInitialized) return;

    document.addEventListener('click', (event) => {
        if (!(event.target instanceof Element)) return;
        const link = event.target.closest('a[href]');
        if (!link) return;

        const contactMethod = getContactMethod(link);
        if (!contactMethod) return;

        const eventParameters = {
            contact_method: contactMethod,
            cta_position: link.dataset.trackPosition || 'nao_informada',
            cta_label: (link.textContent || link.getAttribute('aria-label') || 'contato').trim().slice(0, 100),
            ...getPageTrackingContext(link)
        };

        const methodEventName = {
            telefone: 'phone_click',
            email: 'email_click',
            whatsapp: 'whatsapp_click'
        }[contactMethod];

        trackAnalyticsEvent('contact_click', eventParameters);
        if (methodEventName) trackAnalyticsEvent(methodEventName, eventParameters);
        trackAnalyticsEvent('generate_lead', eventParameters);
    }, true);

    document.addEventListener('submit', (event) => {
        const form = event.target;
        if (!(form instanceof HTMLFormElement)) return;

        const eventParameters = {
            form_id: form.id || 'formulario_sem_id',
            contact_method: 'formulario',
            ...getPageTrackingContext(form)
        };

        trackAnalyticsEvent('form_submit', eventParameters);
        trackAnalyticsEvent('generate_lead', eventParameters);
    }, true);

    window.soulcontContactTrackingInitialized = true;
}

function initializeAnalytics() {
    if (window.soulcontAnalyticsInitialized) {
        return Promise.resolve();
    }

    const existingScript = document.getElementById(ANALYTICS_CONFIG.scriptId);
    if (existingScript) {
        return existingScript.dataset.loaded === 'true'
            ? Promise.resolve()
            : new Promise((resolve, reject) => {
                existingScript.addEventListener('load', resolve, { once: true });
                existingScript.addEventListener('error', reject, { once: true });
            });
    }

    return new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.id = ANALYTICS_CONFIG.scriptId;
        script.async = true;
        script.src = `https://www.googletagmanager.com/gtag/js?id=${ANALYTICS_CONFIG.measurementId}`;

        script.addEventListener('load', () => {
            script.dataset.loaded = 'true';
            window.dataLayer = window.dataLayer || [];
            window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
            window.gtag('js', new Date());
            window.gtag('config', ANALYTICS_CONFIG.measurementId, {
                anonymize_ip: true
            });
            updateGoogleConsent(true, getCookie(COOKIE_CONFIG.names.marketing) === 'true');
            initializeContactTracking();
            window.soulcontAnalyticsInitialized = true;
            resolve();
        }, { once: true });

        script.addEventListener('error', reject, { once: true });
        document.head.appendChild(script);
    }).catch((error) => {
        console.warn('Nao foi possivel carregar o Google Analytics apos o consentimento.', error);
    });
}

function initializeMarketing() {
    // Placeholder para inicializacao de marketing/pixels.
}

function initializeServices() {
    const analyticsEnabled = getCookie(COOKIE_CONFIG.names.analytics) === 'true';
    const marketingEnabled = getCookie(COOKIE_CONFIG.names.marketing) === 'true';

    if (analyticsEnabled) initializeAnalytics();
    if (marketingEnabled) initializeMarketing();
}

document.addEventListener('DOMContentLoaded', () => {
    initializeContactTracking();
    showCookieBanner();
    if (getCookie(COOKIE_CONFIG.names.consent) === 'true') {
        initializeServices();
    }
});
