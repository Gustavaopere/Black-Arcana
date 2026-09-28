# Reliquified L_Ender's Cataclysm 0.1.1 — Exact Artifact Audit

## Scope

This record closes the exact-current semantic denominator for physical:

`reliquified_lenders_cataclysm-1.21.1-0.1.1.jar`

Physical SHA-1:

`be89d697455f04a1531ed81b45bcc038354430c8`

The artifact is All Rights Reserved. This audit is clean-room factual inspection only.

## Isolated audit

- NON-MERGE PR: **#441**
- final audit HEAD: `1484b00834d7aa070a401f76716e8448d01654be`
- workflow: `Reliquified 0.1.1 exact artifact audit`
- final run: **36380842145**
- result: **GREEN**
- publisher source: Modrinth project `rBEndPUc`, version `ZHAIRSeF`
- exact publisher filename: `reliquified_lenders_cataclysm-1.21.1-0.1.1.jar`

The workflow hard-fails unless the downloaded publisher artifact SHA-1 equals the physical digest.

## Exact identity result

The audit proved:

- publisher SHA-1 = `be89d697455f04a1531ed81b45bcc038354430c8`;
- physical SHA-1 = `be89d697455f04a1531ed81b45bcc038354430c8`;
- metadata mod id = `reliquified_lenders_cataclysm`;
- metadata version = `0.1.1`.

Therefore the audited publisher bytes are the current physical provider bytes for catalog purposes.

## Exact relic-item denominator

The hash-matched JAR contains exactly five top-level provider relic item classes:

- `VoidCloakItem`;
- `ScouringEyeItem`;
- `VoidVortexInBottleItem`;
- `VacuumGloveItem`;
- `VoidBubbleItem`.

A narrow static-registration scan of exact `ItemRegistry` found exactly five registered item ids:

- `scouring_eye`;
- `vacuum_glove`;
- `void_bubble`;
- `void_cloak`;
- `void_vortex_in_bottle`.

The audit asserts this registry set equals the exact item-id set independently extracted from localization keys.

## Exact ability denominator

A narrow factual bytecode scan records only the string argument consumed by each exact `AbilityData.builder(String)` invocation. It found exactly seven declarations:

| Owner | Ability ID |
|---|---|
| `void_cloak` | `void_invulnerability` |
| `void_cloak` | `void_rune` |
| `void_cloak` | `seismic_zone` |
| `scouring_eye` | `glowing_scour` |
| `void_vortex_in_bottle` | `spawn_vortex` |
| `vacuum_glove` | `vacuum_slowdown` |
| `void_bubble` | `protective_bubble` |

Independently, exact `en_us.json` key structure contains exactly the same seven `tooltip.relics.<owner>.ability.<ability>` roots.

The audit hard-asserts:

- declaration count = **7**;
- localization-root count = **7**;
- owner/ability declaration set = localization owner/ability root set.

It also found no provider data resource under `data/reliquified_lenders_cataclysm/` that would provide a separate data-defined ability inventory.

## Clean-room boundary

Permitted evidence retained by the audit:

- cryptographic digest;
- archive paths/class names;
- metadata identity/version;
- localization **keys only**, not values;
- method signatures/string constants;
- exact registration identifiers;
- exact `AbilityData.builder(String)` argument identities.

The workflow does not preserve or upload full `javap -c` output and does not copy implementation bodies, localization prose, textures, models, sounds or other protected assets.

The narrow bytecode pass exists only to prove registry/declaration cardinality and identity.

## Semantic conclusion

The exact physical 0.1.1 artifact contains a complete owner-scoped denominator of **7 provider ability roots across 5 relic owners**.

Under the established Reliquified catalog convention, those roots are provider-owned semantic magic identities. The physical provider is therefore eligible for:

`COUNTED_EXACT 7 / +7 STRICT`

Assembled runtime compatibility, deployed loot behavior, persistence, networking and balance remain separate QA.
