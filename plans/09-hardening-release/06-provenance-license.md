# 09.06 — Provenance & License Audit

## Objective

Close Black Arcana's clean-room and third-party compliance state before public distribution. The project is All Rights Reserved for Black Arcana-owned material, but that does not override third-party rights or grant permission to copy reference implementations.

Ambiguous rights fail closed. This engineering policy is not a substitute for legal advice.

## Public records

The release repository must maintain:

- root `LICENSE` — Black Arcana-owned All Rights Reserved notice;
- root `SOURCES.md` — reference/dependency/compatibility index;
- root `THIRD_PARTY_NOTICES.md` — reproducible third-party audit and derivation ledger;
- `docs/reference/` — clean-room behavior classification and host-capability evidence.

The built JAR must contain `LICENSE` and `THIRD_PARTY_NOTICES.md`.

## Clean-room audit

Confirm no Mahou Tsukai or other reference implementation code/assets entered the repository. The audit must cover more than string search:

- source structure, identifiers and comments;
- copied/decompiled implementation fragments;
- translations/writing;
- textures/models/animations;
- sounds/music;
- particles or other binary resources;
- names strongly tied to external protected expression where Stage 01 intended an original identity.

The Stage 01 observable catalog and classification matrix are design evidence, not permission to derive source.

## Dependency/API audit

Audit exact release-facing versions and terms for:

- Iron's Spells 'n Spellbooks;
- Ars Nouveau;
- Eidolon: Repraised;
- Malum;
- RPG Skill Tree sibling integration;
- Curios when shipped as a supported Stage 05A provider;
- any new host added by Rituals/Spell Domains/Progression before release.

For normal API integration, record the external authority and version without claiming ownership of its source/assets.

## Minimum record for actual derivation

No substantial source or asset may be copied/adapted unless `THIRD_PARTY_NOTICES.md` records:

- upstream project and canonical URL;
- immutable commit/tag/source snapshot;
- exact upstream file/resource;
- exact local file/resource;
- `DERIVED_CODE` or `DERIVED_ASSET`;
- applicable code/asset license or written permission;
- notice/source/copyleft obligations;
- modification note/date;
- permission evidence where required.

An installed JAR/file ID proves artifact identity, not source-reuse rights.

## Project license check

Black Arcana's metadata declares `All Rights Reserved`; the root `LICENSE` must agree. Do not silently convert the project to an open-source license as part of release cleanup. If the owner later chooses a different license, that is a separate explicit decision and must first be compatible with every actual third-party-derived component.

## CI/validator direction

Release validation should fail when:

- required root provenance files are absent;
- a derivation lacks exact source revision/files/rights;
- an ARR/restricted asset lacks permission evidence;
- required notices are missing from source or JAR;
- a new dependency/reference appears without ledger coverage;
- forbidden clean-room reference identifiers/assets are detected by the maintained audit rules.

Automated checks complement manual review; they cannot prove copyright originality on their own.

## Acceptance

- Black Arcana-owned license state is explicit and packaged;
- every dependency/reference/compatibility target is indexed;
- Mahou Tsukai remains clean-room reference only;
- all actual third-party source/assets are either provably compliant or removed/reimplemented independently;
- no unresolved provenance/permission blocker remains in the release artifact.
