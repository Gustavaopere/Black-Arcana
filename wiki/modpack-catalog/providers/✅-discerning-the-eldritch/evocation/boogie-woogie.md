# Boogie Woogie

**Registro físico confirmado (2026-10-13):** ✅ `COUNTED_EXACT` — `discerning_the_eldritch:boogie_woogie`, classe `net.acetheeldritchking.discerning_the_eldritch.spells.evocation.BoogieWoogieSpell`, `SchoolRegistry.EVOCATION_RESOURCE`; [Java21 #38455449207](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38455449207) e [dossiê SHA-exato](../EXACT-BINARY-SPELLS-1.4.4-1.21.md). Parâmetros source-pinned; runtime/Survival ⚠️; +0.

- **ID:** `discerning_the_eldritch:boogie_woogie`
- **School:** Evocation
- **Levels:** 1–5
- **Min rarity:** Rare
- **Cast:** Instant
- **Mana neutral:** 20–40
- **Cooldown:** 10 s
- **Target range:** `15 + level` = 16–20 blocks
- **Recast window:** 80 ticks / 4 s

## Contract

Uses Iron's `TargetEntityCastData`, stores caster and target positions, then directly teleports each entity to the other's previous position. Target receives vanilla Confusion for 60 ticks / 3 s.

Default recast count = 1. If `ECHO_VIBRATION_RING` is equipped, recast count = `1 + spellLevel` (2–6).

## Dedup / safety

This is exact **two-entity transposition**, not ordinary blink. A bridge must not perform a second swap after observing teleport. Dimension/cross-world behavior, passenger handling and protection/PvP restrictions are not explicitly handled in the class and require runtime QA.

## Presentation

`CLAP_SPELL_CAST`; clap finish animation from Ace's Spell Utils.

## Source

`BoogieWoogieSpell.java`, branch `1.21@7bbd81f...`.
