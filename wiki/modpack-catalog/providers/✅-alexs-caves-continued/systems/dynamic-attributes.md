# Dynamic Attributes — ACDynamicAttributeItem (Alex's Caves Continued 1.0.10)

**Contrato técnico estático:** ⚠️ PARCIAL / NOT_CERTIFIED. **Hook mutador:** NOT_VERIFIED. **QA física:** NOT_TESTED. **Perk executável:** NOT_CERTIFIED. **Política:** NO_MUTATION/fail-closed. **Provider:** OPEN. **Novas raízes mágicas:** 0.

## 1. Identidade, proveniência e descrição

**ACDynamicAttributeItem** é a interface de suporte que declara a consulta de modificadores de atributos condicionados a slot e stack de item. Ela não é feitiço, encantamento, entidade, item registrável ou operação de cast independente. A interface não possui resource ID próprio de registry. A descrição aqui é interpretação técnica do comportamento nativo, não texto promocional do provider.

- **Mod:** Alex's Caves Continued, mod ID alexscaves, versão **1.0.10** no pack; Minecraft **1.21.1** / NeoForge / Java **21**.
- **JAR físico/publisher:** alexscaves-1.0.10-neoforge+1.21.1.jar, **75.279.314 bytes**, SHA-1 **6960b299a39a039ac8a5eb9b07be4ad0e3e0a570**, SHA-256 **36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c**; CurseForge projeto **1645389**, arquivo **8856293**.
- **Owner:** com.github.alexmodguy.alexscaves.server.item.ACDynamicAttributeItem; classfile SHA-256 **22671a5b460c001b73982a2cff6c555f52559ee3390d48728c7ccff04c9e52be**.
- **Assinatura pública abstrata:** acModifiers(EquipmentSlot, ItemStack):Multimap; JVM descriptor **(Lnet/minecraft/world/entity/EquipmentSlot;Lnet/minecraft/world/item/ItemStack;)Lcom/google/common/collect/Multimap;**. A erasure não especifica os argumentos genéricos do Multimap nem prova aplicação final pela engine.
- **Evidência:** [auditoria binária SHA-exata e limites](../EXACT-DYNAMIC-ATTRIBUTE-DISCOVERY-1.0.10.md); [auditor e oito regressões nativas](../../../../../docs/qa/alexscaves_1010_dynamic_attribute_probe_test.py).
- **Fonte adjacente:** Codx-org/AlexsCavesContinued @ 523308608422ab8e31974befa7111ecdf495dd37 declara **1.1.1**. Não é autoridade de valores para 1.0.10.

## 2. Ativação, ordem, guardas e consumidores

O JAR 1.0.10 contém **sete classes implementadoras diretas**, cada uma com corpo próprio acModifiers, e **três implementadoras por herança** de SpearItem (ExtinctionSpearItem, FrostmintSpearItem e LimestoneSpearItem). Essas subclasses não declaram corpo próprio de acModifiers. O censo global cobriu 1.555 classfiles; as referências tipadas de chamada acModifiers encontradas no publisher pertencem aos sete próprios owners. **O gatilho exato de aplicação pela engine e execução de mixins do pack continuam NÃO VERIFICADOS**.

Cada implementador direto declara getDefaultAttributeModifiers(ItemStack) e solicita **ACCompat.itemAttributes(BiFunction,ItemStack,Supplier)** em **@14**, passando uma consulta por slot e um supplier de fallback. O helper nativo itera EquipmentSlot.values(); a cada resultado não null, converte o slot em EquipmentSlotGroup, adiciona as entradas ao builder de ItemAttributeModifiers e marca que houve resposta. Somente se **todas** as consultas retornaram null usa o fallback da superclasse. Um Multimap vazio é resposta não null e suprime o fallback agregado no caminho correspondente.

| Implementador direto | Seleção confirmada em acModifiers |
|---|---|
| **DivingArmorItem** | Se o slot consultado coincide com acSlot.getSlot(), devolve divingArmorAttributes; caso contrário, ImmutableMultimap.of() vazio |
| **GingerbreadArmorItem** | Se coincide com acSlot.getSlot(), devolve getOrCreateDurabilityAttributes(stack.getDamageValue(),stack.getMaxDamage()); senão, ImmutableMultimap.of() vazio |
| **OrtholanceItem** | MAINHAND: campo defaultModifiers; outro slot: null |
| **PrimitiveClubItem** | MAINHAND: defaultModifiers[clamp(enchantLevel(stack,SWIFTWOOD),0,3)]; outro slot: null |
| **SharpenedCandyCaneItem** | MAINHAND: campo defaultModifiers; outro slot: null |
| **SpearItem** | MAINHAND: campo defaultModifiers; outro slot: null; três lanças derivadas herdam esse corpo |
| **TotemOfPossessionItem** | MAINHAND: campo defaultModifiers; outro slot: null |

A tabela representa **retornos no bytecode 1.0.10**, não atributos finais, ritmo de ataque, defesa efetiva ou estados de jogadores. Os construtores e valores nativos desses mapas foram aprofundados na prova suplementar #1118; o comportamento integral dos equipamentos permanece em escopo futuro de suas fichas.

## 3. Efeitos e parâmetros exatos do recorte

**Ampliação da auditoria — #1118:** a [prova de construção dos mapas e referência NeoForge 21.1.250](../EXACT-DYNAMIC-ATTRIBUTE-CONSTRUCTION-1.0.10.md) documenta os valores dos construtores, as quinze fábricas de registro e o caminho externo de seleção. Ortholance fornece +5 de dano e -2.4000000953674316 de velocidade; Candy Cane +3/+4; Totem +2/-2.4000000953674316; Limestone/Frostmint/Extinction Spears +3/+5/+8 de dano e -3 de velocidade, todos ADD_VALUE. Diving leggings solicitam +0.5 de natação ADD_VALUE; chestplate solicita toughness do material. Gingerbread mantém mapa inicial distinto do cache por dano. O componente de atributos não vazio do NeoForge evita o fallback stack-aware; a aplicação final continua não verificada. Os dados não constituem atributos finais do jogador nem certificado dos equipamentos completos.

**GingerbreadArmorItem.getOrCreateDurabilityAttributes(int damage,int maxDamage)** possui 73 instruções. Usa Map.containsKey(damage) e, em hit de cache, retorna o mapa existente. No caminho de criação calcula:

- **r = (float)damage / (float)maxDamage**, sem clamp ou guarda explícita de maxDamage no corpo;
- **s = 0.1D + 0.9D × (double)r**;
- atributo **ARMOR**, operação **ADD_VALUE**, magnitude recebida de acDefense;
- atributo **MOVEMENT_SPEED**, operação **ADD_MULTIPLIED_BASE**, magnitude s;
- guarda o resultado em gingerbreadDurabilityDependentAttributes com chave **Integer.valueOf(damage)**, sem incluir maxDamage na chave.

A saída de movimento é um **modificador relativo à base**, não velocidade final medida. A chave de cache só por dano cria uma **possibilidade condicional** de reuso de cálculo entre stacks com maxDamage distintos; não foi demonstrado que isso ocorre no pack. Falhas com maxDamage zero, reload e alterações externas exigem investigação específica.

**PrimitiveClubItem** usa nível Swiftwood com clamp 0..3. O contrato estático de fórmula e níveis do encanto já é individualmente certificado em [Swiftwood](../enchantments/swiftwood.md): ele altera um modificador ATTACK_SPEED do clube, enquanto o +8 ATTACK_DAMAGE do item é constante. Esta interface **não cria outro cast, dano ou certificado do encantamento**.

**Outras superfícies:** os corpos selecionados não criam projétil, mob, nuvem, status, teleporte, explosão, mudança de bloco, seleção de vítima ou alcance. Dano efetivo, PvP, hitbox, LOS, AOE, knockback e targeting de ataques pertencem aos consumidores de equipamento/engine e **não são atributos próprios desta interface**.

## 4. Custos, tempo, escalonamento e unidade

Mana, stamina, ingrediente consumido, carga, intervalo de tick, cooldown, duração, projétil e gasto de durabilidade por execução de acModifiers são **N/A no contrato próprio**: os corpos verificados consultam dados de stack, retornam mapas e constroem componentes, sem settlement de recurso ou agendamento. **Durabilidade atual e máxima são inputs** do ramo Gingerbread, não custo cobrado pelo callback.

Swiftwood é um nível de encantamento obtido por ACCompat.enchantLevel e limitado a quatro índices precalculados. A expressão Gingerbread mistura divisão em float e coeficientes em double; não arredondar esses cálculos como se houvesse precisão decimal exata. Velocidade final de movimento, DPS, ataque, mitigação e frequência de recálculo são **NÃO VERIFICADOS**.

## 5. Grafo técnico, estado e persistência

- Interface e sete implementadores: **server.item.ACDynamicAttributeItem / DivingArmorItem / GingerbreadArmorItem / OrtholanceItem / PrimitiveClubItem / SharpenedCandyCaneItem / SpearItem / TotemOfPossessionItem**.
- Herança: **ExtinctionSpearItem, FrostmintSpearItem, LimestoneSpearItem → SpearItem** para este callback.
- Bridge: **server.misc.ACCompat.itemAttributes** com overload (BiFunction,ItemStack,Supplier) de 48 instruções e overload (Multimap,EquipmentSlot,Supplier) de 19.
- Saída: builder de **net.minecraft.world.item.component.ItemAttributeModifiers**, com EquipmentSlotGroup por slot.
- Dependências: ItemStack.getDamageValue/getMaxDamage; ACEnchantmentRegistry.SWIFTWOOD; ACCompat.enchantLevel; getOrCreateDurabilityAttributes; ImmutableMultimap e Map.
- Estado: cache de modificadores de Gingerbread em campo de item, indexado por **damage**, não por player/UUID. Este código não prova isolamento por stack, invalidation, persistência de cache ou sincronização cliente/servidor.
- Autoria: nenhum caster, target player, owner de projétil, recibo de hit ou identificador de perk é passado por acModifiers. Não derivar crédito de kill/XP/Mastery da existência do atributo.

Os valores internos dos mapas são documentados no dossiê suplementar, mas os efeitos completos dos owners de combate/armadura permanecem responsabilidade de auditorias individuais. Esta ficha de interface não os certifica por associação.

## 6. Interoperabilidade e limites de perks

O Black Arcana detém seu runtime mágico; RPG Skill Tree detém progressão, atributos, Mastery e perks. Modificadores de equipamento são **provider-native**. Uma perk hipotética de velocidade, defesa, duração ou dano precisa identificar um boundary real e server-authoritative que preserve stacking e ownership. **Não há hook mutador por jogador certificado** nesta interface, no fallback de ACCompat ou no builder de atributos; os getters podem ser acessíveis sem que sejam seguros para interceptação.

Nenhum adapter, mixin, novo settlement de dano ou atribuição de XP foi adicionado. **NO_MUTATION / fail-closed**. O retorno null não deve ser substituído arbitrariamente por mapa vazio: a mudança altera a escolha do fallback. O cache de Gingerbread não deve ser mutado globalmente para representar perks individuais sem prova de isolamento.

## 7. Validação e pendências

[Probe nativo](../../../../../docs/qa/alexscaves_1010_dynamic_attribute_probe.py) lê JAR e usa JDK 21; [testes](../../../../../docs/qa/alexscaves_1010_dynamic_attribute_probe_test.py) verificaram **8/8 PASS** no [workflow exato](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44220064013/job/134519414118). Os checks cobrem declaração e roster, classes herdadas, ordens/offsets, null versus vazio, custo da seleção Swiftwood, cache/divisão Gingerbread e fallback do helper; são **testes estáticos**, não GameTests ou QA física.

A [prova compartilhada](../EXACT-DYNAMIC-ATTRIBUTE-DISCOVERY-1.0.10.md) inclui hashes de cada corpo acModifiers, referência de CI, limites do recorte e comando reproduzível. Pendências para certificação plena: concluir a análise dos auxiliares de identidade e natação, fallback/evento do NeoForge 21.1.250 e gates reproduzíveis da auditoria suplementar. Runtime transformado, composição de ItemAttributeModifiers com outros mods/datapacks, lifecycle/reload, interação com atributos e perks de RPG Skill Tree e QA física são limites independentes. Não confundir **interface parcialmente inventariada** com **sete equipamentos completos**.

**Estado final: ⚠️ PARCIAL · NOT_CERTIFIED · NOT_VERIFIED · NOT_TESTED · NO_MUTATION.**
