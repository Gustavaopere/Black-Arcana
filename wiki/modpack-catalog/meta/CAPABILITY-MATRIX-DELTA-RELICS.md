# Capability Matrix Delta — Relics 0.12.8

Status: `✅ EXACT ARTIFACT / 39 BASE ABILITIES + 2 DISTINCT SYNERGIES / 41 COUNTED_EXACT POWERS / RUNTIME FAIL-CLOSED`

| Relics capability | Provider-native meaning | Black Arcana consequence |
|---|---|---|
| 39 base abilities | owner-scoped provider powers with Relics state/progression | do not duplicate identity/state without explicit semantic distinction |
| 2 synergies | first-class owner-scoped `SynergyTemplate` powers | treat as separate provider-owned capabilities; do not collapse by shared local id alone |
| active powers | examples include blink/rewind/stable/retaliation/sacrifice surfaces | preserve provider activation/cooldown/buffer semantics |
| passive/reactive abilities | e.g. regeneration, neutrality, slots, camouflage | do not reinterpret provider passives as Black Arcana casts |
| ability/synergy modes | provider state such as toggle/cyclical selections | mode is not a new semantic identity |
| rank modifiers | provider progression mutates existing ability/synergy | rank unlocks do not create new identities by default |
| target configuration | 0.12.8 per-relic target controls | Black Arcana targeting must not override provider target settlement |
| FTB Teams integration | team context participates in targeting | preserve provider/team ownership |
| relic XP/ranks | independent provider progression | Black Arcana/RPG Skill Tree must not double-award or replace it |
| cooldowns/buffers | provider-owned action timing/resources | do not create parallel cooldown/charge authority |
| Curios lifecycle | equip state drives provider availability | exactly-once equip/unequip handling remains runtime QA |
| Reliquified addons | addon-owned relic content consuming Relics framework | count addon identities under their own dossiers, not under base Relics |

## Exact semantic boundary

Exact physical/publisher 0.12.8 artifact:

- base relics: **20**;
- base abilities: **39**;
- distinct synergies: **2**;
- total counted provider powers: **41**.

Modes/rank modifiers/item identities do not increase the semantic count.

Semantic contribution:

**+41 `COUNTED_EXACT`**

## Runtime boundary

Catalog closure is independent of assembled-pack QA. Config, targeting, persistence, Curios lifecycle, FTB Teams, addons, restart/death/dimension behavior and performance remain fail-closed until directly tested.
