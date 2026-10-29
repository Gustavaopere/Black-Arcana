# Entity-type tags — imunidades e caminho de dados

- Provider: **SnackPirate's Aeromancy Additions**, `aero_additions` `1.2.8`.
- Identidade: `aero_additions:reflection_immune`, `aero_additions:asphyxiation_immune`.
- Superfície: dois TagKeys de entidade e recursos auxiliares publicados; contribuição ao contador estrito de spells: **0**.

**Teto de evidência:** fonte imutável `ae282b32d25ad76ef8d01c637ec05566a767ae4c`; presença do contrato no JAR oficial de publicação `8251034` quando indicada. O JAR publisher tem 753884 bytes, SHA-1 `dee32c9fa84a9b3796e39846608f8f77591ea56f` e SHA-256 `b2dad354467a2cf1a92519ba68c8e2c32807a976d7b235132d625b7f0f90eea8`. Isso não comprova igualdade com o JAR instalado: o checksum histórico instalado tem 35 caracteres inválidos e permanece **`NOT_VERIFIED`**. [Contrato comum](../SOURCE-CONTRACTS-1.2.8.md) · [fechamento](../SOURCE-CATALOG-CLOSURE-1.2.8.md).

## Imunidades declaradas e consumidores

`AAEntityTypeTags` declara dois **`TagKey<EntityType<?>>`**; AAData adiciona seu generator com `includeServer()`. Ambos possuem JSON no publisher:

| Tag de entidade | Membro default | Checagem real |
|---|---|---|
| `aero_additions:reflection_immune` | **`minecraft:llama_spit`** | `AirblastSpell.canReflect` rejeita o tipo; `AAServerEvents.Game.windShieldDeflection` exclui esse tipo no ramo do efeito Wind Shield |
| `aero_additions:asphyxiation_immune` | **`minecraft:drowned`** | `AsphyxiateSpell.checkPreCastConditions` retorna false para o alvo com esse tipo |

A primeira é filtro de **tipo de projétil**; a segunda é filtro de **tipo de alvo**, não resistência de DamageType. A tag de Asphyxiate não é consultada por `BreathlessEffect.applyEffectTick`; ela não cria imunidade universal ao efeito aplicado de outra maneira. O ramo específico de **SummonedBreeze** no evento de projectile impact vem depois do ramo Wind Shield e executa código de deflexão próprio; não o deduzir destas tags ou da existência de um spell Summon Breeze ativo.

## Recursos externos e ressalva de path

O publisher inclui **`data/sable/tags/entity_type/retain_in_sub_level.json`**, `replace=false`, **values vazio**: ele não acrescenta nenhum tipo de entidade. É uma superfície de compatibilidade vazia, sem consumer/runtime Sable homologado.

Também inclui **`data/minecraft/tags/damage_type/entity_type/deflects_projectiles.json`**, cujo values contém **`aero_additions:summoned_breeze`**. O arquivo está sob **`damage_type`**, portanto estruturalmente descreve tag desse registry com path **`minecraft:entity_type/deflects_projectiles`**. Ele **não está** no caminho esperado de tag de entity type (`data/minecraft/tags/entity_type/deflects_projectiles.json`). Não corrigir silenciosamente o path no catálogo, nem afirmar que esse arquivo concede a tag vanilla de deflexão ao Breeze. Como o valor é um ID de entidade em um caminho de DamageType, aceitação/diagnóstico pelo loader fica `NOT_TESTED`; a deflexão explícita em `AAServerEvents` é evidência independente.

**Localizadores:** [AAEntityTypeTags.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/data/AAEntityTypeTags.java#L16-L26) · [AAData.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/data/AAData.java#L41-L45) · [reflection_immune.json](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/generated/resources/data/aero_additions/tags/entity_type/reflection_immune.json#L1-L5) · [asphyxiation_immune.json](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/generated/resources/data/aero_additions/tags/entity_type/asphyxiation_immune.json#L1-L5) · [AirblastSpell.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/airblast/AirblastSpell.java#L117-L118) · [AsphyxiateSpell.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/asphyxiate/AsphyxiateSpell.java#L60-L71) · [AAServerEvents.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/AAServerEvents.java#L68-L88) · [retain_in_sub_level.json](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/resources/data/sable/tags/entity_type/retain_in_sub_level.json#L1-L5) · [deflects_projectiles.json](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/resources/data/minecraft/tags/damage_type/entity_type/deflects_projectiles.json#L1-L6).

**Consumo e QA:** Black Arcana/RPG pode catalogar esta superfície; mudanças de perks precisam de consumidor real e validação causal. Hook/adaptação **`NOT_VERIFIED`**; execução cliente/servidor, configuração efetiva e composição no modpack **`NOT_TESTED`**; **0 certificados**. Valores descritos são contratos de fonte/dados publicados, sem homologação de gameplay.
