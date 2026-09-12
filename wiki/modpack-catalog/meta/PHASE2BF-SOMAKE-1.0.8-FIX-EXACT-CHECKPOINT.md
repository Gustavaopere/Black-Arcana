# Phase 2BF checkpoint — Somake Spells 1.0.8-fix exact artifact

## State

`EXACT REGISTRY CLOSED / SEMANTIC PROMOTION BLOCKED / ZERO COVERAGE DELTA / FAIL-CLOSED`

## Base authority

- canonical main at Phase 2BF start: `41e96385c7ef5903b2595a4b027c9e2d053f09d6`;
- physical modlist SHA-1: `7aaece7acbfb07ba4d0c66029042f36c50d046f0`;
- physical artifact: `somakespells-1.0.8-1.21.1-fix.jar`;
- mod id/runtime: `somakespells` / `1.0.8`;
- physical SHA-1: `b0ad94c1504709662bee2d08700375ccecbb5ec7`;
- CurseForge project/file: `1461634 / 8417850`;
- prior canonical metric: **874** strict semantic objects and **55/100** provider components.

## Evidence isolated from canonical history

PR #191 is an evidence-only draft/non-merge audit branch. The exact artifact was repeatedly materialized and hash-checked before factual inspection. Key runs: `34659320633`, `34664093646`, and targeted gate run `34664411845` at HEAD `397e09e4bfd65f66b82b1b82151915a91c15148d`.

## What Phase 2BF closes

The installed binary closes the old Phase 2AI registry blocker:

- 67 typed Somake `AbstractSpell` holders;
- 67 unique spell registrations/IDs;
- 67 standalone provider spell classes;
- 61 unconditional registrations;
- 3 registrations gated by `mowziesmobs`;
- 3 registrations gated by `iss_magicfromtheeast`;
- both optional mod IDs are physically present, so all 67 identities register for the current provider set.

This replaces the old publisher-only `over 50` lower-bound as the current registry inventory.

## Why the strict semantic numerator remains unchanged

The provider owns a real spell-lock/mastery path. `enableSpellLockSystem` is `COMMON` in `somakespells/general/common.toml`, code-default `false`; disabled state makes `getUnlockedLevel()` return 100. Enabled state can cancel unlearned casts and registers `/somake` behind permission level 2.

The actual deployed COMMON config is not present in authoritative project material. The exact artifact also proves substantial book/grimoire/Upgrade Forge/loot infrastructure, but not a complete object-level survival acquisition table for all 67 identities. The canonical semantic ledger therefore classifies Somake as `CONDITIONAL`: exact registry identity is known, player reachability is not closed strongly enough.

Result:

- Somake strict semantic delta: **+0**;
- strict global minimum: **874**;
- provider-component coverage: **55/100 = 55%**;
- no semantic percentage is declared because the global denominator remains incomplete.

## Remaining blockers

1. authoritative deployed `somakespells/general/common.toml` value for `enableSpellLockSystem`;
2. complete survival acquisition/reachability proof, or an authoritative generic host/provider contract that safely covers all 67 identities under the deployed config;
3. Somake Aqua vs physically present deprecated T.O Magic alpha ownership/runtime QA;
4. stable provider-native API/hook for any future Black Arcana adapter;
5. numerical mechanics/config/runtime QA remain separate from identity counting.

## Authority / architecture consequence

Iron's remains host casting/resource/cooldown authority. Somake owns its registered spell semantics, Elemental Charges and provider progression/equipment state. Black Arcana does not create a second resource/charge/mastery ledger, mirror provider casts or infer an adapter from binary internals. RPG Skill Tree remains progression-only through real contracts and does not own Somake or Black Arcana magic runtime.

This phase is catalog/provenance/deduplication work only and does not advance the active Black Arcana runtime Stage.
