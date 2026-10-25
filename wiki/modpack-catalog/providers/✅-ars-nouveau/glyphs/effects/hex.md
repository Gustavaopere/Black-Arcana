# Ars Nouveau — Hex

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_hex`
- Display name: Hex
- School: Abjuration
- Default tier: 3
- Default mana cost: 100
- Compatible augments: Extend Time, Reduce Time (`glyph_duration_down`), Amplify
- Default Amplify limit: 4
- Source default duration: 30 s
- Source default Extend Time increment: 8 s

## Provider-native behavior

Applies Ars' `Hex` effect. Provider documentation states that Hex increases damage taken while the target is poisoned, withered, burning or frozen, and halves Mana Regeneration and healing while active. Amplify increases effect level; Time augments adjust duration.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:abjuration_essence` + `minecraft:fermented_spider_eye` + `minecraft:blaze_rod` ×3 + `minecraft:wither_rose`.
- Source-default recipe XP: **160 XP** (Tier III).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau already owns this conditional vulnerability/healing/mana-suppression curse. Black Arcana curse content must be mechanically distinct and must not double-apply Hex's provider-local amplification or mana/healing penalties.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectHex`).

## Engenharia para perks — caminho causal individual

- **Source exato:** [`EffectHex.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectHex.java), `com.hollingsworth.arsnouveau.common.spell.effect.EffectHex` no Ars Nouveau 5.13.1.
- **Aplicação:** `onResolveEntity` verifica `LivingEntity` e chama `IPotionEffect.applyConfigPotion(living,ModPotions.HEX_EFFECT,stats)`; a classe `EffectHex` não implementa dano instantâneo nem metade da cura diretamente.
- **Duração/amplificador:** defaults `addPotionConfig(30)` e `addExtendTimeConfig(8)`: no helper, `ticks=30*20+8*(int)(20*getDurationMultiplier())` com configs default, amplifier `(int)getAmpMultiplier()`. Limite default Amplify 4.
- **Efeito downstream:** vulnerability, mana regeneration e healing suppression descritos no provider são implementados em `HEX_EFFECT`/consumidores; não inventar uma fórmula local de +damage ou redução de heal sem inspecionar esses caminhos.
- **Perks:** status aplicado é distinto dos ataques que dispararem aumento de dano no futuro. Deduplicar Mastery pelo cast raiz, não por cada dano periódico.
- **Estado:** ✅ classe/fórmulas source-pinned; ⚠️ outcomes downstream, config física e Survival pendentes; ⛔ nenhuma alteração por RPG Skill Tree implementada ou testada. Avaliar a interface `EffectResolveEvent.Pre` per-effect com clamps e causalidade.

## Certificação estática: status e Dispel — 25/10/2026

**✅ Ficha técnica source-pinned completa somente para planejamento; ⛔ `mutating_hook=NOT_VERIFIED` e ⚠️ `physical_qa=NOT_TESTED`.** Certificação documental não prova que existe perk implementada ou modpack validado.

| Campo | Contrato e limites exatos |
|---|---|
| Identidade, classe e release | `ars_nouveau:glyph_hex`, `EffectHex`, Ars Nouveau **5.13.1**, tier III. [Source no commit imutável](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectHex.java); [identidades no publisher JAR](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). |
| Ação, causalidade e efeitos downstream | `onResolveEntity` retorna imediatamente se o hit não for `LivingEntity`; caso contrário aplica **ModPotions.HEX_EFFECT** via `IPotionEffect.applyConfigPotion`. O texto de `getBookDescription()` afirma aumento de dano recebido quando poison, wither, fire ou frozen e redução de recuperação de mana e cura; **esses cálculos NÃO estão implementados no método EffectHex.onResolveEntity** e requerem prova separada no consumidor do HEX_EFFECT antes de definir fórmula ou hook. |
| Parâmetros, caps e augments | `buildConfig` define `POTION_TIME=30` s, `EXTEND_TIME=8`; getters fallback 30/8. `IPotionEffect`: `ticks=600+8*stats.getDurationInTicks()` com config default e `amplifier=(int)stats.getAmpMultiplier()`. `getPotionAugments()` permite augments potion/Time; `addDefaultAugmentLimits` define **4 Amplify** por default. Não converter texto de livro em percentual ou escalar de dano fixo. |
| Target, geometria, dano e duração | `EntityHitResult` de `LivingEntity` apenas; sem seleção de área, projétil ou dano/tempo aplicado autonomamente além do HEX_EFFECT; destinatário final da Form e o consumidor de debuffs definem as consequências. Descrição do Hex não valida debuffs em todos os mobs ou integração de mana não-Ars. |
| Custos e aprendizagem | Mana default **100**, tier III, recipe datagen `ars_nouveau:abjuration_essence` + `minecraft:fermented_spider_eye` + `minecraft:blaze_rod` ×3 + `minecraft:wither_rose`, XP default **160**, starter default **não**; [aquisição 85/85](../../ACQUISITION.md). Cooldown, pagamento e admissão pertencem à magia composta/provider; tempo de status não é cooldown. |
| Authority, eventos e integração | Não multiplicar dano e cura novamente em Black Arcana se HEX_EFFECT já os modificou; não aplicar cast a cada evento downstream nem interferir na mana do provider. O contrato de perks sobre status ou eventos de heal/damage ainda não está homologado. RPG Skill Tree é sibling de progressão/perks apenas por contrato comprovado. Black Arcana conserva seus próprios casting, Corruption, Strain, WorldEffectPolicy e causalidade, não assume a semântica nativa de Ars. |
| Evidência/validação | `PINNED_SOURCE_PLUS_SHA_EXACT_BINARY_IDENTITY`: source `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` e publisher `ars_nouveau-1.21.1-5.13.1.jar` SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`, **prova compilada somente de ID/classe**. Config instalada, correspondência exata do bytecode de todos os métodos, consumer behavior e clientes/modpack físicos: **não verificados**; `physical_qa=NOT_TESTED`. |

**Invalidação:** mudança de JAR, source, receitas, configs ou listeners de eventos exige reauditoria. Nenhum spell, hook, cast, status mutável ou cap de gameplay foi implementado neste checkpoint.
