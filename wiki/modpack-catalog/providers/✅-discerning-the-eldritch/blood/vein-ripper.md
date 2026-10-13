# Vein Ripper

**Registro físico confirmado (2026-10-13):** ✅ `COUNTED_EXACT` — `discerning_the_eldritch:vein_ripper`, classe `net.acetheeldritchking.discerning_the_eldritch.spells.blood.VeinRipperSpell`, `SchoolRegistry.BLOOD_RESOURCE`; [Java21 #38455449207](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38455449207) e [dossiê SHA-exato](../EXACT-BINARY-SPELLS-1.4.4-1.21.md). Parâmetros source-pinned; runtime/Survival ⚠️; +0.

- **ID:** `discerning_the_eldritch:vein_ripper`
- **School:** Blood
- **Levels:** 1–5
- **Min rarity:** Common
- **Cast:** Instant
- **Mana neutral:** 30–90
- **Spell power neutral:** 6–14
- **Cooldown:** 20 s
- **Search distance:** `7 + level` = 8–12 blocks
- **SpellDamageSource lifesteal:** 15%

## Contract

Finds the closest living target in a forward cone/path, creates an AoE around it, damages visible/pickable targets and applies `BLOOD_ROT_EFFECT` for 3 s. Damage:

`getSpellPower + weaponDamage`.

Successful damage also triggers post-attack enchantment effects. The caster is propelled toward the resolved endpoint and receives Iron's fall-damage immunity for 20 ticks.

The damage source overrides Iron's `SpellDamageSource` with `lifestealPercent=0.15`.

## Dedup / authority

Identity = forward Blood engage + AoE slash + weapon scaling + Blood Rot + 15% spell lifesteal + caster movement. Do not separately award lifesteal or perform another AoE scan.

Fine Blood Rot behavior and party/friendly-fire rules beyond provider damage pipeline: `NÃO VERIFICADO`.

## Source

`VeinRipperSpell.java`, branch `1.21@7bbd81f...`.
