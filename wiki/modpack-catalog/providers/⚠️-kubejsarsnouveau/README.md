# kubejsarsnouveau — 1.3.2

Status: `⚠️ PARTIAL / CURRENT PHYSICAL 1.3.2 / PUBLISHER RELEASE-LINE SOURCE AUDITED / RECIPE-SCHEMA BRIDGE / 0 FIXED GLYPH IMPLEMENTATIONS ESTABLISHED / CURRENT PACK SCRIPT TREE UNVERIFIED / FAIL-CLOSED`

## Current physical identity

Current sibling authority considered: `neoforge-rpg-skilltree@8fd5997c5dab1e038794009712e77271fa3cb0aa`.

Current physical pack evidence:

- JAR: `kubejsarsnouveau-1.3.2.jar`;
- mod id: `kubejsarsnouveau`;
- runtime version: `1.3.2`;
- Minecraft / loader: 1.21.1 / NeoForge;
- physical SHA-1: `f39f4f409e628731be551fd961fac2964768d358`;
- current Ars Nouveau host in the Black Arcana current provider registry: `5.13.1`;
- current KubeJS host: `2101.7.2-build.377`.

CurseForge project 833926 publishes file **7181937** as `kubejsarsnouveau-1.3.2.jar` for Minecraft 1.21.1 / NeoForge, uploaded 2025-11-03. The publisher changelog for that file points to upstream PR #9 ("Update to latest KubeJS").

## Source provenance

Official repository: `BobVarioa/kjsarsnouveau`.

Public 1.21.1 release-line checkpoint used for framework inspection:

`BobVarioa/kjsarsnouveau@18278a05d27def7200158a6d08516d5f22318e44`

The public history from the initial 1.21.1 update is linear:

- `158140e9...` — Update to 1.21.1;
- `9e3359fe...` — updates to latest KubeJS;
- `661ca4f0...` — adds bindings for custom components and bumps source metadata to 1.3.1;
- `b3589e5a...` — removes those bindings;
- `18278a05...` — fixes list components that may be empty.

Important provenance limit: the public repository at `18278a05...` still declares `mod_version=1.3.1`, while the published/installed artifact reports 1.3.2. The CurseForge 1.3.2 changelog points to PR #9, but no public commit with `mod_version=1.3.2` was found. Therefore this is a **publisher release-line source checkpoint**, not a physical-JAR↔source byte-equivalence claim.

The physical fingerprint is handled independently by the deployed-evidence collector.

## Framework disposition

The audited release-line source exposes:

- **3** KubeJS recipe component types;
- **6** Ars Nouveau recipe schemas;
- **0** active KubeJS bindings;
- **0** KubeJS registry-builder registrations;
- **0** provider KubeJS event groups/handlers;
- **0** fixed provider-owned glyph implementations established by this addon.

See [`RELEASE-LINE-1.3.2-FRAMEWORK-SURFACE.md`](RELEASE-LINE-1.3.2-FRAMEWORK-SURFACE.md).

This bridge is a recipe/customization adapter. It does not expose a script builder for Ars `AbstractSpellPart` or another glyph implementation registry in the audited release line.

## Semantic disposition

### Base addon

Strict semantic contribution from the bridge itself: **+0**.

The six recipe schemas can create or mutate recipes that refer to existing Ars content. In particular, the `ars_nouveau:glyph` schema can create glyph recipes and the `ars_nouveau:caster_tome` schema can encode spell/glyph sequences in a tome recipe. Those are recipe/acquisition/preset surfaces; they do not by themselves create a new glyph implementation.

### Current pack scripts

The exact current assembled `kubejs/` tree remains **UNVERIFIED**.

Current repository/Library searches did not expose an authoritative build-377 script tree. Available historical boot evidence belongs to the 2026-09-08 KubeJS build-374 instance and cannot be propagated to the later build-377 physical pack.

Consequently:

- new semantic glyph implementations attributable solely to this bridge: **0 established**;
- current-pack recipe/acquisition mutations made through this bridge: **UNKNOWN**;
- current-pack caster-tome definitions made through this bridge: **UNKNOWN**;
- global strict semantic denominator delta from the base addon: **+0**.

See [`CURRENT-EVIDENCE-2026-10-04.md`](CURRENT-EVIDENCE-2026-10-04.md) and [`PACK-SCRIPT-CLOSURE-CHECKLIST.md`](PACK-SCRIPT-CLOSURE-CHECKLIST.md).

## Authority boundary

- Ars Nouveau owns glyph implementations, spell composition semantics, Source and its runtime.
- KubeJS owns script execution and recipe mutation lifecycle.
- kubejsarsnouveau owns recipe components/schemas that adapt KubeJS to Ars recipe formats.
- Pack scripts own any recipe changes they declare.
- Black Arcana must not treat a recipe schema as a spell/glyph implementation authority.
- RPG Skill Tree receives no casting/runtime authority from this bridge.

## Current result

**⚠️ Partial / conditioned.**

The base addon is cataloged as a zero-semantic recipe bridge. Physical 1.3.2 identity is known; exact current pack recipe/script mutations still require assembled-instance script evidence.

Strict semantic delta from the base framework itself: **+0**.
