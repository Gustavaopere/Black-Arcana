# lord_attack_speed — Vampirism 1.10.13 · engenharia causal para perks

**Identidade:** `vampirism:lord_attack_speed` · `de.teamlapen.vampirism.entity.player.lord.actions.AttackSpeedLordAction` · instant / aura de velocidade de ataque a aliados.

**Proveniência:** `Vampirism-1.21-1.10.13.jar`, mod ID `vampirism`, SHA-1 instalado `349b6e4ea893c98a580775b1725399903e222228`; registry físico 19/19 ✅ [Java21 #38664546643](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38664546643). Comportamento abaixo é **⚠️ SOURCE_CAUSALITY** do pin `TeamLapen/Vampirism@e1ed095713cef5e9eb151d0ee58908fa830d6bb7`, não equivalência binária integral, valores efetivos de config ou gameplay. `⛔` nenhum adapter per-caster aprovado.

## Eixos e limites de perk

| Eixo | Código verificado e implicação | Mutabilidade |
|---|---|---|
| Alvo e geometria | Usa a mesma LordRangeEffectAction: busca LivingEntity da mesma facção em AABB inflada 10 nos três eixos; skip Player com Lord level ≥ caster. | SEM_HOOK_SEGURO para área, target multipliers ou alterar allegiance e gating Lord. |
| Efeito/nível | Aplica ModEffects.LORD_ATTACK_SPEED por laLordAttackSpeedDuration default **30s×20=600 ticks**, amplifier **0** constante no override, mesmo para Lord level alto. | Buff provider-owned; alteração de atributo de velocidade não equivale a DamageType ofensivo. |
| Cooldown exato vs comentário | getCooldown() soma super.getCooldown (600 ticks) + laLordAttackSpeedCooldown default **120** (config documentada 'In seconds' mas sem *20). Resultado computado no source com defaults = **720 ticks (~36s)**, não 150s. A config efetiva deve ser medida. | Risco de unidade confirma necessidade de QA, sem inventar transformação automática de segundos. |
| Resultado/procs | activate retorna true se a LISTA de facção não estava vazia, ainda que todos os players fossem excluídos por Lord level. addEffect executado no loop não retorna count de receptores tratados. | Não dar Mastery só por ActionActivatedEvent ou successful bool. |
| Damage/custo | Sem hurt, projétil, hitbox, blood debit ou dano diretamente produzido pela action. | N/A damageType e target-of-attack; buffs e cooldown pertencem ao provider. |

## Localizadores

- [Subclasse](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/main/java/de/teamlapen/vampirism/entity/player/lord/actions/AttackSpeedLordAction.java#L8-L33)
- [Classe base](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/main/java/de/teamlapen/vampirism/entity/player/lord/actions/LordRangeEffectAction.java#L20-L56)
- [Config](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/main/java/de/teamlapen/vampirism/config/BalanceConfig.java#L461-L463)
- [ActionEvent — setters de cooldown/duração, veto](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/api/java/de/teamlapen/vampirism/api/event/ActionEvent.java#L37-L78): evento pré-onActivated, não setter de raio/dano/target.

**QA obrigatório:** QA attack speed real antes/depois, level, no-target, all targets excluded, potion duration, cooldown efetivo no ActionHandler, PvP/allied targets, server reload e integração attribute RPG. Não duplicar casts, buffs/consumo nem autoridade da action. **+0 novas identidades; Stage 06.05 🟡; Stage 09 PENDING.**
