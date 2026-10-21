# Ars Elemental 0.7.10.1 — Propagate Arc

**✅ Revalidação binária exata (2026-10-13):** `ars_elemental:glyph_propagator_arc` é ID de registro estático provado no JAR 0.7.10.1 (SHA-1 `a1e4021177aae0e16c1f7c6487a82f0b68bbade3`) por [Java 21 #38403443682](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38403443682). `COUNTED_EXACT` para identidade; já contado, **+0**. Afirmações antigas de ID não verificado / `COUNTED_SOURCE_PINNED` abaixo são checkpoints superados. Mana/config/Survival ⚠️. [Dossiê](../EXACT-BINARY-GLYPHS-RITUALS-0.7.10.1.md).


Estado: **✅ `COUNTED_SOURCE_PINNED` — Propagator individualizado** · **⚠️ runtime, ID do registry e Survival pendentes**.

## Identidade e defaults source-pinned

- Nome na matriz editorial: **Propagate Arc**; categoria **Propagator**.
- Provider: `ars_elemental`; JAR físico `ars_elemental-1.21.1-0.7.10.1.jar`, SHA-1 `a1e4021177aae0e16c1f7c6487a82f0b68bbade3`.
- Source pin `Alexthw46/Ars-Elemental@fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d` e Ars Nouveau API base `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`. **A equivalência byte-a-byte entre o source pin e o JAR físico não está provada.**
- Classificação: `COUNTED_SOURCE_PINNED`, **já incluído na contribuição de 47 objetos** (39 partes de spell e oito rituais); **+0 novas identidades** com esta ficha.
- Config efetiva, receitas implantadas, custos modificados e resultados de gameplay em Survival: **⚠️ NÃO VERIFICADOS**. `MethodCarianPhalanx` está excluído (dev-only); `Nullify Defense` tem receita de aprendizado desativada por source default `frame_skip_recipe=false`.

- **Tier:** II.
- **Mana source-default:** 150.
- **School:** Manipulation.
- **Compatible augments:** Arc Projectile set + Extract.
- **ResourceLocation individual:** **NÃO VERIFICADO na matriz preservada**. Não inferir `ars_elemental:glyph_...` do nome de display.

## Semântica e limites

A matriz não preserva uma observação comportamental adicional para esta entrada; não se deduz comportamento não evidenciado pelo nome.

O propagador reemite a cadeia provider-owned através de Ars context/resolver, e não inicia um segundo root cast Black Arcana.

**Authority:** Ars Nouveau/Ars Elemental retêm mana, Source, custos, spell grammar, execução, targeting, world effects e cleanup. Black Arcana não pode cobrar ou resolver novamente o mesmo cast, inserir segundo loop ou mutação. **⛔** Sem contrato real de hook/API, integração fail-closed.

**Fontes:** [matriz](../GLYPHS.md) · [acquisition](../ACQUISITION.md) · [registries](../REGISTRIES.md) · [provider](../README.md). Clean-room: somente fatos registrados na auditoria do Black Arcana, sem código/assets upstream.

## Engenharia de perks — propagação e cadeia de cast

- **Classe:** [`PropagatorArc.java`](https://github.com/Alexthw46/Ars-Elemental/blob/fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d/src/main/java/alexthw/ars_elemental/common/glyphs/PropagatorArc.java), commit fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d.
- **Contrato:** `IPropagator` declara `getCastType=MethodArcProjectile.INSTANCE`; construtor registra o glyph em `EffectReset.RESET_LIMITS`. `onResolve` chama `copyResolver` para continuar a cadeia no novo local; `getTypeIndex=8`.
- **Quantidade:** `propagate` cria 1 projectile central e mais `getBuffCount(Split)` laterais, tipo `SPELL_PROJ_ARC`, com gravidade e `velocity=MethodArcProjectile.getProjectileSpeed(stats)`. Direção parte de `IPropagator.getDirection`; com Extract ou `FakePlayer` usa vetor de propagação, senão orientação do shooter.
- **Perks:** cada propagação usa resolver derivado e não é novo cast nem autoriza reset de mana/Mastery. `EffectReset.RESET_LIMITS` é gramática Ars, não mecanismo de poder ilimitado Black Arcana.
- **Status:** ✅ identidade do JAR e fonte consultada; ⚠️ equivalência da implementação no JAR, addons/servidor/clientes e limites físicos pendentes; ⛔ nenhuma integração RPG ou perk aprovada nesta branch. O Ars mantém autoridade sobre SpellResolver, mana e entidade.
