# Corail Tombstone 9.5.6 — physical equality checkpoint

Status: `PHYSICAL SNAPSHOT = EXACT PUBLISHER FILE 8842741`

## Physical authority

Project Library physical modlist snapshot:

- source: `modlist(1).txt`;
- snapshot date: 2026-09-16;
- exact row: `tombstone-neoforge-1.21.1-9.5.6.jar`;
- mod id: `tombstone`;
- runtime: `9.5.6`;
- physical SHA-1: `d830d16caa20b0d23a44ed6b1d339bc22afc2460`.

Current sibling authority at catalog reconciliation:

``neoforge-rpg-skilltree` current `main` with Tombstone dossier blob `7b99ee63892e9bd3711e27a651c0b62c0d71ba47``

The sibling dossier preserves the same 9.5.6 filename/version line.

## Publisher authority

Exact audited CurseForge artifact:

- project: `243707`;
- File: `8842741`;
- filename: `tombstone-neoforge-1.21.1-9.5.6.jar`;
- SHA-1: `d830d16caa20b0d23a44ed6b1d339bc22afc2460`;
- SHA-256: `520e2a3cb5fb8001da20a23aaf39a7fd8fd937af962c2b43c55460099e30b23b`.

## Result

The physical snapshot SHA-1 equals the exact audited publisher SHA-1.

Consequences for catalog confidence:

- the 10 already-counted prayer/Ritual-Flute action identities move from `COUNTED_RELEASE_BOUNDED` to **`COUNTED_EXACT`**;
- semantic cardinality is unchanged at **+10** for Tombstone;
- the 12 deduplicated castable magic-item families remain **CONDITIONAL** because their effective deployed `AllowedMagicItems` booleans are still unavailable;
- Tombstone remains **⚠️ partial/conditioned**;
- the global strict semantic minimum remains **1677**.

A future deployed-evidence capture should re-observe the physical fingerprint as a drift guard when resolving the 12 config booleans. A mismatch would reopen physical identity for that later environment.
