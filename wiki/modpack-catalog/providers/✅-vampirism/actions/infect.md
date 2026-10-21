# infect — Vampirism 1.10.13 · ficha causal para perks

**Evidência:** Vampirism `1.10.13` / `Vampirism-1.21-1.10.13.jar`, SHA-1 físico `349b6e4ea893c98a580775b1725399903e222228`. Identidade do JAR 19/19 provada em [Java 21 #38664546643](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38664546643); os detalhes abaixo são **SOURCE_CAUSALITY**, pin `TeamLapen/Vampirism@e1ed095713cef5e9eb151d0ee58908fa830d6bb7`, não ABI binária completa nem QA de gameplay. A config descrita é padrão da fonte, não configuração instalada. Sem adapter de perk implementado.

**ID:** `vampirism:infect` · classe `de.teamlapen.vampirism.entity.player.vampire.actions.InfectAction` · categoria **instant / conversão de alvo**.

## Matriz de engenharia

| Eixo | Causalidade e valores do código | Possibilidade de perk |
|---|---|---|
| Admissão/target | Não tem raycast próprio: usa ActivationContext.targetEntity() e filtra para LivingEntity; tenta deriveBiteableEntry target e IBiteableEntity.tryInfect(vampire). | SEM_HOOK_SEGURO para trocar entity-target, range, LOS ou species permission; depende de quem constrói ActivationContext. |
| Exclusões | canBeUsedBy recusa PEACEFUL. No ramo client consulta proxy mouse-over e UtilLib.canReallySee; no ramo activate há condição para Player/AbstractVillager que retorna false quando UtilLib.canReallySee(target,player,false) é true. Sem semântica do UtilLib inspecionada, não interpretar a condicional como check universal de LOS. | NÃO VERIFICADO helper/biteability/guard real em runtime; não inverter a lógica por suposição. |
| Sucesso | Quando tryInfect produz true e alvo permanece no Optional, retorna true e incrementa ModStats.INFECTED_CREATURES; em falha retorna false com som alternativo. | Mais próximo de resultado terminal que ActionActivatedEvent, mas sucesso de conversão persistida depende do provider. |
| Cooldown | Constante getCooldown=10 ticks; isEnabled retorna true; não decorre de default config local. | O evento pode alterar cooldown; duration=-1 instant. Alterar tempo por skill sem regressão requer adapter. |
| Área/dano/custo | Alvo único, sem AOE/projétil/hurt ou preço de sangue diretamente no método. | N/A damage/elemento/aoe. A transformação pertence ao provider. |
| Identidade/progressão | A action Infect é uma raiz; conversão de facção/capability, status da criatura e prêmio de estatística são consequências, não novos casts. | Precisam dedup e verificações de carga/permuta de facção antes de Mastery. |

## Localizadores do código

- [InfectAction](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/main/java/de/teamlapen/vampirism/entity/player/vampire/actions/InfectAction.java#L25-L81)
- [ActionActivatedEvent oficial](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/api/java/de/teamlapen/vampirism/api/event/ActionEvent.java#L37-L78): veto e timers antes de `onActivated`; não define hook para target, hitbox ou dano.

**Aceitação pendente:** Testar players, villagers, PathfinderMob, fake player, Peaceful, check visual canReallySee, cancellation, estado depois de relog, re-infection e side/permissions. Registro em ficha não autoriza mutar a ação no RPG Skill Tree. **+0 nova magia, nenhum adapter implementado, QA físico PENDING.**
