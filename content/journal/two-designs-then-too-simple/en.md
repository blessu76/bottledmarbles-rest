---
title: Two design proposals, and one "too simple"
summary: We compared two full design proposals for the app, took ideas from both, and then threw the result away after one piece of feedback.
date: 2026-11-16
time: 12:15
---
Before polishing the app we wrote down two complete design directions and put them side by side.

## The two proposals

- **Glass and ink:** an ink-colored background with a single accent color, so the interface steps back and the marbles are the star. It brought a color-blind symbol mode, a bottom sheet in thumb reach, and a motion story: lift, carry, drop.
- **Clean premium puzzle:** blue-white and navy with layered cards. Its strength was precise numbers you can build from directly, four screen states, a shake on a wrong pour, and an implementation order.

Our notes were honest about weak spots. The first had no semantic colors or error feedback, and its four-column level tiles were tight at 320 px. The second felt generic, and one of its text sizes broke our own rule of 12 sp or more on small screens. Color contrast and color-blind simulation were not verified for either.

We leaned toward the first one for the look and the second one for specs and states.

## Then the feedback

The feedback was short: **too simple**. So we started over instead of adding decoration.

## Version 2: Teal Glass

- Keep what the app already had, teal and gold, and push it further.
- Dark: deep teal ink with gold as the accent. Light: warm paper with a deep teal accent.
- Glass bottles and marbles drawn with gradients and filters so they read as objects, not flat circles.
- It absorbed the best parts of both proposals: ink with one accent, ten marble colors with symbols, bottom sheets, semantic colors, level states, a progress bar, the wrong-pour shake, and the 320 px rules.

The proposal page covers concept, eight screens in dark and light, asset breakdowns, motion, and an accessibility check.
