# Waystone Warp / Teleport

- Provider: **Waystones** (`waystones`)
- Version: `21.1.45`
- Classificação: **supernatural player action**
- Semantic state: `COUNTED_SOURCE_PINNED`
- Strict contribution: `1`

## Identidade semântica

Uma única raiz provider-owned cobre o ato sobrenatural de transportar o jogador por uma destination Waystones validada.

As superfícies Waystone, Sharestone, Portstone, Warp Stone, Warp Scroll, Bound Scroll, Return Scroll, inventory-button, Warp Plate traversal e Warp Portal traversal convergem para o mesmo pipeline de teleport settlement e são deduplicadas nesta identidade.

## Causalidade

A reconciliação source-pinned fecha o settlement central do provider através do pipeline que termina em `WaystonesAPI.tryTeleportAsync(...)`.

As diferentes superfícies de entrada não criam magias independentes porque reutilizam a mesma causalidade de validação, requirements e teleport provider-native.

## Evidence boundary

Esta ficha fecha identidade, ownership, deduplicação e source-level reachability. Costs, cooldowns, permission policy, deny lists, multiplayer settlement e valores efetivamente implantados permanecem runtime QA.

Source: `../SOURCE-21.1.45-SEMANTIC-CLOSURE.md`.
