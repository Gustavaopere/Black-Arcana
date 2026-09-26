# KubeJS Ars Nouveau — 1.3.2

Status: `⚠️ PARTIAL / CURRENT PHYSICAL 1.3.2 / RECIPE-SCHEMA BRIDGE / 0 PROVIDER-OWNED SPELL OR GLYPH IDENTITIES / PACK SERVER-SCRIPT MUTATIONS UNVERIFIED / +0 STRICT`

## Current physical identity

Current sibling authority: `neoforge-rpg-skilltree@a0bf15c16f7e22eb42c4665bbe7a9dace8b8fda8`, revalidated against the current physical modlist on 2026-09-25.

- JAR: `kubejsarsnouveau-1.3.2.jar`;
- mod id: `kubejsarsnouveau`;
- runtime: `1.3.2`;
- Minecraft / loader: 1.21.1 / NeoForge;
- physical SHA-1: `f39f4f409e628731be551fd961fac2964768d358`;
- current KubeJS: `2101.7.2-build.377`;
- current Ars Nouveau: `5.13.1`.

Older physical Project Library snapshots also show `kubejsarsnouveau-1.3.2.jar`; the current sibling dossier is the newer authority for the current hash/stack.

## Official release

Official CurseForge project: `KubeJS Ars Nouveau` / project `833926`, MIT, Client & Server.

Exact current release:

- file id `7181937`;
- `kubejsarsnouveau-1.3.2.jar`;
- Release;
- NeoForge 1.21.1;
- published 2025-11-03;
- changelog: update to the latest KubeJS line.

## Public source boundary

Official repository: `BobVarioa/kjsarsnouveau` (historically redirected from `MasterOfBob777/kjsarsnouveau`).

Current public source HEAD inspected:

`18278a05d27def7200158a6d08516d5f22318e44`

Its `gradle.properties` still declares:

- `minecraft_version=1.21.1`;
- `mod_id=kubejsarsnouveau`;
- `mod_version=1.3.1`;
- KubeJS development baseline `2101.7.2-build.295`;
- Ars Nouveau file baseline corresponding to the source line.

No public commit/tag declaring `1.3.2` was located in the repository search used for this audit. Therefore source internals are treated as **1.3.1 baseline evidence**, while the physical/release identity is exact 1.3.2.

## Exact framework role established by source/docs

The public source plugin registers **recipe schemas**, not spell/glyph registries. The source baseline registers these six Ars Nouveau recipe types:

1. `ars_nouveau:enchanting_apparatus`;
2. `ars_nouveau:enchantment`;
3. `ars_nouveau:crush`;
4. `ars_nouveau:imbuement`;
5. `ars_nouveau:glyph`;
6. `ars_nouveau:caster_tome`.

The official 1.3.2 CurseForge documentation exposes the same recipe-customization scope for KubeJS `ServerEvents.recipes` and recipe replacement.

### Glyph boundary

`GlyphRecipeJS` is a recipe schema whose output is an item stack and whose inputs are ingredient lists plus XP. The official documentation warns that the glyph must already be a valid glyph present in the Ars tome; this API is appropriate for changing/replacing acquisition recipes, **not for registering a new glyph implementation**.

Therefore a scripted glyph recipe does not mint a new semantic spell/glyph identity. It changes reachability/cost for an Ars-owned glyph.

### Caster Tome boundary

`CasterTomeRecipeJS` accepts a tome type, display metadata and a list of string spell parts. A script can therefore package an Ars spell recipe into a custom tome/item recipe. The underlying spell parts remain Ars/provider identities; a tome item is not a new glyph/spell identity under the Black Arcana metric.

### Source / machine cost boundary

Enchanting Apparatus and Imbuement schemas expose Source-cost fields. Ars Nouveau remains authority for Source, machine execution, glyph validity, caster behavior and recipe settlement. KubeJS Ars Nouveau defines the data bridge only.

## Semantic disposition

Provider-owned standalone spell identities established by the bridge itself: **0**.

Provider-owned standalone glyph identities established by the bridge itself: **0**.

Script-defined recipe/tome customizations can materially change **availability, crafting cost and acquisition paths** of existing Ars magic, but the documented 1.3.2 framework does not expose a generic new spell/glyph registry surface.

Therefore:

- base framework semantic delta: **+0 strict**;
- current pack recipe/tome mutation inventory: **UNVERIFIED**;
- semantic identity count is not blocked by those scripts, but exact reachability/economy of affected Ars objects is;
- provider state: **⚠️ partial / conditioned** until the current `kubejs/server_scripts/**` set is audited.

## Historical pack-script evidence

Project Library logs from a physical boot on 2026-09-08 show KubeJS loading one startup script, `startup_scripts:main.js`, which logged the default `Hello, World!` example. That observation concerns **startup scripts** on an older pack checkpoint and does not prove the absence of `server_scripts` recipe mutations in the current pack.

Current physical authority now records KubeJS build 377, so historical script evidence is retained only as provenance.

## Closure path

See [`PACK-SCRIPT-CLOSURE-CHECKLIST.md`](PACK-SCRIPT-CLOSURE-CHECKLIST.md).

Current closure requires the exact present `kubejs/server_scripts/**` tree, or an equivalent bounded recipe-manager/runtime dump tied to the current pack.

## Authority boundary

- Ars Nouveau owns Source, glyph/spell implementations, spellbook/tome execution and Ars machines.
- KubeJS owns script lifecycle and recipe mutation execution.
- KubeJS Ars Nouveau owns the recipe schemas/serialization bridge.
- Pack scripts own the concrete recipe mutations they declare.
- Black Arcana must not create a parallel Source ledger, duplicate Ars machine settlement or reinterpret recipe existence as cast success.
- RPG Skill Tree may gate progression through real contracts but does not gain Ars/Black Arcana runtime authority from recipe scripts.

## Runtime QA remains fail-closed

Separate assembled checks include:

- dedicated-server boot with physical 1.3.2 + KubeJS build 377 + Ars 5.13.1;
- `/reload` idempotence and no duplicate/stale recipes;
- Enchanting Apparatus reagent/pedestal/Source-cost settlement;
- Imbuement Source cost;
- glyph recipe replacement only for intended existing glyphs;
- Caster Tome spell-part resolution;
- Crush outputs/chances without duplication;
- compatibility of exact 1.3.2 with a source tree that publicly remains at 1.3.1.

## Result

**⚠️ Partial / conditioned.**

KubeJS Ars Nouveau is cataloged as a recipe-schema bridge with **+0 provider-owned semantic spell/glyph identities**. The current pack's concrete recipe/tome mutations remain unverified and can affect Ars magic reachability/economy, but not the semantic numerator absent evidence of a separate registration API.
