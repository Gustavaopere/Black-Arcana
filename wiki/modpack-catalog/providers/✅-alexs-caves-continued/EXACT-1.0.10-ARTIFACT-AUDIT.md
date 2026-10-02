# Alex's Caves Continued 1.0.10 — exact artifact audit

Status: `EXACT PHYSICAL=PUBLISHER / ITEM-ACTIVATION DENOMINATOR + BLOCK-RITUAL SURFACES CLOSED`

## Identity gate

Physical sibling authority:

- `alexscaves-1.0.10-neoforge+1.21.1.jar`;
- mod id `alexscaves`;
- runtime `1.0.10`;
- SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`.

NON-MERGE PR #509 downloads CurseForge File `1645389 / 8856293` and fails before semantic inspection unless publisher SHA-1 equals the physical fingerprint.

Final bounded audit:

- HEAD: `fc05d04cd2b13b6c905bcc77bce35579d4f6f86a`;
- audit run: `36947136917` — SUCCESS;
- artifact: `11202366754`;
- artifact digest: `sha256:455641235c3834c29a2d3519ceda452a07aaff96bd931eebbe08fcedc0e6314e`;
- publisher SHA-1: `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`;
- publisher SHA-256: `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`;
- bytes: `75,279,314`.

Result: exact publisher/physical equality is proven.

## Bounded archive inventory

- archive entries: **8,898**;
- classes: **1,555**;
- non-class resources: **7,343**;
- item classes: **81**;
- block classes: **155**;
- message classes: **25**;
- `data/alexscaves/**` paths: **1,573**.

No third-party JAR bytes are committed to Black Arcana.

## Exhaustive item-interaction pass

The audit disassembles every exact top-level item class and indexes method signatures that can represent a player interaction (`use`, `useOn`, `releaseUsing`, `onUseTick`, `finishUsingItem`, `interactLivingEntity`, `hurtEnemy`, `onKeyPacket`).

Result: **42 exact item classes** expose at least one such interaction surface.

All 42 are dispositioned in the durable catalog. The item pass does not count method signatures mechanically: ordinary weapon firing, food, vehicles, passive/reactive gear, technology and setup actions are excluded according to the semantic-magic metric.

## Exact supernatural item seams

The exact binary pass separately disassembles the primary supernatural candidates and closes these item-owned roots:

- `SeaStaffItem` — one Water Bolt cast root;
- `SugarStaffItem` — two selectable roots: Peppermint Cast and Hex Cast;
- `MagicConchItem` — one charged Deep One summon root;
- `TotemOfPossessionItem` — one bound-entity possession/control root;
- `OccultGemItem` — activation of the bound Beholder observation lifecycle;
- `DarknessArmorItem` — Cloak key action consuming charge and applying Darkness Incarnate.

Downstream projectiles/entities, target transfer, repeated movement/attack updates, enchantment branches, charge state and cooldowns remain consequences/parameters rather than new action identities.

## Exact block-action pass

Run #2 adds direct bytecode inspection of:

- `ConversionCrucibleBlock`;
- `ConversionCrucibleBlockEntity`;
- `BeholderBlock`;
- `BeholderBlockEntity`;
- `ForsakenIdolBlock`.

Exact facts:

- Conversion Crucible exposes a player interaction path that accepts a Cave Biome-bound Biome Treat and provider-requested offerings;
- the exact block entity advances a filled conversion lifecycle and settles through `convertBiome()`;
- the final sacrifice varies by target biome, but all variants settle through the same provider-owned causal action;
- Beholder exact block entity exposes `startObserving(Level, Player)` and spawns a provider Beholder Eye tied to the player;
- Forsaken Idol has no player activation seam in the exact inspected block class.

Therefore block inspection contributes one additional semantic root: **Biome Conversion**. Beholder observation is already counted once under the Occult Gem/Beholder combined owner lifecycle.

## Acquisition evidence

Exact provider data closes normal current acquisition for every counted owner/surface:

- `alexscaves:sea_staff` — Deep One Mage barter loot;
- `alexscaves:sugar_staff` — Licowitch entity loot;
- `alexscaves:magic_conch` — Deep One Knight barter loot;
- `alexscaves:occult_gem` — Forlorn/Watcher loot and exact Beholder crafting relation;
- `alexscaves:totem_of_possession` — exact recipe;
- `alexscaves:cloak_of_darkness` and `alexscaves:hood_of_darkness` — exact recipes;
- `alexscaves:conversion_crucible` and `alexscaves:biome_treat` — exact recipes.

These prove catalog-level owner reachability. Full assembled-pack loot/recipe overrides remain runtime/datapack QA.

## Excluded surfaces

Examples of exact interaction classes intentionally excluded:

- primary weapon modes: Dreadbow, spears, Ortholance, generic thrown/projectile items;
- on-hit weapon behavior: Desolate Dagger, Primitive Club, Sharpened Candy Cane;
- technology/magnetism/explosives: Galena Gauntlet, Raygun, Quarry Smasher, Remote Detonator;
- consumables/feeding/effects: Moth Dust, foods/drinks, Prehistoric Mixture, Radiation Removing Food;
- vehicle/mobility utility: Cave Boat, Submarine, Floater, Candy Cane Hook;
- documentation/progression/setup: Cave Book, Cave Info, Cave Map, Biome Treat;
- block-only Forsaken Idol with no activation seam;
- Underzealot sacrifice/Forsaken transformation, which is mob-native rather than a player-selected provider action.

## Semantic disposition

Counted exact-current identities:

- Sea Staff Water Bolt: 1;
- Sugar Staff Peppermint Cast: 1;
- Sugar Staff Hex Cast: 1;
- Magic Conch Deep One Summon: 1;
- Totem Possession/Control: 1;
- Occult Gem + Beholder Remote Observation: 1;
- Cloak of Darkness / Darkness Incarnate activation: 1;
- Conversion Crucible Biome Conversion: 1.

Total: **8 `COUNTED_EXACT`**.

## Source corroboration boundary

Public Continued source at `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` was used only to interpret behavior-level control flow after exact binary identity/coverage was closed. That public source snapshot is not asserted byte-identical to the installed 1.0.10 JAR. Exact JAR evidence remains authoritative for current identity and existence.

## Clean-room boundary

The durable catalog retains hashes, identifiers, counts, method-level seam facts, owner/acquisition relationships and behavior-level classification needed for cataloging. It does not redistribute JAR bytes, implementation bodies, assets or localization prose.
