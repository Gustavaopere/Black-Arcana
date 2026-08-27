# Mahou Tsukai — public/observable feature inventory

Accessed: 2026-08-27
Primary source: https://www.curseforge.com/minecraft/mc-mods/mahou-tsukai
Reference version visible on source page: 1.21.1 v1.36.27, NeoForge, released 2026-06-07.

This document records only public player-visible behavior. It deliberately does not describe classes, algorithms, packet formats, data structures, assets or implementation details.

## Baseline experience

The reference mod uses a persistent mana pool shown as `Mahou X/Y`; public documentation says maximum mana increases by one for each 100 mana spent. Most spell construction starts with player blood, a ground circle and three category catalysts, sometimes converted into a scroll. A separate Mystic Code item stores three stacks of scrolls and cycles the selected stack. These are important design references primarily because Black Arcana intends to replace them: no permanent second mana HUD, no universal grind-based max-resource growth, no universal blood-circle busywork and no mandatory scroll/staff-like casting container.

## Boundaries

| Reference mechanic | Public behavior | Useful fantasy | Reference problems / Black Arcana concern |
| --- | --- | --- | --- |
| Alarm Boundary | Stationary area alerts the owner when something enters. | Occult ward/perimeter security. | Easy to duplicate vanilla/mod security; persistent area ticking can scale poorly. |
| Enclosure Boundary | Produces an enclosure/base-like structure. | Instant magical refuge. | Primarily substitutes building and creates world mutation; low priority for forbidden magic. |
| Tangible Boundary | Invisible barrier permits caster passage while blocking others. | Personal exclusion ward. | Collision/AI/PvP trapping and persistent-area cost. |
| Displacement Boundary | Teleports things across the boundary; public docs explicitly warn blocks can move. | Spatial threshold. | Severe grief/duplication/contraption risk if block movement is retained. |
| Gravity Boundary | Increases gravity for everyone inside except caster. | Suppression field. | Crowd-control abuse, boss trivialization and compatibility with movement/gravity mods. |
| Drain Life Boundary | Converts nearby health into caster health, fullness and mana; described as expensive. | Sanguine harvesting ward. | Multi-resource positive feedback can become self-sustaining; mob farms/automation can trivialize cost. |

Boundary scrolls can rapidly place a boundary and do not themselves cost mana, while the resulting boundary does. Black Arcana should treat rapid deployment as an invocation UX decision, not duplicate the reference scroll economy.

## Displacement

| Reference mechanic | Public behavior | Useful fantasy | Reference problems / overlap |
| --- | --- | --- | --- |
| Ascension | Teleports caster/entrants to surface; stationary use charges per teleport. | Emergency vertical escape. | Ars already offers broad teleport tools; little unique forbidden identity. |
| Protective Displacement | Enderman-like defensive teleport/evasion. | Reactive blink defense. | Can become pseudo-invulnerability without charges/cooldown and safe-position validation. |
| Projectile Displacement | Teleports caster to their last surviving arrow. | Projectile anchor traversal. | Strong identity if restricted to owned/marked projectiles and safe landing. |
| Ordered Displacement | Network of circles teleports through placement order and loops. | Ritual waygate chain. | Persistent network/chunk bookkeeping; overlaps Ars portals/warp systems. |
| Equivalent Displacement | Paired circles swap entities/items at long range when both chunks are loaded. | Reciprocal transposition. | Player consent, container/automation exploits and forced-chunk concerns. |
| Mental Displacement | Astral projection within a finite radius; exceeding range returns caster. | Vulnerable-body reconnaissance. | Camera/body synchronization, logout/death handling and abuse through walls. |
| Scrying | Uses a named target to temporarily view a loaded target and some surroundings in same dimension, with visibility limitations. | Namescry/divination. | Player privacy/PvP information leak; must not force-load targets/chunks. |

## Projection / weapon manifestation

| Reference mechanic | Public behavior | Useful fantasy | Reference problems / Black Arcana concern |
| --- | --- | --- | --- |
| Strengthening | Temporarily heals/protects durability and improves mining tier/speed/melee damage on a selected item. | Ephemeral occult tempering. | Tool-tier bypass and stacking with modded attributes/enchants. |
| Projection | Memorizes an observed item/tool, then produces a low-durability copy. | Eidetic/spectral replication. | Arbitrary NBT/item duplication is unacceptable in a large modpack. |
| Proximity-projection weapon | Summons a weapon and teleports caster toward attacked target at range. | Rift blade / gap-closing armament. | Copyright-specific presentation must be discarded; teleport needs collision/range checks. |
| Bow of weapon projectiles | Conjured bow launches tools/weapons instead of arrows. | Arsenal-as-ammunition. | Arbitrary item handling can duplicate or destroy data; better as spectral snapshots. |
| Reality-altering personal arena | Sends caster and optionally a target to a personal sword-filled space; exit is tied to target/death/damage behavior. | Forbidden personal domain. | Stranding, logout, cross-dimension persistence, death-item loss and arena grief risks. |
| Power Consolidation | Large world ritual/lake transforms enchanted sword into stronger holy sword; public docs say process can be repeated and expose a nerf factor. | Sacrificial weapon ascension. | Explicit recursive permanent power growth and large terrain mutation. |
| Treasury Projection | Uses weapons from inventory/ender storage to attack enemies. | Spectral arsenal. | Live inventory/NBT duplication, ender-storage coupling, projectile/entity spam. |

## Mystic / offensive control

| Reference mechanic | Public behavior | Useful fantasy | Reference problems / Black Arcana concern |
| --- | --- | --- | --- |
| Damage Replication | Damage and potion effects received by caster are reproduced on a selected target. | Sympathetic wound linkage. | Boss one-shot loops, reflect recursion, arbitrary effect propagation. |
| Large shield | Creates a large protective shield that pushes entities away. | Manifest ward/aegis. | Generic shield overlap; entity collision/knockback abuse. |
| Explosive mana condensation | Charged large explosion plus smaller alternate area mode. | Catastrophic charged spell. | Redundant with existing magic and direct terrain grief; only worthwhile if world-policy-safe and mechanically distinct. |
| Spatial disorientation | Throws one targeted entity or all entities near a targeted empty location. | Vector/gravity manipulation. | Extreme knockback, void kills, boss/PvP denial. |
| Borrowed Authority | Public docs frame it as destructive temporary godlike authority and warn against use near bases. | Forbidden overdrive. | Too vague and power-centric to port directly; requires complete original redesign or removal. |
| Cup of Heaven | Constructs an external polygon and internal nodes; node counts determine stacked debuffs, and all living things in polygon are affected. | Geometric grand curse. | Area graph cost, mass PvP grief, arbitrary entity coverage and visual/network scale. |

## Gaze / perception mechanics

| Reference mechanic | Public behavior | Useful fantasy | Reference problems / Black Arcana concern |
| --- | --- | --- | --- |
| Binding gaze | Immobilizes facing targets while caster looks near them; victims can look away. | Reciprocal eye-contact curse. | Hard crowd-control, latency and accessibility/PvP abuse. |
| Minor clairvoyance | Predicts movement of some entities. | Foresight. | Networking/AI edge cases and limited unique value. |
| Black Flame | Creates rapidly spreading black fire that withers entities and can be quenched by water/rain. | Iconic forbidden soul-fire. | Unbounded propagation and base destruction are unacceptable defaults. |
| Death Collection | Observing deaths accumulates fractional/full souls; full souls prevent caster death. | Mortal ledger / soul anchors. | Automated mob-farm resurrection stockpiles and near-immortality. |
| Reversion | Cleanses effects and disables several special mob immunities/behaviors. | Nullification/reversion gaze. | Hardcoded bypass of other mods' invariants and boss mechanics is unsafe. |
| Fay Sight | Reveals reference-specific Fae and Leylines. | Spirit sight. | Depends on reference-specific world ecology we do not intend to clone. |
| Insight | Reveals inventories/effects/held-item information for blocks/entities. | Occult appraisal. | Player/container privacy and server information leakage. |

## Familiars

| Reference mechanic | Public behavior | Useful fantasy | Reference problems / overlap |
| --- | --- | --- | --- |
| Summon Familiar | Persistent talking/wandering familiar that reports observations. | Bound occult companion. | Ars already has a mature familiar system; avoid duplicate generic companion framework. |
| Recall Familiar | Returns familiar to caster. | Companion utility. | Should belong to whichever host owns the companion. |
| Familiar Exchange | Swaps caster/familiar locations. | Liminal familiar bond. | Valuable only if Black Arcana has a distinct bound-shade companion. |
| Shared Vision | Views what another entity/player sees. | Borrowed sight. | Privacy and arbitrary-player surveillance; safer if limited to owned familiar/marked minion. |
| Familiar's Garden | Moving area around familiar causes friendliness/non-hostility. | Pact sanctuary. | AI suppression can trivialize combat and cause expensive repeated path recalculation. |

## Exchange / contracts

| Reference mechanic | Public behavior | Useful fantasy | Reference problems / Black Arcana concern |
| --- | --- | --- | --- |
| Damage Exchange | Converts incoming damage into mana. | Blood-for-power economy. | Passive resource-positive loop; can be automated and combined with regeneration. |
| Chronal Exchange | Generates mana for half a day and drains for the other half based on placement time. | Time-bound bargain. | Exists only to feed a separate mana economy Black Arcana is rejecting. |
| Durability Exchange | Damages tools, including tools from a chest, to generate mana. | Sacrificial material conversion. | Cross-mod durability/resource arbitrage; automation exploit surface. |
| Catalyst Exchange | Randomly converts catalyst powders to other catalysts. | Occult transmutation. | Reference-specific catalyst economy does not exist in Black Arcana. |
| Alchemical Exchange | Once per day transforms natural blocks in a 5x5x5 area into peer materials. | Slow environmental transmutation. | Overlaps Ars/alchemy mods; unattended world mutation. |
| Contract | Nearby participants form a contract that exempts them from some negative boundaries/binding. | Covenants and ward permissions. | Strong Black Arcana identity if generalized as explicit permission/relationship state. |
| Immunity Exchange | Repeated same damage type becomes harmless while a changed damage type deals double. | Adaptive bargain. | Potential immunity chains and ambiguous modded damage-source grouping. |
| Retribution | Swaps caster/target health percentage with cost scaling to health moved. | Equilibrium/blood debt. | Boss health cheese and lethal PvP swing without eligibility/caps. |

## Supporting systems

| Reference system | Public behavior | Black Arcana disposition signal |
| --- | --- | --- |
| Mana HUD / growth | Persistent numeric mana HUD; max increases with cumulative mana use. | Reject. Black Arcana uses host resources and bounded progression. |
| Blood circle + three catalysts | Universal construction ritual for most spells. | Reject as universal UX; preserve blood/material preparation only where ritual meaning justifies it. |
| Mystic Code | Item stores/cycles three scroll stacks and casts selected scroll. | Replace with direct loadouts/radial selection; books/staves/weapons optional. |
| Fae/Leylines | Fae world ecology near ley lines; ley proximity boosts mana regeneration. | Drop as a cloned subsystem; spirit perception may integrate with Malum/Eidolon instead. |
| Fae Essence ownership/automation | Changes circle ownership/automation behavior. | Fold useful permission semantics into Black Arcana covenants and host automation rules, not a copied resource. |
| Mana Circuits | Owner-bound blocks store and supply the reference mana resource. | Drop. Host resource systems own storage; Black Arcana must not create another energy network. |
| Decorative magic-circle projector | Configurable decorative circles; public docs also describe loading images from URLs. | Defer an original sigil projector; never require remote URL rendering as a gameplay feature. |

## Clean-room boundary

The inventory above is sufficient for Stage 01 classification. Later implementation must use Black Arcana-owned names/specifications and acceptance tests. No implementation task may require looking at Mahou Tsukai code or assets.
