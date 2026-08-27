# Server safety ceilings

Status: PREPARATORY. These are technical abuse/performance guardrails for the Black Arcana server-authoritative runtime. They are not final combat balance; Stage 08 may lower defaults or tighten them. Raising an absolute ceiling requires an explicit architecture/risk review.

## Semantics

- `default` is the initial conservative server-config value.
- `hard ceiling` is the maximum value accepted by config validation unless a later architectural decision deliberately changes it.
- A `hard floor` is used where safety requires a minimum cooldown/immunity interval.
- All counts are per owner/caster/session unless explicitly global.
- No setting may enable arbitrary chunk force-loading, arbitrary command execution, persistent projected items, or bypass `WorldEffectPolicy`.

## Global runtime budgets

| Guardrail | Default | Hard ceiling / floor | Rationale |
| --- | ---: | ---: | --- |
| Cast requests accepted per player per tick | 2 | 4 | Prevent packet/cast spam from becoming effect spam. |
| Entities processed by one ordinary cast | 32 | 128 | Bounds AoE work. |
| Entities inspected by one spatial query | 128 | 256 | Prevents pathological crowded-area scans. |
| Temporary Black Arcana entities per caster | 24 | 64 | Bounds projectiles, echoes and visual helpers. |
| Persistent owned constructs per player | 12 | 32 | Bounds wards, anchors and ritual state. |
| Generic same-dimension remote range | 64 blocks | 128 blocks | Avoids remote-world mechanics becoming chunk scanners. |
| Forced chunks created by Black Arcana | 0 | 0 | Absolute invariant. |

## Dominion and wards

| Guardrail | Default | Hard ceiling / floor |
| --- | ---: | ---: |
| Active ordinary wards per owner | 4 | 16 |
| Ordinary ward radius | 12 blocks | 32 blocks |
| Ordinary ward lifetime without explicit upkeep | 10 min | 60 min |
| Malison Constellation nodes | 8 | 16 |
| Malison polygon area | 4,096 blocks² | 16,384 blocks² |
| Malison entities affected per activation | 48 | 128 |
| Vigil notifications to one owner | 4 / 5 s | 10 / 5 s |
| Inner Dominion active sessions per caster | 1 | 1 |
| Inner Dominion participants | 8 | 16 |
| Inner Dominion arena radius | 32 blocks | 64 blocks |
| Inner Dominion duration | 1,200 ticks | 3,600 ticks |
| Nested Inner Dominion depth | 0 | 0 |

The Dominion runtime must journal participant origins before transfer and guarantee cleanup/return on expiry, death, logout, restart and abnormal termination. Domain sessions never become item-storage or duplication boundaries.

## Cinder / Black Pyre

| Guardrail | Default | Hard ceiling |
| --- | ---: | ---: |
| Spread radius | 8 blocks | 16 blocks |
| Simultaneously active pyre cells per cast | 256 | 1,024 |
| New propagation cells scheduled per tick | 16 | 64 |
| Cell lifetime | 300 ticks | 1,200 ticks |
| Permanent block mutation preset | disabled | policy-controlled only |

Propagation stops at unloaded chunks. Entity damage is independent of terrain mutation so `TEMPORARY`/safe world modes remain mechanically useful.

## Eidetic Arsenal / projections

| Guardrail | Default | Hard ceiling |
| --- | ---: | ---: |
| Stored sanitized weapon profiles | 16 | 64 |
| Active echoes/projected weapons | 12 | 48 |
| Spectral Arsenal projectiles created by one volley | 16 | 64 |
| Raw projected attack-damage contribution before Black Arcana scaling | 40 | 100 |
| Oathforged enhancement points on one item | 10 | 20 |

Projected profiles are value objects, not copied `ItemStack`s. They cannot retain arbitrary data components/NBT, capabilities, inventory contents, ownership tokens, UUID-bearing state, enchantments outside an explicit allow-list or executable callbacks. A projection can never be inserted into an inventory/container or serialized as a normal persistent item.

## Liminal movement

| Guardrail | Default | Hard ceiling / floor |
| --- | ---: | ---: |
| Threshold Gate entity throughput | 8 / s | 32 / s |
| Anchor Recall projectile age | 200 ticks | 600 ticks |
| Anchor Recall range | 48 blocks | 128 blocks |
| Reciprocal Transposition operations per pair | 4 / s | 16 / s |
| Vector Reversal resulting speed | 1.5 blocks/tick | 2.5 blocks/tick |

All endpoints must already be loaded naturally. Player displacement follows explicit PvP/consent policy and collision-safe destination validation.

## Noetic / information and control

| Guardrail | Default | Hard ceiling / floor |
| --- | ---: | ---: |
| Astral Severance radius | 64 blocks | 128 blocks |
| Namescry remote range | 64 blocks | 128 blocks |
| Gaze of Stillness continuous application | 60 ticks | 160 ticks |
| Gaze of Stillness player reapplication immunity | 80 ticks | hard floor 40 ticks |
| Pact Sanctuary radius | 12 blocks | 24 blocks |
| Pact Sanctuary entities processed per refresh | 48 | 128 |
| Pact Sanctuary refresh interval | 20 ticks | hard floor 5 ticks |

Namescry/Astral Severance never force-load chunks and expose only whitelisted information. Player scrying is disabled by default unless server policy plus consent/covenant rules permit it.

## Sanguine / Sepulchral

| Guardrail | Default | Hard ceiling / floor |
| --- | ---: | ---: |
| Sanguine Harvest entities processed per pulse | 24 | 64 |
| Blood Price fraction of a cast payable with health | 35% | 50% |
| Blood Price ordinary minimum remaining health | 4 HP | hard floor 1 HP |
| Sympathetic Wound mirror fraction | 25% | 50% |
| Sympathetic Wound mirrored damage per event | 10 HP | 40 HP |
| Sympathetic Wound lifetime mirrored budget | 40 HP | 200 HP |
| Soul Anchors stored | 2 | 5 |
| Mortal Ledger same-death-event anchor activations | 1 | 1 |
| Post-anchor recovery lockout | 600 ticks | hard floor 200 ticks |
| Equilibrium Rite transferable health per activation | 20 HP | 40 HP |

Soul Anchor accounting and consumption are atomic server transactions. A prevented death cannot simultaneously generate qualifying death credit or trigger another anchor in the same damage/death transaction.

## Boss and PvP policy

- Hostile player use of remote scrying, hard displacement, health exchange, Malison effects and prolonged crowd control defaults to disabled.
- Bosses/protected entities use explicit tags/adapters. Unknown bosses are treated conservatively rather than as ordinary mobs.
- Ordinary resistance mechanics cannot reach 100% immunity through Black Arcana alone.
- Damage reflection/shared-damage events carry a recursion marker and cannot recursively feed themselves.

## Configuration validation contract

1. Invalid numeric values fail validation or are clamped only where the behavior is explicitly documented; silent overflow is forbidden.
2. Server config is authoritative. Client config cannot raise limits or alter eligibility.
3. Every bounded runtime exposes counters/metrics sufficient for GameTests and later performance tests to assert ceilings.
4. Stage 08 owns final balance defaults, but must preserve these safety invariants unless a new decision is recorded in `plans/DECISIONS.md`.
5. Stage 09 must test at both default values and hard-ceiling values for cleanup, restart safety and bounded runtime behavior.
