# Orbit

Status: `SOURCE-PINNED 5.13.1 / GLYPH EFFECT / SEMANTICS+ACQUISITION AUDITED`

- Registry id: `ars_nouveau:glyph_orbit`
- Display name: `Orbit`
- Default tier: `THREE`
- Default mana cost: `50`
- School: no explicit school override; inherited default is an empty set, extensible by addons
- Exact source pin: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native behavior

`Orbit` consumes the remaining spell chain into a child `SpellContext`, prepends `Projectile`, cancels the parent continuation and spawns orbiting projectiles around the target. Base projectile count is `3`; each `Split` adds one more.

The orbit entities retain provider-owned spell resolvers and carry acceleration, radius/AOE and duration state. On hit they resolve the child spell through Ars Nouveau's own spell pipeline.

Compatible augments in the pinned source are:

- Accelerate;
- Decelerate;
- AOE;
- Pierce;
- Split;
- Extend Time;
- Duration Down;
- Sensitive.

## Acquisition / learning

- Provider-generated Glyph recipe: `minecraft:compass` + `minecraft:ender_eye` + `#c:rods/blaze`.
- Source-default recipe XP: **160 XP** (Tier III).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Black Arcana boundary

This is a persistent spell-composition/execution surface owned by Ars Nouveau. Black Arcana must not treat each orbit projectile as a new independent player cast, must not charge a second cost/cooldown, and must not replay child effects through the Black Arcana cast engine.

Any mastery/danger bridge must preserve root-cast causality and bounded attribution rather than multiplying credit by projectile count.

## QA / runtime

Source behavior is pinned to 5.13.1. Full 612-mod runtime/config QA remains separate.

## Certificação estática individual — 25/10/2026

**✅ `STATIC_TECHNICAL_CATALOG_ONLY`; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** A ficha documenta a lógica do source fixo e a identidade binária. Não certifica adapter RPG Skill Tree, config instalada, equivalência de todos os métodos do JAR ou gameplay.

| Campo | Contrato e limites exatos |
|---|---|
| Identidade, classe e versão | `ars_nouveau:glyph_orbit`, `com.hollingsworth.arsnouveau.common.spell.effect.EffectOrbit`, 5.13.1, tier III. [Effect][orbit] e [EntityOrbitProjectile][orbit-entity]. Sem escola explícita na classe; [base][schools] devolve conjunto vazio, extensível por addons. |
| Comportamento e causalidade | Só age com residual não vazio. Cria child context com `MethodProjectile` no início, cancela parent e spawna `total=3+stats.getBuffCount(Split)` carriers. No bloco rastreia posição do hit; em entidade faz dessa entidade o owner rastreado. Cada hit elegível resolve clone/child do residual pelo Ars resolver. |
| Parâmetros e caps | Carrier recebe `offset=i`, `accelerates=(int)acc`, `aoe=(float)AOE`, `extendTimes=(int)duration`, `total`. Executor: raio `R=1.5+0.5*AOE`, divisor angular `T=10-accelerates`, fase `15*i` rad, vida-limiar `1200+600*extendTimes` ticks. Sem clamp local de R, T, quantidade ou duração. Pierce/Sensitive contam recipe, não esses escalares. |
| Targeting, projétil e resultado | Dimensão registrada0,5×0,5; [busca herdada][projectile-hit] usa bounding box expandida pelo delta e inflate1, não raio de dano. Trace até posição angular3ticks adiante; posição real usa tickCount atual. Hit de owner é ignorado enquanto `!tracksGround`; bloco só resolve com `numSensitive>0`. Sem dano próprio: residual decide DamageType e resultado. |
| Custos e aprendizagem | Mana default **50**, tier III; [recipe][recipe-orbit]: compass + ender eye + `#c:rods/blaze`; [XP][recipe-xp]160; [starter][starter]false. Custo efetivo/admissão/cooldown são da composição Ars. Vida default-limiar1200 ticks=60s,  +600 ticks=30s por duração inteira; não é cooldown ou cast time. |
| Integração, autoria e deduplicação | Owner geométrico pode ser a vítima da órbita; caster real continua no SpellContext/resolver. Não atribuir dano/Mastery ao owner sem contrato. API builder/Pre existe, mas safe adapter RPG não foi comprovado; Split multiplica entidades e Pierce multiplica hits sem multiplicar casts/cobrança. |
| Evidência e validação | Effect, entidade, base projectile, contexto e recipe no commit fixo; identidade compilada SHA-exata, sem equivalência integral de métodos. `PINNED_SOURCE_PLUS_SHA_EXACT_BINARY_IDENTITY`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`. |

### Trajetória, fase e limites literais

[`EntityOrbitProjectile.getAngledPosition(nextTick)`][orbit-entity] usa `x=cx−R*sin(nextTick/T+offset)` e `z=cz−R*cos(nextTick/T+offset)`. `getOffset()` retorna índice×15, valor passado diretamente a sin/cos em **radianos**. Embora o Effect grave `TOTAL`, o cálculo angular não o consulta: não afirmar espaçamento igual `2π/total`, 15graus nem compensação de fase por Split. `T=10−(int)acc` é divisor, logo frequência angular é `1/T` rad/tick; Accelerate reduz T e Decelerate aumenta. Sem clamp: T=0 causa entradas não finitas de sin/cos; T negativo inverte sentido matemático. Não há prova de API segura para permitir esses valores.

Com owner vivo, centro acompanha `owner.x,z`; Y é `owner.y+1−(owner.isShiftKeyDown()?0.25:0)`. Sem owner, removido ou `tracksGround`, usa LAST_POS, Y+0,5 quando tracksGround. O hit de bloco inicia `tracksGround=true` e owner nulo; órbita de entidade inicia owner=target. `tick()` marca tracksGround se o owner sumir. `getNextHitPosition()` consulta ângulo de `tickCount+3`; `tickNextPosition` grava ângulo atual. O construtor herdado inicialmente posiciona o carrier no caster, em `eyeY−0,1`; a posição orbital só é escrita em `tickNextPosition`, depois do trace daquele tick. Não presumir que a primeira varredura parte sempre de um ponto já situado na órbita. O raio de trajetória é separado da dimensão 0,5×0,5 do [carrier][dimensions] e dos filtros de colisão herdados.

### Recipe original, hits e vida

O [remainder][context-remainder] começa na posição corrente, conservando augments do Orbit antes do próximo Effect. O Effect prepende `MethodProjectile`; o [construtor herdado][projectile-life] conta Pierce/Sensitive com `spell.getBuffsAtIndex(0,...)`, que [lê os augments contíguos da recipe][spell-augments]. Isso não equivale a alterar `SpellStats.getAoeMultiplier()` nem a lista de stats depois do build. Split usa contagem nos stats, enquanto aceleração/duração são truncadas e AOE é float. No ramo bloco, `makeChildContext` pode ser manipulado pelo residual; no ramo entidade o Effect sobrescreve a spell do child com o residual capturado previamente. Não garantir equivalência com Reset/addons por simples analogia.

[`onHit` de Orbit][orbit-entity] é override completo: ignora client/MISS; para entidade, ignora owner enquanto não tracksGround, depois resolve novo clone/child e chama `attemptRemoval`. Bloco exige `numSensitive>0` e não removido. [attemptRemoval herdado][projectile-hit] decrementa `pierceLeft` e descarta se `<0`, dando nominalmente `1+Pierce` impactos por carrier. Não existe lista de deduplicação de vítimas nesse override: o mesmo alvo pode consumir impactos se continuar elegível. [Filtro herdado][projectile-filter] usa `super.canHitEntity` ou tag `SPELL_CAN_HIT`; não ampliar isso para garantia de friendly fire.

O caminho [traceAnyHit herdado][projectile-life] ainda chama o veto NeoForge `EventHooks.onProjectileImpact`; mas o override de Orbit não chama o [`onHit` base][projectile-native-hit] que publica `SpellProjectileHitEvent`. Logo não anunciar esse evento Ars como gate universal de hit do Orbit. Eventos de resolução dos Effects downstream continuam [no resolver][resolver]. Portais são desativados em `canTraversePortals()`.

Limiar de vida: `60*20+30*20*extendTimes`, removido server-side quando [age>limiar][projectile-life]; sem clamp local para duração negativa. Não confundir o campo público `ticksLeft` salvo com o getter de expiração, que usa `extendTimes`. EntityType [noSave][dimensions] e [descarte em unload][projectile-unload] não garantem órbita persistente após reload. Orbit não declara ocorrência 1 própria; herda [default MAX_INT][defaults], separado de limites de receita/config. Movimento orbital com spell residual já é semântica ocupada; trocar só VFX/escola não cria outra mecânica.

### Fronteira de integração e validação

A API pública existe: [`SpellStats.Builder.build`][stats-builder] publica [`SpellModifierEvent`][modifier-event] com o builder original, depois de augments e itens. Alterações nesse mesmo builder podem participar dos stats retornados; adicionar augments nessa fase não repete automaticamente o loop de `applyModifiers` já executado. Substituir apenas `event.builder` por outro objeto não substitui a referência interna retornada. [`SpellResolver.resume`][resolver] publica [`EffectResolveEvent.Pre/Post`][effect-event] por Effect; o cancelamento de Pre salta aquele Effect. Post é evento de lifecycle, inclusive em caminhos `STOP_ALL`/capability que não executam o callback; não comprova dano ou sucesso no mundo. A mera existência dessas superfícies não comprova um adapter de perks. Parâmetros escalares, presença/contagem de augments e recipe residual são entradas distintas.

Ars é a autoridade de cast, magia composta, mana de jogador, entidades e efeitos. Source de automação é outro recurso. RPG Skill Tree mantém a progressão; qualquer ponte de leitura/mutação exige contrato, limites e deduplicação comprovados. Black Arcana mantém casting, Corruption, Strain e WorldEffectPolicy de seu próprio runtime. Child resolver, pulso, projétil ou alvo adicional não são casts independentes para cobrança, cooldown, Mastery ou procs.

Evidência: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`; publisher `ars_nouveau-1.21.1-5.13.1.jar`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`. A [auditoria binária das 109 identidades](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md) prova o vínculo compilado ID/classe de 85 glyphs e 24 rituais; a análise de fórmulas desta ficha vem do source fixo, sem alegar equivalência binária integral. [Aquisição](../../ACQUISITION.md), [eventos](../../VERIFIED-EVENT-SURFACES-5.13.1.md) e [norma editorial](../../../../meta/PERK-READY-CERTIFICATION-RULES.md). Mudanças de JAR, source, configs, listeners ou receitas invalidam as conclusões correspondentes.

[orbit]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectOrbit.java#L17-L94

[orbit-entity]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/EntityOrbitProjectile.java#L27-L242

[projectile-life]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/EntityProjectileSpell.java#L107-L210

[projectile-hit]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/EntityProjectileSpell.java#L291-L349

[projectile-native-hit]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/EntityProjectileSpell.java#L375-L439

[projectile-filter]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/EntityProjectileSpell.java#L464-L467

[projectile-unload]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/EntityProjectileSpell.java#L321-L326

[dimensions]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/registry/ModEntities.java#L185-L227

[context-remainder]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellContext.java#L281-L317

[spell-augments]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/Spell.java#L246-L272

[resolver]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellResolver.java#L177-L307

[stats-builder]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L138-L152

[modifier-event]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/SpellModifierEvent.java#L13-L32

[effect-event]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/EffectResolveEvent.java#L11-L50

[defaults]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L218-L255

[starter]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L307-L309

[schools]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L189-L199

[recipe-orbit]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L50-L50

[recipe-xp]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L142-L157
