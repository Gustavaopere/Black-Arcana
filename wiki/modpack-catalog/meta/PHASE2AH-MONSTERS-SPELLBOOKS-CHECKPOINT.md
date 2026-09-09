# Phase 2AH checkpoint — Monsters & Spellbooks 0.0.16.3

## State

`CATALOG CLOSURE CANDIDATE / NOT CANONICAL UNTIL MERGED`

## Base

- initial `main`: `2de722272814d2d5664266f5fc8ad05ba25d2940`
- branch: `docs/magic-catalog-phase2ah-monsters-spellbooks-0.0.16.3`
- canonical catalog coverage at branch creation: `36/100 = 36%`

The 37th point is awarded only after latest-main reconciliation, CI GREEN on the reconciled HEAD, review closure and merge.

## Physical provider identity

- artifact: `monstersspellbooks-0.0.16.3.jar`
- mod id: `monstersspellbooks`
- version: `0.0.16.3`
- SHA-1: `b3aa89fd081bf4bfaf8d0f4380bcdc393c66ab0e`
- CurseForge project/file: `1428928 / 8788560`
- exact release: `2026-09-01`, Minecraft 1.21.1 NeoForge

## Catalog closure

Current public source registry inventory:

- 98 explicit spell registrations;
- 5 blood;
- 12 ender;
- 3 evocation;
- 10 fire;
- 4 holy;
- 8 hydro;
- 8 ice;
- 14 lightning;
- 7 nature;
- 25 necro;
- 2 technomancy.

Provider-owned SchoolTypes observed in the current source:

- `monstersspellbooks:necro` — active provider school surface;
- `monstersspellbooks:aero` — retained school object, but exact 0.0.16.2 release says Aero is soft-deleted and current `ModSpellRegistry` has zero Aero registrations.

## Evidence layering

Exact:

- physical 0.0.16.3 artifact/version/hash;
- CurseForge exact 0.0.16.3 release identity and changelog;
- current official source head `1ab9b72af2ea44c3c8b816e665d06531ea44ddc2`;
- 98 registration calls at that source head;
- `ModSpellRegistry` unchanged in the public release-work interval from `823532a3...` to `1ab9b72a...`.

Explicit mismatch:

- inspected source `gradle.properties` still says `mod_version=0.0.14`;
- source dependency pins still say NeoForge 21.1.216 / Iron's 3.15.4;
- pack authority is NeoForge 21.1.248 / Iron's 3.16.3 / Monsters & Spellbooks 0.0.16.3.

Therefore exact 0.0.16.3 class signatures/numerics/config/network/save internals remain `NÃO VERIFICADO`.

## Architecture consequences

- Iron's remains host cast/mana/cooldown authority.
- Monsters & Spellbooks owns its spell/school/effect semantics.
- Black Arcana does not duplicate provider casting, resource settlement, summons, forms or mutations.
- provider Necro is not Black Arcana Corruption/Strain/Souls/Mastery by implication.
- destructive Black Arcana-owned effects continue through `WorldEffectPolicy`.
- retained Aero SchoolType is not counted as an active spell family.
- 98 provider spell identities are deduplication input, not 98 Black Arcana implementation gaps.

## Files in this phase

- `wiki/modpack-catalog/providers/monsters-spellbooks/README.md`
- `wiki/modpack-catalog/providers/monsters-spellbooks/SPELL-CATALOG.md`
- `wiki/modpack-catalog/providers/monsters-spellbooks/SCHOOLS-AND-AUTHORITY.md`
- `wiki/modpack-catalog/providers/monsters-spellbooks/RUNTIME-AND-SAFETY.md`
- `wiki/modpack-catalog/providers/monsters-spellbooks/EVIDENCE-AND-PROVENANCE.md`
- `wiki/modpack-catalog/meta/CAPABILITY-MATRIX-DELTA-MONSTERS-SPELLBOOKS.md`
- this checkpoint
- global coverage/queue ledgers

## Remaining exact-provider QA

The provider may be semantically catalog-closed while these binary/runtime questions remain explicitly deferred:

- exact installed-JAR registry paths and numeric spell config;
- exact 0.0.16.3 targeting/friendly-fire/claim semantics;
- exact summon/form cleanup and persistence behavior;
- real full-modpack runtime compatibility;
- any future Black Arcana runtime adapter/API contract.

None of those deferred items authorizes fabricated runtime integration.
