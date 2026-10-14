# Ars Elemental 0.7.10.1 — Water Jet

**✅ Revalidação binária exata (2026-10-13):** `ars_elemental:glyph_water_jet` é ID de registro estático provado no JAR 0.7.10.1 (SHA-1 `a1e4021177aae0e16c1f7c6487a82f0b68bbade3`) por [Java 21 #38403443682](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38403443682). `COUNTED_EXACT` para identidade; já contado, **+0**. Afirmações antigas de ID não verificado / `COUNTED_SOURCE_PINNED` abaixo são checkpoints superados. Mana/config/Survival ⚠️. [Dossiê](../EXACT-BINARY-GLYPHS-RITUALS-0.7.10.1.md).


Estado: **✅ `COUNTED_SOURCE_PINNED` — Efeito individualizado** · **⚠️ runtime, ID do registry e Survival pendentes**.

## Identidade e defaults source-pinned

- Nome na matriz editorial: **Water Jet**; categoria **Efeito**.
- Provider: `ars_elemental`; JAR físico `ars_elemental-1.21.1-0.7.10.1.jar`, SHA-1 `a1e4021177aae0e16c1f7c6487a82f0b68bbade3`.
- Source pin `Alexthw46/Ars-Elemental@fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d` e Ars Nouveau API base `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`. **A equivalência byte-a-byte entre o source pin e o JAR físico não está provada.**
- Classificação: `COUNTED_SOURCE_PINNED`, **já incluído na contribuição de 47 objetos** (39 partes de spell e oito rituais); **+0 novas identidades** com esta ficha.
- Config efetiva, receitas implantadas, custos modificados e resultados de gameplay em Survival: **⚠️ NÃO VERIFICADOS**. `MethodCarianPhalanx` está excluído (dev-only); `Nullify Defense` tem receita de aprendizado desativada por source default `frame_skip_recipe=false`.

- **Tier:** III.
- **Mana source-default:** 80.
- **Schools:** Water.
- **Compatible augments:** Split, Randomize, Amplify.
- **Provider-specific defaults/limits:** damage 4; amplify 1; Split cost override 40; target search radius 10.
- **ResourceLocation individual:** **NÃO VERIFICADO na matriz preservada**. Não inferir `ars_elemental:glyph_...` do nome de display.

## Semântica e limites

A matriz não preserva uma observação comportamental adicional para esta entrada; não se deduz comportamento não evidenciado pelo nome.

O Tier, a mana e os parâmetros acima são defaults do source, não medidas do cliente/servidor do pack.

**Authority:** Ars Nouveau/Ars Elemental retêm mana, Source, custos, spell grammar, execução, targeting, world effects e cleanup. Black Arcana não pode cobrar ou resolver novamente o mesmo cast, inserir segundo loop ou mutação. **⛔** Sem contrato real de hook/API, integração fail-closed.

**Fontes:** [matriz](../GLYPHS.md) · [acquisition](../ACQUISITION.md) · [registries](../REGISTRIES.md) · [provider](../README.md). Clean-room: somente fatos registrados na auditoria do Black Arcana, sem código/assets upstream.

## Engenharia de perks — execução individual 0.7.10.1

- **Classe fonte:** [`EffectWaterJet.java`](https://github.com/Alexthw46/Ars-Elemental/blob/fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d/src/main/java/alexthw/ars_elemental/common/glyphs/EffectWaterJet.java) pin fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d, não igualdade criptográfica source/JAR.
- **Escolha de alvo:** `numJets=1+getBuffCount(Split)`, impacto no olho do EntityHit ou hitPosition; varre `LivingEntity` viva diferente de shooter em AABB `inflate(10)` e ordena por `distanceToSqr(impactPos)`. Se vazio, apenas partículas splash e retorna, sem marker.
- **Randomize e lançamento:** para cada jet calcula posição inicial circular raio 1.5, angle `2π*i/numJets`; sem Randomize escolhe sempre alvo mais próximo, com Randomize cicla por `potentialTargets[i % size]`. Cria **um** `EntityWaterJet` marker com todas origens, targetIds e dano `DAMAGE+AMP_VALUE*ampMultiplier` (defaults 4+1*amp). Dano posterior e atraso são do EntityWaterJet.
- **Custo:** `getDefaultManaCost=80`; custo override da Augment Split **40**. **Perks:** marker, quantidade de jets e impactos posteriores não são múltiplos casts nem garantem que cada target permaneça válido.
- **Estado:** ✅ símbolo/assinatura reais e ID registral física; ⚠️ config, helper, entidade e Survival runtime pendentes; ⛔ perks RPG/adapters não implementados nem comprovados, settlement/cast pertence ao Ars.
