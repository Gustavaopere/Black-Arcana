# Magic Conch — Summon Deep Ones

- Provider: **Alex's Caves Continued** (`alexscaves`)
- Version: `1.0.10`
- Exact physical/publisher SHA-1: `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`
- Owner: `alexscaves:magic_conch`
- Trigger: charged use/release
- State: `COUNTED_EXACT`

## Semantic identity

The provider settles one temporary allied Deep One group summon for the user. Deep One, Deep One Knight and Deep One Mage are participants or variants of this same root rather than separate summon identities. Charge, enchantments, failed placement, lifetime, reputation and cooldown are branches of this root. The provider's eight counted identities do not change.

## Evidence and certification ceiling

The behavioral and numeric claims below are `EXACT_BINARY_STATIC`: direct `javap -p -c -s` inspection of publisher file `8856293`, **1.0.10**, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, and its bundled data. Offsets belong to the named method in this artifact. See [the common technical proof](../EXACT-TECHNICAL-CONTRACTS-1.0.10.md).

| Static contract field | Evidence / remaining limit |
|---|---|
| Identity | Exact owner, entry point and one causal action documented below; `COUNTED_EXACT` retained. |
| Behavior | Exact entry and downstream settlement/lifecycle inspected. |
| Parameters | Exact constants, expressions and bundled defaults identified; effective pack config/data remain `NOT_VERIFIED`. |
| Targeting | Exact eligibility, owner and selection gates documented. |
| Costs | Exact resource/state debits and their ordering documented. |
| Integration boundary | Provider settlement and unsafe mutation paths identified; a supported Black Arcana mutating hook remains `NOT_VERIFIED`. |
| Validation | Artifact, bytecode and resource checks performed; physical single-player/dedicated-server/multiplayer QA remains `NOT_TESTED`. |

Public source pin `523308608422ab8e31974befa7111ecdf495dd37` declares **Ship 1.1.1**. It can corroborate names/control flow but cannot certify 1.0.10 values; no matching public 1.0.10 source pin has been established. These static findings do not certify effective runtime behavior, a safe hook or physical QA.

## Exact acquisition

Bundled `data/alexscaves/loot_table/gameplay/deep_one_knight_barter.json` includes `alexscaves:magic_conch` as a weighted Deep One Knight barter result. Its entry weight is 10 in a one-roll pool; this is not a guaranteed barter reward. Effective loot overrides and barter gameplay remain unverified. [D1]

## Causal behavior and targeting

1. `use` starts held use, emits `INSTRUMENT_PLAY`, and returns consume. Release plays the cast sound **before** checking charge. It calculates `charge = getUseDuration(stack,null) − timeLeft` and enters cost/summon/cooldown only when **charge > 25 ticks**; 1,200 ticks is the maximum use duration, not a required charge. [C1–C2]
2. The release first settles durability/Taxing Bellow, then computes `time = 1200 + 400 × Lasting Morale level`. The spawn/count branch is server-only; wear occurs before that side check. The Player stat/cooldown block follows it and has no separate side check in this method. [C2]
3. With Charting Call level zero, requested limits are **3 Deep Ones, 2 Knights, 1 Mage**: each added `nextInt(1)` is zero. Each family gets at most **99 placement attempts**, stopping earlier when its counter reaches the limit. The counters increment on a non-null return from `summonDeepOne`. [C2]
4. Placement starts at the summoner's block position plus random integer X/Z offsets **−10 through 9** and Y **+7**. It descends through water/empty cells while above minimum build height, then requires water or a block on which the summoner can stand. The entity is placed at that block's center plus Y 0.5, assigned owner/lifetime, finalized as `TRIGGERED`, and checked for obstruction. It then calls `addFreshEntity`, copies the target, and returns the entity. The boolean result of `addFreshEntity` is discarded; a non-null return is **not proof of accepted world insertion**. [C3]
5. `copyTarget` keeps an existing living target; otherwise it prefers the summoner's `getLastHurtMob`, falling back to `getLastHurtByMob` only when the former is null. The selected candidate must be alive, not the summoner, not allied to the summoner or summon, and not a Deep One. No cursor/ray target, fixed attack radius or spell damage is set by the Conch. Subsequent attacks belong to each entity's AI/combat pipeline. [E3]

## Parameters, enchantments and costs

| Parameter | Exact static rule | Evidence |
|---|---|---|
| Item durability / rarity | 5 / uncommon | C0 |
| Use animation / maximum use | Bow / 1,200 ticks | C1 |
| Minimum release gate | Strictly greater than 25 elapsed ticks | C2, 23–41 |
| Base requested group | 3 / 2 / 1; at most 99 attempts per family | C2, 122–397 |
| Lifetime counter and cooldown input | `1200 + 400 × Lasting Morale level` ticks; nominal 1,200/1,600/2,000/2,400 at bundled levels 0/I/II/III | C2, 86–101, 443–448; D2 |
| Cooldown scope | `ACCompat.addCooldown` passes the stack's **Item** to `ItemCooldowns.addCooldown`; not a unique-stack timer | N1 |
| Normal wear | `hurtAndBreakUsedHand(stack,1,summoner)` after a qualifying release, before placement; no success-count refund in the method | C2, 74–80 |
| Taxing Bellow | Instead of normal wear, invokes `setDamageValue(Math.min(0, damage−1))`, sets the reputation-debit flag, then after family loops calls `lastNonNullSummon.addReputation(summonerUUID,−2)` only if one exists | C2, 44–71, 397–415 |
| Enchantability | Value 1; stack count must equal 1 | C1 |

The Taxing Bellow expression is **`Math.min`**, not a verified clamp to zero. For a positive damage value it passes 0; for damage 0 it passes −1 to the game method. The effective damage component's treatment of that argument has not been tested. Reputation resolves through the provider world data, rather than deducting 2 independently for every participant. [C2, E4]

Charting Call is especially relevant to any quantity perk. For positive level `L`, the binary adds `nextInt(max(L−1,2))`, `nextInt(max(L−2,0))`, and `nextInt(max(L−3,0))` to the three limits, in that order. [C2, 158–221]

| Charting level | Deep One bound | Knight bound | Mage bound | Static interpretation |
|---|---:|---:|---:|---|
| 0 | Not entered | Not entered | Not entered | Base 3/2/1 limits |
| I | 2 | 0 | 0 | A zero-bound Knight call is reached before placement if prior calls complete |
| II | 2 | 0 | 0 | Same zero-bound Knight call |
| III | 2 | 1 | 0 | A zero-bound Mage call is reached before placement if prior calls complete |
| IV | 3 | 2 | 1 | All bounds positive; requested limits 3–5 / 2–3 / 1 |

Bundled Charting Call maximum is **IV**; Lasting Morale is **III**; Taxing Bellow is **I** and excludes vanilla Unbreaking/Mending in its definition. All support `#alexscaves:enchantable/magic_conch`, whose bundled tag contains the Conch. These data limits do not clamp arbitrary levels in the method. [D2]

The zero-bound invocations are an exact static finding. The RNG implementation, exception outcome, cost ordering on an actual server and levels I–IV require physical regression; this card does **not** claim a reproduced modpack crash. No mana, hunger or separate item consumption debit appears in the inspected activation methods.

## State, lifetime and ownership

`setSummonedBy` sets the summoned flag, stores the summoner UUID and initializes the synchronized counter. For a summoned Deep One, a Player with that UUID receives the `HELPFUL` reaction; all Deep Ones are allied to other Deep Ones. This does not establish exclusive command ownership or an owner-disconnect removal rule. [E1, E3]

In `DeepOneBaseEntity.tick`, positive summon time decrements **once per server entity tick**. Summon animation progress rises toward 20 while time is positive and decreases after expiry; server discard occurs when time is nonpositive and progress reaches zero. Therefore the cooldown input is the lifetime **counter**, not a promise of exact disappearance at that same wall-clock tick. AI is gated while a summoned entity's progress is below 20. No wall-clock/offline decrement or summoner-presence check appears in this inspected lifecycle. [E1–E2]

The provider saves/loads `ConchSummoned`, `ConchUUID` and `ConchTime`; unload/reload is not an implicit cancellation. Normal death, other removal and AI settlement remain entity authority. Black Arcana must not recreate the group, rewrite the counter/UUID, repeat the reputation debit or independently remove the entities. [E1]

## Integration boundary

The provider owns use/release, sound, charge, wear, RNG, placement, entity initialization/AI/attacks, reputation, stat, cooldown and expiry. Black Arcana may catalog the root and observe an existing authoritative result once. It must not replay the release, count placement attempts as accepted summons, or replace provider target/ally rules.

Quantity/duration/cost perks remain **fail-closed**. A mutating hook is **`NOT_VERIFIED`** until a supported server boundary proves bounded counts, valid RNG bounds, exactly one debit/cooldown, owner attribution, spawn acceptance and lifecycle persistence. Direct tag edits or a second summon loop are not a verified integration seam.

## Validation and physical QA

Static checks verified the exact artifact hashes, owner constructor, use/release/placement bytecode, cooldown helper, Deep One counter/owner/target/reputation/save-load consumers, and bundled loot/enchantment/tag resources. No game was launched; all physical cases remain **`NOT_TESTED`**.

| Physical case | Required observation |
|---|---|
| Charge and costs | Releases at 25/26 ticks, failed placement, creative/normal users, both hands, normal wear and Taxing Bellow at damage 0/positive; one authoritative cost/cooldown. |
| Quantity | Charting Call 0/I/II/III/IV on the exact JAR; capture RNG outcome and any failure before attributing a gameplay bug. |
| Placement / targeting | Water, land, blocked/void/minimum-height sites; failed entity insertion; last-hurt target precedence and ally exclusions; provider AI damage only. |
| Lifetime / persistence | Counter expiry plus disappearance, owner death/logout/dimension change, chunk unload/reload, world restart and multiple casts/users. |

## Exact evidence locators

Prefix is `com.github.alexmodguy.alexscaves`; descriptors are JVM signatures, intervals are inclusive bytecode labels.

| Ref | Exact class / method / descriptor / offsets |
|---|---|
| C0 | `server.item.ACItemRegistry.<clinit>()V` 2021–2035; `lambda$static$107()Lnet/minecraft/world/item/Item;` 0–24 constructs the Conch with durability 5/uncommon. |
| C1 | `server.item.MagicConchItem.use(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/InteractionHand;)Lnet/minecraft/world/InteractionResultHolder;` 0–32; `getUseDuration(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/LivingEntity;)I` 0–3; `getUseAnimation(Lnet/minecraft/world/item/ItemStack;)Lnet/minecraft/world/item/UseAnim;` 0–3; `getEnchantmentValue()I` 0–1; `isEnchantable(Lnet/minecraft/world/item/ItemStack;)Z` 0–13. |
| C2 | `MagicConchItem.releaseUsing(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;I)V` 0–451; sound 0–20, charge 23–41, cost 44–80, lifetime 86–101, server guard 103–107, count/RNG 110–221, loops 223–397, reputation 397–415, stat/cooldown 418–448. |
| C3 | `MagicConchItem.summonDeepOne(Lnet/minecraft/world/entity/EntityType;Lnet/minecraft/world/entity/LivingEntity;I)Lcom/github/alexmodguy/alexscaves/server/entity/living/DeepOneBaseEntity;` 0–304; placement 6–151, owner/finalization 230–271, obstruction/insertion/target 272–302. |
| E1 | `server.entity.living.DeepOneBaseEntity.setSummonedBy(Lnet/minecraft/world/entity/LivingEntity;I)V` 0–18; `addAdditionalSaveData(Lnet/minecraft/nbt/CompoundTag;)V` 79–119; `readAdditionalSaveData(Lnet/minecraft/nbt/CompoundTag;)V` 98–141; `isEffectiveAi()Z` 0–30. |
| E2 | `DeepOneBaseEntity.tick()V` 115–314 (progress, server countdown and discard). |
| E3 | `DeepOneBaseEntity.copyTarget(Lnet/minecraft/world/entity/LivingEntity;)V` 0–92; `getReactionTo(Lnet/minecraft/world/entity/player/Player;)Lcom/github/alexmodguy/alexscaves/server/entity/util/DeepOneReaction;` 0–43; `isAlliedTo(Lnet/minecraft/world/entity/Entity;)Z` 0–49. |
| E4 | `DeepOneBaseEntity.addReputation(Ljava/util/UUID;I)V` 0–103; `getReputationOf(Ljava/util/UUID;)I` 0–33; `setReputationOf(Ljava/util/UUID;I)V` 0–28. |
| N1 | `server.misc.ACCompat.addCooldown(Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/item/ItemStack;I)V` 0–12. |

| Resource ref | Exact JAR path | SHA-256 |
|---|---|---|
| D1 | `data/alexscaves/loot_table/gameplay/deep_one_knight_barter.json` | `57c4a14e6a92f963e726ed92136034a091bdf8929398e8ba2b9d94a6c302c818` |
| D2 | `data/alexscaves/enchantment/charting_call.json` | `352ec52d0e21298a921cc10fe5253b0484c0b273adf3fc5713bce046758ccacd` |
| D2 | `data/alexscaves/enchantment/lasting_morale.json` | `8c662fb7f68987d8e564ec053ebccdd9232593e5961d2213bbbed037b270232f` |
| D2 | `data/alexscaves/enchantment/taxing_bellow.json` | `275b7ef42207724ae8ee2048097d3f16dbdfc60796f06a98eb77356ddb744df1` |
| D2 | `data/alexscaves/tags/item/enchantable/magic_conch.json` | `730151144ab45cb149cf6adfdf5d9cfb69b450238ff126f7f1ac33a0406d2cd8` |

Sources: [exact artifact audit](../EXACT-1.0.10-ARTIFACT-AUDIT.md), [item disposition](../ITEM-ACTION-DISPOSITION-1.0.10.md), [common technical proof](../EXACT-TECHNICAL-CONTRACTS-1.0.10.md).
