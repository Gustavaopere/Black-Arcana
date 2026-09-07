# Rift Walker

- **ID:** `discerning_the_eldritch:rift_walker`
- **School:** Eldritch
- **Levels:** 1–5
- **Rarity:** Legendary
- **Cast:** Instant
- **Mana neutral:** 35–75
- **Spell power neutral:** 12–32
- **Cooldown:** 12 s
- **Rift radius:** 3
- **Rift damage:** `0.15 * getSpellPower`
- **True invisibility:** 60 ticks / 3 s

## Contract

`onServerPreCast` creates an `UnstableRiftEntity` at the caster **before** teleport. `onCast` resolves a teleport target, teleports, resets fall distance, applies Iron's `TRUE_INVISIBILITY` for 60 ticks, then creates a second unstable rift at the destination.

If raycast hits a LivingEntity, the spell attempts positions around that target and faces the caster toward it after teleport; otherwise it uses Iron's teleport-location helper.

Recast window = 100 ticks. Default recast count is 1; `RIFT_RIPPER_EMBLEM` or `KINGS_EFFIGY` raises it to 3.

Distance = `softCapFormula(entityPowerMultiplier) * (base-level spellPower / 2)`.

## Dedup / authority

The identity is **teleport with origin+destination delayed rifts + temporary true invisibility + item-gated recasts**. Do not replace it with a generic teleport observer or create extra rifts in a bridge.

UnstableRift hit timing/lifetime/friendly-fire are entity-native / `NÃO VERIFICADO` here.

## Source

`RiftWalkerSpell.java`, branch `1.21@7bbd81f...`.
