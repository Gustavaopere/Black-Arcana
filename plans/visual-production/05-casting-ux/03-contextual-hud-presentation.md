# Visual 05.03 — Contextual HUD & Feedback Presentation

## Philosophy

Show information when it matters; do not create a permanent Black Arcana resource bar by default. Combat readability takes priority over completeness.

## Information hierarchy

When space is constrained, prioritize:

1. authoritative cast denial;
2. authoritative success when the selected feedback level permits it;
3. current hard-block/warning forecast for the selected spell;
4. selected-spell identity/context;
5. lower-value explanation.

Forecast and result meanings must remain visually distinct. Never attribute a result to the currently selected spell unless a safe correlation exists.

## Presentation backlog

Subject to Stage 05 data-contract gates:

- concise cooldown/readiness indication;
- provider-resource/cost summary;
- charge/channel state and progress;
- owner-specific ritual/domain timers;
- concise target-failure category;
- synchronized spell icon and semantic status symbols.

Unavailable data is omitted or marked unavailable rather than visually fabricated.

## Anti-clutter

- no permanent mana/resource bar by default;
- no permanent selected-spell panel while idle;
- no full spell description in combat HUD;
- no repeating success spam in minimal/standard modes;
- no unbounded result/history queue;
- avoid duplicating a provider-owned HUD for the same resource without explicit integration justification;
- overflow requires layout redesign, not off-screen rendering.

## Wording

Preview/preflight is advisory. Authoritative denial is the actual server result. Do not word preview as though it denied a cast.

Danger wording remains factual: below minimum may be a hard threshold when the server says so; below recommended is a warning; recommendation met never means forbidden magic is safe; unavailable never displays guessed effective resistance.

## Accessibility/layout

- never rely on color alone;
- wrap/truncate safely;
- support configured HUD scale and all exposed anchors inside the viewport;
- reduced motion/flash affects decoration, not state truth;
- essential denial/risk information must remain readable without particles or motion;
- follow supported vanilla/NeoForge hidden-GUI semantics rather than creating a parallel overlay stack.

## Visual QA

Validate common/small/ultrawide viewports, supported GUI scales, every anchor and scale, feedback levels, denial timing/readability, hazard states, gate states, F1/hidden GUI, assembled-pack overlap and any newly approved cooldown/charge/channel/timer presentation.
