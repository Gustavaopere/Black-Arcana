# Black Arcana reference classification matrix

Status: PREPARATORY — not frozen until Stage 00 merges and Stage 01 is reviewed on its canonical branch.

## Legend

- `KEEP`: core fantasy is distinctive enough to preserve, but implementation/name/assets remain original.
- `REIMAGINE`: preserve the useful gameplay idea but materially change constraints, economy, UX and/or implementation.
- `MERGE`: do not create a standalone clone; fold the useful piece into a Black Arcana framework or an existing host-mod system.
- `DROP`: deliberately excluded.
- `DEFER`: potentially valuable, but not permitted for initial implementation.
- Progression: `T0` framework/support, `T1` initiate, `T2` adept, `T3` master, `T4` forbidden/grand.
- World policy uses Black Arcana modes `OFF`, `COSMETIC`, `TEMPORARY`, `LIMITED`, `FULL`; `FULL` is never a default preset.

## Boundaries / wards

| Reference | Disposition | Black Arcana target | Domain | Invocation | Preferred host | Cost model | World | Risk | Tier | Rationale |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Alarm Boundary | MERGE | Vigil Ward module | Dominion | ritual/ward | Eidolon or core | ritual material + upkeep optional | OFF | Low | T1 | Useful ward primitive, not enough value as its own spell. |
| Enclosure Boundary | DROP | — | — | — | — | — | — | High | — | Duplicates building and creates unnecessary terrain mutation. |
| Tangible Boundary | REIMAGINE | Exclusion Ward | Dominion | ritual/ward | Eidolon + core safety | material + bounded duration/upkeep | TEMPORARY | High | T2 | Keep owner/permission fantasy; no permanent invisible prison. |
| Displacement Boundary | REIMAGINE | Threshold Gate (entities only) | Liminal | ritual/ward | Ars/core | host mana/source + cooldown/upkeep | OFF | High | T2 | Drop block movement entirely; retain bounded threshold teleport. |
| Gravity Boundary | REIMAGINE | Gravitic Ward | Dominion | ritual/ward | Iron's/core | mana + duration budget | OFF | High | T2 | Preserve suppression field with boss/PvP resistance and force caps. |
| Drain Life Boundary | REIMAGINE | Sanguine Harvest | Sanguine | ritual/ward | Eidolon/Malum composite | ritual material + life/soul budget | OFF | Critical | T3 | No health→food→mana positive feedback; bounded targets and yield. |

## Displacement

| Reference | Disposition | Black Arcana target | Domain | Invocation | Preferred host | Cost model | World | Risk | Tier | Rationale |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Ascension | MERGE | Use Ars Blink/Warp capability | Liminal | existing host | Ars | Ars-owned | OFF | Low | — | Generic teleport already exists in the pack. |
| Protective Displacement | REIMAGINE | Veilstep Reflex | Liminal | passive/reaction | Iron's/Ars | mana + charge + internal cooldown | OFF | High | T2 | Bounded evade, not continuous pseudo-invulnerability. |
| Projectile Displacement | REIMAGINE | Anchor Recall | Liminal | direct cast | Ars or Iron's | mana + cooldown | OFF | Medium | T2 | Teleport only to owned/marked projectile with safe-position validation. |
| Ordered Displacement | MERGE | Waygate ordering extension only if needed | Liminal | existing host/ritual | Ars | Ars-owned | OFF | Medium | — | Warp portals already solve generic route travel. |
| Equivalent Displacement | REIMAGINE | Reciprocal Transposition | Liminal | paired ritual | Ars + core | source/mana + pair charge | OFF | Critical | T3 | Entity/item swap only under explicit eligibility; never block/tile swap. |
| Mental Displacement | REIMAGINE | Astral Severance | Noetic/Liminal | direct cast | core + Eidolon flavor | mana + vulnerability + timeout | OFF | High | T3 | Body remains vulnerable; hard radius, logout/death restoration. |
| Scrying | REIMAGINE | Namescry | Noetic | ritual/direct channel | Eidolon/core | focus item + mana + channel | OFF | Critical | T3 | Same-dimension/loaded-target default; server privacy/PvP policy. |

## Projection / armaments

| Reference | Disposition | Black Arcana target | Domain | Invocation | Preferred host | Cost model | World | Risk | Tier | Rationale |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Strengthening | REIMAGINE | Ephemeral Tempering | Eidetic | direct/weapon cast | Iron's/Malum | mana/spirit + cooldown | OFF | High | T2 | Temporary capped modifiers; no permanent mining-tier escalation. |
| Projection copy | REIMAGINE | Echo Armament | Eidetic | direct cast | Iron's/core | mana + memory slot | OFF | Critical | T2 | Spectral non-persistent facsimile from sanitized combat profile; no arbitrary NBT clone. |
| Proximity-projection weapon | REIMAGINE | Rift Blades | Eidetic/Liminal | direct cast | Iron's | mana + cooldown | OFF | High | T2 | Original spectral weapon with bounded gap-close, not reference presentation. |
| Bow of weapon projectiles | MERGE | Spectral Arsenal firing mode | Eidetic | direct cast | Iron's | mana + arsenal budget | OFF | High | T3 | One arsenal framework instead of multiple item-copy systems. |
| Personal reality arena | REIMAGINE | Inner Dominion | Dominion | forbidden cast | core | composite + long cooldown + duration | TEMPORARY | Critical | T4 | Temporary return-safe domain; no death-based escape or persistent loot trap. |
| Power Consolidation | REIMAGINE | Oathforged Ascension | Eidetic/Sepulchral | grand ritual | Eidolon/Malum/core | item sacrifice + spirit/material budget | OFF | Critical | T4 | Finite point budget/hard cap/diminishing returns; no recursive infinite damage. |
| Treasury Projection | REIMAGINE | Spectral Arsenal | Eidetic | direct/channel | Iron's/core | mana + per-projectile budget | OFF | Critical | T3 | Sanitized weapon profiles become ephemeral projectiles; no ender-storage duplication. |

## Mystic / control

| Reference | Disposition | Black Arcana target | Domain | Invocation | Preferred host | Cost model | World | Risk | Tier | Rationale |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Damage Replication | REIMAGINE | Sympathetic Wound | Sanguine | curse/channel | Malum/Eidolon | health/spirit + link duration | OFF | Critical | T3 | Percentage/capped mirrored damage; no recursive reflect or blanket potion replication. |
| Large shield | REIMAGINE | Hexward Aegis | Dominion | direct/channel | Iron's | mana + integrity | OFF | Medium | T2 | Finite-integrity ward with explicit projectile/explosion behavior. |
| Explosive condensation | DEFER | Ruinous Convergence | Cinder | charged cast | Iron's/core | large mana + cooldown | LIMITED | Critical | T4 | Generic explosion is redundant unless safety/charge gameplay proves distinctive. |
| Spatial disorientation | REIMAGINE | Vector Reversal | Liminal | direct cast | Iron's | mana + cooldown | OFF | High | T2 | Force/velocity caps, fall protection window, boss resistance. |
| Borrowed Authority | DEFER | Usurped Mandate | Dominion | grand/forbidden | core | composite + severe lockout | LIMITED | Critical | T4 | Reference is too vague/power-centric; requires an entirely original design later. |
| Cup of Heaven | REIMAGINE | Malison Constellation | Dominion/Sanguine | grand ritual | Eidolon + core | node materials + activation sacrifice | OFF | Critical | T4 | Keep geometric curse language; bounded node graph/area and PvP policy. |

## Gaze / perception

| Reference | Disposition | Black Arcana target | Domain | Invocation | Preferred host | Cost model | World | Risk | Tier | Rationale |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Binding gaze | REIMAGINE | Gaze of Stillness | Noetic | channeled gaze | Iron's/core | mana per tick + cooldown | OFF | Critical | T2 | Reciprocal facing/LoS with break conditions and CC diminishing returns. |
| Minor clairvoyance | DEFER | Noetic Foresight | Noetic | passive/channel | core | focus + cooldown | OFF | Medium | T3 | Low priority and prediction/network complexity. |
| Black Flame | KEEP | Black Pyre | Cinder | direct cast | Iron's + Malum flavor/core safety | mana/spirit composite | TEMPORARY | Critical | T3 | Flagship mechanic, but spread/destruction is budgeted and temporary by default. |
| Death Collection | REIMAGINE | Mortal Ledger / Soul Anchor | Sepulchral | sustained/passive | Malum + core | collected eligible spirits + recharge rules | OFF | Critical | T4 | Max resurrection charges, anti-farm eligibility, recovery lockout. |
| Reversion | REIMAGINE | Nullifying Gaze | Noetic | gaze/channel | Iron's | mana + cooldown | OFF | Critical | Tag/API-driven dispel only; never hard-disable arbitrary mod/boss invariants. |
| Fay Sight | MERGE | Spirit Sight | Sepulchral/Noetic | passive/toggle | Malum/Eidolon | host resource or none | OFF | Low | T1 | Reinterpret as host spirit visibility; do not clone Fae/Leylines. |
| Insight | REIMAGINE | Occult Appraisal | Noetic | gaze/channel | core | mana + channel | OFF | High | T2 | Effects/held items okay; inventories require server privacy permission. |

## Familiars

| Reference | Disposition | Black Arcana target | Domain | Invocation | Preferred host | Cost model | World | Risk | Tier | Rationale |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Summon Familiar | MERGE | Use Ars familiar ownership | Noetic | existing host | Ars | Ars-owned | OFF | Medium | — | Do not duplicate a mature generic familiar framework. |
| Recall Familiar | MERGE | Host familiar recall/extension | Noetic/Liminal | existing host | Ars | Ars-owned | OFF | Low | — | Belongs to host companion system. |
| Familiar Exchange | MERGE | Familiar Transposition extension | Liminal | direct cast | Ars adapter | mana + cooldown | OFF | Medium | T2 | Add only if stable API supports owned-familiar target resolution. |
| Shared Vision | REIMAGINE | Borrowed Sight | Noetic | channel | Ars adapter/core | mana + range | OFF | High | T2 | Restrict default target to owned familiar/consenting bonded entity, not arbitrary players. |
| Familiar's Garden | REIMAGINE | Pact Sanctuary | Dominion/Noetic | familiar aura | Ars adapter/core | upkeep + radius budget | OFF | Critical | T3 | Pacification whitelist, boss exclusions and throttled AI updates. |

## Exchange / contracts

| Reference | Disposition | Black Arcana target | Domain | Invocation | Preferred host | Cost model | World | Risk | Tier | Rationale |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Damage→mana | MERGE | Blood Price cost mode | Sanguine | cost provider | core | health substitutes a bounded fraction of another cost | OFF | Critical | T2 | No passive damage-to-resource generation; only explicit inefficient cast-time substitution. |
| Chronal Exchange | DROP | — | — | — | — | — | — | Medium | — | Exists to feed rejected separate mana economy. |
| Durability Exchange | DROP | — | — | — | — | — | — | Critical | — | Cross-mod durability arbitrage/automation surface outweighs value. |
| Catalyst Exchange | DROP | — | — | — | — | — | — | Low | — | Reference-specific catalyst economy absent. |
| Alchemical Exchange | MERGE | Use Ars/pack transmutation | — | existing host | Ars/other pack mods | host-owned | host-owned | Medium | — | Avoid redundant unattended block conversion. |
| Contract | KEEP | Covenant | Dominion | ritual/state | core + Eidolon presentation | ritual material + consent | OFF | High | T1/T2 | Becomes general permission/relationship primitive for wards, scrying and domains. |
| Immunity Exchange | REIMAGINE | Law of Recurrence | Sanguine/Dominion | defensive curse | Iron's/core | mana + timed state | OFF | Critical | T3 | Resistance ceiling/floor; never full permanent immunity; explicit damage-family mapping. |
| Retribution | REIMAGINE | Equilibrium Rite | Sanguine | forbidden cast/ritual | Iron's/Eidolon/core | health + mana/material + long cooldown | OFF | Critical | T4 | Bounded eligible-health transfer; bosses/PvP use separate caps or disabled default. |

## Supporting systems

| Reference | Disposition | Black Arcana target | Reason |
| --- | --- | --- | --- |
| Persistent mana HUD / spend-to-grow max mana | DROP | Host-resource adapters + RPG progression | Removes infinite grind scaling and duplicate HUD. |
| Universal blood circle + catalysts | DROP | Ritual framework only where preparation matters | Removes repetitive busywork from routine combat casting. |
| Mystic Code scroll holder | DROP | Direct loadouts/radial UX + optional host books/weapons | Removes mandatory item container. |
| Fae + Leylines | DROP | Optional host spirit ecology | Avoids cloning world ecology/worldgen/resource loop. |
| Fae ownership automation | MERGE | Covenant/permission framework | Keep permissions semantics, not the reference resource. |
| Mana Circuits | DROP | Host resource systems | No second energy network. |
| Decorative projector | DEFER | Sigil Projector | Cosmetic idea can return later with original art and local assets only. |

## Initial implementation scope signal

Initial `T1–T3` content may be selected only from non-`DROP`/non-`DEFER` rows. `T4` mechanics remain gated behind Stage 08 balance budgets even if their Stage 07 implementation is technically possible. `MERGE` rows do not authorize new standalone content unless the named host lacks the needed capability after Stage 03 verification.
