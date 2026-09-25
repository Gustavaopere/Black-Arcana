# Capability Matrix Delta — Corail Tombstone 9.5.6

Status: `PARTIAL / PUBLISHER-BOUNDED MAGIC SYSTEM / SEMANTIC CARDINALITY PENDING`

This file records only Tombstone-specific overlap. It does not replace the global capability matrix.

| Tombstone capability | Provider-native meaning | Black Arcana consequence |
|---|---|---|
| Grave Souls | provider resource used for magical enchanting and related progression | do not duplicate or settle Tombstone Soul consumption inside Black Arcana |
| magic scrolls/tablets | provider magical item/action family | keep provider ownership; enumerate before any semantic deduplication |
| Ankh prayer | grave-adjacent provider prayer interaction | do not map generic Black Arcana prayer/ritual UX onto Tombstone without a verified boundary |
| enhanced prayers | Forgotten Knowledge unlock expands prayer behavior | preserve provider unlock/state and exact config |
| Ritual Flute | learned melody / correct-block rite support | do not create a second melody/rite state machine |
| Rite of Silent Bound | named forgotten-knowledge/rite surface tied to undead affinity | preserve provider state; exact action semantics remain unresolved |
| Knowledge of Death | provider progression/perk runtime | do not transfer ownership to Black Arcana or RPG Skill Tree without a real contract |
| 13 enchantments | equipment-driven magical modifiers | gear content; not separate spell identities |
| 24 effects | provider supernatural status states | status content; not separate spell identities |
| grave/death recovery | authoritative provider inventory/death lifecycle | Black Arcana magic must not double-process death/recovery |
| XP restoration | Tombstone death/recovery economy, with 9.5.6 overflow fix | never duplicate XP settlement |
| Create Aeronautics respawn compatibility | provider-specific vehicle respawn boundary introduced in 9.5.5 | treat as external runtime QA, not generic compatibility |

## Semantic boundary

The publisher confirms Tombstone has discrete magic-related action families, but the exact 9.5.6 cardinality is not publicly closed.

Therefore:

- enchantments: **+0 semantic actions**;
- effects: **+0 semantic actions**;
- Souls/Knowledge state: **+0 by themselves**;
- prayers/rites/scroll-tablet actions: **cardinality pending**.

Strict semantic delta: **PENDING**.

## Runtime boundary

Any integration remains fail-closed until the exact assembled pack proves:

- registry/config parity;
- action reachability;
- exactly-once Soul/resource settlement;
- prayer/rite persistence;
- grave/death lifecycle coexistence;
- multiplayer/protection behavior;
- vehicle respawn coexistence;
- restart/reload/migration behavior.
