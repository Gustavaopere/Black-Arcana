# Occult Gem + Beholder — Remote Observation

- Provider: **Alex's Caves Continued** (`alexscaves`)
- Version: `1.0.10`
- Exact physical/publisher SHA-1: `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`
- Owner: `alexscaves:occult_gem` + `alexscaves:beholder`
- Trigger: use of an Occult Gem previously bound to a valid Beholder
- State: `COUNTED_EXACT`

## Semantic identity

The provider starts a remote Beholder observation session and creates a Beholder Eye viewpoint tied to the player. Binding is preparation; camera synchronization, chunk requests, stopping and Eye removal are downstream lifecycle. These do not add an identity to the provider's eight counted roots.

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

## Exact acquisition and binding cost

The bundled Forlorn Ruins chest loot includes Occult Gem at weight 6; Watcher loot includes a 0–1 Gem count with Looting count increase. These are acquisition routes, not guaranteed drops. The Beholder recipe uses `BEB / _B_`, with 3 Thornwood Branches and 1 Occult Gem, and yields one Beholder. [D1]

`useOn` requires a Beholder block and a non-null player. A noncreative holder with exactly one Gem binds that same stack. Otherwise it creates one bound Gem, copies existing custom data, shrinks the original by one only for noncreative players, and adds the bound Gem to inventory or drops it if insertion fails. Thus binding a stack of Gems splits one into a bound stack; it is not an extra consumption on every observation. No durability, mana, hunger or cooldown debit appears in the inspected `use`/session-start methods. [G1–G2]

## Causal behavior, targeting and parameters

| Stage / parameter | Exact static behavior | Evidence |
|---|---|---|
| Binding | Writes `BeholderPos`, encoded `BeholderDimension` and `BeholderTracked=true` to stack custom data | G1 |
| Active versus usable | `isActive` accepts either position **or** dimension field. Position resolution needs both and a decodable dimension; active alone does not establish a valid session | G2 |
| Activation dimension | Requires resolved dimension equal to the user's current level dimension, server side and `ServerLevel`; no cross-dimension activation in this path | G2, 29–94 |
| Initial chunk request | Before checking the current block/type, requests a **3 × 3** chunk square at the bound position using the **player UUID**; passes load=true, ticking=true | G2, 97–160; G3 |
| Valid target | The current block must be `BEHOLDER` and its block entity a `BeholderBlockEntity`; invalid active bindings still return use-success | G2, 112–183 |
| Session start | Creates a Beholder Eye at block center plus Y −0.15, sets player UUID, sets yaw, calls world insertion and overwrites block `currentlyUsingEntityId` | B1 |
| Distance | `startObserving` checks **>1,000 blocks** for an advancement. That comparison is not an activation distance cap | B1, 19–48 |
| Entity insertion / concurrency | The insertion boolean is ignored. No existing-session/busy/owner lock or held-item recheck appears in `startObserving`; repeated starts must be tested | B1 |
| View motion | Eye movement is zero; its setter ignores velocity. While the user resolves, Eye tick zeroes the user's forward/vertical/strafe inputs | V1 |
| Camera start | Initial `prevStopPossession=true` versus false stop state causes server camera-start handling; sends `BeholderSyncMessage`, entity event 77 and marks camera control | V1–V2 |
| Eye chunk request | After full camera control, server requests one user-position chunk (if user resolves) plus a square around the Eye; radius `r=max(2,floor(server viewDistance/2))`, `(2r+1)^2` square calls, with the **Eye entity** as owner | V1, V3 |
| Chunk data | Loading also sends `ClientboundLevelChunkWithLightPacket` for every square position to the resolved ServerPlayer | V3, 134–207 |
| Fixed duration / range | No fixed session timer, mana debit, item cooldown or Gem-to-Eye distance cap appears in these inspected methods | G2, B1, V1 |

Chunk calls describe provider requests, not proven active tickets or a guaranteed count of distinct loaded chunks: the player's chunk can overlap the square, owners differ, and `ACPlatform.forceChunk` delegates only when its controller is non-null. The exact controller is registered as `alexscaves:forced_chunks` and delegates to NeoForge `TicketController`; framework behavior and effective view distance remain runtime authority. [P1–P2]

## Lifecycle, cleanup and state ownership

| Event / owner | Exact path and limit |
|---|---|
| Stack binding | Position/dimension/tracking in custom data. Server inventory tick skips validation when `BeholderTracked` exists and is false; otherwise same-dimension bindings are checked for a loaded non-Beholder block on `(holder.tickCount + holder.id) % 20 == 0`, and for world bounds. Invalid position/dimension keys are removed; tracking is retained. This method contains no chunk-release call. [G1–G3] |
| Block state | `UsingEntityID` persists and syncs the Eye's integer ID. `tick` follows the resolved entity's rotations and broadcasts changed ID; it does not clear an unresolved ID or enforce single-user access. [B1–B2] |
| Eye ownership | `UsingPlayerUUID` persists; server resolution uses the server player list, client resolution uses level player lookup. Transient loading/control/stop flags are not saved in these methods. [V4] |
| Stop input | The local controlling client detecting provider key 4 sends `PossessionKeyMessage(eyeId,playerId,0)`. Server tick also sets stop when the user is sneaking. `onPossessionKeyPacket` sets stop only when its supplied entity equals the Eye's resolved user; it ignores the integer type. [V1, V4, N1] |
| Normal stop sequence | Changed stop state sends reset sync/event 78, then clears the Eye's user UUID. On a later no-user tick, server calls `loadChunksAround(false)` if loading was active; after `tickCount > 3`, the Eye is discarded. [V1–V2] |
| Missing user / disconnect | The no-user tick unloads the Eye-centered square if loading was active. Its helper can release the player-position chunk only if a ServerPlayer still resolves; after UUID clearing/missing user that branch is skipped. [V1, V3] |
| Direct removal | Eye `remove` broadcasts event 78 and delegates to base removal; it does **not** itself call the chunk-release helper. Cross-level camera handling discards the Eye. [V2] |
| Ticket validation on loading | Registered callback `ACWorldData.clearLoadedChunksCallback` removes every entity-owner UUID and block-owner position returned by the provider's `TicketHelper` maps. This is a loading-validation cleanup path; it does not prove session-close release while the server keeps running. [P2–P3] |

The player-UUID initial **3 × 3** request has no matching release in the inspected Gem/Eye session paths. Eye cleanup uses a different owner, recomputes radius/position on unloading, and may no longer resolve the player's chunk. The loading-validation callback is real binary evidence, but does not close disconnect, early removal, changed view distance, dimension travel or repeated-use cleanup in an active server. These are static limitations to test, not a reproduced forced-chunk leak. Destroying the Beholder or removing the Gem is not an explicit Eye stop condition in the inspected Eye tick. [G2–G3, V1–V4, P3]

## Packet authority and integration boundary

The exact network bridge registers one bidirectional payload and dispatches messages to their handlers. Its context obtains the sender from NeoForge's payload player; it adds no per-message player/owner equality check. [N0]

`PossessionKeyMessage` resolves both Eye/camera and Player from packet integer IDs in the sender's current level and checks `PossessesCamera` plus Player type. It does **not** compare that packet Player with the sender. The Eye's downstream equality check verifies the **supplied resolved Player**, so it must not be presented as sender authorization. [N1, V4]

`BeholderSyncMessage` guards null server/player/level, resolves an Eye, then writes `hasTakenFullControlOfCamera=true` **before** comparing its controlling Player to the context Player for proxy camera changes. `BeholderRotateMessage` resolves/type-checks an Eye but performs no rotation write in the shipped handler. Do not infer authenticated server rotation settlement merely from message fields or names. Dedicated-server/client camera behavior remains untested. [N2–N3]

The provider owns binding, session creation, view state, input, packets, chunks, sync, sounds and cleanup. Black Arcana may observe an existing authoritative session once; it must not send these packets, clone cameras, force/unforce chunks, rewrite UUIDs/IDs, replay acquisition or add a session timer as an undocumented perk. A safe mutating hook remains **`NOT_VERIFIED`** and **fail-closed** until sender authorization, one-session ownership and complete ticket/camera release are established.

## Validation and physical QA

Static checks covered exact artifact hashes; Gem binding/use/inventory methods; block session/save-sync methods; Eye tick/stop/remove/ownership/chunk methods; actual network bridge and three handlers; NeoForge ticket delegation/registration/validation callback; and loot/recipe resources. No game was launched. All cases below remain **`NOT_TESTED`**.

| Physical case | Required observation |
|---|---|
| Binding / eligibility | One Gem, stacked Gems, creative, full inventory, automation/null player; partial/corrupt binding, wrong dimension and missing/destroyed block. |
| Session | Same-dimension distant view, start/stop, sneak/key release, player movement, repeated use and two users; verify actual client camera behavior on dedicated server. |
| Cleanup | Count both player-UUID and Eye-owner tickets before/after stop, disconnect, death, forced removal, block destruction, item removal, unload/reload, dimension travel, restart and changed view distance. |
| Authority | Verify sender versus packet player/eye IDs and no cross-player camera/stop mutation; demonstrate a supported server boundary before any adapter. |

## Exact evidence locators

Prefix is `com.github.alexmodguy.alexscaves`; JVM descriptors and inclusive bytecode offsets follow.

| Ref | Exact class / method / descriptor / offsets |
|---|---|
| G1 | `server.item.OccultGemItem.useOn(Lnet/minecraft/world/item/context/UseOnContext;)Lnet/minecraft/world/InteractionResult;` 0–251; `addBeholderTags(Lnet/minecraft/resources/ResourceKey;Lnet/minecraft/core/BlockPos;Lnet/minecraft/nbt/CompoundTag;)V` 0–40. |
| G2 | `OccultGemItem.isActive(Lnet/minecraft/world/item/ItemStack;)Z` 0–32; `getBeholderPosition(Lnet/minecraft/nbt/CompoundTag;)Lnet/minecraft/core/GlobalPos;` 0–56; `use(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/InteractionHand;)Lnet/minecraft/world/InteractionResultHolder;` 0–189. |
| G3 | `OccultGemItem.loadChunksAround(Lnet/minecraft/server/level/ServerLevel;Ljava/util/UUID;Lnet/minecraft/core/BlockPos;Z)V` 0–59; `acInventoryTick(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/Entity;Z)V` 0–174. |
| B1 | `server.block.blockentity.BeholderBlockEntity.startObserving(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/player/Player;)V` 0–114. |
| B2 | `BeholderBlockEntity.tick(Lnet/minecraft/world/level/Level;Lnet/minecraft/core/BlockPos;Lnet/minecraft/world/level/block/state/BlockState;Lcom/github/alexmodguy/alexscaves/server/block/blockentity/BeholderBlockEntity;)V` 0–245; `loadAdditional` / `saveAdditional(Lnet/minecraft/nbt/CompoundTag;Lnet/minecraft/core/HolderLookup$Provider;)V` each 0–16. |
| V1 | `server.entity.item.BeholderEyeEntity.tick()V` 0–230: missing-user cleanup 9–52; load 55–86; movement 89–113; client key 116–167; server camera/stop 170–227. `getDeltaMovement()Lnet/minecraft/world/phys/Vec3;` 0–3; `setDeltaMovement(Lnet/minecraft/world/phys/Vec3;)V` 0. |
| V2 | `BeholderEyeEntity.handleCameraServerSide(Lnet/minecraft/world/entity/Entity;Z)V` 0–72; `remove(Lnet/minecraft/world/entity/Entity$RemovalReason;)V` 0–15; `handleEntityEvent(B)V` 0–91. |
| V3 | `BeholderEyeEntity.loadChunksAround(Z)V` 0–222: player chunk 17–60, radius 63–87, square/packets 89–219. |
| V4 | `BeholderEyeEntity.onPossessionKeyPacket(Lnet/minecraft/world/entity/Entity;I)V` 0–22; `getUsingPlayer()Lnet/minecraft/world/entity/Entity;` 0–44; `readAdditionalSaveData` / `addAdditionalSaveData(Lnet/minecraft/nbt/CompoundTag;)V` 0–19 / 0–16. |
| N0 | `server.message.ACNetwork.registerPayloads(Lnet/neoforged/neoforge/network/event/RegisterPayloadHandlersEvent;)V` 0–26; `lambda$registerPayloads$0(Lcom/github/alexmodguy/alexscaves/server/message/ACNetwork$ACPayload;Lnet/neoforged/neoforge/network/handling/IPayloadContext;)V` 0–30; `ACNetwork$NeoForgeContext.getSender()Lnet/minecraft/server/level/ServerPlayer;` 0–27. |
| N1 | `server.message.PossessionKeyMessage.lambda$handle$0(Lcom/github/alexmodguy/alexscaves/server/message/ACNetworkContext;Lcom/github/alexmodguy/alexscaves/server/message/PossessionKeyMessage;)V` 0–82. |
| N2 | `server.message.BeholderSyncMessage.lambda$handle$0(Lcom/github/alexmodguy/alexscaves/server/message/ACNetworkContext;Lcom/github/alexmodguy/alexscaves/server/message/BeholderSyncMessage;)V` 0–142 (control flag 88–91; equality 107–113). |
| N3 | `server.message.BeholderRotateMessage.lambda$handle$0(Lcom/github/alexmodguy/alexscaves/server/message/ACNetworkContext;Lcom/github/alexmodguy/alexscaves/server/message/BeholderRotateMessage;)V` 0–62. |
| P1 | `server.misc.ACPlatform.forceChunk(Lnet/minecraft/server/level/ServerLevel;Ljava/util/UUID;IIZZ)V` and `forceChunk(Lnet/minecraft/server/level/ServerLevel;Lnet/minecraft/world/entity/Entity;IIZZ)V`, each 0–24. |
| P2 | `AlexsCaves.registerTicketControllers(Lnet/neoforged/neoforge/common/world/chunk/RegisterTicketControllersEvent;)V` 0–30; invokedynamic bootstrap 12 targets `ACWorldData.clearLoadedChunksCallback`. |
| P3 | `server.level.storage.ACWorldData.clearLoadedChunksCallback(Lnet/minecraft/server/level/ServerLevel;Lnet/neoforged/neoforge/common/world/chunk/TicketHelper;)V` 0–121. |

| Resource ref | Exact JAR path | SHA-256 |
|---|---|---|
| D1 | `data/alexscaves/loot_table/chests/forlorn_ruins.json` | `b8acfcb027c9b569a0a3eb9c2c2aa541ba197e63874d5b02930b7030588c9285` |
| D1 | `data/alexscaves/loot_table/entities/watcher.json` | `16b9e32d85d37c493391523b0912a8cd87643d1450df4a5e701823faac0432ab` |
| D1 | `data/alexscaves/recipe/beholder.json` | `4fc02e3ab39d687a5fed7de177b2f5467811ca28cfa5a07734d40d3b15c8e207` |

Sources: [exact artifact audit](../EXACT-1.0.10-ARTIFACT-AUDIT.md), [item disposition](../ITEM-ACTION-DISPOSITION-1.0.10.md), [common technical proof](../EXACT-TECHNICAL-CONTRACTS-1.0.10.md).
