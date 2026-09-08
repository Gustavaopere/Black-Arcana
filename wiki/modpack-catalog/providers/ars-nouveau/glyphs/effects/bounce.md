# Ars Nouveau — Bounce

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_bounce`
- Display name: Bounce
- School: Abjuration
- Default tier: 1
- Default mana cost: 50
- Compatible augments: Extend Time, Reduce Time (`glyph_duration_down`), Amplify
- Source default duration: 30 s
- Source default Extend Time increment: 8 s

## Provider-native behavior

Applies Ars' Bounce effect, causing targets to bounce upward after falling. Provider documentation states that amplification preserves additional forward-facing motion on each bounce.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:abjuration_essence` + `#c:slime_balls` ×3.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns this bounce/mobility status. Black Arcana should not add a generic duplicate bounce buff or take over provider motion-state interpretation.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectBounce`).
