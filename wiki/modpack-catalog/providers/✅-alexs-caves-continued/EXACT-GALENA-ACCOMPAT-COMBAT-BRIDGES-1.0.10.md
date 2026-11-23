# Galena Gauntlet — pontes ACCompat de combate, mineração e uso (publisher 1.0.10)

**Estado:** ⚠️ subcontrato estático causal do JAR publisher, somente leitura. A ficha individual Galena Gauntlet mantém `static_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `perk_certification=NOT_CERTIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION` e `provider_universe_closed=false`. Este relatório não cria nova raiz de cast, nem aprova hooks, mutação de mundo, Mastery ou gameplay.

## Proveniência e evidências

- Modlist sibling (`neoforge-rpg-skilltree`): Alex's Caves Continued, `modid=alexscaves`, versão **1.0.10**, Minecraft **1.21.1**, NeoForge e Java **21**; arquivo `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`.
- JAR publisher examinado: **75.279.314 bytes**, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, 1.555 classes. Paridade com novo dump da instalação: **NOT_VERIFIED**.
- Relatório Galena anterior, cobrindo 17 métodos do item e 24 da entidade consumidora: **1.780.492 bytes**, SHA-256 `c91a48f9892be09c4ab951c8083703b0c5ffbb026fc43e7d808c2033dde8bba9`. Reusado como fonte autenticada dos callsites, sem copiá-los de outras versões.
- Classe de helpers `com/github/alexmodguy/alexscaves/server/misc/ACCompat.class`: SHA-256 `333738f324e6e9d77a488e14b7e81b169c2b2d4f6db5171206a016ad0271f57b`, classfile major 65, 200 métodos declarados e três campos.
- [Sonda read-only](../../../../docs/qa/alexscaves_1010_galena_combat_helpers_probe.py), [manifesto por método/offset](EXACT-GALENA-ACCOMPAT-COMBAT-BRIDGES-1.0.10.json), [verificador fail-closed](../../../../docs/qa/alexscaves_1010_galena_combat_helpers_checks.py) e [workflow](../../../../.github/workflows/alexscaves-1010-galena-combat-helper-discovery.yml). Relatório `bridge-report.json`: **44.637 bytes**, SHA-256 `a88dbcda0906f344ecfcd8d4ecea0ea7ba0babae2013643f938a1a2604861bfa`, obtido na [run #45175127051](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45175127051), job `137694263147`, artefato `14817659241`, expiração em 07/12/2026. Essa run passou na fase de descoberta; o novo checker deve ser validado em CI na HEAD final.
- Recorte exato: **14 corpos de helpers e 21 calls JVM tipadas**, mais uma lambda resolvida por BootstrapMethods, não toda a classe ACCompat. Os dez helpers NBT e `spawnAtLocation` já possuem provas independentes e não recebem outro certificado aqui.

## Attack damage: atributo, fórmula observada e limites

`ACCompat.attackDamageBonus(ItemStack):double` possui 12 instruções e solicita `ItemStack.forEachModifier(EquipmentSlot.MAINHAND, BiConsumer)` @14. O `invokedynamic` @9 referencia o **BootstrapMethods #2** da classe publisher. A resolução do `MethodHandle` apontou de forma específica para `lambda$attackDamageBonus$2([D,Holder,AttributeModifier):void`, 14 instruções, Code SHA-256 `99b220ffb4dd89e2e6139033eb37924f935fa822ac73bec7bb0732b8cab9d5ca` e instruction SHA-256 `0430f8065da3624f36f6846682d8ee40f60b2267e2de66b912e742121418c48e`. A lambda compara `Holder.value()` com `Attributes.ATTACK_DAMAGE.value()` em `if_acmpne @14` e, quando coincidem, solicita o acúmulo de `AttributeModifier.amount()` em `double[0]` (load @20, `dadd` @25, store @26). Essa soma nominal é parte do cálculo de `MagneticWeaponEntity.getDamageForItem`, **não** o dano final aceito após armadura, eventos, imunidade e PvP.

`ACCompat.damageBonus(ItemStack,LivingEntity):float` (20 instruções) verifica `ServerLevel` @6/@9 e, nesse ramo, chama `EnchantmentHelper.modifyDamage` @28 usando `target.damageSources().generic()` como DamageSource de referência. Não confundir automaticamente esse source **generic** com o `mobAttack` solicitado posteriormente em `MagneticWeaponEntity.hurtEntity`. Fórmula completa do engine e aceitação real não verificadas.

`ACCompat.hurt(Entity,DamageSource,float):boolean` (5 instruções) apenas encaminha para `Entity.hurt` @3 e devolve o booleano. A decisão e o settlement pertencem à engine. `ACCompat.postAttackEffects(LivingEntity,Entity,DamageSource):void` (14) tem gate `instanceof ServerLevel` @8/`ifeq` @11, e então delega a `EnchantmentHelper.doPostAttackEffects` @23; não certifica qual proc realmente ocorreu. `ACCompat.knockback(LivingEntity,double,double,double):void` (6) delega a `LivingEntity.knockback` @5, sem clamp ou hook de perk próprio no wrapper.

Consequência para perks: diferenciar o bônus de atributos MAINHAND e enchantment damage da aceitação real de `Entity.hurt`. Nenhuma chamada local autoriza contabilizar Mastery/XP por tentativa, `setLastHurtByPlayer`, trigger de achievement ou estado intermediário; deduplicação/autoria/hit final continuam **NOT_VERIFIED**.

## Encantamentos, mineração, targeting e escalonamento

`ACCompat.enchantLevel(ItemStack,ResourceKey):int` (24 instruções) itera `ItemStack.getEnchantments().entrySet`, compara `Holder.is(ResourceKey)` @42 e lê `Object2IntMap.Entry.getIntValue` @51 na entrada correspondida. `ACCompat.enchantLevelOn(LivingEntity,ResourceKey):int` (10) solicita `RegistryAccess.registryOrThrow(Registries.ENCHANTMENT)` @10, `Registry.getHolderOrThrow` @16 e `EnchantmentHelper.getEnchantmentLevel(holder,living)` @22. São consultas diferentes: itemstack contra valor de encantamento em entidade. Ausência/transformação de registries e resultado real do engine não foram testados.

`ACCompat.miningEfficiencyBonus(Player,ItemStack):float` (5 instruções) lê `Attributes.MINING_EFFICIENCY` @1 e consulta `Player.getAttributeValue` @4. **O argumento ItemStack não é utilizado no corpo local**: não atribuir a ele fórmula independente de nível do encantamento. `ACCompat.submergedMiningFactor(Player):float` (5) lê `Attributes.SUBMERGED_MINING_SPEED` @1 e consulta `Player.getAttributeValue` @4. A verificação de água e as multiplicações por fadiga, haste, chão e `EventHooks.getBreakSpeed` pertencem a `MagneticWeaponEntity.getDigSpeed`, auditado no [subcontrato de dano/mineração](EXACT-GALENA-GAUNTLET-DAMAGE-DIGSPEED-1.0.10.md). As solicitações de destruição de bloco permanecem no [dossiê world safety](EXACT-GALENA-GAUNTLET-MINING-WORLD-EFFECT-1.0.10.md); não inferir autorização de claims a partir da ausência de chamada direta.

## Uso, cooldown, criação da arma e durabilidade

| Helper | Contrato solicitado pelo bytecode 1.0.10 | Fronteira |
|---|---|---|
| `addCooldown(Player,ItemStack,int)`, 7 instruções | `Player.getCooldowns` @1, `ItemStack.getItem` @5, `ItemCooldowns.addCooldown(Item,int)` @9 | Cooldown por identidade de **Item**; no `releaseUsing`, argumento 5 ticks. Diferente de `playerUseCooldown` da entidade |
| `hurtAndBreakUsedHand(ItemStack,int,LivingEntity)`, 8 instruções | `LivingEntity.getUsedItemHand` @4 → `slotOf(hand)` @7 → `ItemStack.hurtAndBreak` @10 | O slot é derivado da mão em uso, não da identidade do argumento stack. Durabilidade efetivamente consumida, evento e resultado da engine não verificados |
| `createEntity(EntityType,Level)`, 4 instruções | `EntityType.create(level)` @2, retorno da referência @5 | Não comprova entidade não nula, aceitação de spawn ou rollback do esvaziamento da mão oposta |
| `useConsume(ItemStack)`, 3 instruções | `InteractionResultHolder.consume(stack)` @1 | Retorno da interação, não um cast consumado |
| `useFail(ItemStack)`, 3 instruções | `InteractionResultHolder.fail(stack)` @1 | Retorno de falha, sem prova de efeitos externos |

Em `onUseTick`, a arma oposta é copiada e a stack original recebe `setCount(0)` antes de o caller solicitar `Level.addFreshEntity`, cujo booleano é descartado. A presente prova reforça que `createEntity` apenas encaminha uma chamada, **não** resolve atomicidade, perda/duplicação, conservação após reload nem restituição; remeter ao [dossiê retorno/drop](EXACT-GALENA-GAUNTLET-RETURN-DROP-1.0.10.md).

## Reprodução e integração segura

A CI baixa o publisher exacto, exige SHA-256 e tamanho, reproduz o relatório Galena antigo, gera o report dos 14 helpers e então executa o checker com `--adversarial`. O verificador prende 14 descritores, hashes de `Code` e listas de instruções, **34 pivôs JVM**, 21 callsites e a resolução bootstrap do callback; testa alterações sintéticas re-seladas e tentativas de promover estados sem prova. Não introduz código/asset de terceiro no Black Arcana.

**Limites:** NÃO VERIFICADOS os corpos do Minecraft/NeoForge para `Entity.hurt`, `EnchantmentHelper`, `ItemStack`, `EntityType.create`, `ItemCooldowns`, efeitos de knockback, proteção de mundo, integração externa, mods de claims, launcher físico, multiplayer, save/restart e evolução de inventário. Sem boundary mutador server-authoritative comprovado, preservar `NO_MUTATION` / fail-closed. A ficha de **Galena Gauntlet permanece ⚠️ parcial**, sem alteração do numerador ou universo do provider.