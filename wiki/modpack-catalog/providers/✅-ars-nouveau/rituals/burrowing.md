# Burrowing

Status: `SOURCE-PINNED 5.13.1 / RITUAL`

- Registry id: `ars_nouveau:ritual_burrowing`
- Class: `RitualDig`
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native behavior

On start, the ritual creates an `EntityRitualProjectile` linked to the ritual tile. Server-side, once per 20 game ticks, it advances one layer downward from the ritual position and attempts to break four positions in its configured cross/column pattern.

A block is eligible only when:

- its destroy speed is non-negative;
- Ars Nouveau's `SpellUtil.isCorrectHarvestLevel(5, ...)` passes;
- `BlockUtil.destroyRespectsClaim(...)` passes.

Eligible blocks are settled through a provider fake player using a diamond pickaxe context and Ars Nouveau's safe-destroy utility. The ritual ends when its next position is outside build height.

Provider description: digs four adjacent holes to bedrock and drops the affected blocks.

## Authority / Black Arcana boundary

Burrowing is an Ars-owned destructive world ritual. Black Arcana must not replay its block breaks, drops or claim checks and must not treat each broken block as a separate cast/ritual completion.

Any independent Black Arcana terrain destruction remains subject to `WorldEffectPolicy`; Ars' own claim-aware destruction does not grant Black Arcana permission to bypass its policy.

## QA

Source semantics are pinned to 5.13.1. Full-pack claim-provider, drop and performance behavior remains runtime QA.

## Engenharia para perks — execução do ritual

- **Source pin:** [`RitualDig.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualDig.java), versão Ars Nouveau 5.13.1.
- **Ativação:** `RitualDig.onStart` cria `EntityRitualProjectile` ligado à posição do ritual. `tick()` no servidor trabalha a cada `20` game ticks.
- **Geometria:** começa em `tile.getBlockPos().north().below(context.progress)`, tenta **quatro** `BlockPos`: posição original, `south().south()`, `south().east()`, `south().west()`; depois `progress++` produz próxima camada. Sai quando o próximo anchor está fora de build height.
- **World/admission:** `canBlockBeHarvested` exige destroy speed >=0 e `SpellUtil.isCorrectHarvestLevel(5,...) `; cada bloco exige `BlockUtil.destroyRespectsClaim`. O provider usa fake player e `Items.DIAMOND_PICKAXE` com `destroyBlockSafely`. **Perks:** não converter em mineração instantânea infinita nem bypass de claims. Black Arcana world effects sempre WorldEffectPolicy.
- **Status:** ✅ código fonte exato; ⚠️ configurações e comportamento físico dos providers adicionais pendentes; ⛔ mutabilidade em ritual ou integração com Mastery não é provada pelos eventos de glyph. Ritual runtime permanece Ars Nouveau.

## Certificação técnica estática para perks — mineração (25/10/2026)

**✅ `STATIC_TECHNICAL_CATALOG_ONLY` · ⛔ `mutating_hook=NOT_VERIFIED` · ⚠️ `physical_qa=NOT_TESTED`.** Identidade `ars_nouveau:ritual_burrowing` ↔ `RitualDig` confirmada pela [auditoria binária compilada](../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). Fluxo analisado em [`RitualDig.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualDig.java), [`EntityRitualProjectile.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/EntityRitualProjectile.java) e [`BlockUtil.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/BlockUtil.java), no source revision `112920ff774831f204031da75b4c4e73d3765157`. Publisher `ars_nouveau-1.21.1-5.13.1.jar`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`: apenas vínculo ID↔classe é comprovado no binário, não equivalência integral dos métodos.

| Campo relevante | Evidência e limite de alteração |
|---|---|
| Ativação e cadência | `RitualDig.onStart` chama `super.onStart`; se `tile != null`, instancia `EntityRitualProjectile` em `getPos().above()`, centraliza X/Z e define `tilePos` antes de `addFreshEntity`. **Não há guarda de lado explícita em `onStart`**: verificar duplicação/side in-game. `tick()` só minera a cada `gameTime%20==0 && !world.isClientSide`. |
| Geometria exata | Âncora `tile.getBlockPos().north().below(getContext().progress)`; quatro candidatos por camada: **âncora, `south().south()`, `south().east()`, `south().west()`**. Avança `context.progress++` após tentar os quatro, independentemente de quantos foram realmente quebrados. Não é AABB contínua, esfera ou varredura de 3×3. |
| Limites e condições | Se a **âncora** estiver fora da altura de construção (`isOutsideBuildHeight`), chama `onEnd()` e retorna. Cada candidato exige destroy speed `>=0`, `SpellUtil.isCorrectHarvestLevel(5,...)` e `BlockUtil.destroyRespectsClaim` com fake player. Duração total depende de altura inicial, ticks do mundo e carregamento da área; não traduzir em cooldown de magia. |
| Efeito/settlement | Quando elegível, `breakBlock` chama `state.getBlock().playerDestroy(..., Items.DIAMOND_PICKAXE)` **antes** de `destroyBlockSafely(..., false, fakePlayer)`. `BlockUtil.destroyBlockSafely` posta outra `BlockEvent.BreakEvent` e pode retornar `false`; o resultado **não é conferido por `RitualDig.breakBlock`**. Assim, preflight de claim não prova sucesso da mutação, drop único ou reversão dos callbacks. |
| Projétil, dano e alvo | O `EntityRitualProjectile` vinculado ao brazier é componente visual/lifecycle que anima a posição e se descarta quando não encontra tile/ritual; o caminho de **quebra** ocorre no `tick` do ritual, não por impacto de projétil. Não há `DamageType`, raycast ofensivo ou escala de dano por projétil provados neste fluxo. |
| Custo, persistência e autoridade | `RitualDig` herda `AbstractRitual.getSourceCost()=0` (Source local declarado; **não equivale a ritual grátis**). Ingredientes/tablet, NBT do `RitualContext`, regras de World/claims, drops e callbacks são Ars/NeoForge. `context.progress` é persistido pelo contexto; comportamento real após unload/reload, múltiplos chunks e builders externos exige QA. |
| Contrato RPG/Black Arcana | Nenhuma perk pode multiplicar drops, ignorar `BlockEvent.BreakEvent`, gerar XP por cada bloco/tick ou aumentar profundidade/área sem hook e budget comprovados. `WorldEffectPolicy` protege mutações *próprias* do Black Arcana e **não substitui** o preflight do Ars. RPG Skill Tree só forneceria perks/Mastery por um boundary real, com causalidade e deduplicação. |

**Gate fail-closed:** testar claims, callbacks e drop accounting, spawn/side de `EntityRitualProjectile`, persistência e custo real do brazier. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; nenhuma transmutação/adapter implementada.
