# Provider Audit Queue Delta — Phase 2Y Ars Nouveau's Flavors & Delight 2.2.2

Status: `SOURCE CATALOG CLOSED / INSTALLED JAR + CURRENT-HOST RUNTIME QA OPEN`

This narrow overlay prevails only for `arsdelight` until the full shared provider queue is regenerated safely.

## Canonical row delta

| Mod ID | Nome atual | JAR atual | Versão atual | Estado da auditoria | Delta |
|---|---|---|---|---|---|
| `arsdelight` | Ars Nouveau's Flavors & Delight | `arsdelight-2.2.2.jar` | `2.2.2` | `VERSION-ALIGNED SOURCE-PIN 2.2.2 / 42 BASE FOODS + 8 NON-FOOD ITEMS + 8 BASE STORAGE/FEAST BLOCKS + 5 JELLIES/1 BE + 4 PIES/4 SLICES + 5 EFFECTS + ENCHANTER'S KNIFE + CUTTING/JELLY/DRYGMY + 3 MIXINS CATALOGADOS / RUNTIME+JAR QA PENDENTES` | preliminary feature page replaced by exact source/API/authority catalog |

## Closed — source catalog

- physical JAR/version/mod id/SHA-1/hash;
- exact version-aligned 2.2.2 source checkpoint;
- source NeoForge and required Ars/FD version boundaries;
- base food/item/block/jelly/pie/effect registries;
- Ars heal/spell-damage/max-mana/mana-regen event behavior and formulas;
- Enchanter's Knife caster-tool lifecycle;
- Cutting Board spell interception/cancellation;
- Jelly spell-context infusion;
- Drygmy fake-player tool path;
- three declared mixins;
- global-loot modifier semantics;
- Ars Elemental / Archwood Good / Thirst optional gates;
- Cuisine Delight datagen integration;
- absence of provider-owned production glyph registrations in the audited source content tree;
- no provider-owned custom payload registration surface identified in the exact source tree;
- clean-room provenance and semantic deduplication consequences.

## Open — installed JAR/current-host runtime

1. Extract and inventory the physical 2.2.2 JAR.
2. Confirm packaged registry/data/mixin surfaces match the version-aligned checkpoint.
3. Validate Ars 5.13.1 + Farmer's Delight 1.3.4 behavior.
4. Validate all five base effects under current event ordering and multiplayer.
5. Validate Enchanter's Knife exactly-once melee→spell settlement and Ars resource cost.
6. Validate Cutting Board handling/cancellation for Cut/Crush/Fell/Break.
7. Validate Jelly projectile/Infuse attachment lifecycle.
8. Validate Drygmy tool copy/durability/cleanup under current Ars internals.
9. Validate feast/pie/jelly save/drop/serving conservation.
10. Validate Wilden/Chimera global-loot paths with current loot addons.
11. Validate Ars Elemental present path.
12. Validate Archwood Good and Diet absent paths.
13. Validate current `thirst` implementation against the legacy source API gate.
14. Validate Cuisine Delight 1.2.10 generated-config data.
15. Client + dedicated-server + full-pack interop smoke.

## Merge gate

Before merge: fetch current `main`, reconcile semantically if it advanced, review the exact final diff, require fresh exact-head CI and keep review threads clear. Runtime/JAR items above may remain explicitly deferred because this PR closes factual source catalog coverage; they must not be reported as runtime PASS.
