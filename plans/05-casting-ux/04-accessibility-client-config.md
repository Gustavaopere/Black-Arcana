# 05.04 — Accessibility & Client Configuration

## State

`IMPLEMENTED / FINAL VALIDATION DEFERRED`

This document records the current client configuration contract and the executable plan for accessibility/presentation completion. Planned behavior is not an implementation claim unless explicitly marked current.

## Goal

Let players reduce clutter, motion, flashes and presentation intensity without changing gameplay or creating a separate accessibility-specific cast path.

Accessibility in Stage 05 means:

- all core casting actions remain rebindable;
- important state is communicated through more than one visual channel where practical;
- small screens/GUI scales remain usable;
- motion/flash/particle intensity can be reduced when Black Arcana effects use them;
- configuration failure/reset falls back safely;
- optional input-provider support never becomes mandatory for core casting.

## Current canonical options

`BlackArcanaClientConfig` currently exposes:

- contextual HUD enable/disable;
- HUD scale: `0.5–2.0`;
- HUD anchor;
- selection duration;
- feedback duration;
- feedback level (`MINIMAL`, `STANDARD`, `VERBOSE`);
- radial behavior (`TOGGLE`, `HOLD`);
- client particle-density multiplier: `0.0–1.0`;
- reduced-motion preference;
- reduced-flashes preference.

These values are registered as `ModConfig.Type.CLIENT`.

## Authority rule

Client preferences may reduce or reshape presentation but never alter:

- damage;
- spell power;
- range;
- cooldown;
- resource cost;
- progression;
- target admission;
- Arcane Danger admission or settlement;
- Corruption/Strain;
- `WorldEffectPolicy`;
- server-side ritual/domain state.

Client config values are not gameplay-authority inputs to cast validation packets.

## Current input accessibility baseline

- radial, selected cast and loadout editor are ordinary rebindable Minecraft mappings;
- quick-cast mappings are optional and unbound by default;
- no gameplay-critical action requires a side mouse button;
- `TOGGLE` and `HOLD` radial behavior provide two interaction styles;
- GUI focus suppresses cast input.

## Accessibility design rules

### 1. Do not rely only on color

Selected, hovered, blocked, cooldown, danger and unavailable states should use text, iconography, outline/pattern or other semantic markers in addition to color.

Do not add a generic "colorblind mode" merely to recolor the same ambiguous states. First make state semantics independent of palette.

### 2. Text must remain bounded

- wrap or truncate safely;
- preserve the important semantic prefix/state;
- do not allow translated strings to leave the viewport;
- use translatable components for player-facing labels;
- test longer translations when layout changes materially.

### 3. Motion is optional presentation

Any future Black Arcana screen shake, camera sway, radial animation, zoom, vignette motion or spell-screen distortion must consult the reduced-motion preference where applicable.

Reduced motion may:

- remove nonessential camera movement;
- shorten/disable decorative transitions;
- replace motion with static emphasis.

It may not change target position, cast timing or gameplay outcome.

### 4. Flashes are optional presentation

Any future bright flash, full-screen pulse, repeated strobe-like emphasis or high-frequency luminosity effect must consult reduced-flashes.

Reduced flashes may substitute a lower-intensity/static indication but must preserve essential information.

### 5. Particles are presentation density

The client multiplier is intended for Black Arcana particles only.

Rules:

- `0` may suppress nonessential local particles;
- `0.5` reduces client density;
- `1` keeps normal intended density;
- the multiplier never changes server hitboxes, area, damage, hazards or world effects;
- gameplay-critical telegraphs need a non-particle fallback if zero density would otherwise hide required information.

## Feedback-level plan

### MINIMAL

Goal: lowest clutter.

- authoritative denial remains visible;
- ordinary selection/success chatter is suppressed;
- no forecast/gate requests should be generated solely for presentation that MINIMAL will not display when the current controller contract permits avoiding them.

### STANDARD

Goal: default combat readability.

- selected spell/context may appear;
- danger/gate context may appear when relevant;
- routine success spam remains suppressed.

### VERBOSE

Goal: diagnostic/high-information presentation.

- includes STANDARD information;
- may include bounded success feedback and additional supported presentation details;
- must still obey screen bounds and anti-clutter budgets.

## Radial behavior plan

### TOGGLE

- press opens;
- the same open key may close predictably;
- selection closes;
- closing must restore normal input state.

### HOLD

- press/hold opens;
- release closes;
- release must not leave a stuck key/cursor state;
- selection remains non-casting.

Neither mode changes server cast semantics.

## Client-config persistence and recovery plan

### Persistence

Preferences should survive normal client restart through NeoForge client config.

### Missing entries

When a new option is added or an old entry is absent:

- use the registered default;
- do not crash on missing client preference;
- do not migrate missing presentation state into server data.

### Invalid/out-of-range values

Use `ModConfigSpec` bounds/enums to reject/coerce through supported NeoForge behavior rather than custom unsafe parsing.

### Reset

A normal supported config reset must restore documented defaults without affecting server-owned loadout/cooldown/progression state.

## Planned accessibility refinements

The following are `PLANNED / NOT YET CLAIMED AS IMPLEMENTED`.

### 1. Semantic icon pass

Define a small original Black Arcana icon vocabulary for:

- selected;
- cooldown;
- danger;
- blocked;
- unavailable;
- warning.

Icons supplement text and must be original/project-owned or otherwise license-compatible.

### 2. Keyboard-only radial operation

Plan a complete keyboard-only selection path so mouse precision is not mandatory for radial selection.

Requirements:

- selection remains separate from casting;
- no hidden default conflicts;
- focus state is visible;
- page navigation works;
- close/cancel works;
- real-client validation covers stuck-input recovery.

### 3. High-contrast readability review

Review current backgrounds, outlines and text against real game scenes without relying on exact custom color claims from static code alone.

If readability fails:

- prefer stronger panel/background contrast and semantic outlines;
- preserve configurable scale;
- avoid large permanent opaque panels.

This is a real-client visual task, not a static-code PASS.

### 4. Sound/haptic-equivalent policy

Do not make sound the only carrier of success/denial/danger state.

If future optional controller providers expose haptics, haptics are supplemental presentation only and must not be required to understand or execute a cast.

### 5. Controller/gamepad integration boundary

Historical Stage 05 goals included controller accessibility where practical, but the current physical modlist does not contain a confirmed general controller framework.

Current disposition: `OPTIONAL / PROVIDER-DEPENDENT / NOT A STAGE-05 COMPLETION BLOCKER`.

If a controller provider is later installed:

1. confirm exact presence/version/mod id from the physical modlist;
2. inspect supported API/docs/source for that exact version;
3. map actions onto existing Stage 05 intent methods;
4. do not create a second client cast engine;
5. keep keyboard/mouse behavior unchanged when the provider is absent;
6. fail closed if the provider API is incompatible.

No speculative controller class/method/API name is authorized by this plan.

## Large-modpack compatibility

`Controlling 19.0.5` is present in the current physical modlist. Black Arcana benefits from remaining ordinary Minecraft key mappings, but must not take a hard dependency on Controlling for gameplay.

The modpack also contains multiple tooltip/HUD-related mods. Therefore:

- keep Black Arcana's contextual layer bounded;
- avoid invasive replacement of vanilla HUD systems;
- test tooltip/layout overlap in the real pack;
- do not assume another mod's rendering order without direct observation;
- treat real overlap regressions as client-compatibility findings rather than hiding them with arbitrary z-order hacks.

## Localization plan

Every new player-facing control/config/state label should use translation keys.

For layout-sensitive changes:

- test at least the default project language plus a deliberately longer-string fixture/translation when practical;
- never size critical hit regions solely from English text assumptions;
- missing translation falls back without altering gameplay state.

## Test plan

### Pure/unit

- enum/default values;
- configured bounds;
- feedback-level state decisions;
- reduced-mode presentation branching where deterministic;
- keyboard-focus/radial state helpers;
- layout containment with longer labels where feasible.

### Config integration

- normal restart persistence;
- missing entry/default recovery;
- enum fallback behavior through supported NeoForge config handling;
- settings remain `CLIENT` only;
- no gameplay packet/value changes from presentation preferences.

### Real client

- HUD enabled/disabled;
- scale 0.5/1/2;
- every anchor;
- `MINIMAL/STANDARD/VERBOSE`;
- `TOGGLE/HOLD`;
- reduced motion/reduced flashes where an applicable effect exists;
- particle density 0/0.5/1 where applicable;
- reset/missing-entry recovery;
- readability over representative bright/dark/complex backgrounds;
- tooltip/HUD coexistence with the actual pack;
- keyboard-only operation if implemented.

## Deferred acceptance

Local persistence, missing-entry migration/default behavior and the perceptual quality of reduced-motion/reduced-flash presentation remain part of the real-client manual matrix where direct observation is required.

Future effects that do not yet exist are not fake-PASSed. They remain `NOT APPLICABLE / CARRIED TO STAGE 09` when the canonical matrix authorizes that disposition.

## Exit criteria

05.04 is fully validated only when:

- client settings persist/recover safely;
- no setting changes gameplay authority;
- required casting actions remain rebindable;
- core information remains understandable without relying only on color/motion/flash/particles;
- `TOGGLE/HOLD` are directly observed;
- reduced preferences are consumed by every applicable implemented effect;
- actual pack HUD/tooltip coexistence has direct evidence where required;
- applicable manual matrix rows are closed honestly.
