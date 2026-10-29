# Item tags — foco, equipamento e peso

- Provider: **SnackPirate's Aeromancy Additions**, `aero_additions` `1.2.8`.
- Identidade: 20 arquivos de tag de item publicados; três keys provider-owned.
- Superfície: contrato de tags de datapack; contribuição ao contador estrito de spells: **0**.

**Teto de evidência:** fonte imutável `ae282b32d25ad76ef8d01c637ec05566a767ae4c`; presença do contrato no JAR oficial de publicação `8251034` quando indicada. O JAR publisher tem 753884 bytes, SHA-1 `dee32c9fa84a9b3796e39846608f8f77591ea56f` e SHA-256 `b2dad354467a2cf1a92519ba68c8e2c32807a976d7b235132d625b7f0f90eea8`. Isso não comprova igualdade com o JAR instalado: o checksum histórico instalado tem 35 caracteres inválidos e permanece **`NOT_VERIFIED`**. [Contrato comum](../SOURCE-CONTRACTS-1.2.8.md) · [fechamento](../SOURCE-CATALOG-CLOSURE-1.2.8.md).

## Keys próprias e consumo

`AAItemTags` declara três `TagKey<Item>`: **`aero_additions:wind_focus`**, **`aero_additions:flight_light`**, **`aero_additions:flight_heavy`**. Os três JSONs gerados estão no publisher. TagKeys são seletores de membros, não registros adicionais de item; listas efetivas podem ser alteradas por outros packs.

| Tag provider | Membros publicados | Consumidor concreto |
|---|---|---|
| `wind_focus` | `minecraft:breeze_rod` | Wind `SchoolType` / seleção de foco pelo host |
| `flight_light` | quatro peças Windmaker, `air_staff`, `wind_sword` | FlightEffect: peso **0** para o slot |
| `flight_heavy` | quatro slots de armadura **iron, golden, diamond, netherite**: 16 IDs vanilla | FlightEffect: peso **4** para o slot |

FlightEffect percorre **todos `EquipmentSlot.values()`** e verifica por ordem: item em `flight_light` **ou slot vazio →0**; senão `flight_heavy` **→4**; senão a tag `#minecraft:anvil` **→10**; senão **→2**. Light vence Heavy se um item estiver nos dois. Soma **W**; a cada `tickCount % 20==0`, remove `aero_additions:flight.gravity`; se **W≠0**, adiciona modificador transitório **`W/4−0.08`**, operação **`ADD_VALUE`**, à gravidade. W=0 deixa esse modificador ausente; o Feather Flight spell possui outra alteração de gravidade. A lista não se restringe a armor: item empunhado também entra no score. Esta é a consequência real das tags, sem promessa de peso físico/velocidade final medida.

## Contribuições a tags externas

| Tag | Membros acrescentados pelo Aero |
|---|---|
| `irons_spellbooks:school_focus` | `minecraft:breeze_rod` |
| `irons_spellbooks:inscribed_rune` | `aero_additions:wind_rune` |
| `irons_spellbooks:staff` | `aero_additions:air_staff` |
| `curios:spellbook` | `aero_additions:updraft_tome` |
| `c:enchantables` | `aero_additions:air_staff` |
| `c:tools/melee_weapon` | `aero_additions:wind_sword` |
| `minecraft:enchantable/sword`, `minecraft:enchantable/sharp_weapon` | `aero_additions:air_staff` |
| `minecraft:head_armor`, `minecraft:enchantable/head_armor` | `aero_additions:windmaker_headpiece` |
| `minecraft:chest_armor`, `minecraft:enchantable/chest_armor` | `aero_additions:windmaker_robes` |
| `minecraft:leg_armor`, `minecraft:enchantable/leg_armor` | `aero_additions:windmaker_leggings` |
| `minecraft:foot_armor`, `minecraft:enchantable/foot_armor` | `aero_additions:windmaker_boots` |
| `minecraft:swords` | `aero_additions:wind_sword` |

Os **20** JSONs (3 próprios + 17 externos) estão em `src/generated/resources/data` e no JAR publisher; não são só intenção do generator. Nenhum concede enchantment, Curios slot extra ou spell sozinho. AAData registra `AAItemTags` somente na geração server-side de dados; a execução lê os JSONs.

**Localizadores:** [AAItemTags.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/data/AAItemTags.java#L20-L78) · [AAData.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/data/AAData.java#L32-L45) · [FlightEffect.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/feather_fall/FlightEffect.java#L25-L39) · [FlightEffect.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/feather_fall/FlightEffect.java#L50-L68) · [flight_light.json](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/generated/resources/data/aero_additions/tags/item/flight_light.json#L1-L10) · [flight_heavy.json](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/generated/resources/data/aero_additions/tags/item/flight_heavy.json#L1-L20) · [wind_focus.json](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/generated/resources/data/aero_additions/tags/item/wind_focus.json#L1-L5).

**Consumo e QA:** Black Arcana/RPG pode catalogar esta superfície; mudanças de perks precisam de consumidor real e validação causal. Hook/adaptação **`NOT_VERIFIED`**; execução cliente/servidor, configuração efetiva e composição no modpack **`NOT_TESTED`**; **0 certificados**. Valores descritos são contratos de fonte/dados publicados, sem homologação de gameplay.
