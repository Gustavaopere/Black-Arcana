# Goety Cataclysm 1.21.1-1.8.2 — ritual `thrall__summon_urchinkin_servant_thrall`

Estado: **✅ catalogado / `COUNTED_EXACT`** · **⚠️ físico/Survival/integração não testados**.

## Identidade do ritual no JAR

- **Recipe path literal:** `data/goety_cataclysm/recipe/thrall/summon_urchinkin_servant_thrall.json`.
- **Recipe type:** `goety:ritual`.
- **Subtipo `ritual_type`:** `goety:summon_tamed`.
- **Outcome semântico exato:** `goety_cataclysm:urchinkin_servant`.
- **`result_ids` do scanner:** `goety:jei_dummy/none`.
- **Conditions de topo capturadas:** `[]`.
- **Classificação editorial factual:** `SUMMON_THRALL`.
- **Posição na lista não-Focus:** 23/24; índice no arquivo: 47/48.
- **Artefato:** `goety_cataclysm-1.21.1-1.8.2.jar`, SHA-1 físico/publicador `4e3052a082200371b36e1a88fdce05e294d82757`; CurseForge `1224214 / 8518940`.
- **Evidência:** [matriz 48/48](../RITUAL-INVENTORY-EXACT-1.21.1-1.8.2.md) e [auditoria SHA-matched #38190078609](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38190078609).
- **Delta no ledger:** **+0 novas identidades semânticas**; este ritual já integrava os 24 objetos `COUNTED_EXACT` não-Focus.

## Operação semântica limitada

O subtipo `goety:summon_tamed` comprova a classificação de invocação/thrall com outcome `goety_cataclysm:urchinkin_servant`. Não implica uma second cast action ou propriedade de servant pelo Black Arcana.
O marcador `goety:jei_dummy/none` em `result_ids` é **placeholder**, não a entidade invocada/convertida e não uma identidade extra.

## Autoridade, limites e QA

Goety controla execução de rituais, Soul Energy e servant lifecycle; Cataclysm mantém entidades-base; Goety Cataclysm mantém as suas adaptações e recipes. Black Arcana não replica o engine ritual ou seus custos/efeitos. Sem interface provider-native demonstrada, a integração é **⛔ fail-closed**.

**NÃO VERIFICADOS individualmente:** inputs/ingredientes, custos, Soul, duração, target anterior, configuração, progressão, owner, dano, persistência, cliente, dedicated server com pack real, multiplayer e Survival. A absence de conditions de topo não valida receita executável.

[Inventário canônico](../RITUAL-INVENTORY-EXACT-1.21.1-1.8.2.md) · [auditoria agregada](../EXACT-1.21.1-1.8.2-ARTIFACT-AUDIT.md) · [README](../README.md). Documentação clean-room factual, sem redistribuição de material ARR.
