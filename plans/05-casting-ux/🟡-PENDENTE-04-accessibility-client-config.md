# 05.04 — Accessibility Client Configuration — Authority Contract

## State

`IMPLEMENTED / PHYSICAL CONFIG VALIDATION PENDING`

Visual accessibility behavior is owned by `plans/visual-production/05-casting-ux/04-accessibility-presentation.md`.

## Canonical client options

`BlackArcanaClientConfig` exposes contextual HUD enable/disable, HUD scale `0.5–2.0`, HUD anchor, selection duration, feedback duration, feedback level, radial behavior (`TOGGLE`/`HOLD`), Black Arcana particle-density multiplier `0.0–1.0`, reduced-motion preference and reduced-flashes preference. These values are `ModConfig.Type.CLIENT`.

## Authority rule

Client preferences may reduce or reshape presentation but never alter damage, spell power, range, cooldown, resource cost, progression, target admission, Arcane Danger admission/settlement, Corruption/Strain, world-effect policy or server ritual/domain state.

Client config values are not gameplay-authority fields in cast-validation packets.

## Input accessibility baseline

Core casting actions remain ordinary rebindable mappings. Quick-cast mappings are optional/unbound by default. No gameplay-critical action requires a side mouse button. `TOGGLE` and `HOLD` provide two radial interaction styles. GUI focus suppresses cast input.

## Persistence/recovery

Preferences persist through supported NeoForge client config. Missing entries use registered defaults; bounds/enums use supported `ModConfigSpec` handling; a normal reset restores documented defaults without altering server-owned loadout/cooldown/progression state.

## Controller/provider boundary

General controller support is optional/provider-dependent until an exact provider/version/API is confirmed. A future adapter maps onto existing intent methods, keeps keyboard/mouse functional without the provider and never creates a second client cast engine.

Controlling may aid key discovery but is not a hard dependency.

## Engineering tests

Cover enum/default/bounds, persistence/default recovery, settings remaining client-only, no gameplay packet/value changes from presentation preferences, radial interaction semantics and safe session teardown.

`ClientConfigAuthorityContractTest` deterministically anchors the current enum/default/bound contract, proves registration through the `Dist.CLIENT` entrypoint as `ModConfig.Type.CLIENT`, and fails if `BlackArcanaClientConfig` leaks into `ClientInputController` or any `network/**` Java source. This is machine-level authority-isolation evidence only; it does not replace normal client-config persistence/recovery or physical input observation.

`RadialToggleInputTest` covers the bounded TOGGLE/HOLD close-decision semantics in production code. `ClientInputAuthorityWiringTest` covers ordinary rebindable mappings and GUI-focus fail-closed wiring. These deterministic tests support, but do not satisfy, the required physical-client acceptance below.

## Remaining engineering acceptance

- config persists and recovers through normal client lifecycle;
- toggle/hold input semantics are directly observed;
- no preference affects gameplay authority in the physical client;
- core keyboard/mouse actions remain usable without optional providers.

Perceptual contrast, reduced-motion/flash behavior, particle visual density, visual redundancy, localization layout and HUD/tooltip overlap are delegated to visual production.
