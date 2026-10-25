# Ars Nouveau — Burst

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_burst`
- Display name: Burst
- Default tier: 3
- Default mana cost: 500
- Compatible augments: AOE, Sensitive, Dampen
- Default Sensitive limit: 1
- Source-config occurrence limit: 1 (min/max1), enforced by recipe/context validation; not a global active-entity cap
- Default invalid combinations: Linger, Wall
- School: no explicit school override in the inspected class; do not infer one

## Provider-native behavior

Burst resolves the remaining spell across a spherical target set and then cancels the original context. Radius is `int(AOE multiplier) + 3` for entity targeting or `+1` with Sensitive block targeting. Dampen changes the filled sphere into a shell. Each eligible target receives a cloned child context/new resolver. Burst is registered in `EffectReset.RESET_LIMITS`.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:manipulation_essence` + `minecraft:tnt` ×5 + `minecraft:firework_star`.
- Source-default recipe XP: **160 XP** (Tier III).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Burst is an Ars spell-composition fan-out runtime. Black Arcana must not route those child executions through a parallel Black Arcana cast pipeline or duplicate resource/effect settlement.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectBurst`).

## Certificação estática individual — 25/10/2026

**✅ `STATIC_TECHNICAL_CATALOG_ONLY`; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** A ficha documenta a lógica do source fixo e a identidade binária. Não certifica adapter RPG Skill Tree, config instalada, equivalência de todos os métodos do JAR ou gameplay.

| Campo | Contrato e limites exatos |
|---|---|
| Identidade, classe e versão | `ars_nouveau:glyph_burst`, `com.hollingsworth.arsnouveau.common.spell.effect.EffectBurst`, 5.13.1, tier III. [Effect][burst]; sem override de escola, [base getSchools][schools] devolve conjunto vazio, com extensão por addons separada. |
| Comportamento e causalidade | Hit de bloco ou entidade define `center=blockPosition`; se o residual está vazio, retorna. `makeSphere` cria `getNewResolver(context.clone().makeChildContext())` para cada alvo selecionado, resolve o residual e só depois cancela parent. Não há entidade de campo nem reaplicação por tick nesta classe. |
| Parâmetros, caps e augments | `r=(int)AOE+(Sensitive?1:3)`; cast double→int trunca, sem clamp local. Preenchido: `d<=r+0.5`; Dampen por presença: também exige `d>=r-0.5`. Compatible AOE, Sensitive e Dampen; default Sensitive limit 1. `per_spell_limit` valor/min/max1, registro `RESET_LIMITS`. Sem cap numérico local de alvos/execuções. |
| Targeting, geometria e resultado | Sensitive itera `withinManhattan(center,r,r,r)` e filtra distância; hit de cada bloco usa coordenadas inteiras e face UP fictícia. Entidades: AABB do bloco central inflada por r, aceita LivingEntity ou `BURST_WHITELIST`, distância calculada por **blockPosition**. Sem filtro local caster/aliado/LOS. Dano/escola/status dependem do residual; Burst não tem DamageType próprio. |
| Custos, aprendizagem e tempo | Mana default **500**, tier III; [recipe][recipe-burst]: manipulation essence + TNT×5 + firework star; [XP][recipe-xp]160; [starter][starter]false. Custo/admissão/cooldown da composição Ars. Fan-out é síncrono no callback, sem duração de campo/projétil própria e sem cobrança autônoma por alvo. |
| Boundary de integração | Eventos públicos da execução de Effects existem, porém adaptar raio/fan-out ou alterar alvo por RPG permanece condicionado. Toda resolução child deve preservar raiz do cast e budget; não contar cada alvo como novo cast/Mastery nem liquidar de novo em Black Arcana. |
| Evidência e validação | `PINNED_SOURCE_PLUS_SHA_EXACT_BINARY_IDENTITY`; callback, helper de distância e resolver no commit fixo;109 IDs/classes SHA-exatos. `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`; config implantada, listeners e equivalência binária integral não comprovados. |

### Esfera/casca reais, não raio universal

[`onResolveBlock`/`onResolveEntity`][burst] convertem o hit em bloco central, perdendo a posição contínua como centro geométrico. O helper [`BlockUtil.distanceFromCenter`][distance] compara centros de blocos e resulta na distância euclidiana entre coordenadas inteiras. Para entidades, usa **o bloco onde está a posição da entidade**, não o ponto atingido nem a distância contínua de seu centro ou bounding box.

A busca de entidades é primeiro `world.getEntities(null,new AABB(center).inflate(r,r,r))`; só depois aplica `LivingEntity` ou `EntityTags.BURST_WHITELIST` e o predicado de distância. A tolerância `+0,5` do filtro não amplia a caixa candidata. Dampen não converte isso numa fronteira física contínua: é seleção de blocos/posições quantizadas numa casca de espessura nominal1 entre `r−0,5` e `r+0,5`. Sem Dampen aceita interior até `r+0,5`, ainda sujeito à caixa.

Sensitive percorre a enumeração `BlockPos.withinManhattan(center,r,r,r)` e o mesmo filtro, copiando cada posição para imutável. Cada hit de bloco usa `new Vec3(x,y,z)`, `Direction.UP` e false; não é recálculo de face, raycast ou LOS. A esfera pode conter blocos de ar; o Effect subsequente decide aplicabilidade/claims/destruição.

Sem augments extras, o r-base é3 para entidades e1 para Sensitive. +1 AOE é +1 no r depois da truncagem; não é multiplicador percentual nem tamanho do projétil. Não existe clamp positivo nem número máximo de alvos próprio nessa classe. A varredura de blocos pode crescer com o volume; Dampen filtra resolução, mas não elimina a enumeração candidata. Uma perk precisa de caps e orçamento antes de modificar essa superfície.

### Cancelamento, validação e causalidade

Cada alvo usa clone do contexto e `makeChildContext`; esse método [pode interpretar IContextManipulator no residual][context-child], não se resume a cortar a lista. O [resolver][resolver] executa Effects server-side com seus próprios eventos Pre/Post. `setCanceled(true)` no parent ocorre após os alvos e [notifica partes restantes][context-cancel]. Partículas e som não provam que um Effect downstream causou dano ou mudança de bloco.

[Declarações][burst]: invalid combos Linger e Wall, Sensitive limit 1, ocorrência 1 min/max1 e `RESET_LIMITS`. [StandardSpellValidator][validation] aplica ocorrência e [invalid combinations][invalid-combos] ao crafting; ocorrência no cast depende da flag de config e o contador [pode ser limpo por IContextManipulator][occurrences]. Essas restrições de receita não são teto global de resoluções no mundo. AOE fan-out/esfera/casca já é assinatura semântica Ars; nova magia exige regra além de nome, escola ou partículas.

### Fronteira de integração e validação

A API pública existe: [`SpellStats.Builder.build`][stats-builder] publica [`SpellModifierEvent`][modifier-event] com o builder original, depois de augments e itens. Alterações nesse mesmo builder podem participar dos stats retornados; adicionar augments nessa fase não repete automaticamente o loop de `applyModifiers` já executado. Substituir apenas `event.builder` por outro objeto não substitui a referência interna retornada. [`SpellResolver.resume`][resolver] publica [`EffectResolveEvent.Pre/Post`][effect-event] por Effect; o cancelamento de Pre salta aquele Effect. Post é evento de lifecycle, inclusive em caminhos `STOP_ALL`/capability que não executam o callback; não comprova dano ou sucesso no mundo. A mera existência dessas superfícies não comprova um adapter de perks. Parâmetros escalares, presença/contagem de augments e recipe residual são entradas distintas.

Ars é a autoridade de cast, magia composta, mana de jogador, entidades e efeitos. Source de automação é outro recurso. RPG Skill Tree mantém a progressão; qualquer ponte de leitura/mutação exige contrato, limites e deduplicação comprovados. Black Arcana mantém casting, Corruption, Strain e WorldEffectPolicy de seu próprio runtime. Child resolver, pulso, projétil ou alvo adicional não são casts independentes para cobrança, cooldown, Mastery ou procs.

Evidência: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`; publisher `ars_nouveau-1.21.1-5.13.1.jar`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`. A [auditoria binária das 109 identidades](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md) prova o vínculo compilado ID/classe de 85 glyphs e 24 rituais; a análise de fórmulas desta ficha vem do source fixo, sem alegar equivalência binária integral. [Aquisição](../../ACQUISITION.md), [eventos](../../VERIFIED-EVENT-SURFACES-5.13.1.md) e [norma editorial](../../../../meta/PERK-READY-CERTIFICATION-RULES.md). Mudanças de JAR, source, configs, listeners ou receitas invalidam as conclusões correspondentes.

[burst]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectBurst.java#L30-L136

[context-child]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellContext.java#L143-L175

[context-cancel]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellContext.java#L227-L253

[resolver]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellResolver.java#L177-L307

[stats-builder]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L138-L152

[modifier-event]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/SpellModifierEvent.java#L13-L32

[effect-event]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/EffectResolveEvent.java#L11-L50

[starter]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L307-L309

[schools]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L189-L199

[validation]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/validation/StandardSpellValidator.java#L38-L66

[occurrences]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/validation/GlyphOccurrencesPolicyValidator.java#L23-L43

[invalid-combos]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/validation/InvalidCombinationValidator.java#L20-L63

[distance]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/BlockUtil.java#L53-L86

[recipe-burst]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L120-L122

[recipe-xp]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L142-L157
