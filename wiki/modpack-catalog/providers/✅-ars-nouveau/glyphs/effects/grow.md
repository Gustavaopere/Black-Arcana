# Grow

- Registry ID: `ars_nouveau:glyph_grow`
- Source class: `EffectGrow`
- School: Elemental Earth
- Default tier: **2**
- Default mana: **70**
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Source-pinned behavior

Applies bone-meal-style growth to provider-calculated block targets, including the water-plant fallback path where applicable. The exact source checks the provider claim-respect helper before attempting growth.

Compatible augments: AOE, Pierce.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:earth_essence` + `minecraft:bone_block` ×5 + `#c:seeds` ×3.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars Nouveau owns Grow semantics. Black Arcana must not duplicate generic crop acceleration without a material forbidden-domain distinction, and any Black Arcana world mutation remains policy-controlled.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.

## Dossiê de engenharia para perks — causalidade exata

- **Código versionado:** [`EffectGrow.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectGrow.java), `com.hollingsworth.arsnouveau.common.spell.effect.EffectGrow` no Ars 5.13.1, método `onResolveBlock`.
- **Alvos:** `SpellUtil.calcAOEBlocks` seleciona posições de blocos, com augments AOE/Pierce permitidos. **Mutação:** só considera bloco com `BlockUtil.destroyRespectsClaim` e `ServerLevel`; usa `BoneMealItem.applyBonemeal` com `ANFakePlayer`, ou fallback `BoneMealItem.growWaterPlant` no vizinho se face for sólida. **Efeito visual:** `world.levelEvent(1505,...)` após sucesso; partículas não são prova de growth independente. **Perks:** velocidade/custo/área precisam preservar chance/condições vanilla de cada bloco e work budget; não supor crescimento garantido.
- **Limite de integração:** ✅ source pin da lógica local, ⚠️ execução auxiliares/config dependem do provider real; ⛔ hook externo de mutação não comprovado. Black Arcana só governa suas world mutations; RPG Skill Tree depende de bridge real. QA Survival PENDING.

## Certificação técnica estática — Grow (25/10/2026)

**✅ `STATIC_TECHNICAL_CATALOG_ONLY` · ⛔ `mutating_hook=NOT_VERIFIED` · ⚠️ `physical_qa=NOT_TESTED`.** `ars_nouveau:glyph_grow` ↔ `EffectGrow` verificado como classe/ID no JAR `ars_nouveau-1.21.1-5.13.1.jar` SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`, não identidade de corpos de métodos. Fonte fixa `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`: [EffectGrow.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectGrow.java), [BlockUtil.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/BlockUtil.java), [SpellUtil.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/SpellUtil.java).

| Campo | Semântica fonte e fronteira de segurança |
|---|---|
| Geometria e targeting | `onResolveBlock(BlockHitResult,...)` itera `SpellUtil.calcAOEBlocks(shooter,hitPos,hit,spellStats)`. Somente `AugmentAOE` e `AugmentPierce` são compatíveis nesta classe. O helper orienta largura/altura/profundidade pela geometria do impacto, não por raio circular independente; não há target de entidade ofensivo ou DamageType. |
| Admissão server/claims | Para cada `blockpos` cria `new ItemStack(Items.BONE_MEAL,64)`, exige `BlockUtil.destroyRespectsClaim(shooter,world,blockpos)` **e** `world instanceof ServerLevel` antes de atuar. Esse item stack local **não equivale** a 64 bonemeals reais cobrados do player; custo vem do Ars e sua configuração. O preflight `destroyRespectsClaim` é chamado para a posição **original**. |
| Crescimento direto | Primeiro tenta `BoneMealItem.applyBonemeal(stack,world,blockpos,ANFakePlayer.getPlayer(serverLevel))`. Se retorna true, executa `world.levelEvent(1505,blockpos,0)` no servidor (partículas) e não tenta o fallback. O boolean indica admissão do caminho de bonemeal, **não confirmação universal** de que a planta cresceu um estágio concreto (growth pode depender de RNG/condições). |
| Fallback aquático adjacente | Se `applyBonemeal` retorna false, calcula `relative=blockpos.relative(rayTraceResult.getDirection())`, consulta `world.getBlockState(blockpos).isFaceSturdy(...,rayTraceResult.getDirection())` e chama `BoneMealItem.growWaterPlant(stack,world,relative,rayTraceResult.getDirection())` se a face for sólida. **Não repete explicitamente** `destroyRespectsClaim` para `relative` antes de alterar o destino adjacente. `world.levelEvent(1505,relative,0)` ocorre somente se o fallback retorna true. |
| Sucesso, custo e limites | `getDefaultManaCost()=70`, default Tier TWO; `AOE/Pierce` alteram candidatos/custo de processamento, sem cooldown individual provado. Cada `blockpos` tem stack local de 64; não inferir custo de 64 itens por target, Mastery por partícula, nem repetição gratuita por perk. `WorldEffectPolicy` do Black Arcana protege apenas seus próprios efeitos; Ars mantém responsabilidade de plant growth, fake player e mana. RPG Skill Tree segue provider de progressão via bridge real. |

**Gate QA:** claims na posição original e adjacente, crescimento aleatório por bonemeal, condições de água/fluid tags, sobreposição de AOE, cancelamentos de eventos, retorno de `growWaterPlant`, energia/mana carregada, efeitos de bonemeal de outros mods, multiplayer e chunks. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`. Stage 06.05/09 não promovido.
