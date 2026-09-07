# Apprentice's Codex 0.9.7.1 — compatibility audit

Source checkpoint: `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`.

Pack identity checkpoint: physical modlist 2026-09-07.

## Rule

A compat package proves that Apprentice's Codex contains code for a provider. It does **not** prove that every seam is active or safe in the full modpack. Eligibility below means the required mod identity/version is present; runtime activation remains a separate QA gate where stated.

## Mandatory foundation

| Provider | 0.9.7.1 minimum/source baseline | Pack | Result |
|---|---|---|---|
| Iron's Spells 'n Spellbooks | `1.21.1-3.16.3`, `< 1.21.1-4.0.0` | `1.21.1-3.16.3` | exact core baseline |
| Iron's Lib | `1.21.1-2.1.0+` | `1.21.1-2.1.0` | exact minimum |
| GeckoLib | `4.8.3+` | `4.9.2` | version-eligible |
| Curios | `9.5.1+1.21.1+` | `9.5.1+1.21.1` | exact minimum |

These are mandatory provider dependencies, not Black Arcana adapters.

## Exact optional compat packages in the 0.9.7.1 source

The source tree contains compat packages for:

- Ars Nouveau;
- Better Combat;
- Botania;
- Create;
- Entity Model Features (EMF);
- Epic Fight;
- Iron's Gems 'n Jewelry;
- Jade;
- JEI;
- Lootr;
- Malum;
- Patchouli;
- Sable;
- Sodium Dynamic Lights.

## Pack reconciliation

### Present and version-eligible

- **Ars Nouveau 5.13.1** — exact source compat is limited to Luminous Device dynamic-light registration through Ars' light manager. It checks `ars_nouveau` at runtime and fails closed if reflective linkage fails.
- **Create 6.0.10** — exactly matches the provider's source baseline. Exact 0.9.7.1 compat surfaces include exposed-item processing, Linear Build sourcing from Create toolboxes, Magi Compressor air integration and endgame-armor compatibility.
- **Sable 2.0.5** — newer than the source development baseline 2.0.3. The provider declares Sable optional from 2.0.3 upward; exact behavior in the pack still requires runtime QA because the installed minor line differs.
- **Create Simulated / Aeronautics / Offroad 1.3.2** — embedded in the installed Aeronautics bundle and newer than the source optional minimum 1.3.0. Eligibility is satisfied; behavior remains provider-owned.
- **Lodestone 1.8.2 + Malum 1.8.2** — match the source baselines. The exact source contains Malum bridges, including Linear Build pouch sourcing and combat/item-specific seams.
- **Atlas API 1.21.1-1.2.0 + Iron's Gems 'n Jewelry 1.21.1-2.0.2** — exact source baselines and pack versions match.
- **Epic Fight 21.17.3.1** — exact source baseline and pack version match.
- **Jade 15.10.6** — above source minimum `15.10.5+neoforge`; client compat eligible.
- **JEI 19.53.0.425** — present; provider declares JEI optional without a restrictive lower version beyond availability in metadata.
- **Lootr 1.21.1-1.11.38.125** — above the source development baseline `1.21.1-1.11.37.118`; exact source contains a Treasure Divination compat bridge.
- **Patchouli 1.21.1-93-NEOFORGE** — exact source baseline.
- **Entity Model Features 3.3.5** — above source minimum `3.2.4`; client compat eligible.

### Absent in the current pack

- **Better Combat** — no top-level/runtime provider found in the physical modlist; its Apprentice compat is dormant.
- **Botania** — no top-level/runtime provider found in the physical modlist; its Apprentice compat is dormant.
- **Sodium Dynamic Lights (`modId=sodiumdynamiclights`)** — the pack has Sodium and LambDynamicLights, but not the exact `sodiumdynamiclights` mod id required by this 0.9.7.1 compat class. Therefore that direct integration is **inactive**. It must not be inferred from the presence of Sodium alone.

The pack's Luminous Device can still use the separate Ars Nouveau dynamic-light compat because `ars_nouveau` is present.

## Critical integration boundaries

### Create / Linear Build

Linear Build may discover additional block sources through the provider's Create-toolbox bridge. This extends where Apprentice obtains items; it does not transfer Create inventory authority to Black Arcana and does not authorize a second item-consumption pass.

### Lootr / Treasure Divination

Lootr-specific treasure recognition remains a provider-local adapter for the Apprentice spell. A Black Arcana divination bridge must not separately reward or rediscover the same container from duplicate callbacks.

### Epic Fight

The provider contains Epic Fight-specific swing/casting support and data resources. Combat animation/input integration does not make Epic Fight the authority of Apprentice mana, spell cooldowns or spell registry state.

### Malum

Malum bridges are optional, provider-scoped interoperability. Similar occult theme does not turn Malum spirits into Black Arcana Corruption/Strain resources.

### Sable/Aeronautics

Physical/sublevel compatibility is an environment adapter. Black Arcana must not assume provider targets or world positions can be consumed unchanged across level/sublevel boundaries unless the exact provider seam exposes a safe resolved result.

## Fail-closed rule

When a provider is absent, below the declared range, uses a different mod id, or fails linkage/runtime QA, disable only the dependent compat surface. Never substitute a thematic equivalent, duplicate a resource, or grant a free effect.

## Confidence

`SOURCE-PINNED COMPAT PACKAGE INVENTORY / MODLIST VERSION RECONCILIATION COMPLETE / CORE BASELINE MATCHES / SELECT OPTIONAL SURFACES VERSION-ELIGIBLE / FULL 612-MOD RUNTIME QA STILL REQUIRED`