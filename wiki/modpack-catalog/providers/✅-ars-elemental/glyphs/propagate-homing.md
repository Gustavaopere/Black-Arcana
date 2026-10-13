# Ars Elemental 0.7.10.1 — Propagate Homing

**✅ Revalidação binária exata (2026-10-13):** `ars_elemental:glyph_propagator_homing` é ID de registro estático provado no JAR 0.7.10.1 (SHA-1 `a1e4021177aae0e16c1f7c6487a82f0b68bbade3`) por [Java 21 #38403443682](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38403443682). `COUNTED_EXACT` para identidade; já contado, **+0**. Afirmações antigas de ID não verificado / `COUNTED_SOURCE_PINNED` abaixo são checkpoints superados. Mana/config/Survival ⚠️. [Dossiê](../EXACT-BINARY-GLYPHS-RITUALS-0.7.10.1.md).


Estado: **✅ `COUNTED_SOURCE_PINNED` — Propagator individualizado** · **⚠️ runtime, ID do registry e Survival pendentes**.

## Identidade e defaults source-pinned

- Nome na matriz editorial: **Propagate Homing**; categoria **Propagator**.
- Provider: `ars_elemental`; JAR físico `ars_elemental-1.21.1-0.7.10.1.jar`, SHA-1 `a1e4021177aae0e16c1f7c6487a82f0b68bbade3`.
- Source pin `Alexthw46/Ars-Elemental@fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d` e Ars Nouveau API base `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`. **A equivalência byte-a-byte entre o source pin e o JAR físico não está provada.**
- Classificação: `COUNTED_SOURCE_PINNED`, **já incluído na contribuição de 47 objetos** (39 partes de spell e oito rituais); **+0 novas identidades** com esta ficha.
- Config efetiva, receitas implantadas, custos modificados e resultados de gameplay em Survival: **⚠️ NÃO VERIFICADOS**. `MethodCarianPhalanx` está excluído (dev-only); `Nullify Defense` tem receita de aprendizado desativada por source default `frame_skip_recipe=false`.

- **Tier:** III.
- **Mana source-default:** 400.
- **School:** Manipulation.
- **Compatible augments:** Homing Projectile set + Extract.
- **ResourceLocation individual:** **NÃO VERIFICADO na matriz preservada**. Não inferir `ars_elemental:glyph_...` do nome de display.

## Semântica e limites

A matriz não preserva uma observação comportamental adicional para esta entrada; não se deduz comportamento não evidenciado pelo nome.

O propagador reemite a cadeia provider-owned através de Ars context/resolver, e não inicia um segundo root cast Black Arcana.

**Authority:** Ars Nouveau/Ars Elemental retêm mana, Source, custos, spell grammar, execução, targeting, world effects e cleanup. Black Arcana não pode cobrar ou resolver novamente o mesmo cast, inserir segundo loop ou mutação. **⛔** Sem contrato real de hook/API, integração fail-closed.

**Fontes:** [matriz](../GLYPHS.md) · [acquisition](../ACQUISITION.md) · [registries](../REGISTRIES.md) · [provider](../README.md). Clean-room: somente fatos registrados na auditoria do Black Arcana, sem código/assets upstream.

## Engenharia de perks — propagação e cadeia de cast

- **Classe:** [`PropagatorHoming.java`](https://github.com/Alexthw46/Ars-Elemental/blob/fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d/src/main/java/alexthw/ars_elemental/common/glyphs/PropagatorHoming.java), commit fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d.
- **Contrato:** `IPropagator`, `getCastType=MethodHomingProjectile.INSTANCE`, `EffectReset.RESET_LIMITS.add(this)`, `onResolve→copyResolver`, typeIndex 8. `numSplits=1+getBuffCount(Split)` homing projectiles do mesmo resolver.
- **Alvos/direção:** cria `EntityHomingProjectileSpell`, aplica `MethodHomingProjectile.basicIgnores(...)`, Dampen→gravidade, velocity do método host `getProjectileSpeed`. Com Extract ou `FakePlayer` usa `IPropagator.getDirection(shooter,resolver,hitPos)`; senão yaw/pitch do caster com spread lateral.
- **Perks:** propagate + homing não deve produzir dupla atribuição de dano/custos/Mastery por spawn. Sem prova de persistência e callbacks do entity, modificação de targeting permanece condicionada.
- **Status:** ✅ identidade do JAR e fonte consultada; ⚠️ equivalência da implementação no JAR, addons/servidor/clientes e limites físicos pendentes; ⛔ nenhuma integração RPG ou perk aprovada nesta branch. O Ars mantém autoridade sobre SpellResolver, mana e entidade.
