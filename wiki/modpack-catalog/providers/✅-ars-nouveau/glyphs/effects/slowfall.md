# Slowfall

- Registry ID: `ars_nouveau:glyph_slowfall`
- Source class: `EffectSlowfall`
- School: Elemental Air
- Default tier: **2**
- Default mana: **30**
- Default duration config: base **30**, Extend Time increment **8**
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Source-pinned behavior

Applies Minecraft Slow Falling through Ars Nouveau's configurable potion-effect path.

Compatible augments: Extend Time, Reduce Time.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:air_essence` + `ars_nouveau:wilden_wing` + `minecraft:feather` ×3 + `#c:rods/blaze` + `#c:crops/nether_wart`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars Nouveau owns duration/config and effect application. Black Arcana mobility/fall-safety mechanics remain independent unless a supported adapter explicitly consumes provider state.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.

## Engenharia para perks — caminho causal individual

- **Source pin:** [`EffectSlowfall.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectSlowfall.java) do Ars 5.13.1.
- **Efeito/targeting:** `onResolveEntity` aceita `LivingEntity` e chama `IPotionEffect.applyConfigPotion(living,MobEffects.SLOW_FALLING,spellStats)`. `EffectSlowfall` não ajusta o vetor de movimento diretamente; gravidade/queda são providas pelo efeito Minecraft.
- **Config:** `buildConfig` define 30s base e 8s por duration unit; com defaults carregados, `ticks=600+8*(int)(20*getDurationMultiplier())`, amplifier `(int)getAmpMultiplier()` do helper. Compatible somente Extend Time e Duration Down. **Perks:** não usar a mesma regra para reduzir dano de queda por outra magia sem hook e teste específicos.
- **Estado:** ✅ classe/método do source pin; ⚠️ scripts de addons, config física e QA Survival pendentes; ⛔ bridge de perks RPG e mutação de `SpellStats` sem validação de causalidade e limites.
