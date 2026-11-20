# Descoberta nativa — BurrowingArrowItem a CaveMapItem (1.0.10)

DISCOVERY_NOT_CERTIFIED. JAR publisher exato, 1555 classfiles, SHA-256 36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c; relatório 94df79a5225df4ffe2ffb01d61bc4d1598c02b4c1afafeadacddb4419d2a08f0, job 136078919330. A tabela conta corpos próprios e sites de instrução de classe/membro, não habilidades independentes.

| Classe | Corpos próprios | Owners tipados | Sites | SHA-256 classe |
|---|---:|---:|---:|---|
| BurrowingArrowItem | 2 | 2 | 2 | be5e566fc89b01c311d70d8d2a0fbbe7387601c9b07e70417135bd668b51fded |
| CandyCaneHookItem | 13 | 7 | 36 | d999251e494c45420e58881181e9d67757247b6865dc4a547bf0da8a46cf8e44 |
| CaveBoatItem | 3 | 2 | 16 | 92fc0840e49f71306bbcafbd3e5f4f5814acbf87846846430007310a2577c18d |
| CaveBookItem | 3 | 2 | 2 | 84177c0ff1fdb42d766262624f877874c7c6db22a16036faf4dd6fe0540fcacf |
| CaveInfoItem | 7 | 10 | 37 | 20b9b5234e829030e0ec01d73669c2be000741695c819fa114941a0dc2e98183 |
| CaveMapItem | 12 | 9 | 29 | 949abbb18960cc013ab5a1b9c73c643005792c214ddbd0c927c96843f73f2b01 |

## Disposições provisórias de escopo

- BurrowingArrowItem: construtor ArrowItem e factory createArrow. Esta factory ignora os argumentos stack de munição e arma no corpo próprio e instancia BurrowingArrowEntity(Level, LivingEntity) @6, passando portador. Factory registry lambda$static$129. Dano, penetração, escavação, lifecycle, colisão e World Safety do projétil são fronteiras ainda abertas; não inferir herança de comportamento vanilla.
- CandyCaneHookItem: treze métodos; use, acInventoryTick, isHookLaunchedInWorld, canLaunchHook, estado ativo/reeling/UUID, enchantability e ItemAbility. Consumidores em CandyCaneHookEntity, GumWormSegmentEntity, ClientEvents, renderer/predicados. Factory lambda$static$179. Já há evidência delimitada do dispatcher ACTickingItem e encantamentos relacionados, não certificação integral. A próxima análise deve seguir launch/reel/attach, distância, cooldown, direção, proprietário, persistência, autoridade e resultado de spawn.
- CaveBoatItem: três campos (type, hasChest e predicado), três corpos incluindo clinit. Quatro factories (25, 26, 145, 146). use recebe stack da mão, raycast Fluid.ANY, passa em MISS, consulta entidades em bounding box expandida pela direção de visão de escala 5 e inflate 1 (não afirmar que este 5 seja alcance do raycast). Retorna PASS se caixa de entidade inflada pelo pick radius contém a posição do olho. Hit BLOCK cria instância normal/com baú no ponto de hit, aplica rotação Y do jogador, falha em colisão; servidor chama addFreshEntity @253 e descarta booleano, solicita GameEvent.ENTITY_PLACE, shrink(1) salvo instabuild. AwardStat e sucesso sided depois; não há prova de aceitação de spawn/claim. Classificar utilitário de transporte após avaliar tipos e entidades.
- CaveBookItem: três corpos; stacksTo(1) e UNCOMMON; factory lambda$static$3. use dispara CONSUME_ITEM e ITEM_USED se ServerPlayer, swing, e openBookGUI apenas cliente; retorna PASS. Nenhum shrink ou custo local. Tooltip cinza. Abrir a GUI não comprova concessão de progressão, e a trigger CONSUME_ITEM não é consumo físico. Boundary do livro e dados de progressão ainda exigem prova.
- CaveInfoItem: sete corpos, subclass BiomeTreatItem, factories 1/2. create constrói stack, vincula CaveBiome e FOOD de BiomeTreat vinculado; getCaveBiome interpreta CUSTOM_DATA; cor por registry e fallback; use tem ramo especial Cave Codex, não atribuir a todos os descendentes. Consumidores SpelunkeryTableMenu, RecipeCaveMap, JEI, GUI, cores e creative tabs. Relação já identificada na #1129; papéis da classe/suas identidades de registro precisam de disposição própria.
- CaveMapItem: doze corpos, campos CHECK_REGEN_TICKS, TRIGGER_REGEN_DIST e MAP_SCALE. Factory lambda$static$4; dispatch acInventoryTick já parcialmente auditado no contrato ACTickingItem: checks locais de 1800 ticks e distância 200 blocos horizontal, sem promessa de cadência efetiva. createMap, createBiomeArray, uso e leitura/persistência de mapa, client render, worker e recipe. Análise seguinte deve acompanhar scheduler, dados salvos, autoridade de busca, unicidade e validade da localização.

18 recursos encontrados por substring de caminho: modelos, recipes, advancements e tags. O resultado contém seus hashes e JSONs. Não é censo de todos os recursos indiretos. Nenhum objeto foi certificado nesta descoberta, ledger e índices não alterados. NO_MUTATION / NOT_VERIFIED / NOT_TESTED, provider OPEN.
