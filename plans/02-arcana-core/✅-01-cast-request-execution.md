# 02.01 — Cast Request & Execution

## Pipeline
`request → identity/loadout validation → progression gate → target validation → world-policy preflight → resource reservation → execution → commit/refund → cooldown → result`.

## Requirements
- Immutable server-side cast context.
- Unique cast id for deduplication/replay protection where needed.
- Structured denial reasons for UI.
- No client authority over damage, costs or target coordinates beyond bounded intent.
- Hooks for charge/channel spells without duplicating execution semantics.

## Tests
Ordering, rollback/refund on failure, duplicate request rejection and denial reason stability.
