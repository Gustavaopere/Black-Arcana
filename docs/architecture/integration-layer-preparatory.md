# Stage 03 — Integration Layer Preparatory Audit

This document records the implementation state of the preparatory integration layer. It is not canonical until the project promotion gates execute successfully.

## Architecture

Black Arcana owns the integration contracts and capability vocabulary. Optional-mod binary references are isolated behind provider-specific packages and reflectively loaded only after NeoForge confirms the provider mod is present. Missing or incompatible providers are represented explicitly through `ArcanaIntegrationAvailability`; they do not silently disappear and never convert a provider-backed spell into a free cast.

## Iron's Spells 'n Spellbooks

The adapter uses the published addon-facing API classifier. Iron's is treated as the preferred host for conventional active Black Arcana spells when its registration surface is compatible. Mana consumption remains a Black Arcana transaction, and provider capability advertisement is conditional on successful API probing.

Baseline: `1.21.1-3.16.3`.

## Ars Nouveau

Ars does not publish a standalone API classifier for the required mana surface, so Black Arcana compiles against the exact installed-pack release with transitives disabled and isolates all Ars binary references in its optional adapter package.

Installed-first baseline: `5.13.0` (CurseForge file `8517890`). `5.13.1` is treated as a newer compatibility target rather than the build baseline.

The synthetic acceptance spell reserves 25 Ars mana, commits it exactly once on successful execution and relies on the canonical Black Arcana cooldown service. An immediate recast is denied before a second resource debit.

Capabilities: `RESOURCE_COST`, `SOURCE_RESOURCE` when the probe is usable.

## Malum

Malum spirits are modeled as discrete typed inventory resources rather than a fabricated mana pool. The provider resolves canonical spirit item ids, performs bounded integer reserve/commit/refund accounting and restores partially removed items if an unexpected inventory mutation prevents the full debit.

The synthetic acceptance spell proves exactly-once spirit consumption plus canonical cooldown denial on immediate recast.

Capabilities: `RESOURCE_COST`, `SOUL_RESOURCE` when usable.

## Eidolon: Repraised

The exact 1.21.1 source exposes `alexthw.eidolon_repraised.api.ritual.Ritual` and public `RitualRegistry.register(ResourceLocation, Ritual)`. Eidolon's `GenericRitualRecipe` resolves a registered ritual by id and the generated recipe format uses `eidolon_repraised:ritual_brazier`.

Black Arcana therefore registers a non-destructive `black_arcana:eidolon_integration_probe` through the public ritual API. Its recipe is guarded by `neoforge:mod_loaded` so the core-only datapack path never attempts to deserialize an Eidolon recipe type.

The server-visible descriptor contains no Eidolon binary types. The real registry check is supplied by the optional bootstrap only after the provider is known to be loaded. A missing registration or linkage failure yields `API_INCOMPATIBLE` and advertises no capability.

Baseline: `1.21.1-0.5.0.2` (CurseForge file `8064602`).

Capability: `RITUAL_HOST` only after the probe ritual is confirmed registered.

## RPG Skill Tree

The RPG integration is reflection-isolated because the project is private/unpublished and therefore cannot currently provide a reproducible public Maven dependency. The probe freezes the required runtime/query/attribute/mastery method surface before advertising `PROGRESSION_QUERY` or `MASTERY_AWARD`.

Black Arcana uses the dynamic mastery lane `black_arcana:casting`. RPG `MasteryState` accepts arbitrary non-blank lane ids, so this does not require a hard-coded lane addition to the RPG mod. Mastery is awarded only after meaningful successful Black Arcana execution; the integration must not create recursive XP feedback.

## Optional dependency policy

Provider declarations in `neoforge.mods.toml` are optional and ordered `AFTER`. Runtime compatibility is not inferred from a broad version range; each adapter decides compatibility through its actual API probe.

- missing provider -> `MISSING_MOD`, no capabilities;
- loaded provider with failed binary/API probe -> `API_INCOMPATIBLE`, no capabilities;
- missing resource provider never makes a spell free;
- mod-bus failures are carried forward into server startup diagnostics;
- server adapter linkage/install failures become explicit unavailable descriptors;
- provider-specific recipes must be conditionally hidden when their serializer/type would not exist.

## Verification status

Source-level contract tests now cover Ars and Malum transactional probes, Eidolon descriptor behavior, Eidolon recipe conditioning and generic unavailable-provider semantics. Compilation of the Eidolon registration code against the pinned release is also a binary contract check.

Still required before Stage 03 can be canonical:

1. a real GitHub Actions runner must execute JUnit, build, GameTest and dedicated-server steps;
2. installed-provider runtime profiles should eventually boot representative Iron's/Ars/Eidolon/Malum combinations rather than relying only on compile/probe contracts;
3. the canonical Stage 00 -> 01 -> 02 promotion order must be resolved before Stage 03 can move `main`.
