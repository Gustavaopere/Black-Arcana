# Cataclysm: Spellbooks 1.1.14 — current-release registry revalidation

## Purpose

Revalidate the current physical Cataclysm: Spellbooks version after the pack advanced from 1.1.13 to 1.1.14, without importing the publisher's generic **65 spells** project claim as a registry count.

## Current physical authority

The current sibling modlist/dossier at `neoforge-rpg-skilltree@49d9910ca0abfb9c0608c2730ab3ae8cefc59a9a` identifies:

- physical JAR filename: `cataclysm_spellbooks-1.1.14-1.21.jar`;
- mod id: `cataclysm_spellbooks`;
- runtime version: `1.1.14-1.21`;
- Minecraft / loader: 1.21.1 / NeoForge.

The current sibling dossier preserves physical SHA-1 `568d798862a61a374ab1e55dcddf5b2e3326b8b5` for the installed 1.1.14 JAR. That value is identical to the SHA-1 of exact publisher File `8847070` audited below, so installed-pack ↔ publisher-file byte equality is closed.

## Exact publisher release

Official CurseForge file:

- project: `1099461`;
- file: `8847070`;
- filename: `cataclysm_spellbooks-1.1.14-1.21.jar`;
- channel: Beta;
- uploaded: 2026-09-09;
- exact audit SHA-1: `568d798862a61a374ab1e55dcddf5b2e3326b8b5`;
- exact audit SHA-256: `a5a0dcad537954f488c862b3409831e0d12b4dfdc50bbfade298cb3d05dff2cf`.

The official 1.1.14 changelog only states:

- a way to obtain the Strange Disc was added;
- manuscripts can be brewed into 500 mB of Timeless Slurry.

It does not publish a new spell registry list or claim that new spell registrations were added in 1.1.14.

## Exact binary delta against the hash-matched 1.1.13 control

Temporary clean-room audit commit:

- branch checkpoint: `a9387be4ac93497495e699eda7c32240b9e997a2`;
- push CI run: `3375` / `35786067439`;
- step: `Temporary Cataclysm Spellbooks 1.1.14 binary delta audit NON-MERGE`;
- step conclusion: **SUCCESS**.

The audit first materialized exact Curse Maven 1.1.13 File `8792628` and required its SHA-1 to equal the already-canonical physical hash:

`4af8348cc77bbff2ab7057c1fac26a5ab0a5b6a2`.

Only after that control check did it compare 1.1.13 with publisher File `8847070`.

### Registry class

Both releases contain:

`net/acetheeldritchking/cataclysm_spellbooks/registries/SpellRegistries.class`

SHA-256 in 1.1.13:

`8c4f8570d832a2a178e2d35244729eacd3208ccb4e9df582a16a01976a4881c7`

SHA-256 in 1.1.14:

`8c4f8570d832a2a178e2d35244729eacd3208ccb4e9df582a16a01976a4881c7`

Result:

`CATACLYSM_REGISTRY_CLASS_IDENTICAL=true`

The exact registry class is byte-for-byte unchanged.

### Spell-related class surface

The bounded class-path comparison found:

- 1.1.13 spell-related class paths: **225**;
- 1.1.14 spell-related class paths: **225**;
- added: **0**;
- removed: **0**.

This is supporting structural evidence. The registry-class equality remains the controlling spell-registration fact.

### Root localization identities

For exact root keys matching `spell.cataclysm_spellbooks.<id>`:

- 1.1.13: **69**;
- 1.1.14: **69**;
- added: **0**;
- removed: **0**.

Therefore the ten translation-only/WIP-or-residual roots already excluded in 1.1.13 remain excluded in the exact 1.1.14 release.

## Registry consequence

The hash-matched 1.1.13 audit had already closed the unchanged `SpellRegistries.class` at:

- **59** `Supplier<AbstractSpell>` spell fields;
- **59** `registerSpell(...)` calls;
- **59** registered provider spell identities;
- **0** conditional branches in the narrow static registration audit.

Because the exact 1.1.14 publisher release contains the **identical registry class bytes**, the exact registered spell identity set remains **59/59** in 1.1.14. The current table is versioned in [`EXACT-1.1.14-SPELL-INVENTORY.md`](EXACT-1.1.14-SPELL-INVENTORY.md).

No spell is added merely because the current project description says **65 new spells**.

## Evidence classification

For the current pack version:

- version/JAR filename: exact physical authority from the sibling modlist;
- publisher binary: exact File `8847070`, cryptographically fingerprinted;
- registry identity/count: exact for the publisher 1.1.14 release;
- physical pack byte equality: **closed** — current sibling SHA-1 `568d798862a61a374ab1e55dcddf5b2e3326b8b5` exactly matches audited publisher File `8847070`;

Accordingly the current semantic inventory is `COUNTED_EXACT` for the installed physical 1.1.14 artifact.

This distinction does not change the semantic count: Cataclysm: Spellbooks remains **59** registered spells in the current-version catalog.

## CI note

Run #3375 later failed in the unrelated Foundation GameTest `throughputandplayerconsentareenforcedbeforemovement`. The Cataclysm audit step itself completed successfully before that failure. That run is evidence for the isolated binary audit only, not a green durable-branch CI claim.

Final repository validation must be performed again after the temporary audit fixture is removed.

## Clean-room / license boundary

Inspection was restricted to:

- cryptographic digests;
- archive/class paths;
- exact class-byte equality for the registry class;
- bounded class-path set comparison;
- localization root-key set comparison.

No implementation body, reconstructed source, assets, models, sounds or upstream prose are copied into Black Arcana.
