import { MOD, icon, banner, TRAITS, traitForRoll, t, getState, currentFear, guessPlayers } from './constants.mjs';
import { EclipseEngine } from './engine.mjs';

const { ApplicationV2, HandlebarsApplicationMixin } = foundry.applications.api;

/**
 * Janela do Eclipse. Para o mestre: monta (jogadores, Medo, d10), improvisa e inicia/encerra.
 * Para os jogadores: mostra o Eclipse em andamento.
 */
export class EclipseApp extends HandlebarsApplicationMixin(ApplicationV2) {
    static DEFAULT_OPTIONS = {
        id: 'eclipse-ntf-app',
        classes: ['eclipse-ntf', 'eclipse-ntf-app'],
        tag: 'div',
        window: { title: 'ECLIPSE.App.Title', icon: 'fa-solid fa-circle-half-stroke', resizable: true },
        position: { width: 720, height: 'auto' },
        actions: {
            playersDown: EclipseApp.#playersDown,
            playersUp: EclipseApp.#playersUp,
            fearDown: EclipseApp.#fearDown,
            fearUp: EclipseApp.#fearUp,
            rollEclipse: EclipseApp.#roll,
            toggleTrait: EclipseApp.#toggleTrait,
            clearRoll: EclipseApp.#clearRoll,
            startEclipse: EclipseApp.#start,
            endEclipse: EclipseApp.#end,
            tickDown: EclipseApp.#tickDown,
            tickUp: EclipseApp.#tickUp,
            resetRest: EclipseApp.#resetRest,
            openGuide: EclipseApp.#openGuide
        }
    };

    static PARTS = {
        main: { template: `modules/${MOD}/templates/eclipse-app.hbs`, scrollable: ['.eclipse-scroll'] }
    };

    constructor(options) {
        super(options);
        this.draft = { players: guessPlayers(), fear: 1, rolls: [], traits: [], duplicates: 0, notes: '', rolled: false, darken: null, spendFear: true };
    }

    static open() {
        const existing = foundry.applications.instances.get('eclipse-ntf-app');
        if (existing) {
            existing.render({ force: true });
            existing.bringToFront?.();
            return existing;
        }
        return new EclipseApp().render({ force: true });
    }

    static refresh() {
        foundry.applications.instances.get('eclipse-ntf-app')?.render();
    }

    /* -------------------------------------------- */

    async _prepareContext(options) {
        const context = await super._prepareContext(options);
        const state = getState();
        const d = this.draft;
        const fearNow = currentFear();
        if (d.fear > fearNow && !state.active && d.spendFear) d.fear = Math.max(1, fearNow);
        if (d.darken === null) d.darken = game.settings.get(MOD, 'darkenScene');

        const activeTraits = state.active ? state.traits : d.traits;
        const rollsByTrait = TRAITS.map(() => []);
        for (const r of (state.active ? state.rolls : d.rolls)) {
            const i = traitForRoll(r);
            if (i >= 0) rollsByTrait[i].push(r);
        }
        const traits = TRAITS.map((tr, i) => ({
            index: i,
            id: tr.id,
            icon: tr.icon,
            img: tr.img,
            range: `${tr.range[0]}–${tr.range[1]}`,
            name: t(`Traits.${tr.id}.name`),
            text: t(`Traits.${tr.id}.text`),
            auto: t(`Traits.${tr.id}.auto`),
            selected: activeTraits.includes(i),
            dice: rollsByTrait[i],
            duplicate: rollsByTrait[i].length > 1
        }));

        const max = d.players * 2 + d.duplicates * 2;
        const pips = (n, lit) => Array.from({ length: n }, (_, i) => ({ lit: i < lit }));
        return {
            ...context,
            isGM: game.user.isGM,
            icon: icon(),
            banner: banner(),
            state,
            draft: d,
            traits,
            fearNow,
            fearPips: pips(Math.max(fearNow, d.fear), d.spendFear ? d.fear : 0),
            previewMax: max,
            previewPips: pips(max, max),
            activePips: pips(state.max, state.counter),
            setup: game.user.isGM && !state.active,
            interactive: game.user.isGM && !state.active,
            canStart: game.user.isGM && !state.active && d.rolled && (!d.spendFear || d.fear <= fearNow),
            fearShort: d.spendFear && d.fear > fearNow,
            rollLabel: t('App.Roll', { n: d.fear }),
            startedAgo: state.startedAt ? this.#ago(state.startedAt) : ''
        };
    }

    #ago(ts) {
        const mins = Math.max(0, Math.round((Date.now() - ts) / 60000));
        return mins < 1 ? t('App.JustNow') : t('App.MinutesAgo', { mins });
    }

    _onRender(context, options) {
        super._onRender?.(context, options);
        const el = this.element;
        el.querySelector('textarea[name="notes"]')?.addEventListener('input', ev => {
            this.draft.notes = ev.currentTarget.value;
        });
        el.querySelector('input[name="darken"]')?.addEventListener('change', ev => {
            this.draft.darken = ev.currentTarget.checked;
        });
        el.querySelector('input[name="spendFear"]')?.addEventListener('change', ev => {
            this.draft.spendFear = ev.currentTarget.checked;
            this.render();
        });
        el.querySelector('input[name="players"]')?.addEventListener('change', ev => {
            this.draft.players = Math.max(1, Number(ev.currentTarget.value) || 1);
            this.render();
        });
    }

    /* -------------------------------------------- */
    /*  Ações                                       */
    /* -------------------------------------------- */

    static #playersDown() {
        this.draft.players = Math.max(1, this.draft.players - 1);
        this.render();
    }

    static #playersUp() {
        this.draft.players = Math.min(12, this.draft.players + 1);
        this.render();
    }

    static #fearDown() {
        this.draft.fear = Math.max(1, this.draft.fear - 1);
        this.render();
    }

    static #fearUp() {
        const cap = this.draft.spendFear ? Math.max(1, currentFear()) : 12;
        this.draft.fear = Math.min(cap, this.draft.fear + 1);
        this.render();
    }

    static async #roll() {
        if (!game.user.isGM) return;
        const n = Math.max(1, this.draft.fear);
        const roll = await new Roll(`${n}d10`).evaluate();
        if (game.dice3d) await game.dice3d.showForRoll(roll, game.user, true).catch(() => null);
        const rolls = roll.dice[0].results.map(r => r.result);
        const traits = [];
        let duplicates = 0;
        for (const r of rolls) {
            const i = traitForRoll(r);
            if (traits.includes(i)) duplicates++;
            else traits.push(i);
        }
        Object.assign(this.draft, { rolls, traits, duplicates, rolled: true });
        this.render();
        this.element?.classList.add('just-rolled');
        setTimeout(() => this.element?.classList.remove('just-rolled'), 1400);
    }

    static #clearRoll() {
        Object.assign(this.draft, { rolls: [], traits: [], duplicates: 0, rolled: false });
        this.render();
    }

    /** Improvisar: o mestre pode ligar/desligar características depois da rolagem. */
    static #toggleTrait(_ev, target) {
        if (!game.user.isGM || getState().active) return;
        const i = Number(target.dataset.index);
        const set = new Set(this.draft.traits);
        set.has(i) ? set.delete(i) : set.add(i);
        this.draft.traits = [...set].sort();
        this.draft.rolled = true;
        this.render();
    }

    static async #start() {
        const d = this.draft;
        const state = getState();
        if (state.usedSinceLongRest) {
            const ok = await foundry.applications.api.DialogV2.confirm({
                window: { title: t('App.Title') },
                content: `<p>${t('App.UsedWarning')}</p>`
            });
            if (!ok) return;
        }
        await EclipseEngine.start({
            players: d.players, fear: d.fear, traits: d.traits, rolls: d.rolls, duplicates: d.duplicates,
            notes: d.notes, darken: d.darken, spendFear: d.spendFear
        });
        Object.assign(this.draft, { rolls: [], traits: [], duplicates: 0, rolled: false, notes: '' });
        this.render();
    }

    static async #end() {
        const ok = await foundry.applications.api.DialogV2.confirm({
            window: { title: t('App.Title') },
            content: `<p>${t('App.EndConfirm')}</p>`
        });
        if (ok) await EclipseEngine.end('sunset');
    }

    static #tickDown() {
        EclipseEngine.tick(-1, { manual: true });
    }

    static #tickUp() {
        EclipseEngine.tick(1, { manual: true });
    }

    static async #resetRest() {
        await EclipseEngine.resetLongRest();
    }

    static async #openGuide() {
        const pack = game.packs.get(`${MOD}.diario-mestre`);
        const doc = (await pack?.getDocuments())?.[0];
        const page = doc?.pages.find(p => p.name === 'Mecânicas: o Eclipse');
        doc?.sheet.render(true, page ? { pageId: page.id } : {});
    }
}
