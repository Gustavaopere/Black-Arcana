# Ars Elemental 0.7.10.1 — Phantom Grasp

**✅ Revalidação binária exata (2026-10-13):** `ars_elemental:glyph_phantom_grasp` é ID de registro estático provado no JAR 0.7.10.1 (SHA-1 `a1e4021177aae0e16c1f7c6487a82f0b68bbade3`) por [Java 21 #38403443682](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38403443682). `COUNTED_EXACT` para identidade; já contado, **+0**. Afirmações antigas de ID não verificado / `COUNTED_SOURCE_PINNED` abaixo são checkpoints superados. Mana/config/Survival ⚠️. [Dossiê](../EXACT-BINARY-GLYPHS-RITUALS-0.7.10.1.md).


Estado: **✅ `COUNTED_SOURCE_PINNED` — Efeito individualizado** · **⚠️ runtime, ID do registry e Survival pendentes**.

## Identidade e defaults source-pinned

- Nome na matriz editorial: **Phantom Grasp**; categoria **Efeito**.
- Provider: `ars_elemental`; JAR físico `ars_elemental-1.21.1-0.7.10.1.jar`, SHA-1 `a1e4021177aae0e16c1f7c6487a82f0b68bbade3`.
- Source pin `Alexthw46/Ars-Elemental@fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d` e Ars Nouveau API base `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`. **A equivalência byte-a-byte entre o source pin e o JAR físico não está provada.**
- Classificação: `COUNTED_SOURCE_PINNED`, **já incluído na contribuição de 47 objetos** (39 partes de spell e oito rituais); **+0 novas identidades** com esta ficha.
- Config efetiva, receitas implantadas, custos modificados e resultados de gameplay em Survival: **⚠️ NÃO VERIFICADOS**. `MethodCarianPhalanx` está excluído (dev-only); `Nullify Defense` tem receita de aprendizado desativada por source default `frame_skip_recipe=false`.

- **Tier:** II.
- **Mana source-default:** 50.
- **Schools:** Necromancy.
- **Compatible augments:** Amplify, Dampen, Fortune, Randomize.
- **Provider-specific defaults/limits:** base_heal 3; amplify 3; Amplify limit 3.
- **ResourceLocation individual:** **NÃO VERIFICADO na matriz preservada**. Não inferir `ars_elemental:glyph_...` do nome de display.

## Semântica e limites

**Observação individual na auditoria:** Phantom Grasp heals inverted-heal targets and uses equivalent magic damage against living targets; successful player damage also adds food exhaustion.

O Tier, a mana e os parâmetros acima são defaults do source, não medidas do cliente/servidor do pack.

**Authority:** Ars Nouveau/Ars Elemental retêm mana, Source, custos, spell grammar, execução, targeting, world effects e cleanup. Black Arcana não pode cobrar ou resolver novamente o mesmo cast, inserir segundo loop ou mutação. **⛔** Sem contrato real de hook/API, integração fail-closed.

**Fontes:** [matriz](../GLYPHS.md) · [acquisition](../ACQUISITION.md) · [registries](../REGISTRIES.md) · [provider](../README.md). Clean-room: somente fatos registrados na auditoria do Black Arcana, sem código/assets upstream.

## Engenharia de perks — execução individual 0.7.10.1

- **Source commit:** [`EffectPhantom.java`](https://github.com/Alexthw46/Ars-Elemental/blob/fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d/src/main/java/alexthw/ars_elemental/common/glyphs/EffectPhantom.java) na versão de código fixada, não prova binária dos métodos no JAR.
- **Branch invertido:** ignora alvo removido/morto. `healVal=GENERIC_DOUBLE.get()+AMP_VALUE.get()*ampMultiplier` defaults 3+3*amp; se `isInvertedHealAndHarm()`, cura a entidade e, quando Randomize, soma `randomRolls(stats,server)` ao valor.
- **Branch normal:** se não inverted, tenta `IDamageEffect.attemptDamage` com `DamageTypes.MAGIC`; se hit aceito e target é Player, chama `causeFoodExhaustion(2.5*(1.5+ampMultiplier))`. Amplify default limit 3.
- **Perks:** heal do undead, dano MAGIC e exaustão do player não podem receber o mesmo modificador universal nem provar proc de hit por mera resolução.
- **Status:** ✅ objeto com ID de JAR física comprovada e source observado; ⚠️ runtime, API host, config deploy e controle de claims ainda condicionados; ⛔ nenhum adapter RPG implementado, sem duplicação de settle/hit/Source/mana.
