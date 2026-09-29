# Magic Scroll

Status: `CONDITIONAL / NOT STRICT-COUNTED`

## Identity

Tombstone castable action family: generic magic-effect cast wrapper.

## Exact 9.5.6 evidence

`ItemMagicScroll`; stored `MobEffectInstance`, target/nearby-entity selection and `EffectHelper.addEffect(...)`.

## Semantic accounting

Current strict contribution: **+0 until deployed `allowMagicScroll` is observed true**. If authoritatively enabled, this card contributes at most **+1**.

## Authority / boundary

Tombstone owns execution, costs, teleport/summon/effect/progression settlement. Black Arcana must not synthesize a second action or bypass provider eligibility.

Eligibility gate: `allowMagicScroll`.

Underlying status-effect variants are metric-excluded and are not counted again.
