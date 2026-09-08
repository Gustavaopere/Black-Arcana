# Provider Audit Queue Delta — Phase 2AC Ars Sophisticated Compatibility 0.3.0

Status: `FUNCTIONAL FAMILY CATALOG CLOSED / EXACT PHYSICAL INTERNALS + RUNTIME QA OPEN`

This narrow overlay prevails only for `arssophisticatedcompat` until the full shared provider queue is regenerated safely. It supersedes only the stale `Ars Sophisticated Compatibility` row/state in `PROVIDER-AUDIT-QUEUE.md`; all unrelated provider rows and later, more specific deltas remain authoritative.

## Canonical row delta

| Mod ID | Nome atual | JAR atual | Versão atual | Estado da auditoria | Delta |
|---|---|---|---|---|---|
| `arssophisticatedcompat` | Ars Sophisticated Compatibility | `arssophisticatedcompat-0.3.0.jar` | `0.3.0` | `PHYSICAL IDENTITY CONFIRMED / OFFICIAL 0.3.0 FAMILY: SOURCE STORAGE + STORAGE SOURCE LINK + POTION JAR + ENCHANTER UPGRADE CATALOGADOS / EXACT PHYSICAL INTERNALS + RUNTIME QA FAIL-CLOSED` | stale `GUIA LIDO / CATÁLOGO GRANULAR PENDENTE` row replaced by physical-identity + functional-family catalog with exact-binary limitations explicit |

## Closed in catalog

- physical filename/mod id/runtime version/SHA-1;
- current physical Ars Nouveau, Sophisticated Core and Sophisticated Storage host versions;
- distinction between installed `arssophisticatedcompat-0.3.0.jar` and accessible official `arssophisticatedstoragecompat-0.3.0.jar`;
- official 0.3.0 functional-family surface: Source Storage, Storage Source Link, Potion Jar, Enchanter's Upgrade;
- documented Stack Upgrade scaling at the functional-family level without inventing formulas;
- provider authority split and deduplication constraints;
- clean-room provenance boundary;
- Notion dependency drift: Sophisticated Core 1.5.0 -> physical 1.5.1.

## Remains open / fail-closed

1. Exact public source or exact binary inspection for installed SHA-1 `7cc6c1e1d92d109230f68b6a63dc4bfb13c245a6`.
2. Exact registry IDs and recipes.
3. Dependency version ranges.
4. Config schema/defaults.
5. Capacity/conversion/repair formulas.
6. Potion representation and cadence.
7. Networking, mixins and event hooks.
8. Physical-artifact license.
9. Real-modpack runtime validation on Ars Nouveau 5.13.1 + Sophisticated Core 1.5.1 + Sophisticated Storage 1.5.91.

## Queue disposition

For queue resolution, the canonical Phase 2 state of `arssophisticatedcompat` is the row above, not the older `GUIA LIDO / CATÁLOGO GRANULAR PENDENTE` state in the shared baseline.

Phase 2 catalog may advance after this documentation lands because the physical identity and publicly documented functional family are cataloged and every unobserved implementation-specific claim remains explicitly fail-closed. This does **not** promote the exact physical binary/API/runtime to validated status.

No Black Arcana adapter should be implemented from this entry until the exact physical binary/API gate needed by that adapter is closed.

The next provider must be selected from the latest 2026-09-08 physical modlist rather than the older 612-entry guide snapshot.

## Merge gate

Before merge: fetch current `main`, reconcile semantically if it advanced, review the exact final catalog-only diff, require fresh CI on the reconciled HEAD and keep review threads clear. Exact physical-internal/runtime items above may remain explicitly deferred and must not be reported as PASS.