# Armor Material — parâmetros e adaptação de armaduras (1.0.10)

**Contrato técnico estático:** ✅ `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`. **Hooks mutadores:** `NOT_VERIFIED`. **QA física:** `NOT_TESTED`. **Perks executáveis:** `NOT_CERTIFIED`. **Política:** `NO_MUTATION`. O provider permanece `OPEN`; esta ficha de suporte acrescenta **+0 raízes mágicas**.

## 1. Identidade e autoridade

`com.github.alexmodguy.alexscaves.server.item.ACArmorMaterial` é uma classe de parâmetros e adaptação, com seis instâncias estáticas em `ACItemRegistry`. Não declara superinterface, registro próprio de material, interação de jogador ou spell. Seus dez métodos próprios, contando dois construtores e `<clinit>`, cobrem criação do material vanilla, durabilidade de propriedades, defesa, toughness, resistência a knockback e ingrediente de reparo. Os efeitos especiais das peças continuam nos respectivos itens e consumidores.

Autoridade: `alexscaves-1.0.10-neoforge+1.21.1.jar`, Minecraft **1.21.1**, CurseForge projeto **1645389**, arquivo **8856293**, **75.279.314 bytes**. SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`; SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. A classe tem SHA-256 `478accf7ab37014dc06a8f3d801348948638dc517db0e21b7fd91d2b47ca40a6`. A [prova comum](../EXACT-ARMOR-MATERIAL-1.0.10.md) e o [manifesto nativo](../EXACT-ARMOR-MATERIAL-1.0.10.json) delimitam esta ficha. A fonte pública `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1** e serve apenas como corroboração adjacente.

O campo privado `name` recebe o nome no construtor, mas nenhum outro método próprio o lê. Esse nome não constitui, sozinho, ID de registry, caminho de textura ou camada de armadura. `vanilla()` fornece uma lista vazia de camadas; a apresentação customizada das peças pertence aos seus owners.

## 2. Construção, ativação e estado

O construtor curto recebe `(name, durability, damageReduction, encantability, sound, toughness)` e delega ao longo com **knockback `0F`** (`@0–14`). O longo inicializa `ingredient=null`, guarda os argumentos e recebe knockback explicitamente (`@0–53`). A grafia do campo nativo de encantabilidade é `encantability`. O array `damageReduction` é retido por referência, sem cópia ou validação própria de comprimento/valores. Não há clamp próprio dos números fornecidos.

`vanilla()` cria, em cada chamada, um `EnumMap<ArmorItem.Type,Integer>`, um novo `ArmorMaterial` e um `Holder.direct` (`@0–112`). Percorre `ArmorItem.Type.values()` e acrescenta uma defesa somente se **`type.ordinal() < damageReduction.length`**. O material recebe esse mapa, encantabilidade, `ACCompat.soundHolder(sound)`, o supplier capturando **`this::getRepairIngredient`**, `List.of()`, toughness e knockback.

Há duas temporalidades distintas: os elementos atuais da defesa são copiados para o mapa e os floats atuais entram no novo material; o supplier de reparo consulta o campo da instância quando for chamado. Uma alteração posterior do array ou de `knockbackResistance` não reescreve o mapa/floats já enviados a um holder anterior. `setRepairMaterial`, por sua vez, pode alterar o resultado futuro daquele supplier. O campo `knockbackResistance` é público; a existência dessa escrita possível não homologa configuração dinâmica, sincronização ou isolamento por jogador.

Os construtores dos seis itens consumidores chamam `material.vanilla()` e `material.properties(new Item.Properties(), type)` antes de delegar a `ArmorItem`. O helper não agenda ticks, seleciona jogador, consulta nível de perk ou acompanha stacks equipados. O bootstrap do registry define valores compartilhados; propriedades de stack, atributos efetivos e callbacks pertencem às camadas consumidoras.

## 3. Defesa, durabilidade e valores exatos

`MAX_DAMAGE_ARRAY` é **`[13,15,16,11]`** (`<clinit> @0–26`). `properties(properties,type)` solicita **`properties.durability(MAX_DAMAGE_ARRAY[type.ordinal()] × durability)`** e devolve o retorno dessa chamada (`@0–17`). `defense(type)` devolve **`damageReduction[type.ordinal()]`** (`@0–9`). Ambos fazem indexação direta, sem o guard existente em `vanilla()`. Nenhum deles possui fallback para tipo cujo ordinal exceda o array; o helper também não testa `null`.

Os números abaixo estão na ordem dos **índices `0,1,2,3`**, sem atribuir esses ordinais aos nomes dos slots do engine. Os nomes `HELMET`, `CHESTPLATE`, `LEGGINGS` e `BOOTS` aparecem nas chamadas de consumidores, mas sua ordem no enum externo não é provada por este JAR. Um tipo adicional do engine só poderá entrar em `vanilla()` se seu ordinal couber no array de defesa; isso não estende o array de quatro posições usado por `properties()`.

| Instância em `ACItemRegistry` / nome armazenado | Multiplicador | Defesa `[0,1,2,3]` | Durabilidade calculada `[0,1,2,3]` | Encantabilidade | Toughness | Knockback |
|---|---:|---|---|---:|---:|---:|
| `PRIMORDIAL_ARMOR_MATERIAL` / `primordial` | 20 | `[3,4,3,2]` | `[260,300,320,220]` | 25 | 0F | 0F |
| `HAZMAT_SUIT_ARMOR_MATERIAL` / `hazmat_suit` | 20 | `[2,4,5,2]` | `[260,300,320,220]` | 25 | 0.5F | 0F |
| `DIVING_SUIT_ARMOR_MATERIAL` / `diving_suit` | 20 | `[2,6,5,2]` | `[260,300,320,220]` | 25 | 0F | 0F |
| `DARKNESS_ARMOR_MATERIAL` / `darkness` | 15 | `[4,5,1,1]` | `[195,225,240,165]` | 40 | 0.5F | 0F |
| `RAINBOUNCE_ARMOR_MATERIAL` / `rainbounce` | 6 | `[2,2,1,2]` | `[78,90,96,66]` | 40 | 0F | 0F |
| `GINGERBREAD_ARMOR_MATERIAL` / `gingerbread` | 10 | `[2,4,5,2]` | `[130,150,160,110]` | 25 | 0F | 0F |

As seis criações estão em `ACItemRegistry.<clinit>()V @34–289` e usam o construtor curto. Defesa é um valor entregue ao material/atributo, não dano líquido evitado; encantabilidade é o inteiro entregue ao construtor vanilla, não nível garantido de encantamento. `toughness()` e `knockbackResistance()` retornam diretamente seus floats (`@0–4`). Durabilidade de item, defesa, toughness e resistência a knockback são grandezas separadas.

## 4. Consumidores e fronteiras dos owners

O censo das **1555 entradas `.class`** do JAR encontra referências tipadas ao helper em sua própria classe, em `ACItemRegistry` e nos seis itens abaixo. As peças listadas descrevem chamadas do registry; não recebem fichas individuais nem certificação integral de comportamento por constarem desta tabela.

| Classe em `com.github.alexmodguy.alexscaves.server.item` | Instância recebida / constantes de tipo nas fábricas | Consumo delimitado |
|---|---|---|
| `PrimordialArmorItem` | Primordial; `HELMET`, `CHESTPLATE`, `LEGGINGS` | `vanilla()` + `properties()`; itens `alexscaves:primordial_helmet`, `primordial_tunic`, `primordial_pants` |
| `HazmatArmorItem` | Hazmat; `HELMET`, `CHESTPLATE`, `LEGGINGS`, `BOOTS` | `vanilla()` + `properties()`; itens `alexscaves:hazmat_mask`, `hazmat_chestplate`, `hazmat_leggings`, `hazmat_boots` |
| `DivingArmorItem` | Diving; `HELMET`, `CHESTPLATE`, `LEGGINGS`, `BOOTS` | `vanilla()` + `properties()`, além das leituras próprias de atributos descritas abaixo; itens `alexscaves:diving_helmet`, `diving_chestplate`, `diving_leggings`, `diving_boots` |
| `DarknessArmorItem` | Darkness; `HELMET`, `CHESTPLATE` | `vanilla()` + `properties()` após solicitar `RARITY_DEMONIC`; itens `alexscaves:hood_of_darkness`, `cloak_of_darkness` |
| `RainbounceBootsItem` | Rainbounce; `BOOTS` | `vanilla()` + `properties()`; item `alexscaves:rainbounce_boots` |
| `GingerbreadArmorItem` | Gingerbread; `HELMET`, `CHESTPLATE`, `LEGGINGS`, `BOOTS` | `vanilla()` + `properties()` e defesa guardada em `acDefense`; itens `alexscaves:gingerbread_helmet`, `gingerbread_chestplate`, `gingerbread_leggings`, `gingerbread_boots` |

`DivingArmorItem.<init>` monta um multimap próprio: `Attributes.ARMOR` recebe `material.defense(type)` com `ADD_VALUE` (`@51–76`); para `LEGGINGS`, acrescenta **0.5D** ao atributo de swim speed com `ADD_VALUE` (`@77–110`); para `CHESTPLATE`, acrescenta `material.toughness()` com `ADD_VALUE` (`@113–144`). Acrescenta knockback com `ADD_VALUE` somente quando **`material.knockbackResistance()>0F`** (`@145–178`), guarda o mapa e retorna. O material Diving declarado tem toughness e knockback zero. O `acModifiers(slot,stack)` devolve esse mapa somente quando `slot==acSlot.getSlot()`; nos outros slots, retorna mapa vazio. O bônus de swim speed é do construtor de Diving, sem campo equivalente em `ACArmorMaterial`.

`GingerbreadArmorItem.<init>` copia `material.defense(type)` para `acDefense` (`@37–43`); prepara atributos próprios de armor e movimento e mantém um cache de atributos dependentes de durabilidade. A leitura de `acModifiers` considera o slot e o dano do stack. Esses consumidores mostram por que alterar apenas um helper não prova mudança coerente dos atributos já criados ou em cache. Fórmulas de desgaste, velocidade e validação de equipamento pertencem ao item consumidor; esta ficha não homologa todos os seus efeitos especiais.

O helper não aplica dano, não cria `DamageSource`, não emite projétil, não resolve vítima/área/LOS e não lê ownership de entidade. A [ação do Cloak](../actions/cloak-darkness-incarnate.md) conserva seu contrato próprio. As defesas e durabilidades aqui não acrescentam escala de magia, duração de transformação ou proteção ambiental às outras peças.

## 5. Reparo, custos e apresentação

`getRepairIngredient()` devolve `Ingredient.EMPTY` enquanto `ingredient==null`; caso contrário, devolve a referência armazenada (`@0–17`). `setRepairMaterial(Ingredient)` apenas substitui essa referência (`@0–5`), inclusive aceitando `null`, que restabelece o fallback. Não há cópia, validação própria do ingrediente, consumo de item ou operação de bigorna nesses dois corpos.

| Material | Som entregue via `ACCompat` / campo de `SoundEvents` | Binding em `ACItemRegistry.setup()` |
|---|---|---|
| Primordial | `ARMOR_EQUIP_LEATHER`, convertido por `rawSound` | `Ingredient.of(alexscaves:tough_hide)`; setter `@24` |
| Hazmat | `ARMOR_EQUIP_IRON`, convertido por `rawSound` | `Ingredient.of(alexscaves:polymer_plate)`; setter `@51` |
| Diving | `ARMOR_EQUIP_IRON`, convertido por `rawSound` | `Ingredient.of(Items.COPPER_INGOT)` / `minecraft:copper_ingot`; setter `@70` |
| Darkness | `SoundEvents.EMPTY`, recebido diretamente | `Ingredient.of(alexscaves:dark_tatters)`; setter `@97` |
| Rainbounce | `ARMOR_EQUIP_GENERIC`, convertido por `rawSound` | Sem binding nos cinco setters do setup inspecionado; campo inicial nulo → `Ingredient.EMPTY` |
| Gingerbread | `ARMOR_EQUIP_LEATHER`, convertido por `rawSound` | `Ingredient.of(alexscaves:gingerbread_crumbs)`; setter `@124` |

Os quatro ingredientes do namespace `alexscaves` são obtidos por seus suppliers; cobre é o item vanilla direto. A sequência acima descreve o corpo de `setup()`; sua existência não certifica que o bootstrap terminou em um cliente/servidor físico. O supplier capturado por `vanilla()` permite consultar o binding que estiver vigente posteriormente. A falta de binding de Rainbounce nesse setup não demonstra impossibilidade de reparo por todas as regras do engine, receitas ou integrações do pack.

Não há mana, souls, stamina, cooldown, gasto de ingrediente nem rotina de dano de durabilidade nos métodos próprios do helper. Ele solicita uma capacidade de durabilidade nas propriedades e fornece um ingrediente ao material; consumo, reparo efetivo, Unbreaking, Mending, desgaste e sincronização pertencem a consumidores externos. Som e lista vazia de camadas também não comprovam áudio/renderer físico nem tamanho de hitbox.

## 6. Integração, marker de tick e limites para perks

Uma futura integração precisa escolher o owner correto: construção/registro de propriedades, atributos aplicados ao slot, estado de cada stack, cobrança de desgaste/reparo e sincronização são pontos distintos. Esta ficha fornece parâmetros e localizadores para investigar esses pontos. Nem `setRepairMaterial` nem o campo público de knockback constituem API homologada de perk por jogador: as instâncias são compartilhadas e os consumidores podem ter capturado valores na construção.

| Eixo pretendido de integração | Contrato observado / limite |
|---|---|
| Defesa / dano recebido | Array por ordinal e cópias no material; Diving/Gingerbread possuem atributos próprios. Não equivale a um multiplicador universal de redução de dano |
| Durabilidade / custo | `MAX_DAMAGE_ARRAY[ordinal] × multiplier` na construção das propriedades; custo de cada uso e reparo não é executado pelo helper |
| Encantamento / resistência | Encantabilidade, toughness e knockback são argumentos distintos de `ArmorMaterial`; regras de enchant e combate são externas |
| Tempo / frequência | Helper sem tick ou cooldown; modificar valores não agenda reavaliação dos atributos já construídos |
| Target / área / alcance | Não aplicável ao contrato próprio; não há seleção de alvo, raio, LOS ou projétil |
| Tamanho / apresentação | Nome armazenado, som adaptado e camadas vazias; sem alteração própria de escala, alcance ou colisão |
| Player / ownership | Instâncias compartilhadas, sem parâmetro de player; nenhum isolamento ou settlement de perk certificado |

**Disposição de `ACArmorTickItem`: suporte documentado aqui, sem ficha nem contagem adicional.** A classe `com.github.alexmodguy.alexscaves.server.item.ACArmorTickItem` é uma interface vazia: **zero campos, zero métodos, zero superinterfaces**; SHA-256 `f3f9e0ea4b09af538ad28414da3f9e34b07f9a16fdc72beeeffd73ee1505f038`. O censo de referências tipadas das 1555 classes encontra somente sua declaração e `DarknessArmorItem` como implementador direto. Não há dispatcher que consulte esse marker no JAR inspecionado. Esse limite é do artefato, não afirmação sobre transformações externas do modpack.

O nome privado `DarknessArmorItem.acArmorTick(ItemStack,Level,Player)` não declara método da interface vazia. Quem o chama é `DarknessArmorItem.acInventoryTick(ItemStack,Level,Entity,boolean)`, após exigir `entity instanceof Player` e `ACCompat.isWornArmor(stack,player)` (`@0–27`). O caminho de inventário usa a outra interface, **`ACTickingItem`**, que de fato declara `acInventoryTick`. `ItemStackTickMixin`, listado em `alexscaves.mixins.json`, testa `instanceof ACTickingItem` e encaminha o callback (`ac_inventoryTick @13–36`); não testa `ACArmorTickItem`. Portanto o marker não cria um segundo scheduler nem um hook mutador certificado.

**Homologação executável para Black Arcana, Enshrouded, RPG Skill Tree ou Epic Fight: `NOT_CERTIFIED`.** O catálogo não altera material, atributos, ingrediente ou dispatcher. Hooks mutadores `NOT_VERIFIED`; política `NO_MUTATION`.

## 7. Validação e localizadores JVM

| Método próprio de `ACArmorMaterial` | Descritor JVM | Evidência de corpo |
|---|---|---|
| `<init>` curto | `(Ljava/lang/String;I[IILnet/minecraft/sounds/SoundEvent;F)V` | Delegação ao longo com `0F`, `@0–14` |
| `<init>` longo | `(Ljava/lang/String;I[IILnet/minecraft/sounds/SoundEvent;FF)V` | Campos e referência do array, `@0–53` |
| `vanilla` | `()Lnet/minecraft/core/Holder;` | EnumMap, guard por comprimento, supplier, lista vazia e holder direto, `@0–112` |
| `properties` | `(Lnet/minecraft/world/item/Item$Properties;Lnet/minecraft/world/item/ArmorItem$Type;)Lnet/minecraft/world/item/Item$Properties;` | Indexação e multiplicação de durabilidade, `@0–17` |
| `defense` | `(Lnet/minecraft/world/item/ArmorItem$Type;)I` | Indexação direta, `@0–9` |
| `toughness` | `()F` | Retorno do campo, `@0–4` |
| `knockbackResistance` | `()F` | Retorno do campo público, `@0–4` |
| `getRepairIngredient` | `()Lnet/minecraft/world/item/crafting/Ingredient;` | Fallback de nulo para `EMPTY`, `@0–17` |
| `setRepairMaterial` | `(Lnet/minecraft/world/item/crafting/Ingredient;)V` | Escrita direta do campo, `@0–5` |
| `<clinit>` | `()V` | Quatro constantes `[13,15,16,11]`, `@0–26` |

Os seis construtores consumidores têm descritor `(Lcom/github/alexmodguy/alexscaves/server/item/ACArmorMaterial;Lnet/minecraft/world/item/ArmorItem$Type;)V`. `ACItemRegistry.<clinit>()V` contém as seis definições e as fábricas das peças; `setup()V @0–124` contém os cinco bindings de reparo. `DivingArmorItem.acModifiers` e `GingerbreadArmorItem.acModifiers` usam `(Lnet/minecraft/world/entity/EquipmentSlot;Lnet/minecraft/world/item/ItemStack;)Lcom/google/common/collect/Multimap;`. O manifesto sela instruções, ramos e classes dos consumidores delimitados; isso não certifica todo comportamento dessas classes.

Validação entregue: inspeção do JAR SHA-exato e contratos estáticos reproduzíveis. QA física pendente: bootstrap do registry e setup, propriedades efetivas por slot no engine, atributos e caches após equipar/desgastar, reparo/bigorna, encantamentos, áudio/renderização, sincronização cliente/servidor e convivência com transformações do pack. Não há prova física nesta entrega.

**Contabilidade:** **uma ficha técnica de sistema; +0 raízes mágicas novas; +0 fichas para o marker vazio.** `STATIC_TECHNICAL_CATALOG_ONLY`, `SHA_EXACT_BINARY_BEHAVIOR`, `NOT_VERIFIED`, `NOT_TESTED`, `NOT_CERTIFIED` e `NO_MUTATION` mantêm limites separados. O universo integral do provider continua `OPEN`.
