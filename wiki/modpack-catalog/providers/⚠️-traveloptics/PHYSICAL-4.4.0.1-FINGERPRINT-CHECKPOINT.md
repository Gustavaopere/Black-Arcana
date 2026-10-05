# T.O Magic n' Extras 4.4.0.1 — physical fingerprint checkpoint

Status: `PHYSICAL SHA-1 CAPTURED BY 2026-08-22 / OTHER_VERIFIED / CURRENT PROVENANCE UNIDENTIFIED / NOT ORIGINAL / NOT PATCH 8861368 / COMMON ONE-ENTRY REPACKS DO NOT MATCH / CURRENT PHYSICAL BYTES REQUIRE AUDIT`

## Physical evidence

Project Library physical inventories captured on **2026-08-22**, **2026-09-08** and **2026-09-16** independently record the same installed artifact:

- JAR: `traveloptics-4.4.0.1-1.21.1.jar`;
- mod id: `traveloptics`;
- runtime: `4.4.0.1-1.21.1`;
- SHA-1: `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4`;
- package/fingerprint column: `4254006126`.

All three Project Library physical captures record SHA-1 `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4`; the 2026-08-22 inventory and later modlists also expose fingerprint column `4254006126`. The current sibling was rechecked at `neoforge-rpg-skilltree@b9edb403c06567423d6c101d136b73a1065f2ad4`; its certified T.O Magic n' Extras dossier is Git-blob-identical to the previously cited checkpoint and still records physical row **#550** as the same filename/version/mod id and SHA-1 `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4`.

## Known comparison artifacts

Original exact publisher File `6342780`:

- SHA-1 `3808493ce45cdfeb6408e85578adecf13df698e8`.

Known third-party patch File `8861368`:

- SHA-1 `680fa679d8ea2419a79571f455436367222f6f9d`.

Physical comparison:

- physical == original: **false**;
- physical == known patch: **false**.

Disposition: **`OTHER_VERIFIED`**.

### Chronology consequence

The earliest direct physical SHA-1 capture now available is **2026-08-22**, moving the cryptographic boundary more than two weeks earlier than the previous 2026-09-08 checkpoint. The public third-party patch File `8861368` was uploaded on **2026-09-12**. Therefore the already-present `7b74816e...` physical artifact cannot be explained as a later download/rename of that public patch file. It may still represent an independent local modification touching similar code, but no such lineage is inferred without the physical bytes.

## August local-modification chronology — narrowed 2026-10-05

Retained Project Library evidence now establishes this bounded sequence:

1. **2026-08-17** — a non-generated Library copy named `traveloptics-4.4.0.1-1.21.1.jar` is retained at **18,393,445 bytes**, the same byte length as publisher File `6342780`; size equality is not hash equality.
2. **2026-08-17**, roughly two minutes later — a model-generated `traveloptics-4.4.0.1-1.21.1-fixed-keyloot.jar` is retained at **18,393,641 bytes**.
3. **2026-08-18** — CurseForge instance metadata still tracks project/file `1046916 / 6342780` under the canonical filename but reports `isModified=true`.
4. **2026-08-19** — the assembled runtime analyzer observes exactly the same **33 Traveloptics spell IDs** as the publisher baseline, including `traveloptics:blackout`; that log does not embed the JAR hash.
5. **2026-08-22** — physical inventory `fcb79de3-0e3e-41af-8136-cd524859f71c.txt` records the canonical Traveloptics row at SHA-1 `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4` and fingerprint `4254006126`.

This materially narrows the provenance interval: the currently fingerprinted `7b74816e...` bytes were already present by **2026-08-22**, only days after the retained local repair workflow.

It does **not** prove that the Aug-17 `fixed-keyloot.jar` was renamed into the canonical file, does not prove that the Aug-19 runtime used SHA-1 `7b74816e...`, and does not identify the entry-level delta. The three-day gap between the hash-unbound Aug-19 runtime observation and the first direct Aug-22 hash capture remains a real evidentiary boundary.

## Common-repack lineage audit — 2026-09-30

Temporary NON-MERGE PR **#474** ran a bounded clean-room lineage test against the exact publisher File `6342780` and exact patch File `8861368`.

The audit downloaded both already-fingerprinted public artifacts and reconstructed several common one-entry replacement strategies for only:

`com/gametechbc/traveloptics/loot/TOLootModifiers.class`

Tested archive strategies:

- Info-ZIP delete + add;
- JDK `jar uf`;
- Python `zipfile` rebuild preserving original target metadata;
- Python `zipfile` rebuild using patch target metadata;
- deterministic high-compression Python rebuild.

Run `36649716927` / job `109680786266` completed successfully. Text-only artifact `11070325102` has artifact digest `sha256:ec77f6a9b0782af9fb9961ac1a3d919871b6aad8b4f7f0f1b0e11645657d6ff7`.

Results:

- none of the tested candidates has SHA-1 `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4`;
- the archived Project Library record `traveloptics-4.4.0.1-1.21.1-fixed-keyloot.jar` has recorded size **18,393,641 bytes**;
- none of the tested candidate archive sizes equals **18,393,641 bytes**;
- exact publisher File `6342780` is **18,393,445 bytes**, matching the recorded size of the separate Aug-17 Library file named `traveloptics-4.4.0.1-1.21.1.jar`; size equality alone is not cryptographic identity and is not promoted as such.

This is **negative lineage evidence only**. It narrows the hypothesis space but does not prove what `7b74816e...` contains, does not prove how the Library `fixed-keyloot` file was produced, and does not establish current spell-registry equality.

The initial #474 workflow label also carried `fb37ae0...` as an assumed older Traveloptics hash. Post-run row-boundary verification against the sibling physical dossiers proved that `fb37ae0...` belongs to neighboring **Transmog row #549**, not Traveloptics. That comparison is explicitly discarded and is not catalog evidence.

## Older CurseForge instance metadata — historical context only

A Project Library `minecraftinstance.json` snapshot stored on 2026-08-18 preserves the CurseForge-managed install metadata for the same on-disk filename:

- project id: `1046916`;
- tracked file id: `6342780`;
- tracked publisher SHA-1: `3808493ce45cdfeb6408e85578adecf13df698e8`;
- `fileNameOnDisk`: `traveloptics-4.4.0.1-1.21.1.jar`;
- `isModified=true`;
- `isWorkingCopy=false`;
- `isFuzzyMatch=false`;
- `latestFile.id=6342780`.

This snapshot predates the earliest direct **2026-08-22** physical SHA-1 capture by four days. It proves that **on 2026-08-18** the launcher tracked that filename as File `6342780` and considered the then-current bytes modified relative to the publisher hash. The new Aug-22 capture substantially narrows the interval, but still does **not** cryptographically establish continuity from the Aug-18 modified state or Aug-19 runtime to `7b74816e...`; the JAR could have been replaced under the same filename before the Aug-22 inventory.

The Aug-22-and-later `7b74816e...` bytes also do not equal known patch File `8861368`. Therefore entry-level provenance remains unidentified and the exact `7b74816e...` bytes/content must still be materialized or otherwise contemporaneously evidenced before registry or loot-modifier semantics can be promoted.

An exact-hash web lookup rechecked on 2026-09-27 returned no indexed public match for `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4`; absence of a search hit is not content/provenance proof.

## Historical modified-runtime registry checkpoint — 2026-08-19

Project Library runtime log `stdout-logs(9).txt`, captured on **2026-08-19**, records NeoForge discovering `traveloptics-4.4.0.1-1.21.1.jar` from the assembled pack's `mods` directory and reports runtime `4.4.0.1-1.21.1`.

In the same captured run, the Fundamental Principles registry analyzer emits one contiguous `traveloptics:` spell block. Bounded extraction of the analyzer rows yields:

- **33 unique `traveloptics:<id>` spell identities**;
- the set starts at `traveloptics:blood_howl` and ends at `traveloptics:stele_cascade`;
- `traveloptics:blackout` is present;
- the extracted 33-ID set is exactly equal to the already-audited File-6342780 33-ID release baseline;
- no additional `traveloptics:` spell ID appears before the analyzer advances to the next provider namespace.

This is direct runtime evidence that an **August assembled-pack modified-runtime snapshot** exposed the same 33 spell identities as the publisher baseline and progressed into resource reload/analyzer execution.

It is **not** contemporaneous hash evidence for the exact Aug-22-and-later physical artifact. The runtime log does not record the JAR SHA-1, and the August `minecraftinstance.json` only proves that the launcher considered the same filename modified at that time. Therefore the Aug-19 33/33 runtime observation must not be projected onto SHA-1 `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4` without a binary/hash bridge.

## September physical/runtime correlation — 2026-10-04 reconciliation

A newly reconciled Project Library pair materially narrows runtime uncertainty for the September physical line:

- `modlist 08.09.2026.txt` at ~12:05 UTC records the exact Traveloptics row as SHA-1 `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4`, fingerprint `4254006126`;
- `debug(9).log` from the same CurseForge instance begins the relevant boot at ~12:19 UTC, creates `TravelopticsMod`, loads both Traveloptics config files and subscribes multiple provider handlers;
- complete-log bounded search contains no `Mod loading issue for:` and no `Adding duplicate value`;
- the later crash is instead an unrelated `shine.mixins.json:ProgramMixin` injection failure during shader initialization.

This is **strong contemporaneous physical-runtime correlation**, not process-embedded hash attestation. It proves that a boot temporally adjacent to the `7b74816e...` physical dump progressed beyond the earlier duplicate-codec registration failure, but it does not identify provenance, spell-registry equality or exact serializer-object identity.

See [`RUNTIME-2026-09-08-PHYSICAL-CORRELATION.md`](RUNTIME-2026-09-08-PHYSICAL-CORRELATION.md).
## Catalog consequence

The clean-room File-6342780 audit remains valid for that publisher artifact and provides a **33-ID release baseline**. It can no longer be presented as byte-exact evidence for the currently fingerprinted physical JAR.

The older launcher metadata does not identify the entry-level provenance of the `7b74816e...` artifact. The 2026-08-19 runtime checkpoint proves a modified assembled-pack snapshot with exactly the same 33 spell IDs, and the 2026-08-22 physical inventory proves that the current `7b74816e...` hash existed three days later; 08/09 and 16/09 then prove that hash remained stable across the later interval. The missing link is now narrower but unchanged in kind: there is still no process-embedded/hash bridge proving that the Aug-19 33-ID runtime used the exact Aug-22 `7b74816e...` bytes. Until those bytes or equivalent contemporaneous exact-content evidence are available:

- August modified-runtime spell-registry equality to the 33-ID baseline is **observed 33/33**;
- current physical spell-registry equality to that 33-ID set is **unverified**;
- the duplicate-codec registry failure is **historically reproduced** in four 2026-08-16 assembled-pack crash reports under the canonical filename, but those processes are hash-unbound;
- current physical `TOLootModifiers` exact serializer-object wiring remains **unverified**, while a 2026-09-08 boot contemporaneous with the `7b74816e...` physical dump progressed beyond that historical duplicate-registry failure path;
- known patch deployment is **disproved by hash**;
- tested common one-entry repacks of the known patch class are **disproved as byte-identical matches** for the current physical hash;
- `traveloptics:blackout` reachability remains unresolved;
- strict semantic contribution remains **+0**.

## Clean-room boundary

This checkpoint records only dated physical filename/version/SHA-1 evidence, dated CurseForge install metadata fields, and comparisons against already-audited artifact hashes. The two dated snapshots are not treated as continuous provenance. No upstream binary or implementation body is redistributed.
