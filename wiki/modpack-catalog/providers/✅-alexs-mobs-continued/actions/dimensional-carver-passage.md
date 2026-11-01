# Dimensional Carver — Void Portal / Dimensional Passage

- Provider: **Alex's Mobs Continued** (`alexsmobs`)
- Version: `2.1.13`
- Exact physical/publisher SHA-1: `50ddafdf3d12b33331e4eecb4ab514ae451baadd`
- Owner item: `alexsmobs:dimensional_carver`
- Semantic type: deliberate supernatural dimensional-traversal action
- State: `CONDITIONAL`

## Identity and trigger

The exact `ItemDimensionalCarver` path exposes a deliberate channel/use action. The provider resolves the portal attachment/destination surface and settles one dimensional-passage semantic root.

Portal entity ticks, particles, lifetime, destination coordinates and teleport lifecycle are downstream parameters/consequences, not additional spell identities.

## Exact settlement

The exact artifact closes provider behavior that:

- ray-traces/resolves the portal attachment and destination surface;
- creates `EntityVoidPortal`;
- sets provider attachment/destination/dimension/lifespan state;
- adds the portal entity to the level;
- settles owner-item durability.

Black Arcana must not create a second portal or duplicate durability settlement.

## Exact recipe and dependency

The exact shaped recipe requires:

- Void Worm Eye;
- Void Worm Mandible;
- Netherite.

The exact provider loot surface supplies Void Worm Eye and Mandible from the Void Worm.

## Reachability gate

Because normal Void Worm reachability remains conditioned on deployed `voidWormSummonable` / `voidWormSpawnDimensions`, normal Dimensional Carver acquisition inherits that unresolved chain.

The Carver action identity and its settlement are exact-current; the blocker is current normal reachability.

## Disposition

- exact action identity: closed;
- exact recipe: closed;
- owner loot dependency: closed to Void Worm;
- current normal acquisition: conditional on the unresolved Void Worm summon path;
- state: `CONDITIONAL`;
- strict contribution from this root: **+0**.

Source: `../EXACT-2.1.13-ARTIFACT-AUDIT.md`.

## Matriz de execução e progressão (2026-10-29)

Carver: **identidade executável provada no JAR exato**, mas obtenção normal requer Eye/Mandible do Void Worm — logo a contagem estrita herda o gate de summon/config. Verificar receita/loot efetivos, segurança do destino, lifespan de `EntityVoidPortal`, descarte após reload e débito de durabilidade em `AMC-D01..D02`. Não presumir `range` ou duração a partir do fonte público **2.2.3**. Mutadores **⛔ fail-closed**; BA não cria portal ou teleporte em paralelo. Veja [matriz de QA](../EXACT-ARTIFACT-PERK-QA-GATES-2.1.13.md).

## Operandos de controle confirmados no JAR 2.1.13 (2026-10-31)

- `ItemDimensionalCarver.rayTracePortal`: clip inicial de **1,5 bloco** a partir dos olhos (`ClipContext.Block.OUTLINE`); o `use` chama o método com `Fluid.ANY`. Não confundir com alcance total de travessia.
- `getUseDuration`: **200 ticks**. `onUseTick` contém o limiar `distanceToSqr(caster, anchor) > 9.0d` (>3 blocos) e um caminho de cooldown de **40 ticks**.
- Quando `remainingUseTicks == 1` no lado do servidor, o código tenta acrescentar `EntityVoidPortal`, chama `onPortalOpen`, aplica **1 ponto de dano à durabilidade** e adiciona cooldown de **200 ticks** ao jogador. Esses são caminhos de controle estáticos, não QA de sucesso/cardinalidade de spawn.
- `onPortalOpen` atribui **1200 ticks** ao lifespan inicial. Destino depende do respawn dimension/position do `ServerPlayer` ou de fallback local; não há autorização documentada para alterar dimensões arbitrariamente.
- `releaseUsingImpl` limpa `HASBLOCK` e `BLOCKX/Y/Z`. Duração efetiva, proteção de destino, lifecycle da entidade, multiplayer e hooks de mutação continuam pendentes.

**Proveniência:** [mapa de bytecode SHA-exato](../EXACT-CONTROL-OPERANDS-2.1.13.md). Estado documental e hooks permanecem ⚠️ / ⛔, respectivamente; não promover índices sem o certificado exigido.
