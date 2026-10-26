# Break

- Registry ID: `ars_nouveau:glyph_break`
- Source class: `EffectBreak`
- School: Elemental Earth
- Default tier: **1**
- Default mana: **10**
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Source-pinned behavior

Break destroys harvestable blocks in provider-calculated AOE/depth geometry. It checks Ars Nouveau's claim-respect helper and a provider break blacklist before mutation. Amplify/Dampen change harvest capability; Fortune and Extract synthesize Fortune/Silk Touch levels for the provider break operation; Sensitive switches the simulated tool to shears; Randomize may skip candidate blocks.

Compatible augments: Amplify, Dampen, Pierce, AOE, Extract, Fortune, Sensitive, Randomize. Default Fortune limit is 4 and Sensitive limit is 1. It is explicitly a default starter glyph.

## Acquisition / learning

- Provider-generated Glyph recipe: `minecraft:iron_pickaxe`.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **yes**. When runtime config preserves this default, Break is considered known without consuming a Glyph item.
- The generated recipe still exists; provider Glyph learning rejects the item while Break is currently configured as a starter.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars owns its break/loot/claim semantics. Any Black Arcana block destruction still requires `WorldEffectPolicy`, loaded-chunk/budget controls and Black Arcana causal ownership; Ars Break is not a world-policy bypass.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.

## Dossiê de engenharia para perks — causalidade exata

- **Código versionado:** [`EffectBreak.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectBreak.java), `com.hollingsworth.arsnouveau.common.spell.effect.EffectBreak` no Ars 5.13.1, método `onResolveBlock`.
- **Alvos/blocos:** `SpellUtil.calcAOEBlocks` recebe multiplicador AOE e contagem Pierce. Ajusta amplificação por Mining Fatigue, seleciona ferramenta simulada (shears com Sensitive; diamond pickaxe conforme tag/stack). **Loot:** Fortune até 4 e Extract/Silk Touch são aplicados à ferramenta simulada; Sensitive até 1. **Admissão:** bounds, `canBlockBeHarvested`, `BREAK_BLACKLIST`, `BlockUtil.destroyRespectsClaim` e `breakExtraBlock`. Randomize *pula* posição com probabilidade de teste `random.nextFloat()<count*0.25F`. Cada quebra aceita pode propagar `ShapersFocus.tryPropagateBlockSpell`. **Perks:** preservar claims, limites de work e causalidade de cada bloco, sem duplicar loot.
- **Limite de integração:** ✅ fonte estática identificada; ⚠️ parâmetros condicionados à configuração carregada; ⛔ nenhum hook externo de mutação verificado. Mana, targeting e settlement pertencem a Ars; RPG Skill Tree não substitui o resolver. Gameplay/Survival e adapter real: PENDING.

## Certificação técnica estática para perks — Break (2026-10-25)

**✅ `STATIC_TECHNICAL_CATALOG_ONLY` · ⛔ `mutating_hook=NOT_VERIFIED` · ⚠️ `physical_qa=NOT_TESTED`.** Identidade `ars_nouveau:glyph_break` ↔ `EffectBreak` fixada na auditoria de class/ID do publisher `ars_nouveau-1.21.1-5.13.1.jar` (SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`); a auditoria do binário **não prova equivalência de métodos**. Código upstream imutável `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`: [EffectBreak.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectBreak.java), [SpellUtil.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/SpellUtil.java), [BlockUtil.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/BlockUtil.java).

| Campo de perk/atributo | Caminho executável confirmado na fonte e limites |
|---|---|
| Entrada/alvos | `EffectBreak.onResolveBlock(BlockHitResult,...)`: não é evento de hit de entidade. Para `SpellUtil.calcAOEBlocks(shooter, hitPos, hit, getAoeMultiplier(), count(AugmentPierce))`, `SpellUtil` deriva largura com `1+floor(AOE)`, altura `1+ceil(AOE)` e profundidade `1+Pierce` (orientação por hit/caster, incluindo normalização para `FakePlayer`). **Não** é esfera, cubo garantido ou aumento independente do alcance de projectile. |
| Amplify e Dampen | Se `MobEffects.DIG_SLOWDOWN` existir, `spellStats.setAmpMultiplier(spellStats.getAmpMultiplier()-miningFatigue.getAmplifier())`; o efeito da debuff depende de `getAmplifier()`, não de um status genérico. Harvest gate usa `canBlockBeHarvested` com nível derivado de `BlockUtil.getBaseHarvestLevel(stats)=(int)(3+stats.getAmpMultiplier())`; `SpellUtil.isCorrectHarvestLevel` converte força para tiers de ferramenta. Não codificar “amplifica dano mágico” nem “apenas mais blocos”. |
| Item/loot simulado | `getStack` copia a mão principal, porém retorna `Items.DIAMOND_PICKAXE` se bloco inicial possui tag `BlockTagProvider.BREAK_WITH_PICKAXE`, ou se mão vazia. `spellStats.isSensitive()` troca para `Items.SHEARS`. `AugmentFortune` e `AugmentExtract` acrescentam Fortune e Silk Touch à stack simulada se o encantamento atual for menor; default limit Fortune=4, Sensitive=1. Não garantir que Fortune e Silk coexistam com regras vanilla/modpack do drop. |
| Gate de proteção e randomização | Cada candidato `pos1` é descartado se `world.isOutsideBuildHeight(pos1)` ou `world.random.nextFloat() < count(AugmentRandomize)*0.25F`. Depois valida `canBlockBeHarvested`, `!BlockUtil.destroyRespectsClaim(...)` e `BlockTagProvider.BREAK_BLACKLIST`. O claim preflight usa fake player e `BlockEvent.BreakEvent`, mas `BlockUtil.breakExtraBlock(...,true)` **também** publica `CommonHooks.fireBlockBreak`, podendo recusar a mutação. |
| Sucesso/propagação | Só se `BlockUtil.breakExtraBlock` retornar **true** chama `ShapersFocus.tryPropagateBlockSpell` para cada `BlockHitResult` secundário. O `bypassTool=true` nesse helper não implica bypass de `BlockEvent.BreakEvent` nem de GameMasterBlock/restrições adicionais. Drops, XP e efeitos de outros mods são responsabilidade desse caminho provider/NeoForge; não contar “tentativa de bloco” como loot/perk. |
| Custos/autoridade | Getter `getDefaultManaCost()=10` é default do glyph, não prova mana carregada, cooldown ou custo extra de cada bloco. Break tem `defaultedStarterGlyph()=true` como default, sujeito ao runtime config e aprendizado do provider. Nenhum `DamageType`, cooldown de spell individual ou mutator externo comprovado aqui. Black Arcana mantém `WorldEffectPolicy` sobre seus próprios world effects; Ars retém resolver, mana, claims, loot e propagação. RPG Skill Tree apenas progressão/Mastery via boundary real e causalidade única. |

**QA/provider gates:** confirmar classfile de método exato, runtime config dos augments, survival drops e Fortune/Silk Touch, claims com fake player, break callbacks repetidos, ShapersFocus, custo de blocos em larga AOE, save/restart e multiplayer. **Sem autorização para multiplicar drops, modificar raio ou evitar proteções externas por perk.** `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`.
