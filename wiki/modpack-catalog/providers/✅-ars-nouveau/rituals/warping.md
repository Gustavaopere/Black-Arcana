# Warping

Status: `SOURCE-PINNED 5.13.1 / TELEPORT RITUAL`

- Registry id: `ars_nouveau:ritual_warping`
- Class: `RitualWarp`
- Activation radius: `5` blocks
- Completion threshold: `3` progress steps, advanced once per 20 server ticks
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native admission

The ritual accepts exactly one `WarpScroll` only when its provider `WARP_SCROLL` data component is valid and `canTeleportWithDim(tile.getLevel())` passes. `canStart` is false until such an item has been consumed.

## Provider-native settlement

At progress 3, the ritual reads the stored `BlockPos` from the consumed Warp Scroll and teleports every `Entity` inside a radius-5 AABB to that position. If a position exists, it also plays the portal-travel sound at the destination and marks the ritual finished.

The destination validation encoded by `WarpScrollData` remains provider authority. This exact path calls entity `teleportTo(x,y,z)` using the stored position; Black Arcana must not substitute its own destination or replay settlement.

## Black Arcana boundary

Warping materially overlaps Space & Displacement but remains an Ars ritual. Black Arcana must not double-teleport, double-consume the scroll or reinterpret this provider destination as a Black Arcana Gate/Recall target.

Independent Black Arcana teleportation continues to use its canonical server-side destination safety contracts.

## QA

Source behavior is pinned to 5.13.1. Cross-dimension/sublevel behavior and interactions with Sable/portal providers remain runtime/integration QA.

## Dossiê de implementação para perks — ritual exato

- **Classe fonte:** [`RitualWarp.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualWarp.java), fonte `112920ff774831f204031da75b4c4e73d3765157` para Ars 5.13.1.
- **Admissão:** `canConsumeItem` admite **um** `WarpScroll`, com `WARP_SCROLL` component, `data.isValid()` e `data.canTeleportWithDim(tile.getLevel())`; `canStart` depende de consumido.
- **Conclusão:** a cada 20 ticks incrementa progress; em `>=3` busca `Entity` em AABB `inflate(5)`, extrai `data.pos().orElse(null)`, chama `entity.teleportTo(x,y,z)` para cada alvo se posição existe, toca som e `setFinished`. **Cuidado:** esse método de `teleportTo(double,double,double)` não mostra transição explícita de dimensão, ainda que a admissão teste `canTeleportWithDim`; efeito cross-dimension exige teste, não promessa.
- **Perks:** alcance, quantidade de alvos, filtros de teleport e consumo de scroll devem preservar ownership Ars; não é uma rota para ignorar gates de deslocamento Black Arcana.
- **Mutabilidade externa:** ⛔ nenhum adapter RPG provado que altere lifecycle, Source ou raio sem duplicar settlement; 🟡 fórmula/lógica source-pinned; ⚠️ runtime, receitas/config física, addons e Survival pendentes.

## Certificação técnica estática de ritual — segundo lote (25/10/2026)

**✅ `STATIC_TECHNICAL_CATALOG_ONLY` — contrato estático completo da ficha; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** Prova não cobre hook seguro, config implantada nem aceitação do modpack.

| Campo de perk | Evidência estática no provider |
|---|---|
| Identidade e release | `ars_nouveau:ritual_warping`; `RitualWarp`; Ars Nouveau 5.13.1. [Source imutável](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualWarp.java) e [registry exato do publisher](../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). |
| Execução, ramificações e settlement | `canConsumeItem(ItemStack)` exige `WarpScroll`, lista de consumidos vazia, componente `DataComponentRegistry.WARP_SCROLL` não-nulo, `data.isValid()` e `data.canTeleportWithDim(tile.getLevel())`. `canStart()` exige um item consumido. No `tick` server a cada `gameTime%20==0`, incrementa progresso; ao chegar a 3 lê `getConsumedItems().get(0)` e `data.pos().orElse(null)`, busca entidades na AABB e chama `Entity.teleportTo(x,y,z)` **somente se posição existir**, toca `PORTAL_TRAVEL` e finaliza `setFinished()` mesmo que destino opcional seja vazio. |
| Fórmulas, parâmetros, limites e caps | Threshold `progress>=3`, incremento por `20 game ticks` em servidor; `AABB(getPos()).inflate(5)`, inclui `Entity` (não apenas LivingEntity ou Player). A classe **não** testa localmente proteção/colisão/border por destino, não prova proteção por validação externa. `canTeleportWithDim` é gate de admissão do item; o `teleportTo(double,double,double)` usado na finalização **não mostra mudança explícita de dimensão**. Distância entre mundo origem/destino não é `5`: 5 é seleção local de entidades. |
| Targeting, área/volume, duração, dano e projétil | Todos `Entity` retornados por AABB do ritual que passarem pelo fluxo; destino é BlockPos do scroll, usando coordenadas inteiras. Sem projétil, dano, AttackType, range de Form ou refresh de status. Partículas client-side (10 por tick) são VFX e não teletransportes independentes. |
| Resource cost, cooldown, receita/admissão | `AbstractRitual.getSourceCost()=0` herdado; exige consumir **um WarpScroll válido** e não aceita segundo. Não equivale a ritual sem custo: scroll já consome item e Source/Energy transacional externa ao getter não foi testada em pack. Não alegar cross-dimension funcional só porque o item aceita seu componente. Custo de magia `SpellResolver` de Form/Effect é N/A neste ritual. |
| Política de mundo e integração entre projetos | Não executar um teleport Black Arcana paralelo, nem gravar o item/alterar destino/ignorar limites de dimensão por perks sem contrato formal. QA físico de collision, chunks, spawn safety e portais intermods necessário. Autoridade de execução e fonte/Source pertence ao Ars; RPG Skill Tree fornece progressão/atributos/Mastery/gates mediante contrato real, Black Arcana detém seu runtime/rituais e WorldEffectPolicy para suas mutações próprias, sem interceptar automaticamente este ritual. |
| Grau de evidência/QA | `PINNED_SOURCE_PLUS_SHA_EXACT_BINARY_IDENTITY`: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` para métodos e publisher `ars_nouveau-1.21.1-5.13.1.jar` SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd` para **ID/classe registrada**. Não foi comprovada equivalência byte-a-byte dos métodos, configuração atual, side/claims reais, multiplayer ou QA físico. |

**Gate fail-closed:** alteração de geometria, itens, persistência, energia/Source ou consumer exige hook real, orçamento, transação e deduplicação provados; o ✅ é documental, não implementação de perk ou promoção de Stage 06.05/09.
