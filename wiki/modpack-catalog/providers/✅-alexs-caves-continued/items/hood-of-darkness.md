# Hood of Darkness — `alexscaves:hood_of_darkness`

**Estado individual:** ⚠️ contrato técnico parcial; hooks `NOT_VERIFIED`, QA física `NOT_TESTED`, `NO_MUTATION`, provider `OPEN`. É **equipamento condicionante** da ação [Cloak Darkness Incarnate](../actions/cloak-darkness-incarnate.md), **não** outra magia/cast.

## Identidade, parâmetros e aquisição

Resource ID `alexscaves:hood_of_darkness` pelo `ACItemRegistry.HOOD_OF_DARKNESS`, factory `lambda$static$134:()Item` (Code SHA-256 `050f52ecb79c931c3a455149c9f7537653be12d3fc22fe11bf940b207da78dea`), construindo `DarknessArmorItem(ACItemRegistry.DARKNESS_ARMOR_MATERIAL, ArmorItem.Type.HELMET)`. Classe compartilhada `com.github.alexmodguy.alexscaves.server.item.DarknessArmorItem`, SHA-256 `872fc610bac5be6010e3981b001c4088c7227e9cffe7938381c34c2f456c4e9a`, `ArmorItem`, `CustomArmorPostRender`, `ACTickingItem` (dispatcher de inventário existente). JAR publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, 75.279.314 bytes, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`; versão física identificada na modlist, sem novo dump da instalação.

O `ACArmorMaterial` tem fator de durabilidade **15** e array `MAX_DAMAGE_ARRAY=[13,15,16,11]`; `ArmorItem.Type.HELMET.ordinal()` resulta no slot 0 desse contrato, portanto **13×15=195** pontos de durabilidade solicitados na criação. O material declara redução `[4,5,1,1]` por ordinal, encantabilidade **40**, toughness **0.5F** e knockback default **0F**; a propriedade do item usa rarity `RARITY_DEMONIC`. A reparação do material é atribuída a `ACItemRegistry.DARK_TATTERS`. Sem leitura de equipamento físico novo nem prova de buff ou valor final da armadura para todos os modifiers do modpack.

Receita publisher `data/alexscaves/recipe/hood_of_darkness.json`, `minecraft:crafting_shaped`, 4 `alexscaves:shadow_silk` e 1 `alexscaves:occult_gem`, SHA-256 `1c3884eb43c47a87062f28461938a1ba4bde0c5af8676623707915c6a0ff7038`. Configuração/datapacks da instalação: `NOT_VERIFIED`.

## Gate funcional, efeitos e ownership

`DarknessArmorItem.canChargeUp(LivingEntity,boolean)` exige o Hood em `EquipmentSlot.HEAD`, ausência do efeito `DARKNESS_INCARNATE` e `DarknessIncarnateEffect.isInLight(entity,11)==false` — a alternativa `allowCreative=true` só permite desconsiderar luminosidade para jogadores criativos. O Hood não carrega `CloakCharge` por conta própria: `acArmorTick` só carrega a stack `CLOAK_OF_DARKNESS` no servidor. O HUD `hasMeter(player)` exige Hood em HEAD e Cloak em CHEST, além da ausência do efeito; não cria recursos.

A ação do Cloak usa o poder de voo **do provider**, com critério de luz e carga; Hood participa como requisito de elegibilidade. No caminho `DarknessArmorItem.onKeyPacket`, a validação local verifica Hood e ausência do efeito, porém não comprova que o remetente do pacote é o usuário-alvo nem que a peça invocada era o Cloak. O receiver exato e seus riscos estão documentados em [Cloak Darkness Incarnate](../actions/cloak-darkness-incarnate.md). Essa ambiguidade impede tratar `onKeyPacket` como hook seguro de mutação ou de perks.

`getArmorTexture(...)` fornece `alexscaves:textures/armor/darkness_armor.png`; o seletor é apresentação cliente via [CustomArmorPostRender](../EXACT-DARKNESS-PRESENTATION-1.0.10.md), sem dano/mana/cooldown próprios. O estado de armadura e a renderização física permanecem não testados.

## Integração, estado e QA

O Hood não mantém contador próprio de carga; o `CloakCharge` é gravado na stack do Cloak via `CUSTOM_DATA`. Duração do efeito, atributos de voo, sync e riscos de remeter payload são da ação compartilhada, sem novo root mágico. **Candidatos a perks:** disponibilidade do gate de equipamento e eficiência de carga **somente conceitual**; sem `WorldEffectPolicy`/hook server-authoritative confirmado, `NO_MUTATION`. Pendente: renderer no cliente, armadura com quebra/reparo, mudança de equipamento em voo, item-alvo em payload, coexistência com outros mods, morte/reload e QA com claims/multiplayer.
