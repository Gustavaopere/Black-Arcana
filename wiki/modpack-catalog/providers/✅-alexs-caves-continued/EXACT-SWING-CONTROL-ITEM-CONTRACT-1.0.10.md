# ACSwingControlItem — contrato estático delimitado 1.0.10

**CERTIFIED_STATIC_7_AXES / STATIC_TECHNICAL_CATALOG_ONLY / SHA_EXACT_BINARY_BEHAVIOR** — candidato #1126. NO_MUTATION; mutating_hook=NOT_VERIFIED; physical_qa=NOT_TESTED; runtime_dispatch=NOT_VERIFIED; perk_certification=NOT_CERTIFIED; provider_universe_closed=false.

| Eixo | Evidência |
|---|---|
| identity | Publisher 1.0.10 SHA-exact artifact; 1555 classes, interface two abstract methods, one direct implementer, zero inherited and zero exact native member references. |
| behavior | Complete PrimitiveClubItem callbacks, precise comparison opcodes and branches, swingTime=-1 write and true/false return; official external virtual dispatch and cancellation reference. |
| parameters | Scale sampled at 0F, double 0.95 versus float promotion, swing threshold 1F, animation comparisons including NaN; official attack speed delay float(20D*(1D/ATTACK_SPEED)), scale clamp, updateSwingTime reference. |
| targeting | Left click receives Player and Entity; stack and target unused locally; swing receives LivingEntity and requires Player for local predicate/write. No target acquisition, area or damage pipeline certified. |
| costs | No resources, damage, mana, stack consumption or cooldown mutation in local callbacks; swingTime animation state only, attack strength ticker independent in reference. |
| integration | NeoForge IItemExtension/StackExtension virtual bridge and CommonHooks.onPlayerAttackTarget, patch callsites early return; event precedes callback. Swiftwood/dynamic-attributes separate. Client/server runtime and safe mutation not verified. |
| validation | Job 136065187890 replayed native SHA and four tests, official reference boundary SHA; candidate adds replay and canonical index/ledger checks, no physical execution. |

## Delimitação nativa e referência

O [manifesto de descoberta](EXACT-SWING-CONTROL-ITEM-DISCOVERY-1.0.10.json) sela o censo de 1555 classes, dois corpos e nenhum member ref exato nativo. A [prova local](EXACT-SWING-CONTROL-ITEM-DISCOVERY-1.0.10.md) documenta os predicados, offsets, distinção float/double e NaN. Referência oficial Mojang 1.21.1 e NeoForge 21.1.250: [selo](EXACT-SWING-CONTROL-ITEM-CONTRACT-1.0.10.json), job [136065187890](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44669005582/job/136065187890). Relatório nativo 67a3bf38959ca92fd40c7a86ffcfa08fc738e036de2eab9f8fd1b54a4e6db8d2; boundary f186d622fdede1b342e56f71f226a29d65556db3ddb32d61fe5a4d024618034f.

### Despacho e cancelamento

Patch Player.java linha 245: Player.attack chama CommonHooks.onPlayerAttackTarget e retorna se false. CommonHooks posta AttackEntityEvent @12, se cancelado retorna false @27; senão lê main hand @29, se não vazio chama virtual Item.onLeftClickEntity @47. Se o callback retornar true, CommonHooks retorna false @58; se falso ou stack vazio retorna true. Não é uma chamada via ACSwingControlItem; a assinatura coincide com IItemExtension, cujo default retorna false. A precedência é evento, predicado do item, restante do ataque. Não prova aceite do dano.

Patch LivingEntity.java linhas 444–445: lê stack da mão indicada e retorna cedo se não vazio e stack.onEntitySwing(entity,hand) true. IItemStackExtension.onEntitySwing(LivingEntity,InteractionHand) chama virtual Item.onEntitySwing(stack,entity,hand) @17; IItemExtension default de três argumentos delega ao overload de dois @3, cujo default é false. PrimitiveClub implementa o de dois. Isso é causalidade estática de referência, não teste do modpack transformado.

### Fórmulas e estado de referência

Player.getCurrentItemAttackStrengthDelay: float((1D/ATTACK_SPEED)*20D), divisão/dmul/d2f @8/12/13. getAttackStrengthScale(f): clamp((float(attackStrengthTicker)+f)/delay, 0F,1F), @1–14. Os callbacks do clube usam f=0F; o limiar de click é 0.95D (não 0.95F). Player.attack usa strength @71 e reset @100 em referência; MultiPlayerGameMode.attack envia a intenção @16 antes da chamada local Player.attack @31 e reset @35 quando não spectator. Não inferir que bloqueio local suprima pacote ou reset cliente. O patch de swing retorna antes da lógica normal. LivingEntity.updateSwingTime incrementa swingTime quando swinging, zera e limpa flag ao atingir duração, ou zera quando não swinging; escreve attackAnim=float(swingTime)/float(duração) @57. A duração vem de getCurrentSwingDuration, fora do recorte auditado. A atribuição -1 ao swingTime não equivale a reset do attackStrengthTicker.

O contrato de [Swiftwood](enchantments/swiftwood.md) e [atributos dinâmicos](systems/dynamic-attributes.md) fornece a relação de velocidade do clube separadamente; não se presume stack modifiers ativos. Sem extensão de alcance, targeting, damage/knockback, cooldown, mana, Mastery, estado persistente ou sincronização próprios da interface. O Player/stack são recebidos pelo engine; nenhum owner armazenado. Não alterar ou forjar cadência por bypass de evento, reset ou pacote. NO_MUTATION/fail-closed, Black Arcana authority de runtime e RPG Skill Tree provider de progressão.

## Validação

[Auditor nativo](../../../../docs/qa/alexscaves_1010_swing_control_item_probe.py), [boundary](../../../../docs/qa/alexscaves_1010_swing_control_item_boundary.py). Quatro regressões de descoberta aprovadas; replay complementar e índices exigidos no HEAD final. Escopo de suporte, não certificação integral do clube ou provider. +1 ficha, +0 raízes. Próximo ACTickingItem.
