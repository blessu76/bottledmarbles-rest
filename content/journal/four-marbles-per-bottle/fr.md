---
title: Quatre billes par bouteille : toutes les règles
date: 2026-11-13
time: 22:28
summary: Les règles de Bottled Marbles tiennent en quelques lignes. Les voici, avec les petites décisions qui les entourent.
lang: fr
copy_review: iris
---
Bottled Marbles est un puzzle de tri : déplacez des billes entre des bouteilles de verre jusqu'à ce que chaque bouteille ne contienne plus qu'une seule couleur. Les règles sont courtes, et c'est voulu.

## Les règles, telles qu'on les a écrites

- Une bouteille contient **4 billes**. Un niveau de n couleurs compte 4 × n billes.
- Il y a n + 2 bouteilles : n sont pleines au départ et **2 sont vides**.
- Vous pouvez verser d'une bouteille non vide vers une bouteille non pleine, et seulement sur une bouteille vide ou sur une bille de la même couleur.
- Vous versez toute la série de billes de même couleur du dessus, tant que la bouteille d'arrivée a de la place, et cela compte pour **un coup**.
- Vous gagnez quand chaque bouteille est soit vide, soit pleine d'une seule couleur.

Le nombre de couleurs augmente avec le niveau : `min(3 + floor((level + 1) / 2), 8)`. Les premiers niveaux ont donc trois couleurs, et les suivants cessent de grandir à huit.

## Quatre et deux

La capacité de quatre et les deux bouteilles de réserve viennent directement du premier prototype. Les deux bouteilles vides sont l'espace de respiration qui rend le versement possible, et nous n'avons jamais eu besoin de changer l'un ou l'autre de ces nombres.

## Petites décisions qui comptent

- Toucher de nouveau la même bouteille la désélectionne, et une bouteille vide ne peut pas être sélectionnée.
- Toucher une bouteille dans laquelle on ne peut pas verser le signale et déplace votre sélection sur elle, au lieu d'ignorer le toucher en silence.
- L'annulation est illimitée et retire un coup du compteur. Recommencer remet le niveau dans sa disposition initiale.

Ces règles viennent du premier prototype jouable et ont été conservées telles quelles dans l'app. Le record que nous gardons pour chaque niveau est le plus petit nombre de coups dont vous avez eu besoin.
