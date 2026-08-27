# Configuration and data contract

Schema version: `1`.

## Ownership

- `SERVER`: authoritative gameplay values. These are the only configuration values allowed to change cast legality, damage, cost, cooldown, progression, targeting or world mutation on a multiplayer server.
- `COMMON`: installation/runtime compatibility defaults shared by environments. They may select adapters or implementation facilities but cannot override a connected server's gameplay outcome.
- `CLIENT`: presentation, accessibility, HUD and input preferences only. They never authorize gameplay.

## Spell data boundary

Data packs may own stable metadata such as spell id, translation key, icon id, tags, presentation ordering, tunable numeric values explicitly exposed by a compiled spell implementation, and schema version. Arbitrary executable behavior is not loaded from JSON. Server execution remains compiled and server-authoritative.

Malformed definitions are rejected with deterministic diagnostics. Unknown schema versions are rejected rather than guessed.

## Multiplayer

Gameplay-authoritative values originate on the server. A future handshake/sync payload will expose the server-approved effective values required by the client UI. Client preferences may hide/rearrange presentation but cannot alter those values.

## ID migration

Renamed IDs map old -> new through an explicit migration table. Removed IDs resolve to no spell with a reason instead of silently pointing at unrelated content. Persisted content must never infer a replacement by display name.
