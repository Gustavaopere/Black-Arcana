# Create Mechanical Companion — 1.9

Status: `✅ CATALOGED / EXACT PHYSICAL=PUBLISHER ARTIFACT / ZERO_SEMANTIC_MECHANICAL_COMPANION_INFRA / +0 STRICT / RUNTIME QA SEPARATE`

## Current physical identity

- sibling physical row: **#193**;
- JAR: `createmechanicalcompanion-1.9-neoforge-1.21.1.jar`;
- mod id: `createmechanicalcompanion`;
- runtime metadata: **empty in the physical modlist**;
- publication/artifact line: `1.9`;
- physical SHA-1: `480d35a7f926c1a2b86521be1feb75710b1c838e`.

Create Mechanical Companion adds a modular Mechanical Wolf bound to a Curios link and integrated with Create. Its Quantum Drive, Tesla Tail and other modules are technological companion/equipment systems rather than a provider-owned magic-action roster.

## Exact publisher-artifact closure

NON-MERGE evidence PR **#554** audits Modrinth version `6ZRWru4y` and hard-gates the publisher artifact against the physical fingerprint.

- audit HEAD: `a1e2e3bb2ddb7799fb049ece985e3de607482102`;
- exact-artifact run: `37145583077` — **SUCCESS**;
- evidence artifact: `11281054748`;
- evidence digest: `sha256:3b35aa2d4c459fb5dea51166e6b245ce2a2875941bfb3607d85a659ae0b440ff`;
- publisher file: `createmechanicalcompanion-1.9-neoforge-1.21.1.jar`;
- publisher SHA-1: `480d35a7f926c1a2b86521be1feb75710b1c838e`;
- publisher SHA-256: `06b216b06ef400fe573303a6acbfb5e599474a61c8fd329356397c69b6f4a2ef`;
- bytes: `357,511`.

The publisher SHA-1 exactly equals the current physical pack SHA-1.

See [`EXACT-1.9-ARTIFACT-AUDIT.md`](EXACT-1.9-ARTIFACT-AUDIT.md).

## Exact semantic inventory

The exact artifact contains **198 entries / 54 classes / 144 resources / 41 provider-data paths / 26 provider JSON files**.

Exact archive-path counts are zero for:

`spell · magic · ritual · ability · mana · arcane · glyph · summon · soul · teleport · portal · enchant · curse`.

The exhaustive player/Curios activation-signature index closes only two provider item surfaces:

- `BlueprintPaintingItem.useOn` — decorative Blueprint Painting placement;
- `MechanicalWolfLink.curioTick` / `onUnequip` — automatic companion lifecycle, persistence, respawn and dismissal.

The Mechanical Wolf itself owns module-driven AI/equipment behavior. Exact bytecode shows Quantum Drive teleporting the **companion entity** automatically under module/cooldown logic; Tesla Tail, Booster Rocket, Mob Radar and Mounted Crossbow are companion modules, not player-cast supernatural actions.

Detailed disposition: [`SEMANTIC-SURFACE-DISPOSITION.md`](SEMANTIC-SURFACE-DISPOSITION.md).

## Acquisition and provider data

The exact provider JSON set contains ordinary recipes/loot/worldgen only, including recipes for the Mechanical Wolf Link, Quantum Drive, Booster Rocket, Tesla Tail, Mounted Crossbow, Mob Radar and other modules, plus Illager Workshop data.

These recipes acquire companion technology/equipment; they do not define ritual/spell recipe types.

## Authority boundary

Create Mechanical Companion remains authority for Mechanical Wolf lifecycle, UUID persistence, Curios link behavior, module inventory, AI, damage, automatic teleport, respawn cooldown and ownership. Create remains authority for its host technology/material progression.

Black Arcana must not reinterpret the mechanical wolf lifecycle or module operations as spells, summon rituals or teleport magic, and must not duplicate provider companion settlement.

## Result

**✅ Cataloged — `ZERO_SEMANTIC_MECHANICAL_COMPANION_INFRA`.**

Strict semantic delta: **+0**.
