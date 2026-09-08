# Provider Audit Queue Delta — Phase 2P Ars Nouveau

## Overlay rule

This file is a narrow status overlay over `PROVIDER-AUDIT-QUEUE.md`. It changes only the `ars_nouveau` row. It does not rewrite or reorder the 103-provider canonical queue.

## `ars_nouveau`

Canonical physical identity:

- provider: Ars Nouveau;
- mod id: `ars_nouveau`;
- JAR: `ars_nouveau-1.21.1-5.13.1.jar`;
- runtime: `5.13.1`;
- exact source pin: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`;
- code license at exact pin: GNU LGPL v3;
- assets at exact pin: All Rights Reserved unless otherwise stated/permission granted.

Previous queue state:

`BASE PROVIDER / GLYPH CATALOG PENDENTE`

Phase 2P overlay state:

`SOURCE-PINNED 5.13.1 / CORE SPELL PARTS 85/85 + ACQUISITION 85/85 / RITUALS 24/24 / FAMILIARS 6/6 / PERKS 20/20 + ARMOR SLOT PROVIDERS 12/12 / PROVIDER SYSTEMS AUDITED / RUNTIME+CONFIG+CLAIM+CLIENT+FULL-PACK QA PENDING / ADDON PROVIDERS SEPARATE`

## Evidence completed

- exact current physical provider identity/version;
- exact 5.13.1 source pin and clean-room license boundary;
- 5/5 Forms, 67/67 Effects and 13/13 Augments;
- 85/85 generated Glyph acquisition recipes/default recipe XP/starter-learning boundaries;
- 24/24 Rituals;
- 6/6 Familiars;
- 20/20 Perks/Threads;
- 12/12 armor perk-slot providers and Tier I/II/III slot layouts;
- Source vs player-mana authority split;
- spell composition/continuation/child-context authority;
- major Black Arcana overlap/deduplication disposition.

## Explicitly not closed

- effective modpack config values;
- claim/protection equivalence for every world-mutating Effect;
- client VFX/render/accessibility behavior;
- cross-mod event ordering and provider-addon activation;
- future runtime integration API seam;
- dedicated-server/full 612-entry modpack runtime QA;
- any Ars addon row other than `ars_nouveau`.

## Selection rule after Phase 2P

This overlay does **not** preselect the next provider. After merge, the next checkpoint must re-read current `main`, the physical modlist, Notion, full queue and concurrent branches/PRs. Ars addon providers remain separate queue rows and must not inherit core-complete status.
