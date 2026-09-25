# Capability Matrix Delta — Crystal Chronicles 0.1.3-alpha

Status: `SOURCE-PINNED PROVIDER / 1 SPELL / PRISMATIC PORTAL + ALPHA TRAVEL`

This delta records only Crystal Chronicles-specific overlap. It does not replace the global capability matrix.

## Provider-owned semantic capability

| Identity | Provider-native role | Black Arcana deduplication consequence |
|---|---|---|
| `crystal_chronicles:prismatic_portal` | activates a formed Bismuth portal outside Alpha; returns the player to spawn from Alpha | treat as a provider-owned portal/dimensional-travel spell; do not duplicate the same Bismuth/Alpha portal contract inside Black Arcana |

## Support surfaces not counted as separate spells

| Surface | Role | Semantic count |
|---|---|---:|
| `crystal_chronicles:prismatic` school | provider taxonomy/attribute/focus authority | 0 |
| Rainbow Bismuth Crystal focus | acquisition/focus support | 0 |
| Bismuth portal frame + chisel | portal assembly/state | 0 |
| Alpha dimension | destination/world runtime | 0 |
| Prismatic/other school armor and weapons | gear | 0 |
| Iron's preset spells embedded in provider weapons | host-owned spell physicalization | 0 |
| Diffraction Ring | provider gear/action support; not promoted as a standalone spell by this audit | 0 |

## Overlap notes

- generic teleportation similarity does not erase the Crystal Chronicles identity because its cast is coupled to provider-owned Bismuth portal state and Alpha return behavior;
- Iron's preset spells on Crystal Chronicles weapons remain Iron's identities;
- future Black Arcana portal magic should distinguish authority, topology, activation requirements, cost and destination semantics rather than duplicating this provider flow.

## Runtime boundary

Any integration remains fail-closed until the exact assembled pack proves:

- registry/config parity;
- portal activation and persistence;
- dimension travel/restart;
- protection and multiplayer behavior;
- dependency coexistence.

Strict semantic contribution of this delta: **+1**.
