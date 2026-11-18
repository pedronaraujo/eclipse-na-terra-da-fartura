from lib import *

PACK = 'adversarios'
SRC = 'DOZE Vol. 1 — Eclipse na Terra da Fartura'


def uuid(key):
    return f'Compendium.{MOD}.{PACK}.Actor.{gid("actor", key)}'


def link(key, label):
    return f'@UUID[{uuid(key)}]{{{label}}}'


SRD = 'Compendium.daggerheart.adversaries.Actor.'

ARTIST = 'Rodrigo Martins, André Ignatiuk, Ranzinza Cinza'


def P(*ps):
    return ''.join(f'<p>{p}</p>' for p in ps)


def adversary(key, name, tier, atype, dif, major, severe, hp, stress, short, motives, attack, exps, lore, feats,
              art=None, token=None, size='medium', resist=(), horde=None, page=None, folder=None, sort=0,
              extra_desc=''):
    aid = gid('actor', key)
    tok = f'{ASSET}/tokens/{token or key}.webp'
    img = f'{ASSET}/art/{art}.webp' if art else tok
    att = None
    if attack:
      an, arng, abonus, aform, atype_d = attack
      att = {'_id': gid(key, 'attack'), 'systemPath': 'attack', 'type': 'attack', 'name': an,
           'img': 'icons/skills/melee/blood-slash-foam-red.webp', 'range': RANGES[arng], 'chatDisplay': False,
           'actionType': 'action', 'baseAction': False, 'originItem': {'type': 'itemCollection'},
           'description': '', 'cost': [], 'uses': {'value': None, 'max': None, 'recovery': None, 'consumeOnSuccess': False},
           'target': {'type': 'any', 'amount': 1}, 'effects': [], 'triggers': [], 'areas': [],
           'save': {'trait': None, 'difficulty': None, 'damageMod': 'none'},
           'roll': dict(roll('attack'), bonus=abonus),
           'damage': {'main': main_damage(aform, atype_d, alt=horde[1] if horde else None), 'resources': {}}}
    items = []
    for i, f in enumerate(feats):
        name_f, form, desc, *rest = f
        opts = rest[0] if rest else {}
        items.append(feature(key, name_f, form, desc, actions=opts.get('actions', ()), effects=opts.get('effects', ()),
                             img=opts.get('img'), sort=(i + 1) * 100))
    description = (f'<p><em>{short}</em></p>' + extra_desc +
                   (f'<div class="eclipse-lore">{lore}</div>' if lore else ''))
    doc = {
        '_id': aid, 'name': name, 'type': 'adversary', 'img': img, 'folder': folder, 'sort': sort,
        'system': {
            'tier': tier, 'type': atype, 'difficulty': dif,
            'damageThresholds': {'major': major, 'severe': severe},
            'resources': {'hitPoints': {'value': 0, 'max': hp}, 'stress': {'value': 0, 'max': stress}},
            'motivesAndTactics': motives, 'description': description, 'notes': '',
            'experiences': {gid(key, 'exp', n): {'name': n, 'value': v, 'description': ''} for n, v in exps},
            'attack': att,
            'resistance': {t: {'resistance': t in resist, 'immunity': False, 'reduction': 0} for t in ('physical', 'magical')},
            'attribution': {'source': SRC, 'page': page, 'artist': ARTIST if art else '', 'srd': False},
            'size': size, 'criticalThreshold': 20,
            'typeData': {'type': 'horde', 'hordeHP': horde[0], 'hordeDamage': horde[1]} if horde else None,
            'advantageSources': [], 'disadvantageSources': []
        },
        'prototypeToken': prototype_token(name, tok, size={'large': 2, 'huge': 3}.get(size, 1)),
        'items': items, 'effects': [], 'flags': {MOD: {'key': key}}
    }
    return finalize_actor(doc)


# ---------------------------------------------------------------- ícones
I = dict(
    heal='icons/magic/life/heart-cross-strong-green.webp', water='icons/magic/water/wave-water-teal.webp',
    love='icons/magic/life/heart-pink.webp', peace='icons/skills/social/diplomacy-handshake.webp',
    snake='icons/creatures/reptiles/snake-fangs-bite-green.webp', poison='icons/skills/toxins/symbol-poison-drop-skull-green.webp',
    rage='icons/magic/control/fear-fright-monster-red.webp', dark='icons/magic/perception/shadow-stealth-eyes-purple.webp',
    fear='icons/magic/control/fear-fright-monster-grin-purple-blue.webp', sack='icons/environment/traps/cage-grey-steel.webp',
    eat='icons/creatures/abilities/mouth-teeth-rows-red.webp', fur='icons/creatures/abilities/bear-roar-bite-brown.webp',
    scream='icons/magic/sonic/projectile-sound-rings-wave.webp', fire='icons/magic/fire/flame-burning-earth-orange.webp',
    firebreath='icons/creatures/abilities/dragon-fire-breath-orange.webp', relentless='icons/magic/unholy/silhouette-evil-horned-giant.webp',
    momentum='icons/skills/melee/strike-weapons-orange.webp', kick='icons/creatures/mammals/ox-bull-horned-glowing-orange.webp',
    knife='icons/skills/melee/strike-dagger-blood-red.webp', acid='icons/magic/acid/dissolve-bone-skull.webp',
    slow='icons/magic/time/hourglass-tilted-gray.webp', swallow='icons/creatures/abilities/mouth-teeth-lamprey-red.webp',
    shape='icons/magic/control/silhouette-hold-change-green.webp', root='icons/magic/nature/root-vine-entangled-humanoid.webp',
    storm='icons/magic/lightning/bolt-strike-forked-blue.webp', group='icons/skills/social/diplomacy-unity-alliance.webp',
    clone='icons/magic/defensive/illusion-evasion-echo-purple.webp', beasts='icons/creatures/abilities/wolf-howl-moon-purple.webp',
    whistle='icons/magic/sonic/explosion-shock-sound-wave.webp', grow='icons/skills/movement/arrows-up-trio-red.webp',
    vertigo='icons/magic/control/hypnosis-mesmerism-swirl.webp', candle='icons/sundries/lights/candle-pillar-lit-yellow.webp',
    hat='icons/magic/symbols/mask-yellow-orange.webp', hope='icons/magic/light/explosion-star-glow-yellow.webp',
    invis='icons/magic/perception/silhouette-stealth-shadow.webp', tornado='icons/magic/air/wind-tornado-funnel-damage-blue.webp',
    boar='icons/creatures/abilities/fang-tooth-blood-red.webp', portal='icons/skills/movement/portal-silhouette-pink.webp',
    abyss='icons/magic/unholy/orb-swirling-teal.webp', mother='icons/magic/life/heart-shadow-red.webp',
    birth='icons/magic/nature/plant-sprout-snow-green.webp', horde='icons/environment/people/charge.webp',
    ghost='icons/magic/death/undead-ghost-strike-white.webp', trample='icons/creatures/mammals/bull-horned-blue.webp',
    axe='icons/weapons/axes/axe-battle-skull-black.webp', eye='icons/magic/perception/eye-ringed-glow-angry-red.webp',
    goat='icons/magic/death/skull-horned-goat-pentagram-red.webp', voices='icons/magic/control/mouth-smile-deception-purple.webp',
    sleep='icons/magic/nature/moon-crescent.webp', puppet='icons/magic/control/hypnosis-mesmerism-pendulum.webp',
    witch='icons/skills/toxins/cauldron-pot-bubbles-green.webp', wake='icons/magic/control/fear-fright-white.webp',
    devil='icons/creatures/unholy/demon-fire-horned-mask.webp', scapegoat='icons/skills/social/trading-injustice-scale-gray.webp',
    wings='icons/creatures/abilities/wing-batlike-red-pink.webp', blood='icons/skills/wounds/blood-spurt-spray-red.webp',
    dive='icons/magic/control/buff-flight-wings-runes-red-yellow.webp', energy='icons/magic/unholy/energy-smoke-pink.webp',
    mosquito='icons/creatures/abilities/stinger-poison-scorpion-brown.webp', smoke='icons/magic/air/fog-gas-smoke-dense-green.webp',
    shadow='icons/magic/unholy/silhouette-robe-evil-glow.webp', thousand='icons/magic/perception/eye-tendrils-web-purple.webp',
    purify='icons/magic/fire/flame-burning-eye.webp', terror='icons/magic/control/fear-fright-shadow-monster-red.webp',
    scales='icons/magic/acid/projectile-needles-salvo-green.webp', crawl='icons/creatures/reptiles/serpent-horned-green.webp',
    mist='icons/magic/air/fog-gas-smoke-dense-white.webp', mirror='icons/magic/symbols/ring-circle-smoke-blue.webp',
    stare='icons/magic/perception/eye-slit-pink.webp', bite_fire='icons/creatures/abilities/mouth-teeth-fire-orange.webp',
    tail='icons/creatures/tentacles/tentacle-earth-green.webp', shake='icons/magic/earth/barrier-stone-explosion-debris.webp',
    heart='icons/magic/life/heart-glowing-red.webp', protect='icons/magic/defensive/shield-barrier-glowing-triangle-green.webp',
)

FOLDERS = [folder('Actor', '1º Patamar', 't1', 100, '#5b3a1a'), folder('Actor', '2º Patamar', 't2', 200, '#6b2a16'),
           folder('Actor', '3º Patamar', 't3', 300, '#701c1c'), folder('Actor', '4º Patamar', 't4', 400, '#3a0f2a')]
FT = {i + 1: f['_id'] for i, f in enumerate(FOLDERS)}


def build():
    out = []
    # ------------------------------------------------------------------ 1º PATAMAR
    out.append(adversary(
        'cobra-norato', 'Cobra Norato', 1, 'support', 13, 6, 12, 5, 6,
        'Uma cobra verde com pontos pretos, gigante e honrosa.', 'Amar, Curar, Proteger',
        ('Mordida Protetora', 'mp', 2, '1d8+3', 'fis'), [('Eu Vou te Salvar', 4), ('Proteger', 2)],
        P('Irmão de Maria Caninana, Cobra Norato costumava ser o protetor dos viajantes e pescadores. Hoje, o encantado meio gente, meio Boiúna, se arrasta entre dois mundos com a fome de voltar a ser homem. Seu corpo é comprido e coberto de escamas frias que guardam o desenho de um rosto nas costas. Sua boca fala a língua dos humanos sem mover o queixo. Contam que leite derramado na boca e um corte de ferro limpo na testa lhe devolvem seu corpo de homem, mas o encanto só se desfaz se a mão não tremer, e toda mão treme. Quando a água do rio fica morna e para de correr, ele já passou por baixo de você.'),
        [
            ('Amor de Irmão', 'passive', P(f'Enquanto o Cobra Norato estiver em alcance Próximo da {link("maria-caninana", "Maria Caninana")}, sua Dificuldade recebe um bônus de <strong>+1</strong>.'), {'img': I['love']}),
            ('Pacifista', 'passive', P('O Cobra Norato só pode atacar um alvo depois de ser atacado.'), {'img': I['peace']}),
            ('Água Curativa', 'action', P('<strong>Marque um Ponto de Fadiga</strong> para manipular a água dos rios e curar <strong>1 Ponto de Vida</strong> de um alvo Próximo.'),
             {'img': I['water'], 'actions': [A.heal('Curar 1 PV', 'hitPoints', 1, target='any', stress=1, rng='p')]}),
            ('Meu Amor é Maior', 'reaction', P(f'Caso o Cobra Norato presencie a morte de {link("maria-caninana", "Maria Caninana")}, ele se move até ela e dá sua vida pela dela. Recupere todos os Pontos de Vida e de Fadiga da Maria Caninana e coloque-a em foco imediatamente.'), {'img': I['heart']}),
        ], page=13, folder=FT[1], sort=100))

    out.append(adversary(
        'homem-do-saco', 'Homem do Saco', 1, 'skulk', 15, 7, 12, 6, 3,
        'Um velho maltrapilho com membros alongados, roupas rasgadas e que carrega um saco enorme nas suas costas.',
        'Comer Fígado, Sequestrar, Fugir', ('Saco de Carne', 'mp', 1, '1d8+4', 'mag'), [('Esconder-se', 5), ('Fugir', 2)],
        P('O Homem do Saco é a personificação do desaparecimento, da culpa e da punição à desobediência. Ele tem a aparência de um velho curvado de mãos e braços desproporcionais, carregando um grande saco encardido de onde emana um calor febril e abafado. Dizem que deixar um pão amanhecido na janela ao pôr do sol desvia seus passos. O cheiro de poeira mofada e o som de pano raspando no chão anunciam sua aproximação. Se esse ruído parar na sua porta, pode ser tarde demais para pedir perdão.'),
        [
            ('A Noite é uma Criança', 'passive', P('Enquanto o Homem do Saco estiver no escuro, todos os seus ataques têm <strong>vantagem</strong>.'), {'img': I['dark']}),
            ('Presença Assustadora', 'passive', P('Um personagem que tente sair do alcance Corpo a Corpo do Homem do Saco deve <strong>marcar um Ponto de Fadiga</strong>.'),
             {'img': I['fear'], 'actions': [A.damage('Marcar Fadiga', resources={'stress': 1}, rng='cac')]}),
            ('Hora da Janta', 'action', P('<strong>Marque um Ponto de Fadiga</strong> para pegar e comer um pedaço de carne do saco e recuperar <strong>1 Ponto de Vida</strong>.'),
             {'img': I['eat'], 'actions': [A.heal('Comer (recuperar 1 PV)', 'hitPoints', 1, stress=1)]}),
            ('Pra dentro do Saco', 'action', P('<strong>Gaste um Ponto de Medo</strong> para que o Homem do Saco tente prender um alvo Corpo a Corpo dentro do saco. O alvo deve ter sucesso em um <strong>Teste de Reação de Agilidade</strong>. Em caso de falha, o personagem fica temporariamente <em>Imobilizado</em>. Quando um alvo Imobilizado por esta habilidade age, ele sofre <strong>1d10+5</strong> de dano mágico adicional se ainda estiver Imobilizado no fim de sua ação.'),
             {'img': I['sack'], 'effects': [imobilizado('Preso dentro do saco: sofre 1d10+5 de dano mágico ao fim de cada ação enquanto estiver preso.')],
              'actions': [A.save('Ensacar', 'agility', fear=1, rng='cac', effects=['Imobilizado'], amount=1),
                          A.damage('Dano dentro do Saco', '1d10+5', 'mag')]}),
        ], page=13, folder=FT[1], sort=200))

    out.append(adversary(
        'mapinguari', 'Mapinguari', 1, 'bruiser', 12, 9, 17, 6, 3,
        'Uma criatura coberta de pelos que se camuflam com a folhagem, com um único olho, garras afiadas e boca ventral vertical.',
        'Caçar, Comer, Imitar, Matar', ('Garras Longas', 'mp', 2, '1d10+2', 'fis'), [('Imitação', 5), ('Protetor da Floresta', 2)],
        P('O Mapinguari é uma criatura diurna e por onde anda deixa um rastro de galhos quebrados, árvores derrubadas e gritos. Ele tem um odor insuportável capaz de ser sentido por quilômetros e pés virados para trás, dificultando o rastreamento. Ele não mata por crueldade: o Mapinguari é o símbolo de proteção da floresta e muitos consideram que é a própria força da natureza se defendendo; ele mata por sua fome insaciável.'),
        [
            ('Pelagem Grossa', 'passive', P('O Mapinguari é <strong>resistente a dano físico</strong>.'), {'img': I['fur']}),
            ('Grito de Caçador', 'action', P('Caso o Mapinguari esteja fora da visão dos personagens, você pode <strong>gastar um Ponto de Medo</strong> para imitar o grito feito por um caçador. Se um personagem responder esse grito, o Mapinguari passa a saber exatamente o local da pessoa que respondeu e começa a persegui-la. Em um momento oportuno, o Mapinguari embosca a criatura.'),
             {'img': I['scream'], 'actions': [A.spend('Gastar Medo', fear=1)]}),
            ('Mordida Ventral', 'action', P('<strong>Marque um Ponto de Fadiga</strong> para rasgar um alvo Corpo a Corpo com uma mordida. Em caso de sucesso, o ataque provoca <strong>2d6+4</strong> de dano físico direto.'),
             {'img': I['eat'], 'actions': [A.attack('Mordida Ventral', '2d6+4', 'fis', rng='cac', stress=1, direct=True)]}),
        ], art='mapinguari', size='large', resist=('physical',), page=14, folder=FT[1], sort=300))

    out.append(adversary(
        'maria-caninana', 'Maria Caninana', 1, 'ranged', 13, 6, 12, 5, 3,
        'Uma cobra verde com pontos pretos, gigante e destrutiva.', 'Destruir, Matar, Odiar',
        ('Cuspe Venenoso', 'd', 2, '1d8+3', 'mag'), [('Puro Ódio', 3)],
        P('Maria Caninana é a personificação do naufrágio violento e do apetite das correntes fluviais, o oposto de seu irmão Cobra Norato. Nascida de ventre humano, possui a anatomia de uma serpente gigante e escura, grande o bastante para estilhaçar cascos de madeira dos barcos que cruzarem seu caminho. Dizem que espalhar cinzas de fogueira no convés disfarça o cheiro humano, mas a forte correnteza costuma lavar a oferenda antes de garantir qualquer proteção. O cheiro súbito de lodo podre e o silêncio dos sapos denunciam sua aproximação, sinais quase sempre confundidos com a vazante natural do rio.'),
        [
            ('Ódio de Irmã', 'passive', P(f'Enquanto a Maria Caninana estiver em alcance Próximo do {link("cobra-norato", "Cobra Norato")}, ela recebe um bônus de dano de <strong>1d6</strong> em todos os seus ataques.'), {'img': I['rage']}),
            ('Constrição', 'action', P('<strong>Marque um Ponto de Fadiga</strong> para tentar constringir um alvo Muito Próximo. O alvo deve ter sucesso em um <strong>Teste de Reação de Agilidade</strong>. Em caso de falha, ele sofre <strong>2d4+3</strong> de dano físico e fica <em>Imobilizado</em>. A criatura Imobilizada se move com a Maria Caninana.'),
             {'img': I['snake'], 'effects': [imobilizado('Enrolado pela Maria Caninana, move-se junto com ela.')],
              'actions': [A.save('Constringir', 'agility', '2d4+3', 'fis', rng='mp', stress=1, effects=['Imobilizado'], amount=1)]}),
            ('Chuva Venenosa', 'action', P('<strong>Gaste um Ponto de Medo</strong> para cuspir veneno em uma área à sua frente. Faça um ataque contra todos os alvos em alcance Próximo. Se acertar, os alvos sofrem <strong>1d12+2</strong> de dano mágico.'),
             {'img': I['poison'], 'actions': [A.attack('Chuva Venenosa', '1d12+2', 'mag', rng='p', fear=1, amount=None)]}),
            ('Meu Ódio é Maior', 'reaction', P(f'Caso Maria Caninana presencie a morte de {link("cobra-norato", "Cobra Norato")}, ela se enfurece e recebe um bônus de <strong>+5 de dano</strong> em todos os seus ataques.'),
             {'img': I['rage'], 'effects': [E('Meu Ódio é Maior', '<p>+5 de dano em todos os ataques.</p>', I['rage'], changes=[{'key': 'system.bonuses.damage.bonus', 'type': 'add', 'value': 5, 'priority': None, 'phase': 'initial'}])],
              'actions': [A.spend('Enfurecer', effects=['Meu Ódio é Maior'], target='self')]}),
        ], page=15, folder=FT[1], sort=400))

    out.append(adversary(
        'mula-sem-cabeca', 'Mula Sem Cabeça', 1, 'solo', 15, 9, 15, 8, 4,
        'Uma mula sem cabeça; no local da cabeça há somente chamas.', 'Castigar, Destruir, Queimar',
        ('Coice Flamejante', 'mp', 3, '1d12+4', 'mag'), [('Incendiar', 3)],
        P('A Mula sem Cabeça é a encarnação do amor da maldição divina. Durante o dia, uma mulher que se entregou a um amor proibido; durante a noite, uma mula amaldiçoada que corre levando destruição por onde passa. Seu corpo de mula emana um calor infernal, com chamas vivas e azuis borbulhando do pescoço amputado, enquanto uma pesada corrente de ferro em brasa se arrasta pelo chão. Dizem que é possível conter sua fúria arrancando a corrente, mas o metal incandescente derreteu os dedos dos que tentaram. O som de correntes arrastando freneticamente e o cheiro de brasa e fumaça anunciam sua presença, sinais fáceis de identificar, mas quando o calor sufocante pode ser sentido e os relinchos agonizantes ouvidos, não há mais para onde correr.'),
        [
            ('Casco Flamejante', 'passive', P('Enquanto a Mula Sem Cabeça estiver em uma <em>Zona de Chamas</em>, personagens que sofrerem dano devem <strong>marcar 1 Ponto de Armadura</strong> sem receber seus benefícios.'), {'img': I['fire']}),
            ('Inclemente (2)', 'passive', P('A Mula Sem Cabeça pode ser posta em foco até <strong>2 vezes</strong> por turno do mestre. Gaste Medo normalmente para colocá-la em foco.'),
             {'img': I['relentless'], 'actions': [A.spend('Foco: Inclemente', fear=1, actionType='passive')]}),
            ('Absorver Chamas', 'action', P('Enquanto a Mula Sem Cabeça estiver em uma Zona de Chamas, <strong>marque um Ponto de Fadiga</strong> para absorver todas as chamas na área, encerrando a Zona de Chamas e curando <strong>2 PV</strong>.'),
             {'img': I['fire'], 'actions': [A.heal('Absorver (curar 2 PV)', 'hitPoints', 2, stress=1)]}),
            ('Coice Descontrolado', 'action', P('<strong>Marque um Ponto de Fadiga</strong> para fazer um ataque padrão contra todos os alvos Muito Próximos.'),
             {'img': I['kick'], 'actions': [A.attack('Coice Descontrolado', '1d12+4', 'mag', rng='mp', stress=1, amount=None)]}),
            ('Zona de Chamas', 'action', P('<strong>Gaste 2 Pontos de Medo</strong> para incendiar a área em alcance Próximo. Alvos nessa área devem ter sucesso em um <strong>Teste de Reação de Força</strong>. Em caso de falha, sofrem <strong>2d8+6</strong> de dano mágico e ficam <em>Em Chamas</em> até sair da área. Em caso de sucesso, sofrem metade do dano. Quando um personagem Em Chamas age, ele sofre <strong>2d6</strong> de dano mágico adicional se ainda estiver Em Chamas no fim da ação dele.'),
             {'img': I['firebreath'], 'effects': [E('Em Chamas', '<p><em>Em Chamas</em>: ao fim de cada ação, se ainda estiver na Zona de Chamas, sofre 2d6 de dano mágico.</p>', I['fire'])],
              'actions': [A.save('Zona de Chamas', 'strength', '2d8+6', 'mag', rng='p', fear=2, half=True, effects=['Em Chamas']),
                          A.damage('Dano: Em Chamas', '2d6', 'mag')]}),
            ('Impulso', 'reaction', P('Quando a Mula Sem Cabeça acertar um ataque contra um personagem, receba <strong>um Ponto de Medo</strong>.'),
             {'img': I['momentum'], 'actions': [A.gain_fear()]}),
        ], page=15, folder=FT[1], sort=500))

    out.append(adversary(
        'noiva-do-candelabro', 'Noiva do Candelabro', 1, 'standard', 12, 5, 11, 5, 2,
        'Uma mulher vestida de noiva, com cabelos negros e portando uma faca envenenada.', 'Amar, Envenenar, Vingança',
        ('Faca Venenosa', 'cac', 1, '1d6+5', 'fis'), [('A morte é algo que se saboreia', 2)],
        P('Uma noiva buscando aplacar a sua dor e se vingar depois de perder o amado logo antes do casamento. O vestido de cetim amarelado impregnado de mofo, os dedos com unhas quebradas e olhos fundos cobertos por um véu de renda corroída pelo tempo contrastam com a faca envenenada e o candelabro gasto que carrega. Velhas crenças sugerem que sussurrar o nome do noivo falecido acalma seu pranto, mas errar o nome ou até a pronúncia correta desperta ainda mais sua fúria. Os que dizem terem encontrado a noiva lembram de um cheiro adocicado de jasmim murcho e o som da seda balançando ao vento.'),
        [
            ('Envenenar-se', 'action', P('<strong>Marque um Ponto de Fadiga</strong> para que a Noiva do Candelabro comece a produzir mais veneno do que seu corpo é capaz de suportar. Até o fim da cena, seu ataque padrão passa a causar <strong>1d8+7</strong> de dano físico, mas você deve <strong>marcar um Ponto de Vida</strong> sempre que ela causar dano.'),
             {'img': I['poison'], 'actions': [A.spend('Envenenar-se', stress=1, target='self'), A.attack('Faca Transbordando Veneno', '1d8+7', 'fis', rng='cac')]}),
            ('A Morte não é o Fim', 'reaction', P('Ao marcar seu último Ponto de Vida, a Noiva do Candelabro explode em veneno ácido em alcance Muito Próximo. Personagens no alcance devem ter sucesso em um <strong>Teste de Reação de Agilidade</strong>. Em caso de falha, sofrem <strong>1d8</strong> de dano físico e devem marcar uma Armadura sem receber os benefícios. Se não for possível marcar um Ponto de Armadura, o alvo deve marcar um Ponto de Vida adicional.'),
             {'img': I['acid'], 'actions': [A.save('Explosão Ácida', 'agility', '1d8', 'fis', rng='mp')]}),
        ], page=16, folder=FT[1], sort=600))

    # ------------------------------------------------------------------ 2º PATAMAR
    out.append(adversary(
        'bernuncinha', 'Bernuncinha', 2, 'bruiser', 14, 15, 28, 7, 5,
        'Uma filhote de bernunça, uma criatura com cabeça de dragão, parte da frente do corpo de leão e traseiro de hipopótamo. Come tudo o que lhe dão e fica cada vez mais comprida.',
        'Dançar, Engolir, Morder', ('Mordida', 'cac', 2, '2d10+4', 'fis'), [('Alimentar-se', 2)],
        P('Essa criatura tem uma fome insaciável e come tudo que vê pela frente. Suas comidas favoritas são crianças desobedientes, pão e bolacha. Ela adora dançar músicas de sanfona, cavaco e pandeiro enquanto faz a digestão. Estão sempre próximas de sua mãe e vivem próximas a rios e lagoas, sendo uma criatura semiaquática que adora se banhar em águas lamacentas.'),
        [
            ('Lentidão', 'passive', P('Enquanto a Bernuncinha estiver engolindo alguém, esta habilidade é ativada. Se a Bernuncinha for posta em foco, mas não tiver nenhum marcador em sua ficha, ela é incapaz de agir. Coloque um marcador na ficha e descreva o que ela está se preparando para fazer. Quando puser a Bernuncinha em foco e ela tiver um marcador na ficha, remova o marcador para que ela possa agir.'), {'img': I['slow']}),
            ('Sopro de Chamas', 'action', P('<strong>Gaste 2 Pontos de Medo</strong> para liberar chamas em alvos Muito Próximos na frente da Bernuncinha. Todos os alvos devem fazer um <strong>Teste de Reação de Agilidade</strong>. Quem falhar sofre <strong>3d6+2</strong> de dano mágico. Quem passar deve marcar um Ponto de Fadiga ou sofrer metade do dano.'),
             {'img': I['firebreath'], 'actions': [A.save('Sopro de Chamas', 'agility', '3d6+2', 'mag', rng='mp', fear=2, half=True)]}),
            ('Sempre Cabe Mais', 'reaction', P('<strong>Contagem Regressiva (Ciclo 1d4).</strong> Quando a Bernuncinha acerta um ataque padrão, você pode <strong>marcar um Ponto de Fadiga</strong> para tentar engolir o alvo. O alvo deve fazer um <strong>Teste de Reação de Força ou Agilidade</strong> para tentar escapar; se falhar, ele é engolido, ficando <em>Imobilizado</em> e com desvantagem em Testes de Ação. Ative a contagem regressiva e diminua sempre que um personagem rolar com Medo. Quando a contagem chegar a zero, o personagem marca 1 PV e 1 PF e a Bernuncinha aumenta em 1 seus limiares de dano. Ela só pode ter uma criatura engolida por vez. Se o personagem morrer enquanto estiver dentro dela, ela pode engolir um novo inimigo.'),
             {'img': I['swallow'], 'effects': [imobilizado('Engolido: desvantagem em Testes de Ação.')],
              'actions': [A.save('Engolir', 'agility', stress=1, rng='cac', effects=['Imobilizado'], amount=1),
                          A.countdown('Sempre Cabe Mais (Bernuncinha)', '1d4', I['swallow'], looping='looping'),
                          A.damage('Digestão (1 PV e 1 PF)', resources={'hitPoints': 1, 'stress': 1})]}),
        ], page=16, folder=FT[2], sort=100))

    out.append(adversary(
        'caipora', 'Caipora', 2, 'support', 15, 10, 17, 4, 6,
        'Uma humanoide que fica mudando de tamanho, coberta com pelos vermelho-sangue.', 'Defender a Natureza, Punir Transgressores',
        ('Cajado de Guaco', 'cac', 1, '2d8+5', 'mag'), [('Protetora dos Animais', 3)],
        P('Parece-se com uma criança pequena, de pele escura como brasa apagada e cabelos vermelhos sempre encharcados; monta um porco-do-mato e carrega uma vara de cipó que usa para levantar de novo os animais já abatidos. Seu assobio vem sempre do lado oposto de onde ela está, tornando difícil rastreá-la.'),
        [
            ('Mudança de Forma', 'passive', P('Uma vez por turno do mestre, a Caipora pode alternar entre as formas abaixo e receber suas habilidades: <strong>Forma Diminuta</strong>, <strong>Forma Mediana</strong> e <strong>Forma Gigante</strong>.'), {'img': I['shape']}),
            ('Forma Diminuta — Velocidade Ganha de Força', 'passive', P('As criaturas têm <strong>desvantagem</strong> para atacar a Caipora, e seu ataque padrão causa <strong>2d4+4</strong> de dano, em vez do valor original.'),
             {'img': I['shape'], 'actions': [A.attack('Cajado (Forma Diminuta)', '2d4+4', 'mag', rng='cac')]}),
            ('Forma Diminuta — Vigor Natural', 'action', P('<strong>Marque um Ponto de Fadiga</strong> para recuperar <strong>1 PV</strong> de qualquer criatura Próxima.'),
             {'img': I['heal'], 'actions': [A.heal('Vigor Natural', 'hitPoints', 1, target='any', stress=1, rng='p')]}),
            ('Forma Mediana — Poder da Natureza', 'action', P('<strong>Marque um Ponto de Fadiga</strong> para utilizar o poder da natureza do ambiente ao seu redor.') +
             '<ul><li><strong>Ambiente aquático:</strong> empurre as criaturas dentro de um alcance Muito Próximo para até um alcance Distante caso falhem em um Teste de Reação de Força ou Agilidade.</li>'
             '<li><strong>Ambiente árido:</strong> escolha um ponto dentro do alcance Distante e faça uma área Próxima se tornar areia movediça. Criaturas devem fazer um Teste de Instinto para perceber a área traiçoeira, e qualquer criatura que entre nessa área deverá fazer um Teste de Reação de Agilidade ou ficar <em>Imobilizada</em> pela areia.</li>'
             '<li><strong>Ambiente de mata:</strong> raízes saem de seu cajado em direção a um alvo para prendê-lo. O alvo deverá fazer um Teste de Reação de Agilidade para não ficar <em>Imobilizado</em>. Até que se liberte, a criatura deverá marcar uma Fadiga antes de fazer qualquer ação que não seja tentar se libertar.</li></ul>',
             {'img': I['root'], 'effects': [imobilizado()],
              'actions': [A.save('Aquático: Empurrar', 'strength', rng='mp', stress=1),
                          A.save('Árido / Mata: Prender', 'agility', rng='d', stress=1, effects=['Imobilizado'])]}),
            ('Forma Gigante — Poder Bruto', 'passive', P('Seu ataque padrão passa a causar <strong>2d12+6</strong> de dano mágico.'),
             {'img': I['grow'], 'actions': [A.attack('Cajado (Forma Gigante)', '2d12+6', 'mag', rng='cac')]}),
            ('Forma Gigante — Natureza em Fúria', 'action', P('<strong>Marque 2 Pontos de Fadiga</strong> para invocar uma forte tempestade centrada em você com alcance Muito Distante. Enquanto estiverem na área da tempestade, ataques à distância têm desvantagem e a Dificuldade do ambiente aumenta em 2.'),
             {'img': I['storm'], 'actions': [A.spend('Invocar Tempestade', stress=2)]}),
        ], art='caipora', token='caipora', page=17, folder=FT[2], sort=200))

    out.append(adversary(
        'clone-curupira', 'Clone Ilusório do Curupira', 2, 'minion', 16, 0, 0, 1, 1,
        'Uma cópia ilusória do Curupira, feita de fogo-fátuo e folhas.', 'Confundir, Cercar, Desaparecer',
        None, [],
        P(f'Criado pela habilidade <em>Natureza Ilusória</em> do {link("curupira", "Curupira")}. Os clones agem independentemente do Curupira; gaste Medo normalmente para colocá-los em foco.'),
        [
            ('Assombrar', 'action', P('Use uma ação para forçar um alvo a <strong>marcar um Ponto de Fadiga</strong>.'),
             {'img': I['clone'], 'actions': [A.damage('Forçar Fadiga', resources={'stress': 1}, rng='d')]}),
            ('Desfazer-se', 'reaction', P('Quando destruído, alvos Muito Próximos devem fazer um <strong>Teste de Reação de Instinto ou Presença</strong>. Em caso de falha, marcam <strong>1 PF</strong>.'),
             {'img': I['clone'], 'actions': [A.save('Explosão Ilusória', 'instinct', rng='mp', resources={'stress': 1})]}),
        ], token='curupira', page=17, folder=FT[2], sort=310))

    out.append(adversary(
        'curupira', 'Curupira', 2, 'leader', 16, 12, 23, 6, 6,
        'Um humanoide com pele morena queimada de sol, cabelos de fogo, orelhas pontudas e pés voltados para trás.',
        'Expulsar Invasores, Reunir Grupos', ('Arco de Fogo', 'd', 2, '2d8+4', 'mag'), [('Amigo dos Animais', 2)],
        P('O Curupira é a cobrança que a mata faz de quem tira mais do que precisa. Tem corpo de menino, cabelos de fogo, dentes verdes e pés virados para trás, o que faz com que suas pegadas sempre apontem para onde ele não está. Caçadores velhos amarram nós em cipós, porque dizem que ele precisa desatar cada um antes de seguir, embora suspeitem que o ritual apenas prolongue a agonia da perseguição.'),
        [
            ('Todos por Um', 'passive', P('Quando o Curupira estiver em foco, você também pode pôr em foco um adversário animal de 1º patamar ou um clone que esteja sob o controle dele. <strong>Marque um Ponto de Fadiga</strong> para colocar um animal de 2º patamar no lugar do de 1º.'),
             {'img': I['group'], 'actions': [A.spend('Animal de 2º patamar', stress=1)]}),
            ('Natureza Ilusória', 'action', P(f'<strong>Gaste um Ponto de Medo</strong> para criar até 3 {link("clone-curupira", "clones")} seus. Você pode manter no máximo 3 clones por vez. Os clones podem agir independentemente do Curupira; gaste Medo normalmente para colocá-los em foco. Os clones têm 1 PV, podem usar uma ação para forçar um alvo a marcar um Ponto de Fadiga e, quando destruídos, alvos Muito Próximos devem fazer um Teste de Reação de Instinto ou Presença. Em caso de falha, marcam 1 PF.'),
             {'img': I['clone'], 'actions': [A.summon(uuid('clone-curupira'), 3, 'Criar Clones', fear=1)]}),
            ('Vocalização Primitiva', 'action', P('<strong>Marque um Ponto de Fadiga</strong> para invocar <strong>1d6+1</strong> animais de 1º patamar ou <strong>1d4</strong> animais de 2º patamar da região para auxiliá-lo.'),
             {'img': I['beasts'], 'actions': [A.spend('Chamar Animais', stress=1)]}),
            ('Assobio Aterrorizante', 'action', P('<strong>Gaste um Ponto de Medo</strong> para assobiar e fazer com que todos os personagens em alcance Distante façam um <strong>Teste de Reação de Instinto ou Presença</strong>. Em caso de falha, os personagens devem rolar dois Dados de Medo e ficar com o resultado mais alto. O efeito dura até o Curupira ser derrotado ou até o próximo descanso.'),
             {'img': I['whistle'], 'effects': [E('Assobio Aterrorizante', '<p>Role dois Dados de Medo e fique com o resultado mais alto, até o Curupira ser derrotado ou até o próximo descanso.</p>', I['whistle'], duration='shortRest')],
              'actions': [A.save('Assobiar', 'instinct', rng='d', fear=1, effects=['Assobio Aterrorizante'])]}),
        ], art='curupira', page=17, folder=FT[2], sort=300))

    out.append(adversary(
        'mulher-de-sete-metros', 'Mulher de Sete Metros', 2, 'standard', 12, 7, 19, 4, 3,
        'Uma mulher alta e fantasmagórica que vai aumentando seu tamanho à medida que vão interagindo com ela.', 'Aterrorizar, Vingança',
        ('Dedos Alongados', 'mp', 0, '2d8+1', 'mag'), [('Crescer', 2), ('Perseguir', 2)],
        P('A Mulher de Sete Metros é uma figura alta e esquálida que caminha pelas ruas ao entardecer, e sua sombra se estende pelos telhados muito antes de ela aparecer. Seu vestido branco pende em farrapos, seu pescoço se curva sob os beirais e seus dedos são longos o bastante para bater nas janelas do andar de cima. Ela espia as casas onde crianças permanecem acordadas além da hora de dormir. Os anciãos da Terra da Fartura dizem que a casa com as janelas trancadas e uma vela acesa em cada parapeito é ignorada, e que um terço pendurado na porta desvia o olhar dela. Dizem que quem ousa encará-la sente o ar parar, ouve o ranger de passadas longas sobre as telhas e percebe o cheiro de terra úmida e cera queimada. Alguns juram que quem a chama pelo nome de batismo, como se fosse uma vizinha…'),
        [
            ('Crescimento Ilusório', 'passive', P('A Mulher de Sete Metros aparenta ter o tamanho de uma mulher normal. Ao ser posta em foco pela primeira vez, inicie uma <strong>Contagem Regressiva Decrescente (3)</strong> na ficha dela. Cada ação feita contra ela reduz esse marcador em 1. Sempre que o contador diminuir, sua altura aumenta até chegar a um total de 7 metros. Ela não marca PV até o contador zerar.'),
             {'img': I['grow'], 'actions': [A.countdown('Crescimento Ilusório', 3, I['grow'], looping='decreasing')]}),
            ('Vertigem', 'passive', P('Ao terminar o contador, personagens em alcance Muito Próximo devem fazer um <strong>Teste de Reação de Instinto</strong> ou ficarem <em>Vulneráveis</em> graças à vertigem.'),
             {'img': I['vertigo'], 'effects': [vulneravel('Vertigem diante da Mulher de Sete Metros.')],
              'actions': [A.save('Vertigem', 'instinct', rng='mp', effects=['Vulnerável'])]}),
            ('Grito Silencioso', 'action', P('<strong>Marque um Ponto de Fadiga</strong> para esmorecer todas as fontes de luz não mágicas em alcance Distante. Testes relacionados à visão têm desvantagem nessa área.'),
             {'img': I['candle'], 'actions': [A.spend('Apagar as Luzes', stress=1)]}),
        ], page=18, folder=FT[2], sort=400))

    saci_lore = P('O Saci-Pererê adora aprontar. É sempre bom tomar cuidado com ventos fortes, pois pode ser que ele esteja por perto. Ele cachimba enquanto prepara seus planos. É normal pendurarem peneiras nas varandas para prender um Saci que venha em forma de redemoinho. Os antigos dizem que o único jeito de mantê-lo preso é colocá-lo em uma garrafa com uma cruz desenhada na rolha. Além disso, dizem que ele tem fixação pelo seu gorro.')
    repulso = ('Repulso', 'passive', P('Quando o Saci-Pererê atingir um personagem, o alvo <strong>perde uma Esperança</strong>.'),
               {'img': I['hope'], 'actions': [A.damage('Perder Esperança', resources={'hope': 1})]})
    out.append(adversary(
        'saci-perere', 'Saci-Pererê', 2, 'skulk', 13, 9, 16, 6, 4,
        'Um humanoide de pele negra com uma perna só e uma cabeça de suíno. Muito sagaz e arteiro.', 'Atrapalhar, Brincar, Zoar',
        ('Estilingue', 'mp', 2, '2d6+5', 'fis'), [('Azedar o Doce', 3), ('Desaparecer', 2)], saci_lore,
        [
            ('Gorro', 'passive', P('O gorro do Saci é a fonte de seus poderes. Caso ele perca o gorro, sua Dificuldade diminui em 2; ao marcar qualquer quantidade de Pontos de Vida, ele deve marcar um Ponto de Fadiga; e ele perde a habilidade Redemoinho.'),
             {'img': I['hat'], 'effects': [E('Sem o Gorro', '<p>Dificuldade −2. Ao marcar PV, marque também 1 PF. Perde Redemoinho.</p>', I['hat'], changes=[{'key': 'system.difficulty', 'type': 'add', 'value': -2, 'priority': None, 'phase': 'initial'}])],
              'actions': [A.spend('Perdeu o Gorro', effects=['Sem o Gorro'], target='self')]}),
            repulso,
            ('Invisibilidade', 'action', P('<strong>Marque um Ponto de Fadiga</strong> para ficar <em>Invisível</em>. Enquanto estiver Invisível, sua Dificuldade aumenta em 2 para ser detectado através da visão, ele só pode ser visto por meios mágicos e testes de ataque contra ele são feitos com desvantagem. Coloque um número de marcadores igual a <strong>1d4+2</strong> na ficha dele. Sempre que fizer alguma ação, gaste um marcador. Após o término da ação que consumiu o último marcador, o efeito termina.'),
             {'img': I['invis'], 'effects': [E('Invisível', '<p>Só pode ser visto por meios mágicos; ataques contra ele têm desvantagem. Dura 1d4+2 ações.</p>', I['invis'], statuses=['hidden'])],
              'actions': [A.spend('Ficar Invisível', stress=1, effects=['Invisível'], target='self'),
                          A.countdown('Invisibilidade do Saci', '1d4+2', I['invis'], looping='decreasing')]}),
            ('Redemoinho', 'action', P('<strong>Gaste um Ponto de Medo</strong> para começar a girar em um Redemoinho. Quando entrar em Redemoinho, alvos em alcance Muito Próximo devem ter sucesso em um <strong>Teste de Reação de Força ou Agilidade</strong> ou sofrer <strong>2d8+3</strong> de dano mágico e serem empurrados para alcance Distante. Personagens que tentarem se aproximar do Saci devem ter sucesso em um Teste de Agilidade; caso falhem, não conseguem se aproximar. <strong>Marque um Ponto de Fadiga</strong> em cada turno do mestre para continuar em Redemoinho; caso contrário, a condição termina no início do próximo turno do mestre.'),
             {'img': I['tornado'], 'actions': [A.save('Redemoinho', 'agility', '2d8+3', 'mag', rng='mp', fear=1),
                                                A.spend('Manter Redemoinho', stress=1)]}),
            ('Espírito de Porco do Mato', 'evolution', P(f'Quando o Saci marcar o seu último PV, ele se funde com o seu gorro e seu corpo aumenta em tamanho e massa, ganhando a feição de um porco-do-mato ameaçador. Ele limpa todos os PV e PF marcados, entra em frenesi e é posto em foco imediatamente. Substitua-o por {link("espirito-porco-do-mato", "Saci-Pererê — Espírito de Porco do Mato")}.'),
             {'img': I['boar'], 'actions': [A.transform(uuid('espirito-porco-do-mato'), 'Evoluir')]}),
        ], art='saci', page=18, folder=FT[2], sort=500))

    out.append(adversary(
        'espirito-porco-do-mato', 'Saci-Pererê — Espírito de Porco do Mato', 2, 'skulk', 13, 9, 16, 6, 4,
        'Fundido ao próprio gorro, o Saci cresce em tamanho e massa e ganha a feição de um porco-do-mato ameaçador, em frenesi.',
        'Atrapalhar, Brincar, Zoar — agora em frenesi', ('Presas Afiadas', 'cac', 3, '2d10+6', 'fis'), [('Azedar o Doce', 3), ('Desaparecer', 2)], saci_lore,
        [
            repulso,
            ('Furacão', 'action', P('<strong>Uma vez por cena, gaste um Ponto de Medo</strong> para criar um furacão denso de poeira, galhos e folhas. Todos em alcance Distante devem passar em um <strong>Teste de Reação de Agilidade</strong>. Na falha, sofrem <strong>2d20+7</strong> de dano físico. Até o Saci ser derrotado, a área ao redor dele se torna difícil por causa da ventania: ataques à distância maior que Muito Próximo contra o Saci têm desvantagem, testes de conjuração devem rolar dois Dados de Medo e ficar com o resultado mais alto, e é preciso um Teste de Agilidade para se movimentar qualquer distância maior que Muito Próximo na área.'),
             {'img': I['tornado'], 'actions': [A.save('Furacão', 'agility', '2d20+7', 'fis', rng='d', fear=1, uses=1, recovery='scene')]}),
            ('Passo Umbral', 'action', P('<strong>Gaste um Ponto de Medo</strong> para o Saci se teletransportar para as costas de qualquer alvo em alcance Distante e realizar um ataque corpo a corpo imediatamente. <strong>Marque um Ponto de Fadiga</strong> para retornar ao ponto inicial ao final do ataque.'),
             {'img': I['portal'], 'actions': [A.attack('Passo Umbral', '2d10+6', 'fis', rng='cac', fear=1), A.spend('Retornar', stress=1)]}),
            ('Sorvedouro Abissal', 'reaction', P('Quando um ataque do Saci atinge um personagem, o alvo <strong>perde uma Esperança</strong> e o mestre <strong>ganha um Medo</strong>. Se o alvo já não tiver Esperança para perder, ele deve marcar um Ponto de Fadiga.'),
             {'img': I['abyss'], 'actions': [A.damage('Perder Esperança', resources={'hope': 1}), A.gain_fear()]}),
        ], art='saci', token='espirito-porco-do-mato', page=18, folder=FT[2], sort=510))

    # ------------------------------------------------------------------ 3º PATAMAR
    out.append(adversary(
        'bernunca', 'Bernunça', 3, 'bruiser', 17, 23, 39, 9, 6,
        'Uma criatura com cabeça de dragão, parte da frente do corpo de leão e parte de trás de hipopótamo. Come tudo o que lhe dão para comer e fica cada vez mais comprida.',
        'Dançar, Engolir, Morder, Nadar, Proteger Filhas', ('Mordida', 'cac', 2, '3d10+4', 'fis'), [('Alimentar-se', 3), ('Proteger sua Prole', 2)],
        P('Essa criatura tem uma fome insaciável e come tudo que vê pela frente. Suas comidas favoritas são crianças desobedientes, pão e bolacha. Ela adora dançar músicas de sanfona, cavaco e pandeiro enquanto faz a digestão. É uma mãe superprotetora e vive próxima a rios e lagoas, sendo uma criatura semiaquática que adora se banhar em águas lamacentas.'),
        [
            ('Mãe Protetora', 'passive', P(f'Se a Bernunça estiver na presença de uma ou mais {link("bernuncinha", "Bernuncinhas")}, ela age instintivamente para protegê-las. Sempre que alguém atacar uma Bernuncinha e rolar com Medo, a Bernunça tem <strong>vantagem</strong> para agir contra aquele personagem na próxima vez que for colocada em foco.'), {'img': I['mother']}),
            ('Sopro de Chamas', 'action', P('<strong>Gaste 2 Pontos de Medo</strong> para liberar chamas em alvos Muito Próximos na frente da Bernunça. Todos os alvos devem fazer um <strong>Teste de Reação de Agilidade</strong>. Quem falhar sofre <strong>4d6+4</strong> de dano mágico. Quem passar deve marcar um Ponto de Fadiga ou sofrer metade do dano.'),
             {'img': I['firebreath'], 'actions': [A.save('Sopro de Chamas', 'agility', '4d6+4', 'mag', rng='mp', fear=2, half=True)]}),
            ('Sempre Cabe Mais', 'reaction', P('<strong>Contagem (Ciclo 1d3).</strong> Quando a Bernunça acerta um ataque de mordida, você pode <strong>marcar um Ponto de Fadiga</strong> para tentar engolir o alvo. O alvo faz um <strong>Teste de Reação de Força ou Agilidade</strong> para tentar escapar; se falhar, ele é engolido, ficando <em>Imobilizado</em> e com desvantagem em Testes de Ação. Ative a contagem regressiva e diminua sempre que um personagem rolar com Medo. Quando a contagem chegar a zero, o personagem marca 1 PV e 1 PF e a Bernunça aumenta em 1 seus limiares de dano. A Bernunça pode engolir várias criaturas; use o mesmo ciclo para todas.'),
             {'img': I['swallow'], 'effects': [imobilizado('Engolido: desvantagem em Testes de Ação.')],
              'actions': [A.save('Engolir', 'agility', stress=1, rng='cac', effects=['Imobilizado'], amount=1),
                          A.countdown('Sempre Cabe Mais (Bernunça)', '1d3', I['swallow'], looping='looping'),
                          A.damage('Digestão (1 PV e 1 PF)', resources={'hitPoints': 1, 'stress': 1})]}),
            ('Dando à Luz', 'reaction', P(f'Quando um inimigo morre engolido pela Bernunça, você pode <strong>gastar um Ponto de Medo</strong> para que ela dê à luz uma {link("bernuncinha", "Bernuncinha")}.'),
             {'img': I['birth'], 'actions': [A.summon(uuid('bernuncinha'), 1, 'Dar à Luz', fear=1)]}),
        ], size='large', page=19, folder=FT[3], sort=100))

    boi_lore = P('Mães costumam cantar cantigas de ninar sobre uma criatura que vem buscar as crianças que se recusam a dormir: o Boi da Cara Preta. Seu corpo é de boi magro com a pelagem curta, mas com a cabeça inteiramente negra, com chifres curvados para dentro como ganchos. Seu focinho fareja o choro das crianças pelas frestas das janelas. Dizem que ele não entra onde a criança já dorme; por isso as mães cantam até o sono chegar. O problema é que a cantiga que embala o sono é a mesma que o chama.')
    out.append(adversary(
        'boi-da-cara-preta', 'Boi da Cara Preta', 3, 'horde', 14, 25, 38, 6, 4,
        'Uma manada de bois com a cabeça da cor do céu sem estrelas.', 'Chifrar, Pisotear, Proteger',
        ('Chifres', 'cac', 3, '3d8+4', 'fis'), [('Correr em Bando', 2), ('Pisotear', 3)], boi_lore,
        [
            ('Horda (2d6+2)', 'passive', P('Quando a manada tiver marcado metade dos seus PV ou mais, seu ataque padrão causa <strong>2d6+2</strong> de dano físico, em vez do valor original.'), {'img': I['horde']}),
            ('Fantasmagórico', 'passive', P('A manada do Boi da Cara Preta pode <strong>marcar um Ponto de Fadiga</strong> para atravessar objetos sólidos.'),
             {'img': I['ghost'], 'actions': [A.spend('Atravessar', stress=1)]}),
            ('Pisotear', 'action', P('<strong>Marque um Ponto de Fadiga</strong> para pisotear inimigos na frente da manada, causando <strong>3d12+6</strong> de dano físico. Se os personagens tiverem sucesso em um <strong>Teste de Reação de Agilidade</strong>, eles sofrem metade do dano.'),
             {'img': I['trample'], 'actions': [A.save('Pisotear', 'agility', '3d12+6', 'fis', rng='mp', stress=1, half=True)]}),
            ('O Despertar do Pesadelo', 'evolution', P(f'Quando a manada marcar o último PV, as sombras da manada derrotada se juntam e formam um enorme humanoide com aparência de minotauro. Recupere todos os PV e PF e substitua a manada por {link("despertar-do-pesadelo", "Boi da Cara Preta — O Despertar do Pesadelo")}.'),
             {'img': I['axe'], 'actions': [A.transform(uuid('despertar-do-pesadelo'), 'Despertar')]}),
        ], art='boi-da-cara-preta', horde=(3, '2d6+2'), size='large', page=19, folder=FT[3], sort=200))

    out.append(adversary(
        'despertar-do-pesadelo', 'Boi da Cara Preta — O Despertar do Pesadelo', 3, 'bruiser', 16, 25, 38, 6, 4,
        'As sombras da manada derrotada se juntam em um enorme humanoide com aparência de minotauro.', 'Chifrar, Pisotear, Proteger',
        ('Machado do Suplício', 'mp', 3, '3d12+3', 'fis'), [('Correr em Bando', 2), ('Pisotear', 3)], boi_lore,
        [
            ('Lentidão', 'passive', P('Se o Boi da Cara Preta for posto em foco, mas não tiver nenhum marcador em sua ficha, ele é incapaz de agir. Coloque um marcador na ficha e descreva o que ele está se preparando para fazer. Quando puser este adversário em foco e ele tiver um marcador na ficha, remova o marcador para que ele possa agir.'), {'img': I['slow']}),
            ('Brandindo a Morte', 'action', P('<strong>Marque um Ponto de Fadiga</strong> para atacar todos dentro do alcance Muito Próximo, sugando seu poder vital e causando <strong>3d10+5</strong> de dano mágico. Recupere uma quantidade de PV igual à metade dos PV marcados pelos personagens.'),
             {'img': I['axe'], 'actions': [A.attack('Brandindo a Morte', '3d10+5', 'mag', rng='mp', stress=1, amount=None), A.heal('Sugar Vida', 'hitPoints', 1)]}),
            ('Olhar do Pavor', 'action', P('<strong>Gaste um Ponto de Medo</strong> para trazer à vida os maiores medos do personagem. O personagem deve fazer um <strong>Teste de Reação de Presença</strong> ou terá desvantagem em testes de ação contra o Boi da Cara Preta até que ele seja derrotado ou até um descanso curto.'),
             {'img': I['eye'], 'effects': [E('Olhar do Pavor', '<p>Desvantagem em testes de ação contra o Boi da Cara Preta até ele ser derrotado ou até um descanso curto.</p>', I['eye'], duration='shortRest')],
              'actions': [A.save('Olhar do Pavor', 'presence', rng='d', fear=1, effects=['Olhar do Pavor'], amount=1)]}),
        ], art='boi-da-cara-preta', token='despertar-do-pesadelo', size='large', page=19, folder=FT[3], sort=210))

    out.append(adversary(
        'cabra-cabriola', 'Cabra Cabriola', 3, 'skulk', 16, 18, 34, 8, 4,
        'Uma cabra antropomórfica com aspecto monstruoso, faminta por crianças.', 'Comer Crianças, Espreitar, Matar',
        ('Voz Desconcertante', 'p', 4, '3d8+5', 'mag'), [('Raptar', 2), ('Transformar em Medo', 2)],
        P('A Cabra Cabriola é a personificação do medo. Uma figura humanoide esguia, com membros alongados e uma fome insaciável por crianças. Ela é capaz de imitar vozes perfeitamente, mesmo só tendo as escutado uma só vez, de personificar o maior medo daquele à sua frente e de se regenerar a partir do medo.'),
        [
            ('Eu Sou o Seu Maior Pesadelo', 'action', P('<strong>Marque um Ponto de Fadiga</strong>, escolha um personagem em alcance Distante e peça para o jogador descrever o maior medo do alvo. Ao terminar de descrever, a Cabra Cabriola muda de forma para personificar esse medo e deixa o alvo <em>Amedrontado</em>. Enquanto estiver Amedrontado, o alvo tem desvantagem em Testes de Ação contra a Cabra Cabriola e não pode se aproximar dela voluntariamente. A condição se encerra com um sucesso em um Teste de Instinto.'),
             {'img': I['goat'], 'effects': [E('Amedrontado', '<p>Desvantagem em Testes de Ação contra a Cabra Cabriola; não pode se aproximar dela voluntariamente. Encerra com sucesso em um Teste de Instinto.</p>', I['fear'])],
              'actions': [A.spend('Personificar o Medo', stress=1, effects=['Amedrontado'], rng='d', amount=1)]}),
            ('Vozes Dissonantes', 'action', P('<strong>Gaste um Ponto de Medo</strong> para proferir inúmeras vozes ao mesmo tempo. Alvos Próximos que possam escutar devem ter sucesso em um <strong>Teste de Reação de Presença</strong>. Em caso de falha, os alvos sofrem <strong>2d8+4</strong> de dano físico direto. Em caso de sucesso, eles sofrem metade do dano.'),
             {'img': I['voices'], 'actions': [A.save('Vozes Dissonantes', 'presence', '2d8+4', 'fis', rng='p', fear=1, half=True, direct=True)]}),
            ('Alimentar-se do Medo', 'reaction', P('Sempre que a Cabra Cabriola usar sua habilidade <em>Eu Sou o Seu Maior Pesadelo</em>, ela pode se alimentar desse medo, recuperando <strong>um Ponto de Vida</strong>. Caso faça isso, a condição Amedrontado do alvo se encerra e ela volta ao normal.'),
             {'img': I['heal'], 'actions': [A.heal('Alimentar-se (1 PV)', 'hitPoints', 1, actionType='reaction')]}),
        ], page=20, folder=FT[3], sort=300))

    out.append(adversary(
        'pesadelo-da-cuca', 'Pesadelo da Cuca', 3, 'minion', 14, 0, 0, 1, 1,
        'Alguém posto para dormir e controlado pela Cuca.', 'Andar, Obedecer',
        ('Pancada', 'cac', 1, '5', 'fis'), [],
        P('Estas são pessoas sonâmbulas controladas pela Cuca. Em geral, antes de se alimentar delas, a Cuca as usa para trabalhos braçais, como escudo e para lutar por ela se necessário. Dizem que a maioria são pessoas com insônia e que uma outra forma de acordá-las é fazer com que elas se deparem com seu maior medo.'),
        [
            ('Acordando', 'passive', P('Ao sofrer qualquer dano, o Pesadelo da Cuca é acordado e a pessoa que estava sendo controlada pela Cuca volta a si. Ao voltar a si, ela perde um PV e marca um Ponto de Fadiga.'), {'img': I['wake']}),
            ('Ataque em Grupo', 'action', P('<strong>Gaste um Ponto de Medo</strong> para escolher um alvo e pôr em foco todos os Pesadelos da Cuca próximos dele. Esses lacaios ficam em alcance Corpo a Corpo do alvo e fazem um teste de ataque compartilhado. Se acertarem, cada um causa <strong>5</strong> pontos de dano físico. Os danos são somados.'),
             {'img': I['group'], 'actions': [A.attack('Ataque em Grupo', '5', 'fis', rng='cac', fear=1)]}),
        ], token='pesadelo-da-cuca', page=21, folder=FT[3], sort=410))

    out.append(adversary(
        'cuca', 'Cuca', 3, 'leader', 18, 18, 33, 7, 7,
        'Uma bruxa com corpo de jacaré e cabelos loiros. Dorme uma vez ao ano e captura o sono dos desavisados. Ela se alimenta de pessoas que não dormem.',
        'Acuar, Controlar criaturas, Fazer Dormir', ('Garras', 'cac', 4, '3d10+4', 'fis'), [('Bruxa do Caldeirão', 3), ('Ordenar', 2)],
        P('A Cuca é uma bruxa que se alimenta do sono dos desavisados, pessoas que dormem muito tarde ou não dormem; seu alimento preferido são crianças. Dizem que ela se alimenta do sono daqueles enfeitiçados por ela e por isso ela não precisa dormir. Ela sabe fazer poções e encantos diversos, e dizem que faz acordos escusos com pessoas que a procuram para que ela faça uma poção mágica. Dizem que o que ela mais odeia é ver crianças obedientes que dormem cedo.'),
        [
            ('Aterrorizante', 'passive', P('Quando a Cuca acerta um ataque, todos os personagens Distantes <strong>perdem um Ponto de Esperança</strong>. Receba <strong>um Ponto de Medo</strong>.'),
             {'img': I['terror'], 'actions': [A.damage('Perder Esperança', resources={'hope': 1}, rng='d'), A.gain_fear()]}),
            ('Pesadelos Seguidores', 'passive', P(f'Ao ser posta em foco pela primeira vez, surgem <strong>1d6 + a quantidade de jogadores</strong> {link("pesadelo-da-cuca", "Pesadelos da Cuca")} em alcance Distante.'),
             {'img': I['puppet'], 'actions': [A.summon(uuid('pesadelo-da-cuca'), '1d6+4', 'Invocar Pesadelos')]}),
            ('A Cuca te Pega Daqui', 'action', P('<strong>Marque 2 Pontos de Fadiga</strong> para controlar o corpo de todos os alvos Distantes que estão dormindo devido à habilidade <em>Nana Neném</em>. Aquelas criaturas viram lacaios Pesadelo da Cuca, obedecendo às ordens dela até acordarem.'),
             {'img': I['puppet'], 'actions': [A.spend('Controlar Adormecidos', stress=2)]}),
            ('Nana Neném', 'action', P('Durante a noite, <strong>gaste um Ponto de Medo</strong> para fazer <strong>1d4</strong> inimigos Distantes, que não dormiram ainda esta noite, dormirem. O alvo deve fazer um <strong>Teste de Reação de Instinto</strong>. Em caso de falha, a Cuca recupera um Ponto de Fadiga e o alvo fica <em>Adormecido</em> até sofrer dano.'),
             {'img': I['sleep'], 'effects': [E('Adormecido', '<p>Dormindo até sofrer dano. Pode ser controlado pela Cuca (A Cuca te Pega Daqui).</p>', I['sleep'])],
              'actions': [A.save('Nana Neném', 'instinct', rng='d', fear=1, effects=['Adormecido']), A.heal('Recuperar 1 PF', 'stress', 1)]}),
            ('Te Pega de Lá', 'action', P('<strong>Uma vez por cena, gaste um Ponto de Medo</strong> para pôr em foco todos os outros adversários Distantes. Ataques feitos por eles por conta desta ação causam metade do dano.'),
             {'img': I['group'], 'actions': [A.spend('Comandar', fear=1, uses=1, recovery='scene')]}),
            ('Transformação', 'action', P('Você pode <strong>marcar um Ponto de Fadiga</strong> para tomar a forma de outro humanoide que possa ver com clareza em sua mente. Enquanto estiver nessa forma, sua Dificuldade aumenta em 2 para evitar ser descoberta e enganar. Se atacar, o efeito termina.'),
             {'img': I['witch'], 'actions': [A.spend('Transformar-se', stress=1)]}),
        ], art='cuca', page=20, folder=FT[3], sort=400))

    revelado_feats = [
        ('Energia Devastadora', 'passive', P('Quando um personagem rolar 20 ou menos em testes contra o Encourado, ele deve <strong>marcar 1 Ponto de Fadiga</strong>.'),
         {'img': I['energy'], 'actions': [A.damage('Marcar Fadiga', resources={'stress': 1})]}),
        ('Natureza Demoníaca', 'passive', P('O Encourado é <strong>resistente a dano mágico</strong> e não pode ser enganado por ilusões mágicas.'), {'img': I['devil']}),
    ]
    out.append(adversary(
        'encourado', 'Encourado', 3, 'social', 17, 16, 32, 5, 7,
        'Conhecido como vampiro ou diabo, é descrito como um homem que veste roupas pretas de couro e exala um forte cheiro de sangue.',
        'Criar Tentações, Enganar, Semear Discórdia', ('Pancada', 'cac', 0, '3d6+3', 'fis'), [('Caçador Noturno', 3), ('Tentador', 3)],
        P('O Encourado é o diabo que escolheu virar vaqueiro para andar entre os vivos cobrando dívidas que ninguém lembra de ter contraído. Veste gibão, perneiras e chapéu de couro cru, e tem pés que terminam em cascos, razão pela qual nunca se descalça diante de ninguém. Seu rosto é curtido, sem poros nem suor, e ao meio-dia o corpo não lança sombra alguma. Contam no sertão que ele não entra em casa onde não foi chamado e nem aceita água oferecida com a mão esquerda. Antes dele o gado emudece e o ar cheira a couro novo e sebo queimado. Mas ele sempre cumprimenta primeiro, e na Terra da Fartura não se nega resposta a um boa-tarde.'),
        revelado_feats + [
            ('Bode Expiatório', 'action', P('<strong>Gaste 1 Ponto de Medo</strong> para marcar um personagem como alvo. O Encourado convence uma multidão de indivíduos de que o alvo é a causa de todos os seus infortúnios.'),
             {'img': I['scapegoat'], 'actions': [A.spend('Marcar o Bode Expiatório', fear=1, rng='d', amount=1)]}),
            ('Demônio em Pele de Humano', 'reaction', P(f'Quando o Encourado for derrotado ou um personagem descobrir sua verdadeira identidade, substitua o Encourado por {link("encourado-revelado", "Encourado Revelado")} e coloque-o em foco imediatamente.'),
             {'img': I['devil'], 'actions': [A.transform(uuid('encourado-revelado'), 'Revelar-se')]}),
            ('Manipulação Maldita', 'reaction', P('Quando um personagem faz um teste de ação enquanto o Encourado estiver em cena, você pode <strong>marcar um Ponto de Fadiga</strong> para adicionar <strong>1d6</strong> ao resultado do Dado de Medo.'),
             {'img': I['voices'], 'actions': [A.spend('Manipular (+1d6 no Medo)', stress=1, actionType='reaction')]}),
        ], resist=('magical',), page=21, folder=FT[3], sort=500))

    out.append(adversary(
        'encourado-revelado', 'Encourado Revelado', 3, 'solo', 17, 16, 32, 10, 8,
        'Em sua forma real, o Encourado revela garras e presas, além de longas asas demoníacas.', 'Sobrevoar, Matar, Caçar',
        ('Garras', 'cac', 5, '3d12+5', 'fis'), [('Caçador Noturno', 3), ('Sanguinário', 2)],
        P('Quando escolhe revelar a sua verdadeira forma, o Encourado estende suas enormes asas de morcego e paira sobre sua presa, fazendo com que a lua pareça desaparecer do céu. Seu ar de cobrador de dívidas dá lugar a garras e presas capazes de dilacerar a carne. O cheiro de curtume se transforma em um fedor de enxofre vindo dos mais profundos infernos.'),
        [
            ('Inclemente (3)', 'passive', P('O Encourado Revelado pode ser posto em foco até <strong>3 vezes</strong> por turno do mestre. Gaste Pontos de Medo normalmente para colocá-lo em foco.'),
             {'img': I['relentless'], 'actions': [A.spend('Foco: Inclemente', fear=1, actionType='passive')]}),
            ('Morte Vinda de Cima', 'passive', P('Enquanto estiver voando, o Encourado Revelado ganha <strong>+1</strong> de bônus em sua Dificuldade.'),
             {'img': I['wings'], 'effects': [E('Voando', '<p>+1 na Dificuldade enquanto voa.</p>', I['wings'], changes=[{'key': 'system.difficulty', 'type': 'add', 'value': 1, 'priority': None, 'phase': 'initial'}])],
              'actions': [A.spend('Alçar Voo', effects=['Voando'], target='self')]}),
        ] + revelado_feats + [
            ('Golpe Descendente', 'action', P('Mova-se até um ponto Distante e faça um ataque padrão contra um alvo no meio do caminho.'),
             {'img': I['dive'], 'actions': [A.attack('Golpe Descendente', '3d12+5', 'fis', rng='d')]}),
            ('Sede de Sangue', 'reaction', P('Quando o Encourado Revelado causa dano a um alvo Corpo a Corpo, você pode <strong>marcar uma Fadiga</strong> para fazer com que ele se alimente. O alvo deve marcar mais um PV e o Encourado Revelado recupera um PV.'),
             {'img': I['blood'], 'actions': [A.damage('Alimentar-se (+1 PV)', resources={'hitPoints': 1}, stress=1, actionType='reaction'), A.heal('Recuperar 1 PV', 'hitPoints', 1)]}),
        ], resist=('magical',), page=21, folder=FT[3], sort=510))

    # ------------------------------------------------------------------ 4º PATAMAR
    out.append(adversary(
        'abuhuku', 'Abúhukü', 4, 'solo', 20, 32, 68, 11, 6,
        'Um demônio humanoide esguio com um bico de mosquito.', 'Agarrar, Comer, Espreitar, Perfurar',
        ('Probóscide', 'cac', 9, '4d10+10', 'fis'), [('Espreitar', 5), ('Pelos Grudentos', 3)],
        P('Abúhukü é a personificação da morte, da doença e do mal. Tem um corpo antropomórfico com membros alongados, uma segunda face na nuca e um grande probóscide para sugar o sangue e as entranhas de suas vítimas. Algumas lendas dizem que a fumaça gerada pela queima de uma pimenta específica é tóxica para o Abúhukü, mas ninguém nunca sobreviveu para contar a história. Sua pelagem é fétida e grudenta, o que torna fácil saber se ele está por perto; por outro lado, caso você sinta esse cheiro, já é tarde demais para fugir.'),
        [
            ('Inclemente (3)', 'passive', P('O Abúhukü pode ser posto em foco até <strong>3 vezes</strong> por turno do mestre. Gaste Pontos de Medo normalmente para colocá-lo em foco.'),
             {'img': I['relentless'], 'actions': [A.spend('Foco: Inclemente', fear=1, actionType='passive')]}),
            ('Abraço da Morte', 'action', P('<strong>Marque 2 Pontos de Fadiga</strong> para fazer o Abúhukü se mover e fazer um ataque padrão contra um alvo em alcance Distante. Em caso de sucesso, o alvo sofre <strong>4d20+5</strong> de dano físico e fica <em>Imobilizado</em> graças aos pelos grudentos dele até ter sucesso em um Teste de Força. A cada vez que o Abúhukü for posto em foco, ele pode causar esse dano automaticamente até o alvo escapar. Nesse estado, o Abúhukü perde sua habilidade Inclemente (3).'),
             {'img': I['mosquito'], 'effects': [imobilizado('Preso pelos pelos grudentos do Abúhukü até ter sucesso em um Teste de Força.')],
              'actions': [A.attack('Abraço da Morte', '4d20+5', 'fis', rng='d', stress=2, effects=['Imobilizado']),
                          A.damage('Dano Contínuo', '4d20+5', 'fis')]}),
            ('Fumaça Doentia', 'action', P('<strong>Gaste um Ponto de Medo</strong> para que o Abúhukü produza uma fumaça carregada de doenças em alcance Muito Próximo. Todos dentro da área devem fazer um <strong>Teste de Reação de Instinto</strong>. Em caso de falha, o alvo respira a fumaça e fica <em>Adoecido</em>. Um alvo Adoecido recebe −1 em todos os atributos até o próximo descanso. Essa condição pode acumular até 2 vezes.'),
             {'img': I['smoke'], 'effects': [E('Adoecido', '<p>−1 em todos os atributos até o próximo descanso (acumula até 2 vezes).</p>', I['smoke'], duration='shortRest',
                                               changes=[{'key': f'system.traits.{t}.value', 'type': 'add', 'value': -1, 'priority': None, 'phase': 'initial'} for t in ('agility', 'strength', 'finesse', 'instinct', 'presence', 'knowledge')])],
              'actions': [A.save('Fumaça Doentia', 'instinct', rng='mp', fear=1, effects=['Adoecido'])]}),
            ('Mesclar com as Sombras', 'action', P('<strong>Gaste um Ponto de Medo</strong> para que o Abúhukü se torne um com as sombras e fique <em>Sob as Sombras</em>. Enquanto estiver Sob as Sombras, o Abúhukü tem vantagem em testes e recebe resistência a dano mágico. Ao sofrer dano Maior ou superior, ele deixa de estar Sob as Sombras.'),
             {'img': I['shadow'], 'effects': [E('Sob as Sombras', '<p>Vantagem em testes e resistência a dano mágico. Termina ao sofrer dano Maior ou superior.</p>', I['shadow'])],
              'actions': [A.spend('Mesclar-se', fear=1, effects=['Sob as Sombras'], target='self')]}),
            ('Impulso', 'reaction', P('Quando o Abúhukü acertar um ataque contra um personagem, receba <strong>um Ponto de Medo</strong>.'),
             {'img': I['momentum'], 'actions': [A.gain_fear()]}),
        ], page=22, folder=FT[4], sort=100))

    # Boitatá — colosso em três segmentos
    boitata_lore = P('O Boitatá é o guardião dos campos e a punição de quem os incendeia. Tem o corpo de uma serpente imensa de um fogo azulado que não queima as folhas por onde passa, e olhos enormes, feitos dos olhos de todos os animais mortos nas queimadas. Antes dele, o capim exala cheiro de queimado sem que haja brasa, e carcaças aparecem com as órbitas vazias. A luz das suas chamas dançando sobre a mata pode parecer distante, mas quem fica para olhar essa luz já entregou a ele os próprios olhos.')
    colosso = ('<div class="eclipse-box"><p><strong>4º Patamar · Colosso</strong> — <strong>Tamanho:</strong> 120 m de comprimento. '
               '<strong>Segmentos:</strong> 1 Cabeça, 2 Corpos, 1 Cauda. <strong>Limiares:</strong> 37/69 · <strong>Fadiga:</strong> 8 (compartilhada). '
               '<strong>Experiência:</strong> Fúria Primitiva da Mata +4, Presença Deslumbrante e Cegante +3.</p>'
               f'<p>Segmentos: {link("boitata-cabeca", "Cabeça")} · {link("boitata-corpo", "Corpo (×2)")} · {link("boitata-cauda", "Cauda")}. '
               'Use as regras de Colosso da Campanha de Caça a Monstros do SRD.</p></div>')
    base_short = 'O Boitatá é uma gigantesca serpente de fogo que protege as matas e os animais contra destruidores e caçadores.'
    bmot = 'Cegar contempladores, Defender as profundezas da mata, Queimar invasores'
    bexp = [('Fúria Primitiva da Mata', 4), ('Presença Deslumbrante e Cegante', 3)]
    out.append(adversary(
        'boitata-cabeca', 'Boitatá (Cabeça)', 4, 'solo', 19, 37, 69, 5, 8, base_short, bmot,
        ('Mordida de Fogo', 'mp', 6, '4d12+10', 'fis'), bexp, boitata_lore,
        [
            ('Segmentos Adjacentes: Corpo', 'passive', P('A Cabeça é adjacente ao segmento Corpo.'), {'img': I['crawl']}),
            ('Letal', 'passive', P('Quando a Cabeça é <strong>Destruída</strong>, o Boitatá é derrotado.'), {'img': I['bite_fire']}),
            ('Proteção de Fogo', 'passive', P('Enquanto estiver envolta na Proteção de Fogo, a Cabeça <strong>não pode marcar Pontos de Vida</strong>.'), {'img': I['fire']}),
            ('Cisco no Olho', 'passive', P('Apesar de muito poderosos, os olhos do Boitatá são sua maior fraqueza: sempre que um personagem atacar diretamente algum de seus olhos, a Cabeça perde sua <em>Proteção de Fogo</em> até ser colocada em foco novamente.'), {'img': I['eye']}),
            ('Loucura dos Mil Olhos', 'passive', P('<strong>Contagem (Ciclo 4).</strong> Na primeira vez que o grupo vir o Boitatá, ative a contagem. Personagens em alcance Muito Distante devem fazer um <strong>Teste de Reação de Instinto</strong>. Em caso de falha, o personagem fica <em>Louco</em>. Personagens Loucos diminuem a contagem sempre que rolarem com Medo. Quando ela terminar, todos os personagens em alcance Muito Distante sofrem uma penalidade de −1 em todos os Testes de Ação e Reação até o próximo descanso. Essa penalidade é cumulativa. Caso nenhum personagem fique Louco, o mestre pode gastar 2 Pontos de Medo para forçar o grupo a fazer o Teste de Reação de Instinto novamente.'),
             {'img': I['thousand'], 'effects': [E('Louco', '<p>Diminua a contagem Loucura dos Mil Olhos sempre que rolar com Medo.</p>', I['thousand'])],
              'actions': [A.save('Contemplar o Boitatá', 'instinct', rng='md', effects=['Louco']),
                          A.countdown('Loucura dos Mil Olhos', 4, I['thousand'], looping='looping'),
                          A.spend('Forçar novo teste', fear=2)]}),
            ('O Fogo Purifica', 'passive', P('Sempre que o Boitatá sofrer um ataque corpo a corpo, o atacante deve <strong>marcar um Ponto de Armadura</strong>.'), {'img': I['purify']}),
            ('Terror Grandioso', 'reaction', P('Sempre que o Boitatá errar um ataque, receba <strong>1 Ponto de Medo</strong>.'),
             {'img': I['terror'], 'actions': [A.gain_fear()]}),
            ('Controlar o Fogo', 'action', P('<strong>Marque um Ponto de Fadiga</strong> para controlar o fogo, aumentando-o ou fazendo-o desaparecer. Inimigos em alcance Distante devem fazer um <strong>Teste de Reação de Agilidade</strong>. Em caso de falha, sofrem <strong>4d20+5</strong> de dano mágico e ficam temporariamente <em>Incendiados</em>. Sempre que uma criatura Incendiada age, ela deve marcar 1 PA ou 1 PV. Se passarem, recebem metade do dano e não ficam Incendiados.'),
             {'img': I['firebreath'], 'effects': [E('Incendiado', '<p>Sempre que agir, marque 1 Ponto de Armadura ou 1 Ponto de Vida.</p>', I['fire'])],
              'actions': [A.save('Controlar o Fogo', 'agility', '4d20+5', 'mag', rng='d', stress=1, half=True, effects=['Incendiado'])]}),
        ], art='boitata', size='huge', page=22, folder=FT[4], sort=200, extra_desc=colosso))
    out.append(adversary(
        'boitata-corpo', 'Boitatá (Corpo)', 4, 'solo', 18, 37, 69, 7, 8, base_short, bmot,
        ('Constrição Calcinante', 'mp', 4, '4d8+10', 'fis'), bexp, boitata_lore,
        [
            ('Segmentos Adjacentes: Cabeça, Cauda e Corpo', 'passive', P('O Corpo é adjacente à Cabeça, à Cauda e ao outro Corpo.'), {'img': I['crawl']}),
            ('Chacoalhar', 'action', P('<strong>Gaste um Ponto de Medo</strong> para se chacoalhar e derrubar personagens do seu corpo. Todas as criaturas no Boitatá devem fazer um <strong>Teste de Reação de Força</strong>. Em caso de falha, caem até o chão e devem marcar 1 PV. Em caso de sucesso, devem marcar 1 PF.'),
             {'img': I['shake'], 'actions': [A.save('Chacoalhar', 'strength', rng='mp', fear=1, resources={'hitPoints': 1}), A.damage('Sucesso: marcar 1 PF', resources={'stress': 1})]}),
            ('Olhar por Olho', 'reaction', P('Ao rolar um ataque com Medo contra esse segmento, você pode <strong>marcar um Ponto de Fadiga</strong> para fazer o jogador fazer um <strong>Teste de Reação de Instinto</strong>. Se falhar, ele fica temporariamente <em>Cego</em>. Personagens Cegos têm desvantagem em testes de ataque.'),
             {'img': I['eye'], 'effects': [E('Cego', '<p>Desvantagem em testes de ataque.</p>', I['eye'])],
              'actions': [A.save('Olhar por Olho', 'instinct', rng='cac', stress=1, effects=['Cego'], actionType='reaction', amount=1)]}),
        ], art='boitata', size='huge', page=23, folder=FT[4], sort=210, extra_desc=colosso))
    out.append(adversary(
        'boitata-cauda', 'Boitatá (Cauda)', 4, 'solo', 17, 37, 69, 6, 8, base_short, bmot,
        ('Rabada', 'mp', 4, '4d10+6', 'fis'), bexp, boitata_lore,
        [
            ('Segmentos Adjacentes: Corpo', 'passive', P('A Cauda é adjacente ao segmento Corpo.'), {'img': I['crawl']}),
            ('Ponto de Entrada', 'passive', P('Por estar sempre em contato com o chão, a dificuldade para escalar esse segmento diminui em <strong>3</strong>.'), {'img': I['tail']}),
            ('Porta Fechada', 'passive', P('Ao ser destruído, esse segmento irrompe em chamas e espasmos descontrolados. Personagens sofrem <strong>4d6+8</strong> pontos de dano direto por ação que fizerem enquanto estiverem nesse segmento. Além disso, a dificuldade para escalá-lo aumenta em 5.'),
             {'img': I['fire'], 'actions': [A.damage('Chamas do Segmento', '4d6+8', 'mag', direct=True)]}),
            ('Rasteira', 'action', P('<strong>Marque um Ponto de Fadiga</strong> para fazer um ataque padrão contra todos os alvos em alcance Próximo.'),
             {'img': I['tail'], 'actions': [A.attack('Rasteira', '4d10+6', 'fis', rng='p', stress=1, amount=None)]}),
        ], art='boitata', size='huge', page=23, folder=FT[4], sort=220, extra_desc=colosso))

    out.append(adversary(
        'boiuna', 'Boiúna', 4, 'solo', 18, 40, 70, 12, 8,
        'Uma cobra preta colossal conhecida como o Presságio do Fim.', 'Acabar com o Mundo, Destruir, Exterminar',
        ('Pancada', 'mp', 7, '4d10+12', 'fis'), [('Destruir', 5)],
        P('A Boiúna é a mãe dos rios, a fome antiga que dorme sob o leito da Terra da Fartura. Em algumas regiões é chamada de Cobra-Grande: seu corpo negro é largo como um tronco de árvore, sua pele escamosa cheira a lodo e seus olhos ardem como duas lamparinas acesas sobre a água. Povos ribeirinhos juram já terem visto o rio correr ao contrário e atribuem o feito à Boiúna, mas a verdade é que ninguém ousou entrar na água neste dia, com medo do que poderia acontecer.'),
        [
            ('Aterrorizante', 'passive', P('Quando a Boiúna acerta um ataque, todos os personagens Distantes <strong>perdem um Ponto de Esperança</strong>. Receba <strong>um Ponto de Medo</strong>.'),
             {'img': I['terror'], 'actions': [A.damage('Perder Esperança', resources={'hope': 1}, rng='d'), A.gain_fear()]}),
            ('Escamas Ácidas', 'passive', P('Personagens que entrarem em contato com as escamas da Boiúna devem rolar 1d6. Em um resultado de 2 ou menos, devem marcar uma Armadura. Se não for possível marcar uma Armadura, o atacante deve marcar um Ponto de Vida.'), {'img': I['acid']}),
            ('Inclemente (2)', 'passive', P('A Boiúna pode ser posta em foco até <strong>2 vezes</strong> por turno do mestre. Gaste Pontos de Medo normalmente para colocá-la em foco.'),
             {'img': I['relentless'], 'actions': [A.spend('Foco: Inclemente', fear=1, actionType='passive')]}),
            ('Rajada de Escamas', 'action', P('<strong>Gaste um Ponto de Fadiga</strong> para expelir escamas venenosas na área. Faça um ataque contra os alvos em alcance Próximo. Em um sucesso, cause <strong>4d8+6</strong> de dano físico direto e deixe os alvos <em>Envenenados</em>. Enquanto estiver Envenenado, o alvo deve rolar 1d6 antes de todos os seus testes. Se rolar 4 ou menos, o alvo deve marcar um Ponto de Fadiga.'),
             {'img': I['scales'], 'effects': [E('Envenenado', '<p>Role 1d6 antes de cada teste; com 4 ou menos, marque um Ponto de Fadiga.</p>', I['poison'])],
              'actions': [A.attack('Rajada de Escamas', '4d8+6', 'fis', rng='p', stress=1, direct=True, effects=['Envenenado'], amount=None)]}),
            ('Rastejar e Devastar', 'action', P('<strong>Gaste um Ponto de Fadiga</strong> para mover a Boiúna até alcance Distante. Alvos no caminho devem ter sucesso em um <strong>Teste de Agilidade</strong> ou sofrer <strong>4d8</strong> de dano físico.'),
             {'img': I['crawl'], 'actions': [A.save('Rastejar e Devastar', 'agility', '4d8', 'fis', rng='d', stress=1)]}),
        ], size='huge', page=24, folder=FT[4], sort=300))

    out.append(adversary(
        'loira-do-banheiro', 'Loira do Banheiro', 4, 'social', 19, 28, 58, 6, 5,
        'Uma mulher loira de vestido branco rodeada por brumas.', 'Assustar, Matar, Saciar sua Sede de Sangue',
        ('Garras Sangrentas', 'mp', 5, '4d8+6', 'mag'), [('Assombrar', 5)],
        P('Uma loira gigantesca e fantasmagórica, com a pele cinzenta de quem foi velada por dias, cabelos claros empapados de umidade e pedaços de algodão enfiados nas narinas, encharcados de um sangue que nunca seca. Seu corpo fica preso ao espelho, mas não se engane achando que isso o manterá a salvo. Sua aparição vem acompanhada de brumas que fazem com que os que tentam fugir acabem voltando para ela. Dizem que, para encontrá-la, basta chamar seu nome em frente ao espelho três vezes e ela virá.'),
        [
            ('Cercada por Brumas', 'passive', P('A área em alcance Distante da Loira do Banheiro sempre está tomada por brumas; personagens dentro dessa área têm desvantagem em Testes de Instinto relacionados à visão. Personagens que tentarem sair da área devem ter sucesso em um Teste de Instinto.'), {'img': I['mist']}),
            ('Presença Perturbadora', 'passive', P('Ao falhar em um teste contra a Loira do Banheiro, o personagem <strong>perde um Ponto de Esperança</strong>.'),
             {'img': I['hope'], 'actions': [A.damage('Perder Esperança', resources={'hope': 1})]}),
            ('Sede de Sangue', 'passive', P('<strong>Contagem Regressiva (Decrescente 10).</strong> Quando a Loira do Banheiro entra em cena pela primeira vez, ative a contagem. Sempre que um personagem fizer um teste relacionado à Loira do Banheiro, diminua a contagem em uma quantidade igual ao número de Pontos de Vida que o personagem tem marcado. Quando a contagem termina, a Loira do Banheiro entra em uma sede de sangue insaciável. A partir desse ponto, qualquer interação amigável com a Loira do Banheiro falha automaticamente.'),
             {'img': I['blood'], 'actions': [A.countdown('Sede de Sangue (Loira do Banheiro)', 10, I['blood'], looping='decreasing')]}),
            ('Olhar Desconcertante', 'action', P('O olhar da Loira do Banheiro, sedento por sangue, é assustador. <strong>Gaste um Ponto de Medo</strong> para que todos os personagens em alcance Próximo façam um <strong>Teste de Reação de Presença</strong>. Em caso de falha, eles devem marcar <strong>2 Pontos de Fadiga</strong>.'),
             {'img': I['stare'], 'actions': [A.save('Olhar Desconcertante', 'presence', rng='p', fear=1, resources={'stress': 2})]}),
            ('Brumas do Pavor', 'reaction', P('Quando um personagem faz um Teste de Ação com a Loira do Banheiro em cena, você pode <strong>marcar um Ponto de Fadiga</strong> para retirar <strong>1d4</strong> do resultado do Dado de Esperança.'),
             {'img': I['mist'], 'actions': [A.spend('Retirar 1d4 da Esperança', stress=1, actionType='reaction')]}),
            ('O Chamado', 'reaction', P('A Loira do Banheiro aparece em cena no momento em que um mortal repete seu nome três vezes na frente de um espelho. Caso esse espelho seja quebrado, todos os personagens em alcance Distante ficam <em>Azarentos</em> até o próximo descanso. Quando um personagem Azarento faz um teste de ação, seu resultado sempre gera um Ponto de Medo para o mestre. Rolagens com Esperança ainda geram Pontos de Esperança.'),
             {'img': I['mirror'], 'effects': [E('Azarento', '<p>Todo teste de ação gera um Ponto de Medo para o mestre (rolagens com Esperança ainda geram Esperança). Dura até o próximo descanso.</p>', I['mirror'], duration='shortRest')],
              'actions': [A.spend('Espelho Quebrado', effects=['Azarento'], rng='d')]}),
        ], page=24, folder=FT[4], sort=400))
    return FOLDERS + out
