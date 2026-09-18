# 05.04 — Accessibility Client Configuration — Authority Contract

## State

`IMPLEMENTED / DETERMINISTIC ACCEPTANCE COMPLETE / REAL-CLIENT VALIDATION CARRIED TO STAGE 09`

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

`ClientConfigAuthorityContractTest` deterministically anchors the current enum/default/bound contract, proves registration through the `Dist.CLIENT` entrypoint as `ModConfig.Type.CLIENT`, and fails if `BlackArcanaClientConfig` leaks into `ClientInputController` or any `network/**` Java source. It also exercises the pinned NeoForge `21.1.248` `ModConfigSpec.correct(CommentedConfig)` path with an in-memory NightConfig document: valid customized preferences survive correction, missing or malformed values recover through registered defaults, and out-of-range numeric values are clamped to the registered bounds by `ModConfigSpec.Range`. This is machine-level config-spec and authority-isolation evidence that completes the Stage 05 engineering gate. Physical config lifecycle/input observation remains PENDING release evidence in Stage 09.

`RadialToggleInputTest` covers the bounded TOGGLE/HOLD close-decision semantics in production code. `ClientInputAuthorityWiringTest` covers ordinary rebindable mappings and GUI-focus fail-closed wiring. These deterministic tests satisfy the current engineering acceptance; the physical-client observations are transferred to Stage 09 under D035.

## Stage 09 carried physical acceptance

Stage 09 must directly observe config persistence/recovery, toggle/hold behavior, gameplay-authority isolation under client preferences, and provider-free core keyboard/mouse usability. These rows remain PENDING and are release-blocking, not Stage 05 implementation blockers.

Perceptual contrast, reduced-motion/flash behavior, particle visual density, visual redundancy, localization layout and HUD/tooltip overlap are delegated to visual production.


## Completion

Under D035, 05.04 is complete for numbered implementation progression.
