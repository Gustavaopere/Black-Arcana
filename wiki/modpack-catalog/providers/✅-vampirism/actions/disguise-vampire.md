# disguise_vampire — Vampirism 1.10.13 · ficha causal para perks

**Evidência:** Vampirism `1.10.13` / `Vampirism-1.21-1.10.13.jar`, SHA-1 físico `349b6e4ea893c98a580775b1725399903e222228`. Identidade do JAR 19/19 provada em [Java 21 #38664546643](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38664546643); os detalhes abaixo são **SOURCE_CAUSALITY**, pin `TeamLapen/Vampirism@e1ed095713cef5e9eb151d0ee58908fa830d6bb7`, não ABI binária completa nem QA de gameplay. A config descrita é padrão da fonte, não configuração instalada. Sem adapter de perk implementado.

**ID:** `vampirism:disguise_vampire` · classe `de.teamlapen.vampirism.entity.player.vampire.actions.DisguiseVampireAction` · categoria **lasting / disfarce**.

## Matriz de engenharia

| Eixo | Causalidade e valores do código | Possibilidade de perk |
|---|---|---|
| Ingresso | activate marca VampirePlayer.specialAttributes.disguised=true e disguisedAs=null; handler governa unlock, permission, cooldown e duração. | ActionActivatedEvent contém setters de cooldown/duração e veto, mas é PRE-onActivated. |
| Duração/cooldown | vaDisguiseDuration default 60s=1200 ticks; cooldown vaDisguiseCooldown default 60s=1200 ticks, ambos multiplicados por 20 no método. | CONFIG_NATIVE defaults; extension per-caster apenas event/adapter condicionado. |
| Reativação/fim | onActivatedClient e onReActivated retomam estado de disfarce; onDeactivated limpa flag disguised; onUpdate retorna false. | Lifecycle e persistência em real client/relog PENDING; não duplicar estado de facção. |
| Target/range/geometry | Somente self: sem raycast, AOE, hitbox/projétil ou transformação de target no corpo examinado. | N/A para boost de range, geometry ou projectile size. |
| Dano/custo | Nenhum hurt, health heal, DamageType, useBlood ou mana debit diretamente na action. | Não imputar dano ou blood a um disfarce; efeitos de stealth detectados externamente exigem boundary próprio. |

## Localizadores do código

- [Vampire action](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/main/java/de/teamlapen/vampirism/entity/player/vampire/actions/DisguiseVampireAction.java#L14-L74)
- [Defaults](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/main/java/de/teamlapen/vampirism/config/BalanceConfig.java#L412-L414)
- [ActionActivatedEvent oficial](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/api/java/de/teamlapen/vampirism/api/event/ActionEvent.java#L37-L78): veto e timers antes de `onActivated`; não define hook para target, hitbox ou dano.

**Aceitação pendente:** Testar detecção por NPCs, reset no logoff/death, side do cliente, duração exata, conflitos com Invisibility e DisguiseHunter, limpezas por outros mods. Registro em ficha não autoriza mutar a ação no RPG Skill Tree. **+0 nova magia, nenhum adapter implementado, QA físico PENDING.**
