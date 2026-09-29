# Simply Swords: Cataclysm — 1.0.2+1.21.1+neoforge

Status: `✅ CATALOGED / PHYSICAL IDENTITY CLOSED / COMPLETE 4-ACTION OBJECT CATALOG / EXACT-VERSION SOURCE-PINNED INVENTORY 4 / ACTIVE CONFIG SURFACE OPEN / +0 STRICT`

> Folder-prefix rule (2026-09-29): **✅ means the current semantic/action denominator is fully cataloged and materialized.** Deployed config, reachability or runtime QA may still keep individual identities conditional or outside the strict numerator; those conditions remain documented here and do not make the folder structurally partial.

## Current physical authority

- sibling checkpoint: `neoforge-rpg-skilltree@9f24bf2f02a02f4a0ad067ed2c43b4eeb8a8b532`;
- physical row: `#501`;
- JAR: `simplycataclysm-1.0.2+1.21.1+neoforge.jar`;
- mod id: `simplycataclysm`;
- runtime: `1.0.2+1.21.1+neoforge`;
- physical SHA-1: `a2aa0f82ae3a9be2f43a4d47b3cb2201dd4e1469`;
- hosts: Simply Swords `1.70.2-1.21.1`, L_Ender's Cataclysm `3.33`.

## Exact-version public source pin

Official repository:
`Cephelo/SimplyCataclysmMod`

Exact NeoForge 1.21.1 source branch:
`1.21.1-neo`

Release-correlated source checkpoint:
`a81158e53b2d215ff534fa59732edd08cfd1d4f4`

At that checkpoint `gradle.properties` declares:

- `minecraft_version=1.21.1`;
- `mod_id=simplycataclysm`;
- `mod_version=1.0.2+1.21.1+neoforge`;
- `mod_license=All Rights Reserved`.

The commit is dated 2025-12-29 and is titled `unbreakable fix`. Its diff bumps `1.0.1+1.21.1+neoforge` to `1.0.2+1.21.1+neoforge` and adds the Unbreakable component to Ignitium, Cursium and Witherite item classes. That matches the official CurseForge 1.0.2 release published on 2025-12-29, File `7391959`, whose changelog is specifically the NeoForge unbreakable fix.

This is sufficient for an exact-version release-correlated source inventory. Physical-JAR ↔ source-build byte equality has not been established, so the evidence class is source-pinned rather than exact-artifact.

## Complete source-level semantic inventory

The exact source tree contains only 13 Java source files. The player-facing special-combat behavior is concentrated in three material item classes:

- `IgnitiumSwordItem`;
- `CursiumSwordItem`;
- `WitheriteSwordItem`.

`AncientMetalSwordItem` and `BlackSteelSwordItem` have no equivalent special trait/ability implementation in the exact source.

The exact English localization closes four named supernatural combat traits, plus a separate `fireproof_unbreakable` property label. The latter is an item property, not an independent supernatural action.

| # | Material owner | Semantic ability | Exact source surface | Disposition |
|---:|---|---|---|---|
| 1 | Ignitium | Blazing Brand | hit-triggered stacking brand + armor/toughness reduction/lifesteal behavior | inventory closed |
| 2 | Cursium | Accursed Rage | hit-triggered self-rage stack + Cursium bonus damage | inventory closed |
| 3 | Witherite | Mecha Pulse | charge → threshold → shockwave/stun/extra-damage → cooldown state machine | inventory closed |
| 4 | Witherite | Mecha Smite | hit-triggered Wither/fire branch plus conditional self-regeneration branch | inventory closed |

Status effects, particles, sounds, individual weapon items, recipes, material families, stat modifiers and `Fireproof & Unbreakable` are not additional semantic identities.

Therefore the **complete exact-version source inventory is four provider-owned supernatural weapon abilities**.

Object-level catalog: [ACTION-CARDS-1.0.2.md](ACTION-CARDS-1.0.2.md).

## Why the strict contribution remains +0

The same exact source registers `SCConfig.SPEC` as a NeoForge `ModConfig.Type.STARTUP` configuration and exposes numerical gates that can suppress the action surface.

Relevant exact source keys include:

- `accursedRageChance` — source comment explicitly says setting 0 disables the trait;
- `blazingBrandChance` — source comment explicitly says setting 0 disables the trait;
- `mechaPulseChargeChance` — source comment explicitly says setting 0 disables the trait;
- `mechaSmiteHarmfulEffectsChance` — source comment explicitly says setting 0 disables the harmful proc;
- `mechaSmiteFireDuration` — source comment explicitly says setting 0 disables fire;
- `mechaSmiteWitherDuration` — source comment explicitly says setting 0 disables Wither;
- `mechaSmiteRegenChance`, `mechaSmiteRegenUsesPercentage`, `mechaSmiteRegenPercentage` and `mechaSmiteRegenThreshold` — jointly determine whether the restorative branch is causally reachable.

The deployed pack's effective STARTUP values have not been authoritatively captured. Archived current-instance debug logs do confirm that NeoForge loaded and watched `config/simplycataclysm-startup.toml`, but those logs do not expose the values. Source defaults are not substituted for deployed state.

Accordingly:

- semantic denominator for this provider: **exactly 4 source-pinned identities**;
- current active/reachable subset: **conditional / unresolved**;
- strict global contribution: **+0 pending deployed config evidence**.

This separates inventory closure from current-pack activation.

## Deduplication / ownership

- Simply Swords owns its base weapon archetypes and shared weapon framework.
- L_Ender's Cataclysm owns source materials, original mob/boss content and its native effects.
- Simply Swords: Cataclysm owns the four cross-provider combat abilities above.
- Reusing the name/icon/theme of Cataclysm's Blazing Brand does not create a second Cataclysm identity in addition to the provider-owned weapon trait; the provider action is counted once at its causal root.
- Provider status effects such as `accursed_rage`, `pulse_charge` and `pulse_cooldown` are state/effect machinery, not additional player actions.
- Black Arcana must not duplicate weapon proc execution, effect application, lifesteal, stun/cooldown or item state.
- RPG Skill Tree remains sibling authority only for progression/attributes/Mastery/perks/gates through real contracts.

## Current closure gate

To promote any of the four identities into the strict current-pack numerator, capture authoritative deployed STARTUP config values for the physical 1.0.2 JAR and classify each action as active or disabled.

Minimum required evidence:

1. physical fingerprint still matches SHA-1 `a2aa0f82ae3a9be2f43a4d47b3cb2201dd4e1469`;
2. effective `accursedRageChance`;
3. effective `blazingBrandChance`;
4. effective `mechaPulseChargeChance`;
5. effective `mechaSmiteHarmfulEffectsChance`;
6. effective `mechaSmiteFireDuration`;
7. effective `mechaSmiteWitherDuration`;
8. effective `mechaSmiteRegenChance`;
9. effective `mechaSmiteRegenUsesPercentage`;
10. effective `mechaSmiteRegenPercentage` and `mechaSmiteRegenThreshold` so the selected threshold mode can be evaluated.

Do not infer those values from upstream defaults. The read-only deployed-evidence collector has a bounded route that fingerprints the physical JAR and reads only these ten keys from `config/simplycataclysm-startup.toml`.

## Runtime QA remains separate

Even after config closure, assembled runtime QA remains separate for:

- one proc per logical hit;
- amplifier boundaries;
- lifesteal exactly once;
- Mecha Pulse threshold/cooldown behavior;
- stun/Wither/fire interactions;
- multiplayer attacker ownership;
- config/client presentation agreement;
- 1.0.2 unbreakable regression;
- recipe/smithing behavior.

## Result

**✅ Catalog complete — exact-version source inventory closed at 4; deployed STARTUP config remains open.**

Inventory: **4 provider-owned supernatural weapon abilities**.

Strict global delta: **+0** until deployed STARTUP config proves current activation.