# Stage 05 — Casting Runtime & Client Contract Master Plan

## Scope after visual-production extraction

Stage 05 remains the engineering authority for direct casting input, server-owned loadouts, client/server presentation-data boundaries, synchronization, stale-state handling and safe client intent.

UI/HUD composition, information architecture, visual semantics, iconography, textures/resources, targeting presentation, spell inspection, VFX, audio, animation and contextual help are planned separately under `plans/visual-production/05-casting-ux/`.

The visual backlog is not part of the numerical runtime implementation sequence unless a specific presentation contract is required for gameplay safety or release acceptance.

Under D035, required physical/real-client/provider-real observations are consolidated in Stage 09 after their originating runtime/integration contracts and deterministic gates are complete. They remain release-blocking PENDING evidence and are never inferred as PASS.

## Non-negotiable architecture

- The client proposes bounded intent; the server decides cast legality and outcome.
- Loadouts are bounded, persistent, server-owned state.
- Selection is not casting.
- Client preview/forecast state is advisory and server-authored when it describes gameplay facts.
- Client configuration may change presentation only, never damage, power, range, cost, cooldown, progression, targeting, Arcane Danger or world effects.
- Synchronization is event-driven and bounded; no per-tick full-state stream.
- Provider resources and provider-owned gameplay state remain provider-owned.
- Dedicated-server startup must not classload physical-client presentation classes.

## Canonical engineering plans

1. `✅-01-input-loadouts.md` — input/loadout authority, persistence, session behavior and network intent.
2. `✅-02-radial-wheel.md` — radial selection runtime contract; presentation is delegated to visual production.
3. `✅-03-contextual-hud.md` — synchronized feedback/data/correlation contract; HUD composition is delegated to visual production.
4. `✅-04-accessibility-client-config.md` — client-config authority/persistence contract; visual accessibility behavior is delegated to visual production.
5. `✅-05-final-client-validation-handoff.md` — runtime/input/full-pack validation handoff. Visual-only QA is delegated to visual production.
6. `✅-06-modpack-coexistence.md` — authority/input/provider coexistence. Visual overlap/readability fixes are delegated to visual production.
7. `✅-07-presentation-data-contracts.md` — authoritative gate for whether data is safe to render at all.

Former 05.08–05.16 presentation plans and their implementation checkpoints now live under `plans/visual-production/05-casting-ux/`.

## Runtime flow

`key/input -> bounded client intent -> network ingress -> canonical server coordinator -> identity/loadout -> progression -> cooldown/resource/target/world/hazard gates -> effect settlement -> bounded result/snapshot -> client presentation`

Nothing in visual production may add a parallel cast path or convert local UI state into admission authority.

## Visual handoff rule

Engineering plans expose only the minimum stable facts needed by a presentation surface. They do not freeze final layout, palette, icons, textures, models, particle style, sound, animation or screen composition.

When a desired visual requires a new gameplay-derived datum, the change starts here or in `05.07` as a bounded server-authored contract. The visual plan cannot infer or synthesize that datum from resource ids, local timers, particles, world scans or provider heuristics.

See `plans/visual-production/MIGRATION-MAP.md` for the extraction audit.
