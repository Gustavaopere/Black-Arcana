# Phase 2AX Checkpoint — FamiliarsLib 1.7.1

## Scope

Documentation/catalog closure for the physically installed FamiliarsLib component. No Black Arcana runtime code was added or changed by this phase.

## Reconciled base and branch history

- phase branch: `docs/magic-catalog-phase2ax-familiarslib-1.7.1`;
- original branch point: `40fedc5b1658e90b51565690851c2ad113203763`;
- reconciled pre-edit base: `main@9cc91f1bf9b7f41708ea70635d5b36b282947866`;
- the branch was fast-forwarded safely from the old point because the old point was an ancestor; no Phase 2AX work was discarded.

Phase 2AW / PR #161 was already integrated on the reconciled base. Its immediate post-merge run #2308 failed at Foundation GameTest after unit tests, diff sanity, NeoForge build and JAR verification succeeded; later current-main run #2334 completed the full gate successfully. That historical nuance remains preserved.

## Physical identity

Current physical modlist authority:

- top-level entries: **595**;
- Minecraft: 1.21.1;
- NeoForge: `21.1.248`;
- modlist SHA-1: `7aaece7acbfb07ba4d0c66029042f36c50d046f0`;
- JAR: `familiarslib-1.21.1-1.7.1.jar`;
- mod id: `familiarslib`;
- runtime version: `1.21.1-1.7`;
- physical SHA-1: `7fa3f3116e35c12456425ae195924ced33fcc2eb`.

## Publisher evidence

- CurseForge project: `1316458`;
- exact file: `8059464`;
- filename: `familiarslib-1.21.1-1.7.1.jar`;
- platform/game: NeoForge / Minecraft 1.21.1;
- publication date: 2026-05-08;
- changelog intent: fixes familiar beds not actually healing familiars.

The Modrinth `1.21.1-1.7` changelog is also relevant to semantic deduplication: it states that all Sound-school content was removed from FamiliarsLib and moved to Tunes 'n Tomes.

## Official source evidence

Official repository: `Alshanex/FamiliarsLib`.

The strongest release-correlated commit is:

- commit: `56561e7fd474fbd5c5166c1ac96f235faae156ab`;
- date: 2026-05-08;
- message: `Fixed bug with familiar beds not working`;
- tree: `9d39b4751b9e52874f66cf2187afab239d00b251`;
- recursive tree: complete (`truncated=false`).

This is strong temporal/semantic correlation with publisher file 8059464, but no tag or reproducible-build evidence was established. The installed binary is therefore **not claimed to be source-exact**.

The correlated source metadata declares:

- `minecraft_version=1.21.1`;
- `neo_version=21.1.90`;
- `irons_spells_version=1.21.1-3.15.5`;
- `curios_version=9.2.2`;
- `mod_id=familiarslib`;
- `mod_version=1.21.1-1.7`.

## Runtime/provider findings

The release-correlated tree demonstrates real FamiliarsLib authority over familiar framework state and transport:

- serializable NeoForge attachment `player_familiar_data` backed by `PlayerFamiliarData`;
- familiar entity/lifecycle abstractions, beds and storage;
- familiar selection, summon, release, movement and storage flows;
- `PayloadHandler` with 17 optional payload registrations: 9 serverbound and 8 clientbound;
- base spellcasting familiar classes and familiar spellbook/school interoperability;
- Iron's spell classification tags under `data/familiarslib/tags/irons_spellbooks/spells/**`.

Those tags classify provider-external Iron's spells. They are not spell registrations. No FamiliarsLib-owned spell registry or `data/familiarslib/spells/**` content appears in the complete correlated tree.

## Coverage disposition

Internal provider-component metric after canonicalization:

- predecessor canonical coverage: **51/100**;
- Phase 2AX canonical component: **#52**;
- current canonical coverage after Phase 2AX: **52/100 = 52%**;
- denominator delta: **0**.

User-facing semantic magic metric:

- FamiliarsLib independent semantic spells/glyphs/rituals: **0**;
- semantic numerator delta: **+0**;
- semantic denominator delta attributable to FamiliarsLib: **+0**;
- global semantic denominator remains open and no final percentage is claimed.

## Stage 07.07 / Borrowed Sight disposition

No FamiliarsLib ownership adapter is admitted by this phase. Black Arcana's current noetic runtime revalidates authorization server-side through its own ownership registry. Stage 07.07 requires provider-specific ownership evidence; generic nearby tameables, theme matching or a spellcasting familiar superclass are insufficient.

A future FamiliarsLib adapter requires an exact-version provider-native ownership contract that can be validated on the server. Until that seam is proven, the integration remains **fail-closed**.

## License / clean-room

License surfaces disagree:

- release-correlated `gradle.properties`: `All Rights Reserved`;
- current CurseForge surface: GPLv3;
- current Modrinth surface: MIT.

No reuse permission is inferred from this conflict. The audit is factual/read-only and Black Arcana copies no provider code, assets or text.

## Canonicalization result

Phase 2AX completed the required gates:

- final pre-merge HEAD: `b5b36a6fa3b1a5bf3b2add56ec3c604592f5ca71`;
- PR: **#166**;
- pre-merge Black Arcana CI: **#2336 — GREEN** on the exact final HEAD;
- latest-main gate immediately before merge: `main@9cc91f1bf9b7f41708ea70635d5b36b282947866`, unchanged from the reconciled base;
- merge commit: `4238275d2086a00c6f31960114733d74b8cdb1d8`;
- post-merge `main`: confirmed at the exact merge SHA;
- post-merge Black Arcana CI: **#2337 / workflow run `34430446827` — GREEN**, including unit tests, diff sanity, NeoForge build, built-JAR verification, Foundation GameTest server, dedicated-server smoke and canonical QA-JAR publication.

Therefore Phase 2AX is **CANONICAL / POST-MERGE VALIDATED**. Phase 3 remains blocked by the broader provider catalog/deduplication and reconstructible semantic denominator gates.
