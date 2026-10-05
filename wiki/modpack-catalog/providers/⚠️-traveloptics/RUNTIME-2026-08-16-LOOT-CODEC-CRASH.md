# T.O Magic n' Extras — 2026-08-16 assembled-pack loot-codec crash reproduction

Status: `HISTORICAL ASSEMBLED-RUNTIME FAILURE REPRODUCED / CANONICAL FILENAME / PROCESS HASH UNBOUND / CURRENT PHYSICAL FIX STATE UNPROVEN`

## Purpose

This checkpoint records a previously uncataloged Project Library runtime fact: before the retained Aug-17 local repair artifacts, the assembled modpack repeatedly failed while Traveloptics handled NeoForge's registry `RegisterEvent`.

This changes the evidentiary status of the old `TOLootModifiers` issue from “structural risk only” to **historically reproduced assembled-pack failure**.

It does **not** prove that the crashing process used exact publisher SHA-1 `3808493...`, and it does not prove that current physical SHA-1 `7b74816e...` carries a specific fix.

## Project Library crash evidence

Four retained crash reports from 2026-08-16 independently show the same failure signature:

- `crash-2026-08-16_19.17.49-fml.txt`;
- `crash-2026-08-16_19.52.32-fml.txt`;
- `crash-2026-08-16_23.33.46-fml.txt`;
- `crash-2026-08-16_23.51.05-fml.txt`.

Each report identifies:

- mod file path ending in `mods/traveloptics-4.4.0.1-1.21.1.jar`;
- mod id `traveloptics`;
- runtime version `4.4.0.1-1.21.1`;
- failure while dispatching `net.neoforged.neoforge.registries.RegisterEvent`;
- `java.lang.IllegalStateException: Adding duplicate value ... to registry`;
- the duplicated value is a `RecordCodec` whose unit decoder is `com.gametechbc.traveloptics.loot.KeyLootModifier`.

The corresponding debug/stdout material preserves the same failure path.

This is a direct assembled-runtime reproduction of the duplicate-codec registration failure. It independently aligns with the exact publisher File `6342780` clean-room structure where `TOLootModifiers` registers two names but references `KeyLootModifier.CODEC` twice and `UniversalLootModifier.CODEC` zero times.

## Hash boundary

The crash reports identify the canonical filename and version, but do **not** embed the JAR SHA-1.

Therefore this checkpoint may prove:

- historical assembled-pack Traveloptics registry failure — **YES**;
- failure signature matches the exact publisher structural defect — **YES**;
- exact crashing bytes equal File `6342780` SHA-1 `3808493...` — **NOT PROVEN**;
- exact crashing bytes equal current physical SHA-1 `7b74816e...` — **NOT PROVEN**.

No binary identity is inferred from the filename/version string alone.

## Chronology consequence

The retained local sequence is now:

1. **2026-08-16** — repeated assembled-pack `RegisterEvent` crash from duplicate `KeyLootModifier` codec registration under the canonical Traveloptics filename;
2. **2026-08-17** — Project Library retains both a canonical-name JAR and a separately named `traveloptics-4.4.0.1-1.21.1-fixed-keyloot.jar`;
3. **2026-08-18** — CurseForge launcher metadata records the canonical File-6342780 slot as `isModified=true`;
4. **2026-08-19** — assembled runtime progresses through Traveloptics and the analyzer observes the same 33 spell IDs as the publisher baseline;
5. **2026-08-22** — first direct physical SHA-1 capture of current replacement lineage: `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4`;
6. **2026-09-08** — same physical SHA-1 is captured shortly before an assembled boot that passes the historical duplicate-registry failure path and later crashes for unrelated Shine shader injection.

This chronology is strong evidence of a local repair/replacement episode between the Aug-16 failing state and the Aug-22 verified current lineage.

It still does **not** identify the exact byte transition:

- the Aug-17 `fixed-keyloot.jar` cannot be assumed to have become the canonical file;
- the Aug-19 process is hash-unbound;
- the first direct `7b74816e...` hash is Aug-22;
- exact entry-level delta of `7b74816e...` remains unmaterialized.

## Gate 2 consequence

Gate 2 is narrowed, not fully closed.

Closed:

- the original/old canonical-name runtime failure mode was actually reproduced in the assembled pack;
- the failure is a duplicate `KeyLootModifier` codec registration during Traveloptics `RegisterEvent`.

Still open for the **current physical** artifact:

- process-embedded attestation tying startup to SHA-1 `7b74816e...`;
- direct observation of both `traveloptics:key_loot` and `traveloptics:universal_loot` serializer entries;
- proof that the two resolved serializer values are distinct codec instances.

The existing `black_arcana_catalog_qa` bounded registry probe remains the preferred current-runtime closure mechanism.

## Catalog consequence

No spell identity, mechanics row, semantic count or provider status changes.

Traveloptics remains:

`⚠️ partial / conditioned`

The new fact only upgrades one evidence statement:

- “actual registry-startup failure in assembled pack” changes from `NOT REPRODUCED` to **`REPRODUCED HISTORICALLY / PROCESS HASH UNBOUND`**.

Current physical runtime promotion remains fail-closed.
