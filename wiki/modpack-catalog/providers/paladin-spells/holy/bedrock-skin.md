# Bedrock Skin

- **Status:** PRESENTE — released in current 1.1.1 line
- **ID:** `paladin_spells:bedrock_skin`
- **School:** Holy
- **Levels:** 1–10
- **Min rarity:** Rare
- **Cast:** Instant / 0 ticks
- **Mana neutral:** 30–165
- **Cooldown:** 25 s
- **Spell power neutral:** 5–23
- **Duration neutral:** 10–28 s
- **Role:** self-rooted defensive stance

## Source 1.1.1

`duration = 5 + getSpellPower`

Intended percentage reduction:

`normalized=(level-1)/(maxLevel-1)`

`exponent=1.2/(1+0.05*getSpellPower)`

`scaled=normalized^exponent`

`armorBonus=0.20*armor/(armor+100)`

`reduction=min(0.95, 0.10 + 0.50*scaled + armorBonus)`

The cast stores this value as `bedrock_skin_reduction`, applies `BEDROCK_SKIN_EFFECT` with amplifier `level-1`, creates `BedrockSkinEntity`, mounts the caster onto it and assigns the duration.

`BedrockSkinEntity` is invulnerable, disallows horizontal motion, permits vertical falling, anchors its passenger at its own coordinates and discards after duration or when it is no longer a vehicle. **Root/immobilization is therefore source-confirmed.**

`BedrockSkinEffect` independently declares an Armor modifier of `+10 ADD_VALUE` before amplifier semantics.

## Mitigation QA blocker

Repository search on the exact branch found `bedrock_skin_reduction` only where it is declared/written; no `LivingIncomingDamageEvent` or equivalent consumer was found. Thus the formula is an intended/stored value, but percentage mitigation settlement is **not source-confirmed as actually applied**.

Do not silently add the missing damage handler in a documentation/dedup bridge. Any fix must be explicit and runtime-tested.

## Mandatory matrix

- damage/heal: none directly;
- target/range: self;
- duration/scaling: formulas above, reduction cap 95%;
- immobilization: provider entity confirmed;
- armor modifier: +10 ADD_VALUE effect declaration confirmed; final amplifier behavior follows MobEffect runtime and needs live observation for exact displayed armor;
- acquisition/focus/ritual: specific route `NÃO VERIFICADO`;
- VFX/audio: self-cast animation; additional final assets `NÃO VERIFICADO`;
- dedup: occupies rooted heavy-defense Holy stance;
- QA/fail-closed: percentage mitigation cannot be claimed active without live proof.

## Source

Paladin branch `1.21@31f64ccdb39d062b21cc25d434cb62d6463b486e`, `BedrockSkinSpell`, `BedrockSkinEffect`, `BedrockSkinEntity`.
