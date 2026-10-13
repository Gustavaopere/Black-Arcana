# Ars Elemental 0.7.10.1 — Poison Spores

**✅ Revalidação binária exata (2026-10-13):** `ars_elemental:glyph_poison_spores` é ID de registro estático provado no JAR 0.7.10.1 (SHA-1 `a1e4021177aae0e16c1f7c6487a82f0b68bbade3`) por [Java 21 #38403443682](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38403443682). `COUNTED_EXACT` para identidade; já contado, **+0**. Afirmações antigas de ID não verificado / `COUNTED_SOURCE_PINNED` abaixo são checkpoints superados. Mana/config/Survival ⚠️. [Dossiê](../EXACT-BINARY-GLYPHS-RITUALS-0.7.10.1.md).


Estado: **✅ `COUNTED_SOURCE_PINNED` — Efeito individualizado** · **⚠️ runtime, ID do registry e Survival pendentes**.

## Identidade e defaults source-pinned

- Nome na matriz editorial: **Poison Spores**; categoria **Efeito**.
- Provider: `ars_elemental`; JAR físico `ars_elemental-1.21.1-0.7.10.1.jar`, SHA-1 `a1e4021177aae0e16c1f7c6487a82f0b68bbade3`.
- Source pin `Alexthw46/Ars-Elemental@fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d` e Ars Nouveau API base `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`. **A equivalência byte-a-byte entre o source pin e o JAR físico não está provada.**
- Classificação: `COUNTED_SOURCE_PINNED`, **já incluído na contribuição de 47 objetos** (39 partes de spell e oito rituais); **+0 novas identidades** com esta ficha.
- Config efetiva, receitas implantadas, custos modificados e resultados de gameplay em Survival: **⚠️ NÃO VERIFICADOS**. `MethodCarianPhalanx` está excluído (dev-only); `Nullify Defense` tem receita de aprendizado desativada por source default `frame_skip_recipe=false`.

- **Tier:** II.
- **Mana source-default:** 30.
- **Schools:** Earth.
- **Compatible augments:** Amplify, Dampen, Extend Time, Duration Down, AoE, Fortune, Randomize.
- **Provider-specific defaults/limits:** damage 6; amplify 2.5; potion 10s; extend 3; Amplify limit 2.
- **ResourceLocation individual:** **NÃO VERIFICADO na matriz preservada**. Não inferir `ars_elemental:glyph_...` do nome de display.

## Semântica e limites

A matriz não preserva uma observação comportamental adicional para esta entrada; não se deduz comportamento não evidenciado pelo nome.

O Tier, a mana e os parâmetros acima são defaults do source, não medidas do cliente/servidor do pack.

**Authority:** Ars Nouveau/Ars Elemental retêm mana, Source, custos, spell grammar, execução, targeting, world effects e cleanup. Black Arcana não pode cobrar ou resolver novamente o mesmo cast, inserir segundo loop ou mutação. **⛔** Sem contrato real de hook/API, integração fail-closed.

**Fontes:** [matriz](../GLYPHS.md) · [acquisition](../ACQUISITION.md) · [registries](../REGISTRIES.md) · [provider](../README.md). Clean-room: somente fatos registrados na auditoria do Black Arcana, sem código/assets upstream.

## Engenharia de perks — execução individual 0.7.10.1

- **Source commit:** [`EffectSpores.java`](https://github.com/Alexthw46/Ars-Elemental/blob/fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d/src/main/java/alexthw/ars_elemental/common/glyphs/EffectSpores.java) na versão de código fixada, não prova binária dos métodos no JAR.
- **Gatilho:** target primário só entra no dano quando vivo e possui POISON, HUNGER ou VENOM; default dano `6+2.5*ampMultiplier`, com bônus `2+3*venomAmplifier` se VENOM no alvo inicial. Varre LivingEntity em AABB `inflate(3+aoeMultiplier)` e separa secundários elegíveis para dano dos não elegíveis, que recebem POISON e HUNGER por `20*effectSec`.
- **Dano/efeitos:** `damage(...)` multiplica 1.25 se EntityTypeTags.UNDEAD, tenta dano e gera partículas. Se morte, 5% de chance por `random.nextInt(100)<5` mais `CompatUtils.earthCheck(resolver)` e solo moss/dirt/leaves com espaço livre podem gerar `GROUND_BLOSSOM`; senão aplica HUNGER. Este último branch não exige sucesso explícito de `attemptDamage`.
- **Config default:** potion 10s, Extend Time +3s, Amplify scalar +2.5, amp limit 2. Getters sem config retornam 30/8, portanto separar fallback. **Perks:** mundo, dano, DOT e cultivo dependem de gates diferentes; não multiplicar drops ou status por segunda liquidação.
- **Status:** ✅ objeto com ID de JAR física comprovada e source observado; ⚠️ runtime, API host, config deploy e controle de claims ainda condicionados; ⛔ nenhum adapter RPG implementado, sem duplicação de settle/hit/Source/mana.
