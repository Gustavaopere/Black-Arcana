# Alex's Mobs Continued 2.1.13 — mapa de operandos e decisões do JAR exato

Estado: `SHA_EXACT_BINARY_OPERANDS / THREE_EXISTING_ROOTS / STATIC_ONLY / NO_MUTATING_HOOK / NO_PHYSICAL_QA`.

## Proveniência e alcance

- **JAR de autoridade:** `alexsmobs-2.1.13-neoforge+1.21.1.jar`, mod ID `alexsmobs`, SHA-1 `50ddafdf3d12b33331e4eecb4ab514ae451baadd`.
- **Publisher:** CurseForge projeto 1635121, arquivo 8856498, SHA-256 `eef0b4d36f1e40292b23f90ad3052e2e9aace3a33c6a48c65b8b5f2b061ab6c8`.
- **Fonte da inspeção:** artefato de evidências `alexs-mobs-2.1.13-exact-artifact-audit`, ID 11202548934, workflow [36949047824](https://github.com/Gustavaopere/Black-Arcana/actions/runs/36949047824), PR [#511](https://github.com/Gustavaopere/Black-Arcana/pull/511) (auditoria NON-MERGE). O artefato contém `javap-semantic-seams.txt` e `javap-control-seams.txt`. Os operandos abaixo foram confrontados diretamente com esses dois arquivos do mesmo workflow, sem usar parâmetros da revisão pública 2.2.3.
- **Escopo:** ampliar os contratos de três fichas existentes; **não** adicionar identidades semânticas, promover o estado do índice, declarar testes físicos, certificar hooks ou modificar código do provider.

## 1. Dimensional Carver — `ItemDimensionalCarver`

| Método/trecho de bytecode | Evidência de controle/valor | Consequência técnica para uma perk |
|---|---|---|
| `rayTracePortal(Level, Player, Fluid)`, offsets 79–132 | End point da clip calculado do olho e vetor de visão multiplicado por `1.5d`; `ClipContext.Block.OUTLINE`; `use` passa `ClipContext.Fluid.ANY` | Alcance **da ray trace inicial** é 1,5 bloco, não prova o alcance total de viagem/teleporte |
| `getUseDuration(ItemStack)`, offset 0 | `sipush 200` | Duração de uso declarada = 200 ticks, distinta de tempo necessário para completar a abertura |
| `use`, offsets 7–28 e 128–210 | Verifica dano versus durabilidade máxima antes de iniciar uso; usa `HASBLOCK`, `BLOCKX`, `BLOCKY`, `BLOCKZ` no NBT do item | A âncora de posição é estado do item e pode sobreviver a ações intermediárias; não alterar sem teste de persistência |
| `onUseTick`, offsets 192–232 | `LivingEntity.distanceToSqr(storedX, storedY, storedZ) > 9.0d` estabelece um caminho que adiciona cooldown `40` ticks ao `Player` | Limite de **deslocamento do caster em relação à posição armazenada** corresponde a distância >3 blocos, não ao range do alvo |
| `onUseTick`, offsets 232–375 | Condição de `remainingUseTicks == 1` e `!Level.isClientSide()`: constrói `EntityVoidPortal`, define posição/facing, chama `Level.addFreshEntity` e `onPortalOpen`, aplica `AMCompat.hurtAndBreak(..., 1, ...)` e cooldown `200` ticks | Um portal e uma unidade de dano ao item aparecem no caminho de sucesso observado. A cardinalidade real e o tratamento de falha em `addFreshEntity` ainda exigem QA |
| `onPortalOpen`, offsets 0–101 | `EntityVoidPortal.setLifespan(1200)`; seleciona `ServerPlayer.getRespawnDimension/Position` quando disponíveis, ou caminho alternativo com `getSleepingPos`/`getHeightmapPos(..., BlockPos.ZERO)`; destino `BlockPos.above(2)` | `1200` ticks é a vida **atribuída na criação**, não garantia de permanência efetiva; destino não é um ponto arbitrário informado pelo cliente |
| `releaseUsingImpl`, offsets 0–44 | Reinicializa `HASBLOCK=false` e três coordenadas para `0` | Cancelamento limpa a âncora armazenada; validar casos de interrupção e reconexão |

**Limites ainda não comprovados:** efeito do contador de lifespan dentro de `EntityVoidPortal.tick`, proteção/claims, sucesso do spawn, persistência dos portais, multiplicidade sob uso concorrente, e interceptação provider-native de `rayTracePortal`, cooldown, âncora, vida e dano de durabilidade. **Mutadores: ⛔ fail-closed.**

## 2. Void Worm — `ItemMysteriousWorm.onEntityItemUpdate`

| Offsets exatos | Fato observado | Implicação |
|---|---|---|
| 0–50 | Verifica `AMConfig.voidWormSummonable`, `AMConfig.voidWormSpawnDimensions.contains(level.dimension().location().toString())`, `ItemEntity.getY() < -60.0d` e `!ItemEntity.isRemoved()` | O limiar é estritamente **Y menor que −60**, não ≤ −60; booleano e lista de dimensões são configuração implantada ainda desconhecida |
| 50–75 | Chama `AMCompat.kill(itemEntity)` e cria `EntityVoidWorm` | Consumo da entidade-item precede construção do boss no fluxo inspecionado |
| 77–111 | Posição do boss usa `item.getX()`, `Y=0`, `item.getZ()`; `setSegmentCount(25 + Random.nextInt(15))` | Segmentos iniciais no intervalo inteiro **25..39**; a altura do boss recém-configurado é 0 antes do processamento posterior |
| 111–140 | `setXRot(-90.0f)`, `updatePostSummon=true`, `setBaseMaxHealth(AMConfig.voidWormMaxHealth, true)`, depois verifica `Level.isClientSide()` | Saúde deriva da config, não há valor implantado comprovado; a inspeção não valida posicionamento final após ticks |
| 143–205 | No caminho server-side, tenta associar advancement via dono/UUID e chama `Level.addFreshEntity(voidWorm)`; retorna `false` | Não substituir por um spawn próprio, nem concluir idempotência/multiplayer sem execução |

**Atenção à ordem causal:** a chamada `AMCompat.kill` ocorre **antes** da verificação `isClientSide` no método observado. Isso é um fato de ordenação do bytecode, **não** comprovação de efeito divergente cliente/servidor nem de duplicação. Requer observação do ciclo nativo e da semântica exata de `AMCompat.kill`.

**Limites ainda não comprovados:** valores efetivos de config, semântica do retorno de `onEntityItemUpdate`, spawn efetivo, falhas de criação, persistência/idempotência e hook mutador. **Mutadores: ⛔ fail-closed.**

## 3. Item Transmutation — `MenuTransmutationTable` e `TileEntityTransmutationTable`

| Método/offset | Fato observado | Implicação |
|---|---|---|
| `MenuTransmutationTable.clickMenuButton`, 0–26 | No client envia `MessageTransmuteFromMenu(player.getId(), choice)`; retorna `true` | A existência de mensagem C2S não prova validação de identidade/sessão na recepção |
| `TileEntityTransmutationTable.getPossibility`, 0–25 | `Mth.clamp(choice, 0, 2)`, consulta array e retorna `ItemStack.EMPTY` quando nulo | Índice inválido é **clampado**, não necessariamente rejeitado: não presumir validação de escolha |
| `TileEntityTransmutationTable.rollPossiblity`, 0–90 | Só servidor com `ServerLevel`, índice clampado `0..2`, usa pools common/uncommon/rare para selecionar candidato | São três opções de uma mesma ação, não três spells; tabelas efetivas podem sofrer overrides |
| `TileEntityTransmutationTable.hasPossibilities`, 0–37 | Exige os três elementos do array não nulos e não vazios | A verificação é agregada; não equivale a autorização do pacote |
| `MenuTransmutationTable.transmute`, 0–152 | Exige `!isClientSide`, tabela presente, razão de tamanhos máximos >0, possibilidades existentes, input não vazio e `experienceLevel >= AMConfig.transmutingExperienceCost` **ou** `Abilities.instabuild` | XP é custo do provider; valor numérico e políticas do usuário atual dependem da config |
| `MenuTransmutationTable.transmute`, 25–137 | `ratio = input.getMaxStackSize() / output.getMaxStackSize()`; `outputCount = max(1, floor(inputCount / ratio))`; `Slot.set(output)` e `Player.giveExperienceLevels(-cost)` | Fórmula estática observada. Não alterar tamanho/quantidade/custo sem conhecer semântica dos recursos |
| `TileEntityTransmutationTable.postTransmute`, 0–117 | Registra `TransmutationData.onTransmuteItem` no mapa do UUID, incrementa contador total pelo tamanho do input, dispara advancement a partir de 1000 e seta UUID para reroll | O resultado possui efeitos de estado posteriores; não duplicar settlement ou reroll |

**Limites ainda não comprovados:** entrada efetiva do handler `MessageTransmuteFromMenu`, autorização de `playerId`, validação de menu/slot/replay, políticas de config/loot e persistência em multiplayer. Os métodos observados **não** autorizam concluir que qualquer vetor de exploração está presente. Exigir testes `AMC-T01..T03` antes de uma perk que altere opções, custo ou resultado. **Mutadores: ⛔ fail-closed.**

## Contabilidade e próximos gates

- Denominador semântico preservado: **3 ações**, **1 `COUNTED_EXACT` + 2 `CONDITIONAL`**.
- Certificações estáticas individuais no índice: **0/3**, sem promoção automática por esta inspeção parcial de operandos; ainda faltam fechamento dos fluxos relevantes e validação do padrão de certificação.
- Hooks mutadores: **0 verificados**; QA físico: **0 testados**.
- O próximo ponto **do índice alfabético global** continua Alex's Caves Continued, tratado por um fluxo independente. Este aprofundamento não desloca o cursor nem modifica os percentuais globais.

Relacionados: [auditoria do JAR](EXACT-2.1.13-ARTIFACT-AUDIT.md), [matriz de QA](EXACT-ARTIFACT-PERK-QA-GATES-2.1.13.md), [drift de source](PUBLIC-SOURCE-VERSION-DRIFT-2026-10-29.md) e [manifesto de alcance](SEMANTIC-REACHABILITY-GATES-2.1.13.json).
