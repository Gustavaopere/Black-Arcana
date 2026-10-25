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

## Certificação estática por pipeline e consumidores — 25/10/2026

**✅ COMPLETE_PERK_READY apenas no escopo `STATIC_TECHNICAL_CATALOG_ONLY` — NÃO é certificação de perk jogável. ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** O ID e a classe no JAR publisher foram auditados separadamente da semântica lida no commit de source.

| Campo exigido | Contrato source-pinned, limites e classificação para perks |
|---|---|
| Identidade/versionamento | Ars Nouveau `5.13.1`; `ars_nouveau:glyph_lightning`; classe `EffectLightning`; escola Elemental Air, tier III. [Source imutável](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectLightning.java) e [registry do publisher SHA-exato](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). |
| Comportamento, causalidade e settlement | `onResolve(HitResult)` instancia `LightningEntity`, posiciona em `safelyGetHitPos`, atribui cause somente se caster for `ServerPlayer`, registra `amps`, `extendTimes`, `ampScalar`, `wetBonus` e `damage=baseConfig+stats.getDamageModifier()`, depois solicita `world.addFreshEntity`. Resultado/colisão/dano não ocorrem na própria classe de Effect; dependem de `LightningEntity.tick` e do Minecraft/NeoForge. |
| Parâmetros, escalas e caps | Defaults: damage base **5,0**, ampScalar **3,0**, wetBonus **2,0**, cap default Amplify **2**. `LightningEntity.getDamage(target)=(damage+ampScalar×amps+(wet?wetBonus:0))×multiplier`; multiplier inicia **1** e ganha 1 por slot de armadura, mão principal e offhand com `Capabilities.EnergyStorage.ITEM` (seis verificações possíveis). Não converter capacidade de energia em bônus de spell independente. Para Shocked o source usa `duration=200+200×extendTimes` ticks e amplifier `min(2,current+1)`, sujeitos ao fluxo do hit. |
| Targeting, geometria, projétil, tipo e duração | `tick` coleta entidades vivas em AABB X/Z **±3**, Y **−3 a +9** relativo ao relâmpago, usa hooks NeoForge e `thunderHit`. Deduplicação de **aplicação de Shocked** por ID na lista `hitEntities` não significa ausência de todos os `thunderHit` em ticks subsequentes; observar o fluxo real, não inferir single-hit global. Tipo final de dano pertence a `LightningBolt.thunderHit`, não à descrição de escola. |
| Custos, aprendizagem e limites da receita | Mana default **100**; tier III; XP receita default 160; starter default não; recipe `ars_nouveau:air_essence` + `minecraft:lightning_rod` ×3 + `minecraft:heart_of_the_sea`. [Acquisition 85/85](../../ACQUISITION.md). Cast/cooldown e mana efetiva da composição são autoridade/config Ars Nouveau. Augments: Amplify, Dampen, Extend Time, Reduce Time (`glyph_duration_down`). Duration multiplier é truncado para int ao preencher `extendTimes`. `EntityStruckByLightningEvent` cancelado executa `continue` após `setDamage(adjusted)` sem restaurar o `origDamage` no caminho observado: **risco potencial source**, não bug físico comprovado. |
| Integração e segurança | **⛔** Não adicionar outro LightningEntity, Shocked/XP adicional ou double-hit ao observar ticks. Fase/side, claims, weather, energy capability e cancelamento devem ser QA físico antes de adapter/perk mutadora. Contrato de perks RPG Skill Tree e hook mutador para este caminho não verificados. Não trocar target, type, raio, mana nem recipients com API presumida. Black Arcana conserva seu runtime, hazards e `WorldEffectPolicy` para efeitos próprios. |
| Grau de evidência/testes | Source `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`; JAR publisher `ars_nouveau-1.21.1-5.13.1.jar`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd` prova **ID/classe registrada**, não todos os métodos do classfile ou gameplay atual. Config final, order de eventos, integrações de outros mods, PvP/claims, servidor e cliente: **NOT_TESTED**. |

**Regra de reauditoria:** alterações de JAR/source, config, modificadores, geometria/ordem de eventos ou consumidor downstream exigem nova verificação técnica antes de liberar qualquer hook. Efeitos/raios/VFX não são eventos novos de cast/Mastery.
