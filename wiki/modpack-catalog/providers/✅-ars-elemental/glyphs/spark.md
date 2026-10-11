# Ars Elemental 0.7.10.1 — Spark

Estado: **✅ `COUNTED_SOURCE_PINNED` — Efeito individualizado** · **⚠️ runtime, ID do registry e Survival pendentes**.

## Identidade e defaults source-pinned

- Nome na matriz editorial: **Spark**; categoria **Efeito**.
- Provider: `ars_elemental`; JAR físico `ars_elemental-1.21.1-0.7.10.1.jar`, SHA-1 `a1e4021177aae0e16c1f7c6487a82f0b68bbade3`.
- Source pin `Alexthw46/Ars-Elemental@fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d` e Ars Nouveau API base `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`. **A equivalência byte-a-byte entre o source pin e o JAR físico não está provada.**
- Classificação: `COUNTED_SOURCE_PINNED`, **já incluído na contribuição de 47 objetos** (39 partes de spell e oito rituais); **+0 novas identidades** com esta ficha.
- Config efetiva, receitas implantadas, custos modificados e resultados de gameplay em Survival: **⚠️ NÃO VERIFICADOS**. `MethodCarianPhalanx` está excluído (dev-only); `Nullify Defense` tem receita de aprendizado desativada por source default `frame_skip_recipe=false`.

- **Tier:** I.
- **Mana source-default:** 15.
- **Schools:** Air.
- **Compatible augments:** Extend Time, Duration Down, Amplify, Dampen, Randomize.
- **Provider-specific defaults/limits:** damage 3; amplify 1.5; potion 15s; extend 5; Amplify limit 2.
- **ResourceLocation individual:** **NÃO VERIFICADO na matriz preservada**. Não inferir `ars_elemental:glyph_...` do nome de display.

## Semântica e limites

**Observação individual na auditoria:** Spark deals +2 source damage against a wet target and uses Lightning Lure instead of Shocked when the provider Air-focus check passes.

O Tier, a mana e os parâmetros acima são defaults do source, não medidas do cliente/servidor do pack.

**Authority:** Ars Nouveau/Ars Elemental retêm mana, Source, custos, spell grammar, execução, targeting, world effects e cleanup. Black Arcana não pode cobrar ou resolver novamente o mesmo cast, inserir segundo loop ou mutação. **⛔** Sem contrato real de hook/API, integração fail-closed.

**Fontes:** [matriz](../GLYPHS.md) · [acquisition](../ACQUISITION.md) · [registries](../REGISTRIES.md) · [provider](../README.md). Clean-room: somente fatos registrados na auditoria do Black Arcana, sem código/assets upstream.
