# Wind Burst

Status: `SOURCE-PINNED 5.13.1 / AIR CONTROL EFFECT / SEMANTICS+ACQUISITION AUDITED`

- Registry id: `ars_nouveau:glyph_wind_burst`
- Display name: `Wind Burst`
- Default mana cost: `30`
- School: Elemental Air
- Exact source pin: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native behavior

`Wind Burst` resolves a wind-charge-style explosion at the target location using Minecraft's explosion pipeline with `Level.ExplosionInteraction.TRIGGER`.

Pinned defaults:

- base explosion radius term: `1.2`;
- AOE multiplier contribution: `1.0`;
- base knockback strength term in the damage calculator: `1.22`;
- Amplify contribution: `0.25`;
- default mana: `30`.

Compatible augments are AOE, Amplify, Dampen and Sensitive. Sensitive sets the caster as explosion owner so the caster can ignore the provider's knockback behavior.

## Acquisition / learning

- Provider-generated Glyph recipe: `minecraft:wind_charge` ×4 + `ars_nouveau:air_essence`.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Black Arcana boundary

This is an Ars Nouveau world/entity effect. Black Arcana must not replay the explosion or knockback. An independent Black Arcana wind/explosion effect would still require Black Arcana's own `WorldEffectPolicy`; provider behavior is not a waiver of project safety rules.

## QA

Exact spell-entry behavior is source-pinned to 5.13.1. Full-pack interaction with protection/claims and other wind-charge hooks remains runtime QA.

## Engenharia para perks — caminho causal individual

- **Source pin:** [`EffectWindburst.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectWindburst.java) do Ars 5.13.1.
- **Explosão real:** `onResolve` chama `world.explode(...)` com `Level.ExplosionInteraction.TRIGGER` e particles/sound de wind charge. Tamanho enviado = `1.2f+(float)(getAoeMultiplier()*GENERIC_DOUBLE.getAsDouble())` (config scalar default 1.0), e strength ao `SimpleExplosionDamageCalculator` = `1.22f+(float)(getAmpMultiplier()*AMP_VALUE.getAsDouble())` (amp default 0.25). Não equiparar strength ao dano final causado por alvo sem examinar pipeline de explosion.
- **Caster-protection:** com Sensitive, source de explosão é o shooter; sem ele, usa `dummyWindCharge`. Não há veto manual em `EffectWindburst`; todas as proteções aplicáveis dependem dos eventos vanilla/NeoForge e de `Level.explode`. Sensitive tem limite default 1.
- **Perks:** modificação de AOE e Amplify afeta magnitude e raio por caminhos independentes; não reaplicar `ANExplosion` (esse executor é de outro glyph). WorldEffectPolicy só rege explosões de Black Arcana, não permite reemitir as do Ars.
- **Estado:** ✅ classe/método do source pin; ⚠️ scripts de addons, config física e QA Survival pendentes; ⛔ bridge de perks RPG e mutação de `SpellStats` sem validação de causalidade e limites.
