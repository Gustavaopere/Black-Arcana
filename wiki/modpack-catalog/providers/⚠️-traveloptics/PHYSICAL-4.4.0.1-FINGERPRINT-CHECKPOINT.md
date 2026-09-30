# T.O Magic n' Extras 4.4.0.1 — physical fingerprint checkpoint

Status: `PHYSICAL SHA-1 CAPTURED / OTHER_VERIFIED / CURRENT PROVENANCE UNIDENTIFIED / OLDER FILE-6342780 LAUNCHER SNAPSHOT IS NON-CONTEMPORANEOUS / NOT KNOWN PATCH 8861368 / CURRENT PHYSICAL BYTES REQUIRE AUDIT`

## Physical evidence

A Project Library physical modlist checkpoint, `modlist(1).txt`, captured on **2026-09-16**, records:

- JAR: `traveloptics-4.4.0.1-1.21.1.jar`;
- mod id: `traveloptics`;
- runtime: `4.4.0.1-1.21.1`;
- SHA-1: `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4`;
- package/fingerprint column: `4254006126`.

The current sibling at `neoforge-rpg-skilltree@1211ebfef1bd6af46705250f2acd54da8f090c96` still preserves the same installed filename/version.

## Known comparison artifacts

Original exact publisher File `6342780`:

- SHA-1 `3808493ce45cdfeb6408e85578adecf13df698e8`.

Known third-party patch File `8861368`:

- SHA-1 `680fa679d8ea2419a79571f455436367222f6f9d`.

Physical comparison:

- physical == original: **false**;
- physical == known patch: **false**.

Disposition: **`OTHER_VERIFIED`**.

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

This snapshot predates the 2026-09-16 physical SHA-1 capture. It proves only that **on 2026-08-18** the launcher tracked that filename as File `6342780` and considered the then-current bytes modified relative to the publisher hash. It does **not** establish temporal continuity to the later `7b74816e...` bytes; the JAR could have been replaced under the same filename in the intervening period.

The September bytes also do not equal known patch File `8861368`. Therefore current provenance remains unidentified and the exact `7b74816e...` bytes/content must still be materialized or otherwise contemporaneously evidenced before registry or loot-modifier semantics can be promoted.

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

It is **not** contemporaneous hash evidence for the September physical artifact. The runtime log does not record the JAR SHA-1, and the August `minecraftinstance.json` only proves that the launcher considered the same filename modified at that time. Therefore the August 33/33 runtime observation must not be projected onto September SHA-1 `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4` without a binary/hash bridge.

## Catalog consequence

The clean-room File-6342780 audit remains valid for that publisher artifact and provides a **33-ID release baseline**. It can no longer be presented as byte-exact evidence for the currently fingerprinted physical JAR.

The older launcher metadata does not identify provenance of the September `7b74816e...` artifact. The 2026-08-19 runtime checkpoint materially narrows the semantic history by proving a modified assembled-pack snapshot with exactly the same 33 spell IDs, but it still lacks the hash bridge required to identify the September bytes. Until those bytes or equivalent contemporaneous exact-content evidence are available:

- August modified-runtime spell-registry equality to the 33-ID baseline is **observed 33/33**;
- current physical spell-registry equality to that 33-ID set is **unverified**;
- current physical `TOLootModifiers` wiring is **unverified**;
- known patch deployment is **disproved by hash**;
- `traveloptics:blackout` reachability remains unresolved;
- strict semantic contribution remains **+0**.

## Clean-room boundary

This checkpoint records only dated physical filename/version/SHA-1 evidence, dated CurseForge install metadata fields, and comparisons against already-audited artifact hashes. The two dated snapshots are not treated as continuous provenance. No upstream binary or implementation body is redistributed.
