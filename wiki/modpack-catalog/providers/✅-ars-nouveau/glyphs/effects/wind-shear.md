# Ars Nouveau — Wind Shear

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_wind_shear`
- Display name: Wind Shear
- School: Elemental Air
- Default tier: 2
- Default mana cost: 50
- Compatible augments: Dampen, Amplify, Randomize
- Default Amplify limit: 2
- Source default base damage: 5
- Source default Amplify scalar: +2.5

## Provider-native behavior

Wind Shear only resolves damage when the target is airborne. The executable source counts open blocks beneath the target up to 10 and uses that count directly in `base damage + amplify scalar * amplification + counted blocks`; grounded targets take no spell damage. The same config class also declares an `airDamage=0.75` field, but the inspected execution path does not use that field in this calculation, so runtime/config QA remains explicit.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:air_essence` + `minecraft:iron_sword` ×3.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns this airborne-height damage primitive. Black Arcana aerial control/damage should not clone the same conditional curve or assume the apparently unused config field is authoritative runtime behavior.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectWindshear`).

## Engenharia para perks — caminho causal individual

- **Source pin:** [`EffectWindshear.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectWindshear.java) do Ars 5.13.1.
- **Alvo:** só tenta dano quando `!target.onGround()` e entidade **não é ItemEntity**. O método não exige explicitamente `LivingEntity` nessa condição, embora `attemptDamage` e resistências downstream possam filtrá-las.
- **Escala de altitude:** começa `numBlocks=0` na blockPosition e executa `while(!world.getBlockState(pos.below()).blocksMotion() && numBlocks<=10){pos=pos.below();numBlocks++;}`. A comparação `<=10` permite **até 11 incrementos**, apesar de a descrição mencionar máximo de 10; não corrigir a divergência por inferência. Dano nominal = `DAMAGE.get()+AMP_VALUE.get()*ampMultiplier+numBlocks` com defaults 5.0 e 2.5.
- **Config não consumida:** `buildConfig` declara `GENERIC_DOUBLE` com default `airDamage=0.75`, mas `onResolveEntity` **não lê** esse campo para a fórmula de dano; não multiplicar altitude por 0.75 em perks até prova em outro executor. `attemptDamage` controla sucesso antes de partículas; Amp default limit 2.
- **Perks:** dano de queda da engine, bônus por altura, eventos de hit e callback de dano são coisas distintas. Alteração externa da busca de blocos exige clamp/work budget e teste de void/altura máxima.
- **Estado:** ✅ classe/método do source pin; ⚠️ scripts de addons, config física e QA Survival pendentes; ⛔ bridge de perks RPG e mutação de `SpellStats` sem validação de causalidade e limites.
