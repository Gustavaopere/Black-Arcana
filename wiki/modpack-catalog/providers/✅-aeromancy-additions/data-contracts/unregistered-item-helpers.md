# Helpers experimentais de item e assets sem registro

- Provider: **SnackPirate's Aeromancy Additions**, `aero_additions` `1.2.8`.
- Identidade: classes `TestCurio` / `TestImbuableTool`; modelos de scroll/ring sem item provider próprio.
- Superfície: código de suporte presente; registro de item ausente; contribuição ao contador estrito de spells: **0**.

**Teto de evidência:** fonte imutável `ae282b32d25ad76ef8d01c637ec05566a767ae4c`; presença do contrato no JAR oficial de publicação `8251034` quando indicada. O JAR publisher tem 753884 bytes, SHA-1 `dee32c9fa84a9b3796e39846608f8f77591ea56f` e SHA-256 `b2dad354467a2cf1a92519ba68c8e2c32807a976d7b235132d625b7f0f90eea8`. Isso não comprova igualdade com o JAR instalado: o checksum histórico instalado tem 35 caracteres inválidos e permanece **`NOT_VERIFIED`**. [Contrato comum](../SOURCE-CONTRACTS-1.2.8.md) · [fechamento](../SOURCE-CATALOG-CLOSURE-1.2.8.md).

## Código presente sem item ativo

`AAItems` possui **nove registros ativos**, todos com fichas próprias. A tentativa de registro **`TEST_PICKAXE`** está comentada, e não há instanciação registrada de `TestCurio`. As classes podem estar compiladas no JAR sem criar Item no registry; **não há ID de item ativo para catalogar para elas**.

`TestCurio extends Item implements ICurioItem`: seu único comportamento especial, **`canEquip`**, consulta o inventário Curios da entidade e `findFirstCurio(this)`; só retorna true se a consulta composta estiver vazia. Assim, o helper tenta impedir uma segunda cópia desse mesmo objeto Item equipada; ausência de inventário também resulta em Optional vazio. Ele não declara slot, atributos, preset, custo, receita ou aquisição.

`TestImbuableTool extends Item implements IPresetSpellContainer`: ao inicializar stack do próprio tipo **sem container existente**, cria `ISpellContainer.create(1,true,false)`, adiciona **Spectral Hammer host nível 6**, `locked=true`, e salva componente **`irons_spellbooks:spell_container`** imutável. Isso descreve **1 slot**, seleção por roda e flag `mustEquip=false` no contrato host; não prova aquisição, callback disparado ou ferramenta registrada. O bloco comentado de AAItems forneceria propriedades Diamond/pickaxe se ativado; por estar comentado, não atribuir tier, durabilidade ou IDs ativos a esta classe.

## Assets que não são registros de item

Os modelos **`assets/aero_additions/models/item/scroll_wind.json`** e **`affinity_ring_wind.json`**, e suas texturas, estão publicados. São layers de apresentação e não chamadas de registro. O creative tab fabrica stacks do **item host `irons_spellbooks:scroll`** para spells Wind; não cria um item provider `scroll_wind`. O material Jewelry `rune_wind` também não cria por si item de anel provider. Esta ficha não transforma esses nomes de arquivo em registry IDs ativos.

Não há recipe, advancement ou loot provider de teste para esses helpers. Presets/classes/assets sem raiz ativa não aumentam as dez magias nem as nove identidades de item. Reutilização via perks exigiria implementar e verificar uma fronteira real, sem ativar acidentalmente código experimental do provider.

**Localizadores:** [AAItems.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/item/AAItems.java#L29-L74) · [TestCurio.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/item/TestCurio.java#L9-L17) · [TestImbuableTool.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/item/TestImbuableTool.java#L9-L25) · [scroll_wind.json](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/resources/assets/aero_additions/models/item/scroll_wind.json#L1-L6) · [affinity_ring_wind.json](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/resources/assets/aero_additions/models/item/affinity_ring_wind.json#L1-L6) · [AACreativeTab.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/AACreativeTab.java#L45-L57).

**Consumo e QA:** Black Arcana/RPG pode catalogar esta superfície; mudanças de perks precisam de consumidor real e validação causal. Hook/adaptação **`NOT_VERIFIED`**; execução cliente/servidor, configuração efetiva e composição no modpack **`NOT_TESTED`**; **0 certificados**. Valores descritos são contratos de fonte/dados publicados, sem homologação de gameplay.
