---
title: Levels come from a solver, not from luck
summary: A random shuffle can leave a level unsolvable. We generate every level ahead of time and prove it can be finished.
date: 2026-11-15
time: 19:10
---
A sorting puzzle has a trap: shuffle the marbles at random and some layouts simply cannot be solved. Nobody enjoys finding that out on move forty.

## The decision

Levels are not generated while you play. A solver builds them before the app ships, and the app bundles the result as a static file: for each level, the bottle layout and the **fewest moves** needed to solve it. The app only reads levels through one small interface, so how they are made can change without touching the screens.

We chose this because a pre-built level is guaranteed to be solvable, and because knowing the minimum lets the app show it next to your best result.

## How a level is made

- Start from n colors with a fixed random seed: n bottles filled, plus 2 empty ones.
- Search for a solution. The first prototype used a depth-first search with a cap of 60,000 states.
- The search skips moves that cannot help: touching a bottle that is already finished, pouring into empty bottles more than once, moving a single marble from a one-marble bottle into an empty bottle.
- A state is stored as the sorted list of bottles, so two layouts that only differ in bottle order count as the same.
- Then find the fewest moves: breadth-first search for small levels, iterative deepening for big ones.
- Levels that are unsolvable, already solved, or too easy are thrown away. What is left is sorted from easy to hard.

## Checking it

The plan includes a test that re-solves every bundled level, and the first playable version aimed for at least 30 levels. The landing page now says 150.
