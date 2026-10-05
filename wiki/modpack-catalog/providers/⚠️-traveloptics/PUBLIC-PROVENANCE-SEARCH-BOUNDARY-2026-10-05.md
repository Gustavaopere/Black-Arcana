# T.O Magic n' Extras 4.4.0.1 — public provenance search boundary

Status: `CURRENT PHYSICAL SHA/FINGERPRINT PUBLIC ORIGIN NOT IDENTIFIED / AUG-17 LOCAL CANDIDATES METADATA-ONLY / PACK-LOCAL EVIDENCE REQUIRED / FAIL-CLOSED`

## Purpose

This checkpoint records the exhausted **public/indexed provenance** search for the current physical Traveloptics artifact:

- canonical filename: `traveloptics-4.4.0.1-1.21.1.jar`;
- current physical SHA-1: `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4`;
- current physical fingerprint: `4254006126`.

It does **not** claim that the artifact has no public origin. Search-engine and repository non-results are negative discovery evidence only.

## Public/indexed search — 2026-10-05

Bounded current web searches used the exact:

- SHA-1 `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4`;
- fingerprint `4254006126`;
- filename `traveloptics-4.4.0.1-1.21.1-fixed-keyloot.jar`.

No indexed result identified the current physical SHA, the physical fingerprint, or the retained `fixed-keyloot` filename as a published artifact/provenance source.

The related public artifact that does surface is the already-audited third-party compatibility patch:

- project/file: `1690333 / 8861368`;
- filename: `traveloptics-4.4.0.1.1-1.21.1-patched.jar`;
- upload date: **2026-09-12**;
- known SHA-1 from the existing clean-room patch audit: `680fa679d8ea2419a79571f455436367222f6f9d`;
- publisher-described scope: correct `TOLootModifiers` so `key_loot` uses `KeyLootModifier.CODEC` and `universal_loot` uses `UniversalLootModifier.CODEC`, with no other mod classes/resources changed.

That patch cannot explain the current artifact as a later download/rename because:

1. `7b74816e...` is directly captured in the assembled instance by **2026-08-22**;
2. File `8861368` was uploaded on **2026-09-12**;
3. the two SHA-1 values differ.

## User-repository search — 2026-10-05

Bounded public GitHub searches across repositories owned by `Gustavaopere` for:

- `fixed-keyloot`;
- `TOLootModifiers`;
- `UniversalLootModifier`;
- `traveloptics`;

did not identify a public script, commit or checked-in artifact establishing how the current `7b74816e...` JAR was produced.

This is not evidence that no local script/history ever existed. It establishes only that no such provenance was found in the searched public repository surface.

## Retained Aug-17 candidate boundary

Project/Library metadata preserves two candidate files from **2026-08-17**:

| Retained record | Model-generated | Recorded size |
| --- | --- | ---: |
| `traveloptics-4.4.0.1-1.21.1.jar` | no | 18,393,445 bytes |
| `traveloptics-4.4.0.1-1.21.1-fixed-keyloot.jar` | yes | 18,393,641 bytes |

The first size equals publisher File `6342780`'s recorded length; size equality is not hash equality.

The currently auditable retained-file surface exposes name, size and timestamps for these two records but no cryptographic checksum for either candidate. Their raw bytes are not available through the present retained-evidence path used by this catalog audit. Consequently:

- neither Aug-17 candidate can be identified as SHA-1 `7b74816e...`;
- neither can be excluded by direct candidate hashing here;
- `fixed-keyloot` must not be treated as the current canonical artifact merely because its name suggests the historical repair;
- the existing #474 common-repack negative audit remains valid but does not identify either retained candidate.

## Current provenance conclusion

Current evidence supports only:

- `7b74816e...` / fingerprint `4254006126` = **current verified physical identity**;
- original File `6342780` = **not current by SHA-1**;
- public patch File `8861368` = **not current by SHA-1 and chronologically too late**;
- common tested one-entry repacks from audit #474 = **not byte-identical matches**;
- public/indexed exact-SHA/fingerprint/fixed-keyloot provenance = **not identified**;
- public user-repository provenance = **not identified**;
- retained Aug-17 candidate identity relative to `7b74816e...` = **unresolved**.

Disposition remains:

`OTHER_VERIFIED / AUGUST LOCAL-MODIFICATION LINEAGE NARROWED / ENTRY-LEVEL PROVENANCE UNRESOLVED`.

## Next authoritative evidence

Repeating general public searches for the same SHA/fingerprint/name is no longer a useful closure strategy unless a new indexed source appears.

Gate 1 now requires one of:

1. exact physical `7b74816e...` bytes from the authoritative assembled instance for clean-room entry-level comparison;
2. a cryptographic checksum/content inventory for either retained Aug-17 candidate that can be bridged to `7b74816e...`;
3. contemporaneous local provenance showing the exact transformation/output that became the canonical current JAR;
4. an exact-current runtime/content attestation strong enough to close the specific downstream registry/stat questions without identifying the historical build process.

Until then, publisher-baseline registry/mechanics evidence must not be promoted to exact-current physical equality.

## Catalog consequence

No spell count or status changes.

- publisher baseline remains 33 registered identities;
- historical modified runtime remains 33/33 observed but hash-unbound;
- current physical registry equality remains unverified;
- current `TOLootModifiers` object wiring remains unverified;
- Blackout current-pack acquisition remains unverified;
- Traveloptics remains **⚠️ partial/conditioned**;
- strict current-physical contribution remains **+0**.
