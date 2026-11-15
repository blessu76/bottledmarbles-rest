---
title: Levels kommen von einem Solver, nicht vom Zufall
summary: Wer Murmeln zufällig mischt, erzeugt manchmal unlösbare Level. Deshalb erzeugen wir jedes Level vorab und belegen, dass es sich schaffen lässt.
lang: de
copy_review: iris 2026-11-15
date: 2026-11-15
time: 19:10
---
Sortierrätsel haben eine Falle: Mischt man die Murmeln zufällig, lassen sich manche Anordnungen schlicht nicht lösen. Niemand merkt das gern im vierzigsten Zug.

## Die Entscheidung

Level werden nicht erzeugt, während du spielst. Ein Solver baut sie, bevor die App erscheint, und die App enthält das Ergebnis als statische Datei: für jedes Level die Anordnung der Flaschen und die **geringste Zugzahl**, die zum Lösen nötig ist. Die App liest Level nur über eine kleine Schnittstelle, sodass sich die Erzeugung ändern kann, ohne die Bildschirme anzufassen.

Wir haben uns dafür entschieden, weil ein vorab gebautes Level garantiert lösbar ist und weil die App mit der bekannten Mindestzahl diese neben deinem Bestergebnis anzeigen kann.

## So entsteht ein Level

- Start mit n Farben und einem festen Zufalls-Seed: n gefüllte Flaschen plus 2 leere.
- Suche nach einer Lösung. Der erste Prototyp nutzte eine Tiefensuche mit einer Obergrenze von 60.000 Zuständen.
- Die Suche überspringt Züge, die nicht helfen können: eine bereits fertige Flasche anfassen, mehr als einmal in leere Flaschen gießen, eine einzelne Murmel aus einer Ein-Murmel-Flasche in eine leere Flasche umfüllen.
- Ein Zustand wird als sortierte Liste der Flaschen gespeichert, sodass zwei Anordnungen, die sich nur in der Reihenfolge der Flaschen unterscheiden, als gleich gelten.
- Danach wird die geringste Zugzahl bestimmt: Breitensuche für kleine Level, iterative Tiefensuche für große.
- Unlösbare, bereits gelöste oder zu leichte Level werden verworfen. Der Rest wird von leicht nach schwer sortiert.

## Die Prüfung

Der Plan enthält einen Test, der jedes mitgelieferte Level erneut löst, und die erste spielbare Version zielte auf mindestens 30 Level. Auf der Startseite stehen jetzt 150.
