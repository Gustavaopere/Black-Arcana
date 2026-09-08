# Capability Matrix Delta — Ars Zero 2.0.2

Phase 2AE records Ars Zero as an Ars-native glyph/cast-device/world-capability provider. This delta improves deduplication evidence only; it does not authorize Phase 3 implementation.

| Capability family | Ars Zero 2.0.2 evidence | Authority | Black Arcana disposition |
|---|---|---|---|
| Multiphase Begin/Tick/End casting | Spell Staff, Psion's Circlet, Multi-phase Turret | Ars Zero + Ars spell execution/resource state | `COVERED EXTERNALLY`; no second generic phase engine |
| Continuous/channelled casting | held-use Staff/Circlet + Beam repeated hit semantics | provider cast/resource lifecycle | observe only through real causal hook; no double debit |
| Temporal/contextual selection | Temporal Context + Select + Anchor | Ars Zero cast context | overlap; no implicit BA mark/context conversion |
| Forced movement/gravity | Push, Anchor, Remove Gravity | provider spell/effect state | overlap; preserve provider authority |
| Geometric/patterned resolution | Geometrize + provider geometry process | provider server geometry lifecycle + world/claim checks | overlap; never accept client geometry authority |
| Beam delivery | Beam | provider resolver + mana-per-hit semantics | external coverage; no duplicate hit loop/resource debit |
| Barrier/shield | Conjure Arcane Shield | provider entity/barrier durability lifecycle | external coverage; no mirrored shield ledger |
| Persistent elemental constructs | Conjure Voxel + seven variants | provider entity/world interaction lifecycle | external coverage; do not recreate entities through BA |
| Blight/environmental corruption-like effect | Conjure Blight + Blight world content | Ars Zero Blight/worldgen authority | **not equivalent to BA Corruption**; no implicit conversion |
| Mana concentration / Source charging | Convergence | Ars/Ars Zero resource authority | never second-credit Source or substitute BA resource |
| Protected block mutation/restoration | Conjure Blight + Temporal Anchor release hardening | provider claim/world-bound authority | future adapters must preserve provider protection and BA WorldEffectPolicy where BA acts |
| Static staff progression/loot | seven production static staffs + Necropolis Lich | provider item/encounter/loot authority | not BA progression unless an explicit deduplicated progression hook is designed |
| Client packet authority | 2.0.2 server reconstruction/ownership validation | server/provider | confirms fail-closed rule: client intent never gameplay authority |

## Gap decision impact

The following generic candidate ideas cannot be called Black Arcana gaps merely because they are desirable fantasies:

- generic multi-stage spell devices;
- generic continuous Ars casting;
- generic geometry spell form;
- generic gravity removal/push;
- generic beam form;
- generic temporary magic barrier;
- generic elemental mana voxel/construct;
- generic blight presentation.

A Black Arcana capability may still exist where its semantics are genuinely different and authority-safe, but it must state that delta explicitly. Black Arcana Corruption/Strain/Danger remain separate provider-owned channels.

## Fail-closed fields

No implementation decision may depend on unverified 2.0.2 registry IDs, exact cost formulas, config keys, API signatures or binary-only data until exact evidence is obtained.
