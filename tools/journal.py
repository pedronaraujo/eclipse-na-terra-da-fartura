from lib import *
from adversaries import uuid as adv_uuid, link as adv_link
from environments import env_uuid, npc_uuid

ART = f'{ASSET}/art'
UI = f'{ASSET}/ui'


def env_link(key, label):
    return f'@UUID[{env_uuid(key)}]{{{label}}}'


def npc_link(key, label):
    return f'@UUID[{npc_uuid(key)}]{{{label}}}'


def page(entry_key, name, html, sort, ptype='text', src=None, level=1, show=True):
    pid = gid(entry_key, 'page', name)
    d = {'_id': pid, 'name': name, 'type': ptype, 'sort': sort, 'title': {'show': show, 'level': level},
         'image': {}, 'video': {'controls': True, 'volume': 0.5}, 'src': src, 'system': {}, 'flags': {},
         'ownership': {'default': -1}, '_stats': dict(STATS, compendiumSource=None)}
    d['text'] = {'format': 1, 'content': f'<div class="eclipse-page">{html}</div>' if ptype == 'text' else ''}
    if ptype == 'image':
        d['image'] = {'caption': html}
    return d


def entry(key, name, pages, sort=0):
    eid = gid('journal', key)
    for p in pages:
        p['_key'] = f'!journal.pages!{eid}.{p["_id"]}'
    return {'_id': eid, 'name': name, 'pages': pages, 'folder': None, 'sort': sort, 'categories': [],
            'flags': {MOD: {'key': key}}, 'ownership': {'default': 0}, '_stats': dict(STATS, compendiumSource=None),
            '_key': f'!journal!{eid}'}


def P(*ps):
    return ''.join(f'<p>{x}</p>' for x in ps)


def H(t, lvl=2):
    return f'<h{lvl}>{t}</h{lvl}>'


def UL(*items):
    return '<ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'


def QS(*items):
    return '<ul class="eclipse-questions">' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'


def READ(*ps):
    return '<blockquote class="eclipse-read">' + P(*ps) + '</blockquote>'


def BOX(title, html):
    return f'<div class="eclipse-box"><h4>{title}</h4>{html}</div>'


def FIG(img, cls='right', cap=''):
    c = f'<figcaption>{cap}</figcaption>' if cap else ''
    return f'<figure class="eclipse-art {cls}"><img src="{ART}/{img}.webp">{c}</figure>'


def BANNER():
    return f'<figure class="eclipse-banner"><img src="{UI}/titulo-eclipse.webp"></figure>'


def DROP(text):
    """Primeiro parágrafo com capitular."""
    return f'<p class="eclipse-drop">{text}</p>'


PITCH = READ(
    'Terra da Fartura é uma terra de campos fartos e matas exuberantes, onde fé e temor se entrelaçam. Antigamente, as vilas viviam a fartura das colheitas, os rios sinuosos e o calor das fogueiras — mas quando eclipses passaram a tomar o céu, monstros começaram a emergir das sombras para se banquetear. Por gerações, os ritos sagrados dos Ibyrã e a proteção dos Encantados mantiveram as criaturas afastadas, mas, de uns tempos para cá, eclipses têm acontecido de forma antinatural, e os próprios seres que protegiam o povo se viraram contra ele.',
    'Em uma campanha de Terra da Fartura, vocês serão <strong>Caçadores de Mitos</strong> que precisam investigar segredos milenares, enfrentar cismas religiosos e abater criaturas sobrenaturais para proteger seu povo do iminente eclipse eterno.')

PROPOSTA = (BANNER() +
            DROP('Em uma terra onde eclipses tornam os protetores naturais em monstros, Caçadores de Mitos devem descobrir a verdade antes que o eclipse eterno cubra o céu.') +
            P('<em>Criado por Henrique, Pedro, Sena e Zeva.</em>', '<strong>Nível de complexidade:</strong> <span class="eclipse-dots">●●●●</span>') +
            H('Proposta') + P('<em>Leia esta apresentação para os jogadores:</em>') + PITCH +
            '<div class="eclipse-columns">' +
            BOX('Tom & Atmosfera', P('Desesperançoso, Gótico, Heroico, Misterioso, Sinistro.')) +
            BOX('Temas', P('Caçada a Monstros, Defesa contra Colonização, Espiritualidade, Exploração, Fim do Mundo, Narrativas Ancestrais, Fúria da Natureza, Povos Originários, Sobrevivência, Terror.')) +
            BOX('Referências', P('<em>Bloodborne</em>, <em>Dark Heart of Andaluria</em>, Folclore do Brasil, <em>The Witcher</em>, tradição de povos originários brasileiros.')) +
            '</div>')

VISAO = (FIG('mata-emaranhada', 'wide', 'A Mata Emaranhada') + P('<em>Se o grupo optar por este cenário, forneça as informações abaixo antes da criação de personagem.</em>') +
         DROP('Uma terra de horizontes fartos, solo fértil e colheitas que nunca falharam, a Terra da Fartura manteve por muito tempo o caminho para a prosperidade intacto. Antes da Proteção — como ficou conhecido o evento que protegeu o continente de uma invasão —, o continente era um refúgio de calma e alegria, onde a vida seguia um curso natural por dias de sol e paz. Em meio a um ambiente diverso e exuberante, que mistura a pujança da mata e a vastidão dos campos, o povo celebrava o trabalho árduo, as colheitas, o convívio com a natureza com festas acolhedoras, fartura à mesa e uma coletividade e solidariedade entre os povos sem igual. Porém, algo que parecia certo e até inalterável se tornou uma promessa passageira: após o fim da Proteção, eclipses solares começaram a ocorrer de forma recorrente e aleatória, e com isso alteraram a distinta realidade local.') +
         P('Situada em um continente esquecido, a Terra da Fartura é um encontro selvagem e deslumbrante de quatro ecossistemas: a <strong>Mata Emaranhada</strong>, densa e variada, onde vivem os enigmáticos <strong>Caá</strong>; <strong>Vento Raso</strong>, com seus campos, praias e dunas, dos nômades <strong>Itacuí</strong>; <strong>Aguapê</strong>, local de misteriosas águas pantanosas, habitadas pelos corajosos <strong>Tatatinas</strong>; e o <strong>Catingal</strong>, a semiárida e resiliente terra dos guerreiros <strong>Nharana</strong>. Além disso, a Terra da Fartura possui rios sinuosos que cortam estas terras de solo generoso e uma vastidão de antigas e grandiosas cidades subterrâneas e ruínas esquecidas.',
           'Esta terra sempre exigiu e teve o respeito de seus habitantes, os <strong>Ibyrã</strong>, nome coletivo dos povos originários da Terra da Fartura. Suas vilas e aldeias prosperaram em comunhão com a natureza e com os espíritos protetores, enquanto perigos ancestrais permaneciam ocultos nas profundezas da mata e da terra. A profusão de rituais e magia dos povos faz parte do sagrado <strong>Yandê-M’Bae</strong>, religião dos Ibyrã, que possui sua fé enraizada no animismo e em cultos e celebrações em honra à ligação entre vivos, natureza e espiritualidade. Ela pratica o respeito aos <strong>Encantados</strong>, entidades místicas da natureza, que tiveram papel fundamental durante a Proteção contra os <strong>Bandeirolas do Norte</strong>, povo invasor que trouxe guerra ao vir expropriar as riquezas da terra sem se importar com quem vivia nela.',
           'Porém, desde a vitória e a expulsão dos estrangeiros, algo mudou. <strong>Pajé Raoni</strong> (Galapa, masc.), um líder espiritual dos Ibyrã, foi o primeiro a perceber e avisar sobre o despertar de <strong>Boiúna</strong>, uma cobra colossal lendária que jaz dormindo. O fim de seu sono traria catástrofes. As defesas milenares já não serviam mais, e, das sombras, seres da noite conhecidos apenas no folclore começaram a reaparecer. Então vieram os eclipses, antes uma visão rara.',
           'Com eles, os dias que normalmente eram calmos e repletos de festas e ritos começaram a ser afetados pelo fenômeno que ficou conhecido como <strong>Noite ao Meio-Dia</strong>, quando a luz é obscurecida por <strong>Chariã, a Onça Celeste</strong>, uma entidade mística de tamanho cósmico. Essa quebra da ordem natural entre dia e noite atingiu os Encantados, cuja ligação espiritual reflete o estado real da natureza, e os transformou em monstros hostis ao povo desta terra. De seres protetores, passaram a agir nas sombras do eclipse. Como o sol, tiveram sua essência primária devorada e, sem empatia pelo povo, os usam para o próprio prazer e diversão.',
           'A própria sobrevivência da Terra da Fartura vem sendo ameaçada. Com o sol tantas vezes encoberto, a produção de alimentos entrou em crise: a cana-de-açúcar definha nos campos e a cachaça se tornou um artigo raro e cobiçado, enquanto a variedade de cores e alimentos dá lugar ao cultivo de tubérculos como inhame e aipim, além de cogumelos na meia-luz. Diante da escassez, um clima de urgência se apossou dos Ibyrã. Em muitos corações, a fé na comunhão com o mundo deu lugar ao medo e à descrença. Em outros, o desespero virou busca incessante por luxúria e prazer antes do fim. As festas, que antes celebravam a colheita, o fluxo da vida e a gratidão à natureza, agora são usadas para mascarar o desespero do fim do mundo.',
           'Duas delas mostram bem essa mudança: as <strong>Festas Juninas</strong>, que reuniam as aldeias ao redor do fogo, com bandeirinhas coloridas, danças em grupo e comidas abundantes para agradecer fartas colheitas e a bonança do clima, hoje se tornaram um momento tenso de busca por acalanto e nostalgia, com o crescente medo do futuro incerto. Os <strong>Festivais das Fantasias</strong>, que tradicionalmente antecediam a primavera e celebravam a alegria, o amor e a comunidade, se tornaram uma folia frenética e constante. Por trás das fantasias, quem pode come e bebe sem limites, perdendo a sua individualidade cotidiana, para celebrar a vida antes que ela se apague, ou para que ela vá embora de uma vez.',
           'Diante do rompimento da realidade vivida por centenas de anos na Terra da Fartura, tensões políticas e religiosas vêm à tona. Os Bandeirolas do Norte cultuavam o <strong>Deus Sol</strong>, um deus único que dava vida a tudo, e pregavam que eram o seu povo escolhido e que, por isso, os Ibyrã deveriam se curvar. Com as consequências da expulsão dos Bandeirolas do Norte da Terra da Fartura, a religião Yandê-M’Bae passa por um conflito interno, entre aqueles que mantêm suas crenças ancestrais e aqueles que passam a acreditar que a expulsão dos invasores trouxe uma punição do Deus Sol aos Ibyrã. Esse grupo, que antes se via como protetor da terra, hoje se considera insignificante, prega que a vida não tem sentido e se vê como algo que logo se findará.',
           'As crenças ancestrais ainda são mantidas dentro da Yandê-M’Bae, mas o conflito interno está aceso e ardente, influenciando diretamente as relações sociais e políticas do povo Ibyrã. Nesse colapso social e espiritual, as <strong>Criaturas da Noite</strong> se aproveitam dos descrentes e dos tomados pelo medo. Ressurgidas depois de séculos presas nas profundezas, elas passam de antigas histórias e folclores à realidade. Infiltram-se na sociedade e influenciam o povo a se corromper e se entregar às trevas.',
           'Antes e durante a Proteção, muitos migraram de terras longínquas, atraídos principalmente pela divulgação dos Bandeirolas do Norte de que haviam “encontrado” uma terra farta. Os Ibyrã sempre receberam bem os poucos forasteiros que chegavam, desde que houvesse respeito à natureza. Depois da Proteção, porém, muitos que vieram das terras estrangeiras, como trabalhadores e desertores, ficaram. Alguns fundaram vilas novas e outros se misturaram aos Ibyrã. Nesses lugares, o culto ao Deus Sol passou a ser feito à maneira do povo, com ervas, danças e cânticos.',
           'Nem tudo é escuridão e medo. Nas fogueiras das vilas circulam rumores de relíquias perdidas capazes de mudar a situação atual, de entidades espirituais poderosas adormecidas nas profundezas do mundo e de campeões que desafiarão as trevas, como talvez já tenha acontecido no passado. Histórias ainda mais antigas, de antes da paz e da fartura milenares dos Ibyrã, surgem como uma faísca de esperança: falam sobre o povo <strong>Takehó</strong>, uma sociedade que teria enfrentado e expulsado as Criaturas da Noite e criado as proteções que duraram até poucos anos atrás.',
           'Esta terra vasta, abundante e indomável precisa de defensores, e a busca pelo retorno do equilíbrio, ancorada na memória e nas histórias sobre como o povo vivia em comunhão com natureza, espírito e Encantados, é a luz no fim da imensa escuridão que se apresenta. Caberá àqueles que, por obra do destino ou do acaso, se dispuserem a enfrentar a noite, o medo e a corrupção do equilíbrio da vida assumir o papel de <strong>Caçadores de Mitos</strong>: corajosos aventureiros que defendem suas aldeias e vilas com a garra de seu povo, tentando transformar de novo as Criaturas da Noite em Mitos antigos.') +
         READ('Vocês são esses heróis. Entre o calor das fogueiras, o mistério das matas e das águas e o avanço implacável da noite, a jornada se inicia: será possível restaurar o equilíbrio, a exuberância e a fartura desta terra, ou ela sucumbirá de vez às trevas?'))


def COM(nome, texto, *qs):
    return H(nome, 3) + P(texto) + QS(*qs)


COMUNIDADES = (P('Todas as comunidades estão disponíveis, mas algumas têm certas especificidades em uma campanha do Eclipse na Terra da Fartura. Forneça as informações a seguir conforme necessário e escolha uma ou mais perguntas para fazer aos jogadores na sessão zero.') +
    COM('Aristocratas', 'Pessoas oriundas das comunidades aristocráticas costumam ser estrangeiros que vieram em busca de riquezas, ou seus descendentes, uma vez que o povo da Terra da Fartura, antes da chegada dos invasores, não possuía esse tipo de divisão social. Muitos dos estrangeiros aristocratas não se envolveram diretamente na guerra, tendo relações mais tênues com os povos da Terra da Fartura e aceitando de alguma forma, ainda que a contragosto, os costumes e a cultura locais, em troca da possibilidade de se estabelecer e criar pequenas vilas pela Terra da Fartura.',
        'Seu personagem é descendente de estrangeiros que participaram da guerra ou que criaram boas relações com os povos Ibyrã? Ou seu personagem é um estrangeiro que veio a esta terra em busca de tesouros?',
        'O que a comunidade espera do seu personagem? Ele ainda mantém relações de hierarquia social como os membros da comunidade?') +
    COM('Desértica', 'Localizados principalmente nas dunas de Vento Raso ou na região semiárida do Catingal, essa comunidade é feita por guerreiros que defenderam o território durante a Proteção. Apesar de ser repleto de dunas, o ambiente de Vento Raso se enche de lagoas de água doce durante períodos de chuvas, o que permite que os Ibyrã prosperem em um local que normalmente seria inóspito. Já no semiárido do Catingal, os povos possuíam um profundo conhecimento ecológico e usam estratégias ancestrais de adaptação, envolvendo uso de plantas, mudança de locais a cada época, conhecimento dos sinais da natureza e conservação do solo.',
        'Seu personagem apoiou a expulsão dos Bandeirolas do Norte, feita principalmente pelos Nharana e pelos Itacuí? Ele acredita que foi a decisão certa para preservar a Terra da Fartura?',
        'Como é a relação do seu personagem com os Nharana ou os Itacuí? Como eles moldaram a personalidade do seu personagem?') +
    COM('Disciplinada', 'Algumas comunidades Ibyrã costumam ter regras bem estabelecidas e mantêm, há centenas de anos, ritos e cuidados com a natureza. Em geral, sua hierarquia se baseia no respeito aos mais velhos, e consideram sua sabedoria como leis que regem sua lógica de funcionamento. Todos os membros da comunidade mantêm rígidas obrigações de cuidado com a natureza.',
        'Que lugar seu personagem ocupa na hierarquia da sua comunidade? Seu personagem enxerga a disciplina conduzida pelos mais velhos como sabedoria ancestral ou como algo antiquado?',
        'Quais são (ou eram) as obrigações de cuidar da natureza do seu personagem?') +
    COM('Erudita', 'O respeito aos ancestrais é algo vital na Terra da Fartura, graças à sabedoria dos anciões. No continente, o conhecimento passa de geração em geração sobretudo de forma oral, por meio de histórias, contos, poesias e provérbios que falam dos acontecimentos do passado e do que se aprendeu com eles. É essencial que cada vila e aldeia tenha pelo menos uma pessoa que possua os conhecimentos ancestrais.',
        'Com que tipos de conhecimento seu personagem tem mais afinidade? Ou ele é um sabe-tudo?',
        'Com quem seu personagem aprendeu isso? Qual foi a importância dessa pessoa para ele?') +
    COM('Fora da Lei', 'Embora os povos Ibyrã sejam conectados e coesos, alguns preferem o caminho fácil. Essas pessoas formam as comunidades Fora da Lei, seja por estarem ligadas à exploração ilegal das riquezas do continente, seja por terem se desiludido com a fé Yandê-M’Bae. Esse tipo de comunidade tem crescido com o advento da Noite ao Meio-Dia. Com o fim dos tempos se aproximando, muitos já não se importam nem com o futuro próximo, pois o presente é tudo o que lhes resta.',
        'O que fez seu personagem se desconectar da natureza, da religião ou do resto dos Ibyrã? Como isso o afetou?',
        'Quais pequenos crimes seu personagem comete para sobreviver? Como os outros o veem por causa disso?') +
    COM('Glacial e Montanhesa', 'Personagens dessas comunidades consistem basicamente de forasteiros. Não existem cadeias de montanhas nem áreas de neve na Terra da Fartura. Porém, ao extremo oeste, depois das fronteiras da Terra da Fartura, existe uma cadeia de montanhas onde a maioria dos rios do continente nasce. São locais ermos e inóspitos, mas existem aqueles loucos o suficiente para chamar esses locais de lar.',
        'Seu personagem veio de um local onde já conhecia os Ibyrã? Por que ele saiu do seu lar para vir à Terra da Fartura?',
        'A cultura de lá era próxima ou distinta da cultura da Terra da Fartura? Qual foi a principal diferença entre a cultura do seu personagem e a dos Ibyrã? E qual foi a maior semelhança?') +
    COM('Livre', 'A comunidade Livre é formada sobretudo por povos que foram presos e escravizados pelos Bandeirolas do Norte logo no início da invasão e libertados durante e após a Proteção. A revolta dessas pessoas e a mobilização dos outros povos para libertar seus irmãos foram essenciais para a vitória. Apesar de curta, a violência que sofreram marcou suas vidas e as de seus descendentes, e a presença dos estrangeiros mudou a dinâmica da população desses lugares.',
        'Quais hábitos dos Bandeirolas do Norte seu personagem acabou absorvendo, mesmo depois da libertação? Como ele é visto pelas outras comunidades por causa disso?',
        'Como seu personagem vê os descendentes dos Bandeirolas e os habitantes vindos de suas terras que ficaram na Terra da Fartura?') +
    COM('Marítima', 'Graças ao extenso litoral da Terra da Fartura, essa comunidade está muito presente no continente. Alguns de seus membros se aventuram nos mares, e outros vivem à beira dos inúmeros rios que cortam a terra. Alguns desses rios chegam a ter milhares de quilômetros de extensão e dezenas de quilômetros de largura, se tornando parte essencial do ambiente, tanto para alimentação quanto para deslocamento.',
        'Como as águas fazem parte do cotidiano do seu personagem? Qual é a ligação dele com a navegação, a pesca e os Encantados das águas?',
        'Seu personagem é de uma comunidade ribeirinha ou praiana? Como viver nela moldou a personalidade dele?') +
    COM('Silvestre', 'As comunidades Silvestres são fortemente conectadas aos princípios da religião Yandê-M’Bae, mantêm uma relação ainda mais forte com a natureza e pregam a necessidade de viver em harmonia com a terra. Muitos ainda têm fé nos Encantados e acreditam que a transformação deles seja passageira e que a falta de fé e de ligação com eles trará algo ainda pior para o povo da Terra da Fartura.',
        'Algum Encantado era protetor da região da comunidade do seu personagem? Se sim, como a transformação dele afetou o povo?',
        'Qual é a posição da comunidade do seu personagem sobre a chegada dos seguidores do Deus Sol? Como o povo reagiu durante a Proteção?'))

ANCESTRALIDADES = (P('Todas as ancestralidades estão disponíveis, mas algumas têm certas especificidades em uma campanha do Eclipse na Terra da Fartura. Forneça as informações a seguir conforme necessário.') +
    H('Clanks', 3) + P('Os Clanks são feitos de uma mistura de metais, pedras e madeiras muito bem tratadas. Essas criaturas servem de receptáculo para espíritos da natureza e têm forte ligação com Encantados, Druidas e Bruxos.') +
    H('Elfos', 3) + P('Os elfos da Terra da Fartura têm traços físicos que imitam a flora da Mata Emaranhada e trazem pequenas bromélias, samambaias e orquídeas em meio aos cabelos e barbas.') +
    H('Galapas, Kataris, Quachos e Símios', 3) + P('Na Terra da Fartura, essas ancestralidades costumam ter aparência semelhante à de animais típicos da região. Os Kataris têm pelagem amarelo-dourada com manchas pretas em forma de roseta, e cada um tem um padrão único. Os Símios geralmente não são muito grandes e têm pelagens variadas, do preto ao dourado intenso. Os Galapas costumam ter cores vivas e formatos incomuns, como pescoço alongado ou protuberâncias no queixo que lembram uma barba, e variam muito de tamanho. Já os Quachos são os mais diversos: suas cores vivas e as manchas pelo corpo lhes dão camuflagens variadas, e é praticamente impossível encontrar dois indivíduos parecidos entre si, mesmo entre parentes.') +
    H('Herdeiros Elementais', 3) + P('Os Herdeiros Elementais são numerosos, têm uma ligação muito forte com os antepassados dos Ibyrã e são vistos como abençoados pelos espíritos que protegem a terra. No passado, cada grupo era mais numeroso em um território: os Herdeiros da Terra na Mata Emaranhada, os do Fogo no Catingal, os do Ar em Vento Raso e os da Água em Aguapê. Hoje vivem espalhados, sendo muito comuns as ancestralidades mistas que carregam alguma dessas heranças.') +
    H('Infernis', 3) + P('Vistos por muitos como filhos do Eclipse, os Infernis sofrem muito preconceito na Terra da Fartura. Apesar disso, seguidores mais empáticos da Yandê-M’Bae acreditam que eles fazem parte da natureza, como todo ser vivo.'))

CLASSES = (FIG('cuca', 'right') + P('Todas as classes estão disponíveis, mas algumas têm certas especificidades em uma campanha do Eclipse na Terra da Fartura. Forneça as informações a seguir conforme necessário.') +
    H('Bardos', 3) + P('Os bardos sempre foram amados em toda a Terra da Fartura pela tradição de contar às novas gerações as histórias e o folclore antigos. Porém, com o advento da Noite ao Meio-Dia, passaram a ser os detentores das histórias dos monstros e das Criaturas da Noite e, para alguns, até os responsáveis por criá-los.') +
    H('Bruxos', 3) + P('A cultura dos bruxos como benzedeiros e pessoas muito sábias perdura até hoje. Com o fim dos tempos cada vez mais próximo, eles são procurados para dar orientação e conselhos sobre situações difíceis que passaram a ser cotidianas depois da Noite ao Meio-Dia.') +
    H('Druidas', 3) + P('Desde os primórdios da Terra da Fartura, os druidas foram essenciais para manter o contato constante entre os mortais e a natureza. A Noite ao Meio-Dia abalou essa conexão, e muitos druidas viram sua importância questionada pela sociedade. Hoje se dividem entre ser vistos como uma possível salvação e como aqueles que erraram ao conduzir o povo ao longo do tempo.') +
    H('Guardiões e Patrulheiros', 3) + P('Guardiões e Patrulheiros sempre foram parte de qualquer vila ou aldeia, como protetores e caçadores. Com a chegada dos Bandeirolas do Norte, assumiram um papel de destaque na Proteção, pois era preciso aumentar o número de pessoas treinadas para defender aquilo que amam e caçar aqueles que queriam mudar a vida da Terra da Fartura. Sempre trabalharam juntos para que os Ibyrã pudessem viver em paz, sem se preocupar com ameaças externas. Agora que a maior ameaça vem da própria natureza do continente, a proteção da população precisa ser redobrada nas comunidades, e a importância deles na cultura Ibyrã cresce ainda mais.') +
    H('Ocultistas', 3) + P('Existem dois tipos de pactuados na Terra da Fartura: os que fazem pactos com Encantados e os que fazem pactos com Criaturas da Noite. Os Encantados, apesar da mudança que sofreram com a Noite ao Meio-Dia, continuam presentes, têm poderes inimagináveis para os mortais e podem oferecer pactos a quem for corajoso o bastante para se tornar seu pactuado. As Criaturas da Noite costumam se mover apenas por instinto, mas algumas são inteligentes e poderosas o bastante para firmar pactos com mortais. Como pouco se sabe sobre os pactos feitos pelos ocultistas, a população os vê com maus olhos e como sinal de que as Criaturas da Noite estão chegando.'))

PRINC_JOG = (P('<em>Se o grupo optar por esta campanha, forneça as informações abaixo antes da criação de personagem.</em>') +
    H('Valorize a Caçada', 3) + P('Encontrar e eliminar as criaturas o mais rápido possível ajuda a reduzir as baixas, mas, se isso for feito sem o devido preparo, pode significar uma corrida rumo à própria morte. Reunir pistas e descobrir a fraqueza das Criaturas da Noite é tão importante quanto a batalha.') +
    H('O Coletivo Acima do Indivíduo', 3) + P('Sair sozinho pelas ruas das diversas cidades e vilarejos durante um eclipse é assinar a própria sentença de morte. Valorizar o grupo como uma unidade é essencial para sobreviver a uma caçada com o menor número de mortes possível.') +
    H('Respeite as Tradições', 3) + P('Apesar de a Noite ao Meio-Dia ter abalado a relação entre mortais e natureza, a Terra da Fartura ainda é um lugar repleto de tradição e cultura. Desrespeitar a cultura é tão grave quanto sofrer o ataque de uma Criatura da Noite. Nesse cenário, a cultura dos povos originários, a relação com a natureza e a noção de comunidade e solidariedade são os pilares do bem e da esperança. Seu personagem não precisa seguir esses pilares; a dualidade é parte fundamental do jogo. Pense em como ele se relaciona com as tradições: quais são importantes para ele e por quê? Como ele se relaciona atualmente com esses pilares?') +
    H('Abrace o Monstro Dentro de Você', 3) + P('A luta contra as Criaturas da Noite não é fácil: a cada dia que passa, muitos Caçadores de Mitos morrem ou ficam incapazes de continuar seu trabalho. Raramente uma caçada pode ser resolvida na conversa, então os Caçadores de Mitos podem e devem fazer tudo o que estiver ao seu alcance para proteger os seus. Mas o custo pode ser alto: alguns se transformam e perdem partes importantes do seu eu.'))

PRINC_MES = (P('<em>Ao mestrar esta campanha, lembre-se das seguintes orientações.</em>') +
    H('O Mundo está Acabando', 3) + P('A chegada da Noite ao Meio-Dia é vista por grande parte da população como o anúncio do fim dos tempos. O povo da Terra da Fartura deve parecer desesperançoso, desesperado e, às vezes, até louco. Os ritos, as festas e os festivais mudaram e ficaram mais sombrios. Mostre a sociedade caminhando aos poucos para o colapso. Ao mesmo tempo, mantenha um fio de esperança a que os jogadores possam se agarrar: alguns poucos ainda se apegam às ancestralidades e às tradições e tentam mudar os rumos da história.') +
    H('Mantenha o Mal em Ação', 3) + P('As forças malignas na Terra da Fartura nunca dormem. Estão sempre em busca de seu objetivo, seja a destruição de uma cidade, de um bioma ou de um continente, a dominação total ou até mesmo o fim dos tempos, e agem pelas sombras. O mundo segue em movimento independentemente dos jogadores, mas sempre em torno deles, como protagonistas da história.') +
    H('Recompense a Criatividade', 3) + P('Monstros e Criaturas da Noite não devem ter uma única maneira de serem derrotados. Use e recompense a criatividade dos jogadores quando encontrarem maneiras diferentes e plausíveis de derrotar aquilo que estão caçando. Da mesma forma, recompense ideias criativas na busca por informações e pistas, mesmo que estejam fora do seu planejamento inicial. A história pode e deve ser construída por todos — não se prenda a predefinições. Lembre-se de que as predefinições podem ser melhoradas ou alteradas quando encontram as ações e os pensamentos dos jogadores.') +
    H('Traduza o Medo em Realidade', 3) + P('O medo é natural para os mortais, e um dos maiores é o medo do desconhecido. Vultos se movendo ao longe, vozes e gritos ecoando, marcas da presença das Criaturas da Noite: lembre-se de mostrar sempre aos jogadores que, durante um eclipse, eles nunca estarão seguros.'))

SESSAO_ZERO = (P('Faça as perguntas abaixo para os jogadores ou crie as suas.') + QS(
    'Onde você estava e o que estava fazendo na primeira vez que testemunhou os efeitos da Noite ao Meio-Dia? O que aconteceu neste dia que seu personagem nunca irá esquecer?',
    'Um lugar que seu personagem conhece mudou drasticamente após a chegada dos Bandeirolas do Norte e das batalhas da Proteção. Como ele era antes e o que a chegada deste povo estrangeiro mudou nele?',
    'Qual é a posição do seu personagem quanto às crenças da Yandê-M’Bae e dos cultuadores do Deus Sol?',
    'Qual é a relação do seu personagem com a espiritualidade Ibyrã? Como ele vê os Encantados? O que mudou na forma como ele se relaciona com tudo isso com o advento da Noite ao Meio-Dia?',
    'Em quais crendices e superstições seu personagem acredita?'))

BIOMAS = (P('<em>Use estas informações para preparar a campanha. Você também pode compartilhá-las com o grupo se for necessário.</em>') +
    H('Vento Raso e os Itacuí', 3) + P('Dividida entre campos de gramíneas douradas, onde árvores de troncos retorcidos guardam segredos antigos em suas grossas cascas, áreas repletas de animais perigosos e dunas douradas coroadas por lagoas cíclicas de águas cristalinas que cercam as praias do Norte, Vento Raso é o local que abriga o povo Itacuí. Nômades, os Itacuí viviam viajando das praias aos campos, atravessando as dunas nas épocas de chuva, quando surgem as <strong>Coroas Cristalinas</strong>, nome dado às lagoas que se formam entre elas nesses períodos.',
      'Atualmente, a região dos campos tem se tornado perigosa: a morte da vegetação rasteira, causada pela falta de sol, soma-se à diminuição das chuvas na região, formando campos secos onde os tão desejados momentos de sol se tornam cruéis, dando início a incêndios naturais destrutivos e contínuos que duram dias a fio. Por isso, o povo Itacuí tem criado vilas fixas perto das águas, seja nas praias do norte, seja à beira dos rios que ainda cortam a região. O povo nômade vem mudando sua cultura milenar para tentar sobreviver. Ao criar personagens ou aventuras relacionados a esta região e aos Itacuí, pense em como essa mudança forçada de costumes e cultura os tem afetado.') +
    H('Aguapê e os Tatatinas', 3) + P('Ao sul, a mata fica mais esparsa e dá lugar a uma enorme planície alagável. Com ciclos bem definidos de cheias e vazantes, o pântano ora fervilhava de vida, ora ficava envolto em brumas. Nessa região perigosa se estabeleceu o corajoso povo Tatatina, que aprendeu a entender os ciclos das águas e a navegar pelas brumas espalhadas por todo o território. Os Tatatinas tiveram um contato profundo com os animais da região, assim como com os Encantados. Antes da Noite ao Meio-Dia, seu conhecimento sobre eles era tamanho que até os mais jovens conseguiam acalmar uma onça ao encontrá-la vagando pela mata. Foram eles, principalmente, que conquistaram o apoio dos Encantados durante a Proteção.',
      'Atualmente, os Tatatinas enfrentam uma das piores situações entre os povos: as mudanças nos ciclos das águas e nos Encantados fizeram boa parte de seus conhecimentos perder utilidade. Precisam lidar com a rápida morte da imensa maioria dos animais e, com isso, com a poluição das águas. Além disso, o fortalecimento das brumas traz sons sinistros, que lembram os gritos dos mortos e trazem medo à população.') +
    H('Catingal e os Nharana', 3) + P('Uma região semiárida se espalha pelo nordeste da Terra da Fartura. A vastidão desse território deixaria desavisados em desespero, mas não os Nharana, o povo que ali vive. Conhecedores da região, aprenderam a rastrear água em tempos de seca, a usar cactos e outras plantas como alimento constante e a caçar animais adaptados à aridez. A resiliência dessa terra tornou os Nharana igualmente resilientes e os fez os maiores guerreiros entre os Ibyrã. Foram um grande problema para os Bandeirolas do Norte durante a invasão, pois sua bravura, sua habilidade e seu conhecimento do terreno logo colocaram os invasores em situações difíceis.',
      'Atualmente, a seca e o calor intenso típicos da região dão lugar à escuridão fria e a ciclos de chuva decorrentes das mudanças nas massas de ar, alteradas pelo frio. Nevoeiros densos, orvalhos pesados e até garoas estagnadas passam a surpreender a região nos momentos de escuridão prolongada.',
      'Os Nharana vêm transformando sua resiliência milenar em criatividade para sobreviver às grandes mudanças de temperatura, entre os momentos de sol forte e os temporais gélidos da Noite ao Meio-Dia. Acostumados ao calor árido do Catingal, reinventaram a caça e o cultivo diante da escuridão, converteram o fogo em um bem precioso contra as geadas e uniram forças para erguer vilas maiores, destacando-se como destemidos Caçadores de Mitos na luta contra a escuridão.') +
    H('Mata Emaranhada e os Caá', 3) + FIG('mata-emaranhada', 'right') + P('No noroeste, uma mata densa se estende até o horizonte. Árvores milenares, de copas fechadas a dezenas de metros do chão, abrigam uma enorme variedade de animais e plantas. Ali vivem os enigmáticos Caá, com vilas e aldeias construídas em comunhão com a mata, em belas casas nas árvores erguidas como se fossem parte da própria floresta. São os mais antigos entre os povos Ibyrã a construir comunidade e cultura, e também os mais isolados. Dizem que guardam histórias sobre o passado que os outros povos desconhecem e que assumiram o dever de proteger as <strong>Ruínas Proibidas</strong>. Em geral, falam pouco — acreditam que as palavras têm poder e por isso as usam com cautela; na maior parte do tempo, se comunicam por sinais, onomatopeias e imitações dos animais.',
      'Atualmente, a Mata Emaranhada está em colapso, impulsionado pela quebra drástica da fotossíntese e pelo desarranjo total da cadeia alimentar que antes a mantinha viva e pulsante. As plantas do sub-bosque definham rapidamente. A umidade sufocante e a falta do calor do sol começam a formar uma névoa pesada, fria e estagnada entre as árvores de algumas regiões. Fungos e parasitas proliferam de forma anômala, e os animais, desnorteados com as janelas de caça alteradas, deixam as profundezas da mata num silêncio ensurdecedor.',
      'Os Caá vêm adaptando seu modo de vida: erguem as casas ainda mais alto nas árvores e as conectam com pontes pênseis de madeira, porque o chão, cada vez mais encharcado e tóxico, deixou de ser caminho seguro para quem vive na mata. Esses moradores também criam, com magia e conhecimentos naturais, formas de se deslocar entre as copas. Com a perda dos cultivos tradicionais, passam a viver em busca de fungos e plantas adaptados à escuridão prolongada e caçam os predadores que, descontrolados, são ao mesmo tempo um perigo e uma solução para a fome. Em tempos de eclipse, a Mata Emaranhada vira um lugar de silêncio pavoroso, que dói aos ouvidos de quem sabe que ele nasce do esgotamento dos recursos.'))

DISTINCOES = (
    H('Reinos Perdidos e a Onça Celeste', 3) + P('Por gerações, os anciões alertaram o povo Ibyrã sobre a importância do antigo povo <strong>Takehó</strong>, que protegeu a terra de Chariã e das Criaturas da Noite e se sacrificou para aprisioná-las em locais que os Ibyrã chamavam de <strong>Ruínas Proibidas</strong>. Durante séculos, os Ibyrã se mantiveram distantes desses lugares, por acreditarem que se aproximar deles traria mau agouro e consequências sombrias. Esse equilíbrio acabou com a chegada dos Bandeirolas do Norte. Cegos pela ganância por ouro e prata, eles avançaram sobre as Ruínas Proibidas, ignorando as tradições sagradas com a arrogância de sua própria ambição.',
      'As civilizações antigas, esquecidas nas ruínas sob a Terra da Fartura, abrigavam os resquícios de cidades exuberantes, outrora iluminadas por imensas construções banhadas a ouro e prata. O povo Takehó se ergueu e prosperou nessas terras antes dos Ibyrã. Esse povo enfrentou um antigo espírito primordial maligno conhecido como <strong>Chariã, a Onça Celeste</strong> — um ser que dava origem às Criaturas da Noite e que, por milhares de anos, caçou o Sol e a Lua, tentando devorá-los para instaurar no mundo uma noite sem fim. De alguma forma, os precursores dos Ibyrã impediram esse espírito, selando o mal nas profundezas de suas cidades. O custo foi alto: a civilização Takehó caiu, e seus poucos sobreviventes se espalharam pelo continente e deram origem aos Ibyrã.') +
    H('O Início', 3) + P('<strong>Fernão Noite Filho</strong> (Katari, masc.), <strong>Sábado Jorge Novo</strong> (Galapa, masc.), <strong>Tonhão Raposa</strong> (Humano, masc.) e <strong>Bartô Maleño Selva</strong> (Infernis, masc.), líderes dos Bandeirolas do Norte, comandaram uma expedição mata adentro durante a <strong>Batalha do Fim</strong>, na qual os Ibyrã finalmente derrotaram e expulsaram os invasores. O grupo havia abandonado as tropas antes mesmo da batalha: via a derrota como certa e queria aproveitar a mobilização dos Ibyrã para buscar tesouros escondidos. Os quatro entraram nas profundezas da Mata Emaranhada para alcançar e pilhar as ruínas de <strong>Opartabá</strong>, passaram por lugares proibidos pelo povo daquela terra e avançaram pelo interior de gigantescas construções subterrâneas banhadas a ouro e prata. O que encontraram ali foi algo muito maior do que a riqueza que buscavam. De alguma forma desconhecida, perturbaram o sono de Boiúna e libertaram Chariã, a Onça Celeste, cujo espírito engoliu os invasores e os cuspiu de volta, transformando aqueles que o haviam libertado em Criaturas da Noite.',
      'Nesse dia teve início a Noite ao Meio-Dia. A Onça Celeste, agora mais insaciável do que nunca, movida pelo ódio e pela amargura de ter ficado presa por séculos, avança sobre o Sol na tentativa de trazer à Terra da Fartura o <strong>Eclipse Eterno</strong>. Os líderes dos Bandeirolas do Norte, agora transformados em servos de Chariã, infiltram-se na sociedade dos Ibyrã, corrompem os desacreditados, alimentam-se daqueles que ainda guardam esperança e transformam a Terra da Fartura em uma terra de medo e descrença.') +
    H('Noite ao Meio-Dia', 3) + FIG('eclipse', 'left') + P('Logo após o fim da Proteção, ainda quando comemoravam a vitória e limpavam as feridas, o sol brilhava a pino em um céu azulado quando uma sombra escureceu os céus e engoliu o Sol. Os pássaros pararam de cantar e os cachorros começaram a uivar; o povo Ibyrã, acostumado a iniciar cantos e batidas cerimoniais nos raros eclipses que aconteciam, sentiu um frio na espinha e silenciou-se. Um eclipse havia iniciado, mas com um ar diferente e, ao contrário dos outros, durou horas. O fenômeno passou, mas voltou poucos dias depois e se repetiu, de novo e de novo. Ora por horas, ora por dias, sem ciclo definido e sem aviso. A Noite ao Meio-Dia simplesmente acontece. Com o passar dos dias, consequências à vida comum passaram a acontecer. A produção de alimentos, antes farta e fácil, ficou complexa e limitada, assim como a convivência com os animais e Encantados; a Terra da Fartura entrou numa crise sem precedentes.',
      'A natureza começou a mudar. O calor e as chuvas típicos da Terra da Fartura passaram a se alternar com períodos de seca e quedas bruscas de temperatura. Muitos animais entraram em crise com a alteração dos dias e das noites. Os predadores noturnos se adaptaram bem à escuridão, mas sofreram com a escassez de alimento. Os insetos, importantes para a polinização, ficaram desorientados durante os intervalos de Noite ao Meio-Dia, o que desequilibrou o meio ambiente.',
      'Em Vento Raso, a vegetação rasteira morreu depois de longos eclipses, e o sol, ao voltar, passou a provocar incêndios sobre a vegetação seca. No Catingal, que sempre resistiu ao calor e à seca, temperaturas muito abaixo do normal estão transformando a biodiversidade. Aguapê, que depende de um ciclo regular de enchentes e vazantes, sofreu as consequências mais bruscas: com a dinâmica das águas desregulada, os peixes morreram em vazantes que ocorrem em momentos inesperados, e as aves do local e outros animais que dependiam desses ciclos morreram rapidamente de fome. Com isso, a região vai se tornando cinzenta e tóxica, por causa dos inúmeros animais mortos.',
      'Ao descrever os biomas da Terra da Fartura, pense no efeito devastador que os longos intervalos de escuridão têm causado ao meio ambiente. Os ciclos de vida desta terra foram interrompidos, e o equilíbrio entre as regiões deu lugar a um caos imprevisível. A Noite ao Meio-Dia pode ocorrer por dias seguidos, com ou sem intervalos com sol. Pode também, às vezes, cessar por alguns dias: uma semana com dias comuns dá espaço para a natureza tentar se regular, porém, a cada tempo que passa, essas pausas parecem se tornar mais raras.'))

YANDE = (P('Considerada a religião mais antiga de toda a Terra da Fartura, a Yandê-M’Bae reúne uma grande comunidade com influência religiosa e política sobre os Ibyrã. Seu nome significa <strong>“nós somos uma coisa”</strong>, expressão de unidade e comunidade em que todos são um perante a natureza. Não existe uma figura religiosa centralizada: cada comunidade tem seu <strong>Pajé</strong>, líder espiritual, guia e curandeiro. Muitas vezes o Pajé também é o líder político do local, pelo grande respeito que os Ibyrã têm por ele.',
           'A religião se baseia no animismo e no xamanismo. O animismo é a crença de que elementos da natureza, como animais, plantas, rochas e fenômenos naturais, possuem uma essência espiritual ou alma, e todos são dignos da vida e da morte. O xamanismo é um conjunto de práticas e rituais espirituais ancestrais que busca a conexão com o sagrado, a natureza e o mundo espiritual. O Pajé é o único autorizado a conduzir os rituais mais importantes de uma comunidade, e cada Pajé é escolhido não pelo povo, mas por suas próprias escolhas.') +
    H('Advento da Noite ao Meio-Dia', 3) + P('Duas vertentes da Yandê-M’Bae surgiram depois do advento da Noite ao Meio-Dia. Os que se mantiveram fiéis às suas origens continuaram com um sentimento de comunidade ainda maior, em que um não tinha como sobreviver sem o outro. Já os que perderam as esperanças mudaram o significado do nome: Yandê-M’Bae passou a significar <strong>“nós somos apenas uma coisa”</strong>, uma pedra no caminho das Criaturas da Noite, à espera da morte. Seus ritos se tornaram macabros e passaram a significar a espera da morte. Isso também fez muitas superstições se tornarem reais para as pessoas, de tanto que acreditavam nelas. Alguns exemplos: o calçado virado adoece a mãe; quebrar um espelho ou ver um gato preto dá azar por anos; bater na madeira evita que algo dito em voz alta realmente aconteça; e muitos outros.') +
    H('Ritos', 3) + P('Os ritos das comunidades Yandê-M’Bae são tão diversos quanto a própria natureza. Há ritos de passagem da infância para a vida adulta, de invocações, de fortalecimento da identidade coletiva e, principalmente, de despedida dos mortos. Todos seguem práticas como o uso de ervas, danças e cânticos, mas cada Pajé e sua comunidade têm liberdade para coordenar o rito de modo a criar a maior conexão possível.') +
    H('Conexão com a Natureza', 3) + P('Conectar-se com a natureza sempre foi central no modo de vida da religião Yandê-M’Bae, e isso passa por se reconhecer como parte dela. Viver bem, para eles, é estar em equilíbrio com o meio ambiente: entender que respirar depende do sopro do vento na floresta, que cortar uma única árvore afeta uma infinidade de ciclos ao redor e que a natureza prospera pela cooperação mútua entre os seres vivos.',
      'O ritmo da vida é o ritmo da terra. Colhe-se o necessário para comer e cuida-se da terra para que ela possa se alimentar no futuro. Ao caçar, agradece-se pela vida que o animal deu, e nunca se caça sem necessidade. Construir uma casa significa entender como ela afetará a vida ao redor: o rio que passa perto, os pássaros que dormem nas árvores ao lado e assim por diante.',
      'Para quem vive assim, a magia vem da própria conexão com a natureza. É a capacidade de controlar a energia vital para transformá-la em algo diferente, sempre com o respeito e o cuidado que essa energia merece. Estar profundamente em contato com a natureza é perceber que se é a própria natureza. Esse pensamento vai se tornando parte da identidade de cada um, e o ritmo de vida, as ações e as reações passam a se basear nessa cosmovisão.',
      'Foi essa forma de vida que levou os Ibyrã a construir a Terra da Fartura. Hoje ela está sob desconfiança e em risco: alguns a acusam de ser a causa da situação atual, enquanto outros esperam que seja a solução para pôr fim à Noite ao Meio-Dia.') +
    H('Senso de Comunidade', 3) + P('A irmandade e a solidariedade entre os Yandê-M’Bae são tão importantes quanto qualquer rito ou a conexão com a natureza. A ideia de que todos são parte de uma só coisa é o que fez os Yandê-M’Bae sobreviverem por tanto tempo, até em situações tão drásticas quanto a Noite ao Meio-Dia. Deixar um irmão para trás é um crime tão grave quanto matar um animal ou cortar uma árvore sem motivo, por puro lazer.'))

CRIATURAS = (H('Criaturas da Noite', 3) + P('O termo Criaturas da Noite abrange todo monstro que sai durante as noites e os eclipses para caçar, destruir e conquistar. O que as diferencia dos monstros comuns é um sexto sentido que as avisa da chegada dos eclipses, algo que os Ibyrã ainda não conseguiram entender nem reproduzir, apesar de muito esforço.',
      'Sua ligação com Chariã parece lhes dar poderes que, de outra forma, não teriam. Um encontro com uma Criatura da Noite quase sempre termina em chacina ou em algo ainda pior.') +
    H('Encantados ou Monstros?', 3) + P('Um elemento central do cenário Eclipse são os Encantados, criaturas místicas intimamente ligadas à natureza, que nasceram para protegê-la e sempre foram parte essencial do equilíbrio da Terra da Fartura. Os povos Ibyrã sempre tiveram com eles uma relação de benefício mútuo, mas, com o advento da Noite ao Meio-Dia, esse vínculo se rompeu quase por completo. Os Encantados se tornaram hostis e se afastaram dos Ibyrã, e muitos acreditam que se juntaram a Chariã e às Criaturas da Noite.',
      'Pouco se sabe sobre o que realmente aconteceu com os Encantados, e menos ainda são os que estão dispostos a se arriscar para descobrir.') +
    H('Transformações na Terra da Fartura', 3) + P('Pessoas que se assemelham às Criaturas da Noite, mesmo conscientes de seus atos, são alvo da mesma aversão que as próprias criaturas. O medo é que, a qualquer momento, percam o controle e causem uma chacina.') +
    H('Ruínas Antigas', 3) + P('As Ruínas Antigas, escondidas sob a Terra da Fartura, eram até recentemente proibidas pela cultura Ibyrã e agora se tornaram um lugar de busca e pesquisa sobre os acontecimentos recentes. Ao contrário dos Bandeirolas, movidos pela ganância, parte dos Ibyrã ainda cultiva a esperança de que a paz e a prosperidade voltem à terra, e eles buscam nas ruínas os antigos conhecimentos perdidos do povo Takehó, que viveu há séculos e teria combatido as Criaturas da Noite e aprisionado Chariã.'))

INCIDENTE = (P('<em>Você pode começar a campanha usando o modelo abaixo ou criar o seu.</em>') +
    READ('Sanfonas e tambores ecoam pelas areias de Vento Raso. No vilarejo de <strong>Inara</strong>, a Festa Junina cheira a melaço queimado, cachaça forte de inhame e fumaça de madeira seca. Ao redor das fogueiras da praça, o povo dança até o suor escorrer. Os rostos sorriem rápido demais, e ninguém olha para o céu. Antes, a festa agradecia à terra fértil. Agora serve para abafar o medo. Todos bebem e dançam como se o amanhã não fosse chegar.',
         'É meio-dia. O sol deveria estar no alto, brilhando nas lagoas entre as dunas. Mas um arrepio atravessa a vila, e os pássaros se calam. A cantoria morre aos poucos e o silêncio cai sobre a praça. No céu, uma sombra colossal engole o Sol: Chariã, a Onça Celeste, estende mais uma vez as garras sobre o mundo. As chamas das fogueiras vacilam, como se até o fogo quisesse ir embora. Antes que alguém grite, a escuridão é total.',
         'Então começam os gritos. Vultos enormes cortam a luz fraca das brasas. Gente cai e não se levanta. Os vultos agarram dezenas de pessoas e as arrastam, ainda gritando, para o escuro das dunas. Os gritos somem antes que alguém consiga reagir. Vocês estão no meio da praça, entre corpos que correm sem direção, e o ataque é mais rápido do que qualquer um esperava.',
         'Tão de repente quanto veio, o eclipse recua. Uma luz cinzenta volta à vila e mostra o estrago: barracas rasgadas, tambores furados, sangue sobre a areia. Parte do povo morreu. Outros desapareceram. Os sobreviventes ficam parados, sem choro e sem fala. Sabem que vai acontecer de novo e não sabem quando.',
         'No centro da praça, a maior fogueira virou carvão, e uma fumaça branca sobe das cinzas. Marcas de arrasto vão da praça até as dunas. Algo antigo, distorcido pela Noite ao Meio-Dia, está por trás do massacre. Cabe a vocês descobrir o que atacou a vila, para onde levaram os desaparecidos, se ainda estiverem vivos, e caçar essa ameaça antes que a escuridão acabe com este povo.') +
    BOX('Dica para o mestre', P(f'Este é o momento perfeito para disparar a mecânica de <strong>Eclipse</strong> (botão <em>Eclipse</em> no menu Daggerheart, na barra lateral). O ambiente {env_link("festa-junina", "Festa Junina")} está pronto para a cena de abertura.')) +
    FIG('criatura-esboco', 'center'))



ALIADOS = (P('<em>Nesta seção você encontra possíveis aliados e suas habilidades.</em>') +
    BOX(npc_link('aliada-cuca', 'Cuca'), P('<strong>Descanse Bem.</strong> <em>Gatilho:</em> os jogadores iniciam um descanso com este PdM presente. <em>Efeito:</em> role 1d6; se rolar 5 ou mais, os jogadores podem fazer um movimento de repouso adicional.')) +
    BOX(npc_link('paje-raoni', 'Pajé Raoni'), P('<strong>Cura dos Espíritos.</strong> <em>Gatilho:</em> um combate inicia com este PdM presente. <em>Efeito:</em> inicie uma Contagem (Ciclo 4). Ela diminui sempre que um personagem marca Pontos de Vida. Quando ativada, este PdM faz com que todos os aliados próximos limpem um Ponto de Vida.')) +
    BOX(npc_link('tuxaua-caue', 'Tuxaua Cauê'), P('<strong>Mestre das Negociações.</strong> <em>Gatilho:</em> um personagem falha em um teste em uma negociação. <em>Efeito:</em> mova-se até Corpo a Corpo com o aliado, oferecendo conselhos e orientação. Uma vez por cena, o personagem pode rolar o teste novamente.')))

TRAITS = [('1–2', 'Aumente o dano dos adversários em <strong>+2</strong>.'),
          ('3–4', 'Aumente a Dificuldade de todos os adversários e ambientes em <strong>1</strong>, enquanto o Eclipse durar.'),
          ('5–6', 'Aumente os limiares de dano dos adversários em <strong>+2</strong>.'),
          ('7–8', 'Diminua o Dado de Esperança dos jogadores para um <strong>d10</strong>.'),
          ('9–10', 'Todas as criaturas obtêm <strong>sucesso crítico ao rolar 19 ou 20</strong> em testes de ataque contra personagens.')]

MECANICAS = (P('<em>As mecânicas a seguir são exclusivas deste cenário.</em>') +
    H('Mecânicas de Campanhas de Caça aos Monstros', 3) +
    P('Eclipse na Terra da Fartura usa todas as <strong>Mecânicas de Campanha de Caça a Monstros</strong> do Documento de Referência do Sistema (SRD) de Daggerheart.') +
    H('Eclipse', 2) + FIG('eclipse', 'right') +
    P('Os Eclipses, que antes eram vistos somente por algumas gerações, se tornaram algo constante na Terra da Fartura. Porém, cada Eclipse se manifesta de uma maneira diferente, com alguns sendo mais duradouros e outros sendo mais mortais. Nem todo Eclipse precisa ser algo grandioso e mortal; isso tira o peso narrativo de Eclipses menores. A seção a seguir detalha como utilizar a mecânica de Eclipse e dá dicas de como implementá-la na sua mesa.') +
    H('Montando um Eclipse', 3) +
    P('<strong>Uma vez por descanso longo, enquanto ainda estiver de dia</strong>, o mestre pode gastar Pontos de Medo para iniciar um Eclipse. Ative uma <strong>contagem regressiva (X)</strong>, com X sendo o <strong>dobro da quantidade de jogadores na cena</strong>; ela diminui em 1 a cada vez que um personagem usar qualquer quantia de Pontos de Esperança. Para cada Ponto de Medo gasto, role um <strong>d10</strong> e adicione a característica correspondente desta tabela ao seu Eclipse. Caso um dado caia em uma característica já adicionada, <strong>aumente a contagem em 2</strong>.') +
    '<table class="eclipse-table"><thead><tr><th>d10</th><th>Característica</th></tr></thead><tbody>' +
    ''.join(f'<tr><td>{a}</td><td>{b}</td></tr>' for a, b in TRAITS) + '</tbody></table>' +
    P('Ao final da contagem ou ao pôr do sol (o que vier primeiro), o Eclipse se encerra junto às suas características.') +
    H('Improvisando um Eclipse', 3) +
    P('Caso as características apresentadas na tabela acima não incluam o que você, como mestre, acha que o seu Eclipse deve incluir, você pode adicionar características à tabela e mudar seus números de acordo com o que achar necessário. Mas tenha cuidado para que as habilidades não se sobreponham e que estejam balanceadas.') +
    BOX('No Foundry', P('Abra o menu <strong>Daggerheart</strong> na barra lateral direita e clique em <strong>Eclipse</strong>. A janela do Eclipse calcula a contagem (2 × jogadores), deixa você escolher quantos Pontos de Medo gastar, rola os d10 com animação, aplica automaticamente as características como efeitos ativos (dano, Dificuldade, limiares, dado de Esperança e margem de crítico), cria a contagem regressiva no rastreador do sistema e a diminui a cada uso de Esperança. Enquanto o Eclipse durar, todos na mesa veem a borda pulsante na tela; ao final (contagem zerada ou botão <em>Pôr do Sol</em>), tudo é desfeito.') +
        P('Você também pode clicar nas características depois da rolagem para <em>improvisar</em> o Eclipse, e escrever características narrativas próprias.')))

CREDITOS = (FIG('capa-doze', 'right') + H('Editorial', 3) +
    P('Eu sempre tive medo do nosso folclore. Afinal, são espíritos e seres mitológicos milenares cultuados ou temidos pelos povos originários desde antes do descobrimento do Brasil. E que por pouco não foram apagados do conhecimento com o extermínio desse mesmo povo. Nas reuniões entre a nossa equipe, uma coisa era clara: essas criaturas são <strong>PROTETORES, GUARDIÕES e NÃO GOSTAM DOS INVASORES</strong>. O pensamento partiu desse princípio, pensando em como esses seres poderiam ser corrompidos e começassem a agir contra aqueles com quem deveriam viver em harmonia. Este livreto que você tem em mãos foi feito com nosso suor e esforço; recheamos ele com o que há de pior.',
      '<em>Ousam caçar alguns mitos?</em><br>— Time Doze') +
    H('Créditos', 3) +
    P('<strong>Design de Jogo:</strong> Henrique “Manik” Fonseca, Giordano “Zeva” Azevedo, Vinícius Sena, Pedro Tostes',
      '<strong>Design Gráfico:</strong> Luiz “Raposo” Nogueira, Markus “Fergo” Silva',
      '<strong>Artistas:</strong> Rodrigo Martins, André Ignatiuk, Ranzinza Cinza',
      '<strong>Módulo para Foundry VTT:</strong> ANAMA Criativa') +
    P('<small>This product includes materials from the Daggerheart System Reference Document 2.0, © Critical Role, LLC. under the terms of the Darrington Press Community Gaming (DPCGL) License. More information can be found at https://www.daggerheart.com. There are no previous modifications by others.</small>',
      '<small>Esta publicação faz parte da Fear Fest 2026. A Fear Fest foi concebida e organizada por Bard &amp; Raven e hospedada pela Heart of Daggers para celebrar o amor compartilhado das comunidades por Halloween e Daggerheart. Confira as outras criações da comunidade em www.heartofdaggers.com/fear-fest.</small>'))


# --------------------------------------------------------------- bestiário
BESTIARIO = [
    (1, [('cobra-norato', 'Cobra Norato', 'Assistente'), ('homem-do-saco', 'Homem do Saco', 'Oportunista'), ('mapinguari', 'Mapinguari', 'Brutamontes'),
         ('maria-caninana', 'Maria Caninana', 'Atirador'), ('mula-sem-cabeca', 'Mula Sem Cabeça', 'Solo'), ('noiva-do-candelabro', 'Noiva do Candelabro', 'Comum')]),
    (2, [('bernuncinha', 'Bernuncinha', 'Brutamontes'), ('caipora', 'Caipora', 'Assistente'), ('curupira', 'Curupira', 'Líder'),
         ('clone-curupira', 'Clone Ilusório do Curupira', 'Lacaio'), ('mulher-de-sete-metros', 'Mulher de Sete Metros', 'Comum'),
         ('saci-perere', 'Saci-Pererê', 'Oportunista'), ('espirito-porco-do-mato', 'Saci — Espírito de Porco do Mato', 'Oportunista (evolução)')]),
    (3, [('bernunca', 'Bernunça', 'Brutamontes'), ('boi-da-cara-preta', 'Boi da Cara Preta', 'Horda (3/PV)'),
         ('despertar-do-pesadelo', 'Boi da Cara Preta — O Despertar do Pesadelo', 'Brutamontes (evolução)'), ('cabra-cabriola', 'Cabra Cabriola', 'Oportunista'),
         ('cuca', 'Cuca', 'Líder'), ('pesadelo-da-cuca', 'Pesadelo da Cuca', 'Lacaio'), ('encourado', 'Encourado', 'Manipulador'),
         ('encourado-revelado', 'Encourado Revelado', 'Solo')]),
    (4, [('abuhuku', 'Abúhukü', 'Solo'), ('boitata-cabeca', 'Boitatá (Cabeça)', 'Colosso'), ('boitata-corpo', 'Boitatá (Corpo)', 'Colosso'),
         ('boitata-cauda', 'Boitatá (Cauda)', 'Colosso'), ('boiuna', 'Boiúna', 'Solo'), ('loira-do-banheiro', 'Loira do Banheiro', 'Manipulador')]),
]

ARTMAP = {'mapinguari': 'mapinguari', 'caipora': 'caipora', 'curupira': 'curupira', 'saci-perere': 'saci', 'espirito-porco-do-mato': 'saci-rosto',
          'boi-da-cara-preta': 'boi-da-cara-preta', 'despertar-do-pesadelo': 'boi-da-cara-preta', 'cuca': 'cuca', 'boitata-cabeca': 'boitata'}


def bestiary_index():
    html = P('Os Encantados corrompidos e as Criaturas da Noite da Terra da Fartura. Clique em um nome para abrir a ficha; arraste a ficha para a cena para criar o token.')
    for tier, lst in BESTIARIO:
        html += H(f'{tier}º Patamar', 3) + '<table class="eclipse-table"><thead><tr><th>Adversário</th><th>Tipo</th></tr></thead><tbody>'
        for key, name, t in lst:
            html += f'<tr><td>{adv_link(key, name)}</td><td>{t}</td></tr>'
        html += '</tbody></table>'
    html += H('Ambientes', 3) + UL(env_link('mae-de-ouro', 'Mãe de Ouro') + ' — 1º Patamar · Exploração',
                                    env_link('festa-junina', 'Festa Junina') + ' — 2º Patamar · Social',
                                    env_link('rondolo', 'Rondolo') + ' — 3º Patamar · Evento',
                                    env_link('opartaba', 'Opartabá') + ' — 4º Patamar · Exploração')
    return html


def creature_page(key, name):
    art = ARTMAP.get(key)
    fig = FIG(art, 'right') if art else f'<figure class="eclipse-art right token"><img src="{ASSET}/tokens/{key}.webp"></figure>'
    return fig + f'<p>@Embed[{adv_uuid(key)}]</p>' + P(f'Abrir ficha: {adv_link(key, name)}')


def env_page(key, name):
    return f'<p>@Embed[{env_uuid(key)}]</p>' + P(f'Abrir ambiente: {env_link(key, name)}')


def interview():
    import os
    path = os.path.join(os.path.dirname(__file__), 'entrevista.html')
    return open(path, encoding='utf-8').read() if os.path.exists(path) else ''


def build_journals():
    jog = entry('guia-jogadores', 'Eclipse na Terra da Fartura — Guia dos Jogadores', [
        page('guia-jogadores', 'Eclipse na Terra da Fartura', PROPOSTA, 100),
        page('guia-jogadores', 'Visão Geral', VISAO, 200),
        page('guia-jogadores', 'Comunidades', COMUNIDADES, 300),
        page('guia-jogadores', 'Ancestralidades', ANCESTRALIDADES, 400),
        page('guia-jogadores', 'Classes', CLASSES, 500),
        page('guia-jogadores', 'Princípios do Jogador', PRINC_JOG, 600),
        page('guia-jogadores', 'Perguntas para a Sessão Zero', SESSAO_ZERO, 700),
    ], 100)
    pages = [
        page('guia-mestre', 'Capa', f'{ART}/capa-doze.webp', 50, ptype='image', src=f'{ART}/capa-doze.webp', show=False),
        page('guia-mestre', 'Eclipse na Terra da Fartura', PROPOSTA, 100),
        page('guia-mestre', 'Editorial & Créditos', CREDITOS, 150),
        page('guia-mestre', 'Visão Geral', VISAO, 200),
        page('guia-mestre', 'Comunidades', COMUNIDADES, 300),
        page('guia-mestre', 'Ancestralidades', ANCESTRALIDADES, 400),
        page('guia-mestre', 'Classes', CLASSES, 500),
        page('guia-mestre', 'Princípios do Jogador', PRINC_JOG, 600),
        page('guia-mestre', 'Princípios do Mestre', PRINC_MES, 650),
        page('guia-mestre', 'Aspectos: Biomas e seus Povos', BIOMAS, 700),
        page('guia-mestre', 'Distinções: a Noite ao Meio-Dia', DISTINCOES, 800),
        page('guia-mestre', 'Distinções: Yandê-M’Bae', YANDE, 850),
        page('guia-mestre', 'Distinções: Criaturas da Noite', CRIATURAS, 900),
        page('guia-mestre', 'Incidente Incitante', INCIDENTE, 1000),
        page('guia-mestre', 'Aliados', ALIADOS, 1100),
        page('guia-mestre', 'Mecânicas: o Eclipse', MECANICAS, 1200),
        page('guia-mestre', 'Perguntas para a Sessão Zero', SESSAO_ZERO, 1300),
        page('guia-mestre', 'Bestiário', bestiary_index(), 1400),
    ]
    s = 1500
    for tier, lst in BESTIARIO:
        for key, name, t in lst:
            pages.append(page('guia-mestre', name, creature_page(key, name), s, level=2))
            s += 10
    for key, name in [('mae-de-ouro', 'Ambiente: Mãe de Ouro'), ('festa-junina', 'Ambiente: Festa Junina'),
                      ('rondolo', 'Ambiente: Rondolo'), ('opartaba', 'Ambiente: Opartabá')]:
        pages.append(page('guia-mestre', name, env_page(key, name.split(': ')[1]), s, level=2))
        s += 10
    iv = interview()
    if iv:
        pages.append(page('guia-mestre', 'Entrevista: Nico de Gallo', iv, 9000))
    mes = entry('guia-mestre', 'Eclipse na Terra da Fartura — Guia do Mestre', pages, 200)
    return [jog], [mes]
