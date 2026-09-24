# Enchantment Descriptions — 21.1.11

Status: `CATALOGED / PHYSICAL SHA-PINNED / EXACT PUBLISHER RELEASE / RELEASE-CORRELATED 1.21.1 SOURCE / CLIENT PRESENTATION ONLY / +0 STRICT SEMANTIC MAGIC / RUNTIME UI QA FAIL-CLOSED`

## Current physical identity

Current sibling authority:

`neoforge-rpg-skilltree@d7c99d23ef1b38fe62c86a362ec521ced8861f96`

Certified dossier:

`PROJECT-INSTRUCTIONS/modlist/Cosmetic + Magic + Map and Information + Utility & QoL/✅-enchantment-descriptions v21.1.11.md`

Physical identity:

- order: **#250** in the current 587-top-level snapshot;
- JAR: `enchdesc-neoforge-1.21.1-21.1.11.jar`;
- mod id: `enchdesc`;
- runtime: `21.1.11`;
- SHA-1: `4d453df785ac21e0e7389cba949f4fa460c3e267`;
- Minecraft 1.21.1 / NeoForge.

## Exact publisher release

CurseForge project: `250419`.

Exact NeoForge 1.21.1 release:

- file ID: `8693034`;
- filename: `enchdesc-neoforge-1.21.1-21.1.11.jar`;
- uploaded: 2026-08-20;
- type: Release;
- size: about 80.7 KiB;
- published change: fixes Sweeping Edge description in various languages.

The same 21.1.11 release is also published on Modrinth for NeoForge 1.21.1 and requires Bookshelf + Prickle.

## Source authority and precision

Official source:

`Darkhax-Minecraft/Enchantment-Descriptions`

Current official branch for this Minecraft line:

`1.21.1`

Important precision boundary:

- the branch declares project base version `21.1`, not a literal immutable `21.1.11` tag;
- the branch is current for the 1.21.1 line and was updated on the same 2026-08-20 release date;
- therefore it is used as **release-correlated source**, not as a claimed byte-exact source pin for the installed JAR.

The branch explicitly declares:

`mod_client_only=true`

and describes itself as adding descriptions of enchantment effects.

## Runtime surface

The common implementation `EnchdescMod`:

- initializes client config only on a physical client;
- checks whether an item stack has enchantments;
- optionally limits display to enchanted books or the enchanting-table screen;
- optionally requires Shift;
- obtains the existing enchantment `ResourceKey`;
- searches localization entries using the existing enchantment namespace/path;
- accepts translated text into tooltip lines.

Observed localization suffixes are:

- `desc`;
- `description`;
- `info`;

with optional level-specific variants.

This is presentation of an already-existing enchantment identity. It does not create or execute the enchantment.

## Provider boundary

Enchantment Descriptions does **not** own:

- enchantment registration;
- enchantment effect execution;
- enchantment levels;
- applicability;
- conflicts;
- enchanting cost/math;
- spell casting;
- rituals;
- magical resources;
- magical progression.

Those remain owned by Minecraft or the mod that registered the enchantment.

Enchantment Descriptions owns only the client presentation/configuration of explanatory tooltip text.

## Modded enchantments

Official documentation states that modded enchantments are supported through localization.

Canonical expected form includes:

`enchantment.%MOD_ID%.%ENCH_ID%.desc`

The current implementation is slightly broader: it also checks `.description` and `.info`, plus level-specific variants.

A missing description therefore means missing/unsupported localization or UI composition, not absence of the enchantment.

## Semantic accounting

Provider-owned spells: **0**.

Provider-owned rituals/rites: **0**.

Provider-owned enchantments: **0**.

Provider-owned equivalent discrete magic actions: **0**.

Strict semantic delta:

**+0**

The mod's CurseForge category includes Magic because it presents magical/enchantment information, but taxonomy alone does not make it a magic-action provider.

## Apothic interaction risk

A public 1.21.1 issue reports a problem with `require_keybind` when used together with Apotheosis/Apothic. The report concerns 21.1.9 and is marked upstream as unverified.

The pack currently uses:

- Enchantment Descriptions 21.1.11;
- Apothic Enchanting 1.6.2.

Therefore the issue is retained only as a smoke-test regression risk. It is not asserted as a reproduced bug in the current pack.

## Runtime QA remains fail-closed

Catalog closure does not prove:

- current deployed client config;
- Shift/`require_keybind` behavior with Apothic;
- tooltip ordering with other UI mods;
- duplicate description suppression;
- PT-BR completeness;
- resource-pack overrides;
- item/book/enchanting-table presentation after reload;
- source branch ↔ installed binary byte equality.

## Result

**✅ Cataloged:** physical 21.1.11 identity/SHA and exact publisher release are pinned, while official 1.21.1 source establishes a client-only tooltip/localization runtime with no magic-action ownership.

Strict semantic contribution: **+0**.
