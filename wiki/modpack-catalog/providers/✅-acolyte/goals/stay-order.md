# Stay order goal

Status: `BINARY_VERIFIED` for exact publisher Acolyte 1.0.3; installed-JAR equality and assembled-pack behavior are `NOT_VERIFIED`, physical QA is `NOT_TESTED`. This AI order is not a spell and adds **0 Acolyte-owned spells**. See [release evidence](../BINARY-CONTRACTS-1.0.3.md) and the [artifact manifest](../ARTIFACT-CATALOG-MANIFEST-1.0.3.json).

`net.raptorzizi.acolyte.entity.goals.GenericStayOrderGoal` accepts a `PathfinderMob` and an owner-entity supplier. Human's shared goal registration installs it at priority **2**, with its current-level owner supplier. The [confirmation protocol](../systems/recruit-confirmation-protocol.md) permits the stored owner to send Follow (`false`) or Stay (`true`); [recruitment](../systems/recruitment-contract.md) persists the boolean and clears it on release/expiry.

## Activation and continuation

The constructor claims goal flags **MOVE** and **JUMP**. `canUse()` requires all of:

- The mob implements `IRecruitableCompanion` and `isRecruited()` is true.
- It is outside water/bubble and is on the ground.
- Its stay-order boolean is true.
- It is not in the following owner-threat case: supplier returns a living owner, squared distance to that owner is **strictly less than 144 blocks²** (distance <12 blocks), and the owner's `getLastHurtByMob()` is non-null.

The threat check reads the owner's last attacker reference; this goal adds no recency timer, attacker's distance check or owner-target reassignment. At exactly 12 blocks the proximity exception does not apply. A null/non-living owner does not by itself prevent activation when the other conditions hold.

`canContinueToUse()` has a deliberately smaller condition set: the mob must implement the interface, be outside water/bubble and still have its stay boolean true. It does not repeat recruitment, on-ground, owner proximity or last-attacker checks. Thus the entry conditions and continuation conditions must not be treated as identical.

`start()` stops path navigation once. `stop()` is empty. This class has no custom tick action, target clearing, cast cancellation, teleport, pose animation or damage action. Its MOVE/JUMP flags participate in normal goal arbitration; actual combat/follow behavior remains the responsibility of the Human/role and Iron's goal contracts.

## Technical contract

| Quantity | Value / authority |
|---|---|
| Affected entity | The constructor's single companion mob; no area target acquisition. |
| Owner-threat proximity | `<144 blocks²`, equivalent to `<12 blocks`; used only on entry. |
| Damage / mana / emeralds | None charged or dealt by this goal. |
| Spell level / cast / cooldown | N/A; this is an order flag and goal eligibility. |
| Duration | Until continuation fails or higher goal arbitration intervenes; no fixed tick countdown in this class. Release/expiry clears the flag. |
| Projectile / speed / knockback | N/A. Start stops navigation; it defines no motion vector or movement-speed value. |
| Persistence | Human `OrderedToStay` NBT boolean; ownership/end-time behavior belongs to the recruitment contract. |

Evidence: `GenericStayOrderGoal#<init>(PathfinderMob,Supplier)` PCs 0–27; `#canUse()Z` PCs 0–112; `#canContinueToUse()Z` PCs 0–40; `#start()V` PCs 0–10; `#stop()V` PC 0. `HumanEntity#registerGoals()V` PCs 33–50 installs priority 2; its owner supplier is `lambda$new$0` PCs 0–22. Packet order authorization is `PacketConfirmRecruit#lambda$handle$2` PCs 88–116. No live stay/follow, threat-response, pathfinding, multiplayer or protection test was performed.
