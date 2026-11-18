import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from lib import *
import adversaries, environments, journal

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRCP = os.path.join(ROOT, 'src', 'packs')

TRAIT_ROWS = [
    ((1, 2), 'Fúria da Noite', 'Aumente o dano dos adversários em +2.', 'icons/skills/melee/strike-slashes-red.webp'),
    ((3, 4), 'Sombra Espessa', 'Aumente a Dificuldade de todos os adversários e ambientes em 1, enquanto o Eclipse durar.', 'icons/magic/perception/shadow-stealth-eyes-purple.webp'),
    ((5, 6), 'Couro da Noite', 'Aumente os limiares de dano dos adversários em +2.', 'icons/magic/defensive/shield-barrier-flaming-pentagon-orange.webp'),
    ((7, 8), 'Esperança Minguante', 'Diminua o Dado de Esperança dos jogadores para um d10.', 'icons/magic/light/explosion-star-small-blue-yellow.webp'),
    ((9, 10), 'Garras da Onça Celeste', 'Todas as criaturas obtêm sucesso crítico ao rolar 19 ou 20 em testes de ataque contra personagens.', 'icons/creatures/claws/claw-talons-glowing-purple.webp'),
]


def rolltable():
    tid = gid('table', 'eclipse')
    results = []
    for i, ((a, b), name, desc, img) in enumerate(TRAIT_ROWS):
        rid = gid('table', 'eclipse', i)
        results.append({'_id': rid, 'type': 'text', 'name': name, 'description': f'<p>{desc}</p>', 'img': img,
                        'range': [a, b], 'weight': b - a + 1, 'drawn': False, 'flags': {},
                        '_key': f'!tables.results!{tid}.{rid}'})
    return {'_id': tid, 'name': 'Características do Eclipse', 'img': f'{ASSET}/ui/eclipse-icon.webp',
            'description': '<p>Role um d10 para cada Ponto de Medo gasto ao iniciar um Eclipse. Se um dado cair em uma característica já adicionada, aumente a contagem em 2.</p>',
            'formula': '1d10', 'replacement': True, 'displayRoll': True, 'results': results, 'folder': None,
            'sort': 0, 'flags': {}, 'ownership': {'default': 0}, '_stats': dict(STATS, compendiumSource=None),
            '_key': f'!tables!{tid}'}


def macro(key, name, img, command, sort):
    mid = gid('macro', key)
    return {'_id': mid, 'name': name, 'type': 'script', 'img': img, 'command': command, 'scope': 'global',
            'folder': None, 'sort': sort, 'flags': {}, 'ownership': {'default': 0},
            '_stats': dict(STATS, compendiumSource=None), '_key': f'!macros!{mid}'}


def macros():
    api = f"game.modules.get('{MOD}')?.api"
    return [
        macro('abrir', 'Eclipse: abrir janela', f'{ASSET}/ui/eclipse-icon.webp', f'{api}?.open();', 100),
        macro('encerrar', 'Eclipse: pôr do sol (encerrar)', 'icons/magic/light/explosion-star-glow-yellow.webp', f'{api}?.end();', 200),
        macro('tick', 'Eclipse: avançar contagem (−1)', 'icons/magic/time/hourglass-tilted-glowing-gold.webp', f'{api}?.tick(-1);', 300),
        macro('guia', 'Eclipse: abrir Guia do Mestre', 'icons/sundries/scrolls/scroll-bound-sealed-red-tan.webp',
              f"(await fromUuid('Compendium.{MOD}.diario-mestre.JournalEntry.{gid('journal', 'guia-mestre')}'))?.sheet.render(true);", 400),
    ]


def main():
    advs = adversaries.build()
    write_pack(SRCP, 'adversarios', advs)
    write_pack(SRCP, 'ambientes', environments.build_env())
    write_pack(SRCP, 'aliados', environments.build_npc())
    jog, mes = journal.build_journals()
    write_pack(SRCP, 'diario-jogadores', jog)
    write_pack(SRCP, 'diario-mestre', mes)
    write_pack(SRCP, 'tabelas', [rolltable()])
    write_pack(SRCP, 'macros', macros())
    # Dados da tabela também para o JS
    with open(os.path.join(ROOT, 'scripts', 'traits.json'), 'w', encoding='utf-8') as fh:
        json.dump([{'range': r, 'name': n, 'text': t, 'img': i} for r, n, t, i in TRAIT_ROWS], fh, ensure_ascii=False, indent=2)
    print('ok', len(advs))


if __name__ == '__main__':
    main()
