# Summon Shadow

- Provider: **ShadowsZ** (`shadowsz`)
- Version: `1.1.9`
- Classificação: **supernatural player action**
- Exact route: `summon`
- State: `EXACT ACTION / DEPLOYED ATTUNEMENT CONDITIONAL`

## Identidade semântica

Ação provider-owned que materializa um shadow armazenado. O audit exato confirma consumo de mana do Iron's e efeitos provider-native de manifestação/portal/teleporte.

`summonAll`, group summon e group toggle são superfícies batch/alias desta mesma causalidade e adicionam **+0** raízes.

## Reachability

O roteador C2S exige attunement. O gamerule implantado `shadowszRestrictPowers` ainda não foi capturado.

## Authority boundary

ShadowsZ possui summon, roster e lifecycle; Iron's possui mana. Black Arcana não deve duplicar settlement ou entidade.

Source: `../EXACT-1.1.9-ARTIFACT-AUDIT.md`.
