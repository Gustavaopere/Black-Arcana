# Iron's 3.16.3 — Slow: efeito de atributos, magnitude e duração

**Estado:** ✅ inspeção `SOURCE-PINNED / CAUSAL-PARTIAL`; ⚠️ comportamento exato no runtime NeoForge/IronsLib, config do pack e adapter RPG ainda não testados. Identidade já presente: `irons_spellbooks:slow`, sem aumentar o numerador de 110 magias. Código `iron431/irons-spells-n-spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252`, versão documental 3.16.3 para MC 1.21.1.

[Ficha de gameplay](../evocation/slow.md). A fonte do catálogo público permanece separada do contrato de mutabilidade.

## Sequência técnica

1. **Valores base:** [`SlowSpell`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/evocation/SlowSpell.java#L32-L70) usa escola Evocation, rarity EPIC, máximo 4, cooldown default **80 s**, tipo `LONG`, `castTime=30` ticks, mana base **50+10×(level−1)**. Spell power **20+4×(level−1)**, sujeito a multiplicadores de power e escola/provider. Cast time e cooldown efetivos podem diferir por config/atributos.
2. **Alvo pré-cast:** [`checkPreCastConditions`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/evocation/SlowSpell.java#L78-L81) chama `Utils.preCastTargetHelper(...,32,0.35,true,predicate)`, filtrando o próprio caster e alvos aliados por `DamageSources.isFriendlyFireBetween`. Isto é alcance de aquisição de **32 blocos**, inflação de mira de 0,35 e **um alvo `LivingEntity`**, não AOE. [`Utils.preCastTargetHelper`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L665-L706).
3. **Execução final:** [`onCast`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/evocation/SlowSpell.java#L83-L92) recupera `TargetEntityCastData` no `ServerLevel` e aplica `new MobEffectInstance(MobEffectRegistry.SLOWED,duration,amplifier,false,false,true)`, além de partículas. O caster original fornece duração e magnitude. Não há explosão, projétil ou dano direto nesse método; `SpellDamageEvent` não é o mecanismo de alteração do debuff.
4. **Duração:** [`getDuration`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/evocation/SlowSpell.java#L99-L101) = `(int)(getSpellPower(level,caster)×20)` ticks. Com multiplicadores unitários, níveis 1–4 produzem **20/24/28/32 segundos nominais**; não são caps globais quando atributos/config podem alterar power.
5. **Intensidade:** [`getAmplifier`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/evocation/SlowSpell.java#L94-L97) = `(int)(7×getEntityPowerMultiplier(caster))`. **O nível da magia não aparece explicitamente nesta expressão.** Com multiplicadores unitários, amplifier **7**. [`SlowedEffect.getPercentForAmplifier`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/effect/SlowedEffect.java#L11-L26) = `(amplifier+1)×0.025` ⇒ **20% nominal** no amplifier 7. A função não declara clamp nesta classe: testar condições extremas e API de atributos.
6. **Atributos realmente afetados:** [`MobEffectRegistry.SLOWED`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/registries/MobEffectRegistry.java#L57-L62) usa modificadores `ADD_MULTIPLIED_TOTAL` de **−0,025 por passo efetivo** em `MOVEMENT_SPEED`, `ATTACK_SPEED`, `CAST_TIME_REDUCTION` e **−0,05 por passo** em `IronsLib MINING_SPEED`. Para amplifier 7, o componente nominal é −20% para os três primeiros e −40% para mineração, **sem garantir que a redução final de ações/swing/cast em jogo seja linear**, pois as outras fórmulas e soft-caps consomem atributos.
7. **Relação com casting:** [`AbstractSpell.getEffectiveCastTime`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L244-L258) obtém `CAST_TIME_REDUCTION` e passa o valor por `Utils.softCapFormula`. Logo, Slow afeta o **atributo de redução de tempo**, mas não injeta diretamente `+20%` no tempo de conjuração; qual é o acréscimo efetivo depende do atributo resultante e do tipo de cast.
8. **Counterspell/dispel:** `SlowedEffect` estende `CustomDescriptionMobEffect` que estende `MagicMobEffect`. Como [`CounterspellSpell.onCast`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/ender/CounterspellSpell.java#L99-L106) remove efeitos ativos cujo `value() instanceof MagicMobEffect`, Slow é **elegível para esse filtro** quando Counterspell processa o alvo sem veto. [hierarquia](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/effect/CustomDescriptionMobEffect.java#L1-L18); isso não garante sucesso em qualquer cenário/contra qualquer mod.
9. **Admissão vs custo:** `SpellPreCastEvent` ocorre depois do gate base de mana. `SpellOnCastEvent.setManaCost` altera a cobrança posterior, mas não torna válido um cast que `canBeCastedBy` já recusou. [`AbstractSpell`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/spells/AbstractSpell.java#L263-L321).

## Matriz por eixo

| Eixo de perk | Prova real | Boundary seguro |
|---|---|---|
| Duração | `(int)(power×20)` | ⚠️ escalonamento indireto com spell power; não comprova setter isolado de duração |
| Intensidade | `(int)(7×entityPowerMultiplier)` | ⚠️ scaling indireto possível via atributos; pode afetar **outras** magias, não é setter per-spell/per-target |
| Tipo de status | `MobEffectRegistry.SLOWED` em LivingEntity | ⛔ sem hook específico de substituição do efeito em `SlowSpell.onCast` validado |
| Número de alvos | helper único + `TargetEntityCastData` | ⛔ sem safe hook multi-target/AoE |
| Alcance | 32 blocos de preflight | ⛔ não misturar alcance de target com duração ou power |
| Movimento/ataque/cast/mineração | quatro modificadores, mineração usa 2× magnitude-base | ⚠️ verificar fórmula final com IronsLib, atributos externos, caps e stacking |
| Damage/DamageType | `onCast` não aplica dano direto | N/A para perk de dano via `SpellDamageEvent` nesta magia |
| Dispel | efeito herda `MagicMobEffect` | ⚠️ compatibilidade provider-native depende de sucesso do Counterspell |
| Custos | 50–80 mana / 80 s default | ⚠️ permanece owner do provider; nenhum novo pool ou cobrança duplicada |

## Checklist de aceitação

- [ ] Confirmar classfiles da versão física Iron's 3.16.3 e config carregada.
- [ ] Testar alvo aliado/self, LOS/aim-assist, desaparecimento do alvo durante `LONG`, PVP e mobs resistentes.
- [ ] Testar tempos reais no servidor para amplifier 7, power alterado, IronsLib `MINING_SPEED`, buffs combinados e caps.
- [ ] Testar `MobEffectInstance` refresh/reaplicação, counterspell/dispel, save/reload e efeito em caster longo.
- [ ] Verificar se algum listener expõe evento de modificação do `MobEffectInstance` com contexto suficiente, antes de classificar perk como API estável.
- [ ] Validar adapter RPG e permissões do Black Arcana sem tocar o processamento interno do Slow provider.

Interoperabilidade clean-room: descrição técnica e links source-pinned, sem cópia de implementação, assets ou código do provider.
