# Visual 05.04 — Accessibility Presentation

## Goal

Allow players to reduce clutter, motion, flashes and presentation intensity without changing gameplay or requiring a separate accessibility cast path.

## Semantic redundancy

Selected, focused, blocked, cooldown, danger, unavailable and result states should use text/icon/shape/outline/pattern or another semantic channel in addition to color. Do not solve ambiguity with a palette-only “colorblind mode”.

## Text/layout

- wrap/truncate safely while preserving the important semantic prefix/state;
- keep translated strings inside the viewport;
- use translation keys for player-facing labels;
- test deliberately long strings where layout changes materially.

## Reduced motion

Screen shake, camera sway, radial transitions, zoom, vignette motion or screen distortion must consult the preference when applicable. Reduced motion may remove decorative camera movement, shorten/disable transitions or replace motion with static emphasis. It may not change target position, cast timing or outcome.

## Reduced flashes

Bright flashes, repeated full-screen pulses or high-frequency luminosity must consult reduced-flashes. Substitute lower-intensity/static emphasis while preserving essential information.

## Particle density

The multiplier controls Black Arcana presentation particles only. Zero may suppress nonessential local particles; lower values reduce density. Gameplay-critical telegraphs require a non-particle fallback when zero density would hide them. Particle density never changes server hitboxes, area, damage, hazard or world mutation.

## Feedback levels

- `MINIMAL`: retain authoritative denial/essential state, suppress ordinary chatter.
- `STANDARD`: default combat readability with selected/contextual danger/gate information as relevant.
- `VERBOSE`: may include bounded success/additional supported details while obeying clutter budgets.

## Additional visual tasks

- original semantic icon vocabulary for selected/cooldown/danger/blocked/unavailable/warning;
- complete keyboard-focus visibility for UI navigation;
- high-contrast review against real bright/dark/complex game scenes;
- sound must never be the only carrier of success/denial/danger;
- optional haptics are supplemental only;
- coexistence review with the actual modpack HUD/tooltip stack;
- localization-sensitive layout validation.

## Visual QA

Exercise contextual HUD enabled/disabled, every scale/anchor, all feedback levels, reduced motion/flashes on applicable effects, particle density `0/0.5/1`, representative scene contrast, long translations and assembled-pack HUD/tooltip overlap.
