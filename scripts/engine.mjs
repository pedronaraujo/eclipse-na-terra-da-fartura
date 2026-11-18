import { MOD, icon, banner, FLAG, EFFECT_STATUS, TRAITS, DEFAULT_STATE, t, getState, isActiveGM, currentFear } from './constants.mjs';

/** Id fixo do efeito: um por ator. Mantém base e token sem duplicar (o delta do token sobrescreve pelo id). */
export const EFFECT_ID = 'eclipsentfEffect';
const COUNTDOWN_SETTING = ['daggerheart', 'Countdowns'];
const AFFECTED_TYPES = ['adversary', 'environment', 'character'];

export class EclipseEngine {
    static _queue = Promise.resolve();
    static _hope = new Map();
    static _writingCountdown = false;
    static _ending = false;

    /* -------------------------------------------- */
    /*  Estado                                      */
    /* -------------------------------------------- */

    static async setState(patch) {
        if (!game.user.isGM) return;
        const next = foundry.utils.mergeObject(getState(), patch, { inplace: false, performDeletions: true });
        if (patch.traits) next.traits = patch.traits;
        if (patch.rolls) next.rolls = patch.rolls;
        if (patch.tokenEffects) next.tokenEffects = patch.tokenEffects;
        if (patch.history) next.history = patch.history;
        await game.settings.set(MOD, 'state', next);
        return next;
    }

    static serialize(fn) {
        this._queue = this._queue.then(fn).catch(err => {
            console.error(`${MOD} |`, err);
            ui.notifications.error(t('Errors.Generic'));
        });
        return this._queue;
    }

    /* -------------------------------------------- */
    /*  Início                                      */
    /* -------------------------------------------- */

    /**
     * @param {object} opts
     * @param {number} opts.players     Jogadores na cena
     * @param {number} opts.fear        Pontos de Medo gastos
     * @param {number[]} opts.traits    Índices das características (TRAITS)
     * @param {number[]} opts.rolls     Resultados dos d10
     * @param {number} opts.duplicates  Quantos dados repetiram característica (+2 cada)
     * @param {string} opts.notes       Características improvisadas / notas
     * @param {boolean} opts.darken     Escurecer a cena
     * @param {boolean} opts.spendFear  Descontar o Medo do rastreador
     */
    static start(opts = {}) {
        return this.serialize(() => this._start(opts));
    }

    static async _start({ players = 1, fear = 0, traits = [], rolls = [], duplicates = 0, notes = '', darken = true, spendFear = true } = {}) {
        if (!game.user.isGM) return ui.notifications.warn(t('Errors.GMOnly'));
        const state = getState();
        if (state.active) return ui.notifications.warn(t('Errors.AlreadyActive'));

        if (spendFear && fear > 0) {
            const cur = currentFear();
            if (fear > cur) return ui.notifications.error(t('Errors.NotEnoughFear', { fear, cur }));
            if (ui.resources?.updateFear) await ui.resources.updateFear(cur - fear);
            else await game.settings.set('daggerheart', 'ResourcesFear', cur - fear);
        }

        const max = Math.max(1, players * 2 + duplicates * 2);
        const uniqueTraits = [...new Set(traits)].sort();
        const countdownId = game.settings.get(MOD, 'useSystemCountdown') ? await this.createCountdown(max) : null;

        let prevDarkness = null;
        let sceneId = null;
        const scene = canvas?.scene;
        if (darken && scene) {
            prevDarkness = scene.environment?.darknessLevel ?? 0;
            sceneId = scene.id;
            const level = game.settings.get(MOD, 'darknessLevel');
            if (level > prevDarkness) await scene.update({ 'environment.darknessLevel': level }, { animateDarkness: 6000 });
        }

        const tokenEffects = await this.applyEffects(uniqueTraits);

        const next = await this.setState({
            active: true, traits: uniqueTraits, rolls, duplicates, notes, counter: max, max, players, fear,
            countdownId, startedAt: Date.now(), sceneId, prevDarkness, tokenEffects, usedSinceLongRest: true
        });

        await this.chatCard('start', next);
        Hooks.callAll(`${MOD}.start`, next);
        return next;
    }

    /* -------------------------------------------- */
    /*  Contagem                                    */
    /* -------------------------------------------- */

    static tick(delta = -1, { manual = false, reason = '' } = {}) {
        if (!game.user.isGM) return;
        return this.serialize(() => this._tick(delta, { manual, reason }));
    }

    static async _tick(delta, { reason }) {
        const state = getState();
        if (!state.active) return;
        const counter = Math.max(0, state.counter + delta);
        const max = Math.max(state.max, counter);
        await this.updateCountdown(state.countdownId, counter, max);
        await this.setState({ counter, max });
        if (delta < 0 && reason) ui.notifications.info(t('Notify.HopeSpent', { name: reason, counter }));
        if (counter <= 0) await this._end('countdown');
    }

    static primeHopeCache() {
        for (const a of game.actors ?? []) {
            if (a.type === 'character') this._hope.set(a.uuid, a.system?.resources?.hope?.value ?? 0);
        }
    }

    static onActorUpdate(actor, changes) {
        if (actor.type !== 'character') return;
        const value = foundry.utils.getProperty(changes, 'system.resources.hope.value');
        if (value === undefined) return;
        const previous = this._hope.get(actor.uuid);
        this._hope.set(actor.uuid, value);
        if (!isActiveGM() || !game.settings.get(MOD, 'autoTick')) return;
        const state = getState();
        if (!state.active || previous === undefined) return;
        if (value < previous) this.tick(-1, { reason: actor.name });
    }

    static async createCountdown(max) {
        try {
            const setting = game.settings.get(...COUNTDOWN_SETTING);
            const data = setting.toObject();
            const id = foundry.utils.randomID();
            data.countdowns[id] = {
                type: 'encounter',
                name: t('Countdown.Name'),
                img: icon(),
                hidden: false,
                ownership: {},
                progress: { current: max, start: max, startFormula: String(max), looping: 'noLooping', type: 'custom' }
            };
            this._writingCountdown = true;
            await game.settings.set(...COUNTDOWN_SETTING, data);
            return id;
        } catch (err) {
            console.warn(`${MOD} | Não foi possível criar a contagem do sistema`, err);
            return null;
        } finally {
            this._writingCountdown = false;
        }
    }

    static async updateCountdown(id, current, start) {
        if (!id) return;
        try {
            const setting = game.settings.get(...COUNTDOWN_SETTING);
            if (!setting.countdowns?.[id]) return;
            const data = setting.toObject();
            data.countdowns[id].progress.current = current;
            data.countdowns[id].progress.start = start;
            this._writingCountdown = true;
            await game.settings.set(...COUNTDOWN_SETTING, data);
        } catch (err) {
            console.warn(`${MOD} |`, err);
        } finally {
            this._writingCountdown = false;
        }
    }

    static async deleteCountdown(id) {
        if (!id) return;
        try {
            const setting = game.settings.get(...COUNTDOWN_SETTING);
            if (!setting.countdowns?.[id]) return;
            // Mesmo padrão do editor de contagens do sistema: operador de deleção da v14 + gravar o modelo
            setting.updateSource({ [`countdowns.${id}`]: globalThis._del ?? null });
            this._writingCountdown = true;
            await game.settings.set(...COUNTDOWN_SETTING, setting);
            const after = game.settings.get(...COUNTDOWN_SETTING);
            if (after.countdowns?.[id]) {
                after.updateSource({ [`countdowns.-=${id}`]: null });
                await game.settings.set(...COUNTDOWN_SETTING, after);
            }
        } catch (err) {
            console.warn(`${MOD} |`, err);
        } finally {
            this._writingCountdown = false;
        }
    }

    /** O mestre pode mexer na contagem pelo rastreador do sistema; acompanhamos aqui. */
    static onCountdownsChanged() {
        if (!isActiveGM() || this._writingCountdown) return;
        const state = getState();
        if (!state.active || !state.countdownId) return;
        const countdown = game.settings.get(...COUNTDOWN_SETTING)?.countdowns?.[state.countdownId];
        if (!countdown) return;
        const current = countdown.progress.current;
        if (current === state.counter && countdown.progress.start === state.max) return;
        this.serialize(async () => {
            await this.setState({ counter: current, max: Math.max(countdown.progress.start, current) });
            if (current <= 0) await this._end('countdown');
        });
    }

    /* -------------------------------------------- */
    /*  Efeitos ativos                              */
    /* -------------------------------------------- */

    static changesFor(actor, traits) {
        const has = i => traits.includes(i);
        const change = (key, type, value) => ({ key, type, value, phase: 'initial', priority: null });
        const changes = [];
        if (actor.type === 'adversary') {
            if (has(0)) changes.push(change('system.bonuses.damage.bonus', 'add', 2));
            if (has(1)) changes.push(change('system.difficulty', 'add', 1));
            if (has(2) && actor.system?.type !== 'minion') {
                changes.push(change('system.damageThresholds.major', 'add', 2));
                changes.push(change('system.damageThresholds.severe', 'add', 2));
            }
            if (has(4)) changes.push(change('system.criticalThreshold', 'downgrade', 19));
        } else if (actor.type === 'environment') {
            if (has(1)) changes.push(change('system.difficulty', 'add', 1));
        } else if (actor.type === 'character') {
            if (has(3)) changes.push(change('system.rules.dualityRoll.defaultHopeDice', 'override', 10));
        }
        return changes;
    }

    static effectData(actor, traits) {
        const changes = this.changesFor(actor, traits);
        if (!changes.length) return null;
        const list = traits
            .filter(i => TRAITS[i].targets.includes(actor.type))
            .map(i => `<li><strong>${t(`Traits.${TRAITS[i].id}.name`)}</strong>: ${t(`Traits.${TRAITS[i].id}.text`)}</li>`)
            .join('');
        return {
            _id: EFFECT_ID,
            name: t('Effect.Name'),
            img: icon(),
            type: 'base',
            transfer: false,
            disabled: false,
            statuses: [EFFECT_STATUS],
            description: `<p>${t('Effect.Description')}</p><ul>${list}</ul>`,
            showIcon: CONST.ACTIVE_EFFECT_SHOW_ICON?.ALWAYS ?? 2,
            flags: { [MOD]: { [FLAG]: true } },
            system: {
                changes,
                duration: { type: 'temporary', description: t('Effect.Duration') },
                conditionals: []
            }
        };
    }

    static async applyTo(actor, traits) {
        const data = this.effectData(actor, traits);
        const existing = actor.effects.get(EFFECT_ID);
        try {
            if (!data) {
                if (existing) await existing.delete();
                return false;
            }
            if (existing) await existing.update({ 'system.changes': data.system.changes, description: data.description, disabled: false });
            else await actor.createEmbeddedDocuments('ActiveEffect', [data], { keepId: true, [MOD]: true });
            return true;
        } catch (err) {
            console.warn(`${MOD} | Falha ao aplicar o Eclipse em ${actor.name}`, err);
            return false;
        }
    }

    static affectedScenes() {
        return [...new Set([game.scenes.active, canvas?.scene].filter(Boolean))];
    }

    static async applyEffects(traits) {
        if (!game.settings.get(MOD, 'applyEffects') || !traits.length) return [];
        const actors = game.actors.filter(a => AFFECTED_TYPES.includes(a.type));
        for (let i = 0; i < actors.length; i += 20) {
            await Promise.all(actors.slice(i, i + 20).map(a => this.applyTo(a, traits)));
        }
        // Tokens não vinculados: herdam do ator base pelo mesmo id; se não herdarem, recebem no delta
        const tokenEffects = [];
        for (const scene of this.affectedScenes()) {
            for (const td of scene.tokens) {
                if (td.actorLink || !td.actor || !AFFECTED_TYPES.includes(td.actor.type)) continue;
                if (td.actor.effects.get(EFFECT_ID)) continue;
                if (await this.applyTo(td.actor, traits)) tokenEffects.push(td.uuid);
            }
        }
        return tokenEffects;
    }

    static async removeEffects(tokenUuids = []) {
        const actors = game.actors.filter(a => a.effects.get(EFFECT_ID));
        for (let i = 0; i < actors.length; i += 20) {
            await Promise.all(actors.slice(i, i + 20).map(a => a.effects.get(EFFECT_ID)?.delete().catch(() => null)));
        }
        const uuids = new Set(tokenUuids);
        for (const scene of this.affectedScenes()) for (const td of scene.tokens) if (!td.actorLink) uuids.add(td.uuid);
        for (const uuid of uuids) {
            const td = await fromUuid(uuid).catch(() => null);
            if (!td?.actor || td.actorLink) continue;
            // Só apagamos cópias guardadas no delta do token (nunca criar "lápide" do efeito herdado)
            const inDelta = td.delta?.effects?.get?.(EFFECT_ID);
            if (inDelta) await td.actor.deleteEmbeddedDocuments('ActiveEffect', [EFFECT_ID]).catch(() => null);
        }
    }

    static async onDocumentCreated(actor, tokenDoc) {
        if (!actor || !isActiveGM() || !AFFECTED_TYPES.includes(actor.type)) return;
        const state = getState();
        if (!state.active || !game.settings.get(MOD, 'applyEffects')) return;
        if (actor.effects.get(EFFECT_ID)) return;
        const ok = await this.applyTo(actor, state.traits);
        if (ok && tokenDoc && !tokenDoc.actorLink) {
            await this.setState({ tokenEffects: [...state.tokenEffects, tokenDoc.uuid] });
        }
    }

    /** Ao carregar o mundo: garante que os efeitos batem com o estado salvo. */
    static async verifyConsistency() {
        const state = getState();
        if (state.active) {
            const tokenEffects = await this.applyEffects(state.traits);
            if (tokenEffects.length) await this.setState({ tokenEffects: [...new Set([...state.tokenEffects, ...tokenEffects])] });
        } else if (game.actors.some(a => a.effects.get(EFFECT_ID))) {
            await this.removeEffects(state.tokenEffects);
        }
    }

    /* -------------------------------------------- */
    /*  Fim                                         */
    /* -------------------------------------------- */

    static end(reason = 'sunset') {
        if (!game.user.isGM) return ui.notifications.warn(t('Errors.GMOnly'));
        return this.serialize(() => this._end(reason));
    }

    static async _end(reason = 'sunset') {
        const state = getState();
        if (!state.active || this._ending) return;
        this._ending = true;
        try {
            await this.removeEffects(state.tokenEffects);
            await this.deleteCountdown(state.countdownId);
            if (state.sceneId && state.prevDarkness !== null) {
                const scene = game.scenes.get(state.sceneId);
                if (scene) await scene.update({ 'environment.darknessLevel': state.prevDarkness }, { animateDarkness: 6000 });
            }
            const history = [{ endedAt: Date.now(), startedAt: state.startedAt, traits: state.traits, reason }, ...(state.history ?? [])].slice(0, 10);
            const next = foundry.utils.mergeObject(foundry.utils.deepClone(DEFAULT_STATE), {
                usedSinceLongRest: state.usedSinceLongRest, history
            });
            await game.settings.set(MOD, 'state', next);
            await this.chatCard('end', { ...state, reason });
            Hooks.callAll(`${MOD}.end`, state, reason);
        } finally {
            this._ending = false;
        }
    }

    static async resetLongRest() {
        await this.setState({ usedSinceLongRest: false });
    }

    /* -------------------------------------------- */
    /*  Chat                                        */
    /* -------------------------------------------- */

    static async chatCard(kind, state) {
        const traits = (state.traits ?? []).map(i => ({
            ...TRAITS[i],
            name: t(`Traits.${TRAITS[i].id}.name`),
            text: t(`Traits.${TRAITS[i].id}.text`),
            range: `${TRAITS[i].range[0]}–${TRAITS[i].range[1]}`
        }));
        const content = await foundry.applications.handlebars.renderTemplate(`modules/${MOD}/templates/chat-${kind}.hbs`, {
            banner: banner(),
            icon: icon(),
            traits,
            rolls: state.rolls ?? [],
            counter: state.counter,
            max: state.max,
            players: state.players,
            fear: state.fear,
            duplicates: state.duplicates,
            notes: state.notes,
            reason: state.reason ? t(`End.Reason.${state.reason}`) : ''
        });
        return ChatMessage.implementation.create({
            content,
            speaker: { alias: t('Chat.Speaker') },
            flags: { [MOD]: { card: kind } }
        });
    }
}
