# Capability Matrix Delta — Ars Sable 1.1.2

Status: `EXACT SOURCE-PINNED SPATIAL BRIDGE / CURRENT SABLE 2.0.5 QA OPEN`

| Capability | Exact 1.1.2 evidence | Black Arcana consequence |
|---|---|---|
| Ars Source Jar visibility from moving Sable sublevels | SourceJar mixin registers original Ars Source tile through `ISpecialSourceProvider`; current position is projected out of the sublevel | Ars Source remains single authority; BA must not mirror or settle Source a second time |
| Moving Storage Lectern addresses | persistent tracking UUID + tracked positions + moved handler cache reconstruction and stale transfer-task clearing | provider owns moving Ars storage addressing; BA must not maintain a competing handler/location map |
| Ars Warp Portal destination projection | same-dimension teleport, cross-dimension DimensionTransition and client WarpPosition coordinates are projected through provider helpers | one provider teleport settles once; BA must not issue a second displacement |
| Warp Scroll / Stable Warp Scroll sublevel targets | dedicated mixins and WarpSublevelTargetData; 1.1.2 specifically fixes unloaded-sublevel destination errors | provider owns its warp target bridge; BA spatial domains need independent identity and server safety contracts |
| Planarium across assembly/disassembly | Planarium/DimBoundary adapters; release changelog states bound connections persist across assembly | no BA duplicate persistence for the same Planarium relation |
| Ars logistics/pathfinding in Sable spaces | Bookwyrm, selected path navigation, Whirlisprig and Wixie mixins | support is provider-targeted; do not generalize to arbitrary mobs or BA entities |
| Ars flying items/follow projectiles | explicit entity mixins/helpers | Ars causal spell/projectile identity remains Ars; avoid duplicate impact/proc settlement |
| Scrying/camera/render projection | common tracking plus five client-only mixins | visuals remain non-authoritative; BA target validation stays server-side |
| Provider-owned magic content | no gameplay block/item registration and no spell/glyph/ritual registration in exact tree | no spell-school/domain is consumed merely by the presence of Ars Sable |
| Provider-owned network protocol | registrar `2` exists but registers zero payload types | do not invent network authority from generic packet helper methods |

## Semantic disposition

Ars Sable occupies the **compatibility problem of making existing Ars systems spatially coherent inside Sable sublevels**. It does not occupy a new magic school.

Black Arcana may still implement forbidden spatial magic, but cannot disguise duplicated provider functionality as a new spell. Any BA displacement must have its own cast identity, costs, Corruption/Strain/hazards, bounded target validation and world-safety semantics, while avoiding duplicate projection/teleport when interacting with provider-owned Ars/Sable systems.

## Version-risk disposition

The source runtime ranges accept Sable `[1.0,)`, but exact build target was 1.2.2 and physical runtime is 2.0.5. That is a QA gate, not an inferred failure and not an inferred PASS.
