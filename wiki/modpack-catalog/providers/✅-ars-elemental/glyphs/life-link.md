# Ars Elemental 0.7.10.1 — Life Link

**✅ Revalidação binária exata (2026-10-13):** `ars_elemental:glyph_life_link` é ID de registro estático provado no JAR 0.7.10.1 (SHA-1 `a1e4021177aae0e16c1f7c6487a82f0b68bbade3`) por [Java 21 #38403443682](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38403443682). `COUNTED_EXACT` para identidade; já contado, **+0**. Afirmações antigas de ID não verificado / `COUNTED_SOURCE_PINNED` abaixo são checkpoints superados. Mana/config/Survival ⚠️. [Dossiê](../EXACT-BINARY-GLYPHS-RITUALS-0.7.10.1.md).


Estado: **✅ `COUNTED_SOURCE_PINNED` — Efeito individualizado** · **⚠️ runtime, ID do registry e Survival pendentes**.

## Identidade e defaults source-pinned

- Nome na matriz editorial: **Life Link**; categoria **Efeito**.
- Provider: `ars_elemental`; JAR físico `ars_elemental-1.21.1-0.7.10.1.jar`, SHA-1 `a1e4021177aae0e16c1f7c6487a82f0b68bbade3`.
- Source pin `Alexthw46/Ars-Elemental@fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d` e Ars Nouveau API base `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`. **A equivalência byte-a-byte entre o source pin e o JAR físico não está provada.**
- Classificação: `COUNTED_SOURCE_PINNED`, **já incluído na contribuição de 47 objetos** (39 partes de spell e oito rituais); **+0 novas identidades** com esta ficha.
- Config efetiva, receitas implantadas, custos modificados e resultados de gameplay em Survival: **⚠️ NÃO VERIFICADOS**. `MethodCarianPhalanx` está excluído (dev-only); `Nullify Defense` tem receita de aprendizado desativada por source default `frame_skip_recipe=false`.

- **Tier:** III.
- **Mana source-default:** 30.
- **Schools:** provider registry plus Necromancy added in post-init.
- **Compatible augments:** Extend Time, Duration Down, Sensitive.
- **Provider-specific defaults/limits:** potion 30s; extend 8.
- **ResourceLocation individual:** **NÃO VERIFICADO na matriz preservada**. Não inferir `ars_elemental:glyph_...` do nome de display.

## Semântica e limites

**Observação individual na auditoria:** Life Link remains an Ars/provider life-link effect and is not a Black Arcana Vincular contract.

O Tier, a mana e os parâmetros acima são defaults do source, não medidas do cliente/servidor do pack.

**Authority:** Ars Nouveau/Ars Elemental retêm mana, Source, custos, spell grammar, execução, targeting, world effects e cleanup. Black Arcana não pode cobrar ou resolver novamente o mesmo cast, inserir segundo loop ou mutação. **⛔** Sem contrato real de hook/API, integração fail-closed.

**Fontes:** [matriz](../GLYPHS.md) · [acquisition](../ACQUISITION.md) · [registries](../REGISTRIES.md) · [provider](../README.md). Clean-room: somente fatos registrados na auditoria do Black Arcana, sem código/assets upstream.

## Engenharia de perks — execução individual 0.7.10.1

- **Classe:** [`EffectLifeLink.java`](https://github.com/Alexthw46/Ars-Elemental/blob/fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d/src/main/java/alexthw/ars_elemental/common/glyphs/EffectLifeLink.java), commit exato `fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d`, identidade estática do JAR físico já provada separadamente.
- **Alvo e inversão:** `onResolveEntity` só age com `LivingEntity` que não é o caster. Sem Sensitive, `entity=target`/`owner=shooter`; com Sensitive inverte ambos. A mesma `EntityCarryMEI(LIFE_LINK,...,owner,entity)` é aplicada nas duas entidades para partilha futura, portanto não são dois casts.
- **Duração:** `ticks=getBaseDuration()*20+getExtendTimeDuration()*stats.getDurationInTicks()`, defaults configurados 30s+8s de extensão por helper. Com Necromancy Focus detectado por `resolver.hasFocus(ModItems.NECRO_FOCUS.get())` usa `forceAddEffect` em ambos, senão `addEffect`. O comportamento efetivo de compartilhamento de dano/cura fica no `LIFE_LINK` effect/handlers e precisa de auditoria separada.
- **Perks:** gates devem preservar as duas UUIDs, consentimento/validade do alvo, source attribution e prevenção de ciclos. Não reinterpretar este glyph como implementação da Vincular do Black Arcana nem duplicar dano.
- **Estado:** ✅ fonte/métodos source-located, ID confirmada no JAR; ⚠️ código-fonte→bytes JAR não equivalentes comprovados, config/QA de host não validados; ⛔ hook e adapter de perks RPG/Black Arcana não aprovados, sem duplicar mana ou efeitos.
