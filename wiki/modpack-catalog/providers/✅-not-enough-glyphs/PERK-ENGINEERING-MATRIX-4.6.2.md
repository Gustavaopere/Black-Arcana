# Not Enough Glyphs 4.6.2 — matriz de engenharia para perks

**Cobertura:** 8/40 fichas de primitivos registrados aprofundadas neste lote, sem aumento de identidades mágicas; 39 dos 40 são source-enabled antes da config SERVER, e Momentum é **source-disabled**. Fonte pública versionada: `Alexthw46/NotEnoughGlyphs@45604dd18d9d2e3e7ca80a2c616b3309f42aca77`; JAR declarado pela modlist: `not_enough_glyphs-1.21.1-4.6.2.jar`. Equivalência source/bytecode e execução física **⚠️ não demonstradas**.

| Ficha individual | Registry ID | Defaults exatos 4.6.2 / risco causal |
|---|---|---|
| [Plow](glyphs/effects/neg/plow.md) | `not_enough_glyphs:glyph_plow` | **0** (retificação: a ficha anterior dizia 5); não sobrescrito localmente · ✅ registrado; ⚠️ config/execução |
| [Flatten](glyphs/effects/arsomega-fallback/flatten.md) | `arsomega:glyph_flatten` | **30** (retificação: a ficha anterior dizia 100); II · ✅ fallback porque arsomega ausente; ⚠️ execução |
| [Momentum](glyphs/effects/neg/momentum.md) | `not_enough_glyphs:glyph_momentum` | **100**, valor inativo; III · ⚠️ REGISTRADO, PORÉM `isEnabled() == false` |
| [Propagate Underfoot](glyphs/effects/arsomega-fallback/propagate-underfoot.md) | `arsomega:glyph_propagate_underfoot` | **100**; II · ✅ fallback porque arsomega ausente; ⚠️ config/host |
| [Propagate Plane](glyphs/effects/neg/propagate-plane.md) | `not_enough_glyphs:glyph_propagate_plane` | **200**; II · ✅ registrado; ⚠️ config/execução |
| [Ray](glyphs/forms/toomanyglyphs-fallback/ray.md) | `toomanyglyphs:glyph_ray` | **15**; não sobrescrito localmente · ✅ fallback porque toomanyglyphs ausente; ⚠️ config |
| [Echoing Trail](glyphs/forms/neg/trail.md) | `not_enough_glyphs:glyph_trail` | **200** (retificação: antes 50); III (retificação: antes II) · ✅ registrado; ⚠️ config/execução |
| [Missile](glyphs/forms/arsomega-fallback/missile.md) | `arsomega:glyph_missile` | **20**; II · ✅ fallback porque arsomega ausente; ⚠️ config/execução |

Retificações frente a cartões legados: IDs têm prefixo `glyph_` estabelecido em `CompatRL`. **Plow: 0 (antes 5); Flatten: 30 (antes 100); Trail: 200, Tier III (antes 50, Tier II)**. A versão efetiva de `SERVER config` e o debit real podem diferir. A escolha de oito documentos corresponde a profundidade de análise, não a novas spells nem habilitação.

**Causalidade:** Plow/Flatten usam ferramentas via FakePlayer; Underfoot/Plane copiam resolver; Ray pode retornar SUCCESS sem atingir alvo; Trail produz vários resolves ao longo de ticks; Missile atinge múltiplas entidades por instância. **⛔** adapter RPG/Black Arcana de perk não implementado; evitar multicobrança, duplicação de mundo, Mastery por projectile/tick e buffers de geometria sem teto.

[Registration matrix](REGISTRATION-MATRIX.md) · [Revalidação source 4.6.2](CURRENT-4.6.2-SOURCE-REVALIDATION.md) · [Padrão técnico](../../meta/PERK-READY-TECHNICAL-STANDARD.md).
