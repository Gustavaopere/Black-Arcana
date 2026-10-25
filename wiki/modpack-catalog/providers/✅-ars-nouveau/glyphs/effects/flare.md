# Ars Nouveau — Flare

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_flare`
- Display name: Flare
- School: Elemental Fire
- Default tier: 2
- Default mana cost: 40
- Compatible augments: Amplify, Dampen, AOE, Fortune, Randomize
- Source default base damage: 7
- Source default Amplify damage scalar: +3
- Default Amplify limit: 2

## Provider-native behavior

Flare only damages living targets already burning, standing in fire, or carrying Ars' Blasting effect. An eligible target spawns damaging Cinder entities even if the direct damage attempt fails or is canceled; block casts can trigger from nearby fire. If the target has Blasting, Flare removes that effect and immediately detonates the provider Blasting explosion at increased strength. AOE increases the number of spawned Cinders. Cinders use Mage Fire and do not spread normal fire to terrain.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:fire_essence` + `minecraft:flint_and_steel` ×2 + `minecraft:fire_charge` ×2 + `minecraft:blaze_rod`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Flare occupies conditional fire detonation/cinder territory. Black Arcana Black Flame content must not be a cosmetic copy of this ignition-conditioned burst or duplicate Blasting settlement.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectFlare`).

## Engenharia para perks — caminho causal individual

- **Source exato:** [`EffectFlare.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectFlare.java), `com.hollingsworth.arsnouveau.common.spell.effect.EffectFlare` no Ars Nouveau 5.13.1.
- **Admissão:** `canDamage` exige fogo no alvo, `ModPotions.BLAST_EFFECT` ou estar em bloco com `BlockTags.FIRE`; dano nominal `DAMAGE+AMP_VALUE*getAmpMultiplier()` com defaults 7 e 3, via `IDamageEffect.attemptDamage`.
- **Cinder spawn:** a classe chama `spawnCinders` depois de passar em `canDamage`, **independentemente do boolean de sucesso** dentro de `damage(...)`. Gera `(int)Math.ceil(3+getAoeMultiplier())` entidades `Cinder` com bloco `MAGIC_FIRE`, `baseDamage=0.5*(DAMAGE+AMP_VALUE*ampMultiplier)`, `dropItem=false`, `hurtEntities=true` e `ShapersFocus.tryPropagateEntitySpell`.
- **Blasting:** se o alvo ainda tem `BLAST_EFFECT`, lê amplifier, remove efeito e chama `BlastEffect.explode(living,amplifier+1)`: uma causa distinta do dano direto e das Cinders, mas pertence à **mesma** cadeia de magia. Ramo bloco inicia Cinders quando bloco atingido ou vizinhos têm `BlockTags.FIRE`.
- **Perks:** área é contagem de Cinders, não raio de dano diretamente. Verificar caps sobre entidades persistentes, proc rate e WorldEffectPolicy apenas na autoridade Black Arcana. Não creditar Blast+Flare+Cinders como três casts.
- **Estado:** ✅ classe/fórmulas source-pinned; ⚠️ outcomes downstream, config física e Survival pendentes; ⛔ nenhuma alteração por RPG Skill Tree implementada ou testada. Avaliar a interface `EffectResolveEvent.Pre` per-effect com clamps e causalidade.

## Certificação estática: dano e propagação — 25/10/2026

**✅ Contrato técnico estático documentado; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** O ✅ não representa perk implementada, correspondência integral de bytecode ou QA em jogo.

| Campo | Contrato e limites source-pinned |
|---|---|
| Identidade e versão | `ars_nouveau:glyph_flare`, `com.hollingsworth.arsnouveau.common.spell.effect.EffectFlare`, Ars Nouveau **5.13.1**, Elemental Fire, tier II. [Callbacks/ID][flare-resolve]. |
| Comportamento e causalidade | LivingEntity no ServerLevel deve estar queimando, ter `BLAST_EFFECT` ou ocupar `BlockTags.FIRE`. Dano direto, Cinders e detonação de Blasting são fases distintas: as duas últimas não dependem de `attemptDamage` retornar true. Bloco atingido ou um dos **seis** vizinhos com tag FIRE inicia Cinders uma vez, retornando no primeiro encontrado. [Admissão/ordem][flare-resolve]. |
| Parâmetros, fórmulas e caps | Dano nominal `D=DAMAGE+AMP_VALUE*a`, defaults **7+3a**; `N=(int)ceil(3+q)` Cinders, cada uma `baseDamage=0,5D`, sem clamp de quantidade local. Amplify cap default **2**; AOE aumenta contagem, não o raio nominal unitário de dispersão. `addExtendTimeConfig(1)` existe, mas nenhum duration augment é compatível e esse parâmetro não é lido neste executor. [Geração][flare-cinders], [config/augments][flare-config]. |
| Targeting, geometria e dano | Aquisição/LOS/range pertencem à Form; Cinder é carrier secundário, hitbox default **0,5×0,5**, fireImmune. Spawn em offsets `x−sin(random.nextInt(360))`, `z−cos(random.nextInt(360))` (argumentos efetivos em radianos); não é distribuição angular uniforme comprovada. Dano direto `DamageTypesRegistry.FLARE` = `ars_nouveau:flare`; dados gerados o incluem em `minecraft:is_fire`, sujeito a datapack. [Registro][cinder-size], [tipos][damage-types], [tag][fire-tag]. |
| Custos e aprendizagem | Mana default **40**, tier II, receita `fire_essence + flint_and_steel×2 + fire_charge×2 + blaze_rod`, XP **55**, starter **não**; [receita][flare-recipe], [XP][recipe-xp], [aquisição](../../ACQUISITION.md). Custo da composição/config não é 40 garantidos; mana do jogador e Source são recursos distintos. Sem cooldown próprio ou TTL fixo de Mage Fire neste glyph. |
| Integração e autoridade | Ars Nouveau mantém casting, custo, status e entidades. [SpellModifierEvent via Builder][stats-builder] e [EffectResolveEvent.Pre][resolve-event] são superfícies públicas reais; [SpellResolver][resolve-pipeline] usa o `stats` local e não relê substituições do campo `preEvent.spellStats`. Cancelar Pre pula este Effect, não equivale a reverter efeitos anteriores. API existente não certifica adapter RPG Skill Tree/Black Arcana: `mutating_hook=NOT_VERIFIED`. Black Arcana mantém casting, Corruption, Strain e WorldEffectPolicy próprios; RPG Skill Tree só fornece progressão por contrato comprovado. [SpellDamageEvent.Pre][damage-event] afeta a tentativa direta, não cancela automaticamente `spawnCinders` nem `BlastEffect.explode`. Procs por impacto, Mage Fire e explosão não são novos casts. |
| Evidência e validação | `PINNED_SOURCE_PLUS_SHA_EXACT_BINARY_IDENTITY`, source `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`, publisher `ars_nouveau-1.21.1-5.13.1.jar` SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`; [auditoria compilada](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md) prova **ID/classe**, não equivalência integral dos métodos. Config instalada, todos os listeners, cliente/servidor físico e resultado em modpack não foram testados: `physical_qa=NOT_TESTED`. |

### Cinders, Mage Fire e Blasting têm executores diferentes

- **Dano direto:** [IDamageEffect][damage-pipeline] soma damageModifier e atributo nativo SPELL_DAMAGE_BONUS ao nominal; Randomize soma `buffCount*random[-1,1]`, Fortune é gravado no SpellDamageSource. Aliados/mortos são rejeitados, Pre relê damage/source e pode vetar; Post só ocorre com `hurt` aceito. `EffectFlare.damage` usa o resultado apenas para partículas: [retorno não controla o resto do callback][flare-resolve]. Mesmo aliado admitido por `canDamage(living)` pode iniciar Cinders; não inferir proteção global a partir do helper.
- **Movimento e propriedade:** [spawnCinders][flare-cinders] usa offset horizontal de termo unitário, velocidade horizontal multiplicada por valores aleatórios entre 0,1 e 0,5, Y aleatório entre0,1 e0,5; `radiusMultiplier=1` não escala com AOE. Atribui `shooter`, `dropItem=false` e `hurtEntities=true`, mas não `setOwner(shooter)` nem `cancelDrop=true`; `shooter` é campo separado do owner herdado. [Tick herdado][falling-tick] soma gravidade −0,04 por tick e aplica drag0,98, com descarte após600 ticks ou condição de altura após100; isso não é duração exata de todo carrier.
- **Impacto físico:** [EnchantedFallingBlock.onHitEntity][falling-hit] usa `ceil(clamp(min(speed,2,5)*baseDamage+getStateDamageBonus(),0,2147483647))`, dano `thrown(this,getOwner())`, conjunto de IDs já tentados e knockback horizontal default `2*0,6` mais Y0,1 em LivingEntity quando há direção. Não usa `IDamageEffect` nem `SpellDamageEvent`; não assumir dano igual a `0,5D` por impacto ou Luck/bônus nativo reaplicados. [Cinder][cinder] ainda redefine `canHitEntity` como `super.canHitEntity(entity) || entity.type.is(EntityTags.SPELL_CAN_HIT)`; a segunda condição pode admitir uma entidade independentemente dos filtros herdados de owner/IDs, logo o conjunto de IDs não prova um veto universal a hits repetidos. Não implementa o splash frost comentado no arquivo: aquele trecho está desativado; o callback ativo só emite fumaça/som.
- **Terreno:** `Cinder.groundBlock` chama o [assentamento herdado][falling-ground]; se falhar descarta e chama callback. Quando as condições herdadas permitem `setBlock`, o estado é `MAGIC_FIRE`, não fogo vanilla. [MagicFire][magic-fire] tem `canBurn=false`, sem laço de propagação; agenda ticks de **15–24** ticks, envelhece atéAGE7 e pode apagar conforme chuva, suporte, gamerule e bloco fonte. A descrição “short lived” não prova TTL universal: com fire source abaixo ou firetick desabilitado o mesmo caminho não garante expiração em um número fixo de segundos. Danos de contato herdados de BaseFireBlock/engine e proteção efetiva não são uma segunda fórmula do glyph.
- **Blasting:** se ainda houver `BLAST_EFFECT` após tentativa direta e spawn, lê amplifier `b`, remove o status e chama [BlastEffect.explode(living,b+1)][blasting]. Esse helper usa `level.explode(null,x,y+1,z,2.0f+pAmplifier,false,ExplosionInteraction.NONE)`; portanto termo de raio neste caminho **3+b**, source explícito **null** e interação NONE. Não é `ANExplosion`, não recebe stats/context/shooter e não fixa o dano final recebido. O tick natural do mesmo status chama explode com `b` quando duration==1 (termo2+b); Flare consome antecipadamente o status, sem transformar suas Cinders em casts autônomos.
- **Shapers Focus:** [tryPropagateEntitySpell][shapers] pode cancelar a continuação no contexto pai e resolver/agendar contexto filho sobre cada Cinder. Budget de entidades, persistência, atribuição de owner, callbacks de bloco e deduplicação precisam de contrato antes de uma perk alterar quantidade/velocidade/tamanho; as APIs públicas de stats não resolvem isso por si só.

**Validade:** mudança de JAR, source, configuração, datapack ou listeners exige reauditoria. Nenhuma mutação executável foi implementada neste lote.

[damage-pipeline]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/IDamageEffect.java#L24-L78
[damage-event]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/SpellDamageEvent.java#L11-L43
[resolve-pipeline]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellResolver.java#L214-L270
[resolve-event]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/EffectResolveEvent.java#L11-L50
[stats-builder]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L138-L152
[general-defaults]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L128-L150
[augment-config]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L247-L255
[recipe-xp]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L142-L157
[flare-resolve]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectFlare.java#L32-L77
[flare-cinders]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectFlare.java#L79-L115
[flare-config]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectFlare.java#L118-L166
[flare-recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L75-L75
[cinder]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/Cinder.java#L20-L76
[cinder-size]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/registry/ModEntities.java#L137-L143
[falling-hit]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/EnchantedFallingBlock.java#L322-L391
[falling-ground]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/EnchantedFallingBlock.java#L235-L319
[falling-tick]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/EnchantedFallingBlock.java#L188-L233
[magic-fire]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/block/MagicFire.java#L106-L207
[blasting]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/potions/BlastEffect.java#L14-L26
[shapers]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/items/curios/ShapersFocus.java#L32-L49
[damage-types]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/registry/DamageTypesRegistry.java#L12-L16
[fire-tag]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/generated/resources/data/minecraft/tags/damage_type/is_fire.json#L1-L8
