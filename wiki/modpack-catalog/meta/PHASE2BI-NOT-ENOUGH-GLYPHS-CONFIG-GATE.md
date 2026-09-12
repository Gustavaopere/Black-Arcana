# Phase 2BI — Not Enough Glyphs 4.6.1 config-authority checkpoint

Status: `CONFIG AUTHORITY CLOSED / DEPLOYED VALUES MISSING / SEMANTIC DELTA +0`

Base audited: `main@75558c92150506cce9f9b98b8f1ae29e4c128e62`.

## Physical/provider anchor

- installed JAR: `not_enough_glyphs-1.21.1-4.6.1.jar`;
- mod id/version: `not_enough_glyphs` / `4.6.1`;
- physical SHA-1: `e5fd04b7c40d6d5a9aea5d6356f3eb628941fca4`;
- embedded Sauce: `0.0.42.89`;
- Minecraft 1.21.1 / NeoForge `21.1.248`;
- physical modlist: 595 top-level entries, SHA-1 `7aaece7acbfb07ba4d0c66029042f36c50d046f0`.

Phase 2AF already closed the current-pack registration matrix: 40 NEG registrations, with `momentum` source-disabled and 39 remaining source-enabled candidates before external/user configuration. The stale Phase 2AD/2AF branches are ancestors of current `main` and contain no unmerged work.

## Exact config authority

Exact Ars Nouveau 5.13.1 source checkpoint `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` supplies the host contract used by NEG glyphs:

1. `GlyphRegistry.registerSpell(AbstractSpellPart)` invokes `part.buildConfig(...)`.
2. It registers that per-glyph spec as `ModConfig.Type.SERVER`.
3. It supplies filename `<namespace>/<path>.toml`; NEG glyphs therefore use `not_enough_glyphs/<glyph>.toml`.
4. Base `AbstractSpellPart.buildConfig(...)` defines `general.enabled` with source default `true`.
5. Base `isEnabled()` returns the resolved `ENABLED` config value.
6. NEG `momentum` independently overrides `isEnabled()` to false and remains excluded.

NeoForge 1.21.1 documents `SERVER` configs as server-authoritative/synchronized and allows per-world overrides in `<server_folder>/world/serverconfig`. Therefore the effective semantic gate is the deployed config set, including any world override; a code default cannot substitute for it.

## Evidence availability

The current uploaded/project material contains the physical modlist and provider/source documentation but no authoritative deployed `not_enough_glyphs/*.toml` server/world config set. Repository search likewise does not expose those deployed files.

Consequently Phase 2BI **does not promote the 39 candidates**. Canonical values remain:

- strict reconstructible semantic minimum: **1249**;
- provider-component coverage: **57/100**;
- Not Enough Glyphs conditional semantic candidates: **39**.

## Required evidence for promotion

Obtain the effective server configuration for all 39 candidate NEG IDs, including any per-world override. Reconcile `general.enabled` per glyph. Only proven-enabled rows may enter the strict semantic ledger; disabled rows remain excluded. If no valid explicit config exists for a row, the runtime fallback/default must be demonstrated from the actual deployed environment rather than inferred solely from source.

This checkpoint changes no Black Arcana runtime authority, Ars/NEG ownership, mana/casting settlement, or provider-component count.
