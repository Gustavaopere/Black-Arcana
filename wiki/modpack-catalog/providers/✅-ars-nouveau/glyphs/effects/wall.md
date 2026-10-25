# Ars Nouveau — Wall

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_wall`
- Display name: Wall
- School: Manipulation
- Default tier: 3
- Default mana cost: 500
- Compatible augments: Sensitive, AOE, Accelerate, Decelerate, Extend Time, Reduce Time (`glyph_duration_down`), Dampen
- Default Sensitive limit: 1
- Source-config occurrence limit: 1 (min/max1), enforced by recipe/context validation; not a global active-entity cap
- Default invalid combination: Linger

## Provider-native behavior

Wall converts the remaining spell into an `EntityWallSpell`: it creates a child context, cancels the original continuation, installs a new resolver, orients the wall from caster facing and stores area, speed, duration, targeting and gravity behavior. Sensitive targets blocks instead of entities; Dampen suppresses gravity. Wall is registered in `EffectReset.RESET_LIMITS`.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:manipulation_essence` + `minecraft:dragon_breath` + `#c:storage_blocks/diamond` + `#c:rods/blaze` ×2.
- Source-default recipe XP: **160 XP** (Tier III).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Wall is a provider-owned persistent spell-execution surface, not merely a barrier graphic. Black Arcana must not create a second settlement/casting path around Ars Wall execution.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectWall`).

## Certificação estática individual — 25/10/2026

**✅ `STATIC_TECHNICAL_CATALOG_ONLY`; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** A ficha documenta a lógica do source fixo e a identidade binária. Não certifica adapter RPG Skill Tree, config instalada, equivalência de todos os métodos do JAR ou gameplay.

| Campo | Contrato e limites exatos |
|---|---|
| Identidade, classe e versão | `ars_nouveau:glyph_wall`, `com.hollingsworth.arsnouveau.common.spell.effect.EffectWall`, 5.13.1, tier III, Manipulation. [Effect][wall] e [executor EntityWallSpell][wall-entity]. |
| Comportamento e causalidade | Com partes restantes, cria child context, cancela parent, define estado do carrier e injeta novo resolver. Direção é face UP/DOWN preservada ou face horizontal `getClockWise()`. Cada alvo recebe um clone/child e novo resolver de Effects; não é um novo `onCast`. |
| Parâmetros, augments e limites | `a=(Sensitive?1:3)+AOE`, `f=round(a)`. Aceleração é `(int)stats.acc`; duração double `extendedTime`; Dampen por presença desliga queda. Sensitive usa `P=max(1,20-2*accelerates)` e dispara em `age==1` ou `age%P==0`; **entidades são verificadas a cada tick**, sem essa condição. `getExpirationTime=(int)(70+20*extendedTime)`. Até6 alvos/passagem; `maxProcs=100` só no ramo entidade. |
| Targeting, geometria, dano e duração | `start=B+(f*dir.x,0,f*dir.z)`; `end=B+(-f*dir.x,f,-f*dir.z)`. Sensitive percorre grade inclusiva start→end com hits UP. Entidades usam `AABB.encapsulatingFullBlocks(start,end)`. Carrier0,5×0,5, não a área. Sem DamageType/dano próprio; o residual resolve. Não há raycast novo ou filtro de amizade no executor. |
| Custos e aquisição | Mana default **500**, tier III; [recipe][recipe-wall]: manipulation essence + dragon breath + `#c:storage_blocks/diamond` + `#c:rods/blaze` ×2; [XP][recipe-xp]160; [starter][starter]false. Custo/config/cooldown do cast são Ars. O limiar de vida-base é70ticks (3,5s), não cooldown. |
| Integração e autoridade | Builder/eventos são superfícies reais, sem safe bridge comprovada. Distinguir tick, histórico de vítima, limite da passagem, total de aplicações e raiz do cast. Mutação de AOE/frequência/duração requer budget; não replicar dano/cast/cobrança em Black Arcana. |
| Evidência e validação | Source imutável de Effect, entidade, resolver e validator; identidade ID/classe no JAR SHA-exato. `PINNED_SOURCE_PLUS_SHA_EXACT_BINARY_IDENTITY`; `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`; sem comprovar config instalada ou equivalência de todos os métodos binários. |

### Geometria executada e separação dos dois modos

[`EffectWall.onResolve`][wall] usa posição do hit de bloco ou posição da entidade; orientação vem do caster, não da face atingida. Para direção horizontal e `f>=0`, a [grade][wall-entity] tem `(2*f+1)` colunas e `(f+1)` alturas em um único bloco de espessura: default não Sensitive `f=3` dá7×4×1. Sensitive sem AOE adicional `f=1` dá3×2×1. Como o código usa somente stepX/stepZ e altura positiva `f`, direções UP/DOWN têm ambos esses steps zero e produzem coluna vertical de1×(f+1)×1, não um plano horizontal garantido.

AABB engloba blocos inteiros, incluindo sua espessura1. O código contém tentativas de `inflate(growthFactor=1)` quando max==min num eixo; não tratar esse fallback como espessura universal adicional, pois `encapsulatingFullBlocks` já inclui o bloco inteiro. Não existe filtro de distância radial/LOS. As exclusões diretas são a própria wall e `LINGERING_BLACKLIST`; caster, itens e outras entidades podem chegar aos Effects seguintes.

Sensitive dispara também no primeiro tick `age==1`, além do módulo de intervalo; aplica o residual a todos os blocos da grade, sem contar `totalProcs` nem teto local por pulso. No ramo entidade, [castSpells][wall-entity] não usa Accelerate/Decelerate: varre a cada tick, consulta histórico por referência fraca e permite novo hit quando `gameTime - registrado > 20`. Isso é intervalo estrito maior que20, não exatamente20ticks.

**Reinserção não garantida no mesmo tick:** ao vencer um registro, remove-o da lista e permite hit, mas o `Optional hit` local continua presente; `if(hit.isEmpty())` não o reinsere nessa passagem. No próximo tick, a busca pode estar vazia, permitindo outra aplicação e só então adicionando registro novo. Portanto o código não comprova um cooldown regular de1s por entidade. Não conceder procs externos supondo uma deduplicação que o executor não garante.

Após aplicar, `i++` e `if(i>5) break` permitem até **6** hits por passagem. `totalProcs+=i` e descarte ao atingir/exceder100 acontecem após a passagem; pode ultrapassar 100, chegando a105 se havia 99 antes de mais 6. Entidades ignoradas por histórico não consomem esse contador. Lista de histórico não é teto do número de candidatos que a busca pode examinar.

### Vida, queda, admissão e limites

[Queda][wall-entity]: landed é `blocksMotion()` do bloco atual; deslocamento Y−0,2/tick até landed, ou posição fixa com Dampen. `traceAnyHit` vazio; o carrier não se comporta como parede sólida que bloqueia passagem. [Tick herdado][projectile-life] remove com `age>expiration` no servidor; depois a subclasse ainda chama `castSpells` sem guard de removido, logo não inferir corte perfeito no tick-terminal. [Registro noSave][dimensions] e [descarte ao descarregar chunk][projectile-unload] excluem garantia de persistência do campo.

[Wall][wall] declara Sensitive limit 1, occurrence1 (min/max1), invalid combo Linger e registro em `RESET_LIMITS`. [Validação de crafting][validation] consulta [invalid combinations][invalid-combos] e [occurrences][occurrences]; no cast ocorrência depende da flag de configuração, e combinação inválida não faz parte desse conjunto de validações de cast. Reset pode limpar contadores. São regras de receita/contexto, sem teto global de walls ativas. Parede de resolução periódica já é semântica Ars ocupada; não considerar mera troca de VFX ou tema uma magia nova.

### Fronteira de integração e validação

A API pública existe: [`SpellStats.Builder.build`][stats-builder] publica [`SpellModifierEvent`][modifier-event] com o builder original, depois de augments e itens. Alterações nesse mesmo builder podem participar dos stats retornados; adicionar augments nessa fase não repete automaticamente o loop de `applyModifiers` já executado. Substituir apenas `event.builder` por outro objeto não substitui a referência interna retornada. [`SpellResolver.resume`][resolver] publica [`EffectResolveEvent.Pre/Post`][effect-event] por Effect; o cancelamento de Pre salta aquele Effect. Post é evento de lifecycle, inclusive em caminhos `STOP_ALL`/capability que não executam o callback; não comprova dano ou sucesso no mundo. A mera existência dessas superfícies não comprova um adapter de perks. Parâmetros escalares, presença/contagem de augments e recipe residual são entradas distintas.

Ars é a autoridade de cast, magia composta, mana de jogador, entidades e efeitos. Source de automação é outro recurso. RPG Skill Tree mantém a progressão; qualquer ponte de leitura/mutação exige contrato, limites e deduplicação comprovados. Black Arcana mantém casting, Corruption, Strain e WorldEffectPolicy de seu próprio runtime. Child resolver, pulso, projétil ou alvo adicional não são casts independentes para cobrança, cooldown, Mastery ou procs.

Evidência: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`; publisher `ars_nouveau-1.21.1-5.13.1.jar`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`. A [auditoria binária das 109 identidades](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md) prova o vínculo compilado ID/classe de 85 glyphs e 24 rituais; a análise de fórmulas desta ficha vem do source fixo, sem alegar equivalência binária integral. [Aquisição](../../ACQUISITION.md), [eventos](../../VERIFIED-EVENT-SURFACES-5.13.1.md) e [norma editorial](../../../../meta/PERK-READY-CERTIFICATION-RULES.md). Mudanças de JAR, source, configs, listeners ou receitas invalidam as conclusões correspondentes.

[wall]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectWall.java#L22-L110

[wall-entity]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/EntityWallSpell.java#L35-L286

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

[invalid-combos]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/validation/InvalidCombinationValidator.java#L20-L63

[recipe-wall]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L117-L119

[recipe-xp]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L142-L157
