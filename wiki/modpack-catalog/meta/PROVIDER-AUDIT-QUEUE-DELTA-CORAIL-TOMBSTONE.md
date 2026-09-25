# Provider Audit Queue Delta — Corail Tombstone 9.5.6

Date: `2026-09-24`

This overlay applies to `tombstone` until the current physical-provider queue is regenerated integrally.

## Current row

| Mod ID | Installed identity | Effective audit state |
|---|---|---|
| `tombstone` | `tombstone-neoforge-1.21.1-9.5.6.jar` / runtime 9.5.6 | ⚠️ `PARTIAL / EXACT PUBLISHER ARTIFACT AUDITED / 10 COUNTED_RELEASE_BOUNDED PRAYER-RITE ACTIONS / CONFIG-CONDITIONAL CASTABLE ITEMS REMAIN / RUNTIME QA FAIL-CLOSED` |

## Physical evidence

Sibling authority:

`neoforge-rpg-skilltree@e54536b2c875d7b60edc27669473d1d8a71eaf84`

The sibling dossier still does not preserve an independent installed-JAR digest.

## Exact publisher evidence

Exact File `8842741` clean-room audit:

- bytes `2,520,705`;
- SHA-1 `d830d16caa20b0d23a44ed6b1d339bc22afc2460`;
- SHA-256 `520e2a3cb5fb8001da20a23aaf39a7fd8fd937af962c2b43c55460099e30b23b`;
- 590 provider classes;
- 1,066 provider resources.

## Closed by current evidence

- exact release artifact identity/hash;
- six provider prayer action identities;
- four Ritual Flute action identities;
- exact Ankh recipe/reachability support;
- publisher-supported Ritual Flute loot/reachability;
- no prayer disable field in the exact config signature; only `prayerCooldown`;
- no Ritual Flute/rite server/common enable-disable field observed;
- 11 scroll-buff variants reconciled as MobEffect physicalizations and excluded;
- readable Forgotten Knowledge scrolls reconciled as progression/lore and excluded by themselves;
- 13 enchantments and 24 effects remain metric-excluded.

## Strict semantic accounting

Prayer subtotal: **6**.

Ritual Flute subtotal: **4**.

Provider strict contribution:

**+10 `COUNTED_RELEASE_BOUNDED`**.

No shared global minimum is changed in this provider-specific overlay; shared ledgers should be reconciled separately after this checkpoint merges.

## Still open

- installed-JAR ↔ publisher-file byte equality;
- deployed `AllowedMagicItems` state; the read-only collector now has a bounded 12-key capture path, but no actual pack result is present in this checkpoint;
- five tablet action candidates;
- Familiar/Guardian/Merchant gemstone action candidates;
- Grave Key / Lost Tablet / Magic Scroll / Scroll of Knowledge semantic eligibility;
- exact resource/Soul settlement;
- prayer/rite persistence;
- death/grave/XP runtime;
- Create Aeronautics vehicle respawn;
- multiplayer/protection/restart;
- Black Arcana integration boundary.

## Effective result

Tombstone remains **⚠️ partial / conditioned**, but the previous all-pending semantic state is superseded.

Current strict provider delta: **+10**.
