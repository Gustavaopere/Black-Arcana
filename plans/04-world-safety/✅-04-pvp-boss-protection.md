# 04.04 — PvP, Boss & Protection Semantics

## Scope
Mind/control effects, displacement, damage replication, execution, resurrection denial and domain capture.

## Requirements
- Respect server PvP setting and allied-team rules where relevant.
- Bosses receive explicit resistance/caps rather than accidental immunity or trivialization.
- Teleport/control effects define safe fallback for protected/invalid destinations.
- Provide extension point for claim/protection integrations later without embedding a specific claim mod in core.

## Acceptance
GameTests cover players, allies, bosses, invulnerable entities and protected/invalid destinations.
