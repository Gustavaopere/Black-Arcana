# Heal

- Registry ID: `ars_nouveau:glyph_heal`
- Source class: `EffectHeal`
- School: Abjuration
- Default tier: **2**
- Default mana: **50**
- Default heal config: **3.0** base + **3.0** per amplification unit
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Source-pinned behavior

Heals a living target, with randomized stats able to alter the heal amount. Healing a Player causes provider-side food exhaustion. Targets using inverted heal/harm semantics instead receive provider-owned magic damage for the same computed amount.

Compatible augments: Amplify, Dampen, Fortune, Randomize.

## Boundary

Ars Nouveau owns healing, food exhaustion, undead/inverted-heal damage and configured values. Black Arcana must not create duplicate healing settlement, damage procs or progression awards from the same provider event.

Status: `SOURCE-PINNED 5.13.1 / RUNTIME+CONFIG QA PENDING`.