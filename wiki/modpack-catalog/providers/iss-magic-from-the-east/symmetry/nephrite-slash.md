# Nephrite Slash

- **ID:** `iss_magicfromtheeast:nephrite_slash`
- **School:** Symmetry
- **Levels:** 1–5
- **Min rarity:** Common
- **Cast:** Instant
- **Mana neutral:** 40–120
- **Spell power neutral:** 4–12
- **Cooldown:** 20 s
- **Primary damage:** `getSpellPower + weaponDamage`

## Contract

Performs a short forward slash sampled across four positions. Valid alive/pickable/visible entities receive provider spell damage; successful hits have invulnerability time set to 0 and trigger post-attack enchantment effects.

Then it creates a ground-following sequence of up to **8 Nephrite crystals**:

- delayed by crystal index;
- progressively larger;
- ordinary crystals use **30%** of primary damage;
- terminal/biggest crystal uses **75%**.

## Public naming boundary

Older public prose described a “Qigong Controlling” mechanic very similar to this slash+crystal behavior, but the current active registry has `nephrite_slash` while `QigongControllingSpell` is commented out. The canonical current name/ID is therefore **Nephrite Slash** unless current runtime language data proves a display alias.

## Dedup

This already owns weapon-scaled Symmetry slash + delayed crystal-line follow-up. Do not duplicate primary slash, iFrame reset or crystal damage.

## Source

`NephriteSlashSpell.java`, registry 1.1.5.
