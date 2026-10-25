# Fangs

- Registry ID: `ars_nouveau:glyph_fangs`
- Source class: `EffectFangs`
- School: Conjuration
- Default tier: **3**
- Default mana: **35**
- Default damage config: **6.0** base + **3.0** per amplification unit
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Source-pinned behavior

Creates provider Evoker Fang entities along a line toward the target. Self-targeting switches to two radial rings around the caster. Duration changes the fang timing and Accelerate shortens the per-fang delay; the exact class notes no Decelerate support in this line.

Compatible augments: Amplify, Dampen, Extend Time, Reduce Time, Accelerate. Amplify is limited to 2 by default.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:conjuration_essence` + `minecraft:prismarine_shard` ×2 + `minecraft:totem_of_undying`.
- Source-default recipe XP: **160 XP** (Tier III).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars owns fang entity lifecycle, timing and damage. Black Arcana summoned hazards must use its own bounded scheduler/damage contracts and cannot treat provider fang timing as a general hazard API.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.

## Dossiê de engenharia para perks — classe de efeito

- **Source pin:** [`EffectFangs.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectFangs.java), Ars Nouveau 5.13.1.
- **Dano bruto:** `DAMAGE.get()+AMP_VALUE.get()*getAmpMultiplier()` com defaults 6.0 e 3.0; máximo Amplify default 2; danos reais dependem de `EntityEvokerFangs` e defesa do alvo.
- **Alcance/contagem:** cast normal tenta **16 posições** em linha, a cada `1.25*(l+1)` blocos na direção do alvo (até 20 blocos de posição); cast self tenta **13 posições**, em dois anéis com 5 presas a raio 1.5 e 8 a raio 2.5. `spawnFangs` exige chão válido e pode **não gerar entidade** para posição sem suporte.
- **Delay:** por fang `j=(int)((index+durationMultiplier)/(1+count(Accelerate)))` em ambos os ramos. Isto é timer de ativação, **não** duração total de área; não existe Decelerate compatível nesta classe. **Perks:** separar número/velocidade/dano/proteção contra chão ausente; reduzir j não cria novos casts.
- **Status:** ✅ source exato lido; ⚠️ equivalência integral do bytecode, caps runtime e Survival requerem testes; API por efeito não foi validada contra RPG/Black Arcana. Sem autorização para segunda liquidação de dano/recurso/target.

## Certificação estática: entidades, gravidade e runa — 25/10/2026

**✅ `COMPLETE_PERK_READY` no escopo `STATIC_TECHNICAL_CATALOG_ONLY`; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** A certificação é da documentação estática. A identidade de ID/classe no publisher JAR foi auditada separadamente da lógica lida no source pin.

| Campo | Contrato técnico e limite de evidência |
|---|---|
| Identidade e versão | `ars_nouveau:glyph_fangs`; `com.hollingsworth.arsnouveau.common.spell.effect.EffectFangs`; Ars Nouveau **5.13.1**, Conjuration, tier III; consumidor `EntityEvokerFangs` [fang-identity][fang-identity] [fang-school][fang-school]. |
| Comportamento e causalidade | `onResolve` aceita o local do hit. Sem shooter, só tenta obter `ANFakePlayer` se houver `castingTile`; sem ambos retorna. O hit de entidade **igual ao caster** seleciona os dois anéis; os demais hits selecionam a linha. Cada posição tenta suporte via `spawnFangs`, não garante entidade [fang-effect][fang-effect]. O dano acontece posteriormente em `EntityEvokerFangs.tick`, não no callback do glyph [fang-entity][fang-entity]. |
| Parâmetros, escala e caps | Dano entregue ao construtor: `(float)(DAMAGE+AMP_VALUE*ampMultiplier)`, defaults **6 + 3×amp**, antes da defesa; `damageModifier` não é somado nesse caminho. Amplify cap default **2**. São **5** posições a raio **1,5** + **8** a raio **2,5** em self, ou **16** em linha a `1,25*(l+1)` blocos (última a **20**). Warmup `j=(int)((index+durationMultiplier)/(1+count(Accelerate)))`; não usa `accMultiplier`. Extend/Reduce alteram o atraso da presa, não o `lifeTicks` fixo **22** da entidade; Decelerate não é compatível [fang-effect][fang-effect] [fang-entity][fang-entity]. |
| Alvo, geometria, dano e tempo | A linha aponta do caster ao X/Z do hit, mas não termina no hit nem herda dele um alcance de dano. `spawnFangs` desce desde `max(hitY,casterY)+1`, buscando face superior sólida, até abaixo de `floor(min(hitY,casterY))-1`, considerando altura de colisão. No servidor, `--warmupDelayTicks==-8` consulta `LivingEntity` na hitbox da presa inflada **0,2 em X/Z, 0 em Y**. Exclui mortos, invulneráveis, caster e aliados do owner. Sem owner usa `damageSources().magic()`, com owner usa `indirectMagic(this,owner)` [fang-entity][fang-entity]. Não é projétil que viaje entre as posições. |
| Custos e aprendizagem | Mana default **35**, tier III, receita **160 XP**, starter default não. Receita: `ars_nouveau:conjuration_essence` + `minecraft:prismarine_shard` ×2 + `minecraft:totem_of_undying` [fang-recipe][fang-recipe] [recipe-xp][recipe-xp]. Custo efetivo é configurado e calculado para a composição; mana de jogador e Source são autoridades diferentes. Warmup e lifetime não são cooldown autônomo. |
| Integração, autoridade e deduplicação | A API nativa **existe**: `SpellStats.Builder.build` publica `SpellModifierEvent` com o builder original mutável [stat-build][stat-build] [modifier-event][modifier-event]; depois `EffectResolveEvent.Pre` é cancelável [resolve-event][resolve-event]. O resolver consome `stats` local e `this.hitResult`, não qualquer campo público substituído no objeto de evento [resolve-consumer][resolve-consumer]. Isso identifica superfícies para auditoria, sem provar adapter RPG Skill Tree, caps, pagamento, autoridade, target replacement ou deduplicação seguros. Black Arcana mantém sua própria `WorldEffectPolicy`, casting, Corruption e Strain. O fato de a classe implementar `IDamageEffect` **não** significa que chame `IDamageEffect.attemptDamage`: o consumidor chama `LivingEntity.hurt` diretamente. Não presumir `SpellDamageEvent.Pre/Post`, Fortune ou random rolls desse helper. Deduplicar cast → presa → hit; 13/16 posições e vários recipients não provam casts adicionais. Warmup negativo não é clampado: a ação de dano exige atingir exatamente **−8** após o decremento; `j≤−8` já pula essa igualdade no primeiro tick. Dano não tem clamp local nesta fórmula; defesa, invulnerability frames e outros listeners continuam relevantes. |
| Evidência e validação | Source `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`; publisher `ars_nouveau-1.21.1-5.13.1.jar`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`. A [auditoria binária de identidades](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md) prova registro ID/classe, não equivalência de todos os métodos, config instalada ou gameplay. Integração RPG/Black Arcana, ordem dos listeners, cliente/servidor e Survival: não testados. |

**Persistência e autoria:** o consumidor recebe owner/damage no construtor; seus métodos NBT mostrados persistem `Warmup` e escrevem `OwnerUUID` **somente se o campo privado `casterUuid` não for nulo**, não o campo customizado `damage`. O construtor mostrado chama `setOwner(casterIn)` herdado e não atribui esse campo privado; portanto não há garantia de que o UUID do caster original seja gravado ou que ownership sobreviva ao reload [fang-entity][fang-entity]. Não inferir dano preservado após save/reload, identidade de entidade em rede ou segurança do fake player a partir desta leitura. Esses limites não autorizam um segundo scheduler ou dano Black Arcana.

**Localizadores imutáveis adicionais:**

[fang-identity]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectFangs.java#L27-L32
[fang-effect]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectFangs.java#L35-L140
[fang-school]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectFangs.java#L151-L159
[fang-entity]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/EntityEvokerFangs.java#L30-L114
[fang-recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L72-L74
[stats-duration]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L48-L58
[stat-build]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L138-L152
[modifier-event]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/SpellModifierEvent.java#L13-L32
[resolve-event]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/EffectResolveEvent.java#L11-L49
[resolve-consumer]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellResolver.java#L220-L279
[cost-config]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L127-L149
[recipe-xp]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L142-L156
