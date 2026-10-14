# Ars Elemental 0.7.10.1 — Oxidize

**✅ Revalidação binária exata (2026-10-13):** `ars_elemental:glyph_oxidize` é ID de registro estático provado no JAR 0.7.10.1 (SHA-1 `a1e4021177aae0e16c1f7c6487a82f0b68bbade3`) por [Java 21 #38403443682](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38403443682). `COUNTED_EXACT` para identidade; já contado, **+0**. Afirmações antigas de ID não verificado / `COUNTED_SOURCE_PINNED` abaixo são checkpoints superados. Mana/config/Survival ⚠️. [Dossiê](../EXACT-BINARY-GLYPHS-RITUALS-0.7.10.1.md).


Estado: **✅ `COUNTED_SOURCE_PINNED` — Efeito individualizado** · **⚠️ runtime, ID do registry e Survival pendentes**.

## Identidade e defaults source-pinned

- Nome na matriz editorial: **Oxidize**; categoria **Efeito**.
- Provider: `ars_elemental`; JAR físico `ars_elemental-1.21.1-0.7.10.1.jar`, SHA-1 `a1e4021177aae0e16c1f7c6487a82f0b68bbade3`.
- Source pin `Alexthw46/Ars-Elemental@fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d` e Ars Nouveau API base `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`. **A equivalência byte-a-byte entre o source pin e o JAR físico não está provada.**
- Classificação: `COUNTED_SOURCE_PINNED`, **já incluído na contribuição de 47 objetos** (39 partes de spell e oito rituais); **+0 novas identidades** com esta ficha.
- Config efetiva, receitas implantadas, custos modificados e resultados de gameplay em Survival: **⚠️ NÃO VERIFICADOS**. `MethodCarianPhalanx` está excluído (dev-only); `Nullify Defense` tem receita de aprendizado desativada por source default `frame_skip_recipe=false`.

- **Tier:** III.
- **Mana source-default:** 80.
- **Schools:** Water, Air.
- **Compatible augments:** Amplify, Extend Time, Duration Down, Pierce, AoE.
- **Provider-specific defaults/limits:** default potion config 30s / extend 8; executable block path reads Randomize count even though Randomize is not exposed as compatible at this pin.
- **ResourceLocation individual:** **NÃO VERIFICADO na matriz preservada**. Não inferir `ars_elemental:glyph_...` do nome de display.

## Semântica e limites

A matriz não preserva uma observação comportamental adicional para esta entrada; não se deduz comportamento não evidenciado pelo nome.

O Tier, a mana e os parâmetros acima são defaults do source, não medidas do cliente/servidor do pack.

**Authority:** Ars Nouveau/Ars Elemental retêm mana, Source, custos, spell grammar, execução, targeting, world effects e cleanup. Black Arcana não pode cobrar ou resolver novamente o mesmo cast, inserir segundo loop ou mutação. **⛔** Sem contrato real de hook/API, integração fail-closed.

**Fontes:** [matriz](../GLYPHS.md) · [acquisition](../ACQUISITION.md) · [registries](../REGISTRIES.md) · [provider](../README.md). Clean-room: somente fatos registrados na auditoria do Black Arcana, sem código/assets upstream.

## Engenharia de perks — execução individual 0.7.10.1

- **Source commit:** [`EffectOxidize.java`](https://github.com/Alexthw46/Ars-Elemental/blob/fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d/src/main/java/alexthw/ars_elemental/common/glyphs/EffectOxidize.java) na versão de código fixada, não prova binária dos métodos no JAR.
- **Entidade:** aplica `ModPotions.RUST` via IPotionEffect somente em LivingEntity; o modificador de armadura efetivo pertence ao status downstream.
- **Blocos:** calcula AOE/Pierce com `SpellUtil.calcAOEBlocks`, ignora posições fora de altura e faz chance adicional `world.random.nextFloat()<count(Randomize)*0.25` antes de checar claim em cada `pos1`. Depois, para `ChangeOverTimeBlock` com próximo estado e random<0.1, faz `world.setBlockAndUpdate(pos, nextState)` usando **variável original `pos`**, não `pos1` iterada. É discrepância source-level potencial na geometria AOE a registrar, sem confirmar impacto em JAR.
- **Perks:** alterar AOE poderia expandir verificações mas a gravação no `pos` original requer teste; não implementar tratamento de oxidação por interceptação de blocos como se cada pos1 fosse mutado.
- **Status:** ✅ objeto com ID de JAR física comprovada e source observado; ⚠️ runtime, API host, config deploy e controle de claims ainda condicionados; ⛔ nenhum adapter RPG implementado, sem duplicação de settle/hit/Source/mana.
