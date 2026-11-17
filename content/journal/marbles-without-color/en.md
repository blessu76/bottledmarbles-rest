---
title: Marbles you can tell apart without color
summary: Ten marble colors, ten symbols, and a few layout tests on small screens. Plus one button that could not be tapped.
date: 2026-11-17
time: 17:00
---
A game about sorting by color has an obvious problem: some players cannot tell the colors apart. Build 6 of the app, which carries the Teal Glass design, tackles that and a few smaller things.

## Symbols on the marbles

There are ten marble colors, and each one also has its own **symbol**. The color is the main signal, the symbol is the backup, so a level stays solvable when two hues look alike.

## Testing small screens

The widget tests render the screens at 320 and 375 px wide, in dark and light, with text scaled to 200%, and fail on any overflow. That matrix is cheap to run and catches the bug class that otherwise shows up only on someone's small phone.

What we have not done: those tests are widget tests plus screenshots from a simulator about 393 px wide. A check on a real phone at 320 or 375 px is still open, and we say so in our notes.

## The button under the scroll view

While building the home screen we found that the settings button did not respond to taps. The cause was layering: it sat in a stack beneath the scroll view, so the scroll view caught every touch. Reordering the stack fixed it. It was fixed in the same build as the redesign.

## Still to come

Six bottle stoppers and five bottle skins are designed, but only the default look ships so far. The structure can grow into them. New pouring animations and haptics are also not in yet; the existing behavior stays.
