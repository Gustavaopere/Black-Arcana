# Not Enough Glyphs 4.6.2 — fechamento da engenharia dos 40 primitivos

**Estado documental:** ✅ **40/40 identidades com dossiês source-located** nesta branch. São **39 source-enabled sob o conjunto de mods carregados** e `not_enough_glyphs:glyph_momentum` **registrado, porém `isEnabled=false`**. Isso **não confirma** a habilitação efetiva de 39 glifos no SERVER do modpack. Nenhuma nova raiz semântica.

**Arquitetura:** Java 21 / NeoForge 1.21.1; source exact-semver `Alexthw46/NotEnoughGlyphs@45604dd18d9d2e3e7ca80a2c616b3309f42aca77`; binário instalado registrado como `not_enough_glyphs-1.21.1-4.6.2.jar`, fingerprint no catálogo SHA-1 `32eea2c478a346ee7499f6a0db156241116f73e9`. Não foi feita equivalência de corpos Java ao JAR nem GameTest/Survival.

## Cobertura detalhada

- [Oito fichas iniciais](PERK-ENGINEERING-MATRIX-4.6.2.md): Plow, Flatten, Momentum, Propagate Underfoot, Propagate Plane, Ray, Echoing Trail e Missile.
- [Mais 22 fichas de filtros e contingências](PERK-ENGINEERING-MATRIX-FILTERS-CONTINGENCIES-4.6.2.md): 7 contingências + 15 filtros.
- **Dez fichas finais** descritas abaixo: 2 efeitos nativos, 2 efeitos fallback Too Many Glyphs, 1 efeito fallback Ars Scalaes, 4 propagadores Ars Omega e 1 forma Ars Omega.

| ID registral | Ficha | Ponto de engenharia |
|---|---|---|
| `not_enough_glyphs:glyph_ride` | [Ride](glyphs/effects/neg/ride.md) | Default 20 mana; EffectRide |
| `not_enough_glyphs:glyph_feed` | [Feed](glyphs/effects/neg/feed.md) | Default 30 mana; EffectFeed |
| `toomanyglyphs:glyph_chaining` | [Chaining](glyphs/effects/toomanyglyphs-fallback/chaining.md) | Default 300 mana; EffectChaining |
| `toomanyglyphs:glyph_reverse_direction` | [Redirect Placement](glyphs/effects/toomanyglyphs-fallback/reverse-direction.md) | Default 0 mana; EffectReverseDirection |
| `ars_scalaes:glyph_resize` | [Resize](glyphs/effects/ars-scalaes-fallback/resize.md) | Default 100 mana; EffectResize |
| `arsomega:glyph_propagate_missile` | [Propagate Missile](glyphs/effects/arsomega-fallback/propagate-missile.md) | Default 200 mana; PropagateMissile |
| `arsomega:glyph_propagate_overhead` | [Propagate Overhead](glyphs/effects/arsomega-fallback/propagate-overhead.md) | Default 100 mana; PropagateOverhead |
| `arsomega:glyph_propagate_projectile` | [Propagate Projectile](glyphs/effects/arsomega-fallback/propagate-projectile.md) | Default 100 mana; PropagateProjectile |
| `arsomega:glyph_propagate_self` | [Propagate Self](glyphs/effects/arsomega-fallback/propagate-self.md) | Default 100 mana; PropagateSelf |
| `arsomega:glyph_overhead` | [Overhead](glyphs/forms/arsomega-fallback/overhead.md) | Default 5 mana; MethodOverhead |

### Gaps de implementação e testes

- `EffectFeed`: extração item-side de inventário, Stuffed 400 ticks, amplificador até 9, chance de explosão por Crush; não replicar a transação ou confundir dano `Pre` com dano confirmado.
- `EffectChaining`: cadeia recursiva/derivada de `SpellContext.clone().withSpell(remaining)`, max default de 16 blocos/8 entidades mas limites de config até `Integer.MAX_VALUE`; nenhum Mastery por filho sem deduplicação.
- `EffectResize`: interação de `addPotionConfig(60*20)` com fórmula de segundos/ticks ambígua; requer teste exato da configuração e helper Ars.
- `PropagateMissile`: Extract consta na descrição e no branch de tiro, mas **não** está na lista normal de augments compatíveis retornada do `MethodMissile`; QA de grammar.
- `MethodOverhead` e `PropagateOverhead`: formas distintas de targeting, embora tematicamente semelhantes.

**Autoridade:** Ars/NEG/Sauce + vanilla executam e cobram; Black Arcana não duplica runtime; RPG Skill Tree oferece progressão por contrato. **⛔ Adapters perks/Mastery/gates não implementados**. Validação física, config efetiva, compatibilidade host real e proteção permanecem **⚠️ condicionadas**.

[Registry 4.6.2](REGISTRATION-MATRIX.md) · [Ledger global](../../meta/PERK-READY-COVERAGE-LEDGER.md).
