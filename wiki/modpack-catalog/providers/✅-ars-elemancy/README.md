# Ars Elemancy — dual/quad-element gear provider

## Engenharia causal por família — 17/10/2026

**✅ 7/7 famílias de equipamento source-pinned com fichas próprias** em [`equipment/`](equipment/): Tempest, Cinder, Silt, Mire, Vapor, Lava e Elemancer. Cada uma relaciona seu foco, bangle, essência e 12 armaduras com IDs reais, escolas/subescolas, mana, atributos, fraqueza/defesa, Curios, PerkSlots, ambiente e limits de adapter. [Matriz causal e barras de progresso](PERK-CAUSAL-EQUIPMENT-MATRIX-1.18.3.md). O registro fonte anterior de **105 items (7 foci + 7 essences + 7 bangles + 84 armors)** permanece a mesma contagem; **0 glyphs e 0 perks próprias**, +0 objetos mágicos novos.

Código fixo `Lyrellion/Ars-Elemancy@dfb18286106aca1ca39a9b0053d64a1ef5041751`, mod instalado `ars_elemancy-1.21.1-1.18.3.jar` SHA-1 declarado `f7e01437c86fc74e2abb2ad93554dc20c30b214b`; análise **SOURCE_CAUSALITY**, sem prova de equivalência binária integral, aplicação de atributos no runtime com Ars Nouveau 5.13.1/Ars Elemental 0.7.10.1, ou hook de RPG. `HeavyArmorE` adiciona **+25** (positivo) à `weaknessMap` por subescola, diferentemente de Light −25 e Medium −12.5. `Elemancer` é branch `SpellSchools.ELEMENTAL`, cuja composição real de `getSubSchools` precisa QA físico; não inferir todas as quatro escolas.

**Barras:** GLOBAL **—%** (piso **1.857/1.855 estritos**, denominador não consolidado); ARS ELEMANCY **7/7 famílias** com fichas causais (100% documental) e **105/105 itens source-pinned**, mas aplicação de perks/atributos **⚠️ QA**, e adapters homologados **⛔ 0**. Stage 06.05 🟡, Stage 09 físico pendente, PR #825 draft sem merge.

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