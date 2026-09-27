# T.O Magic n' Extras 4.4.0.1 — physical fingerprint checkpoint

Status: `PHYSICAL SHA-1 CAPTURED / OTHER_VERIFIED / CURSEFORGE FILE 6342780 SLOT MARKED LOCALLY MODIFIED / NOT KNOWN PATCH 8861368 / CURRENT PHYSICAL BYTES REQUIRE AUDIT`

## Physical evidence

A Project Library physical modlist checkpoint, `modlist(1).txt`, captured on **2026-09-16**, records:

- JAR: `traveloptics-4.4.0.1-1.21.1.jar`;
- mod id: `traveloptics`;
- runtime: `4.4.0.1-1.21.1`;
- SHA-1: `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4`;
- package/fingerprint column: `4254006126`.

The current sibling at `neoforge-rpg-skilltree@d954e7ce193823a0b98fd893f6f915178ed3d597` still preserves the same installed filename/version.

## Known comparison artifacts

Original exact publisher File `6342780`:

- SHA-1 `3808493ce45cdfeb6408e85578adecf13df698e8`.

Known third-party patch File `8861368`:

- SHA-1 `680fa679d8ea2419a79571f455436367222f6f9d`.

Physical comparison:

- physical == original: **false**;
- physical == known patch: **false**.

Disposition: **`OTHER_VERIFIED`**.

## CurseForge instance provenance refinement

A Project Library `minecraftinstance.json` snapshot stored on 2026-08-18 preserves the CurseForge-managed install metadata for the same on-disk filename:

- project id: `1046916`;
- tracked file id: `6342780`;
- tracked publisher SHA-1: `3808493ce45cdfeb6408e85578adecf13df698e8`;
- `fileNameOnDisk`: `traveloptics-4.4.0.1-1.21.1.jar`;
- `isModified=true`;
- `isWorkingCopy=false`;
- `isFuzzyMatch=false`;
- `latestFile.id=6342780`.

Combined with the later physical SHA-1 `7b74816e...`, this narrows provenance materially: the installed path is still managed as CurseForge File `6342780`, but its bytes have been modified locally relative to the tracked publisher hash. This is **not** evidence of a second official Traveloptics release and does **not** identify the modification contents.

The current bytes also do not equal known patch File `8861368`; therefore the exact local modification must still be materialized/audited before its registry or loot-modifier semantics can be promoted.

An exact-hash web lookup rechecked on 2026-09-27 returned no indexed public match for `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4`; absence of a search hit is not content/provenance proof.

## Catalog consequence

The clean-room File-6342780 audit remains valid for that publisher artifact and provides a **33-ID release baseline**. It can no longer be presented as byte-exact evidence for the currently fingerprinted physical JAR.

Although launcher-level provenance is now narrowed to a locally modified File-6342780 install, the exact `7b74816e...` modification bytes/content are still unavailable. Until those bytes or equivalent exact content evidence are available:

- current physical spell-registry equality to the 33-ID baseline is **unverified**;
- current physical `TOLootModifiers` wiring is **unverified**;
- known patch deployment is **disproved by hash**;
- `traveloptics:blackout` reachability remains unresolved;
- strict semantic contribution remains **+0**.

## Clean-room boundary

This checkpoint records only physical filename/version, SHA-1/fingerprint, CurseForge install metadata fields, and comparisons against already-audited artifact hashes. No upstream binary or implementation body is redistributed.
