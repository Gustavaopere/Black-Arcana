# Ars Delight 2.2.2 — effects and event semantics

Status: `SOURCE FORMULAS CLOSED / CURRENT-HOST EVENT-ORDER QA OPEN`

## `blast_resistance`

On `LivingDamageEvent.Pre`, only explosion-tagged damage is modified.

For effect amplifier `a`:

```text
multiplier = max(0, 1 - (a + 1) * 0.2)
newDamage = incomingDamage * multiplier
```

This is provider-owned damage modification. Black Arcana must not apply a second copy of the same reduction to the same hit.

## `flourishing`

On `LivingHealEvent`, if the healed entity has Flourishing, source obtains Ars mana through `CapabilityRegistry.getMana(entity)`.

For amplifier `a`:

```text
factor = 2^a
gain = healedAmount / maxHealth * maxMana * factor
```

The provider then calls `cap.addMana(gain)`.

Authority consequence: this is an Ars-mana credit caused by one heal event. Black Arcana/RPG observers must not produce a second mana credit or reinterpret the gain as BA mana.

## `synchronized_shield`

The same heal event can add absorption when the entity has Synchronized Shield.

```text
factor = 2^a
cap = maxShieldingAbsorption * factor
newAbsorption = min(cap, oldAbsorption + healedAmount * factor)
```

Source server config default for `maxShieldingAbsorption` is `8.0`. `ShieldingEffect` also adds an `Attributes.MAX_ABSORPTION` modifier using the same configured base × `2^a` formula.

Do not replay heal→absorption through a second BA proc path.

## `wilden`

Wilden hooks three Ars calculations.

### Spell damage

On `SpellDamageEvent.Pre`:

```text
damage *= 1 + (a + 1) * wildenSpellDamageBonus
```

Default `wildenSpellDamageBonus = 0.2`.

### Max mana

On `MaxManaCalcEvent`:

```text
maxMana *= 1 + (a + 1) * wildenMaxManaBonus
```

Default `wildenMaxManaBonus = 0.2`.

### Mana regeneration

On `ManaRegenCalcEvent`:

```text
regen *= 1 + (a + 1) * wildenManaRegenBonus
```

Default `wildenManaRegenBonus = 0.2`.

All three are Ars/provider calculations. BA must not mirror the stats into a parallel ledger or multiply the provider result again unless a separately designed BA mechanic explicitly composes through a real supported hook.

## `freezing_spell`

On `SpellDamageEvent.Post`, if the caster has Freezing Spell and the target is a `LivingEntity`, source adds Ars Nouveau's `FREEZING_EFFECT` to the target using the Freezing Spell effect's current duration and amplifier.

This child status is causally downstream of the Ars spell-damage event and must not be treated as a fresh independent cast/proc.

## Optional `lightning_curse`

Ars Elemental compatibility registers `lightning_curse`. On `SpellDamageEvent.Post`, a caster carrying it applies Ars Elemental `LIGHTNING_LURE` to a living target for 20 ticks using the curse amplifier.

Ars Elemental 0.7.10.1 is present physically, but exact current-host behavior remains runtime QA.

## Event/dedup risks

- A single heal may legitimately trigger both Flourishing and Synchronized Shield if both effects are present; that is provider behavior, not double-processing by itself.
- External mods that synthesize/re-fire healing or spell-damage events can create apparent double-dips; reproduce current runtime before classifying a bug.
- Freezing/Lightning child effects must retain caster/event causal identity if BA observers later consume them.
- Backlash must not be inferred from these provider effect events unless a real Black Arcana cast/hazard contract explicitly attributes the damage/action to a BA root cast.
