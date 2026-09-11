# Phase 2AY canonicalization — GTBC's SpellLib

## Canonical evidence

- Phase 2AY audit PR: **#175**
- audited branch HEAD: `2260c46261ac9ab99d839f307fd7b4519d38eef2`
- pre-merge Black Arcana CI: **#2420**, GREEN on the exact audited HEAD
- merge SHA: `9a4e1cd6a462a278083ab946b5ed054864c3315e`
- post-merge Black Arcana CI: **#2421**, GREEN on the exact merge SHA
- post-merge validation includes unit tests, diff sanity, NeoForge build, built-JAR verification, Foundation GameTest server, dedicated-server smoke and canonical QA JAR publication

## Provider-component metric

Phase 2AY closes GTBC's SpellLib 2.2.0 as component **#53** of the established 100-component provider audit denominator.

Canonical provider-component coverage after Phase 2AY: **53/100 = 53%**.

This metric measures audited provider/components. It is not the user-facing semantic spell/magic percentage and must never be substituted for it.

## Semantic magic metric

GTBC's SpellLib contributes **0** independent semantic magic objects. It is publisher-defined library/API infrastructure with no standalone gameplay on its own; attributes and reusable spell/helper abstractions are not standalone provider-owned spell identities.

Therefore Phase 2AY itself does not change the semantic magic numerator or denominator.

A separate source-pinned correction in [`SEMANTIC-MAGIC-DELTA-WEREWOLVES-LEAP.md`](./SEMANTIC-MAGIC-DELTA-WEREWOLVES-LEAP.md) proves that Werewolves Leap was incorrectly left conditional in the older semantic ledger. Once that correction is merged/validated, the strict semantic counted minimum becomes **797**, while the global denominator still remains open.

## Authority / clean-room

- physical modlist remains authority for installed GTBC artifact/version;
- exact public GTBC release and publisher documentation bound the library classification;
- no GTBC JAR decompilation or private source use occurred;
- Iron's and each consuming addon retain authority for their concrete casting/spell identities;
- Black Arcana retains authority for its own canonical casting, costs, targeting/effects, cooldowns, hazards, rituals, Corruption, Strain, Arcane Danger, Backlash and WorldEffectPolicy.