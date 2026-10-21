# Ars Elemental 0.7.10.1 — Nullify Defense

**✅ Revalidação binária exata (2026-10-13):** `ars_elemental:glyph_nullify_defense` é ID de registro estático provado no JAR 0.7.10.1 (SHA-1 `a1e4021177aae0e16c1f7c6487a82f0b68bbade3`) por [Java 21 #38403443682](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38403443682). `COUNTED_EXACT` para identidade; já contado, **+0**. Afirmações antigas de ID não verificado / `COUNTED_SOURCE_PINNED` abaixo são checkpoints superados. Mana/config/Survival ⚠️. [Dossiê](../EXACT-BINARY-GLYPHS-RITUALS-0.7.10.1.md).


Estado: **✅ `COUNTED_SOURCE_PINNED` — Efeito individualizado** · **⚠️ runtime, ID do registry e Survival pendentes**.

## Identidade e defaults source-pinned

- Nome na matriz editorial: **Nullify Defense**; categoria **Efeito**.
- Provider: `ars_elemental`; JAR físico `ars_elemental-1.21.1-0.7.10.1.jar`, SHA-1 `a1e4021177aae0e16c1f7c6487a82f0b68bbade3`.
- Source pin `Alexthw46/Ars-Elemental@fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d` e Ars Nouveau API base `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`. **A equivalência byte-a-byte entre o source pin e o JAR físico não está provada.**
- Classificação: `COUNTED_SOURCE_PINNED`, **já incluído na contribuição de 47 objetos** (39 partes de spell e oito rituais); **+0 novas identidades** com esta ficha.
- Config efetiva, receitas implantadas, custos modificados e resultados de gameplay em Survival: **⚠️ NÃO VERIFICADOS**. `MethodCarianPhalanx` está excluído (dev-only); `Nullify Defense` tem receita de aprendizado desativada por source default `frame_skip_recipe=false`.

- **Tier:** III.
- **Mana source-default:** 1000.
- **Schools:** Necromancy.
- **Compatible augments:** none.
- **Provider-specific defaults/limits:** executable path sets target `invulnerableTime = 0`; learning recipe is separately config-gated and disabled by source default.
- **ResourceLocation individual:** **NÃO VERIFICADO na matriz preservada**. Não inferir `ars_elemental:glyph_...` do nome de display.

## Semântica e limites

**Observação individual na auditoria:** Nullify Defense does not remove armor, resistance or an immunity registry entry in this source path; it resets the vanilla LivingEntity post-hit invulnerability timer.

O Tier, a mana e os parâmetros acima são defaults do source, não medidas do cliente/servidor do pack.

**Authority:** Ars Nouveau/Ars Elemental retêm mana, Source, custos, spell grammar, execução, targeting, world effects e cleanup. Black Arcana não pode cobrar ou resolver novamente o mesmo cast, inserir segundo loop ou mutação. **⛔** Sem contrato real de hook/API, integração fail-closed.

**Fontes:** [matriz](../GLYPHS.md) · [acquisition](../ACQUISITION.md) · [registries](../REGISTRIES.md) · [provider](../README.md). Clean-room: somente fatos registrados na auditoria do Black Arcana, sem código/assets upstream.

## Engenharia de perks — execução individual 0.7.10.1

- **Classe:** [`EffectNullify.java`](https://github.com/Alexthw46/Ars-Elemental/blob/fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d/src/main/java/alexthw/ars_elemental/common/glyphs/EffectNullify.java), commit exato `fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d`, identidade estática do JAR físico já provada separadamente.
- **Única mutação do método:** se a entidade atingida é `LivingEntity`, faz `entity.invulnerableTime=0` sem dano, remoção de armor, quebra de invulnerabilidade absoluta, ou redução de resistance neste trecho. Custo mana default 1000, Tier III e nenhum augment.
- **Aquisição:** o registry do effect está presente no JAR, mas a receita de aprendizagem permanece default-disabled conforme checkpoint de config (`frame_skip_recipe=false`). Contagem semântica não garante disponibilidade Survival.
- **Perks:** zerar invulnerability frames não autoriza interferir em proteção PvP, de outros mods ou flags `isInvulnerable`. A saída do effect não é confirmação de hit/dano posterior; manter `fail-closed` para haste/double hit.
- **Estado:** ✅ fonte/métodos source-located, ID confirmada no JAR; ⚠️ código-fonte→bytes JAR não equivalentes comprovados, config/QA de host não validados; ⛔ hook e adapter de perks RPG/Black Arcana não aprovados, sem duplicar mana ou efeitos.
