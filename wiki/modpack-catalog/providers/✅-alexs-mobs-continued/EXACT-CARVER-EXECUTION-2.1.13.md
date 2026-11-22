# Dimensional Carver — execução estática no publisher 2.1.13

A autoridade binária é o JAR publisher **8856498**, 27.452.738 bytes, SHA-1 `50ddafdf3d12b33331e4eecb4ab514ae451baadd` e SHA-256 `eef0b4d36f1e40292b23f90ad3052e2e9aace3a33c6a48c65b8b5f2b061ab6c8`. O [selo de execução](EXACT-CARVER-EXECUTION-2.1.13.json) tem SHA-256 `28556c1f0b7f8b9ed8b269b89f9ea28a2f80bc1b5a718e03b1d4a4cd1e64bda6`. A prova reproduz o [selo anterior](EXACT-CARVER-PORTAL-LIFECYCLE-2.1.13.json) e inclui os corpos próprios restantes, o processamento da fila, e recursos do JAR. [Ficha individual](actions/dimensional-carver-passage.md)

## Ativação e cobrança

`AMItemRegistry.<clinit> @1912–1923` e o bootstrap da factory `lambda$static$91` vinculam `alexsmobs:dimensional_carver` a `ItemDimensionalCarver`, durabilidade **20** e raridade `EPIC`. O portal `alexsmobs:void_portal` vem de `AMEntityRegistry.lambda$static$66`, categoria `MISC`, **0,5 × 0,5** e `fireImmune`. A receita tem **dois** `void_worm_mandible`, **um** `void_worm_eye` e **dois** itens no tag `#c:ingots/netherite`. O alcance do clip é **1,5 bloco** e a duração de uso **200 ticks**.

Em `use`, o item rejeita dano da stack igual ou superior ao máximo e solicita iniciar o uso antes do raycast. Deriva a âncora de `hitLocation − 0.1F × direção mais próxima` por eixo. Quando `HASBLOCK` existe, usa as coordenadas já guardadas. O corpo não requer tipo de hit `BLOCK` para gravar a âncora. A ultrapassagem de **3 blocos** marca a condição de parada e pede cooldown **40** para jogador. O ramo de conclusão testa `remaining == 1` e lado servidor antes de consumir aquela flag de parada. Portanto esta flag, sozinha, não impede avaliar a criação nesse último callback.

A conclusão solicita `addFreshEntity`, descarta o booleano, chama a rotina de destino, solicita **1** de durabilidade na mão em uso e cooldown **200** para jogador. A chamada existe mesmo quando a inserção retorna falso. O provider limpa `HASBLOCK` e `BLOCKX/Y/Z` no encerramento que passa pela sua rotina de release.

## Destino, alvos e processamento

`onPortalOpen` escreve vida **1200 ticks**, `OVERWORLD` como dimensão inicial e usa posição de sono ou heightmap `MOTION_BLOCKING` em `BlockPos.ZERO` do nível do ator. Para `ServerPlayer`, usa a dimensão de respawn e substitui a posição quando existe uma posição de respawn. O destino gravado fica **2 blocos acima** da posição escolhida. O portal consulta alvos elegíveis em servidor somente quando destino existe, vida e idade superam **20**. A caixa diminui em `0.20000000298023224`; Void Worm tem uma consulta adicional ampliada em **1,5**. O filtro pula cooldown de portal, agachado, portais, multipart e tag `void_portal_ignores`.

O destino ordinário de travessia parte da posição gravada mais **2 blocos** na direção oposta ao attachment, depois centralizado. A dimensão precisa resolver a um `ServerLevel` diferente para usar o helper interdimensional. Se o nível não resolve, o fallback ainda é o teleporte no nível corrente. Void Worm e segmentos passam por tratamento próprio. A duração, direção e posição da travessia pertencem a métodos diferentes.

`teleportEntityFromDimension` enfileira `ServerPlayer`, nível destino e `BlockPos` em `AMTeleportQueue.PLAYERS`. O código de `ServerEvents.onLevelTick` drena a lista em contexto de `ServerLevel`, ajusta Y ao máximo entre Y candidato e a altura da coluna `MOTION_BLOCKING_NO_LEAVES`, pede teleporte ao centro do bloco, ticket `POST_TELEPORT` e sincronização de XP. Limpa a lista quando termina a iteração. A prova dos dois wrappers de level tick delimita esse processamento. A fila é memória do provider, sem garantia de persistência, atomicidade ou aceitação em reconexão.

Para entidade não jogadora, pede desmontagem, troca de nível e criação da entidade de mesmo tipo, restauração do estado, posição e cooldown antes da inserção. Solicita descarte da origem após essa sequência, inclusive no caminho de criação nula. Resultados de inserção, idempotência e equilíbrio de estados após falha requerem QA em jogo.

## Estado e fronteiras

O selo inclui `createAndSetSister`, `link`, UUID da irmã, campos sincronizados e rotinas de NBT. `clearObstructions` exige a flag shattered, destino e latch de limpeza desligado. Neste corpo, os limites dos três laços avaliam somente o deslocamento (−1, −1, −1) do destino. Esse ramo pede `destroyBlock(...,true)`. A criação normal do Carver define shattered falso, e o compartilhamento da rotina com a variante Shattered não concede essa escrita ao item normal.

A comprovação é estática e restrita ao item, portal e consumidores nativos do JAR `2.1.13`. A disponibilidade normal do item ainda depende da obtenção do Void Worm e de configuração e dados ativos. A análise não promove autoria/claims, teleportes efetivos, QA física ou mutação por perks.

```sh
python3 docs/qa/alexsmobs_213_carver_execution.py \
  --jar /caminho/alexsmobs-2.1.13.jar --javap "$JAVA_HOME/bin/javap" \
  --output /tmp/alexsmobs-carver-execution.json
```

`STATIC_TECHNICAL_CATALOG_ONLY`, `CONDITIONAL`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`. O inventário de três raízes permanece identificado, com provider integral aberto.
