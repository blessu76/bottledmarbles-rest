---
title: Murmeln, die man auch ohne Farbe unterscheidet
summary: Zehn Murmelfarben, zehn Symbole, ein paar Layout-Tests auf kleinen Bildschirmen – und ein Button, der sich nicht antippen ließ.
lang: de
copy_review: iris
date: 2026-11-17
time: 17:00
---
Ein Spiel, bei dem man nach Farben sortiert, hat ein offensichtliches Problem: Manche Spielerinnen und Spieler können die Farben nicht auseinanderhalten. Build 6 der App, die das Design Teal Glass mitbringt, nimmt sich dieses Problems an und noch einiger kleinerer Dinge.

## Symbole auf den Murmeln

Es gibt zehn Murmelfarben, und jede hat zusätzlich ihr eigenes **Symbol**. Die Farbe ist das Hauptsignal, das Symbol die Absicherung – so bleibt ein Level lösbar, auch wenn zwei Farbtöne ähnlich aussehen.

## Kleine Bildschirme testen

Die Widget-Tests zeichnen die Bildschirme in 320 und 375 px Breite, dunkel und hell, mit auf 200 % vergrößerter Schrift, und schlagen bei jedem Überlauf fehl. Diese Matrix ist günstig auszuführen und fängt die Art von Fehlern ab, die sonst erst auf dem kleinen Handy von jemandem auffallen.

Was wir noch nicht gemacht haben: Diese Tests sind Widget-Tests plus Screenshots eines Simulators mit etwa 393 px Breite. Eine Prüfung auf einem echten Gerät mit 320 oder 375 px steht noch aus, und das halten wir auch in unseren Notizen so fest.

## Der Button unter der Scroll-Ansicht

Beim Bau des Startbildschirms fiel uns auf, dass der Einstellungen-Button auf Tippen nicht reagierte. Die Ursache lag in der Schichtung: Er saß im Stack unter der Scroll-Ansicht, die jede Berührung abfing. Die Reihenfolge im Stack zu ändern, löste das Problem. Behoben wurde es im selben Build wie das Redesign.

## Noch offen

Sechs Flaschenverschlüsse und fünf Flaschen-Skins sind entworfen, ausgeliefert wird bisher aber nur das Standard-Aussehen. Die Struktur kann dafür wachsen. Neue Gieß-Animationen und Haptik sind ebenfalls noch nicht dabei; das bisherige Verhalten bleibt.
