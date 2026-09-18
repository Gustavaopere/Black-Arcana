# Traveloptics patch 8861368 — clean-room binary-diff audit

Status: `EXACT PATCH CANDIDATE FINGERPRINTED / ONE-ENTRY BINARY DELTA / PHYSICAL DEPLOYMENT UNVERIFIED / NO RUNTIME PASS`

## Evidence checkpoint

Temporary NON-MERGE evidence branch/PR:

- branch: `audit/traveloptics-patch-8861368-diff-2026-09-17`;
- exact HEAD: `acc73532b21bb0d632b24ffc10b8ce6cd16b5d7b`;
- evidence PR: `#324`;
- workflow: **Traveloptics Patch 8861368 Clean-room Binary Diff**;
- run: `35300707366`;
- audit job: `105462531813`;
- text artifact: `10530435084`;
- artifact digest: `sha256:d83f0d9b8fa02766baaeedc398ef876fcecdce3ee88dc6417858ed3acc30070f`.

The workflow downloaded both exact Curse Maven artifacts and compared ZIP entry names and SHA-256 content digests only. It did not parse class files, run `javap`, decompile bytecode, reconstruct implementation, or extract protected asset contents.

## Exact artifacts

Original publisher artifact:

- CurseForge project/file: `1046916 / 6342780`;
- SHA-1: `3808493ce45cdfeb6408e85578adecf13df698e8`;
- SHA-256: `0372b4b8593288726fb0d6e8cdb86202a87677d0c2dafeb96cab50bf057ec298`.

Third-party patch candidate:

- CurseForge project/file: `1690333 / 8861368`;
- filename: `traveloptics-4.4.0.1.1-1.21.1-patched.jar`;
- SHA-1: `680fa679d8ea2419a79571f455436367222f6f9d`;
- SHA-256: `05f588202900c691fb70389435c9997d090f81a699f7df7cdebcbec552298cc2`;
- internal mod id: `traveloptics`;
- internal version metadata: `4.4.0.1-1.21.1`;
- license metadata: All Rights Reserved.

The patch keeps the same internal Traveloptics version metadata as the original artifact. Filename/version text alone therefore cannot distinguish an original JAR from a renamed patched JAR; physical hash evidence remains mandatory.

## Exact binary-diff scope

Both JARs contain exactly **1339 ZIP entries**.

Comparison result:

- added entries: **0**;
- removed entries: **0**;
- changed common entries: **1**;
- changed class entries: **1**;
- changed non-class entries: **0**.

The only changed entry path is:

`com/gametechbc/traveloptics/loot/TOLootModifiers.class`

All non-class resources and metadata entries are byte-identical between the exact original and exact patch candidate.

This independently proves that File `8861368` is a one-class binary delta over File `6342780`. It does **not** independently prove the semantics of that class change because no class parsing/decompilation was performed.

## Publisher-stated patch purpose

The patch publisher states that the changed class corrects the Traveloptics loot-modifier registry wiring so that:

- `key_loot` uses `KeyLootModifier.CODEC`;
- `universal_loot` uses `UniversalLootModifier.CODEC`.

That semantic description is publisher-attributed evidence. The clean-room binary diff corroborates that the patch changes only `TOLootModifiers.class`, but does not treat the publisher statement as a bytecode-derived result.

## Catalog consequence

This audit narrows Gate 1/2 only:

- exact original fingerprint: **known**;
- exact patch-candidate fingerprint: **known**;
- patch binary scope relative to original: **known — exactly one class entry**;
- actual physical pack disposition (`ORIGINAL_EXACT`, `PATCHED_EXACT`, or `OTHER_VERIFIED`): **not known**;
- assembled-pack registry initialization with the actual deployed hash: **not proven**.

Traveloptics therefore remains **⚠️ Parcial / condicionado**.

No semantic object is added, no component point is awarded, and Black Arcana does not silently apply or reproduce the third-party patch.
