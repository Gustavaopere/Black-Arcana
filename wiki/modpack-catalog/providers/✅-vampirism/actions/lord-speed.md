# lord_speed — Vampirism 1.10.13 · engenharia causal para perks

**Identidade:** `vampirism:lord_speed` · `de.teamlapen.vampirism.entity.player.lord.actions.SpeedLordAction` · instant / aura de bônus de velocidade a aliados.

**Proveniência:** `Vampirism-1.21-1.10.13.jar`, mod ID `vampirism`, SHA-1 instalado `349b6e4ea893c98a580775b1725399903e222228`; registry físico 19/19 ✅ [Java21 #38664546643](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38664546643). Comportamento abaixo é **⚠️ SOURCE_CAUSALITY** do pin `TeamLapen/Vampirism@e1ed095713cef5e9eb151d0ee58908fa830d6bb7`, não equivalência binária integral, valores efetivos de config ou gameplay. `⛔` nenhum adapter per-caster aprovado.

## Eixos e limites de perk

| Eixo | Código verificado e implicação | Mutabilidade |
|---|---|---|
| Alvo e geometria | LordRangeEffectAction.activate seleciona LivingEntity na AABB de 1 bloco em player.blockPosition() ampliada em 10 por eixo, com facção igual à do invocador; ignora targets Player com Lord level >= caster. | Não é esfera raio 10 nem target cast genérico. SEM_HOOK_SEGURO para raio/mudança de facção. |
| Resultado | Aplica efeito provider LORD_SPEED por getEffectDuration = laLordSpeedDuration default 30s×20 = 600 ticks; amplifier override = 0, independentemente do nível Lord. Base LordRangeEffectAction retornaria nível−1, mas esta ação sobrescreve. | Eventos de Action não permitem magnitude do effect, nem autoriza buff double-apply. |
| Cooldown discrepante | SpeedLordAction.getCooldown = super.getCooldown(player) + BalanceConfig.laLordSpeedCooldown.get(). O super retorna **600 ticks** e config default **120**, cujo comentário declara **'In seconds'**, porém código **não multiplica por 20**. Resultado fonte com defaults: **720 ticks ≈ 36 s**, não 150 s. Efeito ainda 600 ticks. | DIVERGÊNCIA SOURCE↔COMENTÁRIO: não corrigir fórmula no catálogo por intenção; QA provider-loaded obrigatório antes de balancear perks. |
| Sucesso condicional | LordRangeEffectAction retorna !entitiesOfClass.isEmpty() **mesmo quando todos os Player alvos foram pulados** por Lord level. Não prova que pelo menos um addEffect retornou true. | Premiar Mastery por effect real e target efetivamente elegível, não pelo return true. |
| Dano/custo | Não aplica hurt, DamageType, projectile, custo de blood nem mudança de hitbox no método lido. | N/A dano, projectile e recursos. Black Arcana não assume buffs do provider. |

## Localizadores

- [Subclasse](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/main/java/de/teamlapen/vampirism/entity/player/lord/actions/SpeedLordAction.java#L8-L33)
- [Classe base](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/main/java/de/teamlapen/vampirism/entity/player/lord/actions/LordRangeEffectAction.java#L20-L56)
- [Config](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/main/java/de/teamlapen/vampirism/config/BalanceConfig.java#L458-L460)
- [ActionEvent — setters de cooldown/duração, veto](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/api/java/de/teamlapen/vampirism/api/event/ActionEvent.java#L37-L78): evento pré-onActivated, não setter de raio/dano/target.

**QA obrigatório:** Medir cooldown real em dedicated server com config defaults e override explícito, caster e allies com Lord level maior/igual, nenhum aliado, facção, allied NPC, stats de efeito, respec e multiprovider. Não duplicar casts, buffs/consumo nem autoridade da action. **+0 novas identidades; Stage 06.05 🟡; Stage 09 PENDING.**
