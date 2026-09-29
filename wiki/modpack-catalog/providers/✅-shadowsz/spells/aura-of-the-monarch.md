# `shadowsz:aura_of_the_monarch`

- Provider: **ShadowsZ** (`shadowsz`)
- Version: `1.1.9`
- Classificação: **Umbral spell**
- State: `EXACT REGISTRY / DEPLOYED ATTUNEMENT CONDITIONAL`

## Identidade semântica

Registro incondicional e independente no spell registry exato. Aura/helper conversion state pertence à execução downstream deste spell e adiciona **+0** raízes.

## Reachability

O pre-cast exato consulta `ShadowSummoner.isAttuned`. A rota natural de attunement depende do gamerule efetivo `shadowszRestrictPowers`, ainda não capturado no mundo implantado.

## Evidence boundary

Identidade, registro, deduplicação dos helpers e gate de attunement estão fechados. Números de balanceamento e fórmulas permanecem `NÃO VERIFICADO`.

Iron's Spells mantém autoridade sobre o host de spell/mana; ShadowsZ mantém autoridade sobre esta identidade e sua execução.

Source: `../EXACT-1.1.9-ARTIFACT-AUDIT.md`.
