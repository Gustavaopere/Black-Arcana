# Position Swap

- Provider: **ShadowsZ** (`shadowsz`)
- Version: `1.1.9`
- Classificação: **supernatural player action**
- Exact route: `teleportSwap`
- State: `EXACT ACTION / DEPLOYED ATTUNEMENT CONDITIONAL`

## Identidade semântica

Ação independente que troca as posições do jogador e de um shadow e possui cooldown provider-owned. O teleporte é consequência da própria ação, não uma identidade adicional.

## Reachability

O roteador C2S é attunement-gated. O valor efetivo de `shadowszRestrictPowers` ainda precisa ser capturado no mundo atual.

## Evidence boundary

A causalidade de troca de posição e a existência de cooldown estão fechadas; valores, distância e regras detalhadas de destino não são inferidos.

Source: `../EXACT-1.1.9-ARTIFACT-AUDIT.md`.
