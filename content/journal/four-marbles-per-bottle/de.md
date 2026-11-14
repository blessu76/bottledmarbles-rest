---
title: Vier Murmeln pro Flasche: das ganze Regelwerk
date: 2026-11-13
time: 22:28
summary: Die Regeln von Bottled Marbles passen in wenige Zeilen. Hier sind sie, samt den kleinen Entscheidungen drumherum.
lang: de
copy_review: iris
---
Bottled Marbles ist ein Sortierrätsel: Du bewegst Murmeln zwischen Glasflaschen, bis jede Flasche nur noch eine Farbe enthält. Das ganze Regelwerk ist absichtlich kurz.

## Die Regeln, wie sie aufgeschrieben sind

- Eine Flasche fasst **4 Murmeln**. Ein Level mit n Farben hat 4 × n Murmeln.
- Es gibt n + 2 Flaschen: n davon starten gefüllt, **2 starten leer**.
- Du kannst aus einer Flasche, die nicht leer ist, in eine Flasche gießen, die nicht voll ist, und zwar nur auf eine leere Flasche oder auf eine Murmel derselben Farbe.
- Du gießt die ganze oberste Reihe gleichfarbiger Murmeln um, soweit in der Zielflasche Platz ist, und das zählt als **ein Zug**.
- Du gewinnst, wenn jede Flasche entweder leer oder voll mit einer einzigen Farbe ist.

Die Zahl der Farben wächst mit dem Level: `min(3 + floor((level + 1) / 2), 8)`. Frühe Level haben also drei Farben, und spätere hören bei acht auf zu wachsen.

## Vier und zwei

Die Kapazität von vier und die zwei Reserveflaschen stammen direkt aus dem ersten Prototyp. Die zwei leeren Flaschen sind der Spielraum, der das Umgießen überhaupt erst möglich macht, und wir mussten keine der beiden Zahlen ändern.

## Kleine Entscheidungen, die zählen

- Tippst du dieselbe Flasche erneut an, wird sie abgewählt, und eine leere Flasche lässt sich nicht auswählen.
- Tippst du eine Flasche an, in die du nicht gießen kannst, wird dir das gesagt und deine Auswahl wandert dorthin, statt dass das Antippen stillschweigend ignoriert wird.
- Rückgängig ist unbegrenzt und nimmt einen Zug vom Zähler zurück. Neustart setzt das Level auf seine erste Anordnung zurück.

Diese Regeln stammen aus dem ersten spielbaren Prototyp und wurden in der App unverändert beibehalten. Die Bestmarke, die wir für jedes Level speichern, ist die geringste Anzahl an Zügen, die du gebraucht hast.
