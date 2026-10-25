# Ars Nouveau — Firework

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_firework`
- Display name: Firework
- School: Elemental Fire
- Default tier: 2
- Default mana cost: 50
- Compatible augments: Extend Time, Amplify, Split
- Default Amplify limit: 2

## Provider-native behavior

Firework creates firework rockets at a block or living target. If the caster inventory already contains a Firework Rocket, Ars mirrors that stack; otherwise it generates a provider firework from spell duration/amplification. Split adds additional rockets. Only when no inventory model is found, Amplify determines generated Firework Stars and Extend Time determines the generated flight-duration component; an existing inventory model keeps its own components. Turret casting has a dedicated launch direction path.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:fire_essence` + `minecraft:firework_rocket` ×2 + `minecraft:firework_star`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns this firework-generation/casting surface and inventory lookup. Black Arcana should not duplicate a generic magical firework spell or replay projectile spawning when Ars is causal.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectFirework`).

## Engenharia para perks — caminho causal individual

- **Source exato:** [`EffectFirework.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectFirework.java), `com.hollingsworth.arsnouveau.common.spell.effect.EffectFirework` no Ars Nouveau 5.13.1.
- **Quantidade:** `onResolveBlock` e `onResolveEntity` fazem `count(Split)+1` iterações para gerar `FireworkRocketEntity`. O branch entidade exige `LivingEntity` atingida e chama `setOwner(shooter)`; turret em bloco escolhe orientação especial (ao contrário do jogador).
- **Inventário e fallback:** `fireworkFromInv` procura `Items.FIREWORK_ROCKET` via `InventoryManager.findItem(...,InteractType.EXTRACT)` e obtém o stack daquele slot; se não encontra, gera com `getFirework((int)durationMultiplier,(int)ampMultiplier)`. O código mostrado *não* diminui o stack encontrado no inventário: é modelo/cópia sem afirmar consumo.
- **Dados do foguete:** `getFirework` constrói `DataComponents.FIREWORKS` com `numGunpowder` recebido e `numStars` explosões via `getRandomStar` (`new Random` local). Limite default Amplify=2 na ficha. Variar estética não prova dano ou tempo/altitude exatos sem seguir `FireworkRocketEntity`.
- **Perks:** Split multiplica entidades e carga visual; não cria novos casts, custos ou Mastery. RNG de cores/estrelas é provider-owned e não deve ser tratado como dano arcano determinístico.
- **Estado:** ✅ classe/fórmulas source-pinned; ⚠️ outcomes downstream, config física e Survival pendentes; ⛔ nenhuma alteração por RPG Skill Tree implementada ou testada. Avaliar a interface `EffectResolveEvent.Pre` per-effect com clamps e causalidade.

## Certificação estática: entidades, gravidade e runa — 25/10/2026

**✅ `COMPLETE_PERK_READY` no escopo `STATIC_TECHNICAL_CATALOG_ONLY`; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** A certificação é da documentação estática. A identidade de ID/classe no publisher JAR foi auditada separadamente da lógica lida no source pin.

| Campo | Contrato técnico e limite de evidência |
|---|---|
| Identidade e versão | `ars_nouveau:glyph_firework`; `com.hollingsworth.arsnouveau.common.spell.effect.EffectFirework`; Ars Nouveau **5.13.1**, Elemental Fire, tier II; entidade downstream vanilla `FireworkRocketEntity` [firework-identity][firework-identity] [firework-school][firework-school]. |
| Comportamento e causalidade | Em bloco, gera foguetes no alvo; em entidade, exige `LivingEntity` e prende o foguete à vítima. Cada ramo itera `count(Split)+1` vezes. `fireworkFromInv` consulta o inventory manager do caster via `findItem(...,InteractType.EXTRACT)`, obtém o stack do slot e o devolve sem `extractItem`/`shrink` nesse método. A presença de `EXTRACT` na busca **não prova consumo** do modelo [firework-effect][firework-effect]. Não causa dano no callback do glyph. |
| Parâmetros, escala e caps | Sem modelo encontrado, `getFirework((int)durationMultiplier,(int)ampMultiplier)` constrói `DataComponents.FIREWORKS`: flight duration recebe o primeiro inteiro; a lista de explosões recebe `numStars` estrelas, geradas num loop `i<numStars`. Amplify cap default **2**; compatíveis Extend Time, Amplify, Split. **Com modelo de inventário, Amplify/Extend não reescrevem os componentes**: o modelo encontrado prevalece; Split continua multiplicando spawns [firework-effect][firework-effect] [firework-data][firework-data]. Não há clamp de contagem local além das condições do loop; limites de construção/config são contratos separados. |
| Alvo, geometria, dano e tempo | Entidade: `new FireworkRocketEntity(world,stack,(LivingEntity)hit)` e `setOwner(shooter)`. Bloco não-turret: centro do bloco adjacente à face, com offsets horizontais `i*inRange(-0,3;0,3)`, owner recebido no construtor. **TURRET**: centro do próprio bloco; faces horizontais são invertidas, UP/DOWN preservadas; chama `shoot(dirX,dirY,dirZ,0.5F,1.0F)` no construtor com `shotAtAngle=true`, sem `setOwner(shooter)` explícito nesse ramo [firework-effect][firework-effect]. Flight duration do componente não é lifetime em ticks calculado pelo glyph; hitbox, voo, detonação, dano/LOS e DamageType finais pertencem ao código vanilla, não foram quantificados por esta auditoria de source Ars. |
| Custos e aprendizagem | Mana default **50**, tier II, receita **55 XP**, starter default não. Receita: `ars_nouveau:fire_essence` + `minecraft:firework_rocket` ×2 + `minecraft:firework_star` [firework-recipe][firework-recipe] [recipe-xp][recipe-xp]. Receita de aprendizagem é distinta do modelo de inventário usado no cast. Cast/cooldown e custo efetivo da composição são Ars-owned/configurados; não cobrar uma segunda mana por foguete. |
| Integração, autoridade e deduplicação | A API nativa **existe**: `SpellStats.Builder.build` publica `SpellModifierEvent` com o builder original mutável [stat-build][stat-build] [modifier-event][modifier-event]; depois `EffectResolveEvent.Pre` é cancelável [resolve-event][resolve-event]. O resolver consome `stats` local e `this.hitResult`, não qualquer campo público substituído no objeto de evento [resolve-consumer][resolve-consumer]. Isso identifica superfícies para auditoria, sem provar adapter RPG Skill Tree, caps, pagamento, autoridade, target replacement ou deduplicação seguros. Black Arcana mantém sua própria `WorldEffectPolicy`, casting, Corruption e Strain. Implementar `IDamageEffect` aqui não prova uso de `attemptDamage`: o glyph só cria foguetes vanilla. `SpellDamageEvent`/Fortune/Black Arcana damage source não são inferidos. Preservar caster → foguete → detonação/hit sem transformar Split ou partículas em casts/Mastery adicionais; ownership no ramo turret precisa de teste próprio. |
| Evidência e validação | Source `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`; publisher `ars_nouveau-1.21.1-5.13.1.jar`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`. A [auditoria binária de identidades](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md) prova registro ID/classe, não equivalência de todos os métodos, config instalada ou gameplay. Integração RPG/Black Arcana, ordem dos listeners, cliente/servidor e Survival: não testados. |

**RNG e originalidade:** a geração sem modelo usa `new Random` para shape, cores, trail e twinkle; cores excluem BLACK/GRAY/LIGHT_GRAY/BROWN, com `nextInt(8)` cores por estrela [firework-data][firework-data]. Isso é estética/dado de foguete nativo, não um contrato de probabilidade de dano. Uma perk de alcance/tamanho não pode inferir raio a partir da shape da estrela; novo feitiço precisa de uma diferença mecânica verificável.

**Localizadores imutáveis adicionais:**

[firework-identity]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectFirework.java#L33-L38
[firework-effect]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectFirework.java#L41-L105
[firework-school]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectFirework.java#L112-L116
[firework-data]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectFirework.java#L120-L166
[firework-recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L72-L78
[stats-duration]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L48-L58
[stat-build]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L138-L152
[modifier-event]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/SpellModifierEvent.java#L13-L32
[resolve-event]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/EffectResolveEvent.java#L11-L49
[resolve-consumer]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellResolver.java#L220-L279
[cost-config]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L127-L149
[recipe-xp]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L142-L156
