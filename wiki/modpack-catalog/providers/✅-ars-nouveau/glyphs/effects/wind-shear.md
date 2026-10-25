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

Wind Shear only resolves damage when the target is airborne. The executable source counts non-motion-blocking positions beneath the target with a loop that permits 11 increments and uses that count directly in `base damage + amplify scalar * amplification + counted blocks`; grounded targets take no spell damage. The same config class also declares an `airDamage=0.75` field, but the inspected execution path does not use that field in this calculation, so runtime/config QA remains explicit.

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

## Certificação estática: dano e propagação — 25/10/2026

**✅ Contrato técnico estático documentado; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** O ✅ não representa perk implementada, correspondência integral de bytecode ou QA em jogo.

| Campo | Contrato e limites source-pinned |
|---|---|
| Identidade e versão | `ars_nouveau:glyph_wind_shear`, `com.hollingsworth.arsnouveau.common.spell.effect.EffectWindshear`, Ars Nouveau **5.13.1**, Elemental Air, tier II. [Classe/execução][shear-resolve]. |
| Comportamento e causalidade | `onResolveEntity` somente se `!entity.onGround()` e entidade não é `ItemEntity`. Sem callback de bloco próprio e sem dano de queda vanilla emitido; comentário sobre FALL não troca a fonte realmente construída. Não há teste explícito de LivingEntity no gate; o helper trata mortos/aliados e sucesso de `hurt`. [Execução][shear-resolve], [helper][damage-pipeline]. |
| Parâmetros, fórmula e teto real | `n=0`; enquanto bloco imediatamente abaixo não `blocksMotion()` **e `n<=10`**, move uma posição para baixo e incrementa. Pode resultar **n=11**, apesar da descrição “up to10”. Nominal **5+2,5a+n** com config default. Campo configurável `airDamage=0,75` é declarado mas **não lido** por essa fórmula; não usar5+2,5a+0,75n. Amplify limite default **2**; compatíveis Dampen/Amplify/Randomize. [Loop e dano][shear-resolve], [config][shear-config]. |
| Targeting, geometria e resultado | Um EntityHitResult selecionado pela Form; nenhuma área, extensão de raycast, LOS, projectile size ou duração próprios. A coluna vertical faz até **11 incrementos** e até **12 consultas** ao bloco abaixo (o teste de bloco precede `n<=10` no `&&`), avalia `blocksMotion`, não “somente ar”, e começa na `blockPosition`, não mede distância fracionária dos pés. Fonte efetiva `ars_nouveau:windshear`; tag gerada `minecraft:bypasses_armor` pode ser substituída pelo pack. [DamageType][damage-types], [tag][armor-tag]. |
| Custos e aprendizagem | Mana default **50**, tier II, receita `air_essence + iron_sword×3`, XP default **55**, starter **não**. [Receita][shear-recipe], [XP][recipe-xp], [aquisição](../../ACQUISITION.md). Config de custo e custo agregado/discounts da composição são autoridades Ars; player mana não é Source. Sem cooldown ou canalização autônomos nessa classe. |
| Integração e autoridade | Ars Nouveau mantém casting, custo, status e entidades. [SpellModifierEvent via Builder][stats-builder] e [EffectResolveEvent.Pre][resolve-event] são superfícies públicas reais; [SpellResolver][resolve-pipeline] usa o `stats` local e não relê substituições do campo `preEvent.spellStats`. Cancelar Pre pula este Effect, não equivale a reverter efeitos anteriores. API existente não certifica adapter RPG Skill Tree/Black Arcana: `mutating_hook=NOT_VERIFIED`. Black Arcana mantém casting, Corruption, Strain e WorldEffectPolicy próprios; RPG Skill Tree só fornece progressão por contrato comprovado. [SpellDamageEvent.Pre][damage-event] permite veto/alteração do dano e fonte no caminho real, sem transformar alvo/contexto substituídos no evento em parâmetros relidos. Modificar a curva de altura exige interceptação comprovada: `airDamage` existente não é prova dessa superfície. |
| Evidência e validação | `PINNED_SOURCE_PLUS_SHA_EXACT_BINARY_IDENTITY`, source `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`, publisher `ars_nouveau-1.21.1-5.13.1.jar` SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`; [auditoria compilada](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md) prova **ID/classe**, não equivalência integral dos métodos. Config instalada, todos os listeners, cliente/servidor físico e resultado em modpack não foram testados: `physical_qa=NOT_TESTED`. |

### Como calcular e observar sem duplicar queda

[IDamageEffect.attemptDamage][damage-pipeline] toma o nominal do loop, rejeita morto/aliado, adiciona `stats.getDamageModifier()` e atributo nativo `PerkAttributes.SPELL_DAMAGE_BONUS`; Randomize soma `buffCount*random.nextIntBetweenInclusive(-1,1)`. Se a fonte for SpellDamageSource armazena Fortune. Publica Pre e **relê somente `damageSource`/`damage`**; retorna false para dano<=0/cancelamento ou `hurt` recusado; chama `setLastHurtMob` e Post apenas após hit aceito. Os campos `caster`, `target` e `context` do [evento][damage-event] não são relidos pelo helper como substitutos dos locais. Cancelar Pre neste efeito impede seu único dano, não desfaz outro Effect da composição nem eventos de queda nativos posteriores.

A fonte é [DamageUtil.source(...,WINDSHEAR,shooter)][shear-resolve], `DamageTypesRegistry.WINDSHEAR` registra `ars_nouveau:windshear`. O fato de o JSON gerado marcar bypass de armor não garante imunidades finais, tags do servidor ou proteção de claims do pack. O método não verifica `ServerLevel` no gate; o helper faz cast para ServerLevel e as partículas também: execução autoritativa tem que seguir o pipeline servidor Ars, não chamar o callback indiscriminadamente no cliente.

O limite finito da busca controla custo por resolução, não número total de resoluções de uma cadeia: Linger, Wall, Burst ou Orbit podem multiplicar callbacks. Proc/mastery deve manter identidade do cast e da aplicação confirmada, sem creditar a busca de cada bloco, partículas, queda do alvo ou `EffectResolveEvent.Post` como dano adicional. Mudar target para área ou contagem de alvos não é um simples ajuste de AOE nesse glyph, que não aceita esse augment.

**Validade:** mudança de JAR, source, configuração, datapack ou listeners exige reauditoria. Nenhuma mutação executável foi implementada neste lote.

[damage-pipeline]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/IDamageEffect.java#L24-L78
[damage-event]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/SpellDamageEvent.java#L11-L43
[resolve-pipeline]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellResolver.java#L214-L270
[resolve-event]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/EffectResolveEvent.java#L11-L50
[stats-builder]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L138-L152
[general-defaults]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L128-L150
[augment-config]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L247-L255
[recipe-xp]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L142-L157
[shear-resolve]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectWindshear.java#L27-L60
[shear-config]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectWindshear.java#L62-L100
[shear-recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L110-L110
[damage-types]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/registry/DamageTypesRegistry.java#L12-L16
[armor-tag]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/generated/resources/data/minecraft/tags/damage_type/bypasses_armor.json#L1-L12
