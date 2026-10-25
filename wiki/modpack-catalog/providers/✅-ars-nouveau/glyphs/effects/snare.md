# Ars Nouveau — Snare

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_snare`
- Display name: Snare
- School: Elemental Earth
- Default tier: 1
- Default mana cost: 100
- Compatible augments: Extend Time, Reduce Time (`glyph_duration_down`)
- Source default base duration: 8 s
- Source default Extend Time increment: 1 s

## Provider-native behavior

Snare applies Ars' Snare mob effect to living targets, immediately zeroes their motion, and supports duration adjustment through Time augments. When used on an Ars `EnchantedFallingBlock`, it attempts to ground/place the block and propagates block-shaping spell behavior.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:earth_essence` + `minecraft:cobweb` ×4.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns this immobilization/status effect and its block-shaping interaction. Black Arcana should not double-apply movement suppression or replay block settlement when Ars is causal.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectSnare`).

## Dossiê de engenharia para perks — causalidade exata

- **Código versionado:** [`EffectSnare.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectSnare.java), `com.hollingsworth.arsnouveau.common.spell.effect.EffectSnare` no Ars 5.13.1, método `onResolveEntity`.
- **Ramo entidade viva:** `onResolveEntity` usa `applyConfigPotion(...,ModPotions.SNARE_EFFECT,spellStats)`, zera deslocamento `setDeltaMovement(0,0,0)` e marca `hurtMarked=true`. **Ramo block entity:** se alvo é `EnchantedFallingBlock`, chama `groundBlock(true)` e propaga `ShapersFocus.tryPropagateBlockSpell` quando um bloco é posicionado. **Tempo:** `addPotionConfig(8)`, `addExtendTimeConfig(1)` no default; Time augments Extend Time/Duration Down. **Perks:** status e forçar block settlement são resultados distintos; não repetir alteração de velocidade em ticks como se fosse cast novo.
- **Limite de integração:** ✅ source pin da lógica local, ⚠️ execução auxiliares/config dependem do provider real; ⛔ hook externo de mutação não comprovado. Black Arcana só governa suas world mutations; RPG Skill Tree depende de bridge real. QA Survival PENDING.

## Fórmula de duração — IPotionEffect exato

- **Helpers:** [`IPotionEffect.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/IPotionEffect.java), [`SpellStats.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java).
- **Snare pelo helper `IPotionEffect`:** `ticks=baseDurationSeconds*20+durationBuffSeconds*stats.getDurationInTicks()`; com defaults `base=8`, `extend=1`, fica `ticks=160+(int)(20*durationMultiplier)`, amplifier `(int)getAmpMultiplier()` (mas somente Time augments são listados como compatíveis). `setDeltaMovement(0,0,0)` atua na resolução; bloqueio subsequente pertence a `SNARE_EFFECT`.
- **Estado:** fórmula source-pinned; runtime e configuração carregada ainda exigem QA. Nenhuma alteração externa do MobEffect é autorizada apenas por esses getters.

## Auditoria de contrato estático — mobilidade e controle (25/10/2026)

**✅ Contrato técnico source-pinned completo desta ficha; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** A marca ✅ aqui é de documentação estática, não de comportamento comprovado no cliente ou integração executável.

| Campo necessário à perk | Comportamento real no source fixo e condicionamentos |
|---|---|
| Identidade | Ars Nouveau `5.13.1`, `ars_nouveau:glyph_snare`, classe `EffectSnare`, escola Elemental Earth, tier I. [Fonte exata](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectSnare.java), [IDs binários SHA-exatos](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). |
| Execução, causalidade e recebedor | `onResolveEntity` com `LivingEntity` aplica `ModPotions.SNARE_EFFECT` usando `IPotionEffect.applyConfigPotion`, zera movimento imediatamente por `setDeltaMovement(0,0,0)` e marca `hurtMarked`. **Outro ramo**, com alvo `EnchantedFallingBlock`, chama `groundBlock(true)` e só propaga `ShapersFocus.tryPropagateBlockSpell` se o retorno `BlockPos` for não nulo. O segundo caminho é tentativa de assentamento de block-entity, **não** aplicação do buff de imobilização. |
| Parâmetros, fórmulas e caps | `buildConfig`: tempo base **8 s** e bônus Extend Time **1 s** por `stats.getDurationInTicks()` no helper. Fórmula com defaults `ticks=8×20+1×stats.getDurationInTicks()`; amplificador do helper é `(int)getAmpMultiplier()` e somente Extend Time/Reduce Time compatíveis. `getBaseDuration` fallback 8 e `getExtendTimeDuration` fallback 1. `SNARE_EFFECT` controla efeitos persistentes posteriores à resolução, não outro cast do mesmo glyph. |
| Alvo/target, geometria, projétil, dano e duração | Somente `EntityHitResult` no source dessa classe: `LivingEntity` recebe snare/status/motion e `EnchantedFallingBlock` tenta `groundBlock`. Não há método `onResolveBlock` próprio para blocos estáticos; não confundir com conversão de blocos por Leap/Launch/Pull. Sem projétil, alcance, DamageType ou AoE próprios. |
| Custos, aprendizado e cooldown | Mana default **100**, tier I, recipe default `ars_nouveau:earth_essence` + `minecraft:cobweb` ×4, XP default **27**, starter default **não**. [Acquisition compilada 85/85](../../ACQUISITION.md). Custo final/cooldown/consumidor da magia composta continuam no Ars. |
| Integração/authority | Não multiplicar Mastery por tick da imobilização, nem refazer o assentamento de falling blocks depois de resposta `null`. Custo e persistência do status são Ars-owned; integração com RCA/Strain Black Arcana e RPG Skill Tree exige contrato real. O RPG Skill Tree fornece perks/progressão mas não assume o `SpellResolver` Ars; Black Arcana só controla seu casting, world policy e riscos internos. APIs de mutação externa não estão comprovadas para este ramo. |
| Validação/proveniência | `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`; publisher `ars_nouveau-1.21.1-5.13.1.jar` SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd` para **ID e classe de registro**, não equivalência de todo classfile/source. Config efetiva, edge-cases, claims, multiplayer e modpack QA **NOT_TESTED**. |

**Gate explícito:** alteração de versão/config, eventos, claims, targeting ou vector motion exige revalidação. Sem Mastery por packet/partícula/tick ou bloco secundário; sem segunda mana, reexecução de efeitos ou Stage promovido.
