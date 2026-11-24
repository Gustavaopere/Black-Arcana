# Remote Detonator — censo de registro e consumidores de tickets 1.0.10

**Estado:** evidência estática delimitada; `static_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`, `WORLD_SAFETY_BLOCKED`. Não é um novo objeto catalogável.

## Proveniência e reprodução

- Publisher: Alex's Caves Continued 1.0.10, Minecraft 1.21.1, NeoForge, JAR `alexscaves-1.0.10-neoforge+1.21.1.jar`, 75.279.314 bytes, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- Coleta inicial [#45326182434](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45326182434): 1.555 classes, 6 candidatos, 14 sites; 22.111 bytes, SHA-256 `d1f07af205ec2f8eb189485486441ee7f984e06ea684a29722da406f1791ea1b`.
- Coleta expandida [#45326384195](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45326384195), job 138216868854, HEAD `034d4cdfc0c1581b930826ad580de4e636494c3a`, artifact 14890251581: **1.555 classes, 6 classes candidatas, 21 sites diretos**, e inspeção separada do bootstrap e callback; relatório 46.004 bytes, SHA-256 `3c4b8a9c3f66e05e815eb524b3d00aa43534002bfa034b2d5aaa585088baba9c`. 14 casos sintéticos do filtro aprovados. O escopo do censo é o conjunto exato de proprietários/nomes definido na sonda, não todos os usos reflexivos, mixins ou consumidores externos.
- Sonda: [alexscaves_1010_remote_detonator_ticket_lifecycle_probe.py](../../../../docs/qa/alexscaves_1010_remote_detonator_ticket_lifecycle_probe.py); execução no [workflow](../../../../.github/workflows/alexscaves-1010-remote-detonator-ticket-lifecycle.yml).
- Reuso: [Occult Gem + Beholder](actions/occult-gem-beholder-observation.md), evidências P1–P3 e V1–V3, já documenta o callback e o ciclo do Eye. O presente censo é uma extensão das evidências para o Remote Detonator, não recertificação daquele objeto.

## Registro e callback

`AlexsCaves.registerTicketControllers(RegisterTicketControllersEvent):void` (14 instruções, Code SHA-256 `ef7e29243d96169b0b61edf2e078f9e17d90b23ece93a081b38cb37a5b542396`):

- Offset 9 constrói o ID `alexscaves:forced_chunks`; 12 vincula `LoadingValidationCallback` via bootstrap 12 de `LambdaMetafactory`; 17 solicita a construção de `TicketController(ResourceLocation,LoadingValidationCallback)`.
- Offset 22 solicita `ACPlatform.setTicketController(Object)` antes de `RegisterTicketControllersEvent.register(TicketController)` no offset 27. O setter (3 instruções) executa `putstatic ticketController:Ljava/lang/Object;` no offset 1. Registro solicitado não é prova de evento executado ou aceitação do controller.
- Bootstrap aponta por method handle de tipo 6 para `server/level/storage/ACWorldData.clearLoadedChunksCallback(ServerLevel,TicketHelper):void`, não para lambda local em AlexsCaves. Class SHA-256 `ddb140795a4a38e077575effb858c2f7664780f11046475335ca132200b031f5`, Code SHA-256 `031b43d4234bda3968b06d4ad6460acc5763df92c9a6a1e6d64028acb7d1f112`, 46 instruções.
- Callback: obtém `getEntityTickets()` @3, copia as chaves @11 e chama `removeAllTickets(UUID)` @43 para cada owner; obtém `getBlockTickets()` @53, copia chaves @61 e chama `removeAllTickets(BlockPos)` @93. Incrementa contador uma vez por owner processado @46/@96. A mensagem de debug menciona chunks, mas **o contador do bytecode é de owners processados**, não uma contagem direta dos chunks removidos.
- Trata-se do callback de validação no carregamento; não prova liberação logo após cada uso, nem quantidade efetiva de tickets, nem execução sobre o modpack transformado.

## Censo dos consumidores diretos

As quatro classes abaixo usam os dois overloads compartilhados de `ACPlatform.forceChunk`. Os offsets referem-se ao JAR publisher:

| Classe | Método e site do helper/dispatcher | Argumentos observados |
|---|---|---|
| `RemoteDetonatorItem` | `use` @94 → helper `loadChunksAround` @44 | Jogador UUID, helper solicitado com true; dispatcher recebe booleano do helper e true |
| `OccultGemItem` | `use` @109 → helper @44 | Jogador UUID, helper solicitado com true; dispatcher recebe booleano do helper e true |
| `BeholderEyeEntity` | `tick` @37 e @86 → helper @60/@131 | Helper solicitado com false/true respectivamente; dispatcher de Entity recebe o mesmo booleano nos dois argumentos |
| `NuclearExplosionEntity` | `tick` @211 e `remove` @24 → helper @88 | Helper solicitado com true/false respectivamente; dispatcher de Entity recebe o mesmo booleano nos dois argumentos |

Nas 1.555 classes pesquisadas, existe um único site JVM direto correspondente à assinatura exata do helper `RemoteDetonatorItem.loadChunksAround(ServerLevel,UUID,BlockPos,Z)V`: o `use` @94, precedido por `iconst_1` @93. Nenhuma chamada direta a esse helper com false foi identificada. O censo não exclui reflexão, mixins ou intervenções da engine. A chamada de remoção de NuclearExplosionEntity utiliza a sobrecarga de Entity: não há demonstração de que ela libere tickets adquiridos pelo UUID do jogador no Remote Detonator. O censo identifica consumidor compartilhado, **não prova a cadeia de ignição/spawn entre o item e a explosão**.

Os dois overloads em ACPlatform leem `ticketController` @0/@6, solicitam `TicketController.forceChunk(...):Z` @20, e descartam o booleano (ver [boundaries](EXACT-REMOTE-DETONATOR-BOUNDARIES-1.0.10.json)). Alterar esse dispatcher globalmente afetaria múltiplos consumidores; não constitui um boundary mutador individual de perks.

## Pendências

Contrato da engine 21.1.248 e estado real de tickets, registro efetivo, quotas, unforce, proteção territorial, comportamento cross-dimensional, execução dos callbacks dos blocos e QA física continuam não verificados. Não afirmar vazamento permanente nem garantia de cleanup. A ficha [Remote Detonator](items/remote-detonator.md) continua parcial; nenhuma promoção de índices, casts, hooks ou runtime. A autoridade permanece no provider para tickets e em Black Arcana para seu próprio runtime mágico.
