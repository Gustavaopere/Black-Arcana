# Enchanter's Scythe — contrato causal de equipamento | Ars Hex 5.0.4b

**Tipo de evidência:** `SOURCE_CAUSALITY`, fonte exata de revisão alinhada à release 5.0.4b; **não** há prova de equivalência integral de bytecode com o JAR instalado nem QA de equip/unequip em jogador real. JAR físico `ars_hex-1.21.1-5.0.4b.jar`, SHA-1 documentado `2354710ea312e2a6e0fbc3eb2dbafb8e06f10cf4`. Minecraft 1.21.1, NeoForge; Malum presente na modlist.

## Identidade
- Registro de item: `ars_hex:enchanter_scythe`, condicionado a Malum, factory `new EnchanterScythe(Tiers.NETHERITE, -4F, 0F, 3.0F, LodestoneItemProperties().stacksTo(1))`. Não reinterpretar os três floats do constructor de Malum como stats finais sem verificar o parent.
- Classe: `com.alexthw.ars_hex.malum.EnchanterScythe extends MagicScytheItem implements ICasterTool, IManaDiscountEquipment`. **Equipamento com spell-on-hit, não novo spell ID.**

## Pontos reais de controle

| Eixo para perk | Contrato verificável no source | Implicação |
|---|---|---|
| Entrada/trigger | `hurtEnemy(stack,target,attacker)` constrói `SpellContext` e chama `resolver.onCastOnEntity(..., target, MAIN_HAND)` antes de `super.hurtEnemy` | hit melee é um ingresso da spell inscrita |
| Tipo de alvo | entidade atingida `target: LivingEntity`; `EntityHitResult(target)` | não há retarget/AOE arbitrário nesta classe |
| Spell scribing | recusa qualquer `AbstractCastMethod` na recipe original; `scribeModifiedSpell` antepõe `MethodTouch.INSTANCE` | targeting é mediado por resolver Ars de toque |
| Poder/dano/AOE | dependem das spell parts inscritas e do host `SpellResolver`; a foice não publica setter próprio de damage/range/AOE | não alterar dano/raio via este wrapper |
| Mana discount | `ceil(Σ[part ∈ NECROMANCY] 0.2 * part.getCastingCost())` | desconto provém de Ars; sem segunda mana |
| Repair | `inventoryTick` chama `RepairingPerk.attemptRepair` para entidade `Player` | não duplicar reparo/tick |
| Boomerang | `LivingDamageEvent.Post` com `ScytheBoomerangEntity`, item `ICasterTool` e owner `LivingEntity` chama `item.hurtEnemy(...)`; caso contrário ramo Reactive condicional | há ingresso secundário por dano do boomerang |
| Tempo/cooldown | não declarados diretamente neste wrapper; determinados por spell Ars/Malum e seus hosts | NÃO VERIFICADO |
| Segurança | `SpellContext` usa cast `(ServerLevel) target.level()` sem guarda local demonstrada | QA de execução do evento no lado servidor, sem afirmar crash |

## Riscos prioritários para perk/Mastery
1. **Proveniência:** evento `LivingDamageEvent.Post` pode acionar `hurtEnemy` sem cast voluntário novo. Não contar hit do boomerang + resolver filho como múltiplos casts ou Mastery sem ID canônico.
2. **Recursos:** `IManaDiscountEquipment` devolve desconto ao host; não presumir que `resolver.onCastOnEntity` prove cobrança/fracasso/sucesso da transação de mana. Testar no servidor com valores antes/depois.
3. **Alteração de alvo/área:** não há API publicada aqui para converter `target` em AOE. Uma perk que faça isso precisa hook no próprio `SpellResolver`/provider, se existir e for seguro, e validação de claims/budgets.
4. **Idempotência:** testar hit corpo a corpo, boomerang, enchant Reactive, golpe bloqueado, múltiplas vítimas, logout/relog, e repetição por evento; medir efeitos emitidos e cobranças exatamente uma vez por ingresso elegível.
5. **Compatibilidade:** Arthost 5.13.1/Malum 1.8.2/Lodestone 1.8.2 e pacote físico ainda não testados em cliente/dedicated servidor conjunto.

**Conclusão de engenharia:** source causal e fórmulas conhecidas; **⚠️ runtime real e atribuição de evento pendentes / ⛔ adapter perk, Mastery, retarget ou mudança de DamageType não habilitados**.

## Proveniência
- [Factory e ramo do boomerang — `MalumCompat.java#L29-L46`](https://github.com/Alexthw46/Ars-Unity/blob/b25528adf8c0135585cd6d654582efa147e0a227/src/main/java/com/alexthw/ars_hex/malum/MalumCompat.java#L29-L46)
- [Scribing, alvo, resolver e mana — `EnchanterScythe.java#L37-L102`](https://github.com/Alexthw46/Ars-Unity/blob/b25528adf8c0135585cd6d654582efa147e0a227/src/main/java/com/alexthw/ars_hex/malum/EnchanterScythe.java#L37-L102)
- [Matriz do provider](../PERK-CAUSAL-ENGINEERING-MATRIX-5.0.4b.md)

**Clean-room:** fatos técnicos de interoperabilidade, sem copiar código do provider nem implementar mecanismo paralelo.
