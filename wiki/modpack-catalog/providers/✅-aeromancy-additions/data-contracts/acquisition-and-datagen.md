# Aquisição, creative tab e data providers

- Provider: **SnackPirate's Aeromancy Additions**, `aero_additions` `1.2.8`.
- Identidade: oito receitas, oito advancements, duas adições de loot e `aero_additions:aeromancy_main`.
- Superfície: contratos publicados e infraestrutura de geração; contribuição ao contador estrito de spells: **0**.

**Teto de evidência:** fonte imutável `ae282b32d25ad76ef8d01c637ec05566a767ae4c`; presença do contrato no JAR oficial de publicação `8251034` quando indicada. O JAR publisher tem 753884 bytes, SHA-1 `dee32c9fa84a9b3796e39846608f8f77591ea56f` e SHA-256 `b2dad354467a2cf1a92519ba68c8e2c32807a976d7b235132d625b7f0f90eea8`. Isso não comprova igualdade com o JAR instalado: o checksum histórico instalado tem 35 caracteres inválidos e permanece **`NOT_VERIFIED`**. [Contrato comum](../SOURCE-CONTRACTS-1.2.8.md) · [fechamento](../SOURCE-CATALOG-CLOSURE-1.2.8.md).

## O que existe no publisher

O JAR oficial contém **8 recipes + 8 advancements de receita**, **2 DamageTypes**, **1 UpgradeOrbType**, **20 tags de item**, **2 tags próprias de entity type**, os recursos auxiliares descritos nas outras fichas, localization e as duas rotas de loot abaixo. `src/generated/resources` é incluído em `sourceSets.main.resources`; logo, a presença foi verificada no artefato e não inferida apenas do generator. Arquivos de source com diferença de fim de linha não demonstram JAR instalado igual ao publisher.

| Recipe ID publicado | Tipo e custo declarado | Resultado |
|---|---|---|
| `aero_additions:air_staff` | shaped: 4 Magic Cloth + 2 Sticks + 1 Wind Rune | 1 Air Staff |
| `aero_additions:wind_sword` | shaped: 3 Breeze Rods + 1 Weapon Parts + 1 Wind Rune | 1 Tempest Blade, Wind Blade X bloqueado |
| `aero_additions:wind_rune` | shaped: 8 Breeze Rods + 1 Blank Rune | 1 Wind Rune |
| `aero_additions:wind_upgrade_orb` | shaped: 8 Wind Runes + 1 Upgrade Orb | 1 Wind Upgrade Orb |
| `minecraft:windmaker_headpiece` | smithing: Wind Rune template + Wizard Helmet base + addition `[]` | `aero_additions:windmaker_headpiece` |
| `minecraft:windmaker_robes` | smithing: Wind Rune template + Wizard Chestplate base + addition `[]` | `aero_additions:windmaker_robes`, container vazio 1 slot |
| `minecraft:windmaker_skirt` | smithing: Wind Rune template + Wizard Leggings base + addition `[]` | **`aero_additions:windmaker_leggings`**, ID de item válido |
| `minecraft:windmaker_boots` | smithing: Wind Rune template + Wizard Boots base + addition `[]` | `aero_additions:windmaker_boots` |

Smithing recipe ID `minecraft:windmaker_skirt` e item `aero_additions:windmaker_leggings` são identidades distintas e coerentes; não há item registrado `windmaker_skirt`. Os JSONs de addition vazio são fatos publicados; execução da bancada/consumo/preservação de componentes permanece QA. As quatro alternativas shaped de robes em `AARecipes` estão **comentadas**, não geram quatro receitas adicionais.

Cada receita tem advancement filho de `minecraft:recipes/root`, criterion `has_the_recipe` **OU** criterion de inventário na mesma linha de requirements, e reward da recipe correspondente. Staff/armaduras usam Wind Rune; Sword usa Weapon Parts; Rune e Upgrade Orb usam **Blank Rune**, apesar do nome `has_rune`. Advancement de receita é descoberta do recipe book, não entrega do resultado. Updraft Tome não possui recipe nesses dados.

## Loot de Trial Chambers

O arquivo global **`data/neoforge/loot_modifiers/global_loot_modifiers.json`** (`replace=false`) lista dois modifiers com tipo host **`irons_spellbooks:append_loot`**:

| Condição `neoforge:loot_table_id` | Tabela adicional | Conteúdo de 1 roll | Probabilidade condicional |
|---|---|---|---|
| `minecraft:chests/trial_chambers/reward` | `aero_additions:chests/trial_chambers/normal_vault_add` | peso 6 Breeze Rods, count uniforme 5–10; peso 7 vazio | **6/13** para rods; expectativa **45/13 rods** |
| `minecraft:chests/trial_chambers/reward_ominous` | `aero_additions:chests/trial_chambers/ominous_vault_add` | peso 2 Updraft Tome; peso 7 vazio | **2/9** para 1 Tome |

Probabilidades condicionam a avaliação da tabela adicional, sem outros packs/modifiers; não são estatística global de abertura de Vault nem runtime testado. O serializer, carregamento, ordem e execução pertencem ao host/NeoForge. JEI plugin **`aero_additions:jei_compat`** só adiciona informação de Tome; AALang só gera texto. Nenhum deles registra uma terceira rota de obtenção.

## Geração e apresentação

`AAData` estende DatapackBuiltinEntriesProvider: RegistrySetBuilder inclui **DAMAGE_TYPE → AADamageTypes.bootstrap** e **UPGRADE_ORB_REGISTRY_KEY → AAUpgradeOrbs.bootstrap**, com namespaces minecraft/Aero. No GatherDataEvent, adiciona datapack entries, item tags, recipes e entity tags via `includeServer()`, localization via `includeClient()`. `AAData`, `AARecipes`, `AAItemTags`, `AAEntityTypeTags`, `AAUpgradeOrbs`, `AADamageTypes`, `AALang` são produtores de dados; não são novos spells ou callbacks de gameplay de aquisição.

`AACreativeTab` registra **`aero_additions:aeromancy_main`**, ícone Updraft Tome, e exibe os **9 itens registrados**. Em BuildCreativeModeTabContentsEvent, para essa aba, enumera **spells habilitados cuja escola seja Wind**, em todos os níveis configurados min..max, e cria stacks de **`irons_spellbooks:scroll`** pelo container host. Não registra item `aero_additions:scroll_wind`; a quantidade pode incluir Gust host se o override de escola for efetivo. Creative display não comprova aquisição survival nem cria spells adicionais.

Localization gerada/publicada tem nomes/guias dos itens/spells/effects, incluindo nomes de entidades sem spell ativo. Nome/assets não reativam os cinco registros comentados. Package-info de item/data só declara pacote/contrato de nulidade, sem objeto de registry ou obtenção de item.

**Localizadores:** [AAData.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/data/AAData.java#L21-L45) · [AARecipes.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/data/AARecipes.java#L20-L95) · [AACreativeTab.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/AACreativeTab.java#L20-L58) · [JeiCompat.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/item/JeiCompat.java#L11-L21) · [AALang.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/data/AALang.java#L23-L70) · [en_us.json](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/generated/resources/assets/aero_additions/lang/en_us.json#L1-L56) · [build.gradle](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/build.gradle#L113-L120) · [build.gradle](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/build.gradle#L150-L151) · [global_loot_modifiers.json](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/resources/data/neoforge/loot_modifiers/global_loot_modifiers.json#L1-L7) · [normal_vault_modifier.json](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/resources/data/aero_additions/loot_modifiers/trial_chamber_modifiers/normal_vault_modifier.json#L1-L10) · [ominous_vault_modifier.json](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/resources/data/aero_additions/loot_modifiers/trial_chamber_modifiers/ominous_vault_modifier.json#L1-L10) · [normal_vault_add.json](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/resources/data/aero_additions/loot_table/chests/trial_chambers/normal_vault_add.json#L1-L28) · [ominous_vault_add.json](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/resources/data/aero_additions/loot_table/chests/trial_chambers/ominous_vault_add.json#L1-L19).

**Consumo e QA:** Black Arcana/RPG pode catalogar esta superfície; mudanças de perks precisam de consumidor real e validação causal. Hook/adaptação **`NOT_VERIFIED`**; execução cliente/servidor, configuração efetiva e composição no modpack **`NOT_TESTED`**; **0 certificados**. Valores descritos são contratos de fonte/dados publicados, sem homologação de gameplay.
