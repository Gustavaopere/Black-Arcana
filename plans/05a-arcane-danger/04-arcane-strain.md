# 05A.04 — Arcane Strain

## Objective
Add a short-/medium-term load state that makes repeated dangerous casting progressively riskier without relying only on cooldowns.

## Semantics
Arcane Strain represents immediate accumulated stress from channeling dangerous power. It is distinct from persistent Corruption.

Profiles may add:
- base strain at successful cast commitment;
- damage-linked strain;
- channel-duration strain;
- minimum strain that cannot be resisted/avoided;
- bounded effect of current strain on future preflight/backlash/corruption.

## State and recovery
Use bounded per-player strain units plus recovery metadata. Recovery should be lazy/event-driven from server time where possible:
- query/cast computes effective decayed strain from last-update tick;
- explicit rest/ritual/buff hooks may accelerate recovery;
- relog/restart must not instantly cleanse strain;
- no global scan over every player every tick is required.

Persist enough state in `BlackArcanaSavedData` to reconstruct strain deterministically after restart.

## Interaction with casting
Preflight exposes current/effective strain and predicted post-cast strain. Profiles may use strain to:
- raise backlash multiplier under high load;
- raise corruption acquisition;
- impose a hard gate for selected catastrophic mechanics;
- degrade cast stability through later content hooks.

Strain is not a second mana pool and should not have a permanent HUD bar by default.

## RED
Tests:
- strain increases deterministically after configured casts;
- recovery is monotonic and bounded;
- no negative strain or overflow;
- logout/restart does not cleanse it;
- current strain affects preflight only through profile-declared rules;
- multiple casts in the same tick are deterministic;
- rituals/buffs can contribute recovery modifiers through explicit providers/hooks;
- zero-strain profiles do not create state churn.

## GREEN
Implement bounded state, lazy decay/recovery service, persistence snapshot and profile-facing calculation hooks.

## REFACTOR
Keep recovery math pure and unit-testable. Minecraft time/persistence adapters remain narrow.

## Acceptance
Repeated forbidden casting can become increasingly unsafe even when cooldown and mana permit it, while normal/non-straining spells remain unaffected.
