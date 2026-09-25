# Enchantment Descriptions — 1.21.1 release-correlated presentation surface

## Evidence boundary

Installed artifact:

- `enchdesc-neoforge-1.21.1-21.1.11.jar`;
- mod id `enchdesc`;
- version `21.1.11`;
- SHA-1 `4d453df785ac21e0e7389cba949f4fa460c3e267`.

Exact publisher file:

- CurseForge project `250419`;
- file `8693034`;
- NeoForge 1.21.1;
- 21.1.11;
- 2026-08-20 Release.

Official source branch:

`Darkhax-Minecraft/Enchantment-Descriptions:1.21.1`

This source is **release-correlated**, not claimed as a byte-exact 21.1.11 commit pin.

## Build/runtime declaration

The official branch declares:

- `mod_id=enchdesc`;
- Minecraft `1.21.1`;
- Java 21;
- `mod_client_only=true`;
- Bookshelf and Prickle dependencies;
- description: enchantment-effect descriptions.

## Common Java surface

The visible common source is organized under:

- `api`;
- `impl`;
- `mixin/patch`.

The implementation directory contains:

- `Config.java`;
- `Constants.java`;
- `EnchdescMod.java`.

The mixin patch directory contains:

- `MixinItemEnchants.java`;
- `MixinItemStack.java`.

No spell, ritual or magic-action registry is established by this source surface.

## EnchdescMod behavior

The implementation operates on existing item/enchantment state.

It reads:

- `DataComponents.ENCHANTMENTS`;
- `DataComponents.STORED_ENCHANTMENTS`;
- `Registries.ENCHANTMENT`;
- existing enchantment `ResourceKey` values.

It then resolves localized explanatory text and adds it to tooltip output.

The localization search checks:

- `.desc`;
- `.description`;
- `.info`;

and optional `.<level>` forms.

## Config surface

The client config controls presentation only:

- enabled;
- only on enchanted books;
- only in enchanting-table GUI;
- require Shift;
- activation text;
- prefix;
- suffix;
- text style.

None of these options changes enchantment mechanics.

## Semantic exclusion

The following are explicitly **not** semantic magic objects owned by Enchantment Descriptions:

- descriptions;
- localization keys;
- Shift/keybind presentation condition;
- prefix/suffix/style;
- existing enchantment IDs obtained from another registry;
- enchanted books/items whose enchantments belong to Minecraft/another provider.

## Authority

The enchantment owner controls gameplay.

Enchantment Descriptions controls explanatory text.

A tooltip description must never be used as an authoritative mechanical specification when it differs from provider code/data.

## Result

- provider-owned spells: 0;
- provider-owned rites/rituals: 0;
- provider-owned enchantments: 0;
- provider-owned discrete magic actions: 0.

Strict semantic delta: **+0**.

Status: **✅ zero-semantic presentation-layer closure**.
