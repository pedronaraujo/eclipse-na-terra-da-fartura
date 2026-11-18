# Eclipse na Terra da Fartura — módulo para Foundry VTT

Cenário de **Daggerheart** da revista **DOZE Vol. 1** (ANAMA Criativa), pronto para o sistema
[Daggerheart (Foundryborne)](https://github.com/Foundryborne/daggerheart) no Foundry VTT v14.

> Em uma terra onde eclipses tornam os protetores naturais em monstros, Caçadores de Mitos devem
> descobrir a verdade antes que o eclipse eterno cubra o céu.

## O que vem no módulo

| Compêndio | Conteúdo |
|---|---|
| **Eclipse — Guia dos Jogadores** | Proposta, Visão Geral, Comunidades, Ancestralidades, Classes, Princípios do Jogador, Sessão Zero |
| **Eclipse — Guia do Mestre** | Tudo do guia dos jogadores + Princípios do Mestre, Biomas e seus Povos, Distinções (Reinos Perdidos, O Início, Noite ao Meio-Dia, Yandê-M’Bae, Criaturas da Noite, Encantados), Incidente Incitante, Aliados, Mecânica do Eclipse, Bestiário com fichas embutidas e Ambientes |
| **Eclipse — Adversários** | 27 fichas (4 patamares) com ataques, ações, custos de Medo/Fadiga, testes de reação, condições, contagens, evoluções (transformação automática) e invocações |
| **Eclipse — Ambientes** | Mãe de Ouro, Festa Junina, Rondolo, Opartabá (com adversários potenciais do SRD) |
| **Eclipse — Aliados** | Cuca, Pajé Raoni, Tuxaua Cauê |
| **Eclipse — Tabelas / Macros** | Tabela d10 do Eclipse; macros para abrir, avançar e encerrar o Eclipse |

## A mecânica de Eclipse

No menu **Daggerheart** (aba da direita) aparece o botão **Eclipse**. A janela:

1. sugere o número de jogadores na cena e calcula a contagem (**2 × jogadores**);
2. deixa o mestre escolher quanto **Medo** gastar e rola **1d10 por Medo** (com Dice So Nice, se houver);
3. acende as características sorteadas; repetidas somam **+2** na contagem; o mestre pode ligar/desligar
   características e escrever características improvisadas;
4. ao iniciar: desconta o Medo, cria a contagem no rastreador do sistema, escurece a cena e aplica um efeito
   ativo **Eclipse** em adversários, ambientes e personagens afetados:
   - 1–2: +2 de dano dos adversários · 3–4: Dificuldade +1 (adversários e ambientes)
   - 5–6: limiares +2 · 7–8: Dado de Esperança d10 · 9–10: crítico em 19–20;
5. a contagem diminui sozinha cada vez que um personagem usa Esperança (dá para ajustar à mão);
6. enquanto durar, **todos veem a borda pulsante**, cinzas subindo e um HUD com a contagem; o pulso acelera
   conforme a contagem cai. Ao zerar (ou no botão **Pôr do sol**), tudo é desfeito e o sol volta.

Configurações: escurecer a cena e nível de escuridão, aplicar efeitos, contagem automática, usar o
rastreador do sistema, sons de início/fim, intensidade do efeito de tela (por jogador), animações e posição do HUD.

API: `game.modules.get('eclipse-na-terra-da-fartura').api` → `open()`, `start({...})`, `end()`, `tick(delta)`, `state`.

## Instalação

Manifesto: `https://github.com/pedronaraujo/eclipse-na-terra-da-fartura/releases/latest/download/module.json`

## Desenvolvimento

```bash
npm install
npm run build      # gera src/packs (Python) e compila packs/ (LevelDB)
```

Os dados são gerados por `tools/build.py` (IDs determinísticos). Não edite `packs/` à mão.

## Créditos

Design de jogo: Henrique “Manik” Fonseca, Giordano “Zeva” Azevedo, Vinícius Sena, Pedro Tostes ·
Design gráfico: Luiz “Raposo” Nogueira, Markus “Fergo” Silva · Arte: Rodrigo Martins, André Ignatiuk, Ranzinza Cinza.
Arte e texto © ANAMA Criativa, usados com autorização. Fontes: UnifrakturMaguntia, Cinzel e IM Fell (SIL OFL).

This product includes materials from the Daggerheart System Reference Document 2.0, © Critical Role, LLC.
under the terms of the Darrington Press Community Gaming (DPCGL) License. https://www.daggerheart.com
