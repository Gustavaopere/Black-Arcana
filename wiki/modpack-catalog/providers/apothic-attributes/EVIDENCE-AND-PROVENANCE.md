# Evidence and provenance — Apothic Attributes 2.10.1

## Physical layer

Authoritative physical pack evidence:

- `ApothicAttributes-1.21.1-2.10.1.jar`
- mod id `apothic_attributes`
- version `2.10.1`
- SHA-1 `6a6b84d09801621df5cc2c8a68f35bd93a6cda0f`
- current pack: Minecraft 1.21.1 / NeoForge 21.1.248
- related current providers: Placebo 9.9.2, Curios 9.5.1+1.21.1

The physical artifact is authority for presence/version. No byte-for-byte source/JAR reproducibility claim is made.

## Exact source-version layer

Publisher repository:

`Shadows-of-Fire/Apothic-Attributes@686361b2c7b0e76bf4158890bb8a2e42ef805622`

Evidence at that revision:

- commit message `2.10.1`;
- `gradle.properties`: version 2.10.1, Minecraft 1.21.1, Java 21, NeoForge 21.1.235, Placebo 9.9.0, optional Curios;
- generated NeoForge metadata: mod id/version match, side BOTH and declared minimum ranges;
- root `LICENSE`: MIT for source code;
- `LICENSE_ASSETS`: All Rights Reserved for assets;
- exact `ALObjects` central registry surface;
- exact combat/events/mixin/config/payload/Curios source described by this provider catalog;
- exact changelog: 2.10.1 adds JEI exclusion zones for Attributes GUI; 2.10.0 introduced unified cooldowns + `cooldown_reduction`.

## File-level notice nuance

`StackAttributeModifiersEvent.java` carries an explicit Forge Development LLC copyright/SPDX `LGPL-2.1-only` header in the exact upstream source despite the repository root code license being MIT. This phase performs read-only factual inspection and copies/adapts no upstream implementation. Any future code derivation from that file requires separate file-level license/notice analysis.

## Clean-room classification

Use type: `REFERENCE_ONLY / COMPATIBILITY_TARGET`.

Code consulted: **yes, read-only**, solely to establish factual provider inventory, authority and interoperability constraints.

Assets consulted/copied: **no**.

No upstream implementation is copied or adapted into Black Arcana by this catalog.

## Evidence ceiling

Closed to exact source-version evidence:

- provider registry/content inventory;
- combat/effect/mixin/event surfaces;
- cooldown API;
- clientbound network/config sync;
- Curios/modifier bridge;
- licensing/provenance posture.

Still explicitly not proven:

- byte-equivalence/reproducible build between source and physical JAR;
- full physical-modpack compatibility with every combat/attribute consumer;
- any provider hook not present in the audited exact source.

## Provenance ledger

The exact inspection must be recorded in `docs/provenance/REFERENCE_LEDGER.md` before Phase 2AL is promoted to canonical `main`.
