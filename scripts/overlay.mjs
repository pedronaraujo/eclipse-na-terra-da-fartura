import { MOD, icon, TRAITS, t, getState } from './constants.mjs';

/**
 * Efeito de tela do Eclipse (todos os clientes): borda pulsante, coroa girando, cinzas subindo
 * e um HUD com a contagem. Animações de entrada ("Noite ao Meio-Dia") e saída ("O Sol Retorna").
 */
export class EclipseOverlay {
    static _wasActive = null;

    static statusLine(state = getState()) {
        if (state.active) return t('Menu.StatusActive', { counter: state.counter, max: state.max });
        return state.usedSinceLongRest ? t('Menu.StatusUsed') : t('Menu.StatusReady');
    }

    static sync({ animate = true } = {}) {
        if (!document.body) return;
        const state = getState();
        const wasActive = this._wasActive;
        this._wasActive = state.active;
        const anim = animate && game.settings.get(MOD, 'playAnimations') && wasActive !== null && wasActive !== state.active;

        if (state.active) {
            this.renderOverlay(state);
            this.renderHud(state);
            if (anim) this.playIntro();
            if (anim) this.playSound('soundStart');
        } else {
            if (anim) {
                this.playOutro();
                this.playSound('soundEnd');
            }
            this.removeOverlay(anim);
        }
        this.updateMenuButtons(state);
        document.body.classList.toggle('eclipse-ntf-active', state.active);
        this.refreshFearTracker();
    }

    /**
     * O sistema só recalcula a posição do rastreador de Medo em poucos momentos; quando a contagem do
     * Eclipse entra ou sai do painel de contagens, o rastreador pode ficar deslocado (até fora da tela).
     * Re-renderiza e recalcula sempre que o Eclipse ou as contagens mudam.
     */
    static refreshFearTracker = foundry.utils.debounce(async () => {
        const tracker = ui.resources;
        if (!tracker) return;
        try {
            if (tracker.rendered) await tracker.render();
            tracker.handleOffset?.();
            const hud = document.getElementById('eclipse-ntf-hud');
            if (hud) EclipseOverlay.placeHud(hud);
        } catch (err) {
            console.warn(`${MOD} |`, err);
        }
    }, 250);

    /** Mantém o HUD sempre abaixo do rastreador de Medo quando ele está no topo da tela. */
    static placeHud(hud) {
        hud.style.top = '';
        if (hud.dataset.position !== 'top') return;
        const fear = ui.resources?.element;
        if (!fear?.isConnected || fear.hidden) return;
        const rect = fear.getBoundingClientRect();
        if (rect.height && rect.top < 200) hud.style.top = `${Math.round(rect.bottom + 10)}px`;
    }

    /* -------------------------------------------- */

    static renderOverlay(state) {
        const intensity = game.settings.get(MOD, 'overlayIntensity');
        let el = document.getElementById('eclipse-ntf-overlay');
        if (intensity === 'off') return el?.remove();
        if (!el) {
            el = document.createElement('div');
            el.id = 'eclipse-ntf-overlay';
            el.setAttribute('aria-hidden', 'true');
            const embers = Array.from({ length: 28 }, (_, i) => {
                const side = i % 4;
                const pos = (i * 37) % 100;
                const delay = ((i * 1.7) % 9).toFixed(2);
                const dur = (7 + ((i * 3.1) % 6)).toFixed(2);
                return `<span class="eclipse-ember side-${side}" style="--p:${pos}%;--d:${delay}s;--t:${dur}s"></span>`;
            }).join('');
            el.innerHTML = `
                <div class="eclipse-vignette"></div>
                <div class="eclipse-border"></div>
                <div class="eclipse-corner tl"></div><div class="eclipse-corner tr"></div>
                <div class="eclipse-corner bl"></div><div class="eclipse-corner br"></div>
                <div class="eclipse-embers">${embers}</div>`;
            document.body.appendChild(el);
            requestAnimationFrame(() => el.classList.add('visible'));
        }
        el.dataset.intensity = intensity;
        el.classList.remove('leaving');
        // Quanto menor a contagem, mais rápido o pulso
        const ratio = state.max ? state.counter / state.max : 1;
        el.style.setProperty('--eclipse-pulse', `${(1.6 + 2.4 * ratio).toFixed(2)}s`);
    }

    static renderHud(state) {
        const pos = game.settings.get(MOD, 'hudPosition');
        let hud = document.getElementById('eclipse-ntf-hud');
        if (pos === 'hidden') return hud?.remove();
        if (!hud) {
            hud = document.createElement('div');
            hud.id = 'eclipse-ntf-hud';
            hud.addEventListener('click', () => game.modules.get(MOD).api?.open());
            document.body.appendChild(hud);
            requestAnimationFrame(() => hud.classList.add('visible'));
        }
        hud.dataset.position = pos;
        hud.classList.remove('leaving');
        const pips = Array.from({ length: state.max }, (_, i) =>
            `<span class="pip ${i < state.counter ? 'lit' : 'spent'}"></span>`).join('');
        const traits = state.traits.map(i => {
            const tr = TRAITS[i];
            return `<span class="trait" data-tooltip="<strong>${t(`Traits.${tr.id}.name`)}</strong><br>${t(`Traits.${tr.id}.text`)}"><i class="${tr.icon}"></i></span>`;
        }).join('');
        const notes = state.notes ? `<span class="trait note" data-tooltip="${foundry.utils.escapeHTML(state.notes)}"><i class="fa-solid fa-feather"></i></span>` : '';
        hud.innerHTML = `
            <div class="hud-sun"><img src="${icon()}" alt=""></div>
            <div class="hud-body">
                <div class="hud-title">${t('Hud.Title')}</div>
                <div class="hud-count"><span class="num">${state.counter}</span><span class="of">/ ${state.max}</span></div>
                <div class="hud-pips">${pips}</div>
                <div class="hud-traits">${traits}${notes}</div>
            </div>`;
        hud.dataset.tooltip = t('Hud.Tooltip');
        this.placeHud(hud);
    }

    static removeOverlay(animated) {
        for (const id of ['eclipse-ntf-overlay', 'eclipse-ntf-hud']) {
            const el = document.getElementById(id);
            if (!el) continue;
            if (!animated) {
                el.remove();
                continue;
            }
            el.classList.add('leaving');
            setTimeout(() => el.remove(), 2600);
        }
    }

    static updateMenuButtons(state) {
        for (const btn of document.querySelectorAll('.eclipse-ntf-menu-btn')) {
            btn.classList.toggle('is-active', state.active);
            const s = btn.querySelector('.eclipse-ntf-menu-status');
            if (s) s.textContent = this.statusLine(state);
        }
    }

    /* -------------------------------------------- */
    /*  Animações                                   */
    /* -------------------------------------------- */

    static playIntro() {
        this._cinematic('intro', t('Intro.Title'), t('Intro.Subtitle'), 5200);
    }

    static playOutro() {
        this._cinematic('outro', t('Outro.Title'), t('Outro.Subtitle'), 4600);
    }

    static _cinematic(kind, title, subtitle, duration) {
        document.querySelectorAll('.eclipse-ntf-cinematic').forEach(e => e.remove());
        const el = document.createElement('div');
        el.className = `eclipse-ntf-cinematic ${kind}`;
        el.setAttribute('aria-hidden', 'true');
        el.innerHTML = `
            <div class="cine-sky"></div>
            <div class="cine-stage">
                <div class="cine-sun"></div>
                <div class="cine-corona"></div>
                <div class="cine-moon"></div>
            </div>
            <div class="cine-text"><h1>${title}</h1><p>${subtitle}</p></div>`;
        document.body.appendChild(el);
        setTimeout(() => el.remove(), duration);
    }

    static playSound(key) {
        const src = game.settings.get(MOD, key);
        if (!src) return;
        try {
            foundry.audio.AudioHelper.play({ src, volume: 0.8, autoplay: true, loop: false }, false);
        } catch (err) {
            console.warn(`${MOD} |`, err);
        }
    }
}
