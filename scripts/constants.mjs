export const MOD = 'eclipse-na-terra-da-fartura';
/** Base dos arquivos do módulo (trocada por devBoot para testar direto do GitHub). */
export const BASE = { url: `modules/${MOD}` };
export const asset = p => `${BASE.url}/assets/${p}`;
export const icon = () => asset('ui/eclipse-icon.webp');
export const banner = () => asset('ui/titulo-eclipse.webp');
export const FLAG = 'eclipse';
export const EFFECT_STATUS = 'eclipse-ntf';

/**
 * Características do Eclipse (tabela d10 da revista).
 * `targets` indica que tipos de ator recebem o efeito ativo automaticamente.
 */
export const TRAITS = [
    {
        id: 'dano', range: [1, 2], icon: 'fa-solid fa-burst',
        img: 'icons/skills/melee/strike-slashes-red.webp', targets: ['adversary']
    },
    {
        id: 'dificuldade', range: [3, 4], icon: 'fa-solid fa-shield-halved',
        img: 'icons/magic/perception/shadow-stealth-eyes-purple.webp', targets: ['adversary', 'environment']
    },
    {
        id: 'limiares', range: [5, 6], icon: 'fa-solid fa-heart-crack',
        img: 'icons/magic/defensive/shield-barrier-flaming-pentagon-orange.webp', targets: ['adversary']
    },
    {
        id: 'esperanca', range: [7, 8], icon: 'fa-solid fa-dice-d10',
        img: 'icons/magic/light/explosion-star-small-blue-yellow.webp', targets: ['character']
    },
    {
        id: 'critico', range: [9, 10], icon: 'fa-solid fa-paw',
        img: 'icons/creatures/claws/claw-talons-glowing-purple.webp', targets: ['adversary']
    }
];

export const traitForRoll = r => TRAITS.findIndex(tr => r >= tr.range[0] && r <= tr.range[1]);

export const DEFAULT_STATE = {
    active: false,
    traits: [],
    notes: '',
    rolls: [],
    duplicates: 0,
    counter: 0,
    max: 0,
    players: 0,
    fear: 0,
    countdownId: null,
    startedAt: null,
    sceneId: null,
    prevDarkness: null,
    tokenEffects: [],
    usedSinceLongRest: false,
    history: []
};

export function t(key, data) {
    const k = `ECLIPSE.${key}`;
    return data ? game.i18n.format(k, data) : game.i18n.localize(k);
}

export function getState() {
    try {
        return foundry.utils.mergeObject(foundry.utils.deepClone(DEFAULT_STATE), game.settings.get(MOD, 'state') ?? {}, { inplace: false });
    } catch {
        return foundry.utils.deepClone(DEFAULT_STATE);
    }
}

export function isActiveGM() {
    return game.user.isGM && (game.users.activeGM?.isSelf ?? true);
}

export function currentFear() {
    try {
        return Number(game.settings.get('daggerheart', 'ResourcesFear')) || 0;
    } catch {
        return 0;
    }
}

export function maxFear() {
    try {
        return ui.resources?.maxFear ?? game.settings.get('daggerheart', 'Homebrew')?.maxFear ?? 12;
    } catch {
        return 12;
    }
}

/** Quantos jogadores estão na cena: personagens do grupo ativo, tokens de PJ na cena ou usuários conectados. */
export function guessPlayers() {
    const party = game.actors.find(a => a.type === 'party' && a.system?.active);
    const partySize = party?.system?.partyMembers?.length;
    if (partySize) return partySize;
    const pcTokens = canvas?.scene?.tokens?.filter(tk => tk.actor?.type === 'character' && tk.actor?.hasPlayerOwner) ?? [];
    const unique = new Set(pcTokens.map(tk => tk.actor.id));
    if (unique.size) return unique.size;
    return Math.max(1, game.users.filter(u => u.active && !u.isGM).length);
}
