# Starbuncle Wheel

State: `SOURCE-PINNED 5.4.0 / RUNTIME QA PENDING`

Registry id: `ars_creo:starbuncle_wheel`

## Exact behavior

`StarbuncleWheelTile` is a Create `GeneratingKineticBlockEntity`.

Default source config:

- base generated speed: `16`;
- bonus generated speed: `24`;
- stress capacity registered through Create: `16`.

On load and relevant neighbor-shape updates, the tile recalculates speed. For horizontal facings, if the block on the clockwise side relative to the wheel's facing is in NeoForge tag `storage_blocks/gold`, the wheel uses the bonus speed; otherwise it uses base speed. Vertical facing does not take the gold-block bonus path.

The exact runtime path does **not** search for, bind, feed or tick a living Starbuncle entity. The Starbuncle connection in the exact provider-owned acquisition path is the `ars_nouveau:starbuncle_charm` ingredient used with a Create Water Wheel.

## Authority

- Create owns kinetic network, stress and rotation propagation.
- Ars Creo owns the wheel bridge/block and its configured generator values.
- Ars Nouveau owns the Starbuncle Charm item used by the recipe.
- Black Arcana does not reinterpret kinetic production as mana/Source/Arcane Danger generation.

## QA pending

Validate effective server config, Create stress behavior, update timing and compatibility with moving/sublevel contexts in the installed full pack.

## Engenharia causal para perks — 17/10/2026

**Proveniência:** mod ID `ars_creo`, JAR instalado documentado `ars_creo-1.21.1-5.4.0.jar`, SHA-1 `22a6afd4fbe76354acc9c1ba076c89a94d120d94`. Código da versão `5.4.0`: `baileyholl/Ars-Creo@6a99d36fab441653478fc49de8f28164f0894eb2` (**SOURCE_CAUSALITY**, sem equivalência binária completa nem QA do pack). Hosts: Ars Nouveau `5.13.1`, Create `6.0.10`. **Ars Creo não registra glyph próprio: +0 IDs novos.**

**Starbuncle Wheel — geração cinética** — efeito do provider externo/integração Create, não nova raiz mágica.

| Eixo | Mecanismo no source pinado | Limite de perk |
|---|---|---|
| Registry/config | Uma wheel (`ars_creo:starbuncle_wheel`). Config server `wheelBaseSpeed=16`, `wheelMaxSpeed=24`, `wheelStressCapacity=16` defaults; ranges configuráveis, não métricas efetivas de pack. | ⚠️ config loaded QA; valores não equivalem a mana/Source. |
| Sensor posicional | Se FACING é UP/DOWN ou level null, usa base; senão confere bloco em `pos.relative(facing.getClockWise())` com `Tags.Blocks.STORAGE_BLOCKS_GOLD` para ativar speed bônus. `getGeneratedSpeed()` usa `convertToDirection`. | Um bloco de ouro influencia velocidade; não há summon/contagem de Starbuncles. |
| Lifecycle | No `onLoad`, chama `findGoldBlock` e `updateGeneratedRotation`; comportamento de update por vizinho pertence também à classe do bloco. O setter de Stress é registrado em Create `BlockStressValues.CAPACITIES`. | Não tratar neighborUpdate como novo cast, Source generation ou Mastery passiva. |
| Item/acquisition | Starbuncle Charm aparece na receita da wheel (ver ACQUISITION-RECIPES.md), não como entidade vinculada na tick loop examinada. | Não inventar hunger/bind/pet progression. |
| Risco/perf | Sem target, projectile, DamageSource nem mundo alterado por feitiço próprio. Block wheel pode ser motor Create e afetar rede cinética. | ⛔ não injetar overdrive por perks sem Create kinetic/stress contract real. |

**Âncoras verificáveis:** [StarbuncleWheelTile.java](https://github.com/baileyholl/Ars-Creo/blob/6a99d36fab441653478fc49de8f28164f0894eb2/src/main/java/com/hollingsworth/ars_creo/common/block/StarbuncleWheelTile.java#L18-L44) · [CreoConfig.java](https://github.com/baileyholl/Ars-Creo/blob/6a99d36fab441653478fc49de8f28164f0894eb2/src/main/java/com/hollingsworth/ars_creo/CreoConfig.java#L7-L19) · [CreateCompat.java](https://github.com/baileyholl/Ars-Creo/blob/6a99d36fab441653478fc49de8f28164f0894eb2/src/main/java/com/hollingsworth/ars_creo/CreateCompat.java#L31-L49).

**Aceitação pendente:** Config efetiva/speed base+ouro, tag gold custom, direções horizontal/vertical, start/stop chunks, rede stress com dois motores, sobrevivência e desmontagem Create. O RPG Skill Tree não controla o runtime Ars/Create. **0 adapters homologados, +0 IDs de magia.**
