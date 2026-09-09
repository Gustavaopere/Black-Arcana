# School, Progression and Equipment Bridge

## Evidence boundary

Physical provider: Ars 'n' Spells `3.3.2`.

Implementation facts on this page are pinned to the official NeoForge 1.21.1 `3.3.0` source baseline at `a9930223c96806e5d748ea69d02f9a32cab62de9`. Exact 3.3.2 internal parity remains `NÃO VERIFICADO`.

## School resolution authority

The 3.3.0 NeoForge baseline centralizes Ars-glyph school classification in the provider's `SchoolResolver` so school-sensitive subsystems do not independently guess different results.

The audited resolution chain is provider-owned and follows this priority:

1. explicit provider/datapack glyph mapping;
2. declared Ars `spellSchools` metadata;
3. a small registry-path heuristic only as fallback.

A glyph may declare multiple schools. The provider exposes both a deterministic single-school choice for systems that need one credited track and a multi-school result for scaling use cases.

This classification feeds provider concepts such as affinity, progression, scaling, cooldown categorization and UI. Black Arcana must not replace it with registry-name substring guesses.

## Addon-aware resolution

The 3.3.0 release line explicitly adds/validates school-resolution behavior for installed Ars-addon families including Ars Elemental and Ars Zero. Control-flow/forms/filters that do not define the payload school are intended to remain generic rather than stealing school attribution from the actual effect.

The physical pack contains Ars Elemental `0.7.10.1` and Ars Zero `2.0.2`, matching the optional test profiles declared by the NeoForge source baseline.

This does not authorize Black Arcana to hard-code provider addon glyph ids. School ownership remains an Ars 'n' Spells/provider metadata decision.

## Progression / affinity / cooldown bridge

The provider source line maintains cross-system state and event handling for affinity, progression and cooldown behavior on Ars/Iron's casts. The 3.3.0 hardening specifically protects the delegated `ars_cross_*` path from being counted again as if the zero-cost proxy itself were a normal Iron's school spell.

Semantic rule for Black Arcana:

- delegated Ars payload = one real cast;
- Iron's proxy identity = transport;
- provider affinity/progression/cooldown attribution = provider-owned once;
- Black Arcana must not award a second external progression/mastery event merely because both proxy and delegated payload were observable.

RPG Skill Tree remains authority only for its own progression contracts. Similarity between Ars 'n' Spells affinity/progression and RPG Mastery does not create an automatic bridge.

## Equipment cross-feed

At the NeoForge baseline, `EquipmentIntegration` cross-feeds host mana bonuses according to the active mana mode rather than treating every equipment source identically:

- `ISS_PRIMARY` / `HYBRID`: provider can push Ars-derived mana bonuses toward the active Iron's-side shared-pool attributes;
- `ARS_PRIMARY`: the reverse direction is handled through the Ars-side calculation path and the Iron's-targeting bridge clears its own mirrored modifiers;
- `SEPARATE` / `DISABLED`: provider clears shared-pool cross-feed because the pools are independent.

The 1.21.1 source reads Ars 5.x player attributes/perk-derived totals rather than reproducing the removed 1.20.1 per-item mana API path.

## Resonance and shared scaling

Ars 'n' Spells also owns its resonance/scaling contribution to the cross-system bridge. Exact 3.3.2 formulas or signatures are not restated here unless proven on the installed artifact; the important dedup contract is that Black Arcana must not independently mirror the same provider scaling into both host engines.

## Black Arcana boundary

Black Arcana may consume a verified provider result where a real adapter exists, but must not:

- infer provider school from registry-name heuristics when Ars 'n' Spells already resolves it;
- mirror provider affinity/progression/cooldown state as a second authoritative ledger;
- treat an `ars_cross_*` proxy as a separate progression event;
- duplicate equipment bonus cross-feed;
- convert provider affinity/progression automatically into Black Arcana Corruption, Strain, Arcane Danger or RPG Mastery.

If an exact 3.3.2 school/progression/equipment hook is required and has not been verified, the integration fails closed.