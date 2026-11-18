import { MOD, DEFAULT_STATE } from './constants.mjs';
import { EclipseOverlay } from './overlay.mjs';
import { EclipseApp } from './eclipse-app.mjs';

export function registerSettings() {
    const reg = game.settings.register.bind(game.settings);
    game.settings.register = (ns, key, data) => (game.settings.settings.has(`${ns}.${key}`) ? null : reg(ns, key, data));
    try {
    game.settings.register(MOD, 'state', {
        scope: 'world',
        config: false,
        type: Object,
        default: foundry.utils.deepClone(DEFAULT_STATE),
        onChange: () => {
            EclipseOverlay.sync({ animate: true });
            EclipseApp.refresh();
        }
    });

    game.settings.register(MOD, 'darkenScene', {
        name: 'ECLIPSE.Settings.DarkenScene.Name',
        hint: 'ECLIPSE.Settings.DarkenScene.Hint',
        scope: 'world',
        config: true,
        type: Boolean,
        default: true
    });

    game.settings.register(MOD, 'darknessLevel', {
        name: 'ECLIPSE.Settings.DarknessLevel.Name',
        hint: 'ECLIPSE.Settings.DarknessLevel.Hint',
        scope: 'world',
        config: true,
        type: Number,
        range: { min: 0, max: 1, step: 0.05 },
        default: 0.85
    });

    game.settings.register(MOD, 'applyEffects', {
        name: 'ECLIPSE.Settings.ApplyEffects.Name',
        hint: 'ECLIPSE.Settings.ApplyEffects.Hint',
        scope: 'world',
        config: true,
        type: Boolean,
        default: true
    });

    game.settings.register(MOD, 'autoTick', {
        name: 'ECLIPSE.Settings.AutoTick.Name',
        hint: 'ECLIPSE.Settings.AutoTick.Hint',
        scope: 'world',
        config: true,
        type: Boolean,
        default: true
    });

    game.settings.register(MOD, 'useSystemCountdown', {
        name: 'ECLIPSE.Settings.SystemCountdown.Name',
        hint: 'ECLIPSE.Settings.SystemCountdown.Hint',
        scope: 'world',
        config: true,
        type: Boolean,
        default: false
    });

    game.settings.register(MOD, 'soundStart', {
        name: 'ECLIPSE.Settings.SoundStart.Name',
        hint: 'ECLIPSE.Settings.SoundStart.Hint',
        scope: 'world',
        config: true,
        type: String,
        filePicker: 'audio',
        default: ''
    });

    game.settings.register(MOD, 'soundEnd', {
        name: 'ECLIPSE.Settings.SoundEnd.Name',
        hint: 'ECLIPSE.Settings.SoundEnd.Hint',
        scope: 'world',
        config: true,
        type: String,
        filePicker: 'audio',
        default: ''
    });

    game.settings.register(MOD, 'overlayIntensity', {
        name: 'ECLIPSE.Settings.Intensity.Name',
        hint: 'ECLIPSE.Settings.Intensity.Hint',
        scope: 'client',
        config: true,
        type: String,
        choices: {
            full: 'ECLIPSE.Settings.Intensity.Full',
            subtle: 'ECLIPSE.Settings.Intensity.Subtle',
            off: 'ECLIPSE.Settings.Intensity.Off'
        },
        default: 'full',
        onChange: () => EclipseOverlay.sync({ animate: false })
    });

    game.settings.register(MOD, 'playAnimations', {
        name: 'ECLIPSE.Settings.Animations.Name',
        hint: 'ECLIPSE.Settings.Animations.Hint',
        scope: 'client',
        config: true,
        type: Boolean,
        default: true
    });

    game.settings.register(MOD, 'hudPosition', {
        name: 'ECLIPSE.Settings.HudPosition.Name',
        scope: 'client',
        config: true,
        type: String,
        choices: {
            top: 'ECLIPSE.Settings.HudPosition.Top',
            bottom: 'ECLIPSE.Settings.HudPosition.Bottom',
            hidden: 'ECLIPSE.Settings.HudPosition.Hidden'
        },
        default: 'top',
        onChange: () => EclipseOverlay.sync({ animate: false })
    });
    } finally {
        delete game.settings.register;
    }
}
