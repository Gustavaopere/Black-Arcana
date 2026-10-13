# Sword Dance

**Registro físico confirmado (2026-10-13):** ✅ `COUNTED_EXACT` — `iss_magicfromtheeast:sword_dance` / `net.warphan.iss_magicfromtheeast.spells.symmetry.SwordDanceSpell`, school default `MFTESchoolRegistries.SYMMETRY_RESOURCE` ([prova Java 21 #38449995162](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38449995162); [dossiê](../EXACT-BINARY-SPELLS-1.1.5.md)). Os números e comportamentos descritos abaixo continuam derivados da fonte pinada, não aprovados em runtime físico/Survival. **+0 identidade adicional**.

- **ID:** `iss_magicfromtheeast:sword_dance`
- **School:** Symmetry
- **Levels:** 1–8
- **Min rarity:** Uncommon
- **Cast:** Instant
- **Mana neutral:** 30–100
- **Spell power neutral:** 3 at all levels before entity/config multipliers
- **Cooldown:** 40 s
- **Sword count:** `level+2` = 3–10

## Contract

Spawns Jade Swords in a 360° ring around the caster, each with damage = final Symmetry spell power and wait timer 120 ticks.

`JadeSword`:

- speed 1.2;
- briefly moves outward, then stops;
- during its active seek window tracks `owner.getLastHurtMob()` if that target remains alive;
- accelerates toward that target;
- can clear target invulnerability time after tick 10;
- breaks/discards on later impacts or timer expiration;
- explicitly does **not** pierce shields.

## Dedup / authority

Identity = delayed orbiting sword swarm that keys from the caster's last hurt mob, not generic homing missiles. The JadeSword entity owns targeting/hit cadence. Do not spawn a second swarm or reset iFrames in a parallel listener.

## Source

`SwordDanceSpell.java` + `JadeSword.java`, source 1.1.5.
