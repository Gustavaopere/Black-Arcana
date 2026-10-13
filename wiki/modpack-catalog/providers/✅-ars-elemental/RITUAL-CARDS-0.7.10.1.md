# Ars Elemental 0.7.10.1 — oito rituais individualizados

**✅ Checkpoint binário 2026-10-13:** [8/8 rituais exatos por JAR publisher/físico](EXACT-BINARY-GLYPHS-RITUALS-0.7.10.1.md), [Java 21 #38403443682](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38403443682); status registry `COUNTED_EXACT`, **+0** objetos novos, mínimos globais atuais 1857/1855. Config, consumo Source, effects e Survival ⚠️. Referências source-pinned abaixo são checkpoints históricos.


Estado **✅ 8/8 `COUNTED_SOURCE_PINNED`** com IDs e semântica documentados, **⚠️ config, Source/casting no pack e gameplay Survival pendentes**.

- Source pin `Alexthw46/Ars-Elemental@fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d`, JAR `ars_elemental-1.21.1-0.7.10.1.jar` SHA-1 `a1e4021177aae0e16c1f7c6487a82f0b68bbade3`. A [auditoria RITUALS.md](RITUALS.md) inclui contratos herdados do Ars Nouveau 5.13.1.
- **8/8 IDs e defaults source-pinned**; não há prova de execução física nem equivalência byte-a-byte entre fonte e artefato.
- `ritual_archwood_forest`: **50 Ars Source a cada cinco placements bem-sucedidos**, não 50 one-shot. `ritual_archwood_forestation` herda `getSourceCost()=0`, não provar consumo positivo inexistente.
- 39 glyphs + oito rituais = 47 identidades já contabilizadas. **+0 novas identidades semânticas** nesta individualização. Sem promoção da Stage 06.05.

| # | Ritual ID | Ficha |
|---:|---|---|
| 1 | `ars_elemental:ritual_attraction` | [Abrir](rituals/cards/ritual_attraction.md) |
| 2 | `ars_elemental:ritual_detection` | [Abrir](rituals/cards/ritual_detection.md) |
| 3 | `ars_elemental:ritual_pollination` | [Abrir](rituals/cards/ritual_pollination.md) |
| 4 | `ars_elemental:ritual_repulsion` | [Abrir](rituals/cards/ritual_repulsion.md) |
| 5 | `ars_elemental:ritual_squirrels` | [Abrir](rituals/cards/ritual_squirrels.md) |
| 6 | `ars_elemental:ritual_tesla_coil` | [Abrir](rituals/cards/ritual_tesla_coil.md) |
| 7 | `ars_elemental:ritual_archwood_forest` | [Abrir](rituals/cards/ritual_archwood_forest.md) |
| 8 | `ars_elemental:ritual_archwood_forestation` | [Abrir](rituals/cards/ritual_archwood_forestation.md) |

**⚠️** Consumo de Source, claims/world mutations, recipes, biome/feature effects, config real e persistência precisam de QA físico provider-native. Nenhuma chamada duplicada/adapter sem hook comprovado. Clean-room factual.
