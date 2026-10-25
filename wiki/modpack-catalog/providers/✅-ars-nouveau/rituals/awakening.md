# Awakening

Status: `SOURCE-PINNED 5.13.1 / ENTITY-WORLD CONVERSION RITUAL`

- Registry id: `ars_nouveau:ritual_awakening`
- Class: `RitualAwakening`
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native modes

### Bookwyrm Charm mode

If any consumed item is a `WritableBookItem`, the ritual enters Bookwyrm mode. Once per 20 server ticks it compares progress with the total count of consumed writable books and emits one `BOOKWYRM_CHARM` for each progress slot until that total is reached, then finishes.

### Awakening mode

Without writable books, after progress exceeds `5` the ritual searches positions within Manhattan bounds `(3,1,3)` around the brazier.

For each candidate position it performs provider DFS searches capped at `350` matching blocks for four Archwood families:

- Blazing;
- Flourishing;
- Vexing;
- Cascading.

A matching tree requires at least `50` connected provider log/leaf blocks. When found, the ritual destroys the returned component through Ars' safe-destroy helper and selects the corresponding Weald Walker entity.

A nearby Budding Amethyst is a separate conversion route: that block is replaced with air and an Amethyst Golem is selected.

After a valid target is resolved, the ritual spawns the selected LivingEntity at the converted location and finishes.

## World-safety boundary

This class does not expose the same explicit `destroyRespectsClaim(...)` preflight seen in some other Ars world-effect paths; it delegates tree removal to `destroyBlockSafelyWithoutSound` with an Ars fake player. Whether all protection providers are respected in the installed full pack is therefore a **runtime QA item**, not inferred from helper naming.

Black Arcana must not replay these block removals/entity creations. Any independent Black Arcana world conversion remains governed by `WorldEffectPolicy`.

## Authority

Weald Walker/Golem identity, Bookwyrm Charm creation and conversion lifecycle remain Ars Nouveau authority. They are not Black Arcana summons/familiars merely because the ritual creates living magical entities.

## Engenharia para perks — contrato de ritual

- **Fonte:** [`RitualAwakening.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualAwakening.java), `com.hollingsworth.arsnouveau.common.ritual.RitualAwakening`, Ars 5.13.1.
- **Modo Bookwyrm:** `isBookwyrms()` identifica qualquer `WritableBookItem` consumido. A cada `20` ticks servidor, quando `progress<numBookwyrms` (soma das contagens dos livros consumidos), gera **1** `BOOKWYRM_CHARM`; caso contrário chama `setFinished()`. `incrementProgress()` ao fim da iteração, não uma receita instantânea que dá todos os charms de uma vez.
- **Modo Archwood/Amethyst:** se não há WritableBookItem e `getProgress()>5`, percorre `BlockPos.withinManhattan(brazier,3,1,3)`; em cada candidato `SpellUtil.DFSBlockstates(...,350,...)` para quatro famílias de troncos/folhas (Blazing/Flourishing/Vexing/Cascading). Conversão requer conjunto com `size>=50`, remove blocos através de `destroyBlockSafelyWithoutSound`/`ANFakePlayer`, então instancia Weald Walker; `BUDDING_AMETHYST` pode virar `AIR` e originar Amethyst Golem.
- **Causalidade e segurança:** uma árvore com até 350 posições candidatas removidas não significa 350 rituais, kills ou recompensas. Não há `destroyRespectsClaim` explícito na classe; o helper/world admission precisa de teste físico antes de afirmar proteção ou bypass. Sem limitação nova no Black Arcana; nenhum adapter de mutation RPG validado.
- **Estado:** ✅ source-pinned; ⚠️ tempo, recursos e proteção exigem observar config/JAR runtime. ⛔ não existe adapter RPG/Black Arcana demonstrado para reescrever Source, progresso, alvos ou world effects deste ritual.

## Certificação técnica estática — world conversion / Bookwyrm (25/10/2026)

**✅ `STATIC_TECHNICAL_CATALOG_ONLY`; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** Classe→ID conferida pelo [manifesto binário](../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md); semântica pela versão fixada de [`RitualAwakening.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualAwakening.java). Isto não prova equivalência integral de métodos com o JAR.

| Campo requerido para perks | Contrato de execução e limite |
|---|---|
| Identidade | `ars_nouveau:ritual_awakening`, `RitualAwakening`, Ars Nouveau `5.13.1`, source `112920ff774831f204031da75b4c4e73d3765157`; publisher JAR SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`. |
| Seleção de modo / tick | `isBookwyrms()` detecta a **presença de qualquer** `WritableBookItem` em `getConsumedItems()` e prioriza o modo Bookwyrm sobre a conversão de árvore/ametista. `canConsumeItem` aceita também livros graváveis, além do `super.canConsumeItem`. No servidor, `gameTime%20==0` é a cadência do ritual; `incrementProgress()` roda ao final de **ambos** os ramos, inclusive no ciclo que chama `setFinished()`. |
| Modo Bookwyrm: contagem e items | `numBookwyrms=sum(ItemStack.getCount())` sobre livros graváveis consumidos; enquanto `getProgress()<numBookwyrms`, instancia **um** `BOOKWYRM_CHARM` como `ItemEntity` na posição do brazier, com vetor inicial X/Z ∈ [-0.1,0.1] e Y ∈ [0.4,0.6], e toca `BOOK_PAGE_TURN`. Em contrário finaliza. `AbstractRitual.onItemConsumed` usa `stack.split(1)` na ingestão padrão, mas entradas agregadas/persistidas e settlement físico exigem QA: não inferir lote máximo ou custo por charm além do loop visível. |
| Modo mundo: gatilho e busca | Sem livros, somente com `getProgress()>5` executa `findTargets` a cada tick elegível até identificar alvo; percorre `BlockPos.withinManhattan(getPos(),3,1,3)`, portanto **não** é uma AABB cúbica ilimitada. Para cada posição testa DFS `SpellUtil.DFSBlockstates(...,350,...)` nas 4 famílias, na ordem **Blazing → Flourishing → Vexing → Cascading**. Um componente conectado de troncos/folhas com tamanho `>=50` admite o Weald correspondente. |
| Modo mundo: transformação | Na primeira árvore admitida, `destroyTree` percorre o conjunto retornado com `BlockUtil.destroyBlockSafelyWithoutSound(world,p,false,ANFakePlayer.getPlayer(world,playerUUID))`; após selecionar tipo e posição, `entity.create(serverLevel)`, `setPos` e `addFreshEntity` geram o Walker, com partículas. Alternativamente, `Blocks.BUDDING_AMETHYST` detectado nas posições de busca é substituído por AIR com `world.setBlock(p,...,3)` e origina `AMETHYST_GOLEM`. O source **não verifica retorno de cada remoção** antes do spawn, nem mostra preflight `destroyRespectsClaim` local. Um bloco transformado ou NPC gerado não é um cast separado. |
| Alvo, dano e duração | Targets são conjuntos de BlockPos/árvores conectadas, ou Budding Amethyst; não há raycast, projétil nem dano direto no `tick()`. DFS tem limite de visita de 350 por busca; o custo de repetir buscas depende de mundo/conteúdo e deve ser testado. O caminho sem alvos não chama `setFinished()` neste ramo e continua aumentando progresso, sujeito ao lifecycle do brazier. |
| Source e authority | Getter `AbstractRitual.getSourceCost()=0` é herdado, **não equivale a ausência de ingredientes/custos de ativação**. `RitualAwakening` não chama `setNeedsSource(true)` localmente. Ars detém criação de charms/Wealds, remoção de blocos e recurso do ritual; proteção de claims, spawn admission, loot/drops, itens consumidos e persistence precisam ser verificados. Black Arcana mantém `WorldEffectPolicy` apenas para mutações próprias; RPG Skill Tree não pode assumir authority do ritual. |

**Gate fail-closed:** nenhuma mutação de raio, filtros, DFS, tipo de spawn, drops, custo/Source ou tempo por perk até existir hook/provider boundary e transações/deduplicação verificadas. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`. Nenhum Stage promovido.
