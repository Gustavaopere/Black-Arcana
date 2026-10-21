# Ars Elemental 0.7.10.1 — Create Geyser

**✅ Revalidação binária exata (2026-10-13):** `ars_elemental:glyph_geyser` é ID de registro estático provado no JAR 0.7.10.1 (SHA-1 `a1e4021177aae0e16c1f7c6487a82f0b68bbade3`) por [Java 21 #38403443682](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38403443682). `COUNTED_EXACT` para identidade; já contado, **+0**. Afirmações antigas de ID não verificado / `COUNTED_SOURCE_PINNED` abaixo são checkpoints superados. Mana/config/Survival ⚠️. [Dossiê](../EXACT-BINARY-GLYPHS-RITUALS-0.7.10.1.md).


Estado: **✅ `COUNTED_SOURCE_PINNED` — Efeito individualizado** · **⚠️ runtime, ID do registry e Survival pendentes**.

## Identidade e defaults source-pinned

- Nome na matriz editorial: **Create Geyser**; categoria **Efeito**.
- Provider: `ars_elemental`; JAR físico `ars_elemental-1.21.1-0.7.10.1.jar`, SHA-1 `a1e4021177aae0e16c1f7c6487a82f0b68bbade3`.
- Source pin `Alexthw46/Ars-Elemental@fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d` e Ars Nouveau API base `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`. **A equivalência byte-a-byte entre o source pin e o JAR físico não está provada.**
- Classificação: `COUNTED_SOURCE_PINNED`, **já incluído na contribuição de 47 objetos** (39 partes de spell e oito rituais); **+0 novas identidades** com esta ficha.
- Config efetiva, receitas implantadas, custos modificados e resultados de gameplay em Survival: **⚠️ NÃO VERIFICADOS**. `MethodCarianPhalanx` está excluído (dev-only); `Nullify Defense` tem receita de aprendizado desativada por source default `frame_skip_recipe=false`.

- **Tier:** II.
- **Mana source-default:** 40.
- **Schools:** Water, Fire.
- **Compatible augments:** Sensitive, AoE, Amplify, Dampen, Extend Time, Duration Down.
- **Provider-specific defaults/limits:** potion/lifetime 5s; extend 1; base height 4 + 2× amplification.
- **ResourceLocation individual:** **NÃO VERIFICADO na matriz preservada**. Não inferir `ars_elemental:glyph_...` do nome de display.

## Semântica e limites

A matriz não preserva uma observação comportamental adicional para esta entrada; não se deduz comportamento não evidenciado pelo nome.

O Tier, a mana e os parâmetros acima são defaults do source, não medidas do cliente/servidor do pack.

**Authority:** Ars Nouveau/Ars Elemental retêm mana, Source, custos, spell grammar, execução, targeting, world effects e cleanup. Black Arcana não pode cobrar ou resolver novamente o mesmo cast, inserir segundo loop ou mutação. **⛔** Sem contrato real de hook/API, integração fail-closed.

**Fontes:** [matriz](../GLYPHS.md) · [acquisition](../ACQUISITION.md) · [registries](../REGISTRIES.md) · [provider](../README.md). Clean-room: somente fatos registrados na auditoria do Black Arcana, sem código/assets upstream.

## Engenharia de perks — execução individual 0.7.10.1

- **Classe exata:** [`EffectGeyser.java`](https://github.com/Alexthw46/Ars-Elemental/blob/fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d/src/main/java/alexthw/ars_elemental/common/glyphs/EffectGeyser.java) fonte pinned 0.7.10.1, sem prova de byte-equality ao JAR.
- **Dimensão/altura:** `onResolve` aborta client; `height=(float)max(0,4+2*ampMultiplier)`; `aoe=(float)getAoeMultiplier()`. Direção padrão UP; Sensitive preserva face do hit em bloco, permitindo lateral. Procura base não-air recuando pelo vetor oposto à direção até cerca de `height*2` tentativas.
- **Duração/tipo:** `duration=POTION_TIME.get()*20+(int)(EXTEND_TIME.get()*durationMultiplier*20)`, defaults 5 segundos e +1 segundo, sem clamp local. Cria `EntityLavaGeyser` se `fireCheck(resolverContext)` verdadeiro, senão `EntityGeyser`; lifecycle de damage/Soaked/Fire está nessa entidade, não no glyph.
- **Perks:** mudança de altura/raio afeta entidade world-owned; Sensitive não é imunidade. Não inferir alcance de fogo/fluido de um único campo do glyph.
- **Estado:** ✅ ID JAR + código exato no source commit; ⚠️ gameplay/config/host/auxiliares requerem confirmação; ⛔ adapter de perk RPG não implementado, sem duplicar status, mana ou dano.
