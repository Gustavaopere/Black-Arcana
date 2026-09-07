# Eidolon: Repraised 0.5.0.2 — Spell Catalog

Status: `20/20 REGISTRY INVENTORIED / STATIC SPELL SEMANTICS NORMALIZED / DATA-DRIVEN CHANTS + RUNTIME SETTLEMENT QA PENDING`

Canonical source: `Alexthw46/Eidolon-Repraised@696a47333e43970be7f697790eac0af76b6a04b8`

## Registry

| # | Runtime id | Signs | Base cost | Base delay | Known gate | Verified effect summary |
|---:|---|---|---:|---:|---|---|
| 1 | `eidolon_repraised:dark_prayer` | Wicked×3 | 0 | 10 | effigy + prayer cooldown | Dark deity prayer; reputation/mana loop |
| 2 | `eidolon_repraised:darklight_chant` | Wicked, Flame, Wicked, Flame | 3 | 10 | Dark reputation ≥3 | Dark GhostLight or Glowing 200t |
| 3 | `eidolon_repraised:dark_animal_sacrifice` | Wicked, Blood, Wicked | 0 | 10 | ready effigy + valid animal | ritual-kills animal; Dark rep `3 + 0.5×altar power` |
| 4 | `eidolon_repraised:dark_touch` | Wicked, Soul, Wicked, Soul | 20 fallback | 10 | Dark reputation ≥10 + valid item | data-driven conversion or NECROTIC=50 |
| 5 | `eidolon_repraised:frost_touch` | Wicked, Winter, Blood, Winter, Wicked | 20 | 10 | `FROST_SPELL` research | source water→Ice or Chilled 200t |
| 6 | `eidolon_repraised:dark_villager_sacrifice` | Blood, Wicked, Blood, Soul | 0 | 10 | Dark reputation ≥15 + ready effigy + villager | ritual-kills villager; Dark rep `6 + altar power`; grants sacrifice research |
| 7 | `eidolon_repraised:zombify_villager` | Death, Blood, Wicked, Death, Soul, Blood | 20 | 10 | Dark reputation ≥20 + prayer/effigy + villager | Villager→Zombie Villager; Dark rep `8 + 1.25×altar power` |
| 8 | `eidolon_repraised:enthrall_spell` | Wicked, Mind, Magic, Magic, Mind | dynamic | 10 | valid undead + not player/thrall + enough mana | heals target then enthralls/tames; cost `100×health ratio` at defaults |
| 9 | `eidolon_repraised:light_prayer` | Sacred×3 | 0 | 10 | effigy + prayer cooldown | Light deity prayer; reputation/mana loop |
| 10 | `eidolon_repraised:fire_chant` | Flame×3 | 10 | 5 | `FIRE_SPELL` research | lights candle/campfire/burner or 200 fire ticks |
| 11 | `eidolon_repraised:light_chant` | Sacred, Flame, Sacred, Flame | 3 | 10 | Light reputation ≥3 | Light GhostLight or Glowing 200t |
| 12 | `eidolon_repraised:holy_touch` | Sacred, Soul, Sacred, Soul | 20 fallback | 10 | Light reputation ≥10 + valid item | data-driven conversion or CONSECRATED=50 |
| 13 | `eidolon_repraised:lay_on_hands` | Flame, Soul, Sacred, Soul, Sacred | 15 | 10 | non-undead target optional | heals `5 + 0.05×Light rep`; milk-curable debuff cleanse |
| 14 | `eidolon_repraised:cure_zombie` | Sacred, Soul, Mind, Harmony, Flame, Soul | 20 | 10 | Light reputation ≥20 + prayer/effigy + Zombie Villager | cures/converts Zombie Villager; Light rep `8 + 1.25×altar power` |
| 15 | `eidolon_repraised:smite_chant` | Flame, Magic, Sacred, Death, Magic, Sacred | 40 | 10 | target must be vanilla undead | 10 magic damage + Weakness III 200t; settlement QA |
| 16 | `eidolon_repraised:sunder_armor` | Flame, Magic, Wicked, Magic, Flame | 50 | 10 | LivingEntity target | Vulnerable 1200t; settlement QA |
| 17 | `eidolon_repraised:reinforce_armor` | Sacred, Warding, Sacred, Warding, Sacred | 50 | 10 | LivingEntity target | Reinforced 1800t; settlement QA |
| 18 | `eidolon_repraised:create_water` | Winter, Winter, Flame, Flame | 10 | 10 | valid placement target | creates water; air-placement spends mana, liquid-container branch settlement QA |
| 19 | `eidolon_repraised:undead_lure` | Mind, Magic, Wicked | 50 | 10 | `canCast()` returns true | `cast()` is empty in 0.5.0.2; no verified runtime effect or settlement |
| 20 | `eidolon_repraised:basic_incense` | no fixed signs | 0 | 10 | incense subsystem | dummy PrayerSpell for incense path |

`dynamic` means the effective cost is calculated from provider state/target state rather than being the fixed base value presented to the player.

## Detailed verified entries

### Dark Prayer / Light Prayer

Both are zero-mana `PrayerSpell` instances. A prayer requires a ready nearby Effigy and provider-native prayer eligibility. On commit the provider records the prayer, obtains `AltarInfo`, increases deity reputation and updates player mana/max mana from reputation plus altar power/capacity. Generic defaults are base reputation 1, altar-power multiplier 0.25 and prayer cooldown 21000 ticks.

### Darklight Chant / Light Chant

`LightSpell` is shared by both alignments. It costs 3 mana, requires reputation ≥3 with its bound deity and either places a GhostLight on an unobstructed replaceable block adjacent to the hit face or applies Glowing for 200 ticks to a living target. The Dark instance flips the GhostLight deity state.

### Dark Animal Sacrifice

The registered constructor binds the spell to the Dark deity with base reputation 3 and altar-power multiplier 0.5, without a positive mana cost. It requires a ready prayer context and a valid nearby animal according to the provider's animal/tag/taming/blacklist gates. A successful provider ritual-damage kill produces Dark reputation `3 + 0.5 × altarPower`, updates the prayer/mana loop and records the prayer transaction.

### Dark Villager Sacrifice

This is also a zero-mana prayer/sacrifice transaction. It requires at least 15 Dark reputation, a ready effigy/prayer state and a valid villager. On successful ritual-damage kill it grants the provider's `SACRIFICE_VILLAGER` research/knowledge path, awards Dark reputation `6 + 1.0 × altarPower`, updates mana and records the prayer.

### Zombify Villager

The concrete class uses a fixed 20-mana cast despite the registry constructor also carrying the prayer reward parameters `(8, 1.25)`. It requires at least 20 Dark reputation plus the prayer/effigy gate and a valid Villager. It performs the provider conversion into a Zombie Villager, awards Dark reputation `8 + 1.25 × altarPower`, updates the mana/reputation loop, spends 20 mana and records prayer state.

### Enthrall Undead

`ThrallSpell` has base cost 50, but the actual target-sensitive cost is:

`2 × baseCost × (targetHealth / targetMaxHealth)`

At defaults this is `100 × healthRatio`, so a target at one-third health costs about 33.33 mana while a full-health target costs 100. `canCast` validates the dynamic amount against provider mana. Valid targets are provider-accepted undead that are not players and are not already enthralled. On commit the provider heals the target to full, applies its Thrall/taming path and spends the computed dynamic cost. Black Arcana must never replace this with a fixed 50-mana charge.

### Fire Chant

Costs 10 mana, delay 5. Requires `Researches.FIRE_SPELL`. It can light valid candles/campfires, start an `IBurner`, or set an entity on fire for 200 ticks. The class spends mana only after a valid action commits.

### Frost Touch

Costs 20 mana and requires `Researches.FROST_SPELL`. It replaces a source-water block with Ice or applies Eidolon `CHILLED_EFFECT` for 200 ticks to a living target, then spends mana.

### Lay on Hands

Costs 15 mana. Base heal is 5 and Light devotion contributes `0.05 × reputation`. It heals a valid non-undead looked-at LivingEntity or falls back to the caster. Non-beneficial effects whose cure set contains milk are removed. Healing another damaged entity grants `HEAL_VILLAGER` research and +3 Light reputation by default.

### Cure Zombie

The Light counterpart to Zombify uses a fixed 20-mana cast, requires at least 20 Light reputation plus provider prayer/effigy state and a valid Zombie Villager, triggers the provider conversion path, awards Light reputation `8 + 1.25 × altarPower`, updates the mana/reputation loop, spends mana and records prayer state.

### Dark Touch

Requires Dark reputation ≥10. A nearby single ItemEntity is resolved through deity-compatible `ChantConversionRecipe` entries. Recipe cost overrides the spell fallback cost when non-negative; otherwise fallback is 20. Maximum conversion count is limited by current mana. If no conversion matches and the item is a non-stackable damageable item, it receives 50 `NECROTIC` charges. On later attacks, NECROTIC converts part of the hit into Wither damage and consumes one charge when the secondary damage succeeds.

### Holy Touch

Requires Light reputation ≥10 and uses the same conversion architecture. Non-stackable damageable items receive 50 `CONSECRATED` charges when no conversion recipe is selected. Against undead targets, consecrated attacks multiply the current damage by 1.5 and consume a charge. The implementation also applies Smite bonus handling to entities considered undead by Eidolon's Undeath logic even when their vanilla type is not tagged undead.

### Smite Chant

Declares cost 40 and target gate `EntityTypeTags.UNDEAD`. It deals configurable magic damage (default 10) and, on successful hurt, applies Weakness for 200 ticks at amplifier 2 and grants `SMITE_UNDEAD` research. Direct mana expenditure is not visible in `SmiteSpell.cast()`, so runtime settlement is QA-blocked.

### Sunder Armor

Declares cost 50 and applies Eidolon `VULNERABLE_EFFECT` for 1200 ticks. It inherits `ApplyPotionSpell`, whose concrete cast path does not directly expend mana in the audited source; runtime settlement is QA-blocked.

### Reinforce Armor

Declares cost 50 and applies Eidolon `REINFORCED_EFFECT` for 1800 ticks through the same `ApplyPotionSpell` base. The audited path does not directly expend mana, so settlement remains QA-blocked.

### Create Water

Declares cost 10. The air-placement path creates a water source and visibly spends mana. A separate branch delegates placement into a compatible `LiquidBlockContainer`; that branch does not visibly expend mana in the audited class. The gameplay effect is therefore verified, while resource settlement for the container branch remains runtime-QA blocked.

### Undead Lure

Declares cost 50 and `canCast()` returns true, but `UndeadLureSpell.cast()` is empty in the exact 0.5.0.2 source. There is no source-supported target movement, aggro change, effect application or mana expenditure to document for this build. It remains **registered but functionally unverified/inert at source level** and must not be counted as active crowd-control coverage until runtime evidence proves an external path supplies behavior.

### Basic Incense

The source itself labels the registered `CENSER` entry `// dummy`. It is a `PrayerSpell` bound to the Light deity but registered without a fixed SignSequence. It is a technical spell-registry participant for the incense subsystem, not evidence of a normal player-cast chant.

## Integration note

Every value above is provider-owned and server-configurable where the source exposes a config value. Black Arcana documentation may reference these defaults, but gameplay integrations must not copy them into a second authoritative calculation. Any cast path whose source-level settlement is ambiguous remains fail-closed for economic integration until runtime QA.