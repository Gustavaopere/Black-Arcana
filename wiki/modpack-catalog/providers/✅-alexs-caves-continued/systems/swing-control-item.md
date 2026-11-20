# ACSwingControlItem — controle de golpe e animação

**Contrato técnico estático:** ✅ CERTIFIED_STATIC_7_AXES / STATIC_TECHNICAL_CATALOG_ONLY, candidato #1126. Hook NOT_VERIFIED; runtime NOT_VERIFIED; physical_qa NOT_TESTED; perk NOT_CERTIFIED; NO_MUTATION; provider OPEN.

## Identidade

Interface com.github.alexmodguy.alexscaves.server.item.ACSwingControlItem, mod alexscaves, publisher 1.0.10, Minecraft 1.21.1, Java 21, NeoForge de referência 21.1.250. JAR SHA-1 6960b299a39a039ac8a5eb9b07be4ad0e3e0a570, SHA-256 36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c, 75279314 bytes; classe SHA-256 0fc278b0860306f7746dd2dc445712b42ca4d227d1ec154dfff11471aa67cee3. Não é cast/item independente nem adiciona nova raiz mágica. Um implementador direto, PrimitiveClubItem, sem indiretos; duas declarações abstratas, nenhum campo. Censo tipado 1555 classes, zero chamadas nativas de membros exatos da interface.

## Ativação, condição e efeitos

| Callback | Resultado local |
|---|---|
| onLeftClickEntity(ItemStack,Player,Entity)Z | true se escala de ataque em f=0F promovida a double inferior a 0.95D OU attackAnim !=0F; false caso contrário |
| onEntitySwing(ItemStack,LivingEntity)Z | não-Player false; Player true se escala inferior a 1F E attackAnim>0F; caso contrário escreve swingTime=-1, retorna false |

Left click @2, @6–10, @14–19; swing @14, @18–28, @35. NaN: left scale NaN não satisfaz inferior a 0.95D; animation NaN satisfaz !=0. Swing scale NaN ou animation NaN não satisfaz a conjunção. 0.95F promovido é inferior a 0.95D. Stack e target não são lidos pelo predicado. Nenhum guard de lado ou null local.

## Parâmetros e consumidores

Na referência oficial, delay em ticks = float((1D/ATTACK_SPEED)*20D), strength = clamp((float(ticker)+f)/delay,0F,1F). Animação usa swingTime/duração; reset de swingTime não reseta força de ataque. [Swiftwood](../enchantments/swiftwood.md) e [atributos dinâmicos](dynamic-attributes.md) descrevem o modificador de velocidade, não o dispatch do modpack. Duração do swing não certificada neste escopo.

Player.attack recebe o resultado de CommonHooks.onPlayerAttackTarget (AttackEntityEvent antes de Item.onLeftClickEntity; true do callback impede o restante do ataque). LivingEntity.swing verifica stack da mão e retorna cedo quando stack.onEntitySwing=true; IItemStackExtension e IItemExtension encaminham para a assinatura de dois args. Cliente pode enviar intenção antes da chamada local; sem presumir bloqueio de rede. Ver [fronteira e offsets](../EXACT-SWING-CONTROL-ITEM-CONTRACT-1.0.10.md).

## Custos, estado e interoperabilidade

Sem dano diretamente solicitado, mana, consumo de item, cooldown próprio, AOE, range, projétil, duração de feitiço, owner ou persistência própria; N/A por ser predicado e manipulação local de animação. Não tratar true como dano aplicado ou crédito Mastery. Não duplicar ataques, forjar packets ou resetar ticker para perks. Potência/cadência por atributo real e políticas de servidor exigem validação própria. NO_MUTATION/fail-closed. Black Arcana mantém runtime de magia, RPG Skill Tree fornece progressão. Transformação instalada, lado de execução, eventos concorrentes, QA física e segurança de hook NÃO VERIFICADOS.

[Prova](../EXACT-SWING-CONTROL-ITEM-CONTRACT-1.0.10.md) · [selo](../EXACT-SWING-CONTROL-ITEM-CONTRACT-1.0.10.json) · [descoberta](../EXACT-SWING-CONTROL-ITEM-DISCOVERY-1.0.10.md). Relatórios 67a3bf38959ca92fd40c7a86ffcfa08fc738e036de2eab9f8fd1b54a4e6db8d2 e f186d622fdede1b342e56f71f226a29d65556db3ddb32d61fe5a4d024618034f. Quatro testes nativos aprovados, CI final exigida. Próximo ACTickingItem.
