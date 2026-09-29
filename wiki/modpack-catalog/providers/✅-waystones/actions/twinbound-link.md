# Twinbound Link

- Provider: **Waystones** (`waystones`)
- Version: `21.1.45`
- Classificação: **cooperative ritual-like supernatural action**
- Semantic state: `COUNTED_SOURCE_PINNED`
- Strict contribution: `1`
- Provider surface: **Twinbound Feather**

## Identidade semântica

Ação cooperativa independente em que dois jogadores usam Twinbound Feathers de forma sincronizada e mutuamente direcionada.

A conclusão persiste estado recíproco de vínculo provider-owned. Uma Feather vinculada pode então expor o parceiro como destination dinâmica no ecossistema Waystones.

## Deduplicação

Criar o vínculo não executa o teleport e não duplica a raiz **Waystone Warp / Teleport**. O vínculo prepara estado persistente de destino; o eventual transporte continua pertencendo ao pipeline normal do provider.

## Evidence boundary

A identidade, persistência causal e source-level reachability estão fechadas. Timing da interação, edge cases multiplayer, reconnect/persistence e policy de servidor permanecem QA de runtime.

Source: `../SOURCE-21.1.45-SEMANTIC-CLOSURE.md`.
