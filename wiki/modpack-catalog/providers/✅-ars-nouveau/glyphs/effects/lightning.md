# Lightning

- Registry ID: `ars_nouveau:glyph_lightning`
- Source class: `EffectLightning`
- School: Elemental Air
- Default tier: **3**
- Default mana: **100**
- Default source config: damage **5.0**, amplification scalar **3.0**, wet-target bonus **2.0**
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Source-pinned behavior

Spawns Ars Nouveau's custom LightningEntity at the resolved location and transfers spell amplification/duration data into that entity. The provider documents Shocked stacking and bonus lightning interactions, including wet targets; the exact class sets the wet bonus from config and the lightning's source damage state.

Compatible augments: Amplify, Dampen, Extend Time, Reduce Time. Amplify is limited to 2 by default.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:air_essence` + `minecraft:lightning_rod` ×3 + `minecraft:heart_of_the_sea`.
- Source-default recipe XP: **160 XP** (Tier III).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars owns LightningEntity, Shocked and provider damage semantics. Black Arcana must preserve causal identity and avoid duplicate lightning damage/proc/mastery processing.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.

## Dossiê de engenharia para perks — causalidade exata

- **Código versionado:** [`EffectLightning.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectLightning.java), `com.hollingsworth.arsnouveau.common.spell.effect.EffectLightning` no Ars 5.13.1, método `onResolve`.
- **Spawn:** cria `LightningEntity`, posiciona no hit, `setCause` quando shooter é `ServerPlayer`; executa `world.addFreshEntity`. **Dados enviados:** `amps=(float)spellStats.getAmpMultiplier()`, `extendTimes=(int)getDurationMultiplier()`, `ampScalar=AMP_VALUE.get()` default 3.0, `wetBonus=GENERIC_DOUBLE.get()` default 2.0; `setDamage(DAMAGE.get()+getDamageModifier())` com damage default 5.0. **Executor downstream:** stack Shocked, wet-bonus, timers e hit são geridos por `LightningEntity`, não por esta classe inicializadora. Amplify limit default 2. **Perks:** alterar campos nativos não equivale a spawnar lightning adicional; hook não verificado.
- **Limite de integração:** ✅ source pin confirmado, ⚠️ config e classes auxiliares demandam QA; ⛔ hook de mutação RPG não verificado. Provider mantém autoridade de mana/efeito/owner; sem segundo cast/proc/settlement. Survival: PENDING.

## Auditoria do executor secundário — limitações verificáveis

- **Java:** [`common/entity/LightningEntity.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/LightningEntity.java).
- **Executor `LightningEntity` — dano por alvo:** `getDamage(entity) = (getDamage() + ampScalar*amps + (entity.isInWaterOrRain()? wetBonus:0))*multiplier`, em que `multiplier` inicia em 1 e aumenta para cada um dos 4 slots de armadura e main/offhand com `Capabilities.EnergyStorage.ITEM`. Portanto **não** tratar wet bonus ou itens com energy capability como magia independente. O tick seleciona entidades vivas em AABB de X/Z ±3 blocos e Y de −3 até +9 relativamente ao lightning, usa `EventHooks.onEntityStruckByLightning` e `EntityStruckByLightningEvent`; pode aplicar `SHOCKED_EFFECT` por `200+200*extendTimes` ticks com amplifier `min(2,current+1)`, uma vez por ID na lista `hitEntities`. **Risco a verificar:** no source, cancelamento de `EntityStruckByLightningEvent` faz `continue` depois de `setDamage(adjusted)`, antes de `setDamage(origDamage)`; marcar como potencial restauração incompleta e exigir teste, **não** declarar exploit confirmado.

**Limite:** fatos lidos do source pin, não prova de comportamento no JAR físico ou de adapter RPG. QA no modpack ainda pendente.
