# 06.07 — Curios Integration

## Objective
Make Curios a first-class optional source of arcane preparation without making Black Arcana require Curios or scanning Curios inventories continuously.

## Baseline
Installed-first pack baseline: Curios NeoForge `9.5.1+1.21.1`.

Integration must remain optional and isolated behind Black Arcana-owned interfaces. Dedicated server without Curios must load Black Arcana normally.

## Snapshot model
Curios are queried only when a resistance/preflight snapshot is needed, normally at cast preflight/commit. Do not iterate every player's Curios every tick.

The Curios adapter translates equipped stacks into the same resistance/source contracts used by armor and external providers. The hazard core never depends on Curios classes.

## Item identity
Important Curios should have distinct mechanical identity rather than a flat family of interchangeable resistance bonuses. Candidate roles include:
- Arcane Resistance focused ring/ward;
- Corruption-focused relic;
- strain buffering/recovery artifact;
- affinity-specific containment;
- emergency lethal-backlash protection with charge/break/cooldown semantics.

Final content names/values are deferred to equipment/content balance work.

## Optional-provider rules
- Curios absent -> Curios contribution is zero, no crash and no spell becomes free/unrestricted.
- Curios API mismatch -> adapter marks itself unavailable/incompatible with diagnostics.
- duplicate/invalid slot enumeration cannot double-count a stack.
- snapshot uses actual equipped state on the server.

## RED
Tests:
- Curio contribution appears in resistance snapshot;
- Curios absent still permits standalone Black Arcana operation;
- post-cast Curio swap does not change committed snapshot;
- same stack cannot be counted twice through duplicate slot traversal;
- depleted/broken Curio contributes according to its explicit state;
- emergency Curio consumes exactly once;
- dedicated-server smoke succeeds with Curios absent;
- representative profile succeeds with Curios `9.5.1+1.21.1` installed.

## GREEN
Implement optional Curios adapter, snapshot resolver and at least one synthetic/test containment definition. Do not add broad item content until the provider path is proven.

## REFACTOR
Use the public hazard provider API internally as well, so Curios is one provider among many rather than a special branch in the cast engine.

## Acceptance
A Curio can materially alter preflight/backlash through a server snapshot, while Black Arcana remains fully functional without Curios.
