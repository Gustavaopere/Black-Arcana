# Aspect of the Shulker

**Dossiê documental — 24/10/2026.** `technical_perk_dossier: 1`; identidade `COUNTED_EXACT`; lógica `SOURCE_PINNED / SOURCE_CAUSALITY`; integração `CONTRATO_CONDICIONAL`; QA físico `PENDING`. **+0 identidades**: buff e bullet são filhos da spell, não novas spells.

## Identidade e proveniência

Provider Fire's Ender Expansion (`mod_id=firesenderexpansion`), spell **`firesenderexpansion:aspect_of_the_shulker`**, escola default `irons_spellbooks:ender`. Declarante `net.fireofpower.firesenderexpansion.spells.AspectOfTheShulkerSpell`; consumer `effects.AspectOfTheShulkerEffect#handleAbility`; projétil `entities.spells.MagicShulkerBullet extends ShulkerBullet`. Efeito registrado `firesenderexpansion:aspect_of_the_shulker_effect`. [Registry][registry], [efeito][effect-registry], [bullet][bullet].

MC1.21.1, JAR registrado **`firesenderexpansion-2.4.1.jar`**, SHA-1 `da87a4a0c926dd75236766584cddbae69c6aeff7`, [publisher8167304](https://www.curseforge.com/minecraft/mc-mods/fires-ender-expansion/files/8167304), [prova binária estática](../EXACT-BINARY-SPELLS-2.4.1.md). Source oficial `FireOfPower/firesenderexpansion-1.21.1@5e4067e8112316f55c9f249530ba1917a7bf6643`, build NeoForge21.1.215/Iron's3.15.6; pack registrado NeoForge21.1.250/Iron's3.16.3. Host consultado Iron's3.16.3 `e4056af90302d37eb1739f5ff05020b020e6e252`. Source↔JAR dos métodos/config efetiva não foram equiparados. All Rights Reserved: fatos/paráfrases/permalinks, sem importar implementação/assets. [Versões][versions], [contratos comuns](../SPELL-PERK-BOUNDARIES-2.4.1.md).

[Guia oficial][description], parafraseado: enquanto o aspecto está ativo, ataques mágicos podem gerar uma bala perseguidora contra a vítima. O consumer usa incoming damage, antes do HP final. Aquisição usa elegibilidade host sem override local de loot/crafting; pesos e rota Survival **NÃO VERIFICADOS**. [Host][host-acquisition].

## Ingresso e pipeline causal

1. Uncommon, níveis default1..5, INSTANT0ticks, self. Wrapper jogador Iron's faz admissão, pre-cast cancelável, evento de cast, débito/cooldown conforme CastSource/config; spell não sobrescreve precondição. `AspectOfTheShulkerSpell#onCast` solicita MobEffectInstance em self, duração `(int)(15P)`, amplifier0, ambient=false/particles=false/icon=true, ignora retorno de addEffect e chama super. Sem recast próprio. [Spell][spell], [host][host-cast].
2. `AspectOfTheShulkerEffect#handleAbility(LivingIncomingDamageEvent)` exige **source.getEntity() LivingEntity com buff**, source instanceof SpellDamageSource e ICD daquele UUID igual0. A vítima é event.getEntity(), não o caster buffado. Não exige localmente amount>0, confirmação de HP, escola Ender, identidade da spell ofensiva ou owner do buff. [Proc][proc].
3. LivingIncomingDamageEvent ocorre após checks de invulnerabilidade, antes da mitigação/HP; listeners posteriores podem cancelar. O handler padrão não demonstra receber eventos já cancelados. Ele próprio não testa logical side; o contexto habitual deriva do posting de dano do host. Portanto o proc não comprova hit final nem deve premiar sucesso por antecipação. [Evento NeoForge][incoming].
4. O handler cria **uma** `new MagicShulkerBullet(level,shooter,victim,Axis.X)`, posiciona no centro da AABB do shooter mais3×altura da bullet no Y, solicita addFreshEntity e então escreve `clamp(configICD,0,Integer.MAX_VALUE)`; retorno de spawn não é examinado. O constructor usado delega ao overload vanilla com shooter/target/axis, não ao overload que recebe EntityType. [Proc][proc], [constructor][bullet].
5. Bullet não sobrescreve tick/hit/dano/speed. **Baseline vanilla1.21.1 verificada nos bytes oficiais:** esse overload escolhe `EntityType.SHULKER_BULLET`, dimensões0.3125×0.3125blocks e owner=shooter; registro alternativo FEE `magic_shulker_bullet`1×1/tracking64 não é selecionado por esse constructor. No hit de entidade, tenta **4 health points** com `DamageSources#mobProjectile(this,livingOwnerOrNull)`, fonte plain de tipo `minecraft:mob_projectile`; somente com hurt=true e vítima Living tenta Levitation200ticks (10s), amplifier0, após efeitos pós-ataque de enchantments. Retorno de addEffect não é examinado. Não há fórmula P nessa baseline, nem SpellDamageSource que reative sozinho o predicado deste proc. [Prova estática e reprodução](../../../../../docs/qa/catalog-firesender-spells-2026-10-24.md#baseline-vanilla-do-aspect), [registro][entity-registry].
   NeoForge21.1.250 patcha colisão não-MISS com EventHooks.onProjectileImpact antes de hitTargetOrDeflectSelf; isso é boundary de impacto, não API de spawn/damage FEE. **Bytes vanilla não homologam a composição NeoForge/modpack:** patches, listeners, mitigação, hit final, homing/lifetime/persistência e source↔JAR FEE continuam condicionados à inspeção/QA correspondente. [Patch][bullet-patch].
6. Map privada static UUID→int começa0 por UUID novo. `#applyEffectTick` decrementa apenas quando >0, a cada tick ativo; `#shouldApplyEffectTickThisTick` sempre true. Remover buff não limpa map; sem tick do efeito o cooldown residual não é decrementado por esta classe. Não há cleanup/serialização/owner de cast nesse map. Expiração/merge de MobEffect e lifecycle da bullet são downstream, não um segundo cast. [Ticks][ticks], [base MagicMobEffect][magic-effect].

## Matriz de parâmetros e alteração por perks

`P=(10+4(L−1))×SPELL_POWER×schoolPower×POWER_MULTIPLIER` por `AbstractSpell#getSpellPower`; valores neutros com multiplicadores1. [Host][host-formulas]. Aumentar P altera **duração do buff**, não demonstra dano/speed da bullet.

| L default | Mana neutra | P neutro | Duração pedida (ticks / s) |
|---|---|---|---|
| 1 | 55 | 10 | 150 / 7.5 |
| 2 | 80 | 14 | 210 / 10.5 |
| 3 | 105 | 18 | 270 / 13.5 |
| 4 | 130 | 22 | 330 / 16.5 |
| 5 | 155 | 26 | 390 / 19.5 |

| Eixo | Valor / consumidor / fase | Boundary, limite e estado | QA |
|---|---|---|---|
| Nível / power / duração | Max default5; `AspectOfTheShulkerSpell#getDuration(int,LivingEntity)=(int)(15P)`, truncamento final, amp0. `#onCast` aplica self. [Spell][spell]. | POWER_MULTIPLIER **CONFIG_NATIVE**, spell_power/ender_spell_power nativos; level events host **HOOK_VERIFICADO**, adapter **CONDITIONAL**. Getter público não é setter; sem cap adicional de duração nesta classe. | Q1/Q2 |
| Cast / mana / cooldown | INSTANT0ticks; `int((55+25(L−1))×MANA_MULTIPLIER)`; cooldown default80s=1600ticks antes de modifiers; sem recast/charge local. Caster paga uma vez pelo buff. [Spell][spell], [host][host-formulas], [ordem][host-cast]. | Mana/cooldown **CONFIG_NATIVE**; SpellOnCastEvent#setManaCost/setSpellLevel reais pré-onCast, mas ingresso usa mana inicial e nível alterado não recalcula custo. Nenhum custo de mana por bullet neste handler. | Q1/Q2 |
| Proc / alvo / trigger | `AspectOfTheShulkerEffect#handleAbility`: fonte Living buffada + SpellDamageSource + ICD0; vítima do incoming;1 tentativa de spawn por evento elegível. Sem range/LOS/ally check extra local. [Proc][proc], [fase][incoming]. | Observer de incoming **HOOK_VERIFICADO**, não confirmação de hit nem setter do target/resolver do proc. **⛔ SEM_HOOK_SEGURO** para multi-target, área, chance ou retarget FEE sem adapter específico. | Q2/Q3 |
| ICD / orçamento | Config SERVER `General.shulker_aspect_internal_cooldown`, default20ticks, worldRestart; uso clamp0..2147483647. Decrementa em ticks ativos, não tempo absoluto. ICD0 permite tentativa por evento, sem cap global/cast na classe. [Config][config], [proc/ticks][ticks]. | **CONFIG_NATIVE** global, não perk por jogador. Map privada sem setter/API; **⛔ SEM_HOOK_SEGURO** para alterar ICD UUID/limpar estado por perk. Não tratar20 como bullet lifetime. | Q2/Q4 |
| Projétil / geometry / trajetória | Constructor vanilla shooter/victim/Axis.X; baseline EntityType.SHULKER_BULLET0.3125×0.3125blocks, spawn Y=centroCasterY+0.9375blocks. Registro alternativo1×1/tracking64 não é selecionado por esse constructor. Sem override FEE de speed/acceleration/spread/pierce/lifetime/resize. [Bullet][bullet], [registro][entity-registry], [proc][proc], [bytes oficiais](../../../../../docs/qa/catalog-firesender-spells-2026-10-24.md#baseline-vanilla-do-aspect). | **BASELINE_BINARIA_VERIFICADA**, composição física **PENDING**; não é AbstractMagicProjectile, setters dele não se aplicam por analogia. **⛔ SEM_HOOK_SEGURO** para resize/homing/speed/count pré-spawn FEE. | Q3/Q5 |
| Dano / tipo / status terminal | Baseline vanilla tenta4HP, tipo minecraft:mob_projectile/plain DamageSource, owner living ou null; com hurt=true+Living tenta Levitation200ticks/amp0. Sem scaling P declarado para bullet. [Bullet][bullet], [prova](../../../../../docs/qa/catalog-firesender-spells-2026-10-24.md#baseline-vanilla-do-aspect). | **BASELINE_BINARIA_VERIFICADA**, resultado no pack **PENDING**. Não passa por helper Iron's/SpellDamageEvent por esta herança; mitigação/listeners continuam autoridade downstream. **⛔ SEM_HOOK_SEGURO** para conversão de tipo/dano por power nesta classe. | Q3/Q5 |
| Impacto / proteção | Patch NeoForge dá onProjectileImpact para colisão não-MISS antes do hit; filtros/resist/PvP/claims próprios do terminal vanilla/pack ainda não fechados. [Patch][bullet-patch]. | Boundary cancelável de impacto **CONTRATO_CONDICIONAL**, não muda autoria, tamanho ou dano por si; precisa prova física. Não transplantar pipeline Iron's AbstractMagicProjectile. | Q3/Q5 |
| Estado / cleanup / persistência | MobEffect beneficial, amp0; addEffect/refresh/remoção host-owned; map static privado sem cleanup/serialização; cooldown residual pode sobreviver ao buff no processo. [Proc/ticks][ticks], [base][magic-effect]. | Sem token de cast na bullet/map provado. Cleanup após remove/death/logout/restart **PENDING**; não escrever map global para simular perk. | Q2/Q4/Q5 |
| Summons / mundo / custos extras | Bullet é projétil derivado, não summon com AI/slots. Sem mutação de bloco/teleporte/fuel/stamina/HP/rollback própria. [Proc][proc], [bullet][bullet]. | Summon cap/AI **N/A**; baseline vanilla recebe shooter como owner, atribuição final no pack **PENDING**. Não criar segunda bullet/cobrança como fallback. | Q3/Q5 |

## Autoria, concepção e pendências

FEE/Iron's controlam buff/cast/recursos; vanilla/NeoForge controlam bullet. RPG Skill Tree/Black Arcana precisam encadear cast→instância de buff→dano ofensivo→proc→bullet→resultado real, sem considerar cada incoming/bullet novo cast/Mastery. UUID do map identifica entidade, não cast. Enshrouded mantém Shroud/classificação próprios: SpellDamageSource de ingresso não prova tipo mágico do dano da bullet.

Assinatura ocupada: auto-buff temporário que gera projétil perseguidor por evento de dano mágico com ICD por entidade. Uma habilidade original com charges explícitas e owner/token persistente é lacuna conceitual, não extensão já disponível.

- **Q1:** config física, nível/power/duração truncada, CastSource/mana/cooldown e buff recusado/mesclado.
- **Q2:** amount0, dano mitigado/cancelado posteriormente, ordem de listeners, múltiplos hits/spells no mesmo tick, buff expirando/recast, nenhuma dupla mana/XP.
- **Q3:** tipo efetivo/owner/target/AABB, spawn recusado, homing/block/entity/impact cancelado, PvP/aliados/claims, distância/dimensão e budgets de bullets.
- **Q4:** ICD20/0/negativo/extremo, remoção/reaplicação, map residual/concorrência, tick por side, morte/logout e restart.
- **Q5:** confirmar baseline4HP/mob_projectile/Levitation200amp0 no pack, speed/lifetime/cleanup/persistência, dedicado/cliente/Survival/sync e dedupe. A baseline binária não encerra estes casos físicos: todos **PENDING**; sem adapter/perk/runtime novo.

[registry]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/java/net/fireofpower/firesenderexpansion/registries/SpellRegistries.java#L13-L27
[versions]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/gradle.properties#L15-L50
[description]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/resources/assets/firesenderexpansion/lang/en_us.json#L47-L48
[spell]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/java/net/fireofpower/firesenderexpansion/spells/AspectOfTheShulkerSpell.java#L23-L78
[effect-registry]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/java/net/fireofpower/firesenderexpansion/registries/EffectRegistry.java#L11-L15
[proc]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/java/net/fireofpower/firesenderexpansion/effects/AspectOfTheShulkerEffect.java#L21-L46
[ticks]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/java/net/fireofpower/firesenderexpansion/effects/AspectOfTheShulkerEffect.java#L23-L62
[config]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/java/net/fireofpower/firesenderexpansion/Config.java#L18-L35
[bullet]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/java/net/fireofpower/firesenderexpansion/entities/spells/MagicShulkerBullet.java#L10-L18
[entity-registry]: https://github.com/FireOfPower/firesenderexpansion-1.21.1/blob/5e4067e8112316f55c9f249530ba1917a7bf6643/src/main/java/net/fireofpower/firesenderexpansion/registries/EntityRegistry.java#L32-L36
[host-formulas]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L148-L241
[host-cast]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L263-L332
[host-acquisition]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L594-L612
[magic-effect]: https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/effect/MagicMobEffect.java#L8-L47
[incoming]: https://github.com/neoforged/NeoForge/blob/e0e7ab5d273fdc034f23fee7bf91c61ae39d3019/src/main/java/net/neoforged/neoforge/event/entity/living/LivingIncomingDamageEvent.java#L15-L28
[bullet-patch]: https://github.com/neoforged/NeoForge/blob/e0e7ab5d273fdc034f23fee7bf91c61ae39d3019/patches/net/minecraft/world/entity/projectile/ShulkerBullet.java.patch#L1-L11
