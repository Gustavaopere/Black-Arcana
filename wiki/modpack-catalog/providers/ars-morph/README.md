# Ars Morph 2.0.0

Status: `PHASE 2X — SOURCE CATALOG CLOSED / INSTALLED RUNTIME QA OPEN`

## Exact installed identity

- Mod id: `ars_morph`
- Physical JAR: `ars_morph-1.21.1-2.0.0.jar`
- Runtime version: `2.0.0`
- Physical SHA-1 / Modrinth hash: `68ff47cc58c0ffe9570bb907f65c2910311ed45f`
- CurseForge hash: `1937242939`
- Loader/game: NeoForge 1.21.1
- Pack NeoForge: `21.1.248`
- Required physical morph provider: Identity2 `2.2.4`
- Current physical Ars host: Ars Nouveau `5.13.1`
- Current physical optional Ars host: Ars Elemental `0.7.10.1`
- Physical support library: Gabou's Libs `1.8.7`
- Phase 2 class: `ARS GLYPH / IDENTITY2 COMPATIBILITY PROVIDER`

Physical modlist/JAR identity is authoritative for installed presence/version. The current Notion row labels `Estado no pack: Removido`, but the physical modlist contains the JAR; Phase 2X therefore treats Ars Morph as installed and the property as stale.

## Release-aligned source checkpoint

Provider source used read-only:

`Alexthw46/Ars-Morph@4a5a2c706fe5a316fc9ad03ac37a3ac1d1dc3c58`

This is the head of upstream branch `1.21.1-v2` on 2026-06-12. Its `gradle.properties` declares `mod_version=2.0.0`, and the publisher's 2.0.0 NeoForge 1.21.1 file was released on the same date. Phase 2X therefore classifies it as `RELEASE-ALIGNED`, not byte-identical: the installed JAR was not extracted/rebuilt and compared byte-for-byte.

The upstream checkpoint builds against:

- NeoForge `21.1.219`;
- Ars Nouveau `5.11.1.1289`;
- Ars Elemental `0.7.9.3.168`;
- Identity2 NeoForge `2.1.1.1` through CurseForge file `8153522`;
- Gabou's Libs `1.4` through CurseForge file `7195722`;
- Sauce `0.0.40.82` as a compile-only seam.

The physical pack is newer on Ars, Ars Elemental, Identity2 and Gabou's Libs. Source-catalog completeness does not imply current-host runtime compatibility PASS.

## Provider role and authority

Ars Morph does not own the player's morph state. Identity2 owns identity acquisition/state, variants, ability dispatch and the `morph`/`clearMorph` operations. Ars Nouveau owns spell grammar, spell context/resolvers, glyph learning and Ars entity behavior. Ars Elemental owns its optional entities and spell behavior.

Ars Morph owns only the bridge it adds:

- one Ars glyph that requests Identity2 morph operations;
- Identity2 builtin ability adapters for Ars entities;
- Identity2 variant adapters for Ars/Ars Elemental entities;
- Identity2 entity-capability tags for supported Ars forms;
- one Wilden Stalker morph-tick synchronization seam.

Black Arcana must not create a parallel identity ledger, unlock list, variant serializer or replacement morph pipeline.

## Closed source catalog surface

### Glyph — 1/1

[`GLYPH-MORPH.md`](GLYPH-MORPH.md) closes the only registered spell part:

- `ars_morph:glyph_morph` / Morph;
- Tier II;
- 200 Ars mana;
- Conjuration;
- no compatible augments;
- server-only mutation path through Identity2;
- Mob Jar → Spawn Egg → struck EntityType selection precedence;
- player-target and self-clear semantics;
- strict max-health gate;
- FamiliarEntity rejection;
- Ars `IDecoratable` cosmetic-copy seam.

### Identity2 abilities

[`ABILITIES.md`](ABILITIES.md) closes 7 Java ability adapters and their 11 committed data assignments:

- Weald Walker;
- Wilden Hunter;
- Wilden Stalker;
- Starbuncle;
- Whirlisprig;
- Wixie;
- optional Ars Elemental Firenando.

The Java adapters reuse Ars spell/effect/entity pipelines. Identity2 data owns cooldown/use-duration assignments; those child Ars resolver executions are descendants of one provider ability action and must not be independently replayed by Black Arcana/RPG systems.

### Variants and passive form tags

[`VARIANTS-TAGS.md`](VARIANTS-TAGS.md) closes:

- 5 Ars Nouveau variant adapters;
- 3 optional Ars Elemental variant adapters;
- 6 additive Identity2 entity-type tags;
- exact persistent/variant fields represented by each adapter;
- optional-provider data entries using `required:false`.

### Acquisition

[`ACQUISITION.md`](ACQUISITION.md) records the single committed generated glyph recipe: Conjuration Essence + Abjuration Essence + two `ars_nouveau:wilden_drop` tag ingredients, 55 XP.

### Mixins/network/config

[`MIXIN-NETWORK-BOUNDARIES.md`](MIXIN-NETWORK-BOUNDARIES.md) records:

- 0 common mixins;
- 0 client mixins;
- no Ars Morph-owned custom payload registration identified in the exact source tree;
- `IdentityApi.syncBoolean(..., "isFlying", ...)` is a call into the Identity2 provider contract, not an Ars Morph protocol;
- the standalone `MorphConfig.COMMON` spec is empty and its registration is commented out;
- `max_hp_morph` is a glyph config value built by `EffectMorph` through the Ars spell-part configuration path.

## Critical source observations

1. `max_hp_morph` default is 100, minimum 20, maximum `Integer.MAX_VALUE`; the executable check is strict `<`, so a candidate whose max health equals the configured limit is rejected.
2. When a struck living target is another `ServerPlayer`, that player is the morph recipient. When the struck living entity is not a player, the caster is the recipient.
3. A player target resolving to `EntityType.PLAYER` calls Identity2 `clearMorph` instead of setting a new morph.
4. A valid offhand Ars Mob Jar takes selection precedence; a Spawn Egg is consulted only when the selected type still equals the struck living entity's type.
5. The source creates a candidate entity and passes serialized NBT to Identity2. Black Arcana must not construct a second independent morph representation.
6. Wixie has a source-risk in its crouching branch: the selected good-effect table has 10 entries, but the random index is always bounded by the 12-entry bad-effect table. This is recorded as a runtime-reproduction hypothesis, not a confirmed installed crash.
7. `MorphEffect` exists in source and would clear Identity2 morph on removal, but `ModRegistry` is empty and no registration/use of this effect is present in the audited production path. It is not counted as active provider content.

## Provenance

The exact checkpoint contains conflicting code-license signals:

- `neoforge.mods.toml`: GNU Lesser General Public License v3.0;
- root `LICENSE`: GNU General Public License v3 text.

The publisher page identifies LGPLv3, but the repository conflict is not resolved by inference. Phase 2X uses source read-only for factual compatibility/deduplication evidence and copies/adapts no implementation or asset. Any future derivation remains fail-closed until exact licensing/provenance is reconciled.

## Remaining validation

- extract/inspect the installed Ars Morph JAR and compare packaged source/data/config surfaces;
- boot client and dedicated server with physical Identity2 2.2.4, Gabou's Libs 1.8.7, Ars 5.13.1 and Ars Elemental 0.7.10.1;
- validate glyph learning and all Mob Jar/Spawn Egg/target-selection paths;
- validate strict max-health boundary below/equal/above configured value;
- validate player-target morph/clear behavior and permission/friendly-target consequences in multiplayer;
- validate FamiliarEntity rejection and cosmetic-item transfer;
- validate all builtin ability assignments/cooldowns and provider event cancellation behavior;
- reproduce or refute the Wixie crouching index-risk;
- validate 8 variant adapters and 6 Identity2 tags under current host versions;
- validate Wilden Stalker `isFlying` sync across login/dimension/death/respawn;
- verify optional Ars Elemental classloading/data behavior when that provider is present and when absent;
- verify no `MorphEffect` registration exists in the packaged installed artifact;
- full-pack conflict test against other morph/scale/combat systems.

None of these installed-runtime checks are reported as PASS by Phase 2X.
