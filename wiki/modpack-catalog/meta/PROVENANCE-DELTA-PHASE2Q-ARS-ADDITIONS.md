# Provenance Delta — Phase 2Q Ars Additions 21.3.0

Status: `READ-ONLY FACTUAL SOURCE AUDIT / CLEAN-ROOM`

## Installed identity

- provider: Ars Additions;
- mod id: `ars_additions`;
- physical JAR: `ars_additions-1.21.1-21.3.0.jar`;
- runtime metadata: `1.21.1-21.3.0`;
- physical SHA-1: `ce2440b606acb20b79a42bf7c6c24d163c93241f`;
- CurseForge project/file: `974408` / `7646325`.

## Source checkpoint

Factual source inspection is pinned to:

`Jarva/Ars-Additions@91f102a90dc058cf40e4eac5a67a881e48b856b4`

At that revision:

- repository `version` is `21.3.0`;
- root `LICENSE` is GNU LGPL v3;
- `gradle.properties` declares `mod_license=LGPLv3` and Minecraft 1.21.1 / NeoForge 21.1.x;
- the source build baseline references Ars Nouveau `5.11.2.1298`.

The installed pack instead uses Ars Nouveau 5.13.1. Therefore source semantics are useful factual evidence for the Ars Additions release line, but runtime compatibility with the installed base provider remains a separate QA requirement.

Matching version/date between the source revision and published 21.3.0 release is not treated as cryptographic proof that the physical CurseForge JAR was built byte-for-byte from that exact commit.

## Clean-room posture

Black Arcana uses this source only to establish factual provider behavior, registry scale, resource/state ownership, acquisition defaults and safe integration boundaries.

No Ars Additions source code, textures, models, sounds, text or other assets are copied/adapted into Black Arcana by Phase 2Q. LGPL licensing of the repository does not by itself turn provider assets or implementation into Black Arcana design material; any future derivation would require a separate provenance/license review and appropriate notices.

## Shared provenance tables

`SOURCES.md` and `THIRD_PARTY_NOTICES.md` are shared high-churn tables used by concurrent work. This narrow Phase 2Q overlay is authoritative for the Ars Additions catalog checkpoint until those tables are regenerated/reconciled safely. It must not be interpreted as deleting or superseding unrelated provenance entries.
