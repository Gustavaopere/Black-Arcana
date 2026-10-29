# Wind Spell Power — tipo de upgrade

- Provider: **SnackPirate's Aeromancy Additions**, `aero_additions` `1.2.8`.
- Identidade: `aero_additions:wind_spell_power` no registry `irons_spellbooks:upgrade_orb_type`.
- Superfície: registro de datapack host / contrato de dados; contribuição ao contador estrito de spells: **0**.

**Teto de evidência:** fonte imutável `ae282b32d25ad76ef8d01c637ec05566a767ae4c`; presença do contrato no JAR oficial de publicação `8251034` quando indicada. O JAR publisher tem 753884 bytes, SHA-1 `dee32c9fa84a9b3796e39846608f8f77591ea56f` e SHA-256 `b2dad354467a2cf1a92519ba68c8e2c32807a976d7b235132d625b7f0f90eea8`. Isso não comprova igualdade com o JAR instalado: o checksum histórico instalado tem 35 caracteres inválidos e permanece **`NOT_VERIFIED`**. [Contrato comum](../SOURCE-CONTRACTS-1.2.8.md) · [fechamento](../SOURCE-CATALOG-CLOSURE-1.2.8.md).

## Identidade, geração e publicação

`AAUpgradeOrbs.WIND_SPELL_POWER` é **ResourceKey de UpgradeOrbType**, não DeferredRegister de item/atributo. `AAData.BUILDER` registra o bootstrap do registry host; `AAUpgradeOrbs.bootstrap` associa este key ao atributo **`aero_additions:wind_spell_power`**, quantidade **0.05**, operação **`ADD_MULTIPLIED_BASE`**, container **`aero_additions:wind_upgrade_orb`**. O nome homônimo do atributo não funde os registries.

O JSON **`data/aero_additions/irons_spellbooks/upgrade_orb_type/wind_spell_power.json`** existe em `src/generated/resources` **e no JAR publisher**; contém esses valores e container stack `count=1`. `AAData.onGatherData` é declaração de **datagen**, não rotina de aplicar upgrade em jogador; na execução o consumer host carrega o registry de datapack e o componente do item aponta ao ResourceKey.

## Efeito e limite de consumo

Cada modificador aceito acrescenta **5% da base Wind**, e não multiplicação de dano total por 1.05 garantida: para base 1 sem outras contribuições, atributo passa a **1.05**; n contribuições independentes legais da mesma operação modelam **1+0.05n**, antes de outros modificadores/clamp. O provider não declara neste bootstrap recipe de bancada de aplicação, limite de slots, elegibilidade de armadura, custo de aplicação, replacement/remoção ou regra para n. Tudo isso depende do Iron's efetivo. Não converter o bootstrap em API de perks nem duplicar settlement.

O item container e a receita para criá-lo estão em [Wind Upgrade Orb](../items/wind-upgrade-orb.md); a operação do material Jewelry é diferente (`add_multiplied_total`).

**Localizadores:** [AAUpgradeOrbs.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/data/AAUpgradeOrbs.java#L12-L19) · [AAData.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/data/AAData.java#L21-L45) · [AAItems.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/item/AAItems.java#L49-L51) · [wind_spell_power.json](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/generated/resources/data/aero_additions/irons_spellbooks/upgrade_orb_type/wind_spell_power.json#L1-L9) · [build.gradle](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/build.gradle#L150-L151).

**Consumo e QA:** Black Arcana/RPG pode catalogar esta superfície; mudanças de perks precisam de consumidor real e validação causal. Hook/adaptação **`NOT_VERIFIED`**; execução cliente/servidor, configuração efetiva e composição no modpack **`NOT_TESTED`**; **0 certificados**. Valores descritos são contratos de fonte/dados publicados, sem homologação de gameplay.
