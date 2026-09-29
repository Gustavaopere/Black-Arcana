# `shadowsz:umbral_bond`

- Provider: **ShadowsZ** (`shadowsz`)
- Version: `1.1.9`
- Classificação: **Umbral spell**
- State: `EXACT REGISTRY / DEPLOYED ATTUNEMENT CONDITIONAL`

## Identidade semântica

Registro incondicional e independente no spell registry exato. O comportamento de guardian binding observado no audit é downstream de `umbral_bond` e não constitui uma segunda ação.

## Reachability

O pre-cast exato consulta `ShadowSummoner.isAttuned`. A disponibilidade natural do attunement depende do gamerule implantado `shadowszRestrictPowers`, ainda não capturado.

## Evidence boundary

Identidade, registro, deduplicação do helper e gate de attunement estão fechados. Valores quantitativos e detalhes de execução não são inferidos.

Iron's Spells mantém autoridade sobre o host de spell/mana; ShadowsZ mantém autoridade sobre esta identidade e seu comportamento provider-native.

Source: `../EXACT-1.1.9-ARTIFACT-AUDIT.md`.
