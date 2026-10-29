# Air Staff

- Provider: **SnackPirate's Aeromancy Additions**, `aero_additions` `1.2.8`.
- Identidade: `aero_additions:air_staff`.
- Superfície: item registrado (`StaffItem`, Iron's); contribuição ao contador estrito de spells: **0**.

**Teto de evidência:** fonte imutável `ae282b32d25ad76ef8d01c637ec05566a767ae4c`; presença do contrato no JAR oficial de publicação `8251034` quando indicada. O JAR publisher tem 753884 bytes, SHA-1 `dee32c9fa84a9b3796e39846608f8f77591ea56f` e SHA-256 `b2dad354467a2cf1a92519ba68c8e2c32807a976d7b235132d625b7f0f90eea8`. Isso não comprova igualdade com o JAR instalado: o checksum histórico instalado tem 35 caracteres inválidos e permanece **`NOT_VERIFIED`**. [Contrato comum](../SOURCE-CONTRACTS-1.2.8.md) · [fechamento](../SOURCE-CATALOG-CLOSURE-1.2.8.md).

## Equipamento e modificadores

`AAItems` registra um staff de pilha máxima **1**, raridade **RARE**, com cinco modificadores restritos a **MAINHAND**. Valores são contribuições ao atributo; dano/velocidade finais incluem a base da entidade e outros modificadores.

| Atributo | Quantidade | Operação | ID do modificador |
|---|---:|---|---|
| `minecraft:generic.attack_damage` | +2 | `ADD_VALUE` | `Item.BASE_ATTACK_DAMAGE_ID` |
| `minecraft:generic.attack_speed` | −3 | `ADD_VALUE` | `Item.BASE_ATTACK_SPEED_ID` |
| `aero_additions:wind_spell_power` | +0.15 | `ADD_MULTIPLIED_BASE` | `aero_additions:wind_spell_power` |
| `irons_spellbooks:spell_power` | +0.05 | `ADD_MULTIPLIED_BASE` | `aero_additions:spell_power` |
| `minecraft:generic.gravity` | −0.25 | `ADD_MULTIPLIED_BASE` | `aero_additions:gravity` |

Aero não declara spell embutido nem consumo de mana próprio neste item. Com bases de potência 1 e sem outros modificadores, Wind=1.15 e potência geral=1.05; o produto usado pelo host é **1.2075**, antes de config/nível. Gravidade recebe −25% da base, sem equivaler por si a voo. Veja [atributo Wind](../attributes/wind-spell-power.md).

## Receita e tags publicados

Receita **`aero_additions:air_staff`**, `minecraft:crafting_shaped`, produz **1**: linhas `CCS` / ` RC` / `S C`; `C=irons_spellbooks:magic_cloth`, `S=minecraft:stick`, `R=aero_additions:wind_rune`. Custo: **4 magic cloth + 2 sticks + 1 wind rune**. Advancement de receita aceita possuir Wind Rune ou a receita já desbloqueada. JSON de receita/advancement está no publisher, além da declaração de datagen.

As tags publicadas incluem `irons_spellbooks:staff`, `c:enchantables`, `minecraft:enchantable/sword`, `minecraft:enchantable/sharp_weapon` e `aero_additions:flight_light`. Esta última dá peso **0** ao slot no cálculo de FlightEffect, inclusive quando empunhado; não concede efeito Flight. [Contrato das tags](../data-contracts/item-tags.md).

**Localizadores:** [AAItems.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/item/AAItems.java#L23-L39) · [AARecipes.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/data/AARecipes.java#L59-L67) · [air_staff.json](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/generated/resources/data/aero_additions/recipe/air_staff.json#L1-L24) · [air_staff.json](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/generated/resources/data/aero_additions/advancement/recipes/combat/air_staff.json#L1-L32) · [AAItemTags.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/data/AAItemTags.java#L29-L58).

**Consumo e QA:** Black Arcana/RPG pode catalogar esta superfície; mudanças de perks precisam de consumidor real e validação causal. Hook/adaptação **`NOT_VERIFIED`**; execução cliente/servidor, configuração efetiva e composição no modpack **`NOT_TESTED`**; **0 certificados**. Valores descritos são contratos de fonte/dados publicados, sem homologação de gameplay.
