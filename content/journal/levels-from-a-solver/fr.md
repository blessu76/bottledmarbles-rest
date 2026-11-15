---
title: Les niveaux viennent d'un solveur, pas du hasard
summary: Mélanger les billes au hasard peut produire des grilles impossibles à résoudre. Nous générons donc chaque niveau à l'avance et prouvons qu'il peut être terminé.
lang: fr
copy_review: iris 2026-11-15
date: 2026-11-15
time: 19:10
---
Les puzzles de tri cachent un piège : si l'on mélange les billes au hasard, certaines dispositions sont tout simplement impossibles à résoudre. Personne n'aime le découvrir au quarantième coup.

## La décision

Les niveaux ne sont pas générés pendant que vous jouez. Un solveur les construit avant la sortie de l'app, qui embarque le résultat sous forme de fichier statique : pour chaque niveau, la disposition des bouteilles et le **nombre minimal de coups** nécessaire pour le résoudre. L'app ne lit les niveaux qu'à travers une petite interface, si bien que leur fabrication peut évoluer sans toucher aux écrans.

Nous avons choisi cette voie parce qu'un niveau déjà construit est garanti résoluble, et parce que connaître le minimum permet à l'app de l'afficher à côté de votre meilleur résultat.

## Comment un niveau est fabriqué

- On part de n couleurs avec une graine aléatoire fixe : n bouteilles remplies, plus 2 vides.
- On cherche une solution. Le premier prototype utilisait une recherche en profondeur plafonnée à 60 000 états.
- La recherche écarte les coups qui ne peuvent pas aider : toucher une bouteille déjà terminée, verser plus d'une fois dans des bouteilles vides, déplacer une bille seule d'une bouteille qui n'en contient qu'une vers une bouteille vide.
- Un état est stocké sous forme de liste triée des bouteilles : deux dispositions qui ne diffèrent que par l'ordre des bouteilles comptent donc pour une seule.
- On cherche ensuite le nombre minimal de coups : recherche en largeur pour les petits niveaux, approfondissement itératif pour les grands.
- Les niveaux impossibles, déjà résolus ou trop faciles sont jetés. Ce qui reste est classé du plus facile au plus difficile.

## Vérification

Le plan comprend un test qui résout de nouveau chaque niveau embarqué, et la première version jouable visait au moins 30 niveaux. La page d'accueil en annonce désormais 150.
