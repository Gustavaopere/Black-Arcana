# Waystones 21.1.45 — prova física SHA-exata de três ações mágicas

**✅ `COUNTED_EXACT` restrito a três identidades de ações sobrenaturais e seus caminhos causais estáticos, não a `AbstractSpell` nem a spells Iron's.** Campanha de 39 providers **24/39 exatos / 15/39 pendentes**; +0 novas raízes semânticas; mínimos **1857 global / 1855 escopo** inalterados. Cliente, servidor e Survival ⚠️.

## Autoridade física verificável

- Modlist atual sibling, linha física **#564**, `waystones-neoforge-1.21.1-21.1.45.jar`, mod ID `waystones`, SHA-1 `6ec1a176a102212db4f6391886db52ed103c830f`, MC 1.21.1 / NeoForge.
- [Release oficial CurseForge file 8873000](https://www.curseforge.com/minecraft/mc-mods/waystones/files/8873000) de **1219809 bytes**, SHA-1 **`6ec1a176a102212db4f6391886db52ed103c830f`**, corresponde ao JAR físico, sem substituição pela release posterior 21.1.46.
- [Discovery Java 21 #38460218529](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38460218529), [reconciliação de ações #38460374624](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38460374624) e [asserções específicas #38460510230](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38460510230) terminaram em **SUCCESS**.
- Workflow clean-room de auditoria permanece somente em [`audit/waystones-21145-20261013`](https://github.com/Gustavaopere/Black-Arcana/tree/audit/waystones-21145-20261013). Não incorporar JAR, código ou assets à `main`.

## Três ações causalmente distintas

| # | Ação sobrenatural | Evidência compilada no JAR | Ficha | Estado |
|---:|---|---|---|---|
| 1 | Waystone Warp / Teleport | `WaystonesAPI.tryTeleportAsync` delega a `InternalMethods.tryTeleportAsync`; `WarpPortalManager.teleportFromPortal` e `WarpPlateBlockEntity` chegam ao mesmo pipeline | [Teleport](actions/waystone-warp-teleport.md) | ✅ identidade estática |
| 2 | Warp Portal Conjuration | `PortalScrollItem` invoca `WarpPortalManager.spawnPortal(ServerPlayer, Waystone)` para criar portal; travessia posterior utiliza a ação 1 | [Portal](actions/warp-portal-conjuration.md) | ✅ identidade estática |
| 3 | Twinbound Link | `TwinboundFeatherItem.use/onUseTick` produz vínculo usando `TwinboundFeatherLinksComponent.with(UUID)` e acesso a `links()`, sem chamar `tryTeleportAsync` | [Twinbound](actions/twinbound-link.md) | ✅ identidade estática |

As classes citadas pertencem ao package `net.blay09.mods.waystones`. A fonte oficial [Waystones 21.1.45 pinada](SOURCE-21.1.45-SEMANTIC-CLOSURE.md) fornece a análise ampla e deduplicação das demais entradas/aliases de transporte; a prova JAR confirma os pontos causais principais sem declarar uma análise dinâmica de todas as interações.

## Exclusões preservadas

| Superfície | Prova estática | Resultado |
|---|---|---|
| Ativação de Waystone | `WaystoneBlock.handleActivation` chama `PlayerWaystoneManager.activateWaystone` | `EXCLUDED_SETUP_DISCOVERY`; +0 |
| Blank Scroll binding | `BlankScrollItem.useOn` chama `WaystonesAPI.setBoundWaystone` | `EXCLUDED_ITEM_PREPARATION`; +0 |
| Attunement de shard | `WarpPlateBlockEntity.serverTick/attuneShard` e `WaystonesAPI.setBoundWaystone` | `EXCLUDED_AUTOMATED_INFRA_PREPARATION`; +0 |

**PUBLISHER_EQUALS_PHYSICAL_SHA1=PASS**

**PHYSICAL_SEMANTIC_ROOTS=3**

**NEW_SEMANTIC_ROOTS=0**

**EXACT_STATIC_ACTION_AUDIT=PASS**

**RUNTIME_SURVIVAL_NOT_VERIFIED=TRUE**

## Boundary de autoridade e QA pendente

- Waystones continua autoritativo sobre teletransporte, validação de destino, requisitos/custos/cooldowns, portais e vínculo Twinbound; `Balm` fornece a infraestrutura do provider. Black Arcana não deve duplicar cadastro de destinos, teleport settlement nem cobrança de custos. RPG Skill Tree é sibling/provider de progressão e gates, apenas via contrato real.
- A auditoria é **estática**: não comprova build source ↔ JAR, comportamento efetivo de modpack, servidor dedicado, cliente, valores da configuração instalada, sucesso de receitas/loot, permissão, multiplayer, portais e vínculos persistidos, integração Waystones:Sable ou hot reload.
- Nenhum novo root é somado; as três ações eram contabilizadas em `COUNTED_SOURCE_PINNED` e foram promovidas somente quanto à evidência física do JAR.
