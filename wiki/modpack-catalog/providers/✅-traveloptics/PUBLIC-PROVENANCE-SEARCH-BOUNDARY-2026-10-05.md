# T.O Magic n' Extras 4.4.0.1 — public provenance search boundary

Status: `CURRENT PHYSICAL SHA/FINGERPRINT PUBLIC ORIGIN NOT IDENTIFIED / AUG-17 LOCAL CANDIDATES METADATA-ONLY / PACK-LOCAL EVIDENCE REQUIRED / FAIL-CLOSED`

## Purpose

This checkpoint records the exhausted **public/indexed provenance** search for the current physical Traveloptics artifact:

- canonical filename: `traveloptics-4.4.0.1-1.21.1.jar`;
- current physical SHA-1: `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4`;
- current physical fingerprint: `4254006126`.

It does **not** claim that the artifact has no public origin. Search-engine and repository non-results are negative discovery evidence only.

## Bounded provenance surfaces — 2026-10-05

The negative discovery result is grounded in temporary **NON-MERGE PR #641**, not in an unrecorded general-web search.

Canonical audit evidence:

- audit PR: **#641** — `chore(audit): temporary Traveloptics public provenance probe`;
- audit HEAD: `7caca3b2c5a73646e413a39b1b9e75fd7cc2a088`;
- workflow run: `37263841885` — **SUCCESS**;
- text-only artifact: `11324569430`;
- artifact digest: `sha256:6ad7373adb0e8c1b7b5555c87c4dfec3e06858f134f478694f51402a7aa96501`;
- retained report name: `traveloptics-public-provenance-report.txt`.

The report records the exact surfaces, revisions, endpoints and query terms below. No matched source body is retained.

### Surface A — exact Git snapshot scans

The audit checked exact immutable revisions with `git grep -I -F` for:

- SHA-1 `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4`;
- fingerprint `4254006126`;
- filename `traveloptics-4.4.0.1-1.21.1-fixed-keyloot.jar`;
- token `fixed-keyloot`.

Revisions:

- `Gustavaopere/Black-Arcana@98f7669d519dc288142f63e03b40175e25cb638d`;
- `Gustavaopere/neoforge-rpg-skilltree@de80b186357cad20ba5b81892a8682777e96e35a`.

The Black Arcana hits are existing catalog/meta references to the physical hash/fingerprint/Aug-17 candidate chronology. The sibling SHA hit is the existing certified Traveloptics physical dossier. The sibling has zero hits for the fingerprint, fixed filename and `fixed-keyloot` token.

No exact-snapshot hit provides a script, commit-local build recipe or other source identifying how `7b74816e...` was produced.

### Surface B — GitHub public code-search API

Endpoint recorded by the audit:

`https://api.github.com/search/code`

Semantics retained in the report: current GitHub indexed public/default-branch **code** search, not a release/binary/full-web index.

Results:

| Query | HTTP | GitHub total | Interpretation |
| --- | ---: | ---: | --- |
| exact SHA-1 `7b74816e...` | 200 | 0 | no indexed code hit on this surface |
| exact fingerprint `4254006126` | 200 | 12 | 12 external numeric-data hits retained by repo/path/URL; none identifies Traveloptics provenance |
| exact retained filename | 200 | 0 | no indexed code hit on this surface |
| `fixed-keyloot` | 200 | 0 | no indexed code hit on this surface |

The 12 fingerprint hits are treated as unrelated numeric collisions, not as provenance matches; their repository/path/URL list is preserved in artifact `11324569430`.

### Surface C — Modrinth SHA-1 lookup

Endpoint recorded by the audit:

`https://api.modrinth.com/v2/version_file/7b74816e89cc15dd0b5a31d9ea1e456024e8fae4?algorithm=sha1`

Result:

- HTTP **404**;
- audit state: `NO_MATCH`.

This proves only that the exact SHA-1 was not resolved by that Modrinth hash endpoint at audit time.

### Known positive public comparison — separate provenance

The related public compatibility patch remains CurseForge project/file `1690333 / 8861368`, filename `traveloptics-4.4.0.1.1-1.21.1-patched.jar`, uploaded **2026-09-12**.

Provenance is deliberately split:

- the **patch publisher** states the semantic purpose: `key_loot` should use `KeyLootModifier.CODEC` and `universal_loot` should use `UniversalLootModifier.CODEC`;
- Black Arcana clean-room evidence in [`PATCH-8861368-BINARY-DIFF.md`](PATCH-8861368-BINARY-DIFF.md) independently proves the binary scope relative to File `6342780`: **1 changed class entry** (`TOLootModifiers.class`) and **0 changed non-class entries**. The binary diff does not claim to derive the class-change semantics.

File `8861368` still cannot explain the current artifact as a later download/rename because:

1. `7b74816e...` is directly captured in the assembled instance by **2026-08-22**;
2. File `8861368` was uploaded on **2026-09-12**;
3. the two SHA-1 values differ.

### Search-boundary conclusion

Across the named, retained surfaces above, no source identifies the provenance/build transformation of current physical `7b74816e...`.

This is intentionally narrower than “no public origin exists”. In particular:

- GitHub code search is not a release/binary/full-web index;
- Modrinth is one distribution/hash registry, not a universal artifact index;
- exact project snapshot scans cover only the two named repositories/revisions;
- private/local history and other public hosts are outside this negative result.

Repeating the **same named queries against the same retained revisions/endpoints** is no longer a useful closure strategy. A newly indexed source, another explicitly named provenance surface, or pack-local evidence remains valid new evidence.

## Retained Aug-17 candidate boundary

Project/Library metadata preserves two candidate files from **2026-08-17**:

| Retained record | Model-generated | Recorded size |
| --- | --- | ---: |
| `traveloptics-4.4.0.1-1.21.1.jar` | no | 18,393,445 bytes |
| `traveloptics-4.4.0.1-1.21.1-fixed-keyloot.jar` | yes | 18,393,641 bytes |

The first size equals publisher File `6342780`'s recorded length; size equality is not hash equality.

The currently auditable retained-evidence corpus preserves name, size and timestamps for these two records but no cryptographic checksum or exact-content bridge for either candidate. Consequently:

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
