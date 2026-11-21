# Gingerbread Helmet — atributo Gingerbread dinâmico por durabilidade (1.0.10)

**Estado:** ⚠️ contrato estático individual **PARCIAL**. `STATIC_DISCOVERY_ONLY`, `NO_MUTATION`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `perks_executable=NOT_CERTIFIED`, universo do provider OPEN; **0** novas raízes mágicas. Este item não é uma magia/cast, mas equipa modificadores de armadura e velocidade potencialmente relevantes para perks.

## Identidade, uso e fonte física

- **Provider/mod ID:** Alex's Caves Continued / alexscaves; MC 1.21.1 / NeoForge / Java21; versão instalada declarada **1.0.10**.
- **Resource ID:** `alexscaves:gingerbread_helmet`. **Slot de equipamento declarado:** `ArmorItem.Type.HELMET` no registro do provider 1.0.10, que usa `GINGERBREAD_ARMOR_MATERIAL`. O número ordinal deste tipo em classes externas ainda requer conferência separada.
- **Publisher exato:** `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, 75.279.314 bytes; dump novo da instalação ainda não verificado.
- **Owner de runtime:** `com/github/alexmodguy/alexscaves/server/item/GingerbreadArmorItem`, SHA-256 `918cc76cd122605e6ba7aa2e8d26e1f4891b3ad8f26554b960e9b07412884a27`. Uma classe compartilha os oito métodos entre quatro peças; a ficha não reconta métodos como novas raízes.
- **Modelo:** `assets/alexscaves/models/item/gingerbread_helmet.json`, SHA-256 `50a572c0b4cd7c407c678cd6ca77a5b4cfd8195505361488bda17806c7939c6c`. Textura da armadura selecionada via método nativo: `alexscaves:textures/armor/gingerbread_armor_0.png` quando usada no slot esperado. O método de textura tem guard específico para LEGS.
- **Evidência auditável:** [dossiê causal exato](../EXACT-GINGERBREAD-ARMOR-DISCOVERY-1.0.10.md), [manifesto de oito métodos e recursos](../EXACT-GINGERBREAD-ARMOR-DISCOVERY-1.0.10.json), [prova dinâmica antecedente](../systems/dynamic-attributes.md), [material antecedente](../systems/armor-material.md) e [workflow](../../../../../.github/workflows/alexscaves-1010-gingerbread-armor-discovery.yml).

## Ativação, condições, atributos e fórmulas

**Gatilho:** equipar/avaliar os modificadores do `ItemStack` no sistema de atributos Minecraft/NeoForge. Não há habilidade de cast ou uso ativo próprio no owner (`N/A` para conjuração, mira, cooldown ou mana). O construtor `GingerbreadArmorItem(ACArmorMaterial,ArmorItem.Type)` inicializa `acSlot`, `acDefense`, mapa default e o cache por dano. O material solicita `ArmorMaterial.vanilla()` e `properties(...,type)` à engine.

**Seleção do slot:** `acModifiers(EquipmentSlot,ItemStack)` compara o slot solicitado a `acSlot.getSlot()`. Apenas no slot correspondente calcula os modificadores a partir de `stack.getDamageValue()` e `stack.getMaxDamage()`; nos outros retorna um multimap vazio (**não null**). `getDefaultAttributeModifiers(ItemStack)` delega `this::acModifiers`, a stack e um supplier de fallback ao helper `ACCompat.itemAttributes`. O efeito real depende do dispatch NeoForge e de outros modificadores externos.

**Defesa e durabilidade:** `acDefense=material.defense(type)` solicita `Attributes.ARMOR` com `ADD_VALUE`. O material Gingerbread tem redução por ordinal `[2,4,5,2]`, multiplicador `10`, `MAX_DAMAGE_ARRAY[ordinal]×10=[130,150,160,110]`, encantabilidade `25`, toughness e knockback `0`. Os valores são **por índice ordinal**; sem classfile de `ArmorItem.Type` exato, **não atribuir uma posição desse array a HELMET**. Não deduzir mitigação final nem durabilidade restante da porcentagem de dano automaticamente.

**Velocidade:** `getOrCreateDurabilityAttributes(int damage,int maxDamage)`, 73 instruções, calcula `s=0.1D+0.9D×((float)damage/maxDamage)` e solicita `Attributes.MOVEMENT_SPEED` com `ADD_MULTIPLIED_BASE`. `s` é magnitude de modifier solicitado, **não velocidade absoluta** e não bônus final confirmado em gameplay. Maior valor de dano acumulado na stack aumenta a magnitude nominal da fórmula quando maxDamage permanece fixo e positivo. Não há clamp confirmado nesse corpo local para valores externos fora do domínio normal; a conversão float seguida de double importa para precisão.

**Cache e risco:** `gingerbreadDurabilityDependentAttributes` é `Map<Integer,Multimap>` mantido no objeto do item e indexado por `Integer.valueOf(damage)` **sem maxDamage, stack UUID ou player UUID**. Em cache hit reutiliza o mesmo mapa; em miss produz ARMOR e MOVEMENT_SPEED e grava com `Map.put`. O mapa inicial `defaultAttributes` é separado e registra `0.1D`; não representa o resultado cacheado para toda durabilidade. Não implementar uma perk individual alterando esse cache de item compartilhado.

## Status, targeting, custos, persistência e segurança

**Targeting, alcance, hitbox, AoE, dano ofensivo, projéteis, status e efeitos de mundo:** **N/A no corpo desta classe**. O item altera potencialmente atributos do usuário equipado; o efeito final sobre movimento e defesa depende de engine, componentes, eventos e outros mods. **Custo:** avaliação de `acModifiers` não desconta mana, item ou durabilidade; desgaste, dano sofrido, reparo, encantabilidade e crafting pertencem à engine e produtores externos. O material indica `alexscaves:gingerbread_crumbs` como ingrediente de reparo; execução no pack e aquisição do item são NÃO VERIFICADAS. O avanço `gingerbread_armor` contém critério de inventário para `gingerbread_helmet`, sem provar obtenção.

**Autoria/persistência:** não existe owner UUID próprio no owner da armadura, somente `ItemStack`/slot, campos do item e mapa de cache não serializado explicitamente nessa classe. Durabilidade do `ItemStack`, recarga/cópia, mixins e rebuild de atributos após reload exigem prova externa. Nenhum evento de dano/cast ou kill identificado como base legítima de XP/Mastery. `NO_MUTATION` e fail-closed até hook mutador com contexto de jogador, causalidade e isolamento.

**Boundary:** Black Arcana governa runtime mágico/world safety; RPG Skill Tree fornece progressão/atributos/Mastery/perks somente por contrato real. Candidatos conceituais: movimento, resistência, proporcionalidade de desgaste, custo de reparo; **nenhum está autorizado como mutação**. O evento NeoForge `ItemAttributeModifierEvent` recebe stack/modificadores iniciais e não identifica automaticamente o jogador; não é boundary per-player certificado.

## Validação e pendências

Publisher físico de versão correta lido em [GitHub Actions #44937619871](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44937619871), job 136947609057 PASS; relatório SHA-256 `4b6a0709a167e49ffb4bd04b2949facfc3c7b0e55dad80c28842eaf26f1fbae1` e [manifesto](../EXACT-GINGERBREAD-ARMOR-DISCOVERY-1.0.10.json). Oito métodos Code de `GingerbreadArmorItem`, consumidores `ACItemRegistry`, `ACArmorRenderProperties`, a própria classe e recursos foram delimitados.

**Pendente:** prova de ordinal de `HELMET` na ABI engine NeoForge/Minecraft exata, fórmulas herdadas e interações com enchanting/repairs, modo de aplicação real `getDefaultAttributeModifiers` em cliente+servidor, render/equipamento visual, cache por dano em stacks de maxDamage distinto, save/restart/PvP, modpack+QA física, hooks mutadores. Permanecer **⚠️ parcial** até certificado dos sete eixos pertinente; não promover classe, material ou suporte a quatro certificados automaticamente. Código/asset de terceiro não foi copiado (clean-room).
