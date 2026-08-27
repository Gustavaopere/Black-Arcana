# 05.02 — Radial Wheel

## Objective
Provide a compact spell selector rather than persistent screen clutter.

## Design targets
6–10 visible slots per ring, icon + short name, cooldown/resource affordance, nested domain/loadout navigation only if usability remains fast.

## Requirements
- Rendering is client-only.
- Selection never triggers a cast until explicit input.
- Handles unavailable/locked spells distinctly.
- Scales safely across GUI scales/aspect ratios.

## Acceptance
Visual/manual test matrix at common resolutions and GUI scales; no input lock after closing wheel.
