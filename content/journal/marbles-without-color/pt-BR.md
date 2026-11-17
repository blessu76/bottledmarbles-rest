---
title: Bolinhas que dá para distinguir sem usar a cor
summary: Dez cores de bolinhas, dez símbolos, alguns testes de layout em telas pequenas e um botão que não dava para tocar.
lang: pt-BR
copy_review: iris
date: 2026-11-17
time: 17:00
---
Um jogo de organizar por cor tem um problema óbvio: algumas pessoas não conseguem distinguir as cores. A versão 6 do app, que traz o design Teal Glass, enfrenta isso e mais algumas questões menores.

## Símbolos nas bolinhas

Existem dez cores de bolinhas, e cada uma também tem o seu próprio **símbolo**. A cor é o sinal principal e o símbolo é o reforço, então o nível continua tendo solução mesmo quando dois tons parecem iguais.

## Testes em telas pequenas

Os testes de widget desenham as telas com 320 e 375 px de largura, nos modos escuro e claro, com o texto ampliado a 200%, e falham diante de qualquer estouro. Essa matriz é barata de rodar e pega o tipo de bug que, de outro jeito, só aparece no celular pequeno de alguém.

O que ainda não fizemos: esses testes são testes de widget mais capturas de tela de um simulador com cerca de 393 px de largura. A verificação em um celular de verdade, com 320 ou 375 px, continua pendente, e isso está dito nas nossas anotações.

## O botão embaixo da área de rolagem

Enquanto construíamos a tela inicial, percebemos que o botão de ajustes não respondia aos toques. A causa estava nas camadas: ele ficava na pilha abaixo da área de rolagem, que recebia todos os toques. Reordenar a pilha resolveu. A correção entrou na mesma versão do redesign.

## O que vem por aí

Seis tampas e cinco estilos de garrafa já estão desenhados, mas por enquanto só o visual padrão é entregue. A estrutura pode crescer para recebê-los. As novas animações de despejo e a resposta tátil também ainda não entraram; o comportamento atual continua o mesmo.
