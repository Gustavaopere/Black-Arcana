# Capability Matrix Delta — Relics 0.12.8

Status: `PARTIAL / PROVIDER-OWNED RELIC ABILITY RUNTIME / 20 CURRENT-DOC BASE RELICS / FINAL ABILITY CARDINALITY PENDING`

| Relics capability | Provider-native meaning | Black Arcana consequence |
|---|---|---|
| relic abilities | named powers with provider-owned state/progression | do not duplicate identity/state without explicit deduplication |
| active RMB powers | examples include Teleportation, Sacrifice, Transgression, Stable and Retaliation | preserve provider activation/cooldown/buffer semantics |
| passive/reactive powers | examples include Camouflage, Damage Condensation and Seven Deadly Sins identities | do not reinterpret passive trigger as Black Arcana cast |
| ability modes | Enabled/Disabled, Full Moon/New Moon and similar provider state | mode is not a new spell identity |
| rank modifiers | provider level/rank progression mutates an existing ability | do not count rank unlocks as independent spells by default |
| target configuration | 0.12.8 per-relic target controls | Black Arcana targeting must not override provider target settlement |
| FTB Teams integration | team context participates in ability targeting | preserve provider/team ownership |
| relic XP | independent provider progression state | Black Arcana/RPG Skill Tree must not double-award or replace it |
| cooldowns/buffers | provider-owned action timing/resources | do not create parallel cooldown/charge authority |
| synergies | cross-relic combined behavior such as documented synergy surfaces | inventory separately; do not silently fold into base ability count |
| Curios lifecycle | equip state drives ability availability | exactly-once equip/unequip handling required |
| Reliquified addons | extend Relics with addon-owned relics | count addon identities under their own provider dossiers, not base Relics |

## Semantic boundary

Relics is a real powers provider, not merely cosmetic gear.

Current evidence confirms discrete ability identities, but exact final 0.12.8 cardinality remains pending.

Therefore:

- base relic roster: **20**;
- semantic ability numerator contribution: **PENDING**;
- synergies: **not yet counted**;
- rank modifiers/modes: **not independent identities by default**.

## Runtime boundary

Remain fail-closed until exact assembled-pack evidence exists for:

- ability config parity;
- target/team filtering;
- cooldown/buffer persistence;
- Curios equip lifecycle;
- XP progression;
- death/relog/restart/dimension change;
- Sophisticated Backpacks;
- Reliquified addons;
- full-pack performance and exactly-once processing.
