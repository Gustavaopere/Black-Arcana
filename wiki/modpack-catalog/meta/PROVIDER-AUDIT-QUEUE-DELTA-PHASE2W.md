# Provider Audit Queue Delta — Phase 2W Ars Hex 5.0.4b

Status: `SOURCE CATALOG CLOSED / INSTALLED CONFIG + RUNTIME QA OPEN`

This narrow overlay prevails only for `ars_hex` until the full shared provider queue is regenerated safely.

## Canonical row delta

| Mod ID | Nome atual | JAR atual | Versão atual | Estado da auditoria | Delta |
|---|---|---|---|---|---|
| `ars_hex` | Ars Hex | `ars_hex-1.21.1-5.0.4b.jar` | `5.0.4b` | `RELEASE-ALIGNED SOURCE 5.0.4b / MALUM: 1 GLYPH + 3 PERKS + ENCHANTER SCYTHE + 5 RECIPES / IRON'S: SCHOOL-DAMAGE + ELEMENTAL-ARMOR BRIDGES + 5 PARTICLES / HEXEREI DORMANT / 0 MIXINS / 0 PROVIDER PAYLOADS IDENTIFIED / RUNTIME+CONFIG+JAR-PACKAGE QA PENDENTES` | broad guide-only row replaced by granular active-vs-dormant source catalog |

## Closed — source catalog

- exact physical JAR/version/mod id/SHA-1;
- release-aligned Ars-Unity checkpoint with binary-equivalence limitation explicit;
- exact build-host versions and current-pack drift;
- conditional bootstrap for Malum, Iron's and Hexerei;
- 1/1 Malum-backed glyph with tier/mana/damage/augment/school behavior;
- 3/3 Malum-backed Ars thread perks with exact attribute operations;
- Enchanter's Scythe Ars-caster/Malum-weapon behavior and Necromancy mana discount;
- Malum scythe-boomerang/Reactive event seam;
- 5/5 Malum-conditioned committed source recipes;
- Iron school mapping and exact Ars damage multiplier path;
- Ars Elemental armor→Iron school-power modifier path;
- 5/5 Iron particle wrappers;
- COMMON config conceptual defaults + duplicate persisted path observation;
- exact source observation that optional general SPELL_POWER merge reads the target's attribute;
- dormant Hexerei source registry surface (3 items, 1 entity, 12 particles) separated from current runtime;
- 3 Hexerei-conditioned manual recipes plus 1 Hex Casting-conditioned orphan resource classified;
- 0 common + 0 client mixins;
- 0 provider-owned custom payload registrations identified;
- datagen-intent vs committed-generated-resource boundary;
- code LGPLv3 / assets ARR provenance boundary;
- authority/deduplication consequences.

## Open — installed JAR/config/runtime

1. Extract physical `ars_hex-1.21.1-5.0.4b.jar` and compare packaged classes/resources/recipes/tags to the release-aligned source checkpoint.
2. Inspect actual generated/installed COMMON config and determine effective behavior of the shared `IronsDamageBonusScaling` path.
3. Validate Ars 5.13.1 + Ars Elemental 0.7.10.1 + Iron's 3.16.3 + Malum/Lodestone 1.8.2 event/API compatibility.
4. Soul Shatter: damage school/type/Amplify and spirit consequences exactly once.
5. Threads: equipment slot scaling/stacking and host attribute results.
6. Enchanter's Scythe: scribing, Touch insertion, melee hit, boomerang, Reactive, Repairing and Necromancy discount.
7. Iron bridge: school power/resistance multipliers, multi-school behavior, optional general merge and target-vs-caster observation.
8. Elemental armor bridge: exact modifier application/stacking across current 48 elemental armor pieces/provider perk setup.
9. Verify Hexerei and Hex Casting conditional resources remain absent/inactive in the current pack.
10. Confirm whether intended datagen damage/item/block tags are actually packaged.
11. Dedicated-server/client/full-pack interoperability and optional-provider classloading.
12. Confirm Sauce jarjar resolution under the complete pack rather than assuming one nested copy wins globally.

## Open — provenance

No code-license conflict is identified: metadata/root source are LGPLv3. Upstream assets are separately declared All Rights Reserved. Phase 2W copies no source/assets. Any future code derivation must satisfy LGPL obligations; any asset reuse requires separate permission/license evidence.

## Merge gate

Before merge: fetch current `main`, reconcile semantically if it advanced, review the exact final catalog-only diff, require fresh CI on the reconciled HEAD and keep review threads clear. Runtime/config/JAR-package items above may remain explicitly deferred and must not be reported as PASS.
