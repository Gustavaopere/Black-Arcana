# Ars Elemental 0.7.10.1 — Not Summon (filter)

**✅ Revalidação binária exata (2026-10-13):** `ars_elemental:glyph_not_summon_filter` é ID de registro estático provado no JAR 0.7.10.1 (SHA-1 `a1e4021177aae0e16c1f7c6487a82f0b68bbade3`) por [Java 21 #38403443682](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38403443682). `COUNTED_EXACT` para identidade; já contado, **+0**. Afirmações antigas de ID não verificado / `COUNTED_SOURCE_PINNED` abaixo são checkpoints superados. Mana/config/Survival ⚠️. [Dossiê](../EXACT-BINARY-GLYPHS-RITUALS-0.7.10.1.md).


Estado: **✅ `COUNTED_SOURCE_PINNED` — filtro individualizado** · **⚠️ QA/config pendentes**.

## Identidade source-pinned

- Nome editorial: **Not Summon**, modo **invertido**.
- **Registry ID source-pinned:** `ars_elemental:glyph_not_summon_filter`.
- Predicate da dupla: entity implements Ars `ISummon`.
- Source defaults herdados de `AbstractFilter`: Tier I, mana 0, nenhum augment compatível. `ElementalAbstractFilter` define type index 15 e o tratamento de matching/inverted.
- Provider: `ars_elemental`; JAR físico `ars_elemental-1.21.1-0.7.10.1.jar`, SHA-1 `a1e4021177aae0e16c1f7c6487a82f0b68bbade3`.
- Source pin `Alexthw46/Ars-Elemental@fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d` e Ars Nouveau API base `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`. **A equivalência byte-a-byte entre o source pin e o JAR físico não está provada.**
- Classificação: `COUNTED_SOURCE_PINNED`, **já incluído na contribuição de 47 objetos** (39 partes de spell e oito rituais); **+0 novas identidades** com esta ficha.
- Config efetiva, receitas implantadas, custos modificados e resultados de gameplay em Survival: **⚠️ NÃO VERIFICADOS**. `MethodCarianPhalanx` está excluído (dev-only); `Nullify Defense` tem receita de aprendizado desativada por source default `frame_skip_recipe=false`.


## Boundary de targeting

Este filtro opera dentro do casting Ars. Não cria por si só root cast, lei/seal Order do Black Arcana, novo evento ofensivo ou segunda checagem independente de seleção. IDs e default source não substituem teste da configuração e do comportamento no pack real.

**Authority:** Ars Nouveau/Elemental controlam targeting, mana, aplicação de efeitos e execução. **⛔** Hook Black Arcana sem contrato provider-native segue fail-closed.

**Fontes:** [matriz](../GLYPHS.md) · [acquisition](../ACQUISITION.md) · [registries](../REGISTRIES.md). Clean-room factual, sem código ou assets upstream.
