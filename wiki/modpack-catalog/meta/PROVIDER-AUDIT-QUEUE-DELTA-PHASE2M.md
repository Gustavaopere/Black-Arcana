# Provider Audit Queue Delta — Phase 2M

Date: `2026-09-07`

This narrow overlay prevails only for `cataclysm_spellbooks` until the integral provider queue is regenerated. It does not alter unrelated provider rows.

Base reconciliation before Phase 2M: `main@4f45a0a1a3442d75fc11b2d5e6186848870377a5`.

| Mod id | Installed JAR/version | Classification | Phase 2M status | Evidence completed | Remaining gate |
| --- | --- | --- | --- | --- | --- |
| `cataclysm_spellbooks` | `cataclysm_spellbooks-1.1.13-1.21.jar` / `1.1.13-1.21` | `SPELL PROVIDER / CONTENT ADDON` | `CURRENT ARTIFACT IDENTITY + PROVIDER SCALE VERIFIED / PUBLIC 1.1.11-LABELLED SOURCE BASELINE CATALOGED / EXACT 1.1.13 SPELL TABLE PENDING` | physical modlist identity; CurseForge File ID `8792628`, Beta, NeoForge 1.21.1, 2026-09-02; current publisher claim of 65 spells; Abyssal + Technomancy current provider-school claim; public source commit `82a0af71f051058fe515c8b1cb9168e7f972f41c` pinned as **non-current baseline**; 34 concrete old-source registrations enumerated; old-source Abyssal/Technomancy/Sand school registry recorded; clean-room/provenance boundary recorded | exact 1.1.13 JAR/resource inspection; exact current 65 spell IDs/school distribution/config values; current acquisition/items/entities/effects/new boss; runtime/full-pack QA; any supported integration API/hook |

## Promotion achieved

Before this delta, the queue row correctly said that 1.1.13 was installed while the public source was only 1.1.11 and current-JAR extraction was pending.

Phase 2M advances that row by making the old-source boundary useful without weakening it:

- the public 1.1.11-labelled snapshot is pinned to one commit;
- exactly 34 concrete registrations are separated from WIP comments;
- provider-owned school structure is recorded;
- current publisher-level 65-spell scale is separated from exact registry evidence;
- the numerical gap between 65 and 34 is recorded as a scale difference, **not** an inferred 31-ID release diff;
- authority/deduplication consequences are explicit;
- license/source-reuse posture is fail-closed.

## Current exactness ceiling

The 1.1.13 publisher file page proves artifact metadata and a coarse changelog, not the full registry. The linked public repository still declares `mod_version=1.1.11-1.21`.

Therefore Phase 2M does **not** mark `cataclysm_spellbooks` `DONE`, `SOURCE-PINNED CURRENT`, `65/65 CATALOGED`, or runtime-validated.

**PENDÊNCIA — REQUER ARTEFATO EXATO / NAVEGAÇÃO EXTERNA CAPAZ DE ENTREGAR O BINÁRIO**

## Phase 3 consequence

Until the exact installed spell table is resolved:

- Infernal cannot use a presumed gap against provider Fire/Ignis content;
- Order cannot use a presumed gap against current Technomancy;
- Chaos cannot use presentation alone to claim uniqueness against Cataclysm boss-derived magic;
- new Space/Displacement or summon/familiar candidates must account for the baseline-confirmed Void/gravity/summon occupancy and remain open to additional 1.1.13 overlaps.

This is a fail-closed semantic gate, not a request to transfer provider authority into Black Arcana.