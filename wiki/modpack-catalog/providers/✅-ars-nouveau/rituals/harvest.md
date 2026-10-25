# Harvest

Status: `SOURCE-PINNED 5.13.1 / CROP-PROCESSING RITUAL`

- Registry id: `ars_nouveau:ritual_harvest`
- Class: `RitualHarvest`
- Source cost declaration: `100`
- Processing cadence: every `200` game ticks
- Horizontal range: `4` blocks; inspected vertical band: `-1..+1`
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native behavior

Every 200 ticks, Harvest scans its bounded crop volume and handles provider-supported crop forms:

- mature Nether Wart: rolls drops, retains one replant unit, resets age to `0`;
- mature Cocoa: rolls drops, retains one replant unit, resets age to `0`;
- tagged harvest stems: processes drops and safely destroys the upper stem block;
- mature `CropBlock`: rolls drops, retains one matching seed/block item where available, then resets the crop to age `1`.

Generated drops are first inserted through the ritual tile's `InventoryManager` into connected/available storage. Remainders are spawned into the world. Mage Bloom Crop items are explicitly excluded from this insertion/drop path.

The processing helper calls `setNeedsSource(true)` on successful crop processing; the ritual's Source cost declaration is `100`. Because `needsSource` is provider state rather than a local integer debit in this class, this page does not infer one 100-Source payment per individual crop.

## Authority / Black Arcana boundary

Crop maturation checks, drop calculation, replanting, adjacent inventory insertion and Source settlement are Ars Nouveau authority. Black Arcana must not duplicate outputs, replant twice or grant per-crop cast/progression credit.

## QA

Source behavior is pinned to 5.13.1. Effective Source debit batching and compatibility with modded crop/drop/storage hooks remain runtime QA.

## Engenharia para perks — execução do ritual

- **Source pin:** [`RitualHarvest.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualHarvest.java), versão Ars Nouveau 5.13.1.
- **Volume/cadência:** `RitualHarvest.tick` roda a cada `200` ticks, percorrendo blocos de `pos.offset(4,-1,4)` a `pos.offset(-4,1,-4)` (9×3×9 posições candidatas antes de redirecionar para blocos acima). Não é varredura ilimitada, mas cada tentativa de drops e inventário tem custo.
- **Culturas:** Nether Wart AGE=3, Cocoa AGE=2, `HARVEST_STEMS` e `CropBlock.isMaxAge`. `processAndSpawnDrops` usa `Block.getDrops`, reduz uma seed/bloco quando replantando, tenta `tile.getInventoryManager().insertStack` e emite `ItemEntity` para sobras; exclui `MAGE_BLOOM_CROP` desse caminho.
- **Custo:** `setNeedsSource(true)` após work e `getSourceCost=100`; não inferir pagamento 100 a cada cultura a partir deste boolean. **Perks:** quantity, seed/loot/replant e Source pertencem à transação Ars; observer não pode duplicar drops.
- **Status:** ✅ código fonte exato; ⚠️ configurações e comportamento físico dos providers adicionais pendentes; ⛔ mutabilidade em ritual ou integração com Mastery não é provada pelos eventos de glyph. Ritual runtime permanece Ars Nouveau.

## Certificação técnica estática de ritual — segundo lote (25/10/2026)

**✅ `STATIC_TECHNICAL_CATALOG_ONLY` — contrato estático completo da ficha; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** Prova não cobre hook seguro, config implantada nem aceitação do modpack.

| Campo de perk | Evidência estática no provider |
|---|---|
| Identidade e release | `ars_nouveau:ritual_harvest`; `RitualHarvest`; Ars Nouveau 5.13.1. [Source imutável](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualHarvest.java) e [registry exato do publisher](../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). |
| Execução, ramificações e settlement | No lado cliente só gera partículas; no servidor, a cada `gameTime%200==0`, percorre `BlockPos.betweenClosed(pos.offset(4,-1,4),pos.offset(-4,1,-4))`. `FarmBlock`, `CropBlock` acima, NetherWart acima ou `HARVEST_STEMS` acima redirecionam a posição para `blockpos.above()` antes do processamento. Nether Wart madura AGE3 e Cocoa AGE2 chamam `processAndSpawnDrops`, resetam age0 e marcam Source; `HARVEST_STEMS` com bloco inferior igual processa drops e chama `BlockUtil.destroyBlockSafely`; `CropBlock.isMaxAge` processa drops e reseta para age1. |
| Fórmulas, parâmetros, limites e caps | Varredura nominal XZ±4 e Y−1..+1 (**9×3×9=243 posições candidatas**) antes de poder subir um bloco — posição efetivamente processada pode alcançar Y+2. `processAndSpawnDrops` faz `Block.getDrops`, opcionalmente reduz uma seed de BlockItem que replanta a mesma cultura; tenta `InventoryManager.insertStack`, cria `ItemEntity` para sobras; suprime output de `MAGE_BLOOM_CROP`. `setNeedsSource(true)` no helper e nos callbacks de wart/cocoa, mesmo que nenhum item seja depositado. Não inferir quantidade determinística de loot com RNG/data packs. |
| Targeting, área/volume, duração, dano e projétil | Mundo/blocos de crop no volume definido; modded crops dependem de implementação vanilla/Tag, sem alvo de Form, projétil, dano, tipo de dano ou efeito de duração próprios. Drops/estoques/conteúdo do mundo são Ars-owned, e `WorldEffectPolicy` Black Arcana só governa seus efeitos próprios. |
| Resource cost, cooldown, receita/admissão | `getSourceCost()=100 Source`, `setNeedsSource(true)` por tentativas de processamento bem-sucedidas; não concluir 100 por crop nem afirmar atomicidade entre drops, seed, armazenamento e consumo. Receita de start, claims e storage externo exigem evidência física. Custo de magia `SpellResolver` de Form/Effect é N/A neste ritual. |
| Política de mundo e integração entre projetos | Não duplicar drops/seed/replant, duplicar Mastery por bloco ou bypassar protections. `BlockUtil.destroyBlockSafely` e `world.setBlockAndUpdate` nessa classe não provam `destroyRespectsClaim` antes de todas as alterações; claims, lock de inventários, datapacks e save/restart devem ser QA físico. Autoridade de execução e fonte/Source pertence ao Ars; RPG Skill Tree fornece progressão/atributos/Mastery/gates mediante contrato real, Black Arcana detém seu runtime/rituais e WorldEffectPolicy para suas mutações próprias, sem interceptar automaticamente este ritual. |
| Grau de evidência/QA | `PINNED_SOURCE_PLUS_SHA_EXACT_BINARY_IDENTITY`: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` para métodos e publisher `ars_nouveau-1.21.1-5.13.1.jar` SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd` para **ID/classe registrada**. Não foi comprovada equivalência byte-a-byte dos métodos, configuração atual, side/claims reais, multiplayer ou QA físico. |

**Gate fail-closed:** alteração de geometria, itens, persistência, energia/Source ou consumer exige hook real, orçamento, transação e deduplicação provados; o ✅ é documental, não implementação de perk ou promoção de Stage 06.05/09.
