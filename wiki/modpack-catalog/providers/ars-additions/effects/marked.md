# Ars Additions — Marked

Status: `1/1 REGISTRY SOURCE-PINNED / EFFECT-INTERNAL SEMANTICS AUDIT PENDING`

- Registry id: `ars_additions:marked`
- Registry class: `AddonEffectRegistry`
- Effect class: `MarkedEffect`

`EffectMark` applies this provider effect to marked players for a server-configured duration; the source default is 300 seconds with a 0–900 second configured range.

The effect is provider-owned presentation/state associated with Reliquary Mark/Recall. Black Arcana must not treat the presence of `marked` alone as proof that a Black Arcana mark, target lock or progression event occurred.

Source checkpoint: `Jarva/Ars-Additions@91f102a90dc058cf40e4eac5a67a881e48b856b4` (`AddonEffectRegistry`, `EffectMark`, `ServerConfig`).
