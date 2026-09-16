# Mana Slash

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:mana_slash`
- **Iron's school:** Ender
- **Levels:** 1
- **Minimum rarity:** Rare
- **Cast type:** Instant
- **Cooldown:** 0 s
- **Resource:** Iron's mana
- **Crafting:** disabled by spell config
- **Looting:** explicitly disabled
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 50`
- `spellPowerPerLevel = 25`
- `baseManaCost = 30`
- `manaCostPerLevel = 0`
- `castTime = 0`

Raw damage is weapon-referenced rather than a fixed spell coefficient:

`max(1, referencedWeaponDamage * spellPowerPercent / 100) * providerDamageMultiplier`

For normal fallback casting, the referenced value comes from the caster's current weapon damage. For Swingcast Staff context, the provider captures the actual casting catalyst stack and resolves its displayed attack-damage modifiers through NeoForge's `ItemAttributeModifierEvent`.

## Provider/item binding

The guide describes Mana Slash as a latent Crystal Bladed Staff spell. The source confirms an item/cast-context path: if Swingcast context exists but the catalyst stack cannot be resolved, casting fails rather than silently using another weapon.

The cast creates a provider `MANA_SLASH_PROJECTILE` and stores the resolved damage on that projectile.

## Acquisition

The spell is explicitly non-craftable and non-lootable. Its registered presence must not be interpreted as ordinary scroll availability.

## Causality

The projectile and any later mana-orb consequences remain one provider cast chain. Black Arcana/RPG must not treat projectile spawn, hit and orb creation as separate player-authored spell casts.

## Deduplication

Occupies the **item-bound mana blade/projectile whose damage scales from the casting weapon's attack damage** niche.

## Confidence

`SOURCE-PINNED SPELL / EXACT ITEM-DAMAGE RESOLUTION+ACQUISITION EXCLUSIONS / PROJECTILE HIT+MANA-ORB NUMBERS+PACK MULTIPLIER QA PENDING`