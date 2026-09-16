# Sophisticated Backpacks: Ars Compat 0.3.0

Status: `EXACT PHYSICAL RELEASE ALIGNED TO OFFICIAL FILE 8653384 / ARS NOUVEAU↔SOPHISTICATED BACKPACKS COMPATIBILITY BRIDGE / PUBLISHER SURFACE CLOSED / 0 PROVIDER-OWNED SPELL-GLYPH-RITUAL IDENTITIES PUBLISHED / CATALOG CLOSED / RUNTIME QA FAIL-CLOSED`

## Installed identity

Physical pack authority records:

- JAR: `arssophisticatedcompat-0.3.0.jar`;
- mod id: `arssophisticatedcompat`;
- runtime version: `0.3.0`;
- loader/game: NeoForge / Minecraft 1.21.1;
- physical SHA-1: `7cc6c1e1d92d109230f68b6a63dc4bfb13c245a6`;
- physical CurseForge fingerprint/hash column: `2725765601`.

Independent current modpack indexing maps that exact filename and SHA-1 to CurseForge File ID `8653384`. The official CurseForge file page for project `1653477` independently identifies File ID `8653384` as `arssophisticatedcompat-0.3.0.jar`, release `0.3.0`, NeoForge 1.21.1, uploaded 2026-08-15.

This closes the installed release identity at the catalogue/provenance level. It does not claim that Black Arcana independently re-downloaded and byte-compared a fresh publisher copy in this checkpoint.

## Correction of the previous evidence model

The earlier catalogue compared the physical JAR against **Sophisticated Storage: Ars Compat** File ID `8655579`, filename `arssophisticatedstoragecompat-0.3.0.jar`, and therefore treated the installed artifact as a different byte artifact.

That comparison joined two distinct sibling projects:

- File `8653384` / `arssophisticatedcompat-0.3.0.jar` = **Sophisticated Backpacks: Ars Compat**;
- File `8655579` / `arssophisticatedstoragecompat-0.3.0.jar` = **Sophisticated Storage: Ars Compat**.

The installed provider is the **Backpacks** compat. The Storage compat remains a separate product and is not used as the binary authority for this folder.

## Exact publisher surface for File 8653384

The official 0.3.0 NeoForge 1.21.1 release describes a compatibility addon for Ars Nouveau and Sophisticated Backpacks with these gameplay-facing surfaces:

1. **Source Storage Upgrade** — stores Ars Source in a backpack, with capacity scaling through Sophisticated Stack Upgrades;
2. **Backpack Sourcelink upgrades** — convert eligible backpack contents into Source;
3. **Potion Jar Upgrade** — stores potion duration and maintains potion effects;
4. **Enchanter's Upgrade** — repairs enchanted items using stored Source;
5. Ars Nouveau-themed backpack upgrade templates and recipes.

The project description names Agronomic, Alchemical, Mycelial, Volcanic and Vitalic Sourcelink variants.

Publisher-declared required families are Ars Nouveau, Sophisticated Backpacks and Sophisticated Core. Exact host versions are not inferred here when the current physical snapshot does not expose them in this provider dossier.

## Semantic catalogue result

The exact release is an **upgrade/compatibility bridge**, not a spell school or casting provider. The publisher surface exposes storage/conversion/potion/repair upgrades and templates; it publishes no provider-owned standalone spell, glyph or ritual identities.

Catalogue consequence:

- standalone spells owned by this provider: **0**;
- glyph/spell-part identities owned by this provider: **0**;
- rituals owned by this provider: **0**;
- semantic magic identities added to the strict spell/action ledger: **0**.

This is a closed zero-semantic catalogue result at the accepted publisher/exact-release evidence level. It does not assert the absence of internal helper registries, item IDs or implementation classes; those belong to runtime/API inspection, not to the spell-identity count.

## Authority boundary

- Ars Nouveau owns Source identity/economy and Ars magical semantics.
- Sophisticated Backpacks/Core own backpack inventory, upgrades, stacking, persistence and container lifecycle.
- this compat owns only the bridge upgrades between those providers.
- Black Arcana must not mirror Source, duplicate repair/potion settlement, invent a second conversion loop or reinterpret an upgrade transaction as a Black Arcana cast.

## Runtime boundary

Catalog completion does **not** certify runtime compatibility. Exact classes, registries, configuration, networking, lifecycle hooks and full-pack behavior remain fail-closed until supported evidence or runtime QA establishes them.

See:

- [Functional contract](FUNCTIONAL-CONTRACT.md)
- [Transaction/lifecycle boundaries](TRANSACTION-LIFECYCLE.md)
- [Runtime QA gate](RUNTIME-QA.md)
