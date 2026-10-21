# Ars Additions — Retaliate

Status: `SOURCE-PINNED 21.3.0 / DESCRIPTION-PATH DIVERGENCE / RUNTIME QA PENDING`

- Provider: Ars Additions
- Type: Form / `AbstractCastMethod`
- Registry path: provider-generated `glyph_retaliate`
- Display name: Retaliate
- Default tier: III
- Default mana cost: 25
- Compatible augments: none
- Source class: `MethodRetaliate`

## Provider-native behavior

Every cast entry point delegates to the same `cast(caster, resolver)` method. The executable method obtains `caster.getKillCredit()`, rejects null/self, and resolves the remaining spell directly against that living entity through the Ars resolver.

## Description divergence

The provider description states that the target is the last entity that dealt damage to the caster and that the damage must have occurred within five seconds. The inspected `MethodRetaliate` executable path does **not** perform an explicit age/timestamp check; it uses `getKillCredit()` directly.

Phase 2Q therefore does not claim a verified five-second runtime window. Whether Minecraft/provider state elsewhere naturally expires in the intended interval must be observed in runtime before a bridge relies on it.

## Black Arcana boundary

This is provider-owned reactive targeting. Black Arcana must not observe Retaliate and then independently resolve/settle the same child spell. If a future Black Arcana revenge/retaliation mechanic exists, its identity must be materially different and remain inside the canonical Black Arcana cast pipeline.

Source checkpoint: `Jarva/Ars-Additions@91f102a90dc058cf40e4eac5a67a881e48b856b4` (`MethodRetaliate`).

## Engenharia para perks — execução exata 21.3.0

- **Classe pinada:** [`MethodRetaliate.java`](https://github.com/Jarva/Ars-Additions/blob/91f102a90dc058cf40e4eac5a67a881e48b856b4/src/main/java/com/github/jarva/arsadditions/common/glyph/MethodRetaliate.java); commit `91f102a90dc058cf40e4eac5a67a881e48b856b4`, versão de source 21.3.0.
- **Actual selector:** `cast` reads `LivingEntity lastHurtBy=caster.getKillCredit()`; returns FAILURE for null or self, otherwise calls `resolver.onResolveEffect(caster.level(), new EntityHitResult(lastHurtBy))` and returns SUCCESS. It does **not** check elapsed damage time or a timestamp in this class.
- **Entrypoints:** all `onCast`/block/entity overloads share this selector; UseOnContext path rejects null player. Default mana 25, tier III, compatible augments empty.
- **Description mismatch:** UI describes a 5-second revenge target. This exact implementation lacks that explicit window: survival / vanilla kill-credit lifecycle must be measured. **Perks:** bypassing the selector with RPG's last-damage cache would create a second targeting authority and potentially extend the intended window.
- **Estado:** ✅ classe versionada e entrada source-audited; ⚠️ diferença host Ars 5.13.1 versus build baseline 5.11.2, config instalada, helpers/callback, runtime e Survival ainda não aprovados; ⛔ nenhuma perk RPG/adaptador Black Arcana foi implementado ou testado. Não duplicar mana, Source, inventário ou resolução do provider.
