# hissing — Vampirism 1.10.13 · ficha causal para perks

**Evidência:** Vampirism `1.10.13` / `Vampirism-1.21-1.10.13.jar`, SHA-1 físico `349b6e4ea893c98a580775b1725399903e222228`. Identidade do JAR 19/19 provada em [Java 21 #38664546643](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38664546643); os detalhes abaixo são **SOURCE_CAUSALITY**, pin `TeamLapen/Vampirism@e1ed095713cef5e9eb151d0ee58908fa830d6bb7`, não ABI binária completa nem QA de gameplay. A config descrita é padrão da fonte, não configuração instalada. Sem adapter de perk implementado.

**ID:** `vampirism:hissing` · classe `de.teamlapen.vampirism.entity.player.vampire.actions.HissingAction` · categoria **instant / controle de aggro**.

## Matriz de engenharia

| Eixo | Causalidade e valores do código | Possibilidade de perk |
|---|---|---|
| Target/seleção | Busca Mob em new AABB(player.blockPosition()).inflate(10,10,10). É box expandida a partir de um bloco, não esfera raio 10. Apenas mobs cuja target atual == player são alterados. | SEM_HOOK_SEGURO para expansão por player, retarget para entidades externas, cone/LOS ou aumentar entidades. |
| Efeito | Para cada Mob elegível, interrompe WrappedGoal::isRunning de targetSelector e chama e.setTarget(null). Toca som de grito antes da busca. | O retorno de activate=true não indica que pelo menos um Mob foi atingido/teve aggro removido. |
| Cooldown | vaHissingCooldown default 60s=1200 ticks; isEnabled condicional ao BalanceConfig. | Cooldown em ActionActivatedEvent SOURCE-VERIFIED; nenhum setter do alcance no evento. |
| Dano/área | Sem damageSource/hurt, projectile, status effect de duração ou dano elemental; a área é de *busca de alvo*, não de ataque. | N/A DamageType ou dano por criatura. Procs/Mastery têm que observar redução real do alvo. |
| Custo/risco | Sem useBlood/XP neste método; percorre mobs na AABB e goal selectors. | Limites de scans e AI ticks precisam QA; não converter grito em penalidade mágica extra automaticamente. |

## Localizadores do código

- [Hissing source](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/main/java/de/teamlapen/vampirism/entity/player/vampire/actions/HissingAction.java#L14-L43)
- [Cooldown](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/main/java/de/teamlapen/vampirism/config/BalanceConfig.java#L423-L424)
- [ActionActivatedEvent oficial](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/api/java/de/teamlapen/vampirism/api/event/ActionEvent.java#L37-L78): veto e timers antes de `onActivated`; não define hook para target, hitbox ou dano.

**Aceitação pendente:** Testar alvo player vs alvo aliado, mob sem target, integração com AI mods, multi-mob, summon ownership, início sem alvos, target rapidamente reatribuído e Mastery false-positive. Registro em ficha não autoriza mutar a ação no RPG Skill Tree. **+0 nova magia, nenhum adapter implementado, QA físico PENDING.**
