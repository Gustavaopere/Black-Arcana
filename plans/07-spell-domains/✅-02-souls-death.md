# 07.02 — Souls & Death

## Candidate mechanics
Soul harvesting, death collection, limited soul anchors/resurrection charges, spirit sight and death-powered effects.

## Balance
No infinite stored lives. Charges have hard cap, expensive replenishment and clear death semantics. Soul rewards cannot be farmed recursively from summoned/invalid entities unless explicitly allowed.

## Integration
Malum is preferred for spirit economy; Eidolon for occult unlocks; core owns resurrection safety/persistence.

Provider-native boundaries are mandatory:

- `Malum 1.8.2` remains authority for real spirit resources. Black Arcana does not synthesize Malum spirit value from generic `LivingDeathEvent`s.
- `MinecraftSoulAnchorRuntime.creditDeath(...)` is an explicit server-authoritative seam for a validated provider-backed or deliberately configured fallback credit. Without such a producer, harvesting remains fail-closed rather than creating a parallel soul economy.
- the current Malum bridge can query/consume/refund real `malum:<affinity>_spirit` shards and Spirit Sight can expose supported registry-backed Malum traces, but no verified Malum 1.8.2 callback currently proves how much provider-owned spirit a particular death generated.
- Eidolon: Repraised `0.5.0.2` remains the preferred occult presentation/unlock provider when a safe identity-bearing hook exists. Its current public custom-ritual callback does not expose the caster/player identity, so the existing anchor-attunement ritual must not be silently promoted into a player-specific Soul Anchor unlock. That player gate remains fail-closed pending a safe hook.
- no generic bonus, synthetic spirit, free anchor, arbitrary death reward or inferred player ownership is used as fallback.

## Implemented contracts

### Mortal Ledger / Soul Anchor

- bounded `SoulAnchorLedger` with hard anchor ceiling, bounded recent-death identity history, anti-farm eligibility input, recovery lockout and exactly-once death settlement;
- deterministic `SoulDeathTransactionIds` keeps duplicate callbacks for the same player/server tick on the same transaction identity;
- `SoulAnchorSavedData` persists ledger snapshots, anchors, recovery state and recent death IDs with bounded restore and per-record malformed-data containment;
- `MinecraftSoulAnchorRuntime` owns server-side configuration, persistence settlement and the `LivingDeathEvent` death-prevention bridge;
- a death is canceled only after one existing anchor is atomically consumed; health restoration is finite, positive and capped by current max health;
- no automatic death-to-spirit producer is installed without a provider-backed causal event.

### Spirit Sight

- `SpiritSightPolicy` is whitelist/fail-closed and does not authorize hidden-player or private-container disclosure;
- `SpiritTraceProvider` validates bounded provider IDs, dimension IDs, finite coordinates/radius and provider-backed traces;
- `MinecraftSpiritSightRuntime` owns bounded providers/sessions, radius/category/privacy filtering, expiry and provider-disappearance fail-closed behavior;
- `MalumSpiritTraceProvider` recognizes only stable supported entity registry IDs and marks `malum:soul_tag_entity` private because host state carries target identity;
- `MalumServerIntegrationBootstrap` registers the provider only when the supported Malum integration is available; otherwise the visibility path remains unavailable.

## Automated evidence

07.02 was rebuilt on fresh canonical `main` ancestry in PR #47 with explicit RED→GREEN cycles.

- Mortal Ledger RED: workflow `33664955018`; GREEN: `33665443159`.
- Souls domain specs RED: `33665811923`; GREEN: `33666136372`.
- Spirit Sight policy GREEN: `33668083636` after the test-only RED.
- Spirit provider contract GREEN: `33668752028` after the test-only RED.
- Spirit Sight runtime: the first run exposed one unrelated non-reproducible Equilibrium GameTest failure while all four new Spirit Sight GameTests passed; rerun on the exact same head `94c3da5d753f4bad3b4c27863bc3b66bba9dcc86` passed the full pipeline with all 38 GameTests and dedicated-server smoke (`33669496953`). No Equilibrium production code was changed for that flake.
- Soul Anchor runtime RED: workflow `33978656892` ran 40 GameTests and failed only the two new Soul Anchor tests because `MinecraftSoulAnchorRuntime` was absent.
- Soul Anchor runtime GREEN: workflow `33980621225` on `f2962ef078adaef4a581dae537e18a8d9aa68a23` passed JUnit, diff sanity, NeoForge build, JAR inspection, all 40 required GameTests and dedicated-server smoke.

Automated isolated CI does not claim real-modpack/manual acceptance for optional host behavior. Provider-specific behavior requiring the installed full modpack remains in the deferred final-validation campaign under D031.

## Acceptance
Death/relog/restart tests prove exact charge accounting and no duplication. Spirit Sight tests prove bounded visibility, privacy denial, provider failure/disappearance fail-closed behavior and session expiry.

Canonical merge: PR #47 / `998186beed3522a0821a7dbb911f5e31cd6a9e1d`. Exact-SHA post-merge workflow `33981437469` passed the complete automated pipeline and published the canonical QA artifact. Final real-modpack/provider/manual acceptance remains deferred under D031 and is not inferred from automated CI.
