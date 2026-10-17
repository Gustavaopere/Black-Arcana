# summon_bat — Vampirism 1.10.13 · ficha causal para perks

**Identidade:** `vampirism:summon_bat`, provider `vampirism`; classificação instant / invocação; classe `de.teamlapen.vampirism.entity.player.vampire.actions.SummonBatVampireAction`. **✅ COUNTED_EXACT somente no registry compilado** [#38664546643](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38664546643), **⚠️ SOURCE_CAUSALITY para corpo**, **⛔ adapter e gameplay não homologados**. JAR instalado `Vampirism-1.21-1.10.13.jar`, SHA-1 `349b6e4ea893c98a580775b1725399903e222228`. Source pin `TeamLapen/Vampirism@e1ed095713cef5e9eb151d0ee58908fa830d6bb7`; todos os números são defaults ou constantes do source, não configuração medida no modpack.

Invoca várias entidades BlindingBat nativas, opcionalmente com comportamento de targeting refinado.

## Matriz de parâmetros e causalidade

| Eixo | Prova verificada no código exato | Estado de perk |
|---|---|---|
| Gates | canBeUsedBy requer BAT ativa **ou** refinement SUMMON_BATS equipado; usa Player e seu server-world; ActionHandler valida demais gates. | É ação nativa, não summons independentes que disparam XPs separados. |
| Contagem/fan-out | vaSummonBatsCount default 16, configurável 1..100; com refinement e amount>1, usa divisão inteira por 2 (default 8). Loop cria entidade, restringe lifespan, resting=false, copia posição caster, adiciona ao Level. | CONFIG_NATIVE count global; sem hook de amount por jogador. Não criar duplicatas para aumentar perks. |
| Target/geometry | Cada BlindingBat começa na posição player, setTargeting() somente com refinement; alvo e ataque subsequentes pertencem à classe entidade, não ao método de action analisado. | Target type/range, damageType e collider dos bats = NÃO VERIFICADO nesta ficha; depender do pipeline nativo. |
| Cooldown | vaSummonBatsCooldown default 300s (6000 ticks); refinement aplica fator 0.7 ao produto antes de cast para int → 4200 ticks default. ActionEvent pode mutar cooldown. | Evento SOURCE-VERIFIED para cooldown/veto; spawn de pelo menos uma entidade não é demonstrado pelo simples activate=true. |
| Lifecycle e custo | RestrictLiveSpan é invocado, mas tempo numérico precisa inspeção do corpo BlindingBat; nenhuma chamada useBlood neste action. | QA spawn 0/partial, chunks, owner, despawn, unload e limites. Sem charge paralelo. |
| Dano/efeito | Sem hurt direto no método de action; agressão da entidade é downstream. | N/A damage multiplier na action; perks ofensivas devem rastrear ataque concreto do bat e origem. |

## Implementação e evidências

- [Action source](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/main/java/de/teamlapen/vampirism/src/main/java/de/teamlapen/vampirism/entity/player/vampire/actions/SummonBatVampireAction.java#L17-L63).
- [Config counts/cooldown](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/main/java/de/teamlapen/vampirism/src/main/java/de/teamlapen/vampirism/config/BalanceConfig.java#L409-L411).
- [ActionEvent API pública](https://github.com/TeamLapen/Vampirism/blob/e1ed095713cef5e9eb151d0ee58908fa830d6bb7/src/main/java/de/teamlapen/vampirism/src/api/java/de/teamlapen/vampirism/api/event/ActionEvent.java#L37-L78): `ActionActivatedEvent` cancelável e com `setCooldown(int)`/`setDuration(int)`, **antes de** `onActivated`. Nenhum setter de área/dano/target consta nesse evento.

**QA bloqueante:** Testar 16→8 no refinement, config 1, 100, entidade criada/invalidada, world cap, logout/save, prioridade de alvo/facções, damage attribution e custo por tick. **Sem merge de runtime, sem projeção de hooks externos, sem nova identidade semântica.**
