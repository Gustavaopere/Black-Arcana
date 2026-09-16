# Mobstein 5.4.4 — Black Arcana integration and deduplication rules

## Governing rule

Mobstein remains authority for its own **corporeal reconstruction** runtime. Black Arcana may later react to provider-owned state only through a verified safe boundary. Similarity to Souls & Death does not transfer ownership.

## Authority matrix

| Surface | Authority | Black Arcana rule |
|---|---|---|
| full bodies / anatomical remains | Mobstein | do not mirror into a second corpse ledger |
| organ extraction | Mobstein | do not synthesize provider organs from Black Arcana death credit |
| Clinical Stretch resurrection | Mobstein | do not bypass provider resurrection gates |
| Reviver/Lightningbolt/Mobstenio/Suspicious syringes | Mobstein | preserve item-specific semantics and exceptions |
| resurrected creature tame/AI/lifecycle | Mobstein | no second ownership or respawn controller |
| Surgery Stretch | Mobstein | no duplicate surgery execution pipeline |
| Attack/Health/Speed/Template surgery perks | Mobstein | do not reinterpret as RPG Skill Tree perks or Black Arcana mastery |
| Subject Assembly | Mobstein | treat as provider mannequin/test-subject system, not soul projection |
| Igor experiments | Mobstein | do not recreate provider RNG pool |
| Dr. Mobstenio | Mobstein | preserve NPC progression/lifecycle |
| Witherstein | Mobstein | preserve boss awakening/progression |
| Mobstein structures | Mobstein/worldgen | no global scans or force-loading |
| Soul Anchor / Mortal Ledger / Black Arcana soul contracts | Black Arcana | remain separate metaphysical systems |
| Goety Soul Energy | Goety | never substitute Mobstein corpses/organs |
| Malum spirits | Malum | never flatten into Mobstein organs/bodies |
| Eidolon soul state | Eidolon | preserve provider identity |
| RPG attributes/mastery | RPG Skill Tree where contracted | may gate/credit only through real causal integration, never own Mobstein runtime |

## Resurrection deduplication

The word `resurrection` spans multiple providers but does not imply one universal resource.

Mobstein's public model is physical reconstruction:

`body/remains + machine/syringe + provider acquisition gates -> reconstructed creature`

Black Arcana Souls & Death uses its own bounded metaphysical contracts. Therefore:

- do not consume Black Arcana Soul Anchor charges to pay Mobstein resurrection;
- do not generate Black Arcana soul currency when a Mobstein machine revives a body;
- do not convert Mobstein organs into generic Black Arcana souls;
- do not automatically revive a Mobstein pet through Black Arcana death hooks;
- do not replace Mobstein's night/day syringe gating with Black Arcana casting.

A future intentional bridge must define exactly what crosses the boundary and must preserve both providers' real costs.

## Companion and summon deduplication

Mobstein resurrected creatures and experiments may behave as tameable companions/bodyguards, but they are not Black Arcana summons merely because they accompany the player.

Black Arcana must not:

- register them in a second summon-cap ledger;
- infer ownership from who triggered a nearby spell;
- clean them up as temporary summons;
- teleport/respawn them through generic Black Arcana summon recovery without a provider contract;
- award repeated mastery for existence, aura ticks or idle time.

## Mastery/progression credit

If a future RPG Skill Tree integration wants to reward meaningful Mobstein accomplishments, credit must be based on a server-authoritative causal fact such as a verified provider event for a completed resurrection, experiment creation or boss milestone.

Until such a hook exists:

`NO CAUSAL HOOK -> NO AUTOMATIC MASTERY CREDIT`

Specifically prohibited:

- polling nearby resurrected mobs every tick;
- credit for continuous buffs/auras;
- credit from guessed entity names;
- credit from client packets or GUI interaction alone;
- duplicate credit when one provider operation produces several downstream effects.

## Damage/proc causality

Damage caused by Mobstein companions remains Mobstein/entity combat unless a future bridge establishes owner-attributed causal semantics.

Black Arcana Backlash and offensive proc systems must not automatically treat companion damage as a Black Arcana spell hit. This preserves the existing no-proc-chain/backlash invariants.

## World safety

Mobstein publicly documents world-affecting behavior such as structure progression, lightning presentation, Spider-surgery cobweb placement and Snow Golem surgery potentially breaking the Surgery Stretch.

These are provider-owned world effects. Black Arcana `WorldEffectPolicy` governs Black Arcana mutations; it must not double-apply, cancel or “re-settle” Mobstein's own changes unless a future explicit compatibility adapter is designed for that purpose.

Any Black Arcana operation targeting a Mobstein structure/entity still obeys normal Black Arcana world-border, protection, loaded-chunk and bounded-work policies.

## Sable boundary

Mobstein 5.4.4 declares Sable compatibility, and Sable 2.0.5 is installed. The exact behavioral seam remains unverified.

Therefore:

- do not assume Mobstein machines are safe on moving Sable structures;
- do not assume reconstructed entities migrate between Sable sub-levels correctly;
- do not force-load or scan Sable spaces to find Mobstein machines;
- do not create a Mobstein↔Sable adapter from inferred internals;
- do not equate Sable core compatibility with Sable Ragdolls or other Sable addons.

## Optional integration posture

Because no supported Mobstein API/event surface is proven, integration must currently be absent rather than heuristic.

Acceptable future pattern:

1. exact Mobstein and Sable versions confirmed from modlist;
2. supported public boundary documented/proven;
3. server-authoritative causal event/data identified;
4. adapter isolated behind a Black Arcana-owned interface;
5. provider costs/state remain provider-owned;
6. dedup identity defined;
7. missing/incompatible provider fails closed;
8. tests verify no double-processing.

Unacceptable pattern:

- reflection into ARR internals;
- guessed registry IDs;
- classpath scanning every tick;
- entity-name matching as ownership proof;
- duplicate corpse/soul/resource stores;
- client-authoritative resurrection or mastery.

## Phase 3 result

Mobstein is sufficiently cataloged for semantic overlap decisions at the public behavior level, but provider-specific code integration remains:

`NOT APPROVED / FAIL-CLOSED`.