# Ars Nouveau — Infuse

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_infuse`
- Display name: Infuse
- Default tier: 2
- Default mana cost: 30
- Compatible augments: AOE, Extend Time
- Default AOE limit: 1
- Default Extend Time limit: 1
- School: no explicit school override in the inspected class; do not infer one

## Provider-native behavior

Infuse obtains potion contents from Ars' potion-provider/inventory surfaces. Priority is: an `IPotionProvider` item or flask (one use consumed), then a normal PotionItem (one item consumed and bottle returned), then a nearby Potion Jar with more than 100 units (100 removed). Direct entity resolution applies the potion contents; AOE spawns a splash potion and Extend Time spawns a lingering potion.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:abjuration_essence` + `minecraft:glass_bottle` + `#c:rods/blaze`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns potion/flask/jar consumption and application for this spell. Black Arcana must not consume a second potion resource, duplicate the thrown potion, or infer an Ars spell school not declared by the exact source class.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectInfuse`).

## Engenharia para perks — caminho causal individual

- **Source exato:** [`EffectInfuse.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectInfuse.java), `com.hollingsworth.arsnouveau.common.spell.effect.EffectInfuse` no Ars Nouveau 5.13.1.
- **Escolha de destino:** `onResolve` com `getAoeMultiplier()>0` ou `getDurationMultiplier()>0` desvia para `spawnPotionEntity` ao invés de `onResolveEntity`; se AOE>0, seleciona `Items.SPLASH_POTION` mesmo quando Extend Time>0; caso contrário `LINGERING_POTION`. Sem esses stats, em entidade viva aplica conteúdo via `PotionUtil.applyContents(...)`.
- **Prioridade/consumo:** `getPotionData` busca primeiro `IPotionProvider` pela `PotionProviderRegistry` e faz `consumeUses(stack,1,shooter)`/return, então `PotionItem` (diminui 1 salvo infinite materials e devolve glass bottle) e finalmente `PotionJarTile` próximo com `getAmount()>100`, removendo 100. Cada rota altera um recurso Ars diferente; não consumi-los novamente em adapter RPG.
- **Admissão/cap:** `getCompatibleAugments` apenas AOE/Extend Time, cada um limite default 1. Não assume sucesso quando falta PotionContents; não gerar progresso de heal/damage a partir do spawn de frasco antes do impacto.
- **Perks:** duração nominal vem do potion payload e das regras da entidade splash/lingering, **não** diretamente do stat duration do Infuse; hooks por EffectResolve precisam ser avaliados na fase correta.
- **Estado:** ✅ classe/fórmulas source-pinned; ⚠️ outcomes downstream, config física e Survival pendentes; ⛔ nenhuma alteração por RPG Skill Tree implementada ou testada. Avaliar a interface `EffectResolveEvent.Pre` per-effect com clamps e causalidade.
