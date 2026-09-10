# FamiliarsLib 1.7.1

## Catalog status

Phase 2AX catalogs installed `familiarslib` 1.7.1 as canonical provider component **#52**.

- reconciled audit base: `main@9cc91f1bf9b7f41708ea70635d5b36b282947866`;
- predecessor canonical internal component coverage: **51/100**;
- current canonical internal component coverage after Phase 2AX: **52/100**;
- FamiliarsLib semantic spell/magic-object delta: **0**;
- final pre-merge HEAD `b5b36a6fa3b1a5bf3b2add56ec3c604592f5ca71` passed Black Arcana CI #2336;
- PR #166 merged as `4238275d2086a00c6f31960114733d74b8cdb1d8`;
- exact merge SHA passed post-merge Black Arcana CI #2337 / workflow run `34430446827`.

The component percentage is an internal catalog-completion metric. It is not the user-facing percentage of spells/magics.

## What FamiliarsLib owns

FamiliarsLib is the framework/core library for the Alshanex familiar ecosystem. The release-correlated official source demonstrates provider-owned surfaces for:

- familiar entity/lifecycle abstractions;
- serializable player-familiar attachment state;
- familiar beds and storage;
- summon, selection, release, movement, storage and synchronization networking;
- familiar spellcasting abstractions and familiar-spellbook/school interoperability;
- classification tags over external Iron's spells.

Its `PayloadHandler` registers 17 optional payload handlers: 9 serverbound and 8 clientbound. This is real provider networking, not a Black Arcana transport seam.

## What it does not own in the current semantic catalog

The complete release-correlated source tree does not contain a FamiliarsLib-owned spell registry or `data/familiarslib/spells/**` content. The files under `data/familiarslib/tags/irons_spellbooks/spells/**` classify external Iron's spell identities; they do not mint new spell identities.

The `1.21.1-1.7` publisher changelog also explicitly states that all Sound-school content was removed and moved to Tunes 'n Tomes. Consequently older prose that associates Sound-school content directly with FamiliarsLib must not inflate the current 1.7.x inventory.

For the semantic magic-object metric:

- new independent spells: **0**;
- new independent glyphs/spell-parts: **0 observed**;
- new independent rituals/rites: **0 observed**;
- Phase 2AX semantic numerator delta: **+0**;
- Phase 2AX semantic denominator delta attributable to this provider: **+0**.

## Provider boundaries

FamiliarsLib remains authority for its familiar framework state and transport.

Iron's Spells remains authority for the external spells referenced or cast through the interoperability/classification surfaces observed here.

Tunes 'n Tomes owns the Sound-school content moved out of the 1.7 line and must be counted under its own provider record.

Black Arcana remains authority for canonical casting, targeting, transactional costs, cooldowns/charges, hazards, rituals, Corruption, Strain, Arcane Danger, Backlash and world safety.

## Physical / publisher / source evidence

- physical JAR: `familiarslib-1.21.1-1.7.1.jar`;
- physical runtime: `1.21.1-1.7`;
- physical SHA-1: `7fa3f3116e35c12456425ae195924ced33fcc2eb`;
- CurseForge project/file: `1316458 / 8059464`;
- publisher date: 2026-05-08;
- official repository: `Alshanex/FamiliarsLib`;
- strongest release-correlated commit: `56561e7fd474fbd5c5166c1ac96f235faae156ab`;
- correlated tree: `9d39b4751b9e52874f66cf2187afab239d00b251`, recursive `truncated=false`.

The source correlation is strong but is **not** promoted to an exact source-to-binary pin. No matching release tag or reproducible-build proof was established.

See [`EVIDENCE-AND-PROVENANCE.md`](./EVIDENCE-AND-PROVENANCE.md) for the detailed evidence layers, networking/persistence findings, semantic-count rationale, exactness gaps and license discrepancy.

## Black Arcana Stage 07.07 disposition

No new FamiliarsLib runtime adapter is justified by Phase 2AX.

Borrowed Sight and other familiar-sensitive Black Arcana behavior may only accept a non-native familiar ecosystem through a verified provider-specific ownership adapter. Generic nearby tameables, class-name inference, spellcasting-pet ancestry or client selection are insufficient. The server must be able to prove ownership through a stable provider-native seam.

The correlated source shows provider-owned familiar state, but this audit does not yet close an exact installed-version public ownership contract. Integration therefore remains **fail-closed**.

## Clean-room / license

License surfaces disagree between the release-correlated source property (`All Rights Reserved`), current CurseForge (GPLv3) and current Modrinth (MIT). No reuse permission is inferred. Phase 2AX is read-only factual inspection; no provider code/assets/text are copied or adapted.

Phase 3 remains blocked until the provider catalog/deduplication pass establishes real Black Arcana gaps and the global semantic magic denominator is reconstructible.
