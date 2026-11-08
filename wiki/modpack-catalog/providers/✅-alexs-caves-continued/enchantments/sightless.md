# Sightless — controle do Totem of Possession sem requisito de olhar direto (1.0.10)

**Estado: ✅ contrato técnico estático individual SHA-exato, com auditoria do JAR, selo reproduzível e regressões semânticas verificadas na PR #1060.** A integração à `main` permanece condicionada à CI geral da revisão. **`mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `NO_MUTATION`.** O efeito é um modificador do [Totem of Possession](../actions/totem-possession-remote-control.md), não uma ação/cast mágico independente.

## 1. Identidade e proveniência

| Campo | Evidência verificada |
|---|---|
| Provider / mod ID | Alex's Caves Continued · `alexscaves` |
| Ambiente | Minecraft **1.21.1**, NeoForge, Java **21** |
| Modlist/JAR | `alexscaves-1.0.10-neoforge+1.21.1.jar`; **75.279.314 bytes** |
| JAR SHA-1 | `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570` |
| JAR SHA-256 | `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c` |
| Enchantment | `alexscaves:sightless` · `ACEnchantmentRegistry.SIGHTLESS` |
| Recurso | `data/alexscaves/enchantment/sightless.json`, **369 bytes** · SHA-256 `1e7d093a0d459e2e6a29b40cd625b4fb1f990285343b53e4421c8f3727b2ecb9` |
| Item/tag | `#alexscaves:enchantable/totem_of_possession` → `alexscaves:totem_of_possession` · SHA-256 `185a085206993877d91ca6d8c697273c14f945b1d55cb6179e3236c138c357cf` |
| Descrição publisher `en_us` (paráfrase) | Permite controlar mobs vinculados ao Totem sem precisar manter linha de visão direta |
| Tradução `pt_br` no JAR | Chaves de Sightless **não encontradas** no locale `pt_br` auditado; não inventar tradução oficial |

**JSON declarado:** `weight=2`, `max_level=I`, `min_cost=1+13×(L−1)`, `max_cost=41+10×(L−1)`, `anvil_cost=4`, `slots=["mainhand"]`; sem `exclusive_set` no recurso. São parâmetros de aquisição do encantamento, **não** cobrança de mana, stamina, dano, alcance ou cooldown de ativação.

O [manifesto SHA-exato de Sightless](../EXACT-SIGHTLESS-STATIC-1.0.10.json), a [sonda read-only](../../../../../docs/qa/alexscaves_1010_sightless_static_probe.py) e o [relatório técnico](../EXACT-SIGHTLESS-STATIC-1.0.10.md) usam o JAR da modlist. Código-fonte adjacente 1.1.1 serve apenas de orientação e não certifica valores da versão instalada.

## 2. Grafo causal e universo de referências

O censo de **1.555 classfiles** do provider encontrou referências binárias diretas a `SIGHTLESS` exclusivamente em `ACEnchantmentRegistry.class` (registro) e `TotemOfPossessionItem.class` (consumidor). É um censo de string/símbolo em bytecode, não prova de ausência de datapacks, invocação reflexiva ou código de outros mods.

Os métodos de `TotemOfPossessionItem` foram inspecionados com `javap` Java 21 e hash do corpo compilado. Principais contratos:

| Método | Instruções / digest do método compilado |
|---|---|
| `use(Level,Player,InteractionHand)` | 66 / `4109cf2033dc2c448aa71707a6f3dcd16b10d7d3e482fbceeba9da6681c2a237` |
| `onUseTick(Level,LivingEntity,ItemStack,int)` | 478 / `4d366c998c89884f53bc9554f52c6477c5c6bbb8e6aea1bf0f93867dc1b41d39` |
| `releaseUsing(ItemStack,Level,LivingEntity,int)` | 29 / `58020e6c31d745f1cfd3a47863efca68eddaf1ee52cfcad5e783f57fb3eade30` |
| `isEntityLookingAt(LivingEntity,Entity,double)` | 70 / `3226c9fb46cf1ee4a4e453886629c5c377800d05b36f8f7e7405ba27ae496e88` |
| `getControlledEntity(Level,ItemStack)` | 44 / `eec3e7482771787aa302b22eaefacb0d5321f438493dd5cef79a0ce01578dd83` |
| `resetBound(ItemStack)` | 16 / `a5802d147771c7e3aabbb3a58451e1b762d66cccd40d5fae43c147672a4c4dab` |

Também foram inspecionados `isBound`, `getBoundEntityUUID`, `updateEntityIdFromServer`, `setPossessed` e `getUseDuration`, totalizando **11 métodos selecionados**. O censo e os hashes exatos não autorizam criar wrappers mutadores nem encerrar o universo de chamadas herdadas da engine. O `onUseTick` foi confrontado com a [prova independente de Astral Transferring](../EXACT-ASTRAL-TRANSFERRING-1.0.10.json), e âncoras selecionadas com o [manifesto anterior de Totem](../EXACT-TECHNICAL-CONTRACTS-1.0.10.json).

## 3. Ativação — diferença entre entrada e manutenção

**Início do uso** (`TotemOfPossessionItem.use`):

- Resolve `controlledEntity`, consulta `isBound(stack)` e, se o vínculo estiver inválido (entidade ausente ou não viva) e o lado não for cliente, solicita `setPossessed(false)` e `resetBound(stack)` (offsets @35–80).
- Para iniciar, exige `isBound(stack)` e entidade controlada não nula (@83–93).
- Depois aceita **olhar válido** via `isEntityLookingAt(...,5D)` (@96–105) **ou** `ACCompat.enchantLevel(stack,SIGHTLESS)>0` (@108–116, `ifle → 145`).
- Quando aceito, solicita som nativo, `Player.startUsingItem(hand)` e `ACCompat.useConsume(stack)` (@119–144); caso contrário, `ACCompat.usePass(stack)` (@145–150).

**Continuidade do uso** (`onUseTick`) tem teste **diferente**: após os filtros de vínculo/existência, falha do olhar com `enchantLevel(stack,SIGHTLESS)==0` conduz a `stopUsingItem()` (@143–174, `ifeq → 203`). Não é um teste de nível positivo. Isso não significa que nível negativo seja aquisição válida: o início continua exigindo `>0` e o JSON limita `max_level=I`. Sob datapacks/valores não previstos, a diferença `ifle` versus `ifeq` deve permanecer explícita.

O código também impede manutenção com `controlledEntity instanceof Player` quando `totemOfPossessionPlayers` está desabilitado no config (@177–200), independentemente de Sightless. Ausência de vínculo, entidade nula/não viva e desgaste até o limite têm caminho de interrupção anterior, com `resetBound`, `stopUsingItem` e envio de `UpdateItemTagMessage` condicionado ao cliente (@8–142). Nesse caminho coexistem outros efeitos, inclusive o encantamento irmão **Detonating Death**, que não deve ser imputado a Sightless.

## 4. Geometria de olhar, distância e targeting

O valor `5D` enviado a `isEntityLookingAt` **não é um alcance máximo de cinco blocos** nem um raio AOE. O helper é um teste angular que consulta distância atual `distanceTo(seen)`, direção normalizada de visão `getViewVector(1F).normalize()`, vetor normalizado rumo à altura de olhos da entidade, produto escalar e `hasLineOfSight(seen)`.

A sequência JVM `@0–14` escala a tolerância por distância:

`tolerânciaEscalada = 5 × (1 + 0,1 × distanceTo(seen))`.

No corpo `@90–124`, compara:

`dot(viewNormalizado, direçãoNormalizada) > 1 − tolerânciaEscalada / comprimentoDoVetor`

**e** exige `hasLineOfSight(seen)`. As operações `dmul`, `dadd`, `ddiv`, `dsub`, `dcmpl` e a guarda `ifle` foram verificadas em janelas do método compilado 1.0.10. Não substituir por cone rígido de 5 graus, por raycast de cinco blocos nem prometer detecção através de qualquer obstrução: Sightless apenas oferece um **bypass do resultado do helper** nos dois pontos de controle documentados. Não altera por si só o processamento de alvos dos demais consumidores.

## 5. Efeito visual de glow e estado durante o controle

O ramo `controlledEntity instanceof Mob` em `onUseTick` primeiro prossegue com a navegação nativa `Mob.getNavigation().moveTo(...)` (@369–407). Dentro desse ramo, **`level(SIGHTLESS)>0`** (@408–415, `ifle → 424`) permite solicitar `controlledEntity.setGlowingTag(true)` (@418–421). Isso não é um novo projétil, dano, status com duração registrada ou uma AOE.

No `releaseUsing`, caso o alvo seja resolvido, é solicitado **`setGlowingTag(false)`** antes de qualquer checagem de lado (@8–19). **Não há captura/restauração do valor anterior do brilho nesse método.** Por isso, caso outro sistema já tenha dado glow ao mob, a limpeza do Totem pode desativá-lo no recorte observado. Esse risco precisa de QA física e de uma política de autoridade antes de qualquer perk que manipule glow. O ramo glow é para `Mob`; a eventual permissão de controle de Player não amplia automaticamente esse efeito visual.

O `releaseUsing` também envia `UpdateItemTagMessage(user.getId(),stack)` do cliente para o servidor (@19–38) e solicita `stack.shrink(1)` quando `getDamageValue()>=getMaxDamage()` (@41–54). Glow e desgaste são decisões distintas: o release força glow `false` mesmo sem prova de que Sightless havia ativado glow anteriormente.

## 6. Custo, duração e outros efeitos compartilhados

`onUseTick` verifica **`timeUsing % 2 == 0`**, `Level.isClientSide()` e usuário não criativo antes de solicitar `ItemStack.setDamageValue(getDamageValue()+1)` (@230–272). Esta escrita aparece **no caminho cliente** da versão instalada; **não comprova débito de durabilidade autoritativo no servidor**, sincronização correta, rollback ou resistência a manipulação de mensagens. O método de release pode consumir a stack quando seu dano já atingiu o máximo; não confundir essa condição com custo de Sightless por nível.

O método próprio `getUseDuration(ItemStack)` retorna o literal **72.000**, mas `onUseTick` invoca a assinatura `getUseDuration(ItemStack,LivingEntity)`, que é outra fronteira de API/herança no Java da release: não declarar equivalência de retorno só por semelhança do nome. Esse limite de uso não é um cooldown individual nem duração de glow certificada.

O Totem continua utilizando os parâmetros já analisados do controle remoto e a movimentação do Mob/não-Mob; **Sightless não introduz no seu próprio ramo** multiplicador de velocidade, valor de dano, `DamageSource`, raio de dano, cura, projéteis, custo mágico ou aquisição de um novo alvo. O uso nativo pode produzir efeitos por [Rapid Possession](rapid-possession.md), [Astral Transferring](astral-transferring.md) e [Detonating Death](detonating-death.md), que têm contratos próprios e não devem ter seus parâmetros contados como componentes adicionais de Sightless.

## 7. Owner, sincronização, persistência e segurança

`getControlledEntity` usa **`ControllingEntityID`** da custom data da stack para procurar `Level.getEntity(id)` no cliente; na rota de `ServerLevel`, usa **`BoundEntityUUID`** e `ServerLevel.getEntity(uuid)`. São identificadores diferentes, com disponibilidade dependente do mundo carregado. `updateEntityIdFromServer` é um método de sincronização selecionado; a auditoria de seu corpo e mensagens não equivale a prova de autorização do remetente.

`resetBound` remove `BoundEntityTag`, `BoundEntityUUID` e `ControllingEntityID` da custom data da stack. O release por si só **não executa esse reset** no corpo observado. A marcação `setPossessed`, compartilhada com o Totem, exige atribuição e política próprias; não presumir limpeza integral da entidade, proteção de claims/PvP, multiplayer ou manutenção da identidade do alvo após unload/reload/troca de dimensão.

## 8. Matriz de perks, atributos e Mastery

| Eixo | Contrato de interoperabilidade | Limite fail-closed |
|---|---|---|
| Gate inicial | `bound && controlledEntity!=null && (looking || level>0)` | Não permitir cast sem vínculo/alvo válido |
| Gate durante uso | `!looking && level==0` implica interrupção, junto aos demais filtros | Não equiparar `==0` com `<=0`; corrigir só após contrato mutador real |
| Targeting | Helper com tolerância angular dependente de distância + LOS | Não tratar 5D como range máximo nem ignorar world safety/PvP |
| Glow | Solicitação de `true` para Mob com nível positivo; release força `false` | Não restaurar estado preexistente por suposição; não criar loop próprio de status |
| Movimento e dano | Permanecem no Totem e em encantamentos irmãos | Não duplicar casts, pathfinding, dano, alvo ou XP |
| Desgaste | Incremento solicitado no cliente a cada 2 ticks elegíveis; release pode reduzir stack no limite | Não converter automaticamente em custo server-owned ou custo por perk |
| Owner e reload | Bound UUID servidor / entidade ID cliente; custom data da stack | Não creditar Mastery sem identidade/ação aceitas; testar reload/dimensões |
| Hooks e QA | `NOT_VERIFIED` / `NOT_TESTED` | **`NO_MUTATION`**, sem adapter imaginário |

## 9. Validação e pendências

A certificação estática individual requer [manifesto reprodutível](../EXACT-SIGHTLESS-STATIC-1.0.10.json) de recursos, censo de classfiles e 11 métodos SHA-exatos, regressões [`sightless_cards_test.py`](../../../../../docs/qa/alexscaves_1010_sightless_cards_test.py), sonda `--seal`, verificador de 544 índices e CI integral. A versão do método `onUseTick` conserva digest **`4d366c998c89884f53bc9554f52c6477c5c6bbb8e6aea1bf0f93867dc1b41d39`**, idêntico ao manifesto independente de Astral Transferring.

**PENDÊNCIAS distintas do contrato estático:** implementação mutadora, revisão de segurança da mensagem de atualização de item, atributos/perks e Mastery com de-duplicação; QA física de cliente/servidor, glow já existente, alvo morto/nulo, player-control config, valores de nível fora do JSON, recarga, desgaste cliente/servidor, PvP/claims e reload. Nenhum Java de runtime, Stage, datapack ou hook de terceiro foi alterado. **`NO_MUTATION`** permanece obrigatório.
