# Wind Upgrade Orb

- Provider: **SnackPirate's Aeromancy Additions**, `aero_additions` `1.2.8`.
- Identidade: `aero_additions:wind_upgrade_orb`.
- Superfície: item registrado (`Item`, componente de upgrade host); contribuição ao contador estrito de spells: **0**.

**Teto de evidência:** fonte imutável `ae282b32d25ad76ef8d01c637ec05566a767ae4c`; presença do contrato no JAR oficial de publicação `8251034` quando indicada. O JAR publisher tem 753884 bytes, SHA-1 `dee32c9fa84a9b3796e39846608f8f77591ea56f` e SHA-256 `b2dad354467a2cf1a92519ba68c8e2c32807a976d7b235132d625b7f0f90eea8`. Isso não comprova igualdade com o JAR instalado: o checksum histórico instalado tem 35 caracteres inválidos e permanece **`NOT_VERIFIED`**. [Contrato comum](../SOURCE-CONTRACTS-1.2.8.md) · [fechamento](../SOURCE-CATALOG-CLOSURE-1.2.8.md).

## Orb e tipo de upgrade

Aero registra item empilhável até **64**, raridade **UNCOMMON**, com componente **`irons_spellbooks:upgrade_orb_type`** apontando ao ResourceKey **`aero_additions:wind_spell_power`** no registry de UpgradeOrbType. Esse ID pertence a um registry diferente do atributo homônimo; o item possui ID próprio.

O tipo publicado aplica **+0.05 ao atributo `aero_additions:wind_spell_power`**, operação **`ADD_MULTIPLIED_BASE`**, usando este item como container. Para base Wind `B`, cada contribuição válida representa **0.05×B**; com base 1 e nenhum outro efeito, 1 orb seria Wind **1.05**. A equação não autoriza aplicação ilimitada: item elegível, limite de upgrades, bancada, remoção e consumo são responsabilidade do host. O orb em inventário não concede o bônus; Aero não define callback de aplicação no Item. [Ficha do tipo de upgrade](../data-contracts/upgrade-orb-wind-spell-power.md).

## Receita publicada

**`aero_additions:wind_upgrade_orb`**, shaped, **1 resultado**: `RRR` / `ROR` / `RRR`; **8 Wind Runes + 1 `irons_spellbooks:upgrade_orb`**. Expandindo somente a receita de Rune, são **64 Breeze Rods + 8 Blank Runes + 1 Upgrade Orb**. Advancement desbloqueia por **Blank Rune**, conforme JSON e declaração ativa; não exige possuir Wind Rune no criterion embora seja ingrediente da receita. O payload do upgrade está no JAR publicado, além do datagen.

**Localizadores:** [AAItems.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/item/AAItems.java#L49-L51) · [AAUpgradeOrbs.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/data/AAUpgradeOrbs.java#L12-L19) · [wind_spell_power.json](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/generated/resources/data/aero_additions/irons_spellbooks/upgrade_orb_type/wind_spell_power.json#L1-L9) · [AARecipes.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/data/AARecipes.java#L88-L95) · [wind_upgrade_orb.json](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/generated/resources/data/aero_additions/recipe/wind_upgrade_orb.json#L1-L21) · [wind_upgrade_orb.json](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/generated/resources/data/aero_additions/advancement/recipes/misc/wind_upgrade_orb.json#L1-L32).

**Consumo e QA:** Black Arcana/RPG pode catalogar esta superfície; mudanças de perks precisam de consumidor real e validação causal. Hook/adaptação **`NOT_VERIFIED`**; execução cliente/servidor, configuração efetiva e composição no modpack **`NOT_TESTED`**; **0 certificados**. Valores descritos são contratos de fonte/dados publicados, sem homologação de gameplay.
