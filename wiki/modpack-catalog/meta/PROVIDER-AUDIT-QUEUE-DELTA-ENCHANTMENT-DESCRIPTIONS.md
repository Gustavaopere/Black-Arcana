# Provider Audit Queue Delta — Enchantment Descriptions 21.1.11

Date: `2026-09-24`

This overlay applies to `enchdesc` until the current physical-provider queue is regenerated integrally.

## Current row

| Mod ID | Installed identity | Effective audit state |
|---|---|---|
| `enchdesc` | `enchdesc-neoforge-1.21.1-21.1.11.jar` / SHA-1 `4d453df785ac21e0e7389cba949f4fa460c3e267` | ✅ `CATALOGED / EXACT PHYSICAL + PUBLISHER RELEASE / RELEASE-CORRELATED 1.21.1 SOURCE / CLIENT TOOLTIP PRESENTATION / ZERO OWNED MAGIC ACTIONS / +0 STRICT SEMANTIC MAGIC` |

## Physical authority

`neoforge-rpg-skilltree@d7c99d23ef1b38fe62c86a362ec521ced8861f96`

Certified dossier:

`PROJECT-INSTRUCTIONS/modlist/Cosmetic + Magic + Map and Information + Utility & QoL/✅-enchantment-descriptions v21.1.11.md`

## Exact publisher authority

- CurseForge project `250419`;
- file ID `8693034`;
- `enchdesc-neoforge-1.21.1-21.1.11.jar`;
- NeoForge 1.21.1;
- Release;
- uploaded 2026-08-20;
- change: Sweeping Edge description localization fix.

## Official source authority

Official `1.21.1` branch:

- project base version `21.1`;
- `mod_client_only=true`;
- tooltip/localization implementation;
- no provider enchantment/spell/ritual/action registry established.

Because the branch is mutable and not tagged as literal 21.1.11, this is **release-correlated source evidence**, not a claimed immutable exact source pin.

## Closed by current evidence

- physical JAR/mod id/version/SHA-1;
- exact publisher file;
- client-only role;
- description/localization lookup contract;
- existing enchantment IDs are consumed, not registered;
- provider contributes zero spell/ritual/enchantment/action identities;
- strict semantic contribution fixed at +0.

## Runtime/UI gates remain fail-closed

- installed binary ↔ current source byte equality;
- deployed config;
- Apothic `require_keybind` coexistence;
- tooltip ordering/duplication;
- resource-pack/localization completeness;
- language switching/reload;
- UI behavior on enchanted books/items/enchanting table.

## Semantic accounting

Enchantment Descriptions contributes **+0** to the strict semantic magic numerator.

It is a presentation/support component, not a magic-action provider.
