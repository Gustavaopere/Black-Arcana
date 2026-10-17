# vampire_invisibility — Vampirism 1.10.13 · ficha causal para perks

**Evidência:** Vampirism `1.10.13` / `Vampirism-1.21-1.10.13.jar`, SHA-1 físico `349b6e4ea893c98a580775b1725399903e222228`. Identidade do JAR 19/19 provada em [Java 21 #38664546643](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38664546643); os detalhes abaixo são **SOURCE_CAUSALITY**, pin `TeamLapen/Vampirism@e1ed095713cef5e9eb151d0ee58908fa830d6bb7`, não ABI binária completa nem QA de gameplay. A config descrita é padrão da fonte, não configuração instalada. Sem adapter de perk implementado.

**ID:** `vampirism:vampire_invisibility` · classe `de.teamlapen.vampirism.entity.player.vampire.actions.InvisibilityVampireAction` · categoria **lasting / invisibilidade**.

## Matriz de engenharia

| Eixo | Causalidade e valores do código | Possibilidade de perk |
|---|---|---|
| Ativação | activate invoca player.asEntity().setInvisible(true). | É flag de entidade, não stealth universal; o evento de action precede setInvisible. |
| Cooldown/duração | vaInvisibilityCooldown default 25s=500 ticks; vaInvisibilityDuration default 25s=500 ticks. Handler dos timers provider-native. | CONFIG_NATIVE valores; ActionActivatedEvent.setCooldown/setDuration validado somente no source. |
| Resolução de lifecycle | onUpdate reimpõe setInvisible(true) quando flag atual não está ativa; onDeactivated define setInvisible(false) e VampirePlayer.specialAttributes.invisible=false; onActivatedClient ajusta o special attribute. | Há divergência proposital de lado entre flag entidade e special flag de cliente. Não aplicar perk duplicando efeitos a cada tick. |
| Alvo/geometria | Self; sem AOE, raycast, projectile, hitbox mutável ou damage type no método. | N/A dano/range/retarget. |
| Custo/procs | Sem useBlood ou hurt neste corpo. Action success diferente de inimigos realmente incapazes de ver o jogador. | Mastery por ação validada e não por cada tick invisível; detecção é downstream. |

## Localizadores do código

- [Vampire action](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/main/java/de/teamlapen/vampirism/entity/player/vampire/actions/InvisibilityVampireAction.java#L12-L75)
- [Defaults](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/main/java/de/teamlapen/vampirism/config/BalanceConfig.java#L386-L388)
- [ActionActivatedEvent oficial](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/api/java/de/teamlapen/vampirism/api/event/ActionEvent.java#L37-L78): veto e timers antes de `onActivated`; não define hook para target, hitbox ou dano.

**Aceitação pendente:** Testar outros sources de invisibilidade, remoção da flag por terceiros durante ação, respawn e loaded chunks, ActionWheel, client/server sync, detecção de mobs e PvP. Registro em ficha não autoriza mutar a ação no RPG Skill Tree. **+0 nova magia, nenhum adapter implementado, QA físico PENDING.**
