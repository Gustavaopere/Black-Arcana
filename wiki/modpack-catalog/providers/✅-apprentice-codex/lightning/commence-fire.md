# Commence Fire

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:commence_fire`
- **Iron's school:** Lightning
- **Levels:** 1–5
- **Minimum rarity:** Uncommon
- **Cast type:** Long + recast weapon lifecycle
- **Cooldown:** 12 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 30`
- `baseManaCost = 100`
- `manaCostPerLevel = 30`
- `castTime = 30 ticks`
- summoned/recast lifetime: **200 ticks / 10 s**
- aim range: **64 blocks**

Raw shot damage:

`3.5 * (spellPower / 100)`

then multiplied by `DamageMultiplierKey.COMMENCE_FIRE`.

Maximum activation/recast count:

`min(10, 3 + round(2 * spellPower / 100))`

Headshot multiplier percentage:

`min(500, 200 + round(30 * spellPower / 100))`

## Recast and firing semantics

The initial long cast summons the rifle. Subsequent use enters the provider's recast path; firing uses a fixed base recast cast time of **10 ticks / 0.5 s**, with the provider's Magi Agent Suit boots helper allowed to modify that path.

Recast is rejected while the summoned rifle is in recoil. Damage/headshot values are recalculated immediately before the shot so temporary cast-time/Focus Staffbow spell-power context is reflected at firing time.

The rifle resolves assisted aim, determines whether the hit is a headshot, settles damage through the provider entity, then emits the matching miss/block/entity firing result.

## What it does

Provider guide semantics: summons a magical rifle that follows the caster; using the spell again unleashes a powerful shot.

One summon plus its recasts remains one provider lifecycle. Black Arcana/RPG progression must not count the initial summon and every internal rifle callback as unrelated spell identities.

## Acquisition

Registered through Iron's spell registry. Exact 0.9.7.1 scroll/loot availability remains in the provider-wide acquisition audit.

## Deduplication

Occupies the **summon persistent rifle → bounded recast precision shot/headshot** niche. Generic magical rifle or remote follow-up shot designs overlap directly.

## Confidence

`SOURCE-PINNED SPELL + RECAST PATH / HEADSHOT GEOMETRY + PACK CONFIG MULTIPLIER RUNTIME QA PENDING`