# vampire_rage — Vampirism 1.10.13 · ficha causal para perks

**Identidade:** `vampirism:vampire_rage`, provider `vampirism`; classificação lasting / efeitos de combate; classe `de.teamlapen.vampirism.entity.player.vampire.actions.RageVampireAction`. **✅ COUNTED_EXACT somente no registry compilado** [#38664546643](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38664546643), **⚠️ SOURCE_CAUSALITY para corpo**, **⛔ adapter e gameplay não homologados**. JAR instalado `Vampirism-1.21-1.10.13.jar`, SHA-1 `349b6e4ea893c98a580775b1725399903e222228`. Source pin `TeamLapen/Vampirism@e1ed095713cef5e9eb151d0ee58908fa830d6bb7`; todos os números são defaults ou constantes do source, não configuração medida no modpack.

Mantém buffs de combate enquanto o estado Rage estiver ativo, sem infligir dano diretamente.

## Matriz de parâmetros e causalidade

| Eixo | Prova verificada no código exato | Estado de perk |
|---|---|---|
| Gate | canBeUsedBy recusa ação BAT ativa, além dos gates de ActionHandler. | RPG não deve bypass do conflito Bat/Rage. |
| Duração/cooldown | Default cooldown vaRageCooldown=20 s (400 ticks); duração = 20 × (vaRageMinDuration(default 13 s)+ vaRageDurationIncrease(default 5 s) × vampire.getLevel()). Níveis e refinements nativos permanecem autoridade Vampirism. | Cooldown/duração mutáveis em ActionActivatedEvent antes da execução; output final condicionado a onActivated. |
| Efeitos | applyEffects aplica MOVEMENT_SPEED 22 ticks amplifier 2 (=Speed III), DAMAGE_BOOST 22 ticks amplifier 0 (=Strength I), DIG_SPEED 22 ticks amplifier 0 (=Haste I). | Atributos/damage multiplier downstream são vanilla; não inferir multiplicador de dano líquido sem medir. |
| Reaplicação/remoção | Ativação aplica buffs; onUpdate reaplica no servidor quando tickCount%20==0; onDeactivated remove três efeitos. Recast simultâneo/outros mods podem influir na interação de efeitos. | Não atribuir 1 cast por renovação de 20 ticks, não apagar efeitos de outros mods sem QA. |
| Target e ataque | Self, sem projétil, AOE, raycast, daño direct ou colisão criada no método. | N/A projectile damageType/range/target alternativo. |
| Recurso | Sem useBlood ou mana explícitos no corpo Rage; não inferir custo temático. | Sem hook de economia a inserir. |

## Implementação e evidências

- [Action source](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/main/java/de/teamlapen/vampirism/src/main/java/de/teamlapen/vampirism/entity/player/vampire/actions/RageVampireAction.java#L12-L85).
- [Rage defaults](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/main/java/de/teamlapen/vampirism/src/main/java/de/teamlapen/vampirism/config/BalanceConfig.java#L395-L398).
- [ActionEvent API pública](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/main/java/de/teamlapen/vampirism/src/api/java/de/teamlapen/vampirism/api/event/ActionEvent.java#L37-L78): `ActionActivatedEvent` cancelável e com `setCooldown(int)`/`setDuration(int)`, **antes de** `onActivated`. Nenhum setter de área/dano/target consta nesse evento.

**QA bloqueante:** Testar múltiplos buffs provenientes de outros mods, remoção, interrupção por Bat, recast, restart, damage source, cliente vs servidor, vanilla boost sem duplicar Mastery. **Sem merge de runtime, sem projeção de hooks externos, sem nova identidade semântica.**
