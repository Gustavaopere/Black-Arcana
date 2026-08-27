# 00.04 — Config & Data Contracts

## Objective
Separate server gameplay authority from client presentation and make content tunable without unsafe ad-hoc config reads.

## Work
- Define server/common/client config ownership.
- Define data-driven spell metadata schema and version field.
- Decide JSON/codec/datapack boundaries versus compiled execution logic.
- Define config sync/handshake rules for multiplayer.
- Establish migration behavior for renamed/removed spell ids.
- Define validation diagnostics for malformed data.

## Acceptance
Malformed definitions fail with clear diagnostics; server values override client gameplay settings; old persisted ids can be migrated or safely ignored; client-only preferences never change server outcomes.
