# Ars Elemental 0.7.10.1 — Conjure Terrain

**✅ Revalidação binária exata (2026-10-13):** `ars_elemental:glyph_conjure_terrain` é ID de registro estático provado no JAR 0.7.10.1 (SHA-1 `a1e4021177aae0e16c1f7c6487a82f0b68bbade3`) por [Java 21 #38403443682](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38403443682). `COUNTED_EXACT` para identidade; já contado, **+0**. Afirmações antigas de ID não verificado / `COUNTED_SOURCE_PINNED` abaixo são checkpoints superados. Mana/config/Survival ⚠️. [Dossiê](../EXACT-BINARY-GLYPHS-RITUALS-0.7.10.1.md).


Estado: **✅ `COUNTED_SOURCE_PINNED` — Efeito individualizado** · **⚠️ runtime, ID do registry e Survival pendentes**.

## Identidade e defaults source-pinned

- Nome na matriz editorial: **Conjure Terrain**; categoria **Efeito**.
- Provider: `ars_elemental`; JAR físico `ars_elemental-1.21.1-0.7.10.1.jar`, SHA-1 `a1e4021177aae0e16c1f7c6487a82f0b68bbade3`.
- Source pin `Alexthw46/Ars-Elemental@fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d` e Ars Nouveau API base `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`. **A equivalência byte-a-byte entre o source pin e o JAR físico não está provada.**
- Classificação: `COUNTED_SOURCE_PINNED`, **já incluído na contribuição de 47 objetos** (39 partes de spell e oito rituais); **+0 novas identidades** com esta ficha.
- Config efetiva, receitas implantadas, custos modificados e resultados de gameplay em Survival: **⚠️ NÃO VERIFICADOS**. `MethodCarianPhalanx` está excluído (dev-only); `Nullify Defense` tem receita de aprendizado desativada por source default `frame_skip_recipe=false`.

- **Tier:** I.
- **Mana source-default:** 20.
- **Schools:** Conjuration, Earth.
- **Compatible augments:** AoE, Pierce, Amplify, Randomize.
- **Provider-specific defaults/limits:** Amplify limit 2; Randomize limit 1.
- **ResourceLocation individual:** **NÃO VERIFICADO na matriz preservada**. Não inferir `ars_elemental:glyph_...` do nome de display.

## Semântica e limites

**Observação individual na auditoria:** Conjure Terrain composes provider-side with Conjure Water, Crush and Smelt and uses provider block placement logic; this does not bypass Black Arcana `WorldEffectPolicy` for Black Arcana-owned effects.

O Tier, a mana e os parâmetros acima são defaults do source, não medidas do cliente/servidor do pack.

**Authority:** Ars Nouveau/Ars Elemental retêm mana, Source, custos, spell grammar, execução, targeting, world effects e cleanup. Black Arcana não pode cobrar ou resolver novamente o mesmo cast, inserir segundo loop ou mutação. **⛔** Sem contrato real de hook/API, integração fail-closed.

**Fontes:** [matriz](../GLYPHS.md) · [acquisition](../ACQUISITION.md) · [registries](../REGISTRIES.md) · [provider](../README.md). Clean-room: somente fatos registrados na auditoria do Black Arcana, sem código/assets upstream.

## Engenharia de perks — execução individual 0.7.10.1

- **Classe:** [`EffectConjureTerrain.java`](https://github.com/Alexthw46/Ars-Elemental/blob/fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d/src/main/java/alexthw/ars_elemental/common/glyphs/EffectConjureTerrain.java), commit exato `fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d`, identidade estática do JAR físico já provada separadamente.
- **Escolha de bloco por count:** a classe usa **`spellStats.getBuffCount(AugmentAmplify.INSTANCE)`**, não apenas `getAmpMultiplier()`: zero seleciona DIRT (ou tag terrain com Randomize), um COBBLESTONE (ou tag cobble com Randomize), dois COBBLED_DEEPSLATE. `Randomize` e Amplify default limit 1/2.
- **Interação com próximos glyphs:** quando `spellContext.hasNextPart()`, consome partes até o próximo `AbstractEffect`; se Conjure Water com amp0 troca por MUD; se Crush troca por SAND/tag sand (amp0) ou SANDSTONE/RED_SANDSTONE (amp>0); se Smelt com amp1 vira STONE/tag, com >1 DEEPSLATE. Se não reconhecido regride `currentIndex` uma posição. A busca mexe no cursor do `SpellContext`, mas não cria novo cast.
- **World effects:** delega a criação a `GlyphEffectUtil.placeBlocks(...toPlace.defaultBlockState())`; autorização de claims/placement exige auditoria desse helper e teste instalado. **Perks:** modificar `ampMultiplier` em `EffectResolveEvent.Pre` não equivale a modificar `getBuffCount(Amplify)`; evitar interfaces genéricas incorretas e double placement.
- **Estado:** ✅ fonte/métodos source-located, ID confirmada no JAR; ⚠️ código-fonte→bytes JAR não equivalentes comprovados, config/QA de host não validados; ⛔ hook e adapter de perks RPG/Black Arcana não aprovados, sem duplicar mana ou efeitos.
