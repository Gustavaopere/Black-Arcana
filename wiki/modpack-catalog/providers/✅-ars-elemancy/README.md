# Ars Elemancy — dual/quad-element gear provider

Status: `PHASE 2T / SOURCE-PINNED 1.18.3 CATALOG COMPLETE / RUNTIME+PACK QA PENDING`

## Installed identity

- mod id: `ars_elemancy`
- physical JAR: `ars_elemancy-1.21.1-1.18.3.jar`
- runtime version: `1.18.3`
- physical SHA-1: `f7e01437c86fc74e2abb2ad93554dc20c30b214b`
- source checkpoint: `Lyrellion/Ars-Elemancy@dfb18286106aca1ca39a9b0053d64a1ef5041751`
- physical host providers: Ars Nouveau `5.13.1`, Ars Elemental `0.7.10.1`

The source checkpoint itself declares `mod_version=1.18.3`; matching version numbers do not prove the installed JAR was built byte-for-byte from that exact commit.

## Correct provider class

`GEAR / ELEMENTAL SPECIALIZATION / ARS ELEMENTAL COMPAT`

Ars Elemancy does **not** register a glyph family or a second casting engine. `registerGlyphs()` and `registerPerks()` are empty at the exact checkpoint.

It instead provides seven equipment identities:

| Identity | School contract |
|---|---|
| Tempest | Air + Water |
| Cinder | Air + Fire |
| Silt | Air + Earth |
| Mire | Earth + Water |
| Vapor | Fire + Water |
| Lava | Fire + Earth |
| Elemancer | Ars `ELEMENTAL` / all-element identity |

## Exact owned content

- 105 item registrations;
- 84 armor items = 21 four-piece sets;
- 7 foci;
- 7 essences;
- 7 bangles;
- 0 provider-owned blocks found;
- 33 ArmorMaterial registrations;
- 3 new Ars PerkSlot values: 4, 5 and 6;
- 1 local RecipeType + 1 local RecipeSerializer registration named `armor_upgrade`;
- 1 creative tab;
- 0 custom network payloads registered.

See `REGISTRIES.md`, `EQUIPMENT-CATALOG.md`, `ACQUISITION.md`, `FOCI.md`, `BANGLES.md`, `ARMOR.md`, `CONFIG-COMPAT.md` and `TECHNICAL-AUDIT.md`.

## Authority

Ars Nouveau owns spell grammar, mana, perk registry and spell execution. Ars Elemental/Sauce own the elemental attribute and elemental-equipment contracts used here. Ars Elemancy owns its fused equipment identities and their direct item behavior. Black Arcana does not replay mana discounts, focus amplification, environmental Curio effects, bangle attributes, armor attributes or elemental resistance handling.

No Black Arcana runtime Stage or adapter is promoted by this source catalog.