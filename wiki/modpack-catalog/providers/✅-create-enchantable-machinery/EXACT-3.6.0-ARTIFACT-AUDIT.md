# Create: Enchantable Machinery 3.6.0 — exact artifact audit

Status: `EXACT PHYSICAL=PUBLISHER / ZERO PROVIDER-OWNED MAGIC-IDENTITY ROSTER`

## Identity gate

- physical JAR: `createenchantablemachinery-3.6.0+mc1.21.1-neoforge.jar`;
- mod id: `createenchantablemachinery`;
- runtime: `3.6.0`;
- physical SHA-1: `ed9a5cf654235f54a3c5aced27ac654d5258e393`.

NON-MERGE PR #556 downloads Modrinth version `Cw5k6c0a` and fails unless its SHA-1 equals the physical fingerprint.

- audit HEAD: `dd9ae99608f7561961ca909ce1f5cf2c2987e0ea`;
- run: `37159216158` — SUCCESS;
- artifact: `11286842169`;
- digest: `sha256:fc321c53755dfd7220744b5a40ebc6a749b50d2fa6a5020254c8ac99742a55d0`;
- publisher SHA-1: `ed9a5cf654235f54a3c5aced27ac654d5258e393`;
- publisher SHA-256: `933ad37b064d8c6005f1f6eb09b3274fe9f5961a6841fb9e7bb65a7bff66f653`;
- bytes: `575,739`.

Result: exact publisher/physical equality is proven.

## Archive inventory

- entries: **282**;
- classes: **142**;
- resources: **140**;
- provider-data paths: **17**;
- provider JSON files: **12**.

Semantic path counts:

- spell 0;
- magic 0;
- ritual 0;
- ability 0;
- mana 0;
- arcane 0;
- glyph 0;
- summon 0;
- soul 0;
- teleport 0;
- portal 0;
- curse 0;
- enchant 201 — expected because enchantment application/state is the addon's purpose.

## Enchantment ownership

No `data/*/enchantment/**` definitions exist in the exact artifact. Exact bytecode references `Registries.ENCHANTMENT`, standard `ItemEnchantments` and Minecraft/external enchantment holders; no provider-owned enchantment registration surface is present.

The provider's 12 JSON files are eleven block loot tables plus the `enchantable_blocks` tag. Loot tables copy `minecraft:enchantments` from the block entity back to the underlying Create machine item.

## Enchantable machine denominator

Exact `createenchantablemachinery:enchantable_blocks` = **11** Create blocks: Drill, Saw, Harvester, Encased Fan, Millstone, Crushing Wheel, Plough, Mixer, Press, Roller and Spout.

The provider registers one alternative enchantable block implementation for each mapped Create block. These are state/container variants, not eleven magic actions.

## Activation surface

The exhaustive signature index finds placement/state hooks on enchantable blocks and only three meaningful `use` mixin seams on Drill/Roller/Saw. Those seams check whether the held matching Create block item is already enchanted and delegate to the corresponding enchantable block `useItemOn` path.

No player-owned spell, ritual, rite, summon or supernatural action lifecycle is exposed.

## Semantic disposition

`ZERO_SEMANTIC_MACHINE_ENCHANTMENT_APPLICATION / +0 strict`.

Enchanting Table/anvil use, enchantment persistence, goggles/Jade display, machine-speed/drop changes and compatibility with modded enchantments are enchantment/machine mechanics. Existing enchantment identities remain owned by Minecraft or their originating mods.

## Clean-room boundary

The durable catalog retains hashes, counts, IDs, path names and behavior-level classifications required for denominator work. No third-party JAR bytes, implementation bodies or assets are committed.
