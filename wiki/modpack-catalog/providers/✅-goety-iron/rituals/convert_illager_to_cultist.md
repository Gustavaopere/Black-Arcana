# Goety Iron 3.1 — ritual `convert_illager_to_cultist`

Estado: **✅ CATALOGADO / `COUNTED_EXACT`** · ⚠️ execução real de Survival, config e API de ritual **pendentes**.

## Identidade física e semântica

- **Ordinal não-Focus:** 4/12; ordinal no JAR ordenado por path: 4/14.
- **Resource path literal:** `data/goetyiron/recipe/convert_illager_to_cultist.json`.
- **Recipe type do pacote:** `goety:ritual`.
- **Campo `ritual_type`:** `goety:convert_complete_tamed`.
- **Resultado semântico do ritual:** `goetyiron:cultist_servant`.
- **Campo `result_ids` literal:** `goety:jei_dummy/none`.
- **Condições no topo:** `[]` (sem condition declarada capturada no topo, não significa ausência de custo/requisito runtime).
- **JAR físico e publisher hash-matched:** `GoetyIron-1.21.1-NeoForge-3.1.jar` / SHA-1 `c8529867e798661ed01fb2948abda23735888fc6`.
- **Classe de evidência:** `COUNTED_EXACT`; matriz [14/14 paths](../RITUAL-INVENTORY-EXACT-3.1.md), reauditoria textual [#38186445480](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38186445480).
- **Delta desta ficha:** **+0 novas identidades semânticas** — receita e outcome já contabilizados entre os 12 não-Focus.

## Natureza da operação

O campo `ritual_type` é `goety:convert_complete_tamed`. O identificador `goetyiron:cultist_servant` é o destino semântico de conversão/summon documentado no payload da recipe. O `result_ids` `goety:jei_dummy/none` é um **marcador placeholder**, não item de recompensa, spell nem registry de cast independente.

Esta ficha documenta **um ritual empacotado pelo addon**, não uma magia de casting nova do Black Arcana. O path não é promovido a registry ID de spell independente.

## Ownership e execução condicionada

Goety controla infraestrutura de rituais, Soul Energy e servant lifecycle; Iron's fornece entidades/spell substrate quando usado; Goety Iron controla a adaptação e este pacote de receitas. O Black Arcana não duplica somas de custos, owner de servant, execução do ritual ou efeitos de outcome. Na ausência de API/evento provider-native comprovado para a versão física, qualquer bridge permanece **⛔ fail-closed**.

**NÃO VERIFICADOS individualmente** nesta catalogação: entradas e catalisadores da recipe, quantidades, custos, tempos, gating, criatura de origem/estado anterior, condições externas/configs, chunk/dimensão, multiplicidade, XP/Mastery, câmbio de owner e comportamento em servidor dedicado real/Survival.

## Referências

- [Matriz nominal do JAR exato](../RITUAL-INVENTORY-EXACT-3.1.md).
- [Inventário semântico original](../EXACT-3.1-ARTIFACT-AUDIT.md).
- [Contrato do provider](../README.md).

Clean-room factual: nenhum corpo de receita, classe, assets ou código de terceiros incluído.
