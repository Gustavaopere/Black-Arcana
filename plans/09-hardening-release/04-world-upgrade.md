# 09.04 — World & Player-data Upgrade

## Objective
Ensure renames/removals/version changes do not corrupt worlds or strand players.

## Scope
Spell ids, loadouts, unlocks, cooldowns, soul anchors, active temporary effects, ritual state and domain recovery markers.

## Requirements
Version persisted schemas; migrate when safe, discard/recover conservatively otherwise; never crash a world because optional content disappeared.

## Acceptance
Fixture worlds/player data from prior schema versions load with documented results.
