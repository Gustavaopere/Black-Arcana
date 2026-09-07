# Eidolon: Repraised 0.5.0.2 — Spell Catalog

Status: `20/20 REGISTRY INVENTORIED / PARAMETER EXPANSION IN PROGRESS`

Canonical source: `Alexthw46/Eidolon-Repraised@696a47333e43970be7f697790eac0af76b6a04b8`

## Registry

| # | Runtime id | Signs | Base cost | Base delay | Known gate | Verified effect summary |
|---:|---|---|---:|---:|---|---|
| 1 | `eidolon_repraised:dark_prayer` | Wicked×3 | 0 | 10 | effigy + prayer cooldown | Dark deity prayer; reputation/mana loop |
| 2 | `eidolon_repraised:darklight_chant` | Wicked, Flame, Wicked, Flame | 3 | 10 | Dark reputation ≥3 | Dark GhostLight or Glowing 200t |
| 3 | `eidolon_repraised:dark_animal_sacrifice` | Wicked, Blood, Wicked | pending exact settlement | 10 | deity/sacrifice gates | animal sacrifice, Dark reputation |
| 4 | `eidolon_repraised:dark_touch` | Wicked, Soul, Wicked, Soul | 20 fallback | 10 | Dark reputation ≥10 + valid item | data-driven conversion or NECROTIC=50 |
| 5 | `eidolon_repraised:frost_touch` | Wicked, Winter, Blood, Winter, Wicked | 20 | 10 | `FROST_SPELL` research | source water→Ice or Chilled 200t |
| 6 | `eidolon_repraised:dark_villager_sacrifice` | Blood, Wicked, Blood, Soul | pending exact settlement | 10 | deity/sacrifice gates | villager sacrifice, Dark reputation |
| 7 | `eidolon_repraised:zombify_villager` | Death, Blood, Wicked, Death, Soul, Blood | constructor parameter 8 | 10 | target/devotion logic pending expansion | converts target via Zombify path |
| 8 | `eidolon_repraised:enthrall_spell` | Wicked, Mind, Magic, Magic, Mind | pending | 10 | undead/target logic pending expansion | enthralls undead |
| 9 | `eidolon_repraised:light_prayer` | Sacred×3 | 0 | 10 | effigy + prayer cooldown | Light deity prayer; reputation/mana loop |
| 10 | `eidolon_repraised:fire_chant` | Flame×3 | 10 | 5 | `FIRE_SPELL` research | lights candle/campfire/burner or 200 fire ticks |
| 11 | `eidolon_repraised:light_chant` | Sacred, Flame, Sacred, Flame | 3 | 10 | Light reputation ≥3 | Light GhostLight or Glowing 200t |
| 12 | `eidolon_repraised:holy_touch` | Sacred, Soul, Sacred, Soul | 20 fallback | 10 | Light reputation ≥10 + valid item | data-driven conversion or CONSECRATED=50 |
| 13 | `eidolon_repraised:lay_on_hands` | Flame, Soul, Sacred, Soul, Sacred | 15 | 10 | non-undead target optional | heals 5 + 0.05×Light rep; milk-curable debuff cleanse |
| 14 | `eidolon_repraised:cure_zombie` | Sacred, Soul, Mind, Harmony, Flame, Soul | constructor parameter 8 | 10 | target/devotion logic pending expansion | cures/converts zombie villager |
| 15 | `eidolon_repraised:smite_chant` | Flame, Magic, Sacred, Death, Magic, Sacred | 40 | 10 | target must be vanilla undead | 10 magic damage + Weakness III 200t; settlement QA |
| 16 | `eidolon_repraised:sunder_armor` | Flame, Magic, Wicked, Magic, Flame | 50 | 10 | LivingEntity target | Vulnerable 1200t; settlement QA |
| 17 | `eidolon_repraised:reinforce_armor` | Sacred, Warding, Sacred, Warding, Sacred | pending | 10 | target/equipment logic pending expansion | defensive armor effect pending source expansion |
| 18 | `eidolon_repraised:create_water` | Winter, Winter, Flame, Flame | pending | 10 | target logic pending expansion | water creation/manipulation pending source expansion |
| 19 | `eidolon_repraised:undead_lure` | Mind, Magic, Wicked | pending | 10 | undead/target logic pending expansion | undead lure/control pending source expansion |
| 20 | `eidolon_repraised:basic_incense` | no fixed signs | 0 | 10 | incense subsystem | dummy PrayerSpell for incense path |

`pending` means the 0.5.0.2 class has not yet been normalized into this file; it does not mean cost/effect is absent.

## Detailed verified entries

### Darklight Chant / Light Chant

`LightSpell` is shared by both alignments. It costs 3 mana, requires reputation ≥3 with its bound deity and either places a GhostLight on an unobstructed replaceable block adjacent to the hit face or applies Glowing for 200 ticks to a living target. The Dark instance flips the GhostLight deity state.

### Fire Chant

Costs 10 mana, delay 5. Requires `Researches.FIRE_SPELL`. It can light valid candles/campfires, start an `IBurner`, or set an entity on fire for 200 ticks. The class spends mana only after a valid action commits.

### Frost Touch

Costs 20 mana and requires `Researches.FROST_SPELL`. It replaces a source-water block with Ice or applies Eidolon `CHILLED_EFFECT` for 200 ticks to a living target, then spends mana.

### Lay on Hands

Costs 15 mana. Base heal is 5 and Light devotion contributes `0.05 × reputation`. It heals a valid non-undead looked-at LivingEntity or falls back to the caster. Non-beneficial effects whose cure set contains milk are removed. Healing another damaged entity grants `HEAL_VILLAGER` research and +3 Light reputation by default.

### Dark Touch

Requires Dark reputation ≥10. A nearby single ItemEntity is resolved through deity-compatible `ChantConversionRecipe` entries. Recipe cost overrides the spell fallback cost when non-negative; otherwise fallback is 20. Maximum conversion count is limited by current mana. If no conversion matches and the item is a non-stackable damageable item, it receives 50 `NECROTIC` charges. On later attacks, NECROTIC converts part of the hit into Wither damage and consumes one charge when the secondary damage succeeds.

### Holy Touch

Requires Light reputation ≥10 and uses the same conversion architecture. Non-stackable damageable items receive 50 `CONSECRATED` charges when no conversion recipe is selected. Against undead targets, consecrated attacks multiply the current damage by 1.5 and consume a charge. The implementation also applies Smite bonus handling to entities considered undead by Eidolon's Undeath logic even when their vanilla type is not tagged undead.

### Smite Chant

Declares cost 40 and target gate `EntityTypeTags.UNDEAD`. It deals configurable magic damage (default 10) and, on successful hurt, applies Weakness for 200 ticks at amplifier 2 and grants `SMITE_UNDEAD` research. Direct mana expenditure is not visible in `SmiteSpell.cast()`, so runtime settlement is QA-blocked.

### Sunder Armor

Declares cost 50 and applies Eidolon `VULNERABLE_EFFECT` for 1200 ticks. It inherits `ApplyPotionSpell`, whose concrete cast path does not directly expend mana in the audited source; runtime settlement is QA-blocked.

## Integration note

Every value above is provider-owned and server-configurable where the source exposes a config value. Black Arcana documentation may reference these defaults, but gameplay integrations must not copy them into a second authoritative calculation.