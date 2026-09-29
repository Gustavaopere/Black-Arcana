# Shadow Eyes

- Provider: **ShadowsZ** (`shadowsz`)
- Version: `1.1.9`
- Classificação: **supernatural player action**
- Exact route: `toggleShadowEyes`
- State: `EXACT ACTION / DEPLOYED ATTUNEMENT CONDITIONAL`

## Identidade semântica

Ação independente que alterna o estado provider-owned de visão sobrenatural do jogador. Feedback visual/sonoro e efeitos resultantes são downstream desta mesma raiz.

## Reachability

O roteador de ações do jogador é bloqueado por `ShadowSummoner.isAttuned`. O gamerule efetivo `shadowszRestrictPowers` ainda precisa ser capturado no mundo atual.

## Evidence boundary

A existência e a causalidade da ação estão fechadas. Alcance, duração e parâmetros quantitativos não são inferidos.

Source: `../EXACT-1.1.9-ARTIFACT-AUDIT.md`.
