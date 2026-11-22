# Galena Gauntlet — dano solicitado, efeitos pós-ataque, desgaste e velocidade de mineração (publisher 1.0.10)

**Estado:** ⚠️ subcontrato de **observação estática SHA-exata**. A ficha `equipment/galena-gauntlet.md` continua `static_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED` e `NO_MUTATION`; o universo completo de Alex's Caves permanece aberto. Esta análise não certifica dano liquidado, evento de perk, derrubada de bloco, conservação de item nem a semântica dos helpers externos.

## 1. Identidade e reprodutibilidade

- **Provider:** Alex's Caves Continued; mod ID `alexscaves`; Minecraft 1.21.1 / NeoForge; versão publisher **1.0.10**. Arquivo `alexscaves-1.0.10-neoforge+1.21.1.jar`, **75.279.314 bytes**, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. A paridade com o JAR extraído da instalação atual permanece **NOT_VERIFIED**.
- **Classe nativa:** `com/github/alexmodguy/alexscaves/server/entity/item/MagneticWeaponEntity`, SHA-256 `a26794c9eba89c554e812078886beda6129d5298219f685f6d0e2be315fbf071`. O relatório registra 24 métodos executáveis nesta classe e varredura de 1.555 classfiles.
- **Evidência reutilizada, sem promoção de certificação:** `report.json` do workflow [#45071358036](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45071358036), artefato #14773961125; tamanho **1.780.492 bytes**, SHA-256 `c91a48f9892be09c4ab951c8083703b0c5ffbb026fc43e7d808c2033dde8bba9`. Relatório original reproduzido pelo auditor de descoberta da Galena, com JAR publisher verificado.
- **Nova prova causal:** `docs/qa/alexscaves_1010_galena_damage_digspeed_checks.py` verifica descritores, SHA do atributo `Code`, SHA da lista de instruções e **90 offsets/opcodes/operandos** em `getDamageForItem` (3 instruções), `damageItem` (37), `hurtEntity` (141) e `getDigSpeed` (80). Os testes adversariais internos alteram 18 opcodes e um destino de salto, exigindo rejeição por drift causal independentemente da rejeição criptográfica. A CI reproduz e confere separadamente o SHA fixo do relatório. Não reutiliza certificação de um método para outro.

## 2. Cálculo do dano solicitado e atribuição

A rota `hurtEntity(LivingEntity controller, Entity target)` primeiro obtém o `ItemStack` controlado e lê o atributo **`Attributes.ATTACK_DAMAGE`** do controller @6–12. Soma o retorno de **`getDamageForItem(stack)`** @15–19, que delega a `ACCompat.attackDamageBonus(stack)` @1 do método próprio. Para `target instanceof LivingEntity` @33, soma ainda `ACCompat.damageBonus(stack,target)` @39–50. As conversões `d2f` e operações `fadd` são explícitas no bytecode.

**Valor de dano encaminhado ao helper (não dano efetivamente aplicado):**

`D_solicitado = float(ATTACK_DAMAGE_controller) + float(ACCompat.attackDamageBonus(stack)) + [se target LivingEntity: ACCompat.damageBonus(stack,target)]`.

O método constrói `DamageSources.mobAttack(controller)` @88–97 e pede `ACCompat.hurt(target, source, D_solicitado)` @99. **Não há valor de dano-base numérico fixado** nesse método. Fórmulas internas, cap/clamp, resistência, invulnerabilidade, eventos, mitigação, PvP e condições de aceitação dos helpers/engine **NÃO VERIFICADOS**. Não inferir que todo pedido de dano foi aceito nem que há um hit por cast.

A variável de knockback é inicializada a partir de `Attributes.ATTACK_KNOCKBACK` @22–30. Se o alvo for `LivingEntity`, soma `ACCompat.enchantLevelOn(controller, Enchantments.KNOCKBACK)` @52–63. **Apenas quando `ACCompat.hurt` retorna verdadeiro** @99–102, o método solicita `ACCompat.postAttackEffects(controller,target,source)` @115 e `damageItem(1)` @118–120; se o knockback resultante for positivo e o alvo for vivo do tipo adequado, solicita `ACCompat.knockback(target, K×0.5, sin(yaw), -cos(yaw))` @123–173. Depois solicita fator `Vec3.multiply(0.6,1,0.6)` ao movimento da arma @176–191. Valores aceitos pelo motor físico não foram medidos.

## 3. Fogo e autoria: guardas distintos da aceitação de dano

A rota lê `Enchantments.FIRE_ASPECT` no `ItemStack` @65–72. Se o nível for positivo, **antes da chamada a `ACCompat.hurt`**, solicita `target.igniteForSeconds(4 × nível)` @74–85. Após a guarda de dano e o ramo de knockback, se **a entidade arma** `isOnFire()` @195, solicita `target.igniteForSeconds(5)` @201–205. Essa segunda rota é alcançável após o salto @102 para @194 quando `ACCompat.hurt` retorna falso; **não tratar incêndio como equivalente a dano aceito**. Os efeitos reais e cancelamentos por eventos da engine seguem não verificados.

Ao final, se `controller instanceof Player` **e** `target instanceof LivingEntity` @208–232, o método chama `ItemStack.hurtEnemy(target,player)` @234–242 e `LivingEntity.setLastHurtByPlayer(player)` @243–247. Esses callsites ficam **após** o ponto de convergência @194 e não estão protegidos localmente pelo `boolean` retornado por `ACCompat.hurt`. Portanto não utilizar a atribuição como confirmação independente de dano, abate, XP ou Mastery.

Há ainda a solicitação do trigger `KILL_MOB_WITH_GALENA_GAUNTLET` @273–278 quando o alvo apresenta `getHealth() <= 0` @250–257 **e** `player.distanceTo(target) >= 19.5f` @260–270. Isso é uma condição observada para chamar o trigger, não prova de causalidade da morte, conquista concedida ou kill credit.

## 4. Durabilidade da arma controlada

`damageItem(int amount)` obtém o controller @1; exige `LivingEntity` @8. Se for `Player`, retorna sem desgaste quando `Player.isCreative()` for verdadeiro @21–36. Exige que a stack controlada seja `ItemStack.isDamageableItem()` @40–50. Então solicita `ACCompat.hurtAndBreakUsedHand(stack, amount, livingController)` @53–57. Compara `stack.getDamageValue()` a `stack.getMaxDamage()` @62–70 e, quando o valor não é menor, solicita `remove(DISCARDED)` @73–77. **Não confundir** com custo da própria luva no `use/onUseTick` nem presumir que o callback `hurtAndBreakUsedHand` completou um dano unitário sem auditar o helper e as regras de encantamento.

## 5. `getDigSpeed`: fórmula intermediária, ambiente e evento NeoForge

`getDigSpeed(Player, BlockState, BlockPos)` inicia com `S = ItemStack.getDestroySpeed(state)` @6–12. Somente se `S > 1.0f` @14–18, soma `ACCompat.miningEfficiencyBonus(player,stack)` @21–30. Se `MobEffectUtil.hasDigSpeed(player)` for verdadeiro @32–36, multiplica por `1 + 0.2f × (MobEffectUtil.getDigSpeedAmplification(player)+1)` @39–55. Uma rota `MobEffects.DIG_SLOWDOWN` @57–77 seleciona fatores literais **0.3f, 0.09f, 0.0027f, 0.00081f** @108–141 segundo a tabela local observada para amplificações 0–3; efeitos de amplificações fora dessa tabela e compatibilidade com alterações de registries ainda não foram auditados.

Importante: **`isEyeInFluid(WATER)` e `onGround()` são chamados sobre `MagneticWeaponEntity`**, não sobre o player @144–176. Sob água, o método aplica o multiplicador de `ACCompat.submergedMiningFactor(player)` @154–161; caso a arma esteja fora do chão, divide por **5** @163–176. A etapa final passa `S` a `EventHooks.getBreakSpeed(player,state,S,pos)` @178–190 e devolve o resultado do evento. No `tick`, a seleção de mineração depende adicionalmente de `getDigSpeed > 1.0f` e chama `Level.destroyBlock` apenas em ramos próprios, já identificados na auditoria anterior.

**O evento NeoForge pode alterar o valor calculado**; esta inspeção não demonstra se o servidor permite quebrar o bloco, quem recebe drops, quais permissões de claims prevalecem, ou se um mod de terceiros cancela ou transforma a operação.

## 6. Pontos de design e bloqueios

- **Dano/perks:** atributos do controller, bônus por stack e por alvo, Fire Aspect, knockback e pós-ataque possuem boundaries *observados*, mas **nenhum mutador per-player certificado**. Evitar callbacks duplicados, atribuição de Mastery por tentativa de dano, XP por tick ou procs em acertos negados.
- **Desgaste/recursos:** o pedido `damageItem(1)` só aparece no ramo de retorno verdadeiro de `ACCompat.hurt`; o método pode afetar a durabilidade de outra stack, distinta da luva. Não reembolsar, replicar ou remover itens sem prova de conservação.
- **Mineração/world safety:** não transformar `EventHooks.getBreakSpeed` em autorização para `Level.destroyBlock`, nem ignorar `WorldEffectPolicy`; a mudança de targeting/range não permite bypass de claims.
- **Pendências:** auditar corpos reais dos helpers `ACCompat`, `ProjectileUtil`, dano/morte da engine, eventos de combate e mineração, resultantes da inicialização/perks, estados de propriedade/persistência, artefato físico instalado, cliente, dedicated server, PvP/claims e testes em modpack. Sem hooks reais, **`NO_MUTATION`/fail-closed**.

**Clean-room:** referências são assinaturas, valores escalares, callsites e comportamento observável; nenhuma implementação de terceiro é copiada para Black Arcana. Este dossiê não altera índices nem o numerador de certificação da Gauntlet.
