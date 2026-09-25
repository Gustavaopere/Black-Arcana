# Provider Audit Queue Delta — Fantasy Armor 1.2.4-1.21.1

Date: `2026-09-24`

This narrow overlay applies to `fantasy_armor` until the current physical-provider queue is regenerated integrally.

## Current row

| Mod ID | Installed identity | Effective audit state |
|---|---|---|
| `fantasy_armor` | `fantasy_armor-neoforge-1.2.4-1.21.1.jar` / SHA-1 `2b103680ca80a1d617dcae74630c4df8e93d3c55` | ✅ `CATALOGED / EXACT 1.2.4 SOURCE-PINNED / 29 ARMOR SETS / PASSIVE CONFIGURED VANILLA EFFECTS / ZERO SPELL-RITUAL-ACTIVE-ACTION REGISTRY / +0 STRICT SEMANTIC MAGIC / RUNTIME QA FAIL-CLOSED` |

## Physical authority

`neoforge-rpg-skilltree@d7c99d23ef1b38fe62c86a362ec521ced8861f96`

Certified sibling dossier:

`PROJECT-INSTRUCTIONS/modlist/Adventure and RPG + Armor, Tools, and Weapons + Cosmetic + Magic/✅-fantasy-armor v1.2.4-1.21.1.md`

## Publisher authority

CurseForge:

- project `1083998`;
- exact NeoForge file `7850813`;
- `fantasy_armor-neoforge-1.2.4-1.21.1.jar`;
- Release;
- published 2026-03-31;
- published change: Turkish-i issue fix.

## Exact source authority

`kend1e/FANTASY-ARMOR@0d58f07346fd7fffc08fac907aa908e5e4295667`

The commit is dated 2026-03-31, is titled `Fixed turkish i issue`, bumps the 1.21.1 NeoForge project to `mod_version=1.2.4-1.21.1`, and remains the repository master at this checkpoint.

## Closed by current evidence

- physical JAR/mod id/version/SHA-1;
- exact publisher file;
- exact source release pin;
- 19 NeoForge Java classes;
- 29 armor-set identities;
- 116 registered armor pieces;
- Moon Crystal item support;
- attributes configuration;
- full-set effect configuration and application;
- nine distinct default vanilla MobEffect identities used across sets;
- absence of Java spell/ritual/cast/keybind/active-item-use surface;
- semantic contribution fixed at +0.

## Runtime gates remain fail-closed

- physical JAR ↔ locally rebuilt source byte equality;
- deployed armor attribute config;
- deployed armor effect config;
- effect removal/refresh lifecycle;
- stale modifiers;
- Epic Fight coexistence;
- Cosmetic Armor coexistence;
- FirstPerson/player model rendering;
- resource-pack/model stack;
- dedicated-server/full-pack runtime.

## Semantic accounting

Fantasy Armor contributes **+0** to the strict spell/ritual/equivalent-action numerator.

Its magical content is equipment-driven passive attributes/effects rather than provider-owned discrete actions.
