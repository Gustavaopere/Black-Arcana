# Create: More Features 0.1.3 — exact artifact audit

Status: `EXACT PHYSICAL=PUBLISHER / SEMANTIC MAGIC DENOMINATOR CLOSED AT ZERO`

## Identity gate

- physical JAR: `create_mf-0.1.3-neoforge-1.21.1.jar`;
- mod id: `create_mf`;
- runtime: `0.1.3`;
- physical SHA-1: `09c4b6ab3ca3c372e2a0b405e75ae19876aebdc4`;
- CurseForge project/file: `1091960 / 8325313`.

NON-MERGE PR #538 / run `37020906917` succeeded with exact physical/publisher equality.

- audit HEAD: `8e4aa1dd81f91fc8cf8bce553cf5c89274fa7be9`;
- evidence artifact: `11233935270`;
- artifact digest: `sha256:b4e0ba4843a66d9f708f2e9562631853e89633b273f448b0736c92d72c4d6647`;
- publisher SHA-256: `32196d6cc8ba1ad5cac8d4e8828347ac4453c59d8be502c52a77c7799b261f54`;
- bytes: `10,567,277`.

## Bounded archive inventory

- entries: **615**;
- classes: **145**;
- resources: **470**;
- provider data paths: **108**.

Magic-semantic path counts are all zero:

`spell=0 · magic=0 · ritual=0 · ability=0 · mana=0 · arcane=0 · glyph=0 · summon=0 · soul=0 · teleport=0 · portal=0 · enchant=0 · potion=0 · curse=0`.

Domain-positive path counts are non-magical Create/villager surfaces, including villager/profession/mechanism resources.

## Exhaustive activation index

Every provider class was signature-scanned for:

`use · useOn · useWithoutItem · releaseUsing · onUseTick · finishUsingItem · interactLivingEntity · hurtEnemy · inventoryTick · onArmorTick · onItemUseFirst · mineBlock`.

Only five provider classes match, each only through `useWithoutItem`: Andesite Box, Brass Box, CKB Vibration Blocker, Refined Radiance Box and Shadow Steel Box.

Disassembly resolves these calls to block/container/menu/configuration behavior rather than a spell/ritual/action engine.

## Data surface

The exact data surface contains Create recipes, advancements, tags and villager/mechanism content. No provider-owned ritual recipe type, spell registry, magic-action registry, glyph family, summon action or portal-action roster is present.

## Semantic result

- standalone spell/glyph/ritual/ability roots: **0**;
- player-owned supernatural action roots: **0**;
- box/menu interactions: **EXCLUDED**;
- villager professions/trades: **EXCLUDED**;
- mechanisms/farms/storage/devices: **EXCLUDED**;
- reintroduced Create content and recipes: **EXCLUDED**.

Disposition: **`ZERO_SEMANTIC_CREATE_AUTOMATION_VILLAGER_INFRA`**.

## Clean-room boundary

The durable catalog retains hashes, counts, identifiers and behavior-level classifications required for semantic cataloging. It does not redistribute the JAR, implementation bodies, assets or localization prose.
