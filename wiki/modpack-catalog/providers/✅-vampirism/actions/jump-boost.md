# jump_boost — Vampirism 1.10.13 · ficha causal para perks

**Evidência:** Vampirism `1.10.13` / `Vampirism-1.21-1.10.13.jar`, SHA-1 físico `349b6e4ea893c98a580775b1725399903e222228`. Identidade do JAR 19/19 provada em [Java 21 #38664546643](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38664546643); os detalhes abaixo são **SOURCE_CAUSALITY**, pin `TeamLapen/Vampirism@e1ed095713cef5e9eb151d0ee58908fa830d6bb7`, não ABI binária completa nem QA de gameplay. A config descrita é padrão da fonte, não configuração instalada. Sem adapter de perk implementado.

**ID:** `vampirism:jump_boost` · classe `de.teamlapen.vampirism.entity.player.vampire.actions.JumpBoostAction` · categoria **lasting / movimento**.

## Matriz de engenharia

| Eixo | Causalidade e valores do código | Possibilidade de perk |
|---|---|---|
| Ativação e atributo | applyEffect chama VampirePlayer.specialAttributes.setJumpBoost(vsJumpBoost + 1), default config vsJumpBoost=1 => special jumpBoost=2; é flag provider-owned, não necessariamente amplifier de Jump Boost vanilla. | SEM_HOOK_SEGURO para reescrever atributo por RPG; mecânica do salto downstream requer auditoria do handler. |
| Duração e cooldown | vaJumpBoostDuration default Integer.MAX_VALUE segundos é clamp entre 10 e Integer.MAX_VALUE/20−1 e convertido em ticks; cooldown vaJumpBoostCooldown default 0s ×20 + 1 tick. | ActionActivatedEvent muta timer provider com clamps a testar, sem mudar jump height diretamente. |
| Reactivation/fim | onActivatedClient e onReActivated restauram setJumpBoost; onDeactivated faz setJumpBoost(0); onUpdate retorna false. | Testar reconexão, mount, dimension change, modifiers de Epic Fight e desligamento. |
| Alvo/físico | Self movement: sem projectile, AOE, target entity, DamageType, hurt ou raycast. | N/A range, hitbox de projectile ou damage per-target. |
| Custo | Nenhum useBlood nem mana diretamente na action; default normal vsJumpBoost=1, config limite −1..5. | CONFIG_NATIVE global; sem cobrança extra por salto. |

## Localizadores do código

- [JumpBoostAction](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/main/java/de/teamlapen/vampirism/entity/player/vampire/actions/JumpBoostAction.java#L10-L55)
- [Config jump](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/main/java/de/teamlapen/vampirism/config/BalanceConfig.java#L338-L338)
- [Config timers](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/main/java/de/teamlapen/vampirism/config/BalanceConfig.java#L425-L427)
- [ActionActivatedEvent oficial](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/api/java/de/teamlapen/vampirism/api/event/ActionEvent.java#L37-L78): veto e timers antes de `onActivated`; não define hook para target, hitbox ou dano.

**Aceitação pendente:** QA salto em diferentes superfícies, fall damage, multijump e outros movement mods, save/reload, clamp de duração, special attribute real e composição com atributos RPG. Registro em ficha não autoriza mutar a ação no RPG Skill Tree. **+0 nova magia, nenhum adapter implementado, QA físico PENDING.**
