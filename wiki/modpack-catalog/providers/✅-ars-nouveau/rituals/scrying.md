# Scrying

Status: `SOURCE-PINNED 5.13.1 / DIVINATION RITUAL`

- Registry id: `ars_nouveau:ritual_scrying`
- Class: `RitualScrying`
- Completion threshold: `15` progress steps, advanced once per 20 server ticks
- Player application radius: `5` blocks
- Base duration: `60 × 20 × 5 = 6000 ticks` (5 minutes)
- Manipulation Essence multiplier: `×3` (15 minutes)
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native admission

The ritual requires at least one consumed item before start. It accepts:

- at most one Manipulation Essence as duration modifier;
- one target-defining item, either a BlockItem or an item matching a registered `ScryRitualRecipe`.

## Provider-native settlement

At completion, each `ServerPlayer` within radius 5 receives the Ars `SCRYING_EFFECT`. The ritual resolves its target as either:

- `TagScryer`, when the consumed item matches a registered scry ritual recipe; or
- `SingleBlockScryer`, when the target item is a block.

The selected `IScryer` is serialized into the player's persisted NBT under `an_scryer`, then synchronized to the client through the provider packet.

## Black Arcana boundary

Discovery/highlighting state and the serialized scry target remain Ars Nouveau authority. Black Arcana must not infer its own discovery ledger from nearby highlighted blocks or overwrite `an_scryer`.

Any Familiars & Divination integration should observe a supported provider state/hook rather than duplicating the scan/highlight system.

## QA

Source lifecycle is pinned to 5.13.1. Exact recipe-driven target coverage and client presentation in the full pack remain runtime/data QA.

## Dossiê de implementação para perks — ritual exato

- **Classe fonte:** [`RitualScrying.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualScrying.java), fonte `112920ff774831f204031da75b4c4e73d3765157` para Ars 5.13.1.
- **Admissão:** `canStart` exige `getConsumedItems()` não vazio. `canConsumeItem` permite no máximo uma `MANIPULATION_ESSENCE` como modificador e um `BlockItem` ou item que case com `ScryRitualRegistry`.
- **Progresso:** `incrementProgress` a cada `20` ticks no servidor, completa em `>=15`; aplica a `ServerPlayer` em AABB `inflate(5.0)`. A duração de `SCRYING_EFFECT` é `60*20*5` ticks, multiplicada por 3 se Essence consumida (=6000 ou 18000 ticks defaults).
- **Persistência:** resolve `TagScryer` de receita ou `SingleBlockScryer` por BlockItem; `grantScrying` serializa o contrato para a chave `an_scryer` sob `Player.PERSISTED_NBT_TAG` e manda `PacketGetPersistentData`. Não assumir que partículas vistas no cliente são evento de descoberta confiável.
- **Perks:** revela estado persistente, mas um mod externo não deve gravar/modificar `an_scryer` sem contrato público de leitura/escrita.
- **Mutabilidade externa:** ⛔ nenhum adapter RPG provado que altere lifecycle, Source ou raio sem duplicar settlement; 🟡 fórmula/lógica source-pinned; ⚠️ runtime, receitas/config física, addons e Survival pendentes.
