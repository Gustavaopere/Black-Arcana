# Cloak of Darkness — Darkness Incarnate

- Provider: **Alex's Caves Continued** (`alexscaves`)
- Version: `1.0.10`
- Exact physical/publisher SHA-1: `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`
- Owner: `alexscaves:cloak_of_darkness` with the provider Darkness armor condition
- Trigger: provider armor key after charge/eligibility is satisfied
- State: `COUNTED_EXACT`

## Semantic identity

The provider resets cloak charge and applies the active Darkness Incarnate state to the wearer, including provider flight. Charge, light gates, HUD, input, duration, flight and cleanup belong to this one root; they do not change the provider's eight counted identities.

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

The bundled shaped Cloak recipe is `D_D / DOD / DDD`: 7 Shadow Silk and 1 Occult Gem. The Hood recipe is `DOD / D_D`: 4 Shadow Silk and 1 Occult Gem. Each yields one matching armor item. Assembled-pack recipe overrides are unverified. [D1]

## Charge, activation and targeting

1. `acInventoryTick` invokes the **executable private `acArmorTick`** for a Player wearing the stack. On the server, for the Cloak, that method reads charge and adds **one** when below configured charge time and the stack's `CanCharge` gate is true; it writes the tag and sends `UpdateItemTagMessage` when charge changes. This is present in 1.0.10 bytecode, independent of later source preprocessor comments. [A1–A2]
2. For an equipped chest Cloak, server inventory tick refreshes `CanCharge` when the last light timestamp is nonpositive or elapsed time is **>10 ticks**. The private eligibility predicate requires the Hood in HEAD, no active Darkness Incarnate and darkness under the light test; its `allowCreative=true` charge-refresh path lets creative Players bypass the light condition only. The stack gate defaults true when the entire tag is absent; otherwise it reads `CanCharge`. `acArmorTick` runs before this refresh in the inventory callback. [A1–A3]
3. The light test uses the **root vehicle's block position**. It reads block light and substitutes 15 when that position sees the sky and `sunAboveHorizon` is true. Light is disqualifying at **>=11**. The helper treats time-of-day fraction `<0.259` or `>0.74` as sun above horizon; preserve this predicate rather than replacing it with a new brightness approximation. [F1, H1]
4. The local client checks meter **>=1**, provider key **2** down, and that the chest stack is this Cloak; it sends `ArmorKeyMessage(CHEST.ordinal(),wearer.id,2)` and also calls `onKeyPacket` locally. The meter is `CloakCharge / configuredChargeTime`, and `hasMeter` requires Cloak+Hood and no active effect. These UI/client guards are not server authorization. [A2–A3]
5. `onKeyPacket` accepts a LivingEntity passing `canChargeUp(entity,false)`, sets **the supplied stack's charge to 0**, and adds Darkness Incarnate for configured flight time, amplifier 0, nonambient and without particles/icon. Its integer `key` argument is unused; it contains no full-charge, chest-Cloak or server-side check. Ordinary intended targeting is self/wearer; packet routing must be audited separately. [A4, N1]

## Parameters, costs and downstream effect

| Parameter / cost | Exact static value / rule | Evidence |
|---|---|---|
| Charge config | `darkness_cloak_charge_time`, default **1,000 ticks**, permitted **20..2,147,483,647** | C1 |
| Duration config | `darkness_cloak_fly_time`, default **200 ticks**, same permitted bounds | C1 |
| Nominal times at 20 TPS | 50 s charge / 10 s effect at defaults; effective server config and uninterrupted charge eligibility are unverified | C1, A1–A4 |
| Light / refresh | Disqualifying brightness >=11; refresh when timestamp <=0 or elapsed >10 | A2–A3, F1 |
| Activation debit | Reset charge to 0 before effect addition; no durability, mana, hunger, item consumption or separate cooldown debit in the inspected activation method | A4 |
| Flight while active | ServerPlayer `mayfly=true`, `flying=true`; flight speed `0.05F × 4 = 0.2F`; fall distance reset to 0 | F2 |
| Ground impulse | Effect tick adds **+0.1 Y velocity** when on the ground | F2 |
| Early light cancellation | `CommonEvents.livingTick` checks active effect every **5 entity ticks** and removes it when `isInLight(entity,11)` passes | L1 |
| End speed | Sets flight speed to **0.05F**, not a captured previous speed | F2 |
| End flight flags | Outside spectator: sets flying=false; sets mayfly=false for noncreative; requests slow-falling flag where accessor exists | F2 |
| Slow falling | The accessor flag is consumed by `LivingEntityMixin.ac_livingTick`, adding **80 ticks** of vanilla Slow Falling, amplifier 0, nonambient/no particles/icon | L3 |

The charge and duration config names differ (`charge_time` versus **`fly_time`**). These are binary-declared defaults/ranges, not a reading of the assembled server's config. Charge progress is stored in custom data (`CloakCharge`, `CanCharge`, `LastLightTimestamp`, `LastEquipMessageTime`). It is not an independent cooldown or Black Arcana resource pool. [A1–A4, C1]

## Packet path and authorization boundary

`ArmorKeyMessage.handle` enqueues its lambda. The lambda gets the sender (or local client Player), requires a non-null context Player, resolves `message.playerId` in that Player's level, **clamps** `equipmentSlot` to `0..EquipmentSlot.values().length−1`, requires the resolved entity be a Player, reads its slot item, and dispatches to `KeybindUsingArmor.onKeyPacket` with packet type. [N1]

The exact bridge registers bidirectional payload handling and supplies NeoForge's payload sender, then dispatches to the message handler. Neither that bridge nor this message lambda compares the resolved Player with the sender, checks full charge, validates `type==2`, or requires CHEST+Cloak specifically. The downstream Darkness method checks Hood/darkness/no-existing-effect, but adds no charge, stack-identity or key check. Hood and Cloak share the `DarknessArmorItem` class. These are exact static guard limits; no cross-player/uncharged activation exploit has been exercised. [N0–N1, A3–A4, A0]

`UpdateItemTagMessage` serializes item/custom data; its handler resolves a packet entity ID, then a matching main/off-hand item implementing `UpdatesStackTags`, and passes custom data to its default setter. It does not select an armor slot. Consequently the send in server `acArmorTick` does not alone establish successful equipped-Cloak client meter synchronization. Actual armor component/container synchronization and packet identity checks remain runtime QA. Directly writing charge or replaying either packet is not a verified adapter. [N2–N3]

## Effect cleanup, ownership and compatibility

`DarknessIncarnateEffect.onEffectEnd` calls `toggleFlight(false)`. The exact LivingEntity mixin invokes effect end on effect removal, and end/start on an update when its boolean update argument is true; provider `CommonEvents` also calls flight-off on remove/expiry events. Static cleanup paths therefore exist beyond a single source method. The light-cancellation branch reaches ordinary effect removal. [F2, L1–L2]

Flight mutation stores no previous speed/mayfly/flying snapshot and does not obtain a shared lease from other flight sources. The cleanup writes default speed and capability flags directly, and only calls `onUpdateAbilities` when the old `flying` value differs from the requested toggle boolean. Armor removal is not an explicit effect-end condition in the inspected effect/light tick; death, logout, dimension travel, forced removal, creative/spectator switching and cross-mod flight restoration require physical checks. Do not claim that all such paths restore another mod's flight entitlement. [F2, L1–L3]

The provider owns equipment eligibility, charge/tag state, input, effect addition/removal, light cancellation, flight, fall reset, slow falling, visuals and sounds. Black Arcana may observe an authoritative activation once. Duration/recharge/light/flight perks remain **fail-closed** with mutating hook **`NOT_VERIFIED`** until server sender/slot/charge settlement, synchronization and ownership-safe flight cleanup are established. Black Arcana must not zero charge, add the effect or restore flight independently as a second settlement.

## Validation and physical QA

Static checks verified exact artifact hashes; armor registration/class construction; executable charge/input/activation methods; config declarations; light/effect/flight consumers; actual network bridge, armor-key and custom-data handlers; removal/expiry/mixin/slow-fall paths; and both recipes. No game was launched. All cases below remain **`NOT_TESTED`**.

| Physical case | Required observation |
|---|---|
| Charge | Default/effective config, one increment per eligible server tick, <=10/>10 refresh, new/missing tags, equip order, Hood absent, creative light bypass, client meter synchronization. |
| Activation | Full/partial charge; key, sender identity and target Player, bounded slot, Hood versus Cloak dispatch, repeated input and exactly one charge reset/effect. |
| Effect / light | Speed, fall-distance reset, ground impulse, vehicle position, light 10/11, daytime sky and five-tick cancellation. |
| Cleanup / compatibility | Expiry, removal/update, armor removal, death/logout/reconnect, dimension change, creative/spectator transitions, dedicated server and concurrent flight providers; verify default-speed writes and 80-tick Slow Falling. |

## Exact evidence locators

Prefix is `com.github.alexmodguy.alexscaves`; descriptors are JVM signatures and offsets inclusive.

| Ref | Exact class / method / descriptor / offsets |
|---|---|
| A0 | `server.item.ACItemRegistry.<clinit>()V` 2446–2477; `lambda$static$134` / `$135()Lnet/minecraft/world/item/Item;` 0–13 construct Hood/Cloak using `DarknessArmorItem` and HELMET/CHESTPLATE. |
| A1 | `server.item.DarknessArmorItem.acArmorTick(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/player/Player;)V` 0–115; `canChargeUp(Lnet/minecraft/world/item/ItemStack;)Z` 0–23. |
| A2 | `DarknessArmorItem.acInventoryTick(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/Entity;Z)V` 0–266: armor callback 0–27; chest/owner check 30–70; server refresh 79–204; client meter/key/send 207–263. |
| A3 | `DarknessArmorItem.canChargeUp(Lnet/minecraft/world/entity/LivingEntity;Z)Z` 0–82; `getMeterProgress(Lnet/minecraft/world/item/ItemStack;)F` 0–35; `hasMeter(Lnet/minecraft/world/entity/player/Player;)Z` 0–74. |
| A4 | `DarknessArmorItem.onKeyPacket(Lnet/minecraft/world/entity/Entity;Lnet/minecraft/world/item/ItemStack;I)V` 0–126: eligibility 0–19, reset 22–39, effect 42–87. |
| C1 | `server.config.ACServerConfig.<init>(Lnet/neoforged/neoforge/common/ModConfigSpec$Builder;)V` 689–715 charge key/default/range; 718–745 flight key/default/range. |
| F1 | `server.potion.DarknessIncarnateEffect.isInLight(Lnet/minecraft/world/entity/LivingEntity;I)Z` 0–55. |
| F2 | `DarknessIncarnateEffect.tick(Lnet/minecraft/world/entity/LivingEntity;I)V` 0–80; `toggleFlight(Lnet/minecraft/world/entity/LivingEntity;Z)V` 0–166; `onEffectEnd(Lnet/minecraft/world/entity/LivingEntity;)V` 0–16; `isCreativePlayer(Lnet/minecraft/world/entity/LivingEntity;)Z` 0–31. |
| H1 | `server.misc.ACCompat.sunAboveHorizon(Lnet/minecraft/world/level/Level;Lnet/minecraft/core/BlockPos;)Z` 0–27. |
| L1 | `server.event.CommonEvents.livingTick(Lnet/neoforged/neoforge/event/tick/EntityTickEvent$Pre;)V` 68–125. |
| L2 | `CommonEvents.livingRemoveEffect(Lnet/neoforged/neoforge/event/entity/living/MobEffectEvent$Remove;)V` 0–74; `livingExpireEffect(Lnet/neoforged/neoforge/event/entity/living/MobEffectEvent$Expired;)V` 0–44; `mixin.LivingEntityMixin.ac_onEffectRemoved(Lnet/minecraft/world/effect/MobEffectInstance;Lorg/spongepowered/asm/mixin/injection/callback/CallbackInfo;)V` 0–28; `ac_onEffectUpdated(Lnet/minecraft/world/effect/MobEffectInstance;ZLnet/minecraft/world/entity/Entity;Lorg/spongepowered/asm/mixin/injection/callback/CallbackInfo;)V` 0–47. |
| L3 | `LivingEntityMixin.ac_livingTick(Lorg/spongepowered/asm/mixin/injection/callback/CallbackInfo;)V` 0–32; `setSlowFallingFlag(Z)V` 0–5. |
| N0 | `server.message.ACNetwork.registerPayloads(Lnet/neoforged/neoforge/network/event/RegisterPayloadHandlersEvent;)V` 0–26; `lambda$registerPayloads$0(Lcom/github/alexmodguy/alexscaves/server/message/ACNetwork$ACPayload;Lnet/neoforged/neoforge/network/handling/IPayloadContext;)V` 0–30; `ACNetwork$NeoForgeContext.getSender()Lnet/minecraft/server/level/ServerPlayer;` 0–27. |
| N1 | `server.message.ArmorKeyMessage.handle(Lcom/github/alexmodguy/alexscaves/server/message/ArmorKeyMessage;Lcom/github/alexmodguy/alexscaves/server/message/ACNetworkContext;)V` 0–20; `lambda$handle$0(Lcom/github/alexmodguy/alexscaves/server/message/ACNetworkContext;Lcom/github/alexmodguy/alexscaves/server/message/ArmorKeyMessage;)V` 0–121. |
| N2 | `server.message.UpdateItemTagMessage.<init>(ILnet/minecraft/world/item/ItemStack;)V` 0–14; `handle(Lcom/github/alexmodguy/alexscaves/server/message/UpdateItemTagMessage;Lcom/github/alexmodguy/alexscaves/server/message/ACNetworkContext;)V` 0–179. |
| N3 | `server.item.UpdatesStackTags.updateTagFromServer(Lnet/minecraft/world/entity/Entity;Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/nbt/CompoundTag;)V` 0–5; `server.misc.ACCompat.setTag(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/nbt/CompoundTag;)V` 0–27 (CUSTOM_DATA). |

| Resource ref | Exact JAR path | SHA-256 |
|---|---|---|
| D1 | `data/alexscaves/recipe/cloak_of_darkness.json` | `bb5a5e64b2f7a6200e91dd45e877bc4ad6c9c4aa1012e41c31acdfde89bb46e9` |
| D1 | `data/alexscaves/recipe/hood_of_darkness.json` | `1c3884eb43c47a87062f28461938a1ba4bde0c5af8676623707915c6a0ff7038` |

Sources: [exact artifact audit](../EXACT-1.0.10-ARTIFACT-AUDIT.md), [item disposition](../ITEM-ACTION-DISPOSITION-1.0.10.md), [common technical proof](../EXACT-TECHNICAL-CONTRACTS-1.0.10.md).
