# Totem of Possession — Possession / Remote Control

- Provider: **Alex's Caves Continued** (`alexscaves`)
- Version: `1.0.10`
- Exact physical/publisher SHA-1: `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`
- Owner: `alexscaves:totem_of_possession`
- Trigger: hold use with a valid bound totem; a melee hit establishes its binding
- State: `COUNTED_EXACT`

## Semantic identity

The provider transfers the user's viewing direction into ongoing remote control of the entity bound to the held stack. A melee hit establishes the binding; holding use directs movement toward the user's view hit and causes nearby attack/transfer settlement. Binding, movement, attacks, Astral Transferring, Detonating Death, release and invalidation are branches of **one** possession root. They do not add identities to the provider's eight counted roots.

This is an item use contract. `PossessionKeyMessage` dispatches to entities implementing `PossessesCamera` (Watcher/Beholder paths); it is not the Totem's movement or attack packet. Do not infer camera takeover or Watcher key controls from the item's name. [T2–T4, N4]

## Evidence and certification ceiling

The behavioral and numeric claims below come from direct `javap -p -c -s` inspection of publisher file `8856293`, `alexscaves` **1.0.10**, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, plus its bundled JSON. Bytecode offsets are local to the named method and exact artifact. These are static defaults/branches, not observations of an installed server.

| Field | Evidence status |
|---|---|
| Identity, behavior, numeric branches, targeting and resources | `EXACT_BINARY_STATIC`; references below |
| Effective server config, merged tags/enchantments and other mods' changes | `NOT_VERIFIED` |
| Black Arcana mutating hook | `NOT_VERIFIED`; no safe mutating extension is established here |
| Physical single-player/dedicated-server/multiplayer QA | `NOT_TESTED` |

The seven fields—identity, behavior, parameters, targeting, costs, integration and validation—are documented here at the `EXACT_BINARY_STATIC` ceiling. This does not promote hooks, physical QA or the certification ledger. The public source pin `523308608422ab8e31974befa7111ecdf495dd37` declares **Ship 1.1.1**; it is not the inspected 1.0.10 binary or authority for its numbers. See the shared [exact technical contract proof](../EXACT-TECHNICAL-CONTRACTS-1.0.10.md).

## Exact acquisition

Bundled `data/alexscaves/recipe/totem_of_possession.json` is a shaped crafting recipe yielding one Totem: `DED / DBD / DBD`, where `D` = `alexscaves:moth_dust` (6), `E` = `alexscaves:occult_gem` (1), and `B` = `alexscaves:thornwood_branch` (2). The inventory advancement observes acquisition; it is not an additional ability or another acquisition method. [D1]

## Causal behavior and targeting

1. **Bind by melee hit.** `hurtEnemy` delegates to `acHurtEnemy`. A target in `#alexscaves:resists_totem_of_possession`, or a Player when the player config is false, is rejected with `item.alexscaves.totem_of_possession.invalid` for a player attacker. Otherwise the provider sets target persistent `TotemPossessed=true`, stores `BoundEntityUUID` and serialized `BoundEntityTag` including the entity type `id` on the stack, and plays `TOTEM_OF_POSSESSION_USE`. The method returns true in both branches. It does not itself apply an additional possession damage amount. [T1, T2]
2. **Resolve and begin use.** On server use, UUID resolution occurs in the user's current `ServerLevel`, and `ControllingEntityID` is refreshed for clients. A previously bound but unresolved/dead entity causes server reset of the binding. A surviving bound entity begins use only when the user passes the look-and-line-of-sight gate, or Sightless level is positive; otherwise use returns pass. No distance-cap comparison against 32 occurs in this eligibility gate. [T3, T6, T7]
3. **Recheck each use tick.** A bound target that becomes unresolved/dead, or a stack at maximum damage, enters termination. Otherwise an absent binding/target, a failed look gate without Sightless, or a controlled Player when player possession is disabled stops use. These latter stop branches retain the binding. [T4]
4. **Command movement.** The user's view ray selects a destination; projectile-hittable entities are eligible ray hits except the controlled entity. A Mob receives a navigation `moveTo(destination, ramp × speed)` command. Other entities receive the velocity/rotation branch below. The ray origin is the user, not the controlled entity. This is a command reach, not a demonstrated maximum user-to-bound-target separation. [T4, T8]
5. **Settle nearby attacks on the server.** Query the controlled entity's bounding box inflated by 3 on all axes. Candidates must be projectile-hittable LivingEntities; exclude the controlled entity, the user, allies in either direction, and passengers sharing its vehicle. For a controlled Mob, set `target` and `lastHurtByMob` for each eligible candidate. For a controlled Player, call `attack(target)` and `resetAttackStrengthTicker()` for each candidate. The code iterates the returned list rather than selecting one nearest target. It adds no separate line-of-sight or radial-distance test to this inflated-box query. Damage remains the controlled entity's normal attack settlement, not a fixed Totem damage value. [T4]

The exact resistance-tag payload contains `#c:bosses`, `minecraft:warden`, `minecraft:armor_stand`, `alexscaves:hullbreaker`, `alexscaves:forsaken`, `alexscaves:atlatitan`, and `alexscaves:tremorzilla`. The same JAR contributes `alexscaves:luxtructosaurus` to `#c:bosses` with `replace:false`. Other data packs can expand or replace the effective tags. Player possession config key `totem_of_possession_works_on_players` defaults to **true** in this binary; the running value is unverified. [D2, C1]

The look gate is geometric, not a fixed five-block range: let `d0` be entity distance, `v` the normalized user view, `u` the normalized vector from user eye to target eye, and `d1` that vector's length. It requires `v·u > 1 − [5 × (1 + 0.1 × d0)] / d1` **and** `hasLineOfSight(target)`. Sightless bypasses this test. Preserve the provider predicate, including zero-distance behavior; do not replace it with a new range check. [T7]

## Parameters, modifiers and costs

| Parameter | Exact static value / rule | Authority |
|---|---|---|
| Item durability / rarity | 1000 / uncommon | T1 |
| Use animation / maximum use duration | Block / 72,000 ticks (3,600 s at 20 TPS) | T5 |
| Ramp | `elapsed = 72000 − timeUsing`; `ramp = elapsed < 15 ? elapsed / 15F : 1F` | T4, offsets 275–308 |
| View-ray command distance | `32F × ramp` blocks | T4, 310–350 |
| Speed factor | `1.25F + 0.35F × Rapid Possession level`; Mob navigation speed is `ramp × factor` | T4, 318–404 |
| Non-Mob velocity | `oldVelocity × 0.8F + direction × (0.15F × factor)`; normalize direction only when its length exceeds 1 | T4, 450–648 |
| Non-Mob grounded obstacle step | Add `(0, 0.6, 0)` when non-flying, horizontally colliding, grounded and destination is above it; otherwise positive Y is flattened for non-flying entities | T4, 427–537, 613–628 |
| Non-Mob rotation | When direction length exceeds 1, set yaw/body yaw on server toward the destination | T4, 537–596 |
| Nearby attack selection | Controlled bounding box inflated by 3 blocks; filters above | T4, 717–878, 1054–1078 |
| Use wear | On even `timeUsing`, increment stack damage by 1 **on the client only**, unless user is a creative Player | T4, 230–272 |
| Depletion | `damage >= maxDamage` enters termination; `releaseUsing` shrinks the stack by 1 at that threshold | T4, 28–142; T9, 41–54 |
| Melee attributes | Main hand adds attack damage 2 and attack speed −2.4; these are item attributes, not remote attack bonuses | T1, T5 |
| Enchantability | Value 1; enchantable when stack count equals 1 | T1 |

The use wear branch directly calls `setDamageValue`, rather than `hurtAndBreak`; it contains no Unbreaking calculation. Its nominal client rate is 1 point per 2 use ticks, but **a server-authoritative 100-second lifetime is not established**. The actual tag-sync path copies custom data and does not copy the damage component (see integration boundary). No mana, hunger or cooldown debit appears in the inspected item methods. Normal melee attack settlement, recipes, enchanting, repairs and external modifiers remain provider/game authority. [T4, N1–N3]

| Enchantment | Bundled maximum | Downstream behavior |
|---|---:|---|
| `alexscaves:rapid_possession` | III | Adjusts the speed factor; nominal factors 1.60, 1.95, 2.30 at levels I–III. Does not change the 32-block view-ray limit. |
| `alexscaves:sightless` | I | Bypasses the look/line-of-sight use gate. Controlled Mobs are set glowing while commanded; release clears glow. |
| `alexscaves:astral_transferring` | I | For a controlled Mob, every fourth elapsed use tick, a nearby candidate with **strictly greater current health** and no resistance tag can replace the binding. Sets the new target's possessed flag, UUID and serialized tag; refreshes ID and sound. No separate player-config check appears inside this transfer branch; the next tick's Player gate still applies. |
| `alexscaves:detonating_death` | I | On termination from target loss/death or stack depletion, if a controlled entity still resolves, create a TotemExplosion at its position, radius `2 + floor(entity width)`, attributed to the user, with block interaction `KEEP`; execute and finalize it. No blast occurs when target resolution is null. |

Bundled enchantment definitions support `#alexscaves:enchantable/totem_of_possession`, whose item tag contains this Totem. Detonating Death declares Astral Transferring in its exclusive set. These data-level limits do not clamp the level used by the numeric code; effective enchantment data and nonstandard levels are unverified. [D3, T4]

Detonating Death is not a separate cast or guaranteed death-only trigger: durability exhaustion also reaches the branch, and the call site has no client/server guard. Its custom explosion excludes its source user in the entity query, delegates explosion immunity to `ACPlatform.ignoreExplosion`, explicitly skips Luxtructosaurus, and uses exposure/distance-scaled explosion damage and knockback; it does not reuse the possession attack ally filters. With `R = 2 + floor(width)`, distance ratio `q = distance / (2R)`, and block exposure `e`, eligible targets within `q <= 1` receive `floor(((b²+b)/2) × 7 × 2R + 1)`, where `b=(1−q)e`; a zero-length explosion-to-eye direction is skipped (TNT uses feet Y). Final damage remains subject to the target/game pipeline. `KEEP` prevents block destruction in this path. Do not replay this blast from Black Arcana. [E1]

## State, lifecycle and ownership

| Event / state | Provider behavior and limit |
|---|---|
| Binding storage | Stack custom data: `BoundEntityUUID`, `BoundEntityTag`, `ControllingEntityID`. `BoundEntityTag` supports display/tooltip; this control path resolves an existing world entity by UUID and does not respawn the stored snapshot. |
| Entity marker | Persistent `TotemPossessed` boolean. It contains no owner UUID or totem identity. Illager alliance logic returns false when either side has this marker; a possessed Raider can become another Raider/Illager's retaliation target. |
| Normal release / sight loss / player-config rejection | Stops command ticks. Release clears resolved target glow, sends the client tag update and checks depletion; it does **not** remove UUID/tag binding or `TotemPossessed`. Existing AI navigation/target/velocity is not explicitly reset by `releaseUsing`. |
| Dead/unresolved entity at initial use | Server removes the three binding keys and clears the resolved entity marker when available. Resolution is limited to the current ServerLevel, so dimension/unload absence is not distinguished from other resolution failure in this branch. |
| Death/unresolved/depletion during use | Optional Detonating Death when target resolves; clear resolved target marker, reset binding keys, stop use and send client tag update. |
| Rebind / Astral transfer | Overwrites this stack's binding. The inspected rebind and transfer branches do not clear the previous target's marker. Transfer's loop also does not break after a successful candidate. |
| Drop, trade, duplicate totems, logout, dimension travel, reload | No item-specific owner/unique-controller check, scheduled cleanup, drop/logout callback or cross-dimension search appears in the inspected class. Do not claim exclusive ownership or automatic stale-marker cleanup. Persistence/reload and concurrent users need physical QA. |

These limits matter because the marker changes provider alliance/retaliation behavior beyond the held-use duration. Black Arcana must not normalize them by clearing flags, recreating entities or rewriting tags as an undocumented side effect. [T2–T4, T6, T9, M1, N3]

## Integration boundary and real perk limits

The provider owns binding eligibility, use gates, movement/navigation, nearby targeting, normal attacks, transfers, explosions, wear/depletion, persistent tags, sounds, red dust and red outline/glow. Black Arcana can catalog the action and observe an existing provider result once. It must not independently bind, move, retarget, attack, detonate, spend wear or reset possession state.

`UpdateItemTagMessage` is the actual item synchronization path: release/stop sends it client → server, and server UUID/ID refresh broadcasts it when the integer ID changes. The handler finds an entity by packet entity ID in the sender's level, requires a LivingEntity, picks a main-hand matching item first (else off hand), requires `UpdatesStackTags`, and applies received custom data through its default `updateTagFromServer`. In the inspected method there is no sender/entity equality, bound-target authorization, distance, binding-content validation or damage-component copy. `ACCompat.getTag/setTag` read/write **CUSTOM_DATA** only. Therefore the client wear branch is not proof that dedicated-server durability is decremented. [N1–N3]

This is a static call-path limitation, not a multiplayer exploit demonstration. `PossessionKeyMessage` is outside this Totem path, and is not a substitute authorization layer. No Black Arcana packet replay or direct NBT/component mutation is approved by this card. A mutating hook remains **`NOT_VERIFIED`** until the server-authoritative binding/use/cost settlement and sender authorization are independently demonstrated. [N4]

| Proposed perk surface | What the exact provider actually reads / permits concluding |
|---|---|
| Command reach | The ray distance is the local `32 × ramp` value in `onUseTick`; it is distinct from the geometric look gate and target UUID lookup. There is no inspected public reach setter, distance config or maximum user-to-bound-target distance check. A reach perk needs a verified provider seam at the ray calculation, including client/server agreement. |
| Movement speed / ramp | Rapid Possession modifies the local `1.25 + 0.35 × level` factor each tick. Mob path speed also multiplies by ramp; non-Mob acceleration does not, and retains velocity damping/step rules. Changing a Mob movement attribute or writing velocity once does not establish a Totem speed/ramp modifier. |
| Target count / damage / transfer | The server scans an inflated box, iterates every eligible candidate and delegates actual attacks. Astral transfer is a Mob-only four-tick branch and does not break the list loop. There is no Totem spell-damage scalar, nearest-target selector or supported target-count setter here. A second attack/transfer would duplicate provider settlement. |
| Sightless / duration / resource efficiency | Sightless changes the look gate/glow, not ray reach. Maximum use duration is a separate constant from wear/depletion, and client wear does not establish server resource settlement. Neither reducing a Black Arcana cost nor rewriting custom data proves a provider durability or duration benefit. |
| Binding / ownership / detonation | UUID, serialized tag, ID, marker and explosion branches are internal state, not extension APIs. A perk must preserve rejection, lifecycle and one authoritative explosion; it cannot infer safe ownership from `TotemPossessed` or enable control by replaying the tag packet. |

These are observed internal methods and data predicates, not a supported mutating API. **Fail closed** for all proposed mutations until a provider-owned hook, its execution timing, authority and single settlement are verified; data-level enchantment compatibility alone is insufficient.

## Validation and reproducible checks

Static validation inspected the hashed publisher JAR, item registration/constructor, all item methods and lambdas, actual tag handler/default implementation, config declaration, custom-data helpers, TotemExplosion, possession marker mixins, and bundled recipe/tag/enchantment data. Source snapshots alone and translated tooltips were not used as exact numeric authority. No game was launched: all physical cases below remain **`NOT_TESTED`**.

| Physical case | Required observation before QA promotion |
|---|---|
| Bind / reject / rebind | Valid mob, resistance-tag entity and Player with config true/false; inspect UUID, ID and old/new markers without adding a second action root. |
| Use / ramp / targeting | 15-tick ramp, full 32-block command ray, Mob navigation vs Player velocity, failed line of sight and Sightless behavior; nearby box filters and normal attack outcomes. |
| Costs | Compare client and server damage components across even use ticks, release, reconnect and exhaustion; creative exemption and stack removal. |
| Transfer | Strict current-health comparison, four-tick cadence, resistant target exclusion, multiple candidates, transfer to Player with config false, previous marker retention. |
| Detonation | Death and depletion, null target, damage attribution, allies/source immunity, block preservation, server/client duplication and exactly one authoritative settlement. |
| Release / persistence | Sight loss, release, death, unload, logout, drop/trade, dimension change and save/reload; verify binding/marker/glow/AI cleanup as actually shipped. |
| Multiplayer authority | Two holders / duplicate or transferred binding, packet sender/entity ownership and hand selection; demonstrate a supported server boundary before any mutating hook. |

## Exact evidence locators

Package prefix below is `com.github.alexmodguy.alexscaves`. Method signatures specify JVM descriptors; bytecode offset intervals are inclusive labels, not source line numbers.

| Ref | Exact class / descriptor / bytecode offsets |
|---|---|
| T1 | `server.item.ACItemRegistry.<clinit>()V` 2310–2324 and `lambda$static$126()Lnet/minecraft/world/item/Item;` 0–7 register/construct the Totem. `server.item.TotemOfPossessionItem.<init>()V` 0–83; `getEnchantmentValue()I` 0–1; `isEnchantable(Lnet/minecraft/world/item/ItemStack;)Z` 0–13. |
| T2 | `TotemOfPossessionItem.hurtEnemy(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/LivingEntity;)Z` 0–7; `acHurtEnemy` same descriptor 0–154; `setPossessed(Lnet/minecraft/world/entity/Entity;Z)V` 0–33. |
| T3 | `TotemOfPossessionItem.use(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/InteractionHand;)Lnet/minecraft/world/InteractionResultHolder;` 0–150. |
| T4 | `TotemOfPossessionItem.onUseTick(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/item/ItemStack;I)V` 0–142 termination, 143–229 stop gates, 230–272 client wear, 275–648 movement, 651–714 client particles, 717–1084 server attacks/transfer. |
| T5 | `TotemOfPossessionItem.getUseAnimation(Lnet/minecraft/world/item/ItemStack;)Lnet/minecraft/world/item/UseAnim;` 0–3; `getUseDuration(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/LivingEntity;)I` 0–3; `acModifiers(Lnet/minecraft/world/entity/EquipmentSlot;Lnet/minecraft/world/item/ItemStack;)Lcom/google/common/collect/Multimap;` 0–15. |
| T6 | `TotemOfPossessionItem.getBoundEntityUUID(Lnet/minecraft/world/item/ItemStack;)Ljava/util/UUID;` 0–32; `updateEntityIdFromServer(Lnet/minecraft/server/level/ServerLevel;Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/item/ItemStack;)V` 0–104; `getControlledEntity(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/item/ItemStack;)Lnet/minecraft/world/entity/Entity;` 0–90; `resetBound(Lnet/minecraft/world/item/ItemStack;)V` 0–31. |
| T7 | `TotemOfPossessionItem.isEntityLookingAt(Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/Entity;D)Z` 0–124; use/use-tick pass the constant 5.0 at offsets 99 and 158. |
| T8 | `TotemOfPossessionItem.lambda$onUseTick$0(Lnet/minecraft/world/entity/Entity;Lnet/minecraft/world/entity/Entity;)Z` 0–20 (ray filter). |
| T9 | `TotemOfPossessionItem.releaseUsing(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;I)V` 0–57. |
| C1 | `server.config.ACServerConfig.<init>(Lnet/neoforged/neoforge/common/ModConfigSpec$Builder;)V` 668–686 (player-possession key/default). |
| N1 | `server.message.UpdateItemTagMessage.handle(Lcom/github/alexmodguy/alexscaves/server/message/UpdateItemTagMessage;Lcom/github/alexmodguy/alexscaves/server/message/ACNetworkContext;)V` 0–179; `read(Lnet/minecraft/network/FriendlyByteBuf;)Lcom/github/alexmodguy/alexscaves/server/message/UpdateItemTagMessage;` 0–15; `write(Lcom/github/alexmodguy/alexscaves/server/message/UpdateItemTagMessage;Lnet/minecraft/network/FriendlyByteBuf;)V` 0–17. |
| N2 | `server.item.UpdatesStackTags.updateTagFromServer(Lnet/minecraft/world/entity/Entity;Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/nbt/CompoundTag;)V` 0–5 (default implementation inherited by Totem). |
| N3 | `server.misc.ACCompat.getTag(Lnet/minecraft/world/item/ItemStack;)Lnet/minecraft/nbt/CompoundTag;` 0–23; `getOrCreateTag` same descriptor 0–29; `setTag(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/nbt/CompoundTag;)V` 0–27; `getPersistentData(Lnet/minecraft/world/entity/Entity;)Lnet/minecraft/nbt/CompoundTag;` 0–4. |
| N4 | `server.message.PossessionKeyMessage.lambda$handle$0(Lcom/github/alexmodguy/alexscaves/server/message/ACNetworkContext;Lcom/github/alexmodguy/alexscaves/server/message/PossessionKeyMessage;)V` 0–82; its exact-JAR class references are WatcherEntity, BeholderEyeEntity and network registration, not TotemOfPossessionItem. |
| M1 | `mixin.IllagerMixin.ac_isAlliedTo(Lnet/minecraft/world/entity/Entity;Lorg/spongepowered/asm/mixin/injection/callback/CallbackInfoReturnable;)V` 0–29; `mixin.LivingEntityMixin.ac_onSetLastHurtByMob(Lnet/minecraft/world/entity/LivingEntity;Lorg/spongepowered/asm/mixin/injection/callback/CallbackInfo;)V` 0–62; each class's `isPossessed(Lnet/minecraft/world/entity/Entity;)Z` 0–9. |
| E1 | `server.entity.util.TotemExplosion.<init>(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/Entity;DDDFLnet/minecraft/world/level/Explosion$BlockInteraction;)V` 0–119; `explode()V` 403–409 (`2R`), 494–530 (source exclusion), 615–652 (immunity/range), 655–733 (nonzero direction), 757–805 (exposure/damage), 809–888 (knockback); `finalizeExplosion(Z)V` 0–247; `interactsWithBlocks()Z` 0–15. |
| D1 | JAR `data/alexscaves/recipe/totem_of_possession.json`; `data/alexscaves/advancement/alexscaves/totem_of_possession.json`. |
| D2 | JAR `data/alexscaves/tags/entity_type/resists_totem_of_possession.json`; `data/c/tags/entity_type/bosses.json`. |
| D3 | JAR `data/alexscaves/enchantment/{rapid_possession,sightless,astral_transferring,detonating_death}.json`; `data/alexscaves/tags/item/enchantable/totem_of_possession.json`. |

Sources: `../EXACT-1.0.10-ARTIFACT-AUDIT.md`, `../ITEM-ACTION-DISPOSITION-1.0.10.md`.
