# Esoteric Strike

**Registro físico confirmado (2026-10-13):** ✅ `COUNTED_EXACT` — `discerning_the_eldritch:esoteric_strike`, classe `net.acetheeldritchking.discerning_the_eldritch.spells.eldritch.EsotericStrikeSpell`, `SchoolRegistry.ELDRITCH_RESOURCE`; [Java21 #38455449207](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38455449207) e [dossiê SHA-exato](../EXACT-BINARY-SPELLS-1.4.4-1.21.md). Parâmetros source-pinned; runtime/Survival ⚠️; +0.

- **ID:** `discerning_the_eldritch:esoteric_strike`
- **School:** Eldritch
- **Levels:** 1–5
- **Rarity:** Legendary
- **Cast:** Instant
- **Mana neutral:** 25–45
- **Spell power neutral:** 5–13
- **Cooldown:** 1 s
- **Hit radius:** 2.15 around a point ~1.2 blocks forward

## Damage

`baseDamage = ASUtils.getDamageForAttributes(spell, caster, level, ATTACK_DAMAGE, 0.35)`

`finalDamage = baseDamage + Utils.getWeaponDamage(caster)`.

Thus this is a melee-attribute hybrid spell, not a pure spell-power punch.

The spell scans nearby entities, requires distance/LOS, excludes `ItemEntity`, applies Iron's `DamageSources.applyDamage` with the spell's damage source, triggers post-attack enchantment effects, and spawns an `EsotericStrike` swipe entity for presentation. Offhand casting mirrors the swipe.

## Dedup / authority

- provider scan + damage settlement is authoritative;
- do not add a second melee hit from animation callbacks;
- post-attack enchant effects are intentionally triggered after successful spell damage;
- friendly-fire/team filters beyond `DamageSources` behavior: `NÃO VERIFICADO`.

## Source

`EsotericStrikeSpell.java`, branch `1.21@7bbd81f...`.
