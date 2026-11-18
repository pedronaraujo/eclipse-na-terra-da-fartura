/**
 * Eclipse na Terra da Fartura — módulo para o sistema Daggerheart (Foundryborne).
 * DOZE Vol. 1 · ANAMA Criativa
 *
 * Mecânica de Eclipse: o mestre gasta Medo, rola d10 por ponto gasto e adiciona características
 * ao Eclipse; uma contagem regressiva (2 × jogadores) diminui a cada uso de Esperança. Enquanto
 * o Eclipse durar, todos os clientes veem a borda pulsante e o HUD do Eclipse.
 */
import { MOD, BASE, icon, TRAITS, t, getState, isActiveGM } from './constants.mjs';
import { registerSettings } from './settings.mjs';
import { EclipseEngine } from './engine.mjs';
import { EclipseOverlay } from './overlay.mjs';
import { EclipseApp } from './eclipse-app.mjs';

const TEMPLATES = ['eclipse-app', 'chat-start', 'chat-end'];
const registered = [];
function on(hook, fn) {
    registered.push([hook, Hooks.on(hook, fn)]);
}

export function initialize() {
    registerSettings();
    foundry.applications.handlebars.loadTemplates(TEMPLATES.map(n => `modules/${MOD}/templates/${n}.hbs`));

    // Ícone de status do Eclipse nos tokens afetados (não aparece no HUD de status)
    if (!CONFIG.statusEffects.some(s => s.id === 'eclipse-ntf')) {
        CONFIG.statusEffects.push({ id: 'eclipse-ntf', name: 'ECLIPSE.Status', img: icon(), hud: false });
    }

    const mod = game.modules.get(MOD);
    const api = {
        open: () => EclipseApp.open(),
        start: options => EclipseEngine.start(options),
        end: reason => EclipseEngine.end(reason),
        tick: (delta = -1) => EclipseEngine.tick(delta, { manual: true }),
        get state() {
            return getState();
        },
        traits: TRAITS,
        devBoot,
        _hooks: registered
    };
    if (mod) mod.api = api;
    globalThis.EclipseNTF = api;
    registerHooks();
}

export async function ready() {
    EclipseOverlay.sync({ animate: false });
    EclipseEngine.primeHopeCache();
    if (isActiveGM()) await EclipseEngine.verifyConsistency();
    ui.sidebar?.tabs?.daggerheartMenu?.render?.();
}

/**
 * Carrega uma versão de desenvolvimento por cima da instalada (ou sem instalação), a partir de uma URL
 * (ex.: https://cdn.jsdelivr.net/gh/pedronaraujo/eclipse-na-terra-da-fartura@<sha>). Recarregar a página desfaz.
 */
export async function devBoot(base) {
    const old = globalThis.EclipseNTF?._hooks ?? game.modules.get(MOD)?.api?._hooks;
    if (old) for (const [hook, id] of old) Hooks.off(hook, id);
    BASE.url = base;
    const lang = await fetch(`${base}/lang/${game.i18n.lang === 'pt-BR' ? 'pt-BR' : 'en'}.json`).then(r => r.json());
    foundry.utils.mergeObject(game.i18n.translations, lang);
    for (const n of TEMPLATES) {
        const text = await fetch(`${base}/templates/${n}.hbs`).then(r => r.text());
        Handlebars.registerPartial(`modules/${MOD}/templates/${n}.hbs`, Handlebars.compile(text));
    }
    document.getElementById('eclipse-ntf-dev-css')?.remove();
    const css = await fetch(`${base}/styles/eclipse.css`).then(r => r.text());
    const style = document.createElement('style');
    style.id = 'eclipse-ntf-dev-css';
    style.textContent = css.replaceAll("url('../", `url('${base}/`);
    document.head.appendChild(style);
    initialize();
    await ready();
    return 'eclipse dev build loaded';
}

Hooks.once('init', initialize);
Hooks.once('ready', ready);

function registerHooks() {
    /* Botão no menu Daggerheart (aba da direita) */
    on('renderDaggerheartMenu', (app, element) => {
        const root = element instanceof HTMLElement ? element : element?.[0];
        if (!root || root.querySelector('.eclipse-ntf-menu')) return;
        const state = getState();
        const fs = document.createElement('fieldset');
        fs.className = 'eclipse-ntf-menu';
        fs.innerHTML = `
            <legend>${t('Menu.Legend')}</legend>
            <button type="button" class="eclipse-ntf-menu-btn ${state.active ? 'is-active' : ''}" data-tooltip="${t('Menu.Tooltip')}">
                <span class="eclipse-ntf-menu-sun"><img src="${icon()}" alt=""></span>
                <span class="eclipse-ntf-menu-label">
                    <strong>${t('Menu.Button')}</strong>
                    <small class="eclipse-ntf-menu-status">${EclipseOverlay.statusLine(state)}</small>
                </span>
            </button>`;
        fs.querySelector('button').addEventListener('click', ev => {
            ev.preventDefault();
            EclipseApp.open();
        });
        const anchor = root.querySelector('h2');
        if (anchor) anchor.after(fs);
        else (root.querySelector('div') ?? root).prepend(fs);
    });

    /* Contagem: uso de Esperança */
    on('updateActor', (actor, changes) => EclipseEngine.onActorUpdate(actor, changes));

    /* Atores e tokens criados durante o Eclipse também recebem os efeitos */
    on('createActor', actor => EclipseEngine.onDocumentCreated(actor));
    on('createToken', tokenDoc => EclipseEngine.onDocumentCreated(tokenDoc.actor, tokenDoc));

    /* Sincroniza com edições manuais na contagem do sistema */
    on('updateSetting', setting => {
        if (setting.key === 'daggerheart.Countdowns') EclipseEngine.onCountdownsChanged();
    });

    on('canvasReady', () => EclipseOverlay.sync({ animate: false }));
}
