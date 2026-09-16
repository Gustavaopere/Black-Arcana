# Soul Fire'd 6.1.0 — evidence and provenance

## Physical authority

Current physical pack evidence:

- JAR: `soul-fire-d-neoforge-1.21-6.1.0.jar`;
- mod id: `soul_fire_d`;
- runtime: `6.1.0`;
- SHA-1: `877002a5aa386f9011ebc4eb3360a7647ac359d9`;
- NeoForge pack baseline: `21.1.248`.

Physical modlist/JAR metadata is authority for installed presence/version/hash.

## Exact publisher release

CurseForge:

- project ID `662413`;
- exact NeoForge 1.21 File ID `7364962`;
- filename `soul-fire-d-neoforge-1.21-6.1.0.jar`;
- uploaded `2025-12-22`;
- supports Minecraft `1.21` and `1.21.1`;
- environment Client & Server;
- project license label: `Custom License`.

Modrinth independently exposes 6.1.0 for the same 1.21/1.21.1 line and labels the project `Crystal Nest Community License v1`.

## Exact official source pin

Repository:

- `Crystal-Nest/soul-fire-d`.

Exact branch/revision:

- branch `1.21`;
- commit `0cc7a03b950e74742eb75f51642cc7a0190c7127`;
- commit message `Update mod_version to 6.1.0`;
- tree `a43189fb8689041edb7993d94f85f64597f57303`.

Exact source metadata:

- Java `21`;
- `mod_version=6.1.0`;
- Minecraft `1.21`;
- NeoForge baseline `21.0.143`;
- NeoForge runtime range `[21.0,)`;
- Cobweb `1.4.0`;
- Prometheus `1.2.5`;
- source metadata license `GPL-3.0-or-later`.

The physical pack uses Cobweb 1.4.0 and Prometheus 1.2.5 exactly, and NeoForge 21.1.248 satisfies the declared loader range.

## Exact 6.1.0 changelog evidence

The 6.1.0 changelog records:

- update to Prometheus `1.2.0+`;
- fix for unwanted override of tags in the enchantments datapack.

The exact source dependency pin is stricter/current at Prometheus 1.2.5.

## Prometheus authority evidence

Publisher/developer documentation states that since Soul Fire'd 6.0.0 the fire API moved to Prometheus.

For the exact physical dependency version, official source is independently pinned at:

- `Crystal-Nest/prometheus:1.21@3edbe979b3a383b526f38daeba4eb35d18283a9d`;
- version commit: `Update mod_version to 1.2.5`.

Exact Prometheus 1.2.5 source proves:

- `FireManager.SOUL_FIRE_TYPE = minecraft:soul`;
- generic `FireRegistrar` owns component registration helpers;
- `registerFireCharge(...)` registers the component item under the fire type namespace and updates the creeper-igniter tag through Prometheus's dynamic datapack.

This Prometheus source was consulted only to resolve the provider boundary/API ownership used by exact Soul Fire'd 6.1.0. Prometheus is not being silently cataloged as closed by Phase 2AO.

## Exact source surfaces inspected

Soul Fire'd 6.1.0:

- `gradle.properties`;
- NeoForge metadata template;
- `CommonModLoader`;
- NeoForge `ModLoader`;
- `FireRegistry`;
- both mixin manifests;
- `LootRegistry`;
- `ChestLootModifier`;
- enchantment JSONs for Soul Fire Aspect and Soul Flame;
- Bastion global loot modifier data;
- Soul Fire Charge recipe;
- recursive exact source tree.

Prometheus 1.2.5:

- exact branch pin;
- `FireManager` authority constants;
- `FireRegistrar` generic registration behavior.

No source code was copied or adapted into Black Arcana.

## License metadata conflict

The exact Soul Fire'd source tree contains a GPLv3 license text and `gradle.properties` declares `GPL-3.0-or-later`.

Current publisher surfaces label the distributed project as:

- CurseForge: `Custom License`;
- Modrinth: `Crystal Nest Community License v1`.

This is an unresolved license-metadata discrepancy for reuse/derivation purposes.

Catalog/interoperability consequence:

- read-only factual inspection is recorded here;
- no source/assets are copied/adapted;
- do not claim a code/asset reuse grant from either label without independent reconciliation;
- any future `DERIVED_CODE`/`DERIVED_ASSET` use remains blocked/review-required.

## Exact conclusions supported

- installed/publisher/source version alignment at Soul Fire'd 6.1.0;
- exact source branch for Minecraft 1.21;
- exact physical dependency match for Cobweb/Prometheus;
- generic fire API authority moved to Prometheus;
- exact `minecraft:soul` definition supplied by Soul Fire'd through Prometheus;
- light 10 / damage 2 / vanilla Soul Fire flame particle;
- associated `minecraft:soul_fire_charge` resource/recipe family;
- exactly two enchantment definitions;
- one NeoForge loot-modifier serializer plus one bundled Bastion modifier instance;
- exact zero-mixin result;
- zero standalone spell/glyph/ritual/casting-resource surface observed in the exact provider tree.

## What is deliberately not claimed

- byte-for-byte reproducibility between source output and physical JAR;
- every runtime effect of Prometheus 1.2.5 beyond the inspected boundary;
- successful interoperability with every fire/combat/enchantment mod in the 595-mod pack;
- optional integration hooks advertised by the publisher unless separately proven;
- license resolution beyond the conflicting metadata recorded above.

## Clean-room result

This audit is factual provider cataloging and interoperability analysis. Black Arcana receives no third-party source or asset ownership from Soul Fire'd, Prometheus or Cobweb, and their implementation authority does not transfer into BA.
