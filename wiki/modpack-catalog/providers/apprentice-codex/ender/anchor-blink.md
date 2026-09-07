# Anchor Blink

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:anchor_blink`
- **Iron's school:** Ender
- **Levels:** 1
- **Minimum rarity:** Epic
- **Cast type:** Long
- **Cooldown:** 30 s
- **Resource:** Iron's mana
- **Crafting:** disabled
- **Looting:** disabled
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 400`
- `spellPowerPerLevel = 200`
- `baseManaCost = 80`
- `manaCostPerLevel = 0`
- `castTime = 10 ticks`
- effective cast time deliberately ignores cast-time reduction
- raw dagger damage: `spellPower / 100 * providerDamageMultiplier`
- projectile speed: `1.8`
- maximum anchor-establishment range: `min(128, 16 * spellPower / 100)` blocks

At the one registered level and default spell power, the source-derived maximum anchor range is **64 blocks** before external spell-power modifiers.

## Item prerequisite

The cast requires the generated **Spell-Sided Edge mirror** in the off hand. If the mirror is absent, provider pre-cast validation fails with an action-bar message.

The spell is explicitly non-craftable/non-lootable and is therefore an item-bound capability rather than an ordinary survival scroll.

## Cast and anchor lifecycle

On successful server cast, the provider spawns an owner-linked `AnchorBlinkDaggerEntity`, stores damage and maximum range, and launches it along the caster's look direction.

The public guide describes a short-lived anchor behavior: after the reverse-edge dagger embeds, the caster can satisfy the provider jump condition to blink near it within roughly three seconds. Casting also deactivates the provider's Edge Dancer state.

Exact post-impact teleport safety/placement is owned by the dagger/anchor event path and remains separate from the spell-class coefficients above.

## Causality

Dagger throw, anchor establishment, teleport and Edge Dancer cleanup belong to one provider interaction chain. Black Arcana must not add a second teleport settlement or treat the eventual blink as a fresh provider cast.

## Deduplication

Occupies the **item-bound thrown anchor dagger followed by short-window positional blink** niche.

## Confidence

`SOURCE-PINNED SPELL / EXACT ITEM GATE+DAMAGE+PROJECTILE+RANGE / IMPACT-ANCHOR TELEPORT SAFETY+3s WINDOW INTERNALS+RUNTIME QA PENDING`