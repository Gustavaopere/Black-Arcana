# Ignis Soulfires: Spellbooks 1.1.0 — exact artifact audit

## Status

`EXACT PHYSICAL / EXACT CURSEFORGE FILE / HASH-MATCHED / ARR / BRIDGE_COMPAT + GEAR_LOOT_SUPPORT / ZERO INDEPENDENT SEMANTIC MAGIC / COMPONENT CLOSURE ELIGIBLE`

## Exact artifact identity

- installed JAR: `ignissoulfires_spellbooks-1.1.0.jar`
- mod id: `ignissoulfires_spellbooks`
- runtime version: `1.1.0`
- physical SHA-1: `dcde77db35b6de3562b4e6de0025746eaf68f119`
- exact CurseForge project/file: `1572171 / 8620663`
- exact artifact metadata license: `ARR`
- artifact SHA-256: `27d9270a4b718be50fe30accbd231dff824bb9b2bd14117ce1c081f731c77704`
- artifact size: `835691` bytes
- audit base: `main@fa14b75bf08482031e4fabbc779d30d295e22c5e`
- isolated NON-MERGE evidence PR: `#203`
- audit HEAD: `ed807b77345cde1803767d804e26ea972c41d964`
- evidence run: `34688273425` — GREEN
- text-only evidence artifact: `10296406134`
- evidence digest: `sha256:5e96a319aea648aadf2c70bdf9b870a26a9503068307befc8a9972bb7b1cd52e`

The audit materialized the exact publisher file and hard-failed unless its SHA-1 matched the physical modlist. The ARR JAR itself was not uploaded or persisted as evidence.

## Exact structural inventory

The hash-matched 1.1.0 artifact contains **11 provider classes total**. Signature-level inspection closes these provider-owned surfaces:

- bootstrap/mod entrypoint;
- client setup;
- two armor renderers and one item animator;
- one armor-material registry class;
- two armor item classes;
- one creative-tab event class;
- one creative-tab/layout plugin;
- one item registry class.

The provider registry surfaces are:

- one `DeferredRegister<ArmorMaterial>` with the Souled Ignitium Wizard armor material;
- one `DeferredRegister.Items` with exactly **five item holders**: helmet, chestplate, elytra chestplate, leggings and boots.

The two provider item classes extend Cataclysm: Spellbooks' imbuable armor substrate. One of them also exposes the normal elytra-flight item hooks. Those are equipment behaviors, not standalone player-action identities under the semantic ledger.

## Negative semantic-registry closure

Across every provider class in the exact artifact, clean-room constant-pool and signature inspection finds:

- `AbstractSpell`: **0 class hits**;
- `registerSpell`: **0 class hits**;
- `SpellRegistry`: **0 class hits**;
- `Ritual`: **0 class hits**;
- `Rite`: **0 class hits**;
- `Ability`: **0 class hits**.

The only `DeferredRegister` class hits are the armor-material and item registries above.

Packaged data under the provider consists of item tags and equipment upgrade/fusion/smithing recipe resources. No provider spell/ritual/action data registry is present in the archive.

This is an exact-artifact negative inventory, not an inference from publisher prose.

## Semantic accounting

The semantic ledger excludes items, gear, passive equipment behavior, recipes and downstream consequences of equipment ownership. The exact 1.1.0 artifact therefore contributes:

- standalone spells: **0**;
- glyph/spell-part primitives: **0**;
- rituals/rites: **0**;
- equivalent discrete supernatural player actions: **0**;
- total independent semantic magic objects: **0**.

Disposition: **`ZERO_BRIDGE_INFRA`** for semantic accounting, with provider classification **`BRIDGE_COMPAT + GEAR_LOOT_SUPPORT`**.

The global strict semantic minimum remains **1250**. This closure does not create or remove a semantic identity from another provider.

## Authority and deduplication

- Cataclysm: Ignis Soulfires remains authority for Souled Ignitium and its base material/equipment semantics.
- Cataclysm: Spellbooks / Iron's remain authority for their spellcasting substrate and provider-owned magic registries.
- Ignis Soulfires: Spellbooks owns the five exact compatibility armor items/material registration it actually contributes.
- Black Arcana must not duplicate armor modifiers, spell modifiers, elytra state, provider materials, casting state or resource settlement merely because this bridge participates in those ecosystems.

No Black Arcana runtime adapter is approved by this catalog closure.

## Clean-room boundary

The exact artifact declares All Rights Reserved, and current publisher surfaces also identify the project as ARR. Binary inspection was restricted to cryptographic identity, metadata/resource paths, class/member/type signatures and narrow registry type/count facts.

No implementation bodies, recipe ingredient payloads, localization prose, textures, models, animations, sounds or other upstream creative assets are copied/adapted into canonical Black Arcana documentation or runtime. The exact JAR is not redistributed.

## Remaining QA

The semantic/component catalog can close independently of these runtime questions:

- numerical armor/spell modifiers;
- equip/unequip/relog idempotence;
- Cataclysm/Ignis/Iron's ABI behavior;
- elytra/render lifecycle;
- actual client/server regression in the full pack;
- any future supported provider API seam.

All remain fail-closed unless separately proven.
