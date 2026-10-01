# Weapons of Miracles 2.0.178 — exact artifact audit

Status: `EXACT PHYSICAL=PUBLISHER / 64-SKILL REGISTRY CLOSED / OWNER-ACQUISITION SURFACES BOUNDED`

## Physical/publisher identity

Current physical sibling dossier:

- row: **#568**;
- JAR: `WeaponsOfMiracles-2.0.178.jar`;
- mod id: `wom`;
- runtime: `2.0.178`;
- physical SHA-1: `b507eb376778cfd1cbecec2841c38891b26a7349`.

NON-MERGE PR #499 audits CurseForge project/file `918614 / 8829395`.

Evidence checkpoint used here:

- audit HEAD: `542e5a350c39531794ce340b39952d25aa1e65f4`;
- run: `36905999133` — SUCCESS;
- artifact: `11184480812`;
- artifact digest: `sha256:9bb3c7c94092c79cd394bf4a9c51518d38225c0ef013a7072dfade22b5d1b75e`;
- publisher SHA-1: `b507eb376778cfd1cbecec2841c38891b26a7349`;
- publisher SHA-256: `0c36ba17bc812c65f5e37f9227d8b6a5185aac70b82a88d1bf52ee13103592cc`;
- bytes: `20,941,584`.

Result: physical and publisher bytes are identical by SHA-1.

## Bounded archive inventory

The exact artifact audit records:

- archive entries: **2,027**;
- classes: **333**;
- non-class resources: **1,694**;
- skill-like classes: **69**;
- skill-like resources: **439**;
- `data/wom/**` paths: **182**;
- exact skill-parameter JSONs: **58**;
- exact Epic Skills JSON files: **4**;
- exact weapon-capability JSON files: **27**;
- exact provider recipe JSONs: **36**.

No third-party JAR bytes are committed to Black Arcana.

## Exact WOMSkills registry

Direct `WOMSkills` disassembly closes **64 unique registered IDs**. The category breakdown is:

- Dodge: **8**;
- Guard: **6**;
- Passive: **14**;
- Mover: **3**;
- Identity: **8**;
- Weapon Innate: **15**;
- Weapon Passive: **10**.

This exact registry supersedes the public descriptive count of 27 skills for technical denominator purposes.

## Exact progression/reachability surface

The artifact packages four WOM Epic Skills JSON trees with **39 current nodes** across Acrobat/Prodigy progression. Those files directly include all six non-weapon identities promoted into the supernatural semantic set:

- `ender_step`;
- `ender_obscuris`;
- `shadow_step`;
- `time_travel`;
- `voodoo_magic`;
- `avatar_of_might`.

The same exact artifact closes weapon→skill bindings in `WOMWeaponCapabilityPresets`.

Relevant mappings include:

- `wom:agony` -> `agony_plunge`;
- `wom:tormented_mind` -> `true_berserk`;
- `wom:antitheus` -> `demonic_ascension`;
- `wom:ruine` -> `plunder_perdition` / Ender Ritual;
- `wom:moonless` -> `lunar_eclipse`;
- `wom:solar` -> `solar_arcano`;
- `wom:nova` -> `flash_mutilation`.

## Exact acquisition surfaces

The bounded audit disassembles the provider item registry, weapon capability presets, chest-loot injector and provider loot-drop table, and parses all 36 provider recipe JSONs.

Catalog-level normal acquisition is directly closed for:

- `wom:agony` — provider chest-loot injection;
- `wom:tormented_mind` — provider chest-loot injection;
- `wom:ruine` — provider chest-loot injection;
- `wom:moonless` — provider chest-loot injection;
- `wom:antitheus` — exact smithing recipe;
- `wom:solar` — exact crafting recipe.

`wom:nova` is registered and bound to `flash_mutilation`, but the audited recipe/chest/drop surfaces do not close its normal survival acquisition. The audit intentionally does not infer absence from every possible external script/datapack source; the action is therefore retained as `CONDITIONAL`, not claimed unreachable.

## Semantic classification rules

The canonical semantic ledger counts a standalone spell/glyph/ritual or an equivalent **discrete supernatural player action**. It excludes ordinary martial techniques, passive/reactive skills, locomotion helpers, technological weapon operations, equipment state, resource mechanics and downstream consequences.

Important exact distinctions:

- `soul_protection` and `shulker_cloak` register reactive damage-pre handlers and maintain charge/state; no independent cast root is established;
- `meditation` is explicitly implemented as a provider `PassiveSkill`;
- `voodoo_magic` is not treated as a passive merely because it has no conventional spell cast method: exact update/input behavior establishes deliberate player-driven health/stamina conversion;
- `ender_blast`, `ender_fusion` and `orbital_beam` are presented by the provider as technological weapon actions and are outside the supernatural-magic metric;
- `charybdis`, `regierung`, `sakura_state` and `unbreakable` remain combat/weapon techniques or states where exact evidence does not establish an independent supernatural/arcane identity.

## Result

Exact current registry denominator: **64/64 skills dispositioned**.

Semantic supernatural subset: **13**.

- **12 `COUNTED_EXACT`**;
- **1 `CONDITIONAL`** (`flash_mutilation`);
- **51 `EXCLUDED`**.

Strict semantic contribution: **+12**.

## Clean-room boundary

The durable catalog retains hashes, IDs, counts, category membership, bounded call-target/control-flow facts, ownership mappings and behavior-level classification needed for cataloging/interoperability. It does not redistribute implementation bodies, JAR bytes, assets or protected upstream prose beyond minimal identity labels required to distinguish actions.
