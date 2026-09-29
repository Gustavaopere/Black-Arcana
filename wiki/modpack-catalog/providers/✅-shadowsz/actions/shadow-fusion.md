# Shadow Fusion

- Provider: **ShadowsZ** (`shadowsz`)
- Version: `1.1.9`
- Classificação: **supernatural player action**
- Exact route: `fuseShadows`
- State: `EXACT ACTION / DEPLOYED ATTUNEMENT + CONFIG CONDITIONAL`

## Identidade semântica

Ação independente de fusão sacrificial de shadows. O audit exato distingue esta causalidade de summon/dismiss, progressão, equipment e roster management.

## Reachability

Dois gates implantados são relevantes:

- o jogador precisa passar pelo attunement provider-owned, cuja rota natural depende de `shadowszRestrictPowers`;
- a ação lê `fusionEnabled`.

O artefato declara `fusionEnabled=false` por default, mas default não é evidência do config implantado.

## Semantic disposition

Fusion é a décima raiz exata. Ela só entra no strict quando o estado implantado autorizar alcance normal do jogador e `fusionEnabled=true`.

Source: `../EXACT-1.1.9-ARTIFACT-AUDIT.md`.
