# Alshanex's Familiars 4.0.3 — exact artifact audit

## Purpose

Close the current spell/ritual **identity inventory** against the exact physical 4.0.3 artifact without treating All Rights Reserved implementation as reusable source material.

## Artifact identity

- physical JAR: `alshanex_familiars-1.21.1_v4.0.3.jar`
- mod id: `alshanex_familiars`
- CurseForge project/file: `1171602 / 8675568`
- expected physical SHA-1: `e5051c2385a426d05bf203ba8081a23d891f6686`
- isolated audit download SHA-1: `e5051c2385a426d05bf203ba8081a23d891f6686` — exact match
- audit run/job: `34649305941 / 103427464735`
- text-only audit artifact: `10283338450`

The audit materialized the file from the Curse Maven coordinate for the exact publisher File ID, then required the SHA-1 equality check to pass before any inventory inspection.

## Spell registry facts retained

Read-only factual inspection retained only:

- `PetSpellRegistry` declares one `DeferredRegister<AbstractSpell>`;
- seven `Supplier<AbstractSpell>` spell fields exist;
- the static initializer assigns all seven through **7** `registerSpell` calls;
- the initializer has **0 conditional branch instructions** in the narrow registration check;
- exact provider classes and filtered literal IDs map 1:1 to seven current spell IDs.

No spell method body, formula, effect implementation or source reconstruction is retained.

## Ritual resource facts retained

Archive/resource inspection found **11** JSON resources under the provider namespace whose exact type is `alshanex_familiars:ritual_recipe`. For each, the catalog retains only the recipe identity and result ID. The provider's public Wiki independently establishes that this is its player-facing ritual subsystem rather than ordinary crafting nomenclature.

## Clean-room boundary

This audit does **not** authorize implementation reuse. The project is treated as All Rights Reserved. Black Arcana copies/adapts no upstream code, assets, models, sounds or prose. Binary inspection is limited to factual interoperability/catalog evidence required to identify current registrations and avoid semantic duplication.

## Result

- exact current provider-owned spells: **7**;
- exact packaged provider ritual identities: **11**;
- semantic magic objects admitted by the ledger: **18**;
- Sound/Melodic content: **0 additional Alshanex identities** because current ownership migrated to Tunes n' Tomes;
- runtime QA/API adapter status: still separate and fail-closed where unverified.
