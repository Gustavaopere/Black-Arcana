# Spirit Challenging

- **ID:** `iss_magicfromtheeast:spirit_challenging`
- **School:** Spirit
- **Levels:** 1–5
- **Min rarity:** Rare
- **Cast:** Long, 20 ticks
- **Mana neutral:** 65–145
- **Cooldown:** 120 s
- **Initial target range:** 8 blocks
- **Soul link radius:** 12 blocks
- **ExtractedSoul duration:** 10–18 s
- **Linked damage percent neutral:** 10–50%

## Contract

Targeting is denied for entity types in `SPIRIT_CHALLENGING_IMMUNE`. Otherwise the spell creates an `ExtractedSoul` whose maximum/current HP equals the target's current HP at cast time, visually copies the target, and records target as owner and caster as extractor.

While the soul exists:

- normal damage dealt to the soul is retransmitted to the original target as `SOUL_DAMAGE` at the stored 10–50% coefficient, capped on overkill by the soul's remaining HP;
- damage sources tagged `SOUL_HURTING` retransmit 100% instead;
- moving the soul more than 12 blocks from its owner destroys it and punishes the owner;
- killing the soul also punishes the owner;
- punishment = Soulburn 200 ticks + Iron's `SLOWED` 200 ticks amplifier 3;
- Counterspell safely dismisses it only when used by the extractor or when server config `passChallenging=true`; default is false;
- anti-magic unsummons the soul.

## Dedup / authority

Identity = temporary linked proxy entity that redirects damage to a living target. `ExtractedSoul` + `SoulChallengingEvents` are the causal authority; do not emulate this with a generic mark/debuff listener.

## Acquisition

`NÃO VERIFICADO` in this source pass.

## Source

`SpiritChallengingSpell.java` + `ExtractedSoul.java` + `SoulChallengingEvents.java`, source 1.1.5.
