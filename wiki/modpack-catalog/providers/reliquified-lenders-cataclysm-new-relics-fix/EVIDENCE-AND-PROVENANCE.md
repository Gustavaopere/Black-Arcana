# New Relics Fix 1.0.2 — evidence and provenance

## Physical authority

Current physical artifact:

- `reliquified-lenders-cataclysm-new-relics-fix-1.0.2.jar`
- mod id `reliquified_lenders_cataclysm_new_relics_fix`
- runtime `1.0.2`
- SHA-1 `9d4710e665ec74af917bb9f5f819154ca9f74ca0`
- Minecraft 1.21.1 / NeoForge pack baseline `21.1.248`

The physical modlist/JAR metadata is authority for installed identity/version/hash.

## Exact publisher release

CurseForge project:

`https://www.curseforge.com/minecraft/mc-mods/reliquified-l-ender-s-cataclysm-new-relics-fix`

Exact file:

`https://www.curseforge.com/minecraft/mc-mods/reliquified-l-ender-s-cataclysm-new-relics-fix/files/8778365`

Publisher evidence:

- project ID `1665965`;
- file ID `8778365`;
- filename `reliquified-lenders-cataclysm-new-relics-fix-1.0.2.jar`;
- release `1.0.2` for NeoForge / Minecraft 1.21.1;
- uploaded `2026-08-31`;
- Client & Server;
- All Rights Reserved;
- no additional files published for the release.

The exact file changelog says 1.0.2 limits the bridge to the addon's base class and prevents global `RelicItem` modifications.

## Public behavior evidence

The publisher description defines the component as a compatibility bridge from Reliquified L_Ender's Cataclysm `0.1.1` expectations built around Relics `0.10` to newer Relics `0.12` APIs.

It publishes eight functional fix families and names exactly five fixed relics. Those publisher claims are the ceiling for semantic cataloging in this phase.

## Physical dependency evidence

Current physical pack rows confirm:

- Relics `0.12.8`, SHA-1 `1fe7d57ebfa56ebd0aeecfed01075f8b55b94ef7`;
- Curios `9.5.1+1.21.1`, SHA-1 `418fcd42e3a7844c9bdc71c9b6401fdb3894e0c4`;
- OctoLib `0.6.2`, SHA-1 `f4f66d677b104c6af7f5c0f7e3c08d8e4370ecad`;
- L_Ender's Cataclysm `3.33`, SHA-1 `5ff39c0eddfa08ea0e921bdcb17da7f32f0b00ce`;
- Reliquified L_Ender's Cataclysm `0.1.1`, SHA-1 `be89d697455f04a1531ed81b45bcc038354430c8`.

All dependency families named by the publisher are therefore physically present. This proves stack presence, not behavior correctness.

## Source search result

No official public exact-version source repository for the **fix 1.0.2** was located through the publisher page or GitHub repository search used in this audit.

The original addon has a public repository:

`Octo-Studios/reliquified-lenders-cataclysm`

but its current `1.21.1` branch metadata declares `mod_version=0.2`, while the physical original addon is `0.1.1`. That current source is therefore not promoted to exact installed-original internals and cannot substitute for missing fix source.

Only repository/version metadata was used to establish this mismatch; no original-addon implementation is imported into Black Arcana.

## What is deliberately not claimed

This audit does not claim:

- an exact fix source pin;
- exact mixin class/count/target inventory;
- exact transformation service or bytecode signatures;
- exact player-motion packet class or payload;
- exact Curios modifier UUIDs/keys;
- exact RelicTemplate IDs/data layout;
- exact XP/rank/cooldown persistence keys;
- source↔physical-JAR reproducibility;
- successful runtime execution in the full pack.

The physical modlist exposes a fix mixin config name, but a config filename alone is not enough to invent its entries or behavior.

## Semantic closure rationale

A source-level implementation inventory is unavailable, but the provider's semantic role is bounded by exact current publisher evidence:

- it is explicitly a compatibility bridge, not replacement content;
- 1.0.2 narrows transformations to the original addon's base class;
- the publisher enumerates the complete public fix families;
- the publisher enumerates exactly five affected existing relics;
- no new relic or spell identity is published as fix-owned content.

This is enough to close the **component identity/authority/deduplication surface** at the publisher evidence ceiling without pretending internal implementation closure.

## Clean-room / license

CurseForge marks the fix **All Rights Reserved**.

Black Arcana therefore uses only public behavior/release metadata and physical inventory for factual interoperability/cataloging. No fix code, bytecode, assets or proprietary data are copied or adapted.

Future interoperability that requires exact internal signatures remains fail-closed unless a legitimate supported public boundary is independently proven.

## Runtime QA still required

- dedicated-server startup with the exact physical stack;
- all five relics instantiated and equipped;
- no duplicate/stale Curios modifiers;
- XP/level/rank/cooldown persistence;
- active ability behavior on dedicated multiplayer;
- player-motion network synchronization;
- update/removal scenarios that detect double adaptation after upstream native support;
- verification that the 1.0.2 base-class restriction behaves as published in the physical JAR.
