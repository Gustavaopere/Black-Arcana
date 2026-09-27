# Iron's Gems 'n Jewelry — 1.21.1-2.0.2

Status: `✅ CATALOGED / EXACT PHYSICAL=PUBLISHER ARTIFACT / ZERO_SEMANTIC_EQUIPMENT_PROC_FRAMEWORK / +0 STRICT / RUNTIME QA SEPARATE`

## Physical identity

- JAR: `irons_jewelry-1.21.1-2.0.2.jar`;
- mod id: `irons_jewelry`;
- runtime: `1.21.1-2.0.2`;
- physical SHA-1: `2f8d934d04111037dcf3fe7b04c96aec892da744`;
- CurseForge project/file: `1101111 / 8365016`.

## Exact artifact surface

The exact artifact contains 248 provider resources (122 assets + 126 data files). Its data surface is jewelcrafting-oriented: materials, parts, patterns, loot/trades, recipes, Curios slots, tags and village jeweler structures.

The bounded artifact scan finds **0** spell/ritual/rite/ability-like paths/classes. It does, however, contain an internal action framework; that fact is preserved rather than hidden.

## Internal `IAction` registry

Current public 1.21.1 source at `iron431/irons-jewelry@bd3fae5579376472c04d9090e42a7a932d604333` declares the same `1.21.1-2.0.2` version and registers eight generic action codecs:

`knockback`, `ignite`, `apply_effect`, `apply_damage`, `apply_freeze`, `heal`, `explode`, `create_items`.

These are not a spellbook/cast registry. The source wires `IAction` through `ActionParameter` into jewelry `BonusInstance` behavior, and event handlers invoke them from equipment events such as shield block, projectile hit, attack/damage-related bonuses. Material/pattern definitions provide these action payloads to jewelry bonuses.

Under the canonical metric, downstream equipment procs/effects do not become independent player-selected magic identities merely because their implementation uses an action codec.

**Semantic contribution: +0 — `ZERO_SEMANTIC_EQUIPMENT_PROC_FRAMEWORK`.**

See [exact audit](EXACT-1.21.1-2.0.2-ZERO-SEMANTIC-AUDIT.md).

## Authority boundary

Iron's Jewelry owns jewel definitions, bonus/proc state, cooldowns and settlement. Curios hosts equipment slots. Black Arcana must not duplicate proc settlement or recast these payloads as standalone spells.

## Result

**✅ Cataloged.** Internal action codecs are equipment-proc primitives; zero independent semantic magic actions.
