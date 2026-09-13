# Visual 05A.11 — Arcane Danger HUD & Tooltip Presentation

## Purpose

Communicate danger clearly before casting using only the bounded server-authored data defined by `plans/05a-arcane-danger/11-hud-tooltip-preflight.md`.

## Presentation requirements

- spell tooltip/radial surfaces may show danger tier and concise Arcane Resistance recommendation;
- contextual preflight may show current effective Arcane Resistance, expected risk class and a bounded hard-gate category only when the runtime contract provides it;
- non-normal danger presentation may show current/minimum/recommended resistance plus factual states such as below minimum, below recommended, recommendation met or unavailable;
- recommendation met must never be worded/styled as “safe” or as eliminating Backlash/Corruption risk;
- static danger metadata remains a visual fallback when matching dynamic forecast data is unavailable;
- loadout hover tooltip may present synchronized static preflight without triggering extra prediction/network work;
- Corruption/strain UI remains absent until a bounded synchronized state contract exists.

## Accessibility

Danger and gate state must not rely on color alone. Tooltip/HUD content must remain bounded at required GUI scales and must remain understandable when motion/particles are reduced.

## Visual QA

- verify gate wording and resistance forecast together in a real client;
- verify loadout tooltip placement/readability across required resolutions and GUI scales;
- verify stale reconnect/datapack transitions do not visually resurrect old state;
- verify interaction with Stage 05 accessibility settings and the assembled modpack UI stack.
