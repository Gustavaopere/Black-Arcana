# sunscreen — Vampirism 1.10.13 · ficha causal para perks

**Identidade:** `vampirism:sunscreen`, provider `vampirism`; classificação lasting / proteção ambiental; classe `de.teamlapen.vampirism.entity.player.vampire.actions.SunscreenVampireAction`. **✅ COUNTED_EXACT somente no registry compilado** [#38664546643](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38664546643), **⚠️ SOURCE_CAUSALITY para corpo**, **⛔ adapter e gameplay não homologados**. JAR instalado `Vampirism-1.21-1.10.13.jar`, SHA-1 `349b6e4ea893c98a580775b1725399903e222228`. Source pin `TeamLapen/Vampirism@e1ed095713cef5e9eb151d0ee58908fa830d6bb7`; todos os números são defaults ou constantes do source, não configuração medida no modpack.

Mantém o efeito SUNSCREEN nativo enquanto a ação está ativa.

## Matriz de parâmetros e causalidade

| Eixo | Prova verificada no código exato | Estado de perk |
|---|---|---|
| Admissão | activate chama applyEffect() e retorna true; ActionHandler preserva unlock, action flags e timer. | ActionActivatedEvent pode editar cooldown/duração mas não certifica supressão efetiva de sun damage. |
| Duração/cooldown | vaSunscreenCooldown default 500 segundos=10000 ticks; duration default 40s=800 ticks. Com refinement SUN_SCREEN, faz int duration *= vrSunscreenDurationMod default 1.5 (truncamento inteiro quando aplicável). | CONFIG_NATIVE para configurações globais e refinement; hook event apenas timer. |
| Status/reaplicação | MobEffectInstance(ModEffects.SUNSCREEN, 22 ticks, amplifier 3); reaplica a cada tickCount%20==0 no servidor; remove SUNSCREEN ao desativar. | Preservar owner de efeito; não reproduzir protetor de sol na Black Arcana. |
| Alvo/dano | Self, sem attack range, dano, projectile, AOE ou hitbox; proteção de sol downstream do efeito. | N/A combat-damage boost e dano elemental. |
| Causalidade/custo | A ativação é uma raiz; sucessivos onUpdate de status não são novos casts. O método não chama useBlood. | QA aplicação real versus sunDamage; nenhum adapter de custo. |

## Implementação e evidências

- [Action source](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/main/java/de/teamlapen/vampirism/src/main/java/de/teamlapen/vampirism/entity/player/vampire/actions/SunscreenVampireAction.java#L13-L77).
- [Config](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/main/java/de/teamlapen/vampirism/src/main/java/de/teamlapen/vampirism/config/BalanceConfig.java#L399-L401).
- [Refinement](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/main/java/de/teamlapen/vampirism/src/main/java/de/teamlapen/vampirism/config/BalanceConfig.java#L445-L445).
- [ActionEvent API pública](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/main/java/de/teamlapen/vampirism/src/api/java/de/teamlapen/vampirism/api/event/ActionEvent.java#L37-L78): `ActionActivatedEvent` cancelável e com `setCooldown(int)`/`setDuration(int)`, **antes de** `onActivated`. Nenhum setter de área/dano/target consta nesse evento.

**QA bloqueante:** QA day/night, other sunscreen sources, effect removal, default expiry e refinement, respawn, vanilla sun check, client/server, no-double-award. **Sem merge de runtime, sem projeção de hooks externos, sem nova identidade semântica.**
