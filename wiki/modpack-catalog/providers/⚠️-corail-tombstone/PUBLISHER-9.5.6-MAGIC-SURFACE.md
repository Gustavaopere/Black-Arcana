# Corail Tombstone 9.5.6 — publisher + exact-artifact magic surface

## Evidence boundary

Physical authority:

`neoforge-rpg-skilltree@6657e5bd006d16a244fd4cfe219fc7a15c911714`

Physical artifact identity:

`tombstone-neoforge-1.21.1-9.5.6.jar` / mod id `tombstone` / runtime `9.5.6`.

Exact publisher artifact:

- CurseForge project `243707`;
- file `8842741`;
- SHA-1 `d830d16caa20b0d23a44ed6b1d339bc22afc2460`;
- SHA-256 `520e2a3cb5fb8001da20a23aaf39a7fd8fd937af962c2b43c55460099e30b23b`.

Installed-byte equality remains unasserted because the sibling row has no independent SHA.

## Release lineage relevant to magic

| Version | Publisher-reported change relevant to this catalog |
|---|---|
| 9.5.6 | high-level XP restoration overflow fix |
| 9.5.5 | Create Aeronautics vehicle-respawn compatibility |
| 9.5.4 | learned Ritual Flute melodies auto-play on the correct block; old flute screen removed |
| 9.5.3 | adds Nights of Nour lore sequence |
| 9.5.2 | Grave Guardian trades data-driven; readable scrolls adjusted |
| 9.5.0 | Bone Scepter and spellcasting animation for tamed undeads / Grave Guardian |

## Public + exact reconciliation

| Surface | Reconciled state |
|---|---|
| Ankh prayer near Decorative Grave | exact `onGrave` action + exact recipe + publisher reachability; counted |
| enhanced prayers | five player-facing identities reconciled against exact PrayerHelper/action keys; counted |
| Ritual Flute | four exact executable melody/action paths; counted |
| readable Forgotten Knowledge scrolls | progression/lore documents; +0 by themselves |
| 11 scroll-buff variants | exact MobEffect-backed physicalizations; metric-excluded |
| five magic tablets | exact castable actions, but independent per-item allow config makes current eligibility conditional |
| Familiar/Guardian/Merchant gemstones | exact castable actions, but per-item allow config makes current eligibility conditional |
| Gemstone of Prayer | prayer invocation/support; deduplicated against counted prayer identities |
| Grave Key / Lost Tablet / Magic Scroll / Scroll of Knowledge | exact active/config-gated magic-item surfaces; semantic roles/deduplication closed by the later castable matrix, eligibility still depends on deployed config |
| Knowledge of Death | progression state; +0 by itself |
| 13 enchantments | gear identities; +0 |
| 24 effects | status identities; +0 |

## Current counted semantic result

Strict release-bounded action count:

- prayers: **6**;
- Ritual Flute actions: **4**;
- total: **10**.

`SEMANTIC_DELTA = +10 COUNTED_RELEASE_BOUNDED`

Additional magic-item action families remain outside the strict sum because the exact release exposes 12 provider-specific one-to-one `allow_*` gates and the deployed values are not available. Exact semantic deduplication is recorded in `EXACT-9.5.6-CONDITIONAL-CASTABLE-MATRIX.md`.

## Clean-room boundary

The exact JAR was used only for factual clean-room interoperability/catalog evidence: hashes, paths, IDs, enum/field identities, signatures, structured references and config-field names.

No proprietary implementation body or asset is copied or reconstructed.

## Next closure evidence

To promote the whole provider from ⚠️ to ✅, obtain:

1. deployed `AllowedMagicItems` values for the exact pack;
2. physical installed-JAR digest if `COUNTED_EXACT` rather than release-bounded evidence is desired.

Runtime/death/grave/XP/multiplayer QA remains independent from semantic catalog closure.
