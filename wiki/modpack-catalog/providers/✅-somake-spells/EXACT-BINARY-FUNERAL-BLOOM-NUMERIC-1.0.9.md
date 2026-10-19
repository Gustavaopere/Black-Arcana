# Somake Spells 1.0.9 — Funeral Bloom numeric fingerprints (Java 21)

**Status:** 🟡 PENDING_EXACT_SHA_NUMERIC_AUDIT. This document must not be used to infer formulas or perk multipliers before real evidence is inspected.

## Physical gate and scope

- Installed/sibling modlist baseline: `neoforge-rpg-skilltree/main@ed5b65b890767b406ce41127bcb793775263c7bd`, `somakespells-1.0.9-1.21.1.jar` (File 8867079), mod ID `somakespells`, SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`.
- [Read-only scanner](../../../../docs/qa/somake_109_numeric_fingerprint.py), [synthetic tests](../../../../docs/qa/somake_109_numeric_fingerprint_test.py), [Java21 workflow](../../../../.github/workflows/somake-109-numeric-fingerprints.yml).
- Source-pinned class cohort: `FuneralBloomSpell`, `FuneralBloomControllerEntity`, `FuneralBloomBudEntity`, `FuneralBloomImpactEntity`.
- Selected method families: radius, impact damage, max targets, duration, wave interval, telegraph, Wither, lifecycle, impact, prediction and impact scale/opening.

## Contract of numeric evidence

The scanner emits numeric literal occurrences **by method**, arithmetic instruction counts, branch counts, JVM descriptors and bounded selected callsite counts. It does not emit instruction streams, constant pools, reconstructed Java, implementation bodies or the provider JAR. A numeric literal in a JVM method is not automatically a distance, tick duration, cap, clamp bound, multiplicative scaling coefficient or actual configuration value. Its meaning requires stack/dataflow proof and runtime acceptance.

| Axis | Before exact numeric gate |
|---|---|
| Spell ID / class | ✅ `somakespells:funeral_bloom` and four provider class identities previously verified |
| Radius and number of targets | ⚠️ Getters and `SchoolType.getPowerFor`, `Mth.clamp` already observed; no supported effective values |
| Damage / Wither | ⚠️ Impact and Wither getters exist; formulas and conditions unverified |
| Time / pulses | ⚠️ Duration, wave interval, telegraph, bud lifetime and visual opening require values and causal checks |
| Per-player mutators | ⛔ `FAIL_CLOSED`; no supported callback or setter by player established |
| Game, client, multiplayer, Survival | ⚠️ Not tested by static audit |

**Promotion gate:** inspect outputs from the exact JAR, reconcile all literal claims with method-level evidence, keep ambiguous numeric parameters conditional, then review CI on the HEAD and avoid Stage promotion. Black Arcana owns its magic runtime, not Somake's native spell execution; RPG Skill Tree supplies progression only through real contracts.