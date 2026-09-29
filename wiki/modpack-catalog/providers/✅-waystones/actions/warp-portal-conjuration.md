# Warp Portal Conjuration

- Provider: **Waystones** (`waystones`)
- Version: `21.1.45`
- Classificação: **portal-conjuration player action**
- Semantic state: `COUNTED_SOURCE_PINNED`
- Strict contribution: `1`
- Provider surface: **Portal Scroll**

## Identidade semântica

A Portal Scroll executa uma raiz sobrenatural distinta do teleport direto: o jogador seleciona um destino e o provider cria um Warp Portal orientado para esse alvo.

A criação do portal é o resultado causal independente desta ação.

## Deduplicação

A travessia posterior do portal não cria uma quarta identidade. O portal reutiliza a raiz já contada **Waystone Warp / Teleport** para settlement de transporte.

## Evidence boundary

A reconciliação source-pinned fecha a separação causal entre portal spawn e teleport settlement. Duração, lifecycle, multiplayer behavior e policy efetivamente implantada permanecem runtime QA.

Source: `../SOURCE-21.1.45-SEMANTIC-CLOSURE.md`.
