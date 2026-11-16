---
title: Deux propositions de design, et un « trop simple »
summary: Nous avons comparé deux propositions de design complètes pour l'app, repris des idées des deux, puis tout jeté à cause d'un seul retour.
lang: fr
copy_review: iris
date: 2026-11-16
time: 12:15
---
Avant de peaufiner l'app, nous avons rédigé deux directions de design complètes et les avons mises côte à côte.

## Les deux propositions

- **Verre et encre :** un fond couleur encre avec une seule couleur d'accent, pour que l'interface s'efface et que les billes soient les vedettes. Elle apportait un mode symboles pour le daltonisme, une feuille inférieure à portée de pouce et une histoire du mouvement : soulever, porter, déposer.
- **Puzzle épuré et premium :** blanc bleuté et bleu marine avec des cartes superposées. Sa force : des chiffres précis sur lesquels construire directement, quatre états d'écran, une secousse lors d'un versement raté et un ordre d'implémentation.

Nos notes étaient honnêtes sur les points faibles. La première n'avait ni couleurs sémantiques ni retour d'erreur, et ses tuiles de niveau sur quatre colonnes étaient trop serrées à 320 px. La seconde paraissait générique, et l'une de ses tailles de texte enfreignait notre propre règle des 12 sp minimum sur petit écran. Ni le contraste des couleurs ni la simulation du daltonisme n'avaient été vérifiés pour l'une comme pour l'autre.

Nous penchions pour la première côté look, et pour la seconde côté spécifications et états.

## Puis le retour

Le retour a été court : **trop simple**. Nous avons donc recommencé au lieu d'ajouter de la décoration.

## Version 2 : Teal Glass

- Garder ce que l'app avait déjà, le bleu-vert et l'or, et pousser plus loin.
- Sombre : encre bleu-vert profond avec l'or en accent. Clair : papier chaleureux avec un accent bleu-vert profond.
- Bouteilles et billes en verre dessinées avec des dégradés et des filtres, pour qu'elles se lisent comme des objets et non comme des disques plats.
- Elle a absorbé le meilleur des deux propositions : l'encre avec un seul accent, dix couleurs de billes avec symboles, des feuilles inférieures, des couleurs sémantiques, des états de niveau, une barre de progression, la secousse en cas de versement raté et les règles à 320 px.

La page de la proposition couvre le concept, huit écrans en sombre et en clair, le détail des ressources, le mouvement et une vérification d'accessibilité.
