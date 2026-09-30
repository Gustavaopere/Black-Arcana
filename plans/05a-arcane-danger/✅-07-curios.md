# 05A.07 — Curios Integration

## Objective
Make Curios a first-class optional source of arcane preparation without making Black Arcana require Curios or scanning Curios inventories continuously.

## Baseline
Installed-first pack baseline: Curios NeoForge `9.5.1+1.21.1`.

Integration remains optional and isolated behind Black Arcana-owned interfaces. Dedicated server without Curios must load Black Arcana normally.

## Snapshot model
Curios are queried only when a resistance/preflight snapshot is needed, normally at cast preflight/commit. Do not iterate every player's Curios every tick. The adapter translates equipped stacks into the same provider contracts used by armor/external integrations; hazard core never depends on Curios classes.

## Item identity
Important Curios should have distinct roles: Arcane Resistance, Corruption protection, strain buffering/recovery, affinity-specific containment or exactly-once emergency lethal-backlash protection.

## Optional-provider rules
Curios absent contributes zero without disabling Black Arcana; API mismatch is diagnosed as unavailable/incompatible; duplicate slot enumeration cannot double-count; snapshots use actual server-equipped state.

## RED
Tests cover provider contribution, missing Curios, post-cast swap immutability, duplicate traversal, depleted items, exactly-once emergency consumption, dedicated-server absence and the installed `9.5.1+1.21.1` profile.

## GREEN
Implement optional Curios adapter, snapshot resolver and at least one synthetic/test containment definition. Do not add broad item content until the provider path is proven.

## REFACTOR
Use the public hazard provider API internally as well, so Curios is one provider among many rather than a special branch in the cast engine.

## Acceptance
A Curio can materially alter preflight/backlash through a server snapshot while Black Arcana remains fully functional without Curios.
