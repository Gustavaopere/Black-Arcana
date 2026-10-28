# Recruitment contract

Status: `BINARY_VERIFIED` for exact publisher Acolyte 1.0.3; installed-JAR equality and assembled-pack behavior are `NOT_VERIFIED`, physical QA is `NOT_TESTED`. Recruitment is a provider companion/economy mechanic and adds **0 Acolyte-owned spells**. See [release evidence](../BINARY-CONTRACTS-1.0.3.md) and the [artifact manifest](../ARTIFACT-CATALOG-MANIFEST-1.0.3.json).

`IRecruitableCompanion` defines ownership, order and contract APIs. `HumanEntity` implements it; Human Mage, Warrior and Archer inherit that implementation. The [confirmation protocol](recruit-confirmation-protocol.md) accepts only `HumanEntity`, so a demon's use of the same spell host does not make it recruitable through this route.

## Acquisition, ownership and price

Interacting with an unowned Human opens the recruit menu on the server. An existing owner can reopen the owned menu; a different player's interaction delegates to the host superclass. Hiring is an explicit client-to-server confirmation. The server obtains the entity's **current** recruit cost, counts exact `minecraft:emerald` stacks in the player's main inventory list, removes the price, then assigns ownership and contract end time. No item is supplied by the entity; no mana, XP, school, spell level or progression gate is tested by this recruitment path. Creative mode has no exemption in the confirmation handler.

| Selected profile state | Emerald price | Duration in game ticks | Nominal time at 20 TPS |
|---|---:|---:|---:|
| Tier 1, or any tier other than 2–4 | 5 | 24,000 | 20 minutes |
| Tier 2 | 7 | 48,000 | 40 minutes |
| Tier 3 | 9 | 72,000 | 60 minutes |
| Tier 4 | 11 | 96,000 | 80 minutes |
| Null selected profile | 1 | 72,000 | 60 minutes |

The six publisher live pools contain only tiers 1–3. Tier 4 is supported by the Human cost/duration switches but is not a fourth shipped tier in those pools. The interface's generic defaults are 1 emerald and 24,000 ticks; the table records the actual Human overrides, including their distinct null-profile duration. A menu's displayed tier falls back to 1 when the profile is null, so that label does not establish the fallback price/duration.

`isRecruited()` means only that owner UUID is non-null. `isOwnedBy(Player)` compares the player's UUID with that stored UUID. The owner object is resolved by `Level.getPlayerByUUID` in the companion's current level; this is not a global cross-dimension player lookup. Owner UUID, end time and stay order are ordinary Human fields, not the skin/anger synchronized-data fields; the menu supplies an owner-facing snapshot to its recipient.

## Contract clock and release

Hiring sets `ownerUUID = player UUID` and `contractEndTime = level.gameTime + getContractDurationTicks()`, then sends the hiring message. `HumanEntity` also emits 10 happy-villager particles on the server. Duration uses world **game time**, not time-of-day or a real-time deadline.

The interface helpers define:

- Active contract: `contractEndTime > 0`; ownership is not part of this helper's condition.
- Remaining ticks: 0 when inactive, otherwise `max(0, contractEndTime − level.gameTime)`.
- Progress: 0 when inactive, otherwise `remainingTicks / current getContractDurationTicks()`, as floats. It is a remaining fraction, not elapsed progress; no upper clamp is applied.
- Expiry: on a server-side contract tick, an active contract with remaining ticks ≤0 invokes `onContractExpired()`.

`HumanEntity#tick` calls this check after its host tick. An unloaded entity is not polled by this method; its next server tick evaluates the saved absolute deadline against current game time. No offline-owner pause, owner-death extension, refund or renewal operation appears in these methods. Confirmation against an already recruited entity returns without extending the deadline, even for its current owner.

**Actual Human expiry releases the companion.** Both `HumanEntity#onUnRecruit` and `#onContractExpired` run server-side smoke particles, clear owner UUID, set end time to −1 and set stay order false. They do not discard the Human and do not refund emeralds. The interface's default expiry implementation sends `contract_expired` and discards the entity, but Human overrides it without calling that default; those default effects must not be attributed to these three recruitable families.

If an owned Human dies on the server, it sends `gui.acolyte.recruit.companion_died` to the owner when that owner resolves as a `ServerPlayer`, clears ownership/end time and delegates to normal host death. Combat, drops and target changes after loss of ownership belong to the [Human family](../entities/human-family.md), not to a separate recruitment spell.

## Orders and save fields

Follow and Stay are owner-only packet actions setting one boolean; see the [stay-order goal](../goals/stay-order.md) for the ground/water/owner-threat conditions. No emerald or mana charge accompanies an order or release. `recruit()` itself does not set the stay boolean; ordinary release/expiry clears it.

| NBT key | Stored value / read fallback |
|---|---|
| `OwnerUUID` | UUID written when non-null; absent/invalid UUID reads as no owner. |
| `ContractEndTime` | Long; absent key reads as −1. |
| `OrderedToStay` | Human boolean; restored when the key exists, otherwise constructor default false remains. |

Human save/load calls the interface ownership serialization and separately persists stay, profile, skin and anger state. The profile/skin fields and loader-order implications are covered by the [archetype pipeline](archetype-loadout-pipeline.md). These binary paths establish intended persistence, not a successful restart/dimension migration test.

## Technical contract

| Quantity | Value / authority |
|---|---|
| Target | One current-level Human entity ID; owner UUID identifies the hiring player. No creature summoning occurs. |
| Effective range | Normal interaction starts menu opening; confirmation adds no explicit distance or line-of-sight check. See protocol evidence. |
| Price | Table above; exact emerald identity, no creative waiver in this handler. |
| Mana / cast time / cooldown | No local mana debit, casting stage or action cooldown in recruitment. Host combat spell costs are separate. |
| Duration | Absolute game-time deadline; 20 ticks = 1 nominal second. |
| Damage / area / projectile / velocity | N/A; hiring/order/release deals no direct damage and creates no projectile. Particles are cosmetic. |
| Spell level / school | N/A for recruitment; host spellcasting stays with Iron's. |
| Integration state | Protection, multiplayer, Black Arcana observers, Mastery/perks and assembled-pack lifecycle: `NOT_VERIFIED` / `NOT_TESTED`. |

## Binary evidence

Class names are under `net.raptorzizi.acolyte.entity.mobs.wizards.human` unless otherwise noted.

- `IRecruitableCompanion`: ownership helpers PCs 0–26; `#getRecruitCost()I` PCs 0–1 and `#getContractDurationTicks()J` PCs 0–3; `#hasActiveContract` PCs 0–16; `#getRemainingContractTicks(Level)` PCs 0–26; `#getContractProgress(Level)` PCs 0–27; `#tickContract(Level)` PCs 0–34; default `#recruit(Player,Level)` PCs 0–59; serialization PCs 0–33 / 0–52. The **unused Human default-expiry** behavior is at `#onContractExpired` PCs 0–61.
- `HumanEntity`: constructor PCs 0–56; `#getRecruitCost` PCs 0–60; `#getContractDurationTicks` PCs 0–65; `#tick` PCs 0–40; `#mobInteract` PCs 0–63; `#openRecruitScreen` PCs 0–225; `#recruit` PCs 0–60; release and expiry overrides each PCs 0–64; `#die` PCs 0–72; save/load PCs 0–88 / 0–147; `lambda$new$0` PCs 0–22 resolves the owner supplier.
- `net.raptorzizi.acolyte.network.PacketConfirmRecruit#lambda$handle$2` PCs 0–209 proves validation/payment/recruit ordering; its helpers prove count/remove behavior. Full menu/wire/UI causality is documented in the [confirmation protocol](recruit-confirmation-protocol.md).
