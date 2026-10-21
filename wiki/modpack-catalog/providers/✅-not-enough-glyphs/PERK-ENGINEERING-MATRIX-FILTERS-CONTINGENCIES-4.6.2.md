# Not Enough Glyphs 4.6.2 — contingências e filtros (continuação técnica)

**Checkpoint documental:** as **22 fichas** deste lote (7 contingências + 15 filtros, incluindo os fallbacks) passam a integrar a engenharia causal, elevando a cobertura aprofundada do provider de **8/40 a 30/40**. As fichas representam identidades já catalogadas, sem novas raízes semânticas.

**Fonte:** `Alexthw46/NotEnoughGlyphs@45604dd18d9d2e3e7ca80a2c616b3309f42aca77` (versão declarada 4.6.2), com chamadas registradas em `ArsNouveauRegistry`. JAR físico indicado pela modlist `not_enough_glyphs-1.21.1-4.6.2.jar`, SHA-1 catalogado `32eea2c478a346ee7499f6a0db156241116f73e9`; equivalência do método compilado ao source **⚠️ NÃO COMPROVADA**. As 22 identidades são source-enabled antes de config SERVER; entre as oito fichas anteriores, Momentum permanece source-disabled.

## Contingências — disparadores diferentes

| Identidade | Ficha | Cadeia causal / cuidado |
|---|---|---|
| `not_enough_glyphs:glyph_contingency_fall` | [Contingency: Fall](glyphs/effects/neg/contingency-fall.md) | `FallContingency` → NEG trigger/event → `triggerSpell`; sem hook RPG homologado |
| `not_enough_glyphs:glyph_contingency_heal` | [Contingency: Heal](glyphs/effects/neg/contingency-heal.md) | `HealContingency` → NEG trigger/event → `triggerSpell`; sem hook RPG homologado |
| `not_enough_glyphs:glyph_contingency_health` | [Contingency: Health](glyphs/effects/neg/contingency-health.md) | `HeroicsContingency` → NEG trigger/event → `triggerSpell`; sem hook RPG homologado |
| `not_enough_glyphs:glyph_contingency_death` | [Contingency: Death](glyphs/effects/neg/contingency-death.md) | `DeathContingency` → NEG trigger/event → `triggerSpell`; sem hook RPG homologado |
| `not_enough_glyphs:glyph_contingency_fire` | [Contingency: Fire](glyphs/effects/neg/contingency-fire.md) | `FireContingency` → NEG trigger/event → `triggerSpell`; sem hook RPG homologado |
| `not_enough_glyphs:glyph_contingency_blink` | [Contingency: Blink](glyphs/effects/neg/contingency-blink.md) | `BlinkContingency` → NEG trigger/event → `triggerSpell`; sem hook RPG homologado |
| `not_enough_glyphs:glyph_contingency_time` | [Contingency: Expire](glyphs/effects/neg/contingency-time.md) | `ExpireContingency` → Sauce EXPIRATION → `triggerSpell`; sem hook RPG homologado |

- **Queda:** `fallDistance > 5 + amplifier` em tick. **Vida:** `health <= maxHealth*(2+amplifier)/10` no callback de dano. **Fogo:** exige tag `IS_FIRE`.
- **Cura:** handler `LivingHealEvent`. **Morte/totem:** handlers `LivingDeathEvent` e `LivingUseTotemEvent`. **Teleporte:** handler `EntityTeleportEvent`. Os três triggers homônimos têm corpos vazios em `ContingencyTriggers`; o handler `Events` faz o disparo, não o objeto de trigger sozinho.
- **Expiração:** `ContingencyEffectInstance.EXPIRE`; constantes passadas aos métodos herdados `60, 30, 200` com semântica/unit Saunders ainda pendentes. Não converter em segundos/ticks por suposição.

## Filtros — predicados e caveats

| Identidade | Ficha | Critério causal |
|---|---|---|
| `not_enough_glyphs:glyph_filter_light` | [Filter: Light](glyphs/effects/neg/filter-light.md) | `FilterLight` |
| `not_enough_glyphs:glyph_filter_dark` | [Filter: Dark](glyphs/effects/neg/filter-dark.md) | `FilterDark` |
| `ars_trinkets:glyph_filter_self` | [Filter: Self](glyphs/effects/ars-trinkets-fallback/filter-self.md) | `FilterSelf` |
| `ars_trinkets:glyph_filter_not_self` | [Filter: Not Self](glyphs/effects/ars-trinkets-fallback/filter-not-self.md) | `FilterSelf` |
| `toomanyglyphs:glyph_filter_block` | [Filter: Block](glyphs/effects/toomanyglyphs-fallback/filter-block.md) | `FilterBlock` |
| `toomanyglyphs:glyph_filter_entity` | [Filter: Entity](glyphs/effects/toomanyglyphs-fallback/filter-entity.md) | `FilterEntity` |
| `toomanyglyphs:glyph_filter_living` | [Filter: Living](glyphs/effects/toomanyglyphs-fallback/filter-living.md) | `FilterLiving` |
| `toomanyglyphs:glyph_filter_living_not_monster` | [Filter: Living, Not Monster](glyphs/effects/toomanyglyphs-fallback/filter-living-not-monster.md) | `FilterLivingNotMonster` |
| `toomanyglyphs:glyph_filter_living_not_player` | [Filter: Living, Not Player](glyphs/effects/toomanyglyphs-fallback/filter-living-not-player.md) | `FilterLivingNotPlayer` |
| `toomanyglyphs:glyph_filter_monster` | [Filter: Monster](glyphs/effects/toomanyglyphs-fallback/filter-monster.md) | `FilterMonster` |
| `toomanyglyphs:glyph_filter_player` | [Filter: Player](glyphs/effects/toomanyglyphs-fallback/filter-player.md) | `FilterPlayer` |
| `toomanyglyphs:glyph_filter_item` | [Filter: Item](glyphs/effects/toomanyglyphs-fallback/filter-item.md) | `FilterItem` |
| `toomanyglyphs:glyph_filter_animal` | [Filter: Animal](glyphs/effects/toomanyglyphs-fallback/filter-animal.md) | `FilterAnimal` |
| `toomanyglyphs:glyph_filter_is_baby` | [Filter: Baby](glyphs/effects/toomanyglyphs-fallback/filter-is-baby.md) | `FilterBaby` |
| `toomanyglyphs:glyph_filter_is_mature` | [Filter: Mature](glyphs/effects/toomanyglyphs-fallback/filter-is-mature.md) | `FilterMature` |

- **Light/Dark:** são canais distintos (`LightLayer.SKY` vs `LightLayer.BLOCK`), ambos com limiar `8+ampMultiplier`; Light usa `>=`, Dark usa `<`. As antigas chaves `light_level=10` e `darkness_level=3` dos cartões não sustentam os métodos source 4.6.2.
- **Player/Not Player:** incluem explicitamente `EntityDummy` do Ars; **Monster/Not Monster:** usam `MobCategory.MONSTER`, não subclassificação Java Monster.
- **Self:** o override de `onResolve` não contém predicado explícito que rejeite outra entidade na variante positiva; portanto a compatibilidade real deve ser testada contra o fluxo host antes de fazer perks de safety.
- **Filtros padrão:** `AbstractFilter.getDefaultManaCost=0` do Ars host; configuração SERVER efetiva e pipeline/resolver não comprovados.

**Estado:** ✅ 30/40 com engenharia source-located, ⚠️ JAR corpo/config/Survival, ⛔ adapter perks/Mastery/Black Arcana. **+0 identidades**. [Matriz inicial de 8/40](PERK-ENGINEERING-MATRIX-4.6.2.md) · [Catálogo registral](REGISTRATION-MATRIX.md).
