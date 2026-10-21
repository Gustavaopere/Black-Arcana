# Ars Elemental 0.7.10.1 — Summon Bee

**✅ Revalidação binária exata (2026-10-13):** `ars_elemental:glyph_summon_bee` é ID de registro estático provado no JAR 0.7.10.1 (SHA-1 `a1e4021177aae0e16c1f7c6487a82f0b68bbade3`) por [Java 21 #38403443682](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38403443682). `COUNTED_EXACT` para identidade; já contado, **+0**. Afirmações antigas de ID não verificado / `COUNTED_SOURCE_PINNED` abaixo são checkpoints superados. Mana/config/Survival ⚠️. [Dossiê](../EXACT-BINARY-GLYPHS-RITUALS-0.7.10.1.md).


Estado: **✅ `COUNTED_SOURCE_PINNED` — Efeito individualizado** · **⚠️ runtime, ID do registry e Survival pendentes**.

## Identidade e defaults source-pinned

- Nome na matriz editorial: **Summon Bee**; categoria **Efeito**.
- Provider: `ars_elemental`; JAR físico `ars_elemental-1.21.1-0.7.10.1.jar`, SHA-1 `a1e4021177aae0e16c1f7c6487a82f0b68bbade3`.
- Source pin `Alexthw46/Ars-Elemental@fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d` e Ars Nouveau API base `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`. **A equivalência byte-a-byte entre o source pin e o JAR físico não está provada.**
- Classificação: `COUNTED_SOURCE_PINNED`, **já incluído na contribuição de 47 objetos** (39 partes de spell e oito rituais); **+0 novas identidades** com esta ficha.
- Config efetiva, receitas implantadas, custos modificados e resultados de gameplay em Survival: **⚠️ NÃO VERIFICADOS**. `MethodCarianPhalanx` está excluído (dev-only); `Nullify Defense` tem receita de aprendizado desativada por source default `frame_skip_recipe=false`.

- **Tier:** II.
- **Mana source-default:** 100.
- **Schools:** Conjuration, Earth.
- **Compatible augments:** Extend Time, Duration Down, Split.
- **Provider-specific defaults/limits:** summons 3 + Split; lifetime 60 + 60×durationMultiplier seconds; Summoning Sickness 80% of summon lifetime when Summon Rework is inactive.
- **ResourceLocation individual:** **NÃO VERIFICADO na matriz preservada**. Não inferir `ars_elemental:glyph_...` do nome de display.

## Semântica e limites

A matriz não preserva uma observação comportamental adicional para esta entrada; não se deduz comportamento não evidenciado pelo nome.

O Tier, a mana e os parâmetros acima são defaults do source, não medidas do cliente/servidor do pack.

**Authority:** Ars Nouveau/Ars Elemental retêm mana, Source, custos, spell grammar, execução, targeting, world effects e cleanup. Black Arcana não pode cobrar ou resolver novamente o mesmo cast, inserir segundo loop ou mutação. **⛔** Sem contrato real de hook/API, integração fail-closed.

**Fontes:** [matriz](../GLYPHS.md) · [acquisition](../ACQUISITION.md) · [registries](../REGISTRIES.md) · [provider](../README.md). Clean-room: somente fatos registrados na auditoria do Black Arcana, sem código/assets upstream.

## Engenharia de perks — execução individual 0.7.10.1

- **Classe fonte:** [`EffectSummonBee.java`](https://github.com/Alexthw46/Ars-Elemental/blob/fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d/src/main/java/alexthw/ars_elemental/common/glyphs/EffectSummonBee.java) pin fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d, não igualdade criptográfica source/JAR.
- **Gates:** exige `canSummon(shooter)`; `ticks=(int)(20*(60+60*durationMultiplier))`; quantidade `3+getBuffCount(Split)`; cada `SummonBee` recebe owner, target `shooter.getLastHurtMob()`, aggressive=true e passa por `summonLivingEntity`.
- **Sickness:** quando `!CompatUtils.isSummonRework()`, chama `applySummoningSickness(shooter,(int)(ticks*0.80))`; se Summon Rework estiver ativo, este helper não é chamado neste glyph. **Perks:** count de bees não é count de casts; source não demonstra budget adicional externo, validar entidade e tame/owner.
- **Estado:** ✅ símbolo/assinatura reais e ID registral física; ⚠️ config, helper, entidade e Survival runtime pendentes; ⛔ perks RPG/adapters não implementados nem comprovados, settlement/cast pertence ao Ars.
