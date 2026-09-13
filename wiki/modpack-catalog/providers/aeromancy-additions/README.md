# SnackPirate's Aeromancy Additions 1.2.8 — provider dossier

Status: `COUNTED_SOURCE_PINNED / 10 REGISTERED SPELL IDENTITIES / COMPONENT #64 / CURRENT-HOST RUNTIME QA OPEN`

Physical authority: current 595-entry modlist (`SHA-1 7aaece7acbfb07ba4d0c66029042f36c50d046f0`)
Physical JAR: `aero_additions-1.2.8.jar`
Physical mod id/version: `aero_additions` / `1.2.8`
Physical JAR SHA-1: `dee32c9fa84d6e39846608f8f77591ea56f`
Physical CurseForge hash: `3079423735`
Exact public source: `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`
Exact source tree: `fcee08e613fbfa030f034268a0240c8693ab7f45` (`truncated=false`)

## Provider identity

Aeromancy Additions is a mixed Iron's Spells content provider. It owns a Wind school, ten active Iron's `AbstractSpell` registrations, spell-support effects/entities, school gear/items and acquisition support. It is not a UI-only, library-only or compatibility-only component.

The active spell registry at the exact source pin contains exactly:

- `aero_additions:wind_charge`
- `aero_additions:updraft`
- `aero_additions:airstep`
- `aero_additions:asphyxiate`
- `aero_additions:feather_fall`
- `aero_additions:wind_shield`
- `aero_additions:airblast`
- `aero_additions:wind_blade`
- `aero_additions:flush`
- `aero_additions:dash`

`TornadoSpell`, `ThunderclapSpell`, `SummonBreezeSpell`, `TelelinkSpell` and `ShapeshiftSpell` remain present in source/support assets in varying degrees but their `registerSpell(...)` lines are commented out at the audited pin. They are not registry identities and are not counted.

## Registration and authority

`AASpells` creates the provider spell `DeferredRegister` against Iron's `SpellRegistry`. `Aeromancy` calls `AASpells.register(modEventBus)` directly during mod construction. No provider configuration branch around registration was found, and targeted search found no `ForgeConfigSpec`, `ModConfig` or `BooleanValue` gate that conditionally creates/removes these ten identities.

Iron's remains authority for host spell registration/casting, mana, cooldown and Scroll Forge behavior. Aeromancy owns the concrete Wind spells and their provider-specific effects/state. Black Arcana may catalog or later adapt through a verified boundary; it must not duplicate Iron's/Aeromancy casting, cost settlement, cooldowns, projectiles/effects or provider state.

## Host-native reachability

The Wind school is created with Iron's seven-argument `SchoolType` constructor. In Iron's 3.16.3 this defaults to `requiresLearning=false` and `allowLooting=true`.

Provider data puts `minecraft:breeze_rod` in the Wind focus tag and in the host `irons_spellbooks:school_focus` tag. Iron's 3.16.3 Scroll Forge enumerates spells for the matched school and then applies `allowCrafting`, `isEnabled` and `canBeCraftedBy`. Host `DefaultConfig` defaults `enabled=true` and `allowCrafting=true`; `canBeCraftedBy` only adds the learning gate, which Wind does not require. No Aeromancy override of these gates was found for the ten registered classes.

The provider also wires Breeze Rod survival support into Trial Chambers: `data/neoforge/loot_modifiers/global_loot_modifiers.json` registers `aero_additions:trial_chamber_modifiers/normal_vault_modifier`; that modifier targets `minecraft:chests/trial_chambers/reward` and appends `aero_additions:chests/trial_chambers/normal_vault_add`; the appended table contains `minecraft:breeze_rod` with weight 6 and count 5–10. The provider additionally supplies independent embedded-spell item routes for Updraft (`Updraft Tome`) and Wind Blade (`Wind Sword`). These item/support surfaces strengthen reachability evidence but are not counted as extra spell semantics.

Catalog-level conclusion: the ten registered Wind spells have a source-pinned provider/host-native acquisition path, subject to physical-pack configs and runtime behavior that remain QA gates.

## Dependency/version boundary

Source 1.2.8 targets Minecraft 1.21.1, NeoForge 21.1.228 and Iron's 1.21.1-3.16.1. Generated metadata declares Iron's required range `[1.21.1-3.15.0,1.21.1-4.0.0)` and ExpandAbility `[12.0.0,13.0.0)`.

The physical pack uses NeoForge 21.1.248, Iron's 3.16.3 and embeds ExpandAbility 12.0.0 in the Aeromancy JAR. Those values satisfy the provider's declared dependency ranges where applicable, but version-range acceptance is not assembled-runtime PASS evidence.

## Semantic disposition

Aeromancy contributes **+10 `COUNTED_SOURCE_PINNED`** semantic magic objects. The shared-ledger reconciliation promotes the strict minimum from **1322 to 1332** and closes provider component **#64 / 64 of 100**.

This is a catalog/source-pinned promotion only. No assembled-pack runtime PASS is claimed: current-pack client/server boot, required mixins, payload behavior, physical Scroll Forge/config behavior and representative casts remain direct QA gates.

The promotion becomes canonical only after this reconciliation is merged to `main` and the exact merge SHA passes the project post-merge CI gate.

## Clean-room boundary

This audit records identifiers, registry counts/types, dependency declarations, host-contract relationships, mixin/network footprint, acquisition relationships and compatibility risks. It does not copy provider implementation bodies, assets, localization prose, models, sounds or balance text into Black Arcana.