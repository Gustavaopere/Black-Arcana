# Stage 05 — Modpack Casting-Surface Coexistence — Presentation

## State

`DEFERRED VISUAL/CLIENT ACCEPTANCE`

Runtime/provider authority is defined by `plans/05-casting-ux/🟡-PENDENTE-06-modpack-coexistence.md`. This document owns the client-facing coexistence half only.

## Default presentation strategy

Use side-by-side coexistence rather than forced UI unification:

- Black Arcana HUD remains contextual/transient;
- no permanent Black Arcana mana/resource bar;
- HUD anchor and scale remain configurable;
- direct quick-cast mappings remain unbound by default unless a later reviewed UX decision changes that;
- do not duplicate another provider's persistent mana bar, spell slots, cooldown wheel, key labels or progression UI;
- Black Arcana may show concise Black Arcana-authored denial/risk/context feedback even when invocation is hosted elsewhere.

## Spell Actionbar / Iron's client coexistence

Validate the assembled pack rather than assuming a layout from mod presence. The Black Arcana UI must not obscure or replicate provider-owned information. When `black_arcana:irons_integration_probe` is legitimately surfaced through Iron's, observe whether Black Arcana result/denial/hazard feedback remains readable alongside Spell Actionbar.

The visual layer may adapt its own anchor, scale, density and line count. It must not patch another mod's renderer through brittle mixins merely to obtain a preferred layout.

## Epic Fight / EFIS presentation

Real-client QA should exercise Black Arcana radial/HUD and the legitimate Iron's-hosted probe both outside and inside Epic Fight battle mode where the installed UI permits it. Record:

- radial open/close and pointer/key restoration;
- no stuck mouse/key state;
- no client crash during combat-mode or animation transitions;
- no material HUD readability loss;
- whether the hosted Black Arcana action has an animation/presentation mismatch.

A visual/animation mismatch is classified separately from server cast correctness and does not authorize changes to gameplay authority.

## Keybinding and discovery UX

Use ordinary Minecraft key mappings so Controlling and the vanilla controls screen can discover/rebind them. Audit the actual installed keymap before changing defaults. Validate `R`, `V`, the unbound loadout-editor mapping and optional quick-cast bindings in the assembled pack, including persistence after restart.

Keyboard/mouse is the guaranteed baseline while no controller provider is verified. Controller-specific presentation/input mapping is deferred until an actual provider/version/API exists.

## HUD overlap matrix

Observe the Black Arcana contextual HUD with installed external casting/combat UI at the client combinations supported by the real game, including the established Stage 05 matrix around 854×480, 1920×1080 and 3440×1440; GUI scales Auto/2/3/4 where available; each Black Arcana anchor; and HUD scales 0.5×/1×/2×.

Record whether Black Arcana covers provider action bars/hotbar, external UI covers Black Arcana denial/danger text, tooltips obscure interactive controls, or F1/hidden-GUI behavior is incoherent.

Conflict resolution order:

1. move/rescale Black Arcana through its own configuration;
2. reduce transient density/line count;
3. use a supported layout-reservation boundary only when one is proven;
4. otherwise document a recommended Black Arcana anchor rather than rewriting external configuration.

## Authority constraint for all presentation QA

Client coexistence must never create a second cast, cost, cooldown, target or gate authority. One visual/provider action must still terminate in the runtime contract defined by the numbered Stage 05 plan.

Historical full pre-extraction detail is preserved at `plans/visual-production/_migration-source/05-casting-ux/06-modpack-coexistence.pre-extraction.md`.