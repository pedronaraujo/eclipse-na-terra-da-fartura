from lib import *
from adversaries import uuid as adv_uuid, SRD, P, SRC, I

PACK_ENV = 'ambientes'
PACK_NPC = 'aliados'


def env_uuid(key):
    return f'Compendium.{MOD}.{PACK_ENV}.Actor.{gid("actor", key)}'


def npc_uuid(key):
    return f'Compendium.{MOD}.{PACK_NPC}.Actor.{gid("actor", key)}'


def Q(*qs):
    """Perguntas do ambiente (aparecem como segredo para o mestre, no padrão do SRD)."""
    sid = gid('secret', *qs)
    return f'<section id="secret-{sid}" class="secret">' + ''.join(f'<p><em>{q}</em></p>' for q in qs) + '</section>'


def environment(key, name, tier, etype, dif, short, impulses, adversaries_label, adversaries, feats, art=None,
                page=None, sort=0, extra=''):
    aid = gid('actor', key)
    tok = f'{ASSET}/tokens/{key}.webp'
    items = []
    for i, f in enumerate(feats):
        name_f, form, desc, *rest = f
        opts = rest[0] if rest else {}
        items.append(feature(key, name_f, form, desc, actions=opts.get('actions', ()), effects=opts.get('effects', ()),
                             img=opts.get('img'), sort=(i + 1) * 100))
    pot = {}
    if adversaries:
        pot[gid(key, 'pot')] = {'label': adversaries_label, 'adversaries': adversaries}
    doc = {'_id': aid, 'name': name, 'type': 'environment', 'img': f'{ASSET}/art/{art}.webp' if art else tok,
           'folder': None, 'sort': sort,
           'system': {'tier': tier, 'type': etype, 'difficulty': dif, 'impulses': impulses,
                      'description': f'<p><em>{short}</em></p>{extra}', 'notes': '', 'potentialAdversaries': pot,
                      'attribution': {'source': SRC, 'page': page, 'artist': '', 'srd': False}},
           'prototypeToken': prototype_token(name, tok, disposition=0),
           'items': items, 'effects': [], 'flags': {MOD: {'key': key}}}
    return finalize_actor(doc)


def build_env():
    out = []
    out.append(environment(
        'mae-de-ouro', 'Mãe de Ouro', 1, 'exploration', 11,
        'Envolvida por árvores, uma curiosa aparição em formato de mulher com cabelos dourados aparece para o grupo.',
        'Atrair o grupo, descobrir o motivo de estarem ali, enganar aqueles de coração ruim',
        'Guardiões da Mata',
        [SRD + 'C9vt09lsAa6AeXeg', SRD + '9x2xY9zwc3xzbXo5', SRD + 'G62k4oSkhkoXEs2D', SRD + 'PKSXFuaIHUCoH63A', adv_uuid('mapinguari')],
        [
            ('Presença Encantadora', 'passive', P('A presença mística da Mãe de Ouro é encantadora. Todos os personagens que podem ver a Mãe de Ouro têm <strong>desvantagem em Testes de Presença</strong>.') + Q('Por que ela é tão atraente? Como isso está afetando os personagens?'), {'img': 'icons/magic/light/explosion-star-glow-yellow.webp'}),
            ('Julgamento de Caráter', 'action', P('<strong>Gaste um Ponto de Medo</strong> para fazer com que a Mãe de Ouro julgue o caráter do grupo. Os personagens devem ter sucesso em um <strong>Teste de Reação de Presença</strong>. Em caso de falha, a Mãe de Ouro julga perfeitamente o caráter dos personagens que falharam.') + Q('Como ela julga cada personagem? Como ela age ao fazer isso?'),
             {'img': 'icons/skills/social/trading-justice-scale-yellow.webp', 'actions': [A.save('Julgar o Caráter', 'presence', rng='d', fear=1)]}),
            ('Coração Verdadeiro', 'reaction', P('Caso os personagens consigam convencer a Mãe de Ouro de que são boas pessoas, ela levará o grupo para um local de tesouros. Caso contrário, ela vai prometer o mesmo, mas vai levar o grupo para uma emboscada.') + Q('Como a Mãe de Ouro chegou nessa conclusão? Para onde ela os levará?'), {'img': 'icons/commodities/treasure/goblet-coins-gold.webp'}),
            ('Fulgor Dourado', 'reaction', P('Sempre que um personagem falhar em um Teste de Presença relacionado com a Mãe de Ouro, ele deve <strong>marcar um Ponto de Fadiga</strong>.') + Q('Como o brilho dela afeta os personagens? Por que isso só os afeta quando estão se direcionando a ela?'),
             {'img': 'icons/magic/light/beam-strike-orange-gold.webp', 'actions': [A.damage('Marcar Fadiga', resources={'stress': 1})]}),
        ], art='mata-emaranhada', page=25, sort=100,
        extra=P('<em>Outros adversários potenciais citados na revista:</em> Rilhas em Bando.')))

    out.append(environment(
        'festa-junina', 'Festa Junina', 2, 'social', 14,
        'Uma festa cultural que mistura brincadeiras com crendices populares. A festa predileta dos Encantados da região.',
        'Comemorar as colheitas, homenagear os Encantados, juntar a comunidade, oportunidades para seres Encantados, proteção contra a escuridão',
        'Convidados da Festa', [adv_uuid('caipora'), adv_uuid('curupira'), SRD + 'Al3w2CgjfdT3p9ma', adv_uuid('saci-perere')],
        [
            ('Comilança da Boa', 'passive', P('A comida da Festa Junina é conhecida por ser uma delícia e acalentar o coração do povo. Uma vez durante o evento, cada PJ pode gastar um punhado de ouro para comprar comidas típicas (pé de moleque, pinhão, pamonha, curau, bolo de milho, pipoca, quentão). Ao comerem, <strong>limpam um Ponto de Fadiga e recebem um Ponto de Esperança</strong>.') + Q('Com que comidas o grupo se alimenta? Por que essa comida é tão boa?'),
             {'img': 'icons/consumables/food/plate-fish-bowl-bones-brown.webp', 'actions': [A.heal('Limpar 1 PF', 'stress', 1, target='any'), A.heal('Ganhar 1 Esperança', 'hope', 1, target='any')]}),
            ('Fofoca da Vila', 'passive', P('Um personagem que jogue conversa fora com PdMs da vila durante a Festa Junina pode fazer um <strong>Teste de Presença</strong> para receber informações sobre acontecimentos locais. As informações dependem do resultado:') +
             '<ul><li><strong>Sucesso Crítico:</strong> descobre informações relevantes sobre duas pessoas ou acontecimentos importantes da vila. O personagem pode fazer uma pergunta sobre um rumor e obter uma resposta verdadeira (mas não necessariamente completa).</li>'
             '<li><strong>Sucesso com Esperança:</strong> ouve falar sobre dois acontecimentos recentes, e ao menos um deles é relevante para o personagem.</li>'
             '<li><strong>Sucesso com Medo:</strong> ouve falar sobre dois acontecimentos recentes, e ao menos um deles é relevante para o personagem.</li>'
             '<li><strong>Falha com Esperança:</strong> os habitantes não sentem confiança para fofocar com o personagem por perto. É preciso marcar um Ponto de Fadiga para descobrir um boato relevante.</li>'
             '<li><strong>Falha com Medo:</strong> além de ninguém parecer confiar no personagem, ele se torna alvo de fofocas e boatos. Deve marcar um Ponto de Fadiga e, junto com o mestre, decidir qual fofoca está sendo espalhada sobre ele.</li></ul>' +
             Q('Sobre quem estão falando nas rodas de conversa da festa? Há informações úteis para os personagens? Quais são?'), {'img': 'icons/skills/social/diplomacy-writing-letter.webp'}),
            ('Quadrilha', 'action', P('<strong>Gaste um Ponto de Medo</strong> para começar uma quadrilha, um dos eventos principais da Festa Junina. Se um dos PJs quiser participar da dança, ele deve fazer um <strong>Teste de Presença</strong>. Se tiver sucesso, recebe vantagem para interações sociais durante a Festa Junina e consegue entrar na dança. Se falhar, deve marcar um Ponto de Fadiga e descrever como os dançarinos não o deixam entrar na dança.') + Q('De quem você se aproxima após compartilhar a dança em quadrilha?'),
             {'img': 'icons/skills/trades/music-notes-sound-blue.webp', 'actions': [A.spend('Começar a Quadrilha', fear=1)]}),
            ('Travessura do Saci', 'action', P(f'O {link_adv("saci-perere", "Saci-Pererê")} está presente na festa. <strong>Gaste um Ponto de Medo</strong> para que o Saci esconda um pertence de alguém. O alvo deve fazer um <strong>Teste de Reação de Instinto</strong>; se falhar, seu item some e aparece em outro lugar ou com outra pessoa presente na festa. Se preferir, o mestre pode fazer com que um item apareça com um jogador. Se passar no teste e perceber o Saci, o jogador pode tentar confrontá-lo.') + Q('Que acusações surgem a partir da brincadeira do Saci? Alguém procura algo importante que sumiu? O que é?'),
             {'img': 'icons/skills/social/theft-pickpocket-bribery-brown.webp', 'actions': [A.save('Travessura', 'instinct', rng='p', fear=1, amount=1)]}),
            ('Fogueira', 'reaction', P('A fogueira da Festa Junina é um símbolo de proteção e homenagem ao sol. Alimentar a fogueira, mantendo-a acesa e tratando-a com respeito e reverência, fornece ao personagem <strong>um Ponto de Esperança</strong> e <strong>vantagem</strong> em um teste à escolha do jogador contra monstros e Criaturas da Noite. Além disso, lutar contra Criaturas da Noite em alcance Próximo da fogueira fornece vantagem ao atacar.') + Q('Que conversas acontecem ao redor da fogueira? Que sensação ela dá aos jogadores ao se aproximarem? Que lembranças eles têm?'),
             {'img': 'icons/magic/fire/flame-burning-embers-yellow.webp', 'actions': [A.heal('Ganhar 1 Esperança', 'hope', 1, target='any')]}),
        ], page=25, sort=200))

    out.append(environment(
        'rondolo', 'Rondolo', 3, 'event', 14, 'A ave gigante que traz uma grande tempestade e maus presságios.',
        'Anunciar tempestades, criar pânico nos povoados, trazer maus presságios', 'Na Tempestade',
        [SRD + 'P7h54ZePFPHpYwvB', SRD + 'sRn4bqerfARvhgSV', SRD + 'xIICT6tEdnA7dKDV', SRD + 'tLHNONmalytgnngv'],
        [
            ('Aparição do Rondolo', 'passive', P('<strong>Contagem Regressiva (8).</strong> Quando o Rondolo chegar, inicie esta contagem. Na maioria das vezes, o Rondolo não é visto dentro da tempestade: as nuvens e a chuva são tão densas que é difícil encontrá-lo. Sempre que alguém rolar um teste de ação com Esperança, diminua a contagem em um. Quando a contagem zerar, os jogadores, juntos, devem escolher entre Esperança ou Medo:') +
             '<ul><li><strong>Esperança:</strong> eles conseguem se deslocar para fora da tempestade e o evento se encerra.</li>'
             '<li><strong>Medo:</strong> todos os personagens devem marcar um Ponto de Fadiga. Eles adentram o centro da tempestade e encontram uma colossal ave branca com detalhes cinzas, o próprio Rondolo. Os jogadores devem fazer um <strong>Teste em Grupo</strong>. Conforme o resultado, o Rondolo compartilha uma visão do futuro daqueles personagens. A visão não deve ser objetiva: construa algo subjetivo, com sensações e situações abstratas que envolvam as aspirações dos personagens. Após isso a tempestade cessa.'
             '<ul><li><strong>Sucesso Crítico:</strong> visão positiva do futuro de todo o grupo. Em algum momento da campanha, o jogador pode reivindicar esta visão e transformar uma rolagem de qualquer membro do grupo em um sucesso crítico.</li>'
             '<li><strong>Sucesso:</strong> visão positiva do futuro do personagem. Em algum momento da campanha, o jogador pode reivindicar esta visão e transformar uma rolagem com Esperança em um sucesso crítico.</li>'
             '<li><strong>Falha:</strong> visão negativa do futuro do personagem. Em algum momento da campanha, o mestre pode reivindicar esta visão e transformar um sucesso que não seja crítico do jogador em uma falha com Medo.</li></ul></li></ul>' +
             Q('Os personagens vão se agarrar à esperança de um novo dia e sair da tempestade ou irão encarar o medo e conhecer algo sobre seu futuro?', 'Ter presságios sobre o futuro traz que tipo de sensação a eles? Eles acreditam que podem alterar estas visões?'),
             {'img': 'icons/creatures/birds/raptor-hawk-flying.webp', 'actions': [A.countdown('Aparição do Rondolo', 8, 'icons/creatures/birds/raptor-hawk-flying.webp', looping='decreasing', ctype='narrative')]}),
            ('Mau Presságio', 'passive', P('O Rondolo é um sinal de mau presságio; traz consigo o anúncio de que nada de bom virá adiante. Entre os povos há a dúvida se ele é um aviso de que algo ruim está por vir ou se é ele que faz coisas ruins acontecerem, mas uma coisa é certa: ao aparecer, o medo se instaura por todos. Enquanto está ativo, <strong>todas as rolagens têm seus Dados de Medo aumentados para d20</strong>.') + Q('A presença do Rondolo traz consigo medo e maus presságios. Que lembranças de tempestades cruéis os personagens possuem?'), {'img': 'icons/magic/control/fear-fright-shadow-monster-red.webp'}),
            ('Vendaval', 'passive', P('Com o Rondolo presente, os ventos fortes de uma tempestade comum parecem apenas uma brisa suave. O Rondolo traz consigo vendavais que dificultam qualquer movimento. Todas as criaturas devem fazer um <strong>Teste de Agilidade</strong> para andar até distância Próxima. Sempre que falharem em um teste para se deslocar, devem <strong>marcar um Ponto de Fadiga</strong>.') + Q('Os personagens já viram ventos tão fortes como esse? Existe local possível para se proteger dele?'),
             {'img': 'icons/magic/air/wind-tornado-wall-blue.webp', 'actions': [A.damage('Marcar Fadiga', resources={'stress': 1})]}),
            ('Bater das Asas', 'action', P('<strong>Gaste um Ponto de Medo</strong> para que o bater das asas do Rondolo gere uma gigantesca tempestade de raios e trovões. Todos os personagens devem fazer um Teste de Reação usando uma característica que você escolher para evitarem ser atingidos. Alvos que falharem recebem <strong>3d10+5</strong> de dano mágico.') + Q('Que sensações vêm ao encarar a tempestade de raios e trovões ensurdecedores? Existe esperança em sair vivos dali?'),
             {'img': 'icons/magic/lightning/bolts-forked-large-blue.webp', 'actions': [A.save('Bater das Asas', 'agility', '3d10+5', 'mag', rng='md', fear=1)]}),
            ('Mau Agouro', 'reaction', P('Quando um personagem rolar um teste com Medo, você pode <strong>gastar um Ponto de Medo</strong> para lançar um Mau Agouro nele. O jogador fica <em>Vulnerável</em> e algo de ruim vai lhe acontecer no próximo dia. Você pode decidir o quê, ou mudar um Sucesso com Medo em uma falha.') + Q('Que tipo de má sorte irá se abater sobre os personagens?'),
             {'img': 'icons/magic/death/skull-energy-light-purple.webp', 'effects': [vulneravel('Mau Agouro: algo de ruim vai acontecer no próximo dia.')],
              'actions': [A.spend('Lançar Mau Agouro', fear=1, effects=['Vulnerável'], amount=1, actionType='reaction')]}),
        ], page=26, sort=300))

    out.append(environment(
        'opartaba', 'Opartabá', 4, 'exploration', 20,
        'A cidade adormecida de Opartabá, localizada abaixo de uma floresta, está perdida há milênios, com diversos segredos e perigos a serem encontrados.',
        'Guardar o segredo, manter indesejados fora, ser redescoberta', 'Guardiões da Cidade',
        [SRD + 'Tg1F1PthQWeKdLJT', SRD + 'befIqd5IYKg6eUz2', SRD + 'DJTVWE5AuWKsAdLZ'],
        [
            ('Conhecimento Perdido', 'passive', P('A tecnologia e o conhecimento de Opartabá ficaram perdidos por tempo demais. Testes de Conhecimento feitos para entender algo deste ambiente têm <strong>desvantagem</strong>.') + Q('Que segredos estão escondidos aqui? Qual conhecimento falta para os personagens entenderem esse local?'), {'img': 'icons/skills/trades/academics-book-study-runes.webp'}),
            ('Imperturbado', 'passive', P(f'Apesar de estar escondida por muito tempo, Opartabá ainda está viva, de certo modo, e não gosta de ser perturbada. Se os personagens fizerem algo desrespeitoso para a cidade, sua cultura ou religião, invoque um @UUID[{SRD}befIqd5IYKg6eUz2]{{Oráculo da Perdição}} em alcance Distante do grupo e coloque-o em foco imediatamente.') + Q('Quais ações seriam consideradas desrespeitosas pelo povo que viveu aqui? Como os personagens podem se redimir com a cidade?'),
             {'img': 'icons/magic/death/skeleton-skull-soul-blue.webp', 'actions': [A.summon(SRD + 'befIqd5IYKg6eUz2', 1, 'Invocar Oráculo da Perdição')]}),
            ('Instabilidade Geográfica', 'action', P('<strong>Gaste um Ponto de Medo</strong> para que as rochas do teto que estavam parcialmente soltas sofram um desabamento. O grupo deve ter sucesso em um <strong>Teste de Reação de Força</strong> ou sofre <strong>4d10+6</strong> pontos de dano físico e fica <em>Imobilizado</em> até ter sucesso em um Teste de Força. Em um sucesso, sofrem metade do dano e evitam a condição.') + Q('Qual foi a causa dessa instabilidade? Como os personagens suportam esse desabamento?'),
             {'img': 'icons/magic/earth/projectile-stone-landslide.webp', 'effects': [imobilizado('Soterrado até ter sucesso em um Teste de Força.')],
              'actions': [A.save('Desabamento', 'strength', '4d10+6', 'fis', rng='d', fear=1, half=True, effects=['Imobilizado'])]}),
            ('Retorno dos Cidadãos', 'action', P(f'<strong>Gaste um Ponto de Medo</strong> para invocar <strong>1d4</strong> @UUID[{SRD}Tg1F1PthQWeKdLJT]{{Legiões Fantasmagóricas}} que surgem Próximas, ao redor do grupo.') + Q('Quem eram essas pessoas antes de passarem pelo véu da vida? Como elas se sentem ao ver alguém vivo aqui depois de tanto tempo?'),
             {'img': 'icons/magic/death/undead-ghosts-trio-blue.webp', 'actions': [A.summon(SRD + 'Tg1F1PthQWeKdLJT', '1d4', 'Invocar Legiões', fear=1)]}),
            ('Mistério Lendário', 'reaction', P('Existe um mistério em Opartabá que foi perdido junto à sua civilização. Caso os jogadores consigam resolver esse mistério, eles são recompensados com <strong>2 tesouros lendários</strong> à escolha do mestre.') + Q('Que mistério a cidade esconde? Quais tesouros lendários o grupo pode encontrar?'), {'img': 'icons/magic/symbols/question-stone-yellow.webp'}),
        ], page=26, sort=400))
    return out


def link_adv(key, label):
    return f'@UUID[{adv_uuid(key)}]{{{label}}}'


def npc(key, name, short, motives, feats, token, sort=0, dif=None):
    aid = gid('actor', key)
    tok = f'{ASSET}/tokens/{token}.webp'
    items = []
    for i, f in enumerate(feats):
        name_f, form, desc, *rest = f
        opts = rest[0] if rest else {}
        items.append(feature(key, name_f, form, desc, actions=opts.get('actions', ()), effects=opts.get('effects', ()),
                             img=opts.get('img'), sort=(i + 1) * 100))
    doc = {'_id': aid, 'name': name, 'type': 'npc', 'img': tok, 'folder': None, 'sort': sort,
           'system': {'difficulty': dif, 'description': short, 'motives': motives, 'notes': '',
                      'attribution': {'source': SRC, 'page': 11, 'artist': '', 'srd': False}},
           'prototypeToken': prototype_token(name, tok, disposition=1),
           'items': items, 'effects': [], 'flags': {MOD: {'key': key}}}
    return finalize_actor(doc)


def build_npc():
    return [
        npc('aliada-cuca', 'Cuca (Aliada)', P('Uma aliada que sabe cuidar do descanso dos Caçadores de Mitos.'), 'Acolher, Alimentar, Cuidar',
            [('Descanse Bem', 'passive', P('<strong>Gatilho:</strong> os jogadores iniciam um descanso com esta PdM presente.<br><strong>Efeito:</strong> role <strong>1d6</strong>; se rolar 5 ou mais, os jogadores podem fazer um movimento de repouso adicional.'),
              {'img': 'icons/magic/nature/moon-crescent.webp'})], 'aliada-cuca', 100),
        npc('paje-raoni', 'Pajé Raoni', P('Galapa, masc. Líder espiritual dos Ibyrã, o primeiro a perceber e avisar sobre o despertar de Boiúna.'), 'Guiar, Curar, Proteger as tradições',
            [('Cura dos Espíritos', 'passive', P('<strong>Gatilho:</strong> um combate inicia com este PdM presente.<br><strong>Efeito:</strong> inicie uma <strong>Contagem (Ciclo 4)</strong>. Ela diminui sempre que um personagem marca Pontos de Vida. Quando ativada, este PdM faz com que todos os aliados próximos <strong>limpem um Ponto de Vida</strong>.'),
              {'img': 'icons/magic/holy/prayer-hands-glowing-yellow-green.webp',
               'actions': [A.countdown('Cura dos Espíritos (Pajé Raoni)', 4, 'icons/magic/holy/prayer-hands-glowing-yellow-green.webp', looping='looping'),
                           A.heal('Limpar 1 PV dos aliados', 'hitPoints', 1, target='friendly', rng='p')]})], 'paje-raoni', 200),
        npc('tuxaua-caue', 'Tuxaua Cauê', P('Um tuxaua experiente em negociações, que aconselha e orienta os aliados.'), 'Aconselhar, Negociar, Unir os povos',
            [('Mestre das Negociações', 'reaction', P('<strong>Gatilho:</strong> um personagem falha em um teste em uma negociação.<br><strong>Efeito:</strong> mova-se até Corpo a Corpo com o aliado, oferecendo conselhos e orientação. <strong>Uma vez por cena</strong>, o personagem pode rolar o teste novamente.'),
              {'img': 'icons/skills/social/diplomacy-handshake.webp'})], 'tuxaua-caue', 300),
    ]
