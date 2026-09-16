# Vampire Spells Addon 0.0.9 — affected host capabilities

Status: `HOST-SPELL OVERLAY MAP / SOURCE-PINNED / NO NEW SPELL REGISTRY`

This file maps installed Iron's capabilities affected by Vampire Spells Addon. It is **not** a second spell catalog. Canonical spell identity, level, rarity, base mana, base cooldown and effect remain in the Iron's provider pages.

## 1. Blood School host set

The installed Iron's Spells 3.16.3 catalog contains 10 active Blood spells:

| Host spell | Resource substitution for Vampire | Vampire cooldown overlay | Special addon behavior |
|---|---|---|---|
| `irons_spellbooks:acupuncture` | yes, when eligible | yes | generic Blood bridge |
| `irons_spellbooks:blood_needles` | yes, when eligible | yes | generic Blood bridge |
| `irons_spellbooks:blood_slash` | yes, when eligible | yes | generic Blood bridge |
| `irons_spellbooks:blood_step` | yes, when eligible | yes | generic Blood bridge |
| `irons_spellbooks:devour` | yes, when eligible | yes | Vampire mana price ×2 default; delivered-damage blood restore ×2 default |
| `irons_spellbooks:heartstop` | yes, when eligible | yes | generic Blood bridge |
| `irons_spellbooks:raise_dead` | yes, when eligible | yes | generic Blood bridge; recasts are excluded from resource replacement |
| `irons_spellbooks:ray_of_siphoning` | **no** | yes | keeps mana; delivered-damage blood restore ×1 default; client ray direction reversed |
| `irons_spellbooks:sacrifice` | yes, when eligible | yes | generic Blood bridge |
| `irons_spellbooks:wither_skull` | yes, when eligible | yes | generic Blood bridge |

### Meaning of “when eligible”

Resource substitution requires:

- server-side Vampire player;
- non-creative;
- mana-consuming cast source;
- non-recast;
- spell classified by Iron's as Blood School;
- Ray excluded;
- either full mana is insufficient, or forced blood-only config is enabled.

The addon classifies school dynamically. The table reflects the **current installed 10-spell host set**, not a hardcoded addon allowlist.

## 2. Blood payment behavior

Default config:

```text
bloodCostManaFloor = 20
bloodCostManaCeiling = 140
bloodCostRatioMin = 0.05
bloodCostRatioMax = 0.05
alwaysUseBloodForVampireBloodSpells = false
```

Therefore default blood fallback cost is:

```text
ceil(finalManaCost × 0.05)
```

For Devour, `finalManaCost` includes the Vampire-specific default multiplier `2.0` before resource selection.

Payment is atomic: the addon zeroes the current mana debit only for an eligible blood settlement and requires the full Vampirism blood payment. Failure stops the cast rather than accepting a partial resource payment.

## 3. Blood restoration specials

Only two spells receive delivered-damage blood restoration in the audited source:

| Spell | Default restore multiplier | Default saturation | Payment exception |
|---|---:|---:|---|
| Ray of Siphoning | `1.0` | `0.5` | remains mana-paid; no blood substitution |
| Devour | `2.0` | `0.6` | ordinary eligible blood fallback may apply |

Restoration uses delivered health damage, not raw pre-damage amount, and is capped to free Vampirism blood capacity.

No other Blood spell should be assumed to restore blood simply because it belongs to the school.

## 4. Cooldown overlay

Every Blood School spell cast by a Vampire receives the provider-event cooldown multiplier.

Default:

```text
vampireBloodSpellCooldownMultiplier = 2 / 3
```

The current 10 Blood spells above are therefore all touched by this overlay.

## 5. Holy pipeline overlay

Holy behavior is not modeled as “new Holy spells.” The addon alters existing Iron's Holy cast/damage/heal semantics when Vampirism entities/players participate.

### Dynamic Holy damage/heal behavior

For any relevant Iron's Holy spell passing the audited events:

- Holy damage to a non-player Vampirism Vampire entity is doubled;
- delivered Holy health damage by a Vampire player caster is reflected back to the caster;
- Holy healing on a Vampire player damages the target by the heal amount and suppresses the correlated heal;
- if caster and target differ and the caster is a Vampire player, the caster also receives the heal amount as damage.

These are school/event semantics, not a fixed spell allowlist.

## 6. Explicit Holy utility allowlist

The following six IDs have an additional pre-cast prohibition for Vampire players:

| Spell ID | Vampire behavior |
|---|---|
| `irons_spellbooks:angel_wing` | cast canceled; additional cast data reset; 5 magic self-damage |
| `irons_spellbooks:fortify` | cast canceled; additional cast data reset; 5 magic self-damage |
| `irons_spellbooks:wisp` | cast canceled; additional cast data reset; 5 magic self-damage |
| `irons_spellbooks:haste` | cast canceled; additional cast data reset; 5 magic self-damage |
| `irons_spellbooks:cleanse` | cast canceled; additional cast data reset; 5 magic self-damage |
| `irons_spellbooks:sunbeam` | cast canceled; additional cast data reset; 5 magic self-damage |

Do not infer that every non-damage Holy spell belongs to this list. The source list is exact.

## 7. Deduplication boundary for Black Arcana

For one host cast, Black Arcana must not independently count or settle all of these as separate actions:

```text
Iron's pre-cast
-> addon resource decision
-> Vampirism blood debit if selected
-> spell effect/damage/heal
-> addon delivered-damage/holy settlement
-> Iron's cooldown event modified by addon
```

The causal identity remains the host Iron's cast plus its downstream result.

Likewise, an increase in Vampirism blood after Ray/Devour is not an independent “blood gain action” when it is the settlement of that same delivered spell damage.

## 8. Runtime caveat

The addon release supports Iron's 3.x by metadata, but its own source audit explicitly pinned Iron's 3.16.2 while the pack currently uses 3.16.3. Until the installed combination passes runtime QA, this map is authoritative for **source-level semantics**, not proof that every mixin/reflection injection is active in the running modpack.
