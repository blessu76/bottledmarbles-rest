---
title: Quatro bolinhas por garrafa: o regulamento completo
date: 2026-11-13
time: 22:28
summary: As regras do Bottled Marbles cabem em poucas linhas. Aqui estão elas, junto com as pequenas decisões ao redor.
lang: pt-BR
copy_review: iris
---
Bottled Marbles é um quebra-cabeça de organização: mova bolinhas entre garrafas de vidro até que cada garrafa tenha uma única cor. O regulamento é curto de propósito.

## As regras, como estão escritas

- Uma garrafa comporta **4 bolinhas**. Um nível com n cores tem 4 × n bolinhas.
- Há n + 2 garrafas: n começam cheias e **2 começam vazias**.
- Você pode despejar de uma garrafa que não está vazia em uma garrafa que não está cheia, e somente sobre uma garrafa vazia ou sobre uma bolinha da mesma cor.
- Você despeja toda a sequência de bolinhas da mesma cor que está no topo, até onde houver espaço no destino, e isso conta como **uma jogada**.
- Você vence quando toda garrafa está vazia ou cheia de uma única cor.

O número de cores cresce com o nível: `min(3 + floor((level + 1) / 2), 8)`, então os primeiros níveis têm três cores e os seguintes param de crescer em oito.

## Quatro e dois

A capacidade de quatro e as duas garrafas extras vêm direto do primeiro protótipo. As duas garrafas vazias são o espaço de respiro que torna possível despejar, e não precisamos mudar nenhum dos dois números.

## Pequenas decisões que importam

- Tocar na mesma garrafa de novo a desseleciona, e uma garrafa vazia não pode ser selecionada.
- Tocar em uma garrafa na qual você não pode despejar avisa isso e move sua seleção para ela, em vez de ignorar o toque em silêncio.
- Desfazer é ilimitado e tira uma jogada do contador. Reiniciar devolve o nível à sua primeira disposição.

Essas regras vieram do primeiro protótipo jogável e foram mantidas sem alterações no app. O recorde que guardamos para cada nível é o menor número de jogadas de que você precisou.
