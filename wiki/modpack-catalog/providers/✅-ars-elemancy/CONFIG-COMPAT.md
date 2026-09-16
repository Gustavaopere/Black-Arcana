# Ars Elemancy 1.18.3 — config and compatibility

Status: `SOURCE DEFAULTS / EFFECTIVE PACK CONFIG+RUNTIME QA PENDING`

## Source checkpoint dependencies

`gradle.properties` at the pin uses:

- Minecraft 1.21.1;
- NeoForge 21.1.219;
- Ars Nouveau 5.11.1.1289 build dependency;
- Ars Elemental 0.7.9.155 build dependency;
- Curios 9.2.2+1.21.1;
- GeckoLib 4.8.3;
- Sauce preferred 0.0.29.73 with jarJar range `[0.0.29,)`.

`neoforge.mods.toml` declares runtime minimums Ars Nouveau `[1.21.1-5.2,)` and Ars Elemental `[0.7.0.9,)`. The physical pack has Ars Nouveau 5.13.1 and Ars Elemental 0.7.10.1, satisfying those metadata ranges. This is not proof of full runtime compatibility.

Curios is directly used in source/build but is not separately listed in the audited `neoforge.mods.toml` dependency section. It is present in the physical pack; absence behavior is not assumed safe.

## Common config defaults

- `elemental_maj_focus_discount`: 0.25, range 0..0.99;
- `regen_bonus`: true;
- Tempest focus buff: 1.0;
- Silt focus buff: 1.0;
- Vapor focus buff: 1.0;
- Mire focus buff: 1.0;
- Lava focus buff: 1.0;
- Cinder focus buff: 1.0;
- Elemental focus buff: 1.0;
- `armorMaxMana`: 100, range 0..10000;
- `armorManaRegen`: 4, range 0..100.

Client default:

- `Enable SpellFocusRender`: true.

Effective installed config files were not audited in this source pass.

## All the Arcanist Gear

Source conditionally expands armor perk slots when mod id `allthearcanistgear` is loaded. That mod id is absent from the current physical modlist, so Phase 2T records the non-ATAG slot branch as the expected current path.

## Mixins

One common mixin targets Ars Elemental `CompatUtils` and extends elemental focus recognition. This is a version-sensitive host seam and must fail closed for any future Black Arcana adapter; public class visibility does not establish a stable integration contract.

## Network

`NetworkManager` creates protocol registrar version `1` but registers **zero payload types**. No C2S or S2C gameplay authority is attributed to Ars Elemancy's own network layer at this checkpoint.