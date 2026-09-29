# Boulder Lift

- Provider: **Mowzie's Mobs** (`mowziesmobs`)
- Version: `1.8.2`
- Provider ability id: `spawn_boulder`
- Classificação: **Geomancy player power**
- Provider surface: Earthrend / Geomancy
- State: `COUNTED_EXACT`

## Identidade semântica

Raiz Geomancy que representa o fluxo player-facing de erguer e lançar/interagir com um boulder. O slot técnico `hit_boulder` pertence a esse mesmo fluxo causal e adiciona +0.

## Reachability

A superfície Earthrend/Geomancy e a rota de aquisição do provider estão fechadas em nível de catálogo; worldgen/trade settlement permanece runtime QA.

## Evidence boundary

A ficha registra somente identidade, causalidade, deduplicação e reachability já sustentadas pelo catálogo canônico. Fórmulas, dano, duração, cooldown/durabilidade, animação, networking e demais detalhes finos não são inferidos.

Source: `../PLAYER-MAGIC-INVENTORY.md`.
