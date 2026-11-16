---
title: Duas propostas de design e um "simples demais"
summary: Comparamos duas propostas completas de design para o app, pegamos ideias das duas e depois jogamos o resultado fora por causa de um único comentário.
lang: pt-BR
copy_review: iris
date: 2026-11-16
time: 12:15
---
Antes de refinar o app, escrevemos duas direções de design completas e colocamos lado a lado.

## As duas propostas

- **Vidro e tinta:** um fundo cor de tinta com uma única cor de destaque, para que a interface fique em segundo plano e as bolinhas sejam as estrelas. Trazia um modo de símbolos para daltonismo, uma folha inferior ao alcance do polegar e uma história de movimento: levantar, carregar, soltar.
- **Puzzle limpo e premium:** azul-claro e azul-marinho com cartões em camadas. Seu ponto forte eram números precisos que dava para usar direto na construção, quatro estados de tela, uma tremida ao despejar errado e uma ordem de implementação.

Nossas anotações foram honestas sobre os pontos fracos. A primeira não tinha cores semânticas nem retorno de erro, e seus blocos de nível em quatro colunas ficavam apertados em 320 px. A segunda parecia genérica, e um de seus tamanhos de texto quebrava nossa própria regra de 12 sp ou mais em telas pequenas. Nenhuma das duas teve contraste de cor ou simulação de daltonismo verificados.

Nos inclinamos pela primeira no visual e pela segunda em especificações e estados.

## Então veio o comentário

O comentário foi curto: **simples demais**. Então recomeçamos em vez de acrescentar enfeites.

## Versão 2: Teal Glass

- Manter o que o app já tinha, verde-azulado e dourado, e levar mais longe.
- Escuro: tinta verde-azulada profunda com o dourado como destaque. Claro: papel quente com destaque verde-azulado profundo.
- Garrafas e bolinhas de vidro desenhadas com gradientes e filtros, para parecerem objetos e não círculos chapados.
- Absorveu o melhor das duas propostas: tinta com um único destaque, dez cores de bolinha com símbolos, folhas inferiores, cores semânticas, estados de nível, barra de progresso, a tremida ao despejar errado e as regras de 320 px.

A página da proposta traz o conceito, oito telas em escuro e claro, o detalhamento dos recursos, o movimento e uma verificação de acessibilidade.
