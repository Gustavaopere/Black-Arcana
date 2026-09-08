# Conjure Magelight

- Registry ID: `ars_nouveau:glyph_light`
- Source class: `EffectLight`
- School: Conjuration
- Default tier: **1**
- Default mana: **25**
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Source-pinned behavior

On blocks, creates provider light blocks after claim/bounds/collision checks; without a duration modifier the light is persistent, while time modification selects the temporary-light block path. Amplify/Dampen adjust provider light level. On living entities it applies Night Vision and, subject to caster/Sensitive conditions, Glowing. Sensitive can apply the spell color to Glowing.

Compatible augments: Amplify, Reduce Time, Dampen, Extend Time, Sensitive. Amplify and Sensitive are limited to 1 by default.

## Boundary

Ars Nouveau owns Magelight blocks, potion effects, color presentation and provider config. Black Arcana lighting/world placement must remain policy-controlled and must not duplicate persistent provider lights without a distinct requirement.

Status: `SOURCE-PINNED 5.13.1 / RUNTIME+CONFIG QA PENDING`.