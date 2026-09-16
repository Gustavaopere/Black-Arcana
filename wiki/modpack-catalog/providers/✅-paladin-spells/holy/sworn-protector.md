# Sworn Protector

- **Status:** PRESENTE — current 1.1.1 changelog removes WIP from released spells; stale README wording is not current authority
- **ID:** `paladin_spells:sworn_protector`
- **School:** Holy
- **Levels:** 1–10
- **Min rarity:** Rare
- **Cast:** Instant / 0 ticks
- **Mana neutral:** 30–165
- **Cooldown:** 35 s
- **Spell power neutral:** 10–55
- **Range source:** 36–90 blocks
- **Duration neutral:** 17–26 s
- **Role:** redirect a percentage of nearby player damage to protector

## Formulas

The range helper is named `getRange(int spellPower)` but the call site passes **spellLevel**:

`range = (10 + 2*spellLevel)*3`

Redirect:

`normalized=(level-1)/(maxLevel-1)`

`scaled=normalized^(0.6/(1+0.1*getSpellPower))`

`armorBonus=0.20*armor/(armor+100)`

`redirect=min(1.0, 0.20 + 0.60*scaled + armorBonus)`

At level 1 this starts at 20% + armor bonus; at level 10 it reaches 80% + armor bonus before the 100% cap.

`duration = 15 + 0.20*getSpellPower`.

## Server settlement design

`SwornProtectorEvent` listens to `LivingIncomingDamageEvent` server-side and:

1. only protects Player victims;
2. ignores already-redirected damage to prevent recursion;
3. searches protectors with the effect in a broad 64-block box;
4. filters by each protector's stored range;
5. chooses the nearest eligible protector;
6. refuses redirect when protector is the attacker;
7. subtracts the redirected portion from victim damage;
8. hurts protector exactly once with dedicated `paladin_spells` redirect damage type.

This is a strong exactly-once causal boundary and must remain provider-native.

## Authority blocker found in exact 1.1.1 source

The current `SwornProtectorSpell.onCast` writes `sworn_protector_redirect`, `sworn_protector_range` and `SWORN_PROTECTOR_EFFECT` only inside:

`if (level.isClientSide) { ... }`

The redirection event explicitly runs server-side. Client persistent data/effects are not a valid substitute for server-authoritative state.

Therefore the semantic design/event settlement is fully documented, but **functional activation is `LIVE-JAR/GAMETEST REQUIRED`**. Black Arcana must not silently emulate the missing server state in this catalog branch.

## Mandatory matrix

- target: self as protector; protected victims are nearby Players chosen later by event;
- PvP: attacker==protector guard confirmed; broader party/team/protection semantics `NÃO VERIFICADO`;
- bosses/summons: not protected victims unless Player; damage source attacker can vary;
- acquisition/focus/ritual: specific route `NÃO VERIFICADO`;
- VFX/audio: Bulwark start sound + `CHARGE_RAISED_HAND`; tether visualization not source-confirmed;
- dedup: occupies ally-damage interception/protector-link signature;
- fail-closed: no bridge redirection until server authority is proven/corrected.

## Source

Paladin branch `1.21@31f64ccdb39d062b21cc25d434cb62d6463b486e`, `SwornProtectorSpell` + `SwornProtectorEvent`; changelog 1.1.1.
