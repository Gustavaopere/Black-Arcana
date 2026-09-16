# Paladin Spells — Iron's Spells Addon

Status: `INSTALLED 1.1.1 / SOURCE-PINNED / 5/5 SPELLS CATALOGED / UPSTREAM QA BLOCKERS EXPLICIT`

- **JAR do pack:** `paladin_spells-1.21.1-1.1.1.jar`
- **Mod ID:** `paladin_spells`
- **Runtime version:** `1.21.1-1.1.1`
- **Provider class:** `SPELL_PROVIDER / IRON'S CONTENT ADDON`
- **Native school used:** Iron's `Holy`
- **Source authority:** upstream branch `1.21@31f64ccdb39d062b21cc25d434cb62d6463b486e`
- **Source version pin:** `gradle.properties` declares Minecraft `1.21.1` and mod version `1.21.1-1.1.1`.

The current CurseForge page describes the addon as a tank-oriented Iron's spell pack whose five spells scale with Holy spell power. The current 1.1.1 changelog fixes Sworn Protector duration, Bulwark cooldown to 45 s, a client-only-class server crash, removes WIP from two released spells and nerfs Bulwark duration.

## Catalog — 5/5

| Spell | ID | Role | Documentation state |
|---|---|---|---|
| Bulwark | `paladin_spells:bulwark` | armor amplification | `CATALOGED / LIVE FUNCTION QA REQUIRED` |
| Taunt | `paladin_spells:taunt` | AoE aggro control | `CATALOGED` |
| Sworn Protector | `paladin_spells:sworn_protector` | ally damage redirection | `CATALOGED / SERVER-AUTHORITY QA BLOCKER` |
| Bedrock Skin | `paladin_spells:bedrock_skin` | rooted defense stance | `CATALOGED / MITIGATION QA BLOCKER` |
| Ram | `paladin_spells:ram` | armor-scaling dash attack | `CATALOGED / FRIENDLY-FIRE QA REQUIRED` |

**Provider coverage: 5/5 — DOCUMENTATION COMPLETE.**

`DOCUMENTATION COMPLETE` does not mean every upstream mechanic is proven functional. Static source inconsistencies are kept as QA blockers and integrations must fail closed until live-JAR/GameTest evidence resolves them.

## Iron's base formula inherited by this addon

For the installed Iron's 3.16.3 API:

- mana before config multiplier: `baseManaCost + manaCostPerLevel × (level - 1)`;
- spell power before entity/config multipliers: `baseSpellPower + spellPowerPerLevel × (level - 1)`;
- final spell power additionally multiplies generic spell power, Holy school power and config power multiplier.

Therefore the numeric ranges in individual sheets are **neutral/base ranges** unless otherwise stated.

## Acquisition

No provider-specific spell loot/acquisition table was confirmed in the audited source. The spells are registered into Iron's spell registry. Exact scroll/loot/craft/trade/Inscription behavior in the pack remains `NÃO VERIFICADO` and must follow Iron's/provider configuration rather than a fabricated addon recipe.

## Deduplication impact

Paladin Spells already occupies five strong Holy/tank signatures:

1. temporary armor amplification;
2. forced enemy aggro in an area;
3. ally damage interception/redirection;
4. rooted high-defense stance;
5. armor-scaling Holy charge.

Black Arcana Divine/Celestial/Order/Binding content cannot claim these signatures as empty design space merely by changing VFX or naming.

## Source-vs-runtime QA blockers

- **Bulwark:** spell calculates a large amplifier, but `BulwarkEffect` declares the Armor `ADD_MULTIPLIED_TOTAL` modifier with amount `0.0`; no compensating handler was found in the audited branch.
- **Sworn Protector:** `onCast` writes effect/range/redirect data only under `level.isClientSide`, while the damage-redirection event is server-side. This is an apparent authority mismatch in source.
- **Bedrock Skin:** the spell writes `bedrock_skin_reduction`; repository search found no consumer of that key. Rooting and the effect's Armor modifier are separately source-confirmed.
- **Ram:** its hit scan targets every alive `LivingEntity` except the caster in the swept AABB; no ally/friendly-fire filter appears in the spell class.

These are static source findings, not claims that the installed gameplay is broken. Live-JAR/GameTest confirmation remains required.
