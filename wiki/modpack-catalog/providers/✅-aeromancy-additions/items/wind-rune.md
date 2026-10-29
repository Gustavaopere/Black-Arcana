# Wind Rune

- Provider: **SnackPirate's Aeromancy Additions**, `aero_additions` `1.2.8`.
- Identidade: `aero_additions:wind_rune`.
- Superfície: item registrado (`Item`); contribuição ao contador estrito de spells: **0**.

**Teto de evidência:** fonte imutável `ae282b32d25ad76ef8d01c637ec05566a767ae4c`; presença do contrato no JAR oficial de publicação `8251034` quando indicada. O JAR publisher tem 753884 bytes, SHA-1 `dee32c9fa84a9b3796e39846608f8f77591ea56f` e SHA-256 `b2dad354467a2cf1a92519ba68c8e2c32807a976d7b235132d625b7f0f90eea8`. Isso não comprova igualdade com o JAR instalado: o checksum histórico instalado tem 35 caracteres inválidos e permanece **`NOT_VERIFIED`**. [Contrato comum](../SOURCE-CONTRACTS-1.2.8.md) · [fechamento](../SOURCE-CATALOG-CLOSURE-1.2.8.md).

## Material e aquisição

Item básico com pilha máxima **64**; Aero não adiciona atributo, spell, uso ativo, custo de mana ou raridade especial. Receita publicada **`aero_additions:wind_rune`**, shaped, produz **1**: `BBB` / `BRB` / `BBB`, com **8 `minecraft:breeze_rod` + 1 `irons_spellbooks:blank_rune`**. Advancement usa possuir Blank Rune (ou receita já desbloqueada), apesar do nome de criterion `has_rune`.

É ingrediente para Air Staff, Tempest Blade, Wind Upgrade Orb e template dos quatro Windmaker smithing transforms. A tag publicada **`irons_spellbooks:inscribed_rune`** o apresenta ao consumidor host. O material de jewelry **`aero_additions:rune_wind`** usa este item como ingrediente e dá +0.05 Wind Spell Power por `add_multiplied_total`, com quality 1.5; os limites/slots de aplicação pertencem ao Iron's Jewelry. Nenhum desses usos transforma Wind Rune em spell ou atributo autônomo.

O foco da escola é **Breeze Rod**, via `aero_additions:wind_focus`; o source não põe Wind Rune nessa tag. A rota publicada para rods acrescenta uma tabela de **1 roll**, pesos **6 rods : 7 vazio**, com count uniforme **5–10**, ao loot de `minecraft:chests/trial_chambers/reward`; probabilidade condicional **6/13**, expectativa **45/13 rods** por avaliação dessa tabela. Veja [aquisição/datagen](../data-contracts/acquisition-and-datagen.md) e [material Jewelry](../data-contracts/wind-jewelry-material.md).

**Localizadores:** [AAItems.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/item/AAItems.java#L49-L51) · [AARecipes.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/data/AARecipes.java#L79-L86) · [wind_rune.json](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/generated/resources/data/aero_additions/recipe/wind_rune.json#L1-L21) · [wind_rune.json](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/generated/resources/data/aero_additions/advancement/recipes/misc/wind_rune.json#L1-L32) · [AAItemTags.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/data/AAItemTags.java#L29-L34) · [normal_vault_add.json](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/resources/data/aero_additions/loot_table/chests/trial_chambers/normal_vault_add.json#L1-L28).

**Consumo e QA:** Black Arcana/RPG pode catalogar esta superfície; mudanças de perks precisam de consumidor real e validação causal. Hook/adaptação **`NOT_VERIFIED`**; execução cliente/servidor, configuração efetiva e composição no modpack **`NOT_TESTED`**; **0 certificados**. Valores descritos são contratos de fonte/dados publicados, sem homologação de gameplay.
