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

## Ciclo de vida de EntityVoidPortal — selo estático publisher 2.1.13

Evidência: [manifesto de duas classes com hashes, descritores, branches e janelas JVM](../EXACT-CARVER-PORTAL-LIFECYCLE-2.1.13.json) · [handoff com limites e interpretação causal](../../../../../docs/qa/alexsmobs-213-carver-portal-lifecycle-handoff.md). **Somente** o JAR instalado `alexsmobs-2.1.13-neoforge+1.21.1.jar`, SHA-256 `eef0b4d36f1e40292b23f90ad3052e2e9aace3a33c6a48c65b8b5f2b061ab6c8`.

### Parâmetros, fórmulas e eventos observados

| Superfície da versão instalada | Prova JVM | Contrato estritamente permitido |
|---|---|---|
| Criação pelo item | `ItemDimensionalCarver.onUseTick @265–375` | Instancia `EntityVoidPortal`, define posição/facing, tenta `addFreshEntity @327`, executa `onPortalOpen @341`, aplica durabilidade via `AMCompat.hurtAndBreak @351` e cooldown pelo provider. O retorno booleano de `addFreshEntity` é descartado por `pop @330`; não garante aceitação do spawn |
| Vida atribuída ao abrir | `onPortalOpen: setLifespan(1200) @4` | **1200 ticks inicialmente**; não implica duração efetiva universal |
| Fallback de vida | `EntityVoidPortal.tick: tickCount==1 @5–9; getLifespan @13; ifne @16; setLifespan(2000) @23` | **2000 ticks apenas se o lifespan estiver zero no primeiro tick**; não sobrescreve automaticamente o valor 1200 não nulo |
| Redução/descartes | `tick: getLifespan @858; isub 1 @862; setLifespan @863; ifgt @928; remove(DISCARDED) @935` | Há caminho de decremento unitário e descarte quando lifespan fica não positivo |
| Incremento condicional | `tick: instanceof EntityVoidWormPart @687; getLifespan @694; if_icmpge(22) @699; iadd 1 @708; setLifespan @709` | Existe caminho que adiciona 1 quando o lifespan está abaixo de 22, com demais gates ainda não reconstruídos |
| Janela de ativação do portal | `tick: isClientSide @537; ifne @540; getDestination @553; ifnull @556; getLifespan @560; if_icmple 20 @565; tickCount @569; if_icmple 20 @574` | Consultas/teleportes nessa região são **server-side, com destino não nulo, vida >20 e idade >20 ticks** |
| Alvos/transferência | `Entity.isOnPortalCooldown @627`; `EntityVoidPortal.teleportEntityFromDimension` consulta `AMTeleportQueue.PLAYERS`, aplica `setPortalCooldown` e referencia `ServerLevel.addFreshEntity` | Há filtros de entidade e caminho de movimentação entre dimensões; resultado físico, permissão, destino exato e idempotência não testados |
| Estado sincronizado | `SynchedEntityData`: `LIFESPAN`, `DESTINATION`, `ATTACHED_FACE` e métodos `defineSynchedData`, `get/setLifespan`, `get/setDestination` | Campos da entidade têm acesso sincronizado, sem provar consentimento/autoridade de qualquer mod periférico |
| Estado salvo | `addAdditionalSaveData` (67 instruções/3 branches), `readAdditionalSaveData` (86/5) | Existem caminhos NBT com `AttachFace`, `Lifespan`, `ExitDimension` e `DESTINATION`; QA de save/reload e reconexão **NÃO VERIFICADA** |

### Integração com perks e Mastery

Permitir teoricamente uma perk que altere vida, destino, alcance do clip, cooldown ou custo de durabilidade exigiria **um boundary real do provider**, análise de owner/sidedness e testes de segurança em dimensões, claims e multiplayer. A presença de `setLifespan` e de acessores de `SynchedEntityData` **não demonstra que sejam pontos seguros de extensão**, tampouco permite que o RPG Skill Tree tome autoridade de criação/teleporte. Um adaptador Black Arcana não deve originar um segundo portal, invalidar gates da aquisição pelo Void Worm, nem replicar a cobrança nativa.

**Pendências explícitas:** lifecycle real da entidade em servidor modpack; destino/resolução dimensional e `AMTeleportQueue`; concorrência de travessia; redirecionamento PvP/claims; persistência/save/reload; mods que alteram dimensões; API/hook mutador. O item permanece **⚠️ parcial/condicionado** e **`static_perk_contract=NOT_CERTIFIED` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `NO_MUTATION`**. Os índices continuam em **0/3 contratos estáticos no recorte observado de Alex's Mobs**, sem alterar o denominador semântico.
