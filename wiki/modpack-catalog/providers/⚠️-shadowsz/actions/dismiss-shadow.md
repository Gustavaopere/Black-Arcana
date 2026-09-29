# Dismiss Shadow

- Provider: **ShadowsZ** (`shadowsz`)
- Version: `1.1.9`
- Classificação: **supernatural player action**
- Exact route: `dismiss` / `dismissInternal`
- State: `EXACT ACTION / DEPLOYED ATTUNEMENT CONDITIONAL`

## Identidade semântica

Ação provider-owned que persiste o estado relevante do shadow e desmaterializa sua entidade com efeitos provider-native.

`dismissAll`, group dismiss e group toggle são superfícies batch/alias desta mesma raiz e adicionam **+0**.

## Reachability

O roteador de ações exige attunement. O gamerule efetivo `shadowszRestrictPowers` permanece aberto.

## Authority boundary

ShadowsZ possui dismiss, persistência de roster e lifecycle. Black Arcana não deve executar um segundo caminho de demanifestação/persistência.

Source: `../EXACT-1.1.9-ARTIFACT-AUDIT.md`.
