# Ars Morph 2.0.0 — Systems and authority boundaries

Status: `SOURCE SYSTEMS CLOSED / INSTALLED INTEROP QA OPEN`

## Bootstrap

`ArsMorph` constructor performs:

1. Ars glyph registration through `ArsNouveauRegistry.registerGlyphs()`;
2. common/client setup listener registration;
3. `IdentityReg.preInit()` (currently reserved/no-op).

Common setup calls `IdentityReg.postInit()`, which registers:

- builtin abilities;
- variant adapters;
- morph tick handlers.

`MorphConfig.COMMON_SPEC` registration is commented out.

## Required and optional providers

Runtime metadata requires:

- Minecraft 1.21+;
- Ars Nouveau >= `1.21.1-5.4`;
- Identity2 >= `1.0.0`.

Ars Elemental is not declared as a required metadata dependency. Its Java registrations are reached only from `IdentityReg` when `ModList.isLoaded("ars_elemental")` passes; optional data entries use `required:false` where applicable.

## Morph authority

Identity2 owns:

- current form;
- morph/clear transaction acceptance;
- persistent identity state;
- builtin ability dispatch;
- variant lifecycle;
- capability-tag interpretation;
- provider sync API.

Ars Morph invokes those contracts. It must not be treated as the canonical identity provider.

## Ars authority

Ars Nouveau owns:

- Morph glyph registration/learning framework;
- mana/cast transaction;
- spell context/resolvers/events;
- Mob Jar semantics;
- Ars entity spell fields/colors;
- Ars effects used by morph abilities.

Ars Elemental owns its optional Firenando/Siren/Flashjack entities and homing-projectile behavior.

## Wilden Stalker morph-tick seam

Ars Morph registers one Identity2 morph tick handler for Wilden Stalker.

Server-side path:

- ignore client level;
- require `ServerPlayer` host;
- derive `flying` from not-on-ground + not-in-water, then require the block at `getOnPos()` to be air;
- if current representation is `WildenStalker`, call `setFlying(flying)`;
- call `IdentityApi.syncBoolean(serverPlayer, "isFlying", flying)`;
- catch/log all thrown errors.

The sync call belongs to Identity2's provider transport. It is not a new Ars Morph networking protocol.

## Dormant source class: MorphEffect

`MorphEffect` extends vanilla `MobEffect` and would call `IdentityProgression.clearMorph(player)` when removed from a `ServerPlayer`.

However:

- `ModRegistry` is empty;
- the time-limited-morph config/potion code in `EffectMorph` is commented out;
- no production registration/use of `MorphEffect` was located in the exact tree.

Therefore Phase 2X excludes it from active provider registry/content counts. Packaged-JAR inspection remains the final artifact gate.

## Failure posture

For Black Arcana integration:

- missing Identity2 boundary => fail closed; no fallback morph state;
- missing optional Ars Elemental => do not load/use its classes through BA;
- provider ability exception => do not replay the ability through BA;
- failed Identity2 morph => no BA-side forced morph;
- no safe provider hook => observe only or defer.

## Version drift

Source build vs physical pack:

| Host | Source build | Physical pack |
|---|---|---|
| NeoForge | 21.1.219 | 21.1.248 |
| Ars Nouveau | 5.11.1.1289 | 5.13.1 |
| Ars Elemental | 0.7.9.3.168 | 0.7.10.1 |
| Identity2 | 2.1.1.1 development artifact | 2.2.4 |
| Gabou's Libs | 1.4 development artifact | 1.8.7 |

Version ranges/source compilation establish eligibility, not current runtime compatibility.
