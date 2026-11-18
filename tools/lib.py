"""Helpers para gerar documentos do sistema Daggerheart (Foundryborne) em JSON de compêndio."""
import hashlib, re, json, os

MOD = 'eclipse-na-terra-da-fartura'
ASSET = f'modules/{MOD}/assets'
B62 = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'


def gid(*parts):
    h = int(hashlib.sha1('|'.join(map(str, parts)).encode()).hexdigest(), 16)
    s = ''
    for _ in range(16):
        h, r = divmod(h, 62)
        s += B62[r]
    return s


STATS = {"coreVersion": "14.364", "systemId": "daggerheart", "systemVersion": "2.12.9"}

RANGES = {'cac': 'melee', 'melee': 'melee', 'mp': 'veryClose', 'veryClose': 'veryClose', 'p': 'close', 'close': 'close',
          'd': 'far', 'far': 'far', 'md': 'veryFar', 'veryFar': 'veryFar', '': ''}

DT = {'fis': 'physical', 'mag': 'magical', 'physical': 'physical', 'magical': 'magical'}


def dice_value(formula):
    formula = str(formula).replace(' ', '')
    m = re.fullmatch(r'(\d+)d(\d+)(?:\+(\d+))?', formula)
    if m:
        return {'multiplier': 'flat', 'flatMultiplier': int(m[1]), 'dice': 'd' + m[2],
                'bonus': int(m[3]) if m[3] else None, 'custom': {'enabled': False, 'formula': ''}}
    return {'multiplier': 'flat', 'flatMultiplier': 1, 'dice': 'd6', 'bonus': None,
            'custom': {'enabled': True, 'formula': formula}}


def main_damage(formula, dtype='fis', direct=False, alt=None):
    return {'value': dice_value(formula), 'applyTo': 'hitPoints', 'type': [DT[dtype]], 'base': False,
            'resultBased': False, 'valueAlt': dice_value(alt) if alt else None, 'includeBase': False,
            'direct': direct, 'fullRestore': False, 'itemId': None}


def res_value(resource, amount):
    return {'value': dice_value(str(amount)), 'applyTo': resource, 'base': False, 'resultBased': False,
            'valueAlt': None, 'fullRestore': False, 'itemId': None}


def costs(fear=0, stress=0, scalable=False):
    out = []
    if fear:
        out.append({'scalable': scalable, 'key': 'fear', 'value': fear, 'step': 1 if scalable else None,
                    'itemId': None, 'consumeOnSuccess': False})
    if stress:
        out.append({'scalable': scalable, 'key': 'stress', 'value': stress, 'step': 1 if scalable else None,
                    'itemId': None, 'consumeOnSuccess': False})
    return out


def roll(rtype=None):
    return {'type': rtype, 'trait': None, 'difficulty': None, 'bonus': None, 'advState': 'neutral',
            'diceRolling': {'multiplier': 'prof', 'flatMultiplier': 1, 'dice': 'd6', 'compare': None, 'treshold': None},
            'useDefault': False}


class A:
    """Construtores de ações. Cada função devolve um dict sem _id (atribuído no Feature)."""

    @staticmethod
    def _base(atype, name, img=None, fear=0, stress=0, rng='', target='any', amount=None, effects=(),
              actionType='action', uses=None, recovery=None, scalable=False):
        return {'type': atype, 'systemPath': 'actions', 'name': name, 'img': img, 'description': '',
                'chatDisplay': True, 'actionType': actionType, 'baseAction': False,
                'originItem': {'type': 'itemCollection'},
                'cost': costs(fear, stress, scalable),
                'uses': {'value': None, 'max': str(uses) if uses else '', 'recovery': recovery, 'consumeOnSuccess': False},
                'target': {'type': target, 'amount': amount},
                '_effects': list(effects), 'range': RANGES[rng], 'triggers': [], 'areas': []}

    @staticmethod
    def spend(name='Gastar', fear=0, stress=0, **kw):
        a = A._base('effect', name, fear=fear, stress=stress, **kw)
        return a

    @staticmethod
    def attack(name, formula, dtype='fis', rng='mp', fear=0, stress=0, direct=False, effects=(), amount=1, **kw):
        a = A._base('attack', name, fear=fear, stress=stress, rng=rng, effects=effects, amount=amount, **kw)
        a['roll'] = roll('attack')
        a['damage'] = {'main': main_damage(formula, dtype, direct) if formula else None, 'resources': {}}
        a['save'] = {'trait': None, 'difficulty': None, 'damageMod': 'none'}
        return a

    @staticmethod
    def save(name, trait, formula=None, dtype='fis', rng='p', fear=0, stress=0, half=False, direct=False,
             effects=(), resources=None, **kw):
        a = A._base('attack', name, fear=fear, stress=stress, rng=rng, effects=effects, **kw)
        a['roll'] = roll(None)
        a['damage'] = {'main': main_damage(formula, dtype, direct) if formula else None,
                       'resources': {k: res_value(k, v) for k, v in (resources or {}).items()}}
        a['save'] = {'trait': trait, 'difficulty': None, 'damageMod': 'half' if half else 'none'}
        return a

    @staticmethod
    def damage(name, formula=None, dtype='fis', direct=False, resources=None, fear=0, stress=0, rng='', **kw):
        a = A._base('damage', name, fear=fear, stress=stress, rng=rng, **kw)
        a['damage'] = {'main': main_damage(formula, dtype, direct) if formula else None,
                       'resources': {k: res_value(k, v) for k, v in (resources or {}).items()}}
        return a

    @staticmethod
    def heal(name, resource='hitPoints', amount=1, target='self', fear=0, stress=0, rng='', **kw):
        a = A._base('healing', name, fear=fear, stress=stress, rng=rng, target=target, **kw)
        a['damage'] = {'main': None, 'resources': {resource: res_value(resource, amount)}}
        a['roll'] = roll(None)
        return a

    @staticmethod
    def gain_fear(name='Ganhar Medo', amount=1, **kw):
        a = A.heal(name, 'fear', amount, target='any', actionType='reaction', **kw)
        return a

    @staticmethod
    def countdown(name, start, img=None, looping='noLooping', ctype='encounter', **kw):
        a = A._base('countdown', 'Iniciar Contagem', **kw)
        a['countdown'] = [{'name': name, 'type': ctype, 'hidden': False,
                           'img': img or 'icons/magic/time/hourglass-tilted-glowing-gold.webp',
                           'progress': {'looping': looping, 'type': 'custom', 'startFormula': str(start),
                                        'current': 1, 'start': 1}, 'ownership': {}}]
        return a

    @staticmethod
    def transform(uuid, name='Transformar', **kw):
        a = A._base('transform', name, **kw)
        a['transform'] = {'actorUUID': uuid, 'resourceRefresh': {'hitPoints': True, 'stress': True}}
        return a

    @staticmethod
    def summon(uuid, count, name='Invocar', fear=0, stress=0, **kw):
        a = A._base('summon', name, fear=fear, stress=stress, **kw)
        a['summon'] = [{'actorUUID': uuid, 'count': str(count)}]
        return a


class E:
    """Efeitos (condições) anexados a features e aplicados pelos botões do chat."""

    def __init__(self, name, desc, img, statuses=(), duration='', changes=()):
        self.name, self.desc, self.img, self.statuses, self.duration, self.changes = name, desc, img, statuses, duration, changes


# Condições recorrentes do cenário
def imobilizado(extra=''):
    return E('Imobilizado', f'<p><em>Imobilizado</em>: não pode se mover, mas ainda pode agir no lugar.{(" " + extra) if extra else ""}</p>',
             'icons/magic/control/debuff-chains-shackles-movement-blue.webp', ['restrained'])


def vulneravel(extra=''):
    return E('Vulnerável', f'<p><em>Vulnerável</em>: todas as rolagens contra a criatura têm vantagem.{(" " + extra) if extra else ""}</p>',
             'icons/magic/control/silhouette-fall-slip-prone.webp', ['vulnerable'])


def feature(actor_key, name, form, desc, actions=(), effects=(), img=None, sort=0):
    """Monta um item do tipo feature com ações e efeitos.
    actor_key: identificador estável do ator (para ids determinísticos)."""
    iid = gid(actor_key, 'item', name)
    effs = []
    for e in effects:
        eid = gid(actor_key, name, 'effect', e.name)
        effs.append((e, eid))
    acts = {}
    for i, a in enumerate(actions):
        a = dict(a)
        aid = gid(actor_key, name, 'action', i, a['name'])
        a['_id'] = aid
        a['img'] = a.get('img') or img
        wanted = a.pop('_effects', [])
        ids = []
        for w in wanted:
            for e, eid in effs:
                if e.name == w:
                    ids.append({'_id': eid, 'onSave': False})
        a['effects'] = ids
        acts[aid] = a
    return {'name': name, 'type': 'feature', '_id': iid, 'img': img or 'icons/magic/symbols/rune-sigil-red-orange.webp',
            'system': {'description': desc, 'resource': None, 'actions': acts, 'featureForm': form,
                       'attribution': {'source': 'DOZE Vol. 1 — Eclipse na Terra da Fartura', 'page': None, 'artist': ''},
                       'gmNotes': '', 'granter': None, 'actorResources': []},
            'effects': [effect_doc(e, eid, img) for e, eid in effs],
            'folder': None, 'sort': sort, 'flags': {}, '_stats': dict(STATS, compendiumSource=None)}


def effect_doc(e, eid, fallback_img=None):
    return {'name': e.name, 'img': e.img or fallback_img, '_id': eid, 'type': 'base', 'transfer': False,
            'disabled': False, 'description': e.desc, 'statuses': list(e.statuses), 'tint': '#ffffff',
            'system': {'changes': list(e.changes), 'duration': {'type': e.duration, 'description': ''},
                       'rangeDependence': None, 'stacking': None, 'targetDispositions': [], 'conditionals': []},
            'sort': 0, 'flags': {}, '_stats': dict(STATS, compendiumSource=None)}


def prototype_token(name, tex, size=1, disposition=-1, scale=1.0, actorLink=False):
    return {'name': name, 'displayName': 20, 'actorLink': actorLink, 'width': size, 'height': size,
            'texture': {'src': tex, 'anchorX': 0.5, 'anchorY': 0.5, 'fit': 'contain', 'scaleX': scale, 'scaleY': scale,
                        'tint': '#ffffff', 'alphaThreshold': 0.75},
            'lockRotation': True, 'rotation': 0, 'alpha': 1, 'disposition': disposition, 'displayBars': 20,
            'bar1': {'attribute': 'resources.hitPoints'}, 'bar2': {'attribute': 'resources.stress'},
            'sight': {'enabled': False}, 'ring': {'enabled': False}, 'flags': {}, 'randomImg': False,
            'appendNumber': True, 'prependAdjective': False}


def finalize_actor(doc):
    """Aplica _key em ator, itens e efeitos para o foundryvtt-cli."""
    aid = doc['_id']
    doc['_key'] = f'!actors!{aid}'
    doc.setdefault('effects', [])
    doc['_stats'] = dict(STATS, compendiumSource=None)
    for it in doc.get('items', []):
        it['_key'] = f'!actors.items!{aid}.{it["_id"]}'
        for ef in it.get('effects', []):
            ef['_key'] = f'!actors.items.effects!{aid}.{it["_id"]}.{ef["_id"]}'
    for ef in doc['effects']:
        ef['_key'] = f'!actors.effects!{aid}.{ef["_id"]}'
    return doc


def folder(pack_type, name, key, sort=0, color=None):
    fid = gid('folder', pack_type, key)
    return {'_id': fid, 'name': name, 'type': pack_type, 'folder': None, 'color': color, 'sorting': 'm',
            'sort': sort, 'description': '', 'flags': {}, '_key': f'!folders!{fid}'}


def write_pack(root, pack, docs):
    d = os.path.join(root, pack)
    os.makedirs(d, exist_ok=True)
    for f in os.listdir(d):
        os.remove(os.path.join(d, f))
    for doc in docs:
        slug = re.sub(r'[^A-Za-z0-9]+', '_', doc['name'])[:40]
        with open(os.path.join(d, f'{slug}_{doc["_id"]}.json'), 'w', encoding='utf-8') as fh:
            json.dump(doc, fh, ensure_ascii=False, indent=2)
