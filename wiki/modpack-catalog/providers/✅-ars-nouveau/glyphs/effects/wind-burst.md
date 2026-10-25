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

## Certificação estática: dano e propagação — 25/10/2026

**✅ Contrato técnico estático documentado; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** O ✅ não representa perk implementada, correspondência integral de bytecode ou QA em jogo.

| Campo | Contrato e limites source-pinned |
|---|---|
| Identidade e versão | `ars_nouveau:glyph_wind_burst`, `com.hollingsworth.arsnouveau.common.spell.effect.EffectWindburst`, Ars Nouveau **5.13.1**, Elemental Air; tier I herdado de AbstractSpellPart.defaultTier, não override local. [Classe][burst-resolve], [tier herdado][general-defaults]. |
| Comportamento e causalidade | Override `onResolve(HitResult,...)` chama super (dispatch de entity/block, sem callback concreto deste glyph) e depois `world.explode` na posição do HitResult. Não cria projétil em voo: `dummyWindCharge` é objeto auxiliar local e não é adicionado ao mundo. Há uma chamada de explosão por resolução, com `ExplosionInteraction.TRIGGER`, ignição false, particles GUST e som WIND_CHARGE_BURST. [Execução][burst-resolve], [super][abstract-resolve]. |
| Parâmetros, fórmulas e caps | Tamanho enviado à explosão `R=1.2f+(float)(q*GENERIC_DOUBLE)`; scalar AOE default **1,0**. Termo de knockback enviado ao calculator `K=1.22f+(float)(a*AMP_VALUE)`; scalar amplify default **0,25**. Dampen pode reduzir K; **não há clamp local** de R/K. `SimpleExplosionDamageCalculator(true,false,Optional.of(K),blockTag)` é o contrato literal, não fórmula de dano final. Sensitive cap default **1**, compatíveis AOE/Amplify/Dampen/Sensitive. [Config/augments][burst-config]. |
| Targeting, geometria e efeitos | Centro é `rayTraceResult.getLocation()` para a resolução recebida; sem raio de aquisição, LOS, whitelist de alvos, trajetória ou projectile size próprios. Alcance é da Form. R é parâmetro de explosion, não garantia de alcance esférico de knockback recebido. Passa tag `BlockTags.BLOCKS_WIND_CHARGE_EXPLOSIONS` ao calculator; filtros/oclusão/interação de bloco são delegados à engine. Sem IDamageEffect, DamageType próprio ou duração de status neste glyph. |
| Custos e aprendizagem | Mana default **30**, tier I, receita `wind_charge×4 + air_essence`, XP default **27**, starter **não**. [Receita][burst-recipe], [XP][recipe-xp], [aquisição](../../ACQUISITION.md). Custo efetivo/config, composição e cooldown de cast pertencem à autoridade Ars; mana de jogador não é Source. O objeto dummy não representa outro cast, summon ou custo adicional. |
| Integração e autoridade | Ars Nouveau mantém casting, custo, status e entidades. [SpellModifierEvent via Builder][stats-builder] e [EffectResolveEvent.Pre][resolve-event] são superfícies públicas reais; [SpellResolver][resolve-pipeline] usa o `stats` local e não relê substituições do campo `preEvent.spellStats`. Cancelar Pre pula este Effect, não equivale a reverter efeitos anteriores. API existente não certifica adapter RPG Skill Tree/Black Arcana: `mutating_hook=NOT_VERIFIED`. Black Arcana mantém casting, Corruption, Strain e WorldEffectPolicy próprios; RPG Skill Tree só fornece progressão por contrato comprovado. Não publicar artificialmente `SpellDamageEvent` ou replicar explosão/knockback para encaixar procs. Não usa o `ANExplosion` de Explosion. Evento de explosão vanilla/NeoForge e claims dependem da engine/pack e não foram homologados como adapter desta ficha. |
| Evidência e validação | `PINNED_SOURCE_PLUS_SHA_EXACT_BINARY_IDENTITY`, source `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`, publisher `ars_nouveau-1.21.1-5.13.1.jar` SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`; [auditoria compilada](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md) prova **ID/classe**, não equivalência integral dos métodos. Config instalada, todos os listeners, cliente/servidor físico e resultado em modpack não foram testados: `physical_qa=NOT_TESTED`. |

### Sensitive muda o source, não instala um filtro próprio

[EffectWindburst.onResolve][burst-resolve] sempre instancia `new WindCharge(world,x,y,z,Vec3.ZERO)`. Com `stats.isSensitive()` chama `dummyWindCharge.setOwner(shooter)`, mas a referência passada como source da explosão é **o shooter**; sem Sensitive passa **dummyWindCharge**. A proteção ao caster é a intenção de `getBookDescription`/augment description; não existe nesse arquivo um loop removendo caster da lista de alvos nem um veto manual de knockback. A matriz exata de entidades afetadas, resistência a knockback, colisão, blocos ativáveis e atribuição de dano exige observar a implementação da engine1.21.1 e listeners do pack, sem promovê-la a garantia por analogia com outra magia.

AOE e Amplify alimentam argumentos distintos do calculator/engine; mudar a multiplicidade de carriers/raio de aquisição/dano recebido não deriva de R ou K. `TRIGGER` não é `NONE` nem `DESTROY_WITH_DECAY` e não demonstra “nenhuma interação com terreno”. Não há checagem local contra HitResult.MISS no override; a Form/resolver deve fornecer o hit esperado. Perk de área precisa de caps e testes de escala e causalidade antes de alterar q, e qualquer controle novo de Black Arcana usa seu WorldEffectPolicy próprio. [SpellResolver][resolve-pipeline] pode publicar Post mesmo quando um callback não produziu knockback efetivo; Post/partículas/som não são confirmação de alvo movido ou de mastery.

**Validade:** mudança de JAR, source, configuração, datapack ou listeners exige reauditoria. Nenhuma mutação executável foi implementada neste lote.

[damage-pipeline]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/IDamageEffect.java#L24-L78
[damage-event]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/SpellDamageEvent.java#L11-L43
[resolve-pipeline]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellResolver.java#L214-L270
[resolve-event]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/EffectResolveEvent.java#L11-L50
[stats-builder]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L138-L152
[general-defaults]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L128-L150
[augment-config]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L247-L255
[recipe-xp]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L142-L157
[burst-resolve]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectWindburst.java#L28-L66
[burst-config]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectWindburst.java#L68-L108
[burst-recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L129-L129
[abstract-resolve]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractEffect.java#L55-L67
