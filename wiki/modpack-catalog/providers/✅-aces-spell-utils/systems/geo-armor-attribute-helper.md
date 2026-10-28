# ExtendedGeoArmorItem — atributos por slot e recipiente do peitoral

**Provider:** Ace's Spell Utils `1.2.7.2-1.21.1` · **tipo:** API de equipamento · **estado:** ⚠️ `SOURCE_VERSION_ONLY`, integração `CONDITIONAL`, sem certificação de perk.

As bases reutilizáveis `ExtendedGeoArmorItem` e **`ImbuableExtendedGeoArmorItem`** vivem em `net.acetheeldritchking.aces_spell_utils.items.example.items.armor`; a grafia real da segunda é `Imbuable`. A localização sob `example` não remove sua API. Esta ficha cobre composição de atributos, inicialização do recipiente e ciclo do provider de render; [as peças concretas](../examples/example_armor_chestplate.md) e [a camada emissiva](emissive-geo-armor-rendering.md) têm escopos próprios. Nenhuma base registra spell.

## Construção e operações dos atributos

O [construtor][constructor] recebe `Holder<ArmorMaterial>`, `ArmorItem.Type`, `Properties` e `AttributeContainer...`. Constrói um `Supplier<ItemAttributeModifiers>` memoizado, retornado por [`getDefaultAttributeModifiers()`][getter]. Quando o supplier é avaliado, lê defesa/toughness/resistência do material, usa `EquipmentSlotGroup.bySlot(type.getSlot())` e ID base `minecraft:armor.<type.getName()>`:

| Entrada | Valor / operação no grupo do slot |
|---|---|
| `Attributes.ARMOR` | `material.getDefense(type)`, `ADD_VALUE` |
| `Attributes.ARMOR_TOUGHNESS` | `material.toughness()`, `ADD_VALUE` |
| `Attributes.KNOCKBACK_RESISTANCE` | `material.knockbackResistance()`, `ADD_VALUE`, somente se valor > 0 |
| Cada `AttributeContainer` fornecido | `holder.createModifier(type.getSlot().getName())` |

As [factories públicas][factories] devolvem arrays de containers, sem clamp/default particular:

| Factory | Modificadores produzidos |
|---|---|
| `schoolAttributes(school,mana,schoolSpellPower,spellPower)` | `MAX_MANA`: `mana ADD_VALUE`; holder `school`: `schoolSpellPower ADD_MULTIPLIED_BASE`; `SPELL_POWER`: `spellPower ADD_MULTIPLIED_BASE` |
| `schoolAttributesWithResistance(school,resistSchool,mana,schoolSpellPower,spellPower,resistSpellPower)` | Os anteriores, mais holder `resistSchool`: `resistSpellPower ADD_MULTIPLIED_BASE` |

O nome `resistSchool` não valida que o holder seja resistência. O [consumidor ExampleWarlockArmorItem][example] passa `ELDRITCH_SPELL_POWER,MANA_REGEN,150,0.10F,0.05F,0.05F`: por peça são **+150 MAX_MANA ADD_VALUE**, coeficiente **0.10 ELDRITCH_SPELL_POWER**, **0.05 MANA_REGEN** e **0.05 SPELL_POWER**, estes três `ADD_MULTIPLIED_BASE`. MANA_REGEN continua regeneração. Esses são os termos adicionados aos atributos; valor final depende de base/outros modifiers e regras host, sem garantir um valor percentual final nem somar o mesmo bônus por perk.

No [source host Iron's 3.16.3 consultado][modifier], `AttributeContainer.createModifier(slot)` gera `irons_spellbooks:<slot>_<attribute-path>_modifier`, usando o path sem namespace do atributo. Colisões de ID/slot e stacking entre itens precisam de QA. A memoização da lista não é um setter de perk ou recomputação por tick: material/array mutados posteriormente não garantem novos modifiers.

## Recipiente: somente peitoral, preservando o existente

[`ImbuableExtendedGeoArmorItem`][container] implementa `IPresetSpellContainer`. `initializeSpellContainer(stack)` retorna para null, exige `stack.getItem() instanceof ArmorItem` com tipo `CHESTPLATE` e só quando `!ISpellContainer.isSpellContainer(stack)` grava `ComponentRegistry.SPELL_CONTAINER = ISpellContainer.create(1,true,true)`. Não inicializa capacete/calças/botas, não substitui recipiente existente e não concede spell/nível. Não há guarda local de lado nem cast nesse callback.

No [contrato Iron's 3.16.3 lido][host-container], os argumentos significam capacidade 1, `addsToSpellWheel=true` e `mustBeEquipped=true`; seu [ItemStackMixin][host-init] chama `IPresetSpellContainer.initializeSpellContainer` na cauda do construtor de ItemStack indicado. É evidência de consumer host, sem comprovar aplicação desse mixin no JAR instalado ou compatibilidade com a dependência Ace 3.16.2. Seleção, custo, admissão, cooldown e execução de uma spell posteriormente inserida continuam no host.

## Ciclo de animação e provider

[`registerControllers`][controllers] registra um controlador chamado **`controler`**, cujo predicado seleciona loop `idle` e retorna `CONTINUE`; `getAnimatableInstanceCache()` devolve o cache GeckoLib criado para o item. Esse ciclo não produz cura, dano, cast, proc ou Mastery.

[`createGeoRenderer`][provider] entrega um `GeoRenderProvider` anônimo. O callback `getGeoArmorRenderer(...)` chama `supplyRenderer()` enquanto o campo local de renderer está null e retorna o resultado. A implementação base de `supplyRenderer()` é `@OnlyIn(Dist.CLIENT)` e retorna **null**; o consumidor precisa fornecer o renderer. Como null não preenche o cache, chamadas seguintes podem repetir o supplier. Anotação client e lazy lookup não são prova de classloading seguro em dedicado.

O alvo dos modifiers é o portador no slot do equipamento, sujeito à resolução vanilla/host; o recipiente fica no ItemStack do peitoral. As classes não definem inimigo, raio, LOS, projétil, dano, mana cost, cast time, cooldown ou duração de habilidade. Atributo MAX_MANA não é cobrança de mana. Animação/renderer não alteram hitbox, reach ou permissão de mundo.

## Integração e QA

Factories/construtores e callback de inicialização são APIs nativas. Alteração dinâmica por jogador/perk exige contrato de IDs, sync, remoção e persistência; capacidade diferente do recipiente e troca de spell não têm override seletivo comprovado aqui. Não duplicar os modifiers de equipamento em RPG Skill Tree nem executar cast no callback/frame. Black Arcana conserva seu runtime e WorldEffectPolicy; RPG Skill Tree conserva a progressão por contrato comprovado; Iron's conserva recipiente/casting e GeckoLib conserva apresentação.

QA pendente: quatro slots, composição de peças/IDs, troca e remoção de equipamento, valores base/finais/sync, peitoral vazio/existente/copiado/carregado, preservação de spell e client/dedicado. Nenhum teste físico foi executado nesta ficha.

Pin Ace `a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`; JAR anotado `aces_spell_utils-1.2.7.2-1.21.1.jar`, SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca`, sem paridade source/JAR demonstrada. Source Ace depende de Iron's `3.16.2`; contratos host acima foram lidos separadamente em `3.16.3@e4056af90302d37eb1739f5ff05020b020e6e252`, sem certificar a combinação. `source_pinned=true` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `COMPLETE_PERK_READY=false` · **+0 magias registradas, +0 perks implementadas.**

[constructor]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/example/items/armor/ExtendedGeoArmorItem.java#L32-L61
[getter]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/example/items/armor/ExtendedGeoArmorItem.java#L81-L84
[factories]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/example/items/armor/ExtendedGeoArmorItem.java#L63-L79
[example]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/example/items/armor/ExampleWarlockArmorItem.java#L15-L18
[modifier]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/item/weapons/AttributeContainer.java#L10-L14
[container]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/example/items/armor/ImbuableExtendedGeoArmorItem.java#L13-L37
[host-container]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/ISpellContainer.java#L41-L47
[host-init]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/mixin/ItemStackMixin.java#L12-L19
[controllers]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/example/items/armor/ExtendedGeoArmorItem.java#L86-L101
[provider]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/example/items/armor/ExtendedGeoArmorItem.java#L103-L121
