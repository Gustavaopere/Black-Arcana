# Bulwark

- **Status:** PRESENTE — released in Paladin Spells 1.1.1
- **ID:** `paladin_spells:bulwark`
- **School:** Holy
- **Levels:** 1–10
- **Min rarity:** Rare
- **Cast:** Instant / 0 ticks
- **Mana neutral:** 30–120
- **Cooldown:** 45 s
- **Spell power neutral:** 15–60 before generic/Holy/config multipliers
- **Role:** self armor amplification

## Source 1.1.1

`bonusPercent = getSpellPower(level,caster)`

`amplifier = round(bonusPercent*10)`

`durationSeconds = min(5 + 15*getSpellPower/100, 35)`

With neutral power this is 7.25–14 s. The spell applies `BULWARK_EFFECT` to self and uses the Bulwark sound plus `SELF_CAST_ANIMATION`.

## Authority / QA blocker

`BulwarkEffect` registers an `Attributes.ARMOR` modifier with operation `ADD_MULTIPLIED_TOTAL` but amount **0.0**. The audited 1.21 branch contains no separate Bulwark damage/armor handler that compensates for this.

Therefore:

- intended semantic role = confirmed;
- spell formula/amplifier/duration = confirmed;
- actual armor increase in installed gameplay = `NÃO VERIFICADO / LIVE QA REQUIRED`.

Black Arcana must not duplicate an armor multiplier to “fix” it silently; a correction belongs in an explicit provider compat/fix workstream after runtime proof.

## Mandatory matrix

- damage/heal: none directly;
- target/range: self;
- duration: formula above;
- scaling/caps: spell power multiplier; hard duration cap 35 s;
- acquisition/loot/craft/focus/ritual: specific route `NÃO VERIFICADO`;
- PvP/boss/summon: not direct targets;
- VFX/audio: sound + self-cast animation confirmed; final particles/assets `NÃO VERIFICADO`;
- dedup: occupies temporary Holy armor-amplification signature;
- fail-closed: do not treat armor gain as functioning authority until QA proves it.

## Source

- Paladin branch `1.21@31f64ccdb39d062b21cc25d434cb62d6463b486e`.
- 1.1.1 changelog confirms Bulwark cooldown correction to 45 s and duration nerf.
