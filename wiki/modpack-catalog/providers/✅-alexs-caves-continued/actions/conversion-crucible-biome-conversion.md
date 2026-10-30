# Conversion Crucible — Biome Conversion

- Provider: **Alex's Caves Continued** (`alexscaves`)
- Version: `1.0.10`
- Exact physical/publisher SHA-1: `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`
- Owner: `alexscaves:conversion_crucible` + `alexscaves:biome_treat`
- Trigger: select a target with a bound Biome Treat and complete the provider-requested offering sequence
- State: `COUNTED_EXACT`

## Semantic identity

One provider-owned lifecycle selects a biome, accepts offerings, starts a timed conversion, replaces selected surface blocks and rewrites local biome cells. Treat binding, target choices, offering rolls, final-sacrifice variants, advancement credit and world writes are branches or consequences of **one** counted root. They do not add identities to the provider's eight counted roots.

The owning implementation is `server.block.ConversionCrucibleBlock` plus `server.block.blockentity.ConversionCrucibleBlockEntity`; `server.item.BiomeTreatItem` supplies the bound target. Despite the inherited name `CaveBiome`, the inspected binding and conversion paths do not limit selection to Alex's Caves biomes. [B1, C1–C6]

## Evidence and certification ceiling

All exact values below come from `javap -p -c -s` inspection of publisher file **8856293**, `alexscaves` **1.0.10**, and bundled JSON. Artifact: 75,279,314 bytes; SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`; SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. Offsets are local to the named method in this binary. See the shared [exact technical contract proof root](../EXACT-TECHNICAL-CONTRACTS-1.0.10.md).

| Field | Evidence status |
|---|---|
| Identity, behavior, parameters, targeting, costs and bundled resources | `EXACT_BINARY_STATIC`; locators below |
| Effective registry, merged tags/surface rules and other mods' interception | `NOT_VERIFIED` |
| Black Arcana mutating hook | `NOT_VERIFIED`; no supported mutating extension established |
| Physical single-player/dedicated-server/multiplayer QA | `NOT_TESTED` |

The public source pin `523308608422ab8e31974befa7111ecdf495dd37` declares **1.1.1**, and its inspected parent declares **1.1.0**. Neither certifies 1.0.10 numeric behavior. No matching 1.0.10 source pin was established; exact binary and resource evidence is the authority here. This card does not promote hooks, physical QA or the certification ledger.

## Exact acquisition

| Item | Exact bundled crafting recipe |
|---|---|
| `alexscaves:conversion_crucible` ×1 | Shaped `GCG / GEG / GGG`: 7 × `#alexscaves:storage_blocks/gold`, 1 × `minecraft:cauldron`, 1 × `alexscaves:radiant_essence`. |
| `alexscaves:biome_treat` ×1 | Shaped `RER / RER / ·C·` (`·` is an empty slot): 4 × `#alexscaves:rock_candies`, 2 × `alexscaves:radiant_essence`, 1 × `alexscaves:candy_cane`. |

The bundled gold ingredient tag includes `minecraft:gold_block` and an optional `#c:storage_blocks/gold`; the rock-candy tag contains the sixteen color variants. Effective datapacks can change these ingredient tags. The Crucible loot table drops the Crucible item; its inventory advancement observes acquisition. Neither is another action root. [D1, D2]

## Causal behavior

1. **Bind the Treat.** Use an unbound edible Treat. On finishing use, a Player at food level **0**, or a creative Player, receives a newly created Treat bound to the biome at the Player's block position. This branch returns before normal food settlement. A Player at nonzero food level without creative mode takes the superclass food path instead. Binding has no inspected cave whitelist, dimension restriction or player-selected remote position. The captured key is stored as `CaveBiome` in stack custom data; bound Treat creation also sets `BIOME_TREAT_DONE` food data. [B1, B2]
2. **Select a target.** A non-sneaking item interaction with a Crucible that has no target accepts a bound Biome Treat, stores its key, sets fill to **1**, rolls the first request and marks the block entity updated on the server. This right-click branch does **not** shrink the Treat. Alternatively, server item collection checks every fifth block-entity tick and can select a dropped bound Treat, consuming **one**. No player owner is stored by either selection branch. [C1, C2]
3. **Offer the requested item.** Right-click or the dropped-item collector matches the requested **item identity**, rather than full component/NBT equality. One accepted offering increases fill by one, rerolls the request and sets splash timer to 10. Right-click uses a one-item copy for settlement and debits the held original only outside `instabuild`; dropped-item settlement consumes the supplied stack directly. [C1–C3]
4. **Begin conversion.** When fill is at least **10**, the target is nonnull and witch mode is inactive, the tick path clears requested/display stacks and advances `conversionTime`. Server surface walks are scheduled at counter values **20, 30, 40, 50, 60, 70, 80, 90**. Counter values below 100 increment once per active tick; the following tick at 100 calls `convertBiome`. This is a 100-counter-tick buildup, nominally five seconds at 20 TPS; it is not an immediate use effect. [C2]
5. **Settle and reset.** The biome writer resolves the target against the runtime biome registry, updates available affected chunks, marks them unsaved and sends their biome data to clients. An absent target holder returns without biome writes. Normal completion resets conversion time and fill to **0**, retaining the target; it does not restore converted blocks/biomes or refund offerings. [C2, C6]

## Parameters and modifiers

| Parameter | Exact static rule | Evidence |
|---|---|---|
| Normal fill threshold / cap | Conversion gate `fill >= 10`; offering increment capped at 10 | C2, C3 |
| Conversion counter | Increment while below 100; at 100 invoke biome conversion and reset | C2, offsets 256–378 |
| Dropped-item scan cadence | Server `tickCount % 5 == 0`; at most one matching offering is consumed before the offer loop breaks | C2, 672–837 |
| Scan shape | Crucible inside box `(3,2,3)`–`(13,16,13)` plus above box `(0,16,0)`–`(16,20,16)`, in model sixteenths, translated to block position; query each component AABB for ItemEntities | C1, C4 |
| Splash timer | 10 after each consumed offering | C3, 36–42 |
| Ordinary request roll | `nextInt(2)` selects top or middle palette block as an item; nominal 1/2 each. The switch contains a bottom case, but the literal bound cannot select it | C5, 158–266 |
| Final-request threshold | Non-witch fill **greater than 8** requests the final sacrifice; unresolved target falls back to diamond | C5, 85–152 |
| Surface walk schedule / budget | Eight scheduled walks in an uninterrupted normal cycle; each starts one below the Crucible with max=10, remaining=10 and a fresh visited list | C2, 265–314 |
| Surface placement delay | Queued value `2 × (max − remaining)`: 0, 2, …, 18 for successive processed nodes; queue processing decrements these values each server tick | C7; C2, 885–902 |
| Nominal biome width | `getConversionAreaWidth()` returns **10F**; writer half-extent is `ceil(10 × 0.5) + 1 = 6` on X, Y and Z | C6, C8 |
| Advancement lookup | Separate AABB from position minus 32 to plus 32; nonspectator Players receive conversion credit. A Nether-tagged target with `bedWorks()` also grants Nether-conversion credit | C6, 33–149 |
| Biome Treat item | Stack limit 1, uncommon; unbound food nutrition 20/saturation modifier 0.1; bound food nutrition 1/modifier 0.1; drink animation | B1, B3 |

The palette is computed from the target's runtime biome holder, Overworld/Nether/End noise settings and merged surface rules at the Crucible's column. Fallback top/middle/bottom are grass block/dirt/stone, all netherrack for Nether-tagged targets, and all end stone for End-tagged targets. Nonnull, non-bedrock surface-rule results can replace these fallback states. The caught exception path logs a warning and keeps values already selected. Consequently, the card does not hardcode one surface palette or one ordinary-offering list for every target biome. [C9]

The same block entity has a provider witch-mode branch (`witchModeDuration > 0`): normal biome conversion is suppressed, offering fill caps at 6, and requests become `alexscaves:licowitch_radiant_essence`. Expiration clears target, color, requested/display stacks and fill. It is a provider-controlled branch, not an additional player ability or an override for normal conversion costs. [C2, C3, C5, C8]

No mana debit, fixed item durability debit, configurable radius or cooldown gate appears in the inspected Treat/Crucible methods. These are bounded static findings; external server behavior is unverified.

## Targeting and world mutation

**Biome cells.** Conversion uses an inclusive block-coordinate BoundingBox from Crucible position minus 6 to plus 6 on all three axes. For each overlapping horizontal chunk coordinate, it asks for `ChunkStatus.FULL` with creation false and skips a null result. On the server, `fillBiomesFromNoise` invokes a resolver that maps quart coordinates to block coordinates, returns the target holder only when that sample lies inside the box, and otherwise retains the existing biome. The extra integer argument passed to `makeResolver` is not captured or used. Thus neither a 32-block conversion radius nor an exact 13×13×13 volume of individually rewritten blocks is established. Writes operate on quart biome cells, with chunk availability and coordinate alignment affecting the result. The Nether/bedWorks condition grants advancement credit and does not gate conversion. [C6]

**Surface blocks.** Each scheduled walk processes at most ten nodes and chooses **one** random eligible neighbor at each step. It does not branch into all neighbors. A node already matching any target palette block identity uses a step without queuing a replacement. Otherwise replaceable space immediately above selects the top state; replaceable space two above selects middle; the remaining case selects bottom. Neighbor candidates must be nonreplaceable, unvisited in that walk, outside `#alexscaves:unmovable` and without a current block entity. Downward candidates additionally require a `nextInt(3) == 0` result before selection; that is not a one-third overall chance of moving down. Each walk has its own visited list, so later walks can revisit positions. Eight walks therefore give an upper bound of **80 processed nodes**, not 80 distinct changed blocks. This walk has a step budget and no biome-box containment test. [C7]

The initial node one block below the Crucible bypasses the neighbor candidate filters. On delayed application, the provider rechecks only the current `#alexscaves:unmovable` membership, writes through `Level.setBlockAndUpdate`, and removes the queue record. It does not recheck replaceability, a block entity, player ownership or the earlier visited condition there. The Java field is spelled `UNMOVEABLE`; its exact resource ID is **`alexscaves:unmovable`**, whose bundled payload includes `#minecraft:wither_immune`. Merged tag content remains runtime authority. [C2, C7, D3]

The inspected mutation methods do not call a claim/owner check, break/place event, gamerule permission gate or rollback service. This is an absence finding limited to those methods. It does not demonstrate how Minecraft/NeoForge internals, a claim mod, mixins or other installed components intercept the underlying writes, and it does not establish a runtime protection bypass.

## Costs and lifecycle

| Stage | Exact settlement / limit |
|---|---|
| Fresh target selection by right-click | Bound Treat retained; fill becomes 1. |
| Fresh target selection by dropped item | One bound Treat consumed; fill becomes 1. |
| Fresh conversion offerings | Eight ordinary offerings move fill 1→9; one final sacrifice moves 9→10. Each costs one requested item outside the creative right-click exemption. |
| Right-click creative offering | The one-item copy is consumed internally; held original is retained when `instabuild` is true. |
| Dropped offerings | Each accepted stack loses one directly; there is no creative-player exemption in this path. |
| Repeating on the retained target | Completion leaves fill 0 and request empty. A subsequent non-sneaking interaction rerolls the request without payment; starting from fill 0 then requires nine ordinary offerings plus the final sacrifice. The nine-offering count above applies to fresh target selection only. |
| Stored block-entity state | `WantStack`, `DisplayStack`, `ConvertingToBiome`, `FilledLevel`, `BiomeColor`, `SplashTimer`, `ConversionTime`, `WitchModeDuration`. |
| State not serialized by the inspected save/load methods | Delayed placement queue, visited lists, selected palette and original biome/block snapshots. The constructor creates an empty queue. |
| Completion / removal / refunds | Normal completion clears fill/time and retains target. These classes declare no removal handler or original-state restoration path; no cost refund or world rollback appears in the inspected lifecycle. Break/unload/restart outcomes require physical QA. |

| Final target branch, in predicate order | Final sacrifice, one item |
|---|---|
| `alexscaves:magnetic_caves` | `alexscaves:heart_of_iron` |
| `alexscaves:primordial_caves` | `alexscaves:tectonic_shard` |
| `alexscaves:toxic_caves` | `alexscaves:nuclear_bomb` |
| `alexscaves:abyssal_chasm` | `alexscaves:enigmatic_engine` |
| `alexscaves:forlorn_hollows` | `alexscaves:pure_darkness` |
| `alexscaves:candy_cavity` | `alexscaves:sweet_tooth` |
| Other target in `#minecraft:is_nether` | `minecraft:netherite_ingot` |
| Other target in `#minecraft:is_end` | `minecraft:dragon_breath` |
| Remaining target / unresolved target fallback | `minecraft:diamond` |

These items are consumed as offerings; this code does not place or detonate a sacrificed nuclear bomb, run an enigmatic engine, return a dragon-breath bottle, or grant the sacrificed item's normal use effect. Palette rolls and the final mapping are provider parameters. [C1–C3, C5, C10]

## Boundary / integration

The provider owns target binding, item matching/debit, request rolls, conversion time, palette selection, biome-cell writes, block replacement, sounds, particles, advancement credit and state reset. Black Arcana may catalog this root and observe an existing result once. It must not independently accept offerings, increment fill, start a second timer, replace blocks, refill biome cells, award duplicate credit, refund costs or restore provider state as an undocumented side effect.

`markUpdated()` calls `setChanged()` and `sendBlockUpdated(..., 3)`; update tags and `ClientboundBlockEntityDataPacket` carry the provider state. These synchronize the block entity and are not a supported Black Arcana cast API. No player owner identity or separate custom cast packet is established by the inspected Treat/Crucible path. Candidate method locators are evidence for the contract, not approval to inject into them. A mutating integration remains **`NOT_VERIFIED`**, including claim compatibility and exactly-once cost/world settlement. [C11]

## Validation

Static inspection covered the hashed publisher JAR, Treat and inherited binding helpers, Crucible interaction and full tick path, request/final mapping, palette generation, recursive queue and biome resolver, persistence/synchronization, exact unmovable tag identity, recipes, ingredient tags, loot and advancements. An independent static cross-check confirmed binding eligibility, first-selection cost asymmetry, creative exemption, item-identity matching, request bounds and repeated-cycle costs. No game was launched; no data-loss, multiplayer or claim-bypass incident was reproduced.

| Physical case | Required observation before QA promotion |
|---|---|
| Bind target | Food level 0 versus positive, creative, unbound versus bound Treat; cave/ordinary/Nether/End/modded biomes; verify current-position key and food outcome. |
| Select and pay | Right-click versus dropped Treat; eight ordinary plus final on fresh selection; creative exemption; item/component differences; repeated conversion from retained fill-0 target. |
| Timed conversion | Verify counter 20–90 walks and final biome write at the 100 branch; confirm one authoritative lifecycle at variable TPS and with chunk boundaries. |
| Biome extent | Compare quart samples across X/Y/Z bounds and alignment, including unavailable chunks; distinguish advancement AABB from mutated cells. |
| Block filtering | Palette blocks, replaceable neighbors, downward roll, unmovable tag, initial block below Crucible and block entities; change a queued position before application and inspect the actual rechecks. |
| Protection / multiplayer | Effective claim and gamerule behavior; multiple players feeding one Crucible, item automation, dimension variants and synchronized final state. |
| Persistence / interruption | Break, unload, save/reload, restart and witch-mode interruption at each phase; compare saved progress and queued placements. Observe actual remaining writes and costs without assuming rollback. |

## Exact evidence locators

Package prefix is `com.github.alexmodguy.alexscaves`. `BE` below abbreviates `server.block.blockentity.ConversionCrucibleBlockEntity`. JVM descriptors and bytecode offsets identify the exact binary; intervals refer to offset labels, not source line numbers.

| Ref | Exact class / descriptor / offsets or bundled resource |
|---|---|
| B1 | `server.item.BiomeTreatItem.<init>()V` 0–28; `use(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/InteractionHand;)Lnet/minecraft/world/InteractionResultHolder;` 0–64; `finishUsingItem(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;)Lnet/minecraft/world/item/ItemStack;` 0–70; `getUseAnimation(Lnet/minecraft/world/item/ItemStack;)Lnet/minecraft/world/item/UseAnim;` 0–3. |
| B2 | `server.item.CaveInfoItem.create(Lnet/minecraft/world/item/Item;Lnet/minecraft/resources/ResourceKey;)Lnet/minecraft/world/item/ItemStack;` 0–63; `getCaveBiome(Lnet/minecraft/world/item/ItemStack;)Lnet/minecraft/resources/ResourceKey;` 0–38. `server.misc.ACCompat.getTag(Lnet/minecraft/world/item/ItemStack;)Lnet/minecraft/nbt/CompoundTag;` 0–23; `setTag(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/nbt/CompoundTag;)V` 0–27 (custom-data helpers). |
| B3 | `server.item.ACFoods.<clinit>()V` 1637–1671 (`BIOME_TREAT`, `BIOME_TREAT_DONE`). |
| C1 | `server.block.ConversionCrucibleBlock.useItemOn(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/level/block/state/BlockState;Lnet/minecraft/world/level/Level;Lnet/minecraft/core/BlockPos;Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/InteractionHand;Lnet/minecraft/world/phys/BlockHitResult;)Lnet/minecraft/world/ItemInteractionResult;` 0–17; `acUse(Lnet/minecraft/world/level/block/state/BlockState;Lnet/minecraft/world/level/Level;Lnet/minecraft/core/BlockPos;Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/InteractionHand;Lnet/minecraft/world/phys/BlockHitResult;)Lnet/minecraft/world/InteractionResult;` 0–222; `<clinit>()V` 0–140 (shapes). |
| C2 | `BE.tick(Lnet/minecraft/world/level/Level;Lnet/minecraft/core/BlockPos;Lnet/minecraft/world/level/block/state/BlockState;Lcom/github/alexmodguy/alexscaves/server/block/blockentity/ConversionCrucibleBlockEntity;)V` 219–393 conversion gate/timer/reset; 672–837 server dropped-item collection; 840–940 queue application; 948–1006 witch expiry. |
| C3 | `BE.consumeItem(Lnet/minecraft/world/item/ItemStack;)V` 0–42. |
| C4 | `BE.getItemsAtAndAbove(Lnet/minecraft/world/level/Level;Lnet/minecraft/core/BlockPos;)Ljava/util/List;` 0–34; `lambda$getItemsAtAndAbove$0(Lnet/minecraft/world/level/Level;Lnet/minecraft/core/BlockPos;Lnet/minecraft/world/phys/AABB;)Ljava/util/stream/Stream;` 0–34. |
| C5 | `BE.rerollWantedItem()V` 0–269: witch 53–82, final 85–152, random bound and switch 158–266; `getFinalSacrificeForBiome(Lnet/minecraft/core/Holder;)Lnet/minecraft/world/item/ItemStack;` 0–242. |
| C6 | `BE.convertBiome()V` 0–32 target resolution; 33–149 advancements; 155–240 bounds; 248–348 server/available-chunk selection; 392–444 biome fill/dirty/resend. `makeResolver(Lorg/apache/commons/lang3/mutable/MutableInt;Lnet/minecraft/world/level/chunk/ChunkAccess;Lnet/minecraft/world/level/levelgen/structure/BoundingBox;ILnet/minecraft/core/Holder;)Lnet/minecraft/world/level/biome/BiomeResolver;` 0–10; `lambda$makeResolver$3(Lnet/minecraft/world/level/chunk/ChunkAccess;Lnet/minecraft/world/level/levelgen/structure/BoundingBox;Lorg/apache/commons/lang3/mutable/MutableInt;Lnet/minecraft/core/Holder;IIILnet/minecraft/world/level/biome/Climate$Sampler;)Lnet/minecraft/core/Holder;` 0–54. |
| C7 | `BE.recursivelySpreadBiomeBlocks(Ljava/util/List;Lnet/minecraft/core/BlockPos;II)V` 0–101 enqueue/palette/delay; 102–110 visited/budget; 122–244 candidate filters; 250–280 single-neighbor recursion. `isBiomeBlock(Lnet/minecraft/world/level/block/state/BlockState;)Z` 0–47. |
| C8 | `BE.getConversionAreaWidth()F` 0–3; `isWitchMode()Z` 0–12; `setWitchModeDuration(I)V` 0–5; `setConvertingToBiome(Lnet/minecraft/resources/ResourceKey;)V` 0–10. |
| C9 | `BE.updateTopAndBottomBlocks()V` 0–27 defaults, 30–51 server/target gate, 54–184 settings/fallbacks, 187–525 merged-rule evaluation, 531–541 caught warning; `getFallbackTopBlock`, `getFallbackMiddleBlock`, `getFallbackBottomBlock`, each `(Lnet/minecraft/core/Holder;)Lnet/minecraft/world/level/block/state/BlockState;` 0–44. |
| C10 | `BE.<init>(Lnet/minecraft/core/BlockPos;Lnet/minecraft/world/level/block/state/BlockState;)V` 17–25 queue allocation; `readCrucibleData(Lnet/minecraft/nbt/CompoundTag;Lnet/minecraft/core/HolderLookup$Provider;)V` 0–135; `saveAdditional` same descriptor 0–151. No removal override is declared in the inspected BE or block class. |
| C11 | `BE.markUpdated()V` 0–24; `getUpdateTag(Lnet/minecraft/core/HolderLookup$Provider;)Lnet/minecraft/nbt/CompoundTag;` 0–5; `getUpdatePacket()Lnet/minecraft/network/protocol/game/ClientboundBlockEntityDataPacket;` 0–4; `onDataPacket(Lnet/minecraft/network/Connection;Lnet/minecraft/network/protocol/game/ClientboundBlockEntityDataPacket;Lnet/minecraft/core/HolderLookup$Provider;)V` 0–41. |
| D1 | JAR `data/alexscaves/recipe/conversion_crucible.json`; `data/alexscaves/recipe/biome_treat.json`; `data/alexscaves/tags/item/storage_blocks/gold.json`; `data/alexscaves/tags/item/rock_candies.json`. |
| D2 | JAR `data/alexscaves/loot_table/blocks/conversion_crucible.json`; `data/alexscaves/advancement/alexscaves/conversion_crucible.json`; `data/alexscaves/advancement/alexscaves/convert_biome.json`; `data/alexscaves/advancement/alexscaves/convert_nether_biome.json`. |
| D3 | `server.misc.ACTagRegistry.<clinit>()V` 16–21 binds `UNMOVEABLE` to `alexscaves:unmovable`; JAR `data/alexscaves/tags/block/unmovable.json`. |

Sources: [exact artifact audit](../EXACT-1.0.10-ARTIFACT-AUDIT.md), [item/action disposition](../ITEM-ACTION-DISPOSITION-1.0.10.md), [technical contract proof root](../EXACT-TECHNICAL-CONTRACTS-1.0.10.md).
