# Ars Elemental 0.7.10.1 — Cavitate

**✅ Revalidação binária exata (2026-10-13):** `ars_elemental:glyph_cavitate` é ID de registro estático provado no JAR 0.7.10.1 (SHA-1 `a1e4021177aae0e16c1f7c6487a82f0b68bbade3`) por [Java 21 #38403443682](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38403443682). `COUNTED_EXACT` para identidade; já contado, **+0**. Afirmações antigas de ID não verificado / `COUNTED_SOURCE_PINNED` abaixo são checkpoints superados. Mana/config/Survival ⚠️. [Dossiê](../EXACT-BINARY-GLYPHS-RITUALS-0.7.10.1.md).


Estado: **✅ `COUNTED_SOURCE_PINNED` — Efeito individualizado** · **⚠️ runtime, ID do registry e Survival pendentes**.

## Identidade e defaults source-pinned

- Nome na matriz editorial: **Cavitate**; categoria **Efeito**.
- Provider: `ars_elemental`; JAR físico `ars_elemental-1.21.1-0.7.10.1.jar`, SHA-1 `a1e4021177aae0e16c1f7c6487a82f0b68bbade3`.
- Source pin `Alexthw46/Ars-Elemental@fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d` e Ars Nouveau API base `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`. **A equivalência byte-a-byte entre o source pin e o JAR físico não está provada.**
- Classificação: `COUNTED_SOURCE_PINNED`, **já incluído na contribuição de 47 objetos** (39 partes de spell e oito rituais); **+0 novas identidades** com esta ficha.
- Config efetiva, receitas implantadas, custos modificados e resultados de gameplay em Survival: **⚠️ NÃO VERIFICADOS**. `MethodCarianPhalanx` está excluído (dev-only); `Nullify Defense` tem receita de aprendizado desativada por source default `frame_skip_recipe=false`.

- **Tier:** III.
- **Mana source-default:** 80.
- **Schools:** Water.
- **Compatible augments:** AoE, Amplify, Extend Time, Duration Down, Randomize, Dampen.
- **Provider-specific defaults/limits:** damage 8; amplify 3; `addDefaultPotionConfig` => potion 30s / extend 8; pre-config fallback getters are 15/5.
- **ResourceLocation individual:** **NÃO VERIFICADO na matriz preservada**. Não inferir `ars_elemental:glyph_...` do nome de display.

## Semântica e limites

A matriz não preserva uma observação comportamental adicional para esta entrada; não se deduz comportamento não evidenciado pelo nome.

O Tier, a mana e os parâmetros acima são defaults do source, não medidas do cliente/servidor do pack.

**Authority:** Ars Nouveau/Ars Elemental retêm mana, Source, custos, spell grammar, execução, targeting, world effects e cleanup. Black Arcana não pode cobrar ou resolver novamente o mesmo cast, inserir segundo loop ou mutação. **⛔** Sem contrato real de hook/API, integração fail-closed.

**Fontes:** [matriz](../GLYPHS.md) · [acquisition](../ACQUISITION.md) · [registries](../REGISTRIES.md) · [provider](../README.md). Clean-room: somente fatos registrados na auditoria do Black Arcana, sem código/assets upstream.

## Engenharia de perks — execução individual 0.7.10.1

- **Classe exata:** [`EffectCavitate.java`](https://github.com/Alexthw46/Ars-Elemental/blob/fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d/src/main/java/alexthw/ars_elemental/common/glyphs/EffectCavitate.java) fonte pinned 0.7.10.1, sem prova de byte-equality ao JAR.
- **Gatilho:** target deve ser `BubbleEntity` ou passageiro de uma `BubbleEntity`, no `ServerLevel`, **e** `attemptDamage` direto no target deve retornar true. Fora da bolha não há shockwave.
- **Escala e AOE:** dano nominal `DAMAGE+AMP_VALUE*ampMultiplier`, defaults 8+3*amp; busca outras `LivingEntity` em AABB `inflate(2+getAoeMultiplier())`, excluindo caster e o objeto target. Para cada uma tenta dano e aplica `SOAKED_EFFECT` mesmo quando o resultado de `attemptDamage` no alvo secundário foi false (a aplicação não está guardada pelo retorno).
- **Perks:** dano inicial, dano secundário, status e ondas visuais não são multiplicadores independentes; conferir entidade Bubble real e prevenção de procs recursivos, sem atribuir Mastery por ring particles.
- **Estado:** ✅ ID JAR + código exato no source commit; ⚠️ gameplay/config/host/auxiliares requerem confirmação; ⛔ adapter de perk RPG não implementado, sem duplicar status, mana ou dano.
