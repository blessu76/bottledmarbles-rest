---
title: Four marbles per bottle: the whole rulebook
date: 2026-11-13
time: 22:28
summary: The rules of Bottled Marbles fit on a few lines. Here they are, with the small decisions around them.
---
Bottled Marbles is a sorting puzzle: move marbles between glass bottles until each bottle holds a single color. The whole rulebook is short on purpose.

## The rules, as written down

- A bottle holds **4 marbles**. A level with n colors has 4 × n marbles.
- There are n + 2 bottles: n of them start filled, and **2 start empty**.
- You can pour from a bottle that is not empty into a bottle that is not full, and only onto an empty bottle or onto a marble of the same color.
- You pour the whole run of same-colored marbles on top, as far as the target has room, and that counts as **one move**.
- You win when every bottle is either empty or full of one color.

The number of colors grows with the level: `min(3 + floor((level + 1) / 2), 8)`, so early levels have three colors and later ones stop growing at eight.

## Four and two

Capacity four and two spare bottles come straight from the first prototype. The two empty bottles are the breathing room that makes pouring possible at all, and we have not needed to change either number.

## Small decisions that matter

- Tapping the same bottle again deselects it, and an empty bottle can't be selected.
- Tapping a bottle you can't pour into says so and moves your selection there, instead of silently ignoring the tap.
- Undo is unlimited and takes a move back off the counter. Restart returns the level to its first layout.

These rules came from the first playable prototype and were kept unchanged in the app. The record we keep for each level is the fewest moves you needed.
