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
