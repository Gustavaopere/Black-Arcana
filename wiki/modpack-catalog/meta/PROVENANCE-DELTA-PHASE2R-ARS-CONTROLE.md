# Provenance Delta — Phase 2R Ars Controle 1.6.15

Status: `READ-ONLY FACTUAL SOURCE AUDIT / CLEAN-ROOM`

## Installed identity

- provider: Ars Controle;
- mod id: `ars_controle`;
- physical JAR: `ars_controle-1.21.1-1.6.15.jar`;
- runtime metadata: `1.21.1-1.6.15`;
- physical SHA-1: `fdf381d5733698abe336354c7541299ab495ecae`;
- current physical base provider: Ars Nouveau `5.13.1`;
- current physical Curios: `9.5.1+1.21.1`.

## Source checkpoint

Factual source inspection is pinned to:

`Vonr/Ars-Controle@ecbb83ba512bc9ca7a025556fb9c62dbd32b6430`

At that revision:

- `gradle.properties` declares `mc_version=1.21.1`;
- `mod_id=ars_controle`;
- `mod_version=1.6.15`;
- `mod_license=LGPLv3`;
- NeoForge build baseline `21.1.217`;
- Ars Nouveau build baseline `5.10.6.1245`;
- Curios baseline `9.0.12`;
- CC:Tweaked baseline `1.112.0`;
- root `LICENSE` is GNU Lesser General Public License v3.

The physical pack instead uses NeoForge 21.1.248, Ars Nouveau 5.13.1 and Curios 9.5.1+1.21.1. Source semantics and registries are factual release evidence, but runtime compatibility with those newer installed providers remains a separate QA requirement.

Matching source `mod_version=1.6.15` and installed provider version is not treated as cryptographic proof that the physical JAR was built byte-for-byte from the exact commit.

## Clean-room posture

Black Arcana uses the source only to establish factual registry/content behavior, acquisition defaults, provider-owned persistence/network/capability paths, authority boundaries and deduplication/safety risks.

No Ars Controle source code, textures, models, translations, sounds or other assets are copied/adapted into Black Arcana by Phase 2R. LGPLv3 permits source inspection but does not automatically convert implementation/assets into Black Arcana material. Any future code derivation or bundling would require a separate explicit derivation record and applicable LGPL/notice compliance review.

No runtime adapter is approved by this provenance record. Public Java visibility, mixin targets, data components and attachments are implementation evidence, not automatically stable addon APIs.

## Shared provenance tables

`SOURCES.md`, `THIRD_PARTY_NOTICES.md` and `docs/provenance/REFERENCE_LEDGER.md` are shared/high-churn surfaces touched by concurrent provider/runtime work. To avoid overwriting concurrent entries, this narrow Phase 2R overlay is the authoritative Ars Controle provenance checkpoint until those shared indexes are regenerated/reconciled safely.

This overlay supersedes no unrelated provenance record and does not delete or weaken existing third-party obligations.
