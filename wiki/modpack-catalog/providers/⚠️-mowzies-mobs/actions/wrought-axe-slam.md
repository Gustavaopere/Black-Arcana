# Wrought Axe Slam

- Provider: **Mowzie's Mobs** (`mowziesmobs`)
- Version: `1.8.2`
- Provider ability id: `wrought_axe_slam`
- Classificação: **active provider weapon power**
- Provider surface: ItemWroughtAxe
- State: `COUNTED_EXACT`

## Identidade semântica

Segunda ação ativa provider-owned do Wrought Axe, distinta de Swing no registry exato. Ondas, impacto e animação downstream adicionam +0.

## Reachability

O exact artifact referencia este slot diretamente a partir de `ItemWroughtAxe`; runtime de obtenção/uso permanece provider-owned.

## Evidence boundary

A ficha registra somente identidade, causalidade, deduplicação e reachability já sustentadas pelo catálogo canônico. Fórmulas, dano, duração, cooldown/durabilidade, animação, networking e demais detalhes finos não são inferidos.

Source: `../PLAYER-MAGIC-INVENTORY.md`.
