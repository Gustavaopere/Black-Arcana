# Ars Rituals on moving contraptions

State: `SOURCE-PINNED 5.4.0 / PARTIAL-COMPAT DESIGN / RUNTIME QA REQUIRED`

Release 5.4.0's changelog is `Add ritual support to contraptions`.

`RitualBehavior` reconstructs a ritual by registry id and serialized state, attaches a stand-in `RitualBrazierTile` at the moving position, supports decorative particles, consumes eligible nearby item entities while not running, obtains Source through Ars `SourceUtil`, runs `tryTick` and writes ritual state back into the movement context.

The source explicitly comments that rituals have access to a mocked tile and that some rituals not working is expected. Therefore Phase 2S records `ritual support` as a bridge family, not universal compatibility with every Ars/addon ritual.

The custom body in `RitualInteraction.handlePlayerInteraction` is commented out at the exact checkpoint, so placement/start/item-interaction behavior beyond active movement ticking is not promoted without runtime evidence.

Ritual identity/effects remain Ars-owned. Black Arcana must not duplicate them or derive proc chains from a second synthetic ritual.

## Engenharia causal para perks — 17/10/2026

**Proveniência:** mod ID `ars_creo`, JAR instalado documentado `ars_creo-1.21.1-5.4.0.jar`, SHA-1 `22a6afd4fbe76354acc9c1ba076c89a94d120d94`. Código da versão `5.4.0`: `baileyholl/Ars-Creo@6a99d36fab441653478fc49de8f28164f0894eb2` (**SOURCE_CAUSALITY**, sem equivalência binária completa nem QA do pack). Hosts: Ars Nouveau `5.13.1`, Create `6.0.10`. **Ars Creo não registra glyph próprio: +0 IDs novos.**

**Rituais móveis — persistência/custo/causalidade** — efeito do provider externo/integração Create, não nova raiz mágica.

| Eixo | Mecanismo no source pinado | Limite de perk |
|---|---|---|
| Reidratação | Lê `ritualID` e estado via `RitualRegistry.getRitual` e `ritual.read`; cria `RitualBrazierTile` stand-in no BlockPos atual. O source avisa que alguns rituais podem falhar pela tile mockada. | ⛔ Não chamar receita/efeito como equivalente a ritual Black Arcana, nem declarar compat universal. |
| Ritual lifecycle | tick chama tickBrazierBehavior; quando `ritual.getContext().isDone`, chama `ritual.onEnd`, limpa temporaryData e `writeToTag`. `ritual.tryTick(standIn)` é chamado após validações/Source. O método não possui guard geral `!isClientSide` ao chamar `onEnd`/`tryTick`; effects host-side precisam ser verificados. | ⚠️ possibilidade de execução no lado cliente, efeito/custo exato e callback após reload; não criar um segundo progression event. |
| Item ingress | Se !running, server-only e `gameTime%5==0`, examina `ItemEntity` na AABB(altar atual).inflate(1), e chama `ritual.onItemConsumed(stack)` se `ritual.canConsumeItem(stack)`. No helper não há remoção direta da ItemEntity nem decremento do stack visível; efeito do `onItemConsumed` é delegado ao ritual. | ⚠️ item consume concreto, duplicação/replay, pickup/stack mutation dependem do ritual Ars específico. |
| Source e range | Se consumesSource e needsSourceNow, debita via `SourceUtil.takeSourceMultipleWithParticles(pos,level,6,ritual.getSourceCost())`; se null retorna, senão `ritual.setNeedsSource(false)`. Não há custo paralelo do Black Arcana. | Source é de Ars; não credit/debit repetido por tick. |
| Persistência | Após tryTick, `writeToTag` cria CompoundTag novo, escreve ritualID + ritual state se houver, e flags color/decorative/off; atribui a `context.blockEntityData`. Vida da contraption e montagem/desmontagem são de Create. | Respec/logout/contraption unload e restauração per-ritual exigem teste; não copiar estado para SavedData BA. |
| Interação desativada | RitualInteraction.handlePlayerInteraction possui body custom de start/item/tablet **inteiramente comentado** e retorna `super.handlePlayerInteraction`. Não declarar Start Ritual via mão/tablet em movimento. | ⛔ iniciar ritual por perk/remote interaction sem evento aceito. |

**Âncoras verificáveis:** [RitualBehavior.java](https://github.com/baileyholl/Ars-Creo/blob/6a99d36fab441653478fc49de8f28164f0894eb2/src/main/java/com/hollingsworth/ars_creo/contraption/RitualBehavior.java#L28-L54) · [RitualBehavior.java](https://github.com/baileyholl/Ars-Creo/blob/6a99d36fab441653478fc49de8f28164f0894eb2/src/main/java/com/hollingsworth/ars_creo/contraption/RitualBehavior.java#L86-L137) · [RitualBehavior.java](https://github.com/baileyholl/Ars-Creo/blob/6a99d36fab441653478fc49de8f28164f0894eb2/src/main/java/com/hollingsworth/ars_creo/contraption/RitualBehavior.java#L163-L197) · [RitualInteraction.java](https://github.com/baileyholl/Ars-Creo/blob/6a99d36fab441653478fc49de8f28164f0894eb2/src/main/java/com/hollingsworth/ars_creo/contraption/RitualInteraction.java#L9-L38).

**Aceitação pendente:** Por ritual Ars real: start antes de mover, interruption/unload, items stack de 1/N, Source insuficiente, mock brazier incompatível, side/client, onEnd exatamente uma vez, serialize/deserialize e claims/WorldEffectPolicy. O RPG Skill Tree não controla o runtime Ars/Create. **0 adapters homologados, +0 IDs de magia.**
