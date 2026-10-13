# Waystone Warp / Teleport

**Prova binária física (2026-10-13):** ✅ `COUNTED_EXACT` — `WaystonesAPI.tryTeleportAsync` confirmado no JAR físico `21.1.45`; shared provider teleport pipeline. [Java21 #38460510230](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38460510230), [dossiê](../EXACT-BINARY-ACTIONS-21.1.45.md). Sem promoção de custo, multiplayer, persistência ou Survival (⚠️); +0 nova ação.

- Provider: **Waystones** (`waystones`)
- Version: `21.1.45`
- Classificação: **supernatural player action**
- Semantic state: `COUNTED_EXACT` (**identidade física estática somente**)
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
