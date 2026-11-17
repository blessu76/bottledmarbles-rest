---
title: Des billes qu'on distingue sans la couleur
summary: Dix couleurs de billes, dix symboles, quelques tests de mise en page sur petits écrans, et un bouton impossible à toucher.
lang: fr
copy_review: iris
date: 2026-11-17
time: 17:00
---
Un jeu où l'on trie par couleur a un problème évident : certains joueurs ne distinguent pas les couleurs. La version 6 de l'app, qui intègre le design Teal Glass, s'attaque à ce problème et à quelques autres, plus modestes.

## Des symboles sur les billes

Il y a dix couleurs de billes, et chacune a aussi son propre **symbole**. La couleur est le signal principal, le symbole sert de renfort : un niveau reste donc résoluble quand deux teintes se ressemblent.

## Tester les petits écrans

Les tests de widgets affichent les écrans en 320 et 375 px de large, en mode sombre et en mode clair, avec le texte agrandi à 200 %, et échouent au moindre débordement. Cette matrice coûte peu à exécuter et attrape le genre de bug qui, sinon, n'apparaît que sur le petit téléphone de quelqu'un.

Ce que nous n'avons pas fait : ces tests sont des tests de widgets, complétés par des captures d'un simulateur d'environ 393 px de large. Une vérification sur un vrai téléphone en 320 ou 375 px reste à faire, et nous l'indiquons dans nos notes.

## Le bouton sous la vue défilante

En construisant l'écran d'accueil, nous avons constaté que le bouton des réglages ne réagissait pas aux appuis. La cause tenait aux couches : dans la pile, il se trouvait sous la vue défilante, qui captait tous les touchers. Réordonner la pile a réglé le problème. Le correctif est sorti dans la même version que la refonte.

## À venir

Six bouchons et cinq habillages de bouteille sont dessinés, mais seul l'aspect par défaut est livré pour l'instant. La structure peut évoluer pour les accueillir. Les nouvelles animations de versement et le retour haptique ne sont pas encore là non plus ; le comportement actuel ne change pas.
