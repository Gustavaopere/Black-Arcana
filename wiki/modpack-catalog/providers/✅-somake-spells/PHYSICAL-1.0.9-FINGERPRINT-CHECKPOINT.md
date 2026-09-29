# Somake Spells 1.0.9 — physical fingerprint checkpoint

Status: `PHYSICAL SHA-1 CAPTURED / EXACT PUBLISHER FILE 8867079 HASH MATCH / ACTIVE SUBSET + REACHABILITY STILL CONDITIONAL`

## Physical evidence

A Project Library physical modlist checkpoint, `modlist(1).txt`, captured on **2026-09-16**, records the top-level row:

- JAR: `somakespells-1.0.9-1.21.1.jar`;
- mod id: `somakespells`;
- runtime: `1.0.9`;
- SHA-1: `171841ac9f802be9309ecc166c1d972ac6d404c0`;
- package/fingerprint column: `3978941398`.

The current sibling dossier at `neoforge-rpg-skilltree@4d9710dc0c9bf17e1fdaef29e48d843de80288d0` preserves the same filename/version and explicitly attributes the physical-line update to 2026-09-16.

## Publisher comparison

Exact CurseForge File `8867079` was independently audited at:

- SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`;
- SHA-256 `1f48dfb93e290b45b628b280d902b2b6471b9d80c2c1b70a4980f14dbe85d48a`.

Therefore, for the hash-bearing physical checkpoint:

`PHYSICAL_SHA1 == PUBLISHER_FILE_8867079_SHA1`

Result: **true**.

This closes the former physical-byte-equality blocker for the current 1.0.9 physical line.

## What this does not close

Hash equality means the exact 83-ID structural registry audit applies to the physical JAR bytes. It does **not** prove:

- which optional registrations survive the actual assembled mod composition at runtime;
- the effective deployed `enableSpellLockSystem` value;
- Iron's effective host/datapack `enabled` / `allow_crafting` settlement;
- object-level survival acquisition/reachability;
- Somake Aqua ↔ TravelOptics authority;
- runtime balance/persistence/network behavior.

Strict semantic contribution remains **+0** until those gates close.

## Provenance boundary

Only factual modlist fields and cryptographic fingerprints are retained. No Somake proprietary implementation body or assets are copied.
