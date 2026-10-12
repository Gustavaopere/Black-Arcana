# Goety Cataclysm 1.21.1-1.8.2 — quatro aquisições de Focus via crafting comum

**✅ 4/4 caminhos e outputs individualmente comprovados** em `minecraft:crafting_shaped`; **+0 novas identidades semânticas**. Este é um catálogo de receitas de **aquisição**, não quatro feitiços adicionais.

## Evidência do artefato exato

- JAR físico e do publicador: `goety_cataclysm-1.21.1-1.8.2.jar`, mod ID `goety_cataclysm`, runtime `1.21.1-1.8.2`, SHA-1 `4e3052a082200371b36e1a88fdce05e294d82757`, 1.755.990 bytes.
- Modlist `neoforge-rpg-skilltree/main@06ec1d1d586d4fc3cf957223cfc9ac30077f2875`, posição física #306; CurseForge projeto `1224214`, arquivo `8518940`.
- Auditoria **isolada NON-MERGE** `audit/goety-cataclysm-182-4-crafting-focus-20261011@eae06402af7abbe6195e05a41f72cfd27bbf453d`: [workflow #38191990175](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38191990175), **success**, hash do JAR conferido antes de imprimir quatro `CRAFTING_ROW` com apenas o path, tipo, output e número de conditions de topo. Não há redistribuição do JAR ou do corpo JSON de receitas.
- O scanner exigiu exatamente quatro Focus outputs únicos, recipe type distinto de `goety:ritual`, quatro paths exclusivos e condição top-level contada como zero. Não derivou ingredientes nem claims de jogabilidade.

## Matriz nominal do crafting físico

| # | Holder do Focus | Resource path literal no JAR | Recipe type | Result ID | Top-level conditions | Estado |
|---:|---|---|---|---|---:|---|
| 1 | `AMETHYST_CLUSTER_FOCUS` | `data/goety_cataclysm/recipe/focus/amethyst_cluster_focus.json` | `minecraft:crafting_shaped` | `goety_cataclysm:amethyst_cluster_focus` | 0 | `FOCUS_ACQUISITION_DEDUP` |
| 2 | `ASHEN_BREATH_FOCUS` | `data/goety_cataclysm/recipe/focus/ashen_breath_focus.json` | `minecraft:crafting_shaped` | `goety_cataclysm:ashen_breath_focus` | 0 | `FOCUS_ACQUISITION_DEDUP` |
| 3 | `VOID_RUNE_FOCUS` | `data/goety_cataclysm/recipe/focus/void_rune_focus.json` | `minecraft:crafting_shaped` | `goety_cataclysm:void_rune_focus` | 0 | `FOCUS_ACQUISITION_DEDUP` |
| 4 | `WATER_SPEAR_FOCUS` | `data/goety_cataclysm/recipe/focus/water_spear_focus.json` | `minecraft:crafting_shaped` | `goety_cataclysm:water_spear_focus` | 0 | `FOCUS_ACQUISITION_DEDUP` |

## Reconciliação contra os 48 rituais auditados

A [matriz dos 48 rituais `goety:ritual`](RITUAL-INVENTORY-EXACT-1.21.1-1.8.2.md) comprova **24** caminhos rituais de aquisição de Focus e **24** rituais independentes. A tabela acima comprova mais **4** caminhos de crafting comum (não-ritual), resultando em **28/28 Focuses com caminho de aquisição individualmente associado**. O conjunto das 28 receitas de Focus não se soma às identidades mágicas: o provider mantém **52 objetos `COUNTED_EXACT` = 28 Focus + 24 rituais não-Focus**. **+0 novas identidades** e mínimo global **1.851 / 1.849** inalterado.

## Limites

- **Não verificados:** ingredientes, formato 3×3, quantidade de cada ingrediente, progressão, advancement, tag/recipe unlock, recipe book, configuração, custos, eventos de craft e viabilidade em Survival. `minecraft:crafting_shaped` é **recipe type observado**, não certificado de execução no pack.
- A ausência de condições de topo no arquivo não prova ausência de gates em outros sistemas nem habilitação real em todos os servidores.
- A evidência é factual clean-room sob licença **All Rights Reserved**: nomes, paths, IDs e tipo, nunca código, modelos, sprites ou recipe payload do mod.
- Goety e Cataclysm permanecem authorities de Soul Energy, casting e entidades-base; Goety Cataclysm controla estes Focuses e recipes. Black Arcana não assume nem executa suas receitas.

[Índice dos 28 Focuses](FOCUS-CARDS-1.21.1-1.8.2.md) · [auditoria do artefato](EXACT-1.21.1-1.8.2-ARTIFACT-AUDIT.md) · [README](README.md).
