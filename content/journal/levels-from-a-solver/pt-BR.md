---
title: Os níveis vêm de um solucionador, não da sorte
summary: Embaralhar as bolinhas ao acaso pode gerar tabuleiros sem solução. Por isso geramos todos os níveis com antecedência e provamos que dá para terminá-los.
lang: pt-BR
copy_review: iris 2026-11-15
date: 2026-11-15
time: 19:10
---
Todo quebra-cabeça de separar tem uma armadilha: se você embaralha as bolinhas ao acaso, algumas combinações simplesmente não têm solução. Ninguém gosta de descobrir isso na jogada quarenta.

## A decisão

Os níveis não são gerados enquanto você joga. Um solucionador os constrói antes de o app ser lançado, e o app inclui o resultado como um arquivo estático: para cada nível, a disposição das garrafas e o **menor número de movimentos** necessário para resolvê-lo. O app lê os níveis por uma única interface pequena, então a forma de criá-los pode mudar sem mexer nas telas.

Escolhemos assim porque um nível já construído tem solução garantida, e porque saber o mínimo permite que o app o mostre ao lado do seu melhor resultado.

## Como um nível é feito

- Começamos com n cores e uma semente aleatória fixa: n garrafas cheias, mais 2 vazias.
- Procuramos uma solução. O primeiro protótipo usou busca em profundidade com limite de 60.000 estados.
- A busca ignora movimentos que não podem ajudar: mexer numa garrafa que já está completa, despejar em garrafas vazias mais de uma vez, passar uma única bolinha de uma garrafa com uma só bolinha para uma garrafa vazia.
- Um estado é guardado como a lista ordenada das garrafas, então duas disposições que só diferem na ordem das garrafas contam como a mesma.
- Depois calculamos o menor número de movimentos: busca em largura para níveis pequenos e aprofundamento iterativo para os grandes.
- Níveis sem solução, já resolvidos ou fáceis demais são descartados. O que sobra é ordenado do mais fácil ao mais difícil.

## Verificação

O plano inclui um teste que resolve de novo cada nível incluído, e a primeira versão jogável mirava pelo menos 30 níveis. A página inicial agora diz 150.
