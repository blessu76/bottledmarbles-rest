---
title: How hints and the extra bottle work
summary: Hints show the next move, and the extra bottle adds one empty bottle to a level. Here is what each does, the small limit per round, and how a helped round is recorded.
date: 2026-11-21
time: 14:45
---
Bottled Marbles has two ways to get unstuck: a hint and an extra bottle. Neither is needed to finish a level, and neither involves watching anything.

## What a hint does

A hint shows you the next move. The game works it out with a solver, so the move it points to is one that can lead to a solution. It tells you one move at a time, not the whole answer.

## What the extra bottle does

The extra bottle adds one empty bottle to the level, which gives you more room to sort marbles. In the version we are testing, you can use it once per level, and a hint once per round.

## How a helped round is recorded

If you use a hint or add a bottle, the round is marked as assisted. Both of them can make a level take fewer moves, so a round you finished without help takes the place of an assisted record, and an assisted record never replaces an unassisted one. Using help never blocks your progress: you can still finish the level and move on.

## What stays the same

Undo is free and unlimited, and it does not count as help. The perfect challenge hides hints and the extra bottle altogether. These limits and the way purchases may change them can still change before release, and we will write about it here first.
