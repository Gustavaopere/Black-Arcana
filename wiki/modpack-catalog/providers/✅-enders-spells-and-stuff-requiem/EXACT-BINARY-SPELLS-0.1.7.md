# Requiem 0.1.7 — exact publisher spell registry

**✅ Binary identity `COUNTED_EXACT` — 57/57 static registrations and unique class-local spell IDs. ⚠️ No gameplay/Survival/config PASS.**

## Proven physical artifact

- Official CurseForge project 1336977, file **8762149** (`ess_requiem-0.1.7.jar`), NeoForge 1.21.1.
- Sibling modlist position **#265**, same filename/version/mod ID `ess_requiem`.
- Size **3,129,333 bytes**, SHA-1 `c4648cced4f9e96527cfa4e3f5edcdcead43abb1` identical to physical modlist, SHA-256 `1d4cc4a8c6e3639b9d41b17c073e6d8f259499d5df96e7baad92b469fedd471b`.
- Independent read-only Java 21: [workflow #38655251099](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38655251099), exact publisher bytecode static inspection `PASS`.

## Compiled registry and correction

| Evidence | Result |
|---|---:|
| `GGSpellRegistry` constructed and stored `Supplier` spell roots | 54 |
| `DTESpellRegistry` constructed spell roots (DTE-conditioned) | 3 |
| Unique root IDs obtained from compiled per-class constructors/getters | **57** |
| Strict user-facing supernatural actions | **52** |
| Technical/residual/summon-AI roots, not added | **5** |
| Unexpected/duplicate physical IDs | **0** |
| Physically absent versus exact source inventory | **`ess_requiem:gong`** |

The exact source-version commit `EnderTheNerd/ESS-Requiem@04ab715d657368b177267a8df196c32329acf3f6` declares **55+3 = 58** roots. The publisher binary differs: its `GGSpellRegistry` lacks the `WEAKENING_GONG` static field and registration, with no `ess_requiem:gong` compiled root in that registry. All other 57 expected spell IDs were confirmed, including three DTE addon roots (`forever_dreaming`, `nightmare`, `nightmare_scream`). Physical strict count is **52**, not source-derived 53. This is an actual publisher/source disparity, not a codegen or catalog parsing alias.

`gong` remains documented in the historical source inventory as **SOURCE-ONLY**, not counted for this publisher JAR. Preserve the source citation and do not fabricate a replacement.

## Authority and unverified boundaries

- Requiem owns its concrete spells and auxiliary provider effects; Iron's owns spell framework, casting, mana and cooldown; DTE owns its base spells. The three DTE-conditioned Requiem identities exist in the exact binary and DTE is listed in the physical sibling, but a live conditional initialization/registration PASS is **not** established.
- Register callsites and constructor IDs are compile-time identities, not proof of loaded registries, actual scroll/weapon access, configuration, runtime cast behavior or real client/server.
- Survival, unique gear activation, summons and AI, multiplayer state, damage attribution, provider mana/cooldown settlement and restart/reload lifecycle remain ⚠️.
- No RPG Skill Tree adapter or duplicated Black Arcana casting/resource runtime. Stage 06.05 remains 🟡, direct physical checks deferred under D035 to Stage09.
- Clean-room: JAR was inspected read-only in CI; no copyrighted publisher binary or implementation copied into repository.

## Campaign accounting

Physical semantic delta vs historical source-pinned ledger: **−1**, not a newly discovered magic root. Current reconstructible minima: **1,856 global / 1,854 in scope**, with **29/39** independently proven exact registry providers and **10/39** conditional. No claim of complete semantic denominator or real-play validation.
