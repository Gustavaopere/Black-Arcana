# Ars Nouveau — Linger

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_linger`
- Display name: Linger
- School: Manipulation
- Default tier: 3
- Default mana cost: 500
- Compatible augments: Sensitive, AOE, Accelerate, Decelerate, Extend Time, Reduce Time (`glyph_duration_down`), Dampen
- Default Sensitive limit: 1
- Source-config occurrence limit: 1 (min/max1), enforced by recipe/context validation; not a global active-entity cap

## Provider-native behavior

Linger converts the remaining spell into an `EntityLingeringSpell`: it creates a child `SpellContext`, cancels the original continuation, installs a new resolver and stores AOE, targeting mode, pulse frequency, duration and gravity behavior on the lingering entity. Sensitive switches targeting from entities to blocks; Dampen suppresses gravity. Linger is also registered in `EffectReset.RESET_LIMITS`.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:manipulation_essence` + `minecraft:dragon_breath` + `#c:storage_blocks/diamond` + `#c:rods/blaze` ×2.
- Source-default recipe XP: **160 XP** (Tier III).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

This is a provider-owned persistent spell-execution runtime, not merely an area effect. Black Arcana must not route Ars lingering execution through a second Black Arcana cast pipeline or duplicate provider costs/effect settlement.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectLinger`).

## Certificação estática individual — 25/10/2026

**✅ `STATIC_TECHNICAL_CATALOG_ONLY`; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** A ficha documenta a lógica do source fixo e a identidade binária. Não certifica adapter RPG Skill Tree, config instalada, equivalência de todos os métodos do JAR ou gameplay.

| Campo | Contrato e limites exatos |
|---|---|
| Identidade, classe e versão | `ars_nouveau:glyph_linger`, `com.hollingsworth.arsnouveau.common.spell.effect.EffectLinger`, 5.13.1, tier III, escola Manipulation. [Effect][linger] e [executor EntityLingeringSpell][lingering-entity]. |
| Comportamento e causalidade | `onResolve` obtém a posição do hit, exige `currentIndex < spell.size`, cria child por `makeChildContext`, cancela o parent e instala novo resolver na entidade. O residual ainda pode conter augments sem Effect útil. Cada aplicação executa `getNewResolver(context.clone().makeChildContext()).onResolveEffect`, sem chamar `onCast`/`expendMana` novamente. |
| Parâmetros, augments e caps | AOE armazenado como float; Sensitive boolean; aceleração truncada para int; `extendedTime=durationMultiplier` double. `Dampen` desliga a queda por presença. [Executor][lingering-entity]: `a=(Sensitive?1:3)+AOE`; `P=max(1,20-2*accelerates)` ticks; `age % P == 0`. `getExpirationTime=(int)(70+20*extendedTime)`. Budget `maxProcs=100` e até **6** entidades por passagem; Sensitive não participa desse budget. |
| Target, geometria e resultado | Spawn em `safelyGetHitPos`: posição da entidade ou localização do hit de bloco. Sem Sensitive, busca na caixa de bloco `new AABB(blockPosition()).inflate(a)`; não é esfera. Com Sensitive, grade XZ de `[-round(a),+round(a)]`, mesmo Y, face fictícia UP. Sem dano/Heal/DamageType próprio: o residual determina o resultado. [Carrier][dimensions] mede 0,5×0,5 blocos; essa dimensão não é a área de busca. |
| Custos, aprendizagem e tempo | Mana default **500**, tier III; recipe [datagen][recipe-linger]: manipulation essence + dragon breath + `#c:storage_blocks/diamond` + `#c:rods/blaze` ×2; [XP][recipe-xp] **160**; [starter][starter] false. Custo/config/admissão/cooldown são da composição Ars. Duração da entidade não é cooldown; 70 ticks = 3,5 s como limiar-base. |
| Autoridade e mutabilidade | API real `SpellModifierEvent`/`EffectResolveEvent.Pre` não homologa safe adapter. Perk de AOE aumenta volume/grade; frequência e duração multiplicam execuções; adicionar Presence Dampen não equivale a alterar amplitude. Deduplicar raiz→campo→pulso→alvo/Effect; nenhum segundo cast ou dano em Black Arcana. |
| Evidência e validação | `PINNED_SOURCE_PLUS_SHA_EXACT_BINARY_IDENTITY`; referências imutáveis do Effect, entidade e resolver; identidade compilada SHA-exata. Config instalada, listener externo, custo efetivo, integração RPG e cliente/Survival não testados: `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`. |

### Execução downstream: geometria, frequência e orçamento

[`EntityLingeringSpell.castSpells`][lingering-entity] processa a grade sensível inteira no servidor a cada pulso. Com augments inteiros padrão sem AOE extra, `a=1` e a grade é 3×3; com +1 AOE, 5×5. Não existe nesse ramo teto local de blocos por pulso nem incremento de `totalProcs`. O hit é criado no canto inteiro do bloco com `Direction.UP`, não um novo raycast ou prova de LOS.

No ramo entidade, a caixa tem extensão `(1+2*a)` em cada eixo para `a>=0`; `a=3` produz caixa nominal 7×7×7. São excluídos apenas o próprio campo e `EntityTags.LINGERING_BLACKLIST` nessa seleção. Não há filtro local de LivingEntity, caster, aliado, distância esférica ou linha de visão; o Effect seguinte pode filtrar/rejeitar o alvo. Depois da aplicação, `i++` e o teste `i>5` permitem seis alvos. `totalProcs+=i` só ao fim da passagem; o limiar100 pode ser ultrapassado pela última passagem (até 105 se havia 99 e aplica mais 6), não é teto exato de100 aplicações. Não existe histórico por UUID: o mesmo alvo elegível pode ser reaplicado em cada pulso.

[`tick` e `tickNextPosition`][lingering-entity] verificam `blocksMotion()` do bloco atual e descem 0,2 bloco/tick até landed; com Dampen `tickNextPosition` retorna, mantendo a posição. O override `traceAnyHit` vazio elimina resolução por colisão normal. `Accelerate/Decelerate` alteram **intervalo de aplicação**, com truncamento e piso1tick; não alteram essa velocidade de queda.

O [tick herdado][projectile-life] remove no servidor quando `age > getExpirationTime()` ou não há resolver; `age` é incrementado antes do teste. A subclasse chama `castSpells` depois de `super.tick()` sem testar `isRemoved`, então o retorno interno do pai não prova ausência de uma última aplicação nesse tick. Não há clamp local de duração/AOE negativos. Carrier [registrado noSave][dimensions] e [descarte ao descarregar chunk][projectile-unload]: não prometer persistência/recovery de campo.

### Limites da composição e espaço semântico ocupado

[Linger][linger] declara Sensitive limit 1 e `per_spell_limit` com valor/min/max1 e registra-se em `EffectReset.RESET_LIMITS`. Isso é limite de ocorrência da **receita validada**, não prova universal de um único campo ativo no mundo. [Validator][validation] aplica ocorrência no crafting e, no cast, somente sob `ENFORCE_GLYPH_LIMIT_ON_CAST`; [contador][occurrences] pode ser limpo por manipulador de contexto como Reset. O glyph já ocupa reaplicação periódica em área; mudar apenas VFX/escola não cria uma mecânica original.

### Fronteira de integração e validação

A API pública existe: [`SpellStats.Builder.build`][stats-builder] publica [`SpellModifierEvent`][modifier-event] com o builder original, depois de augments e itens. Alterações nesse mesmo builder podem participar dos stats retornados; adicionar augments nessa fase não repete automaticamente o loop de `applyModifiers` já executado. Substituir apenas `event.builder` por outro objeto não substitui a referência interna retornada. [`SpellResolver.resume`][resolver] publica [`EffectResolveEvent.Pre/Post`][effect-event] por Effect; o cancelamento de Pre salta aquele Effect. Post é evento de lifecycle, inclusive em caminhos `STOP_ALL`/capability que não executam o callback; não comprova dano ou sucesso no mundo. A mera existência dessas superfícies não comprova um adapter de perks. Parâmetros escalares, presença/contagem de augments e recipe residual são entradas distintas.

Ars é a autoridade de cast, magia composta, mana de jogador, entidades e efeitos. Source de automação é outro recurso. RPG Skill Tree mantém a progressão; qualquer ponte de leitura/mutação exige contrato, limites e deduplicação comprovados. Black Arcana mantém casting, Corruption, Strain e WorldEffectPolicy de seu próprio runtime. Child resolver, pulso, projétil ou alvo adicional não são casts independentes para cobrança, cooldown, Mastery ou procs.

Evidência: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`; publisher `ars_nouveau-1.21.1-5.13.1.jar`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`. A [auditoria binária das 109 identidades](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md) prova o vínculo compilado ID/classe de 85 glyphs e 24 rituais; a análise de fórmulas desta ficha vem do source fixo, sem alegar equivalência binária integral. [Aquisição](../../ACQUISITION.md), [eventos](../../VERIFIED-EVENT-SURFACES-5.13.1.md) e [norma editorial](../../../../meta/PERK-READY-CERTIFICATION-RULES.md). Mudanças de JAR, source, configs, listeners ou receitas invalidam as conclusões correspondentes.

[linger]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectLinger.java#L18-L97

[lingering-entity]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/EntityLingeringSpell.java#L28-L225

[projectile-life]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/EntityProjectileSpell.java#L107-L210

[projectile-unload]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/EntityProjectileSpell.java#L321-L326

[dimensions]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/registry/ModEntities.java#L185-L227

[resolver]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellResolver.java#L177-L307

[stats-builder]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L138-L152

[modifier-event]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/SpellModifierEvent.java#L13-L32

[effect-event]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/EffectResolveEvent.java#L11-L50

[starter]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L307-L309

[validation]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/validation/StandardSpellValidator.java#L38-L66

[occurrences]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/validation/GlyphOccurrencesPolicyValidator.java#L23-L43

[recipe-linger]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L93-L95

[recipe-xp]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L142-L157
