# Kinetic Barrier

**✅ Verificação física mais recente (2026-10-13):** `ironsable:kinetic_barrier` é registry estático do JAR físico/publicador 1.2.0 (SHA-1 `6ea9ce03144ec741a1e8d322f06985366d9ecc9e`), [Java 21 #38408009738](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38408009738) SUCCESS. **School default Evocation** por `DefaultConfig.setSchoolResource` no bytecode. `COUNTED_EXACT` para identidade/escola de configuração default, **+0** raízes. As referências históricas abaixo de bytecode/escola não verificados foram superadas somente para symbols/IDs/default school. Config live, mana, cooldown, ship physics, Sable/Survival **⚠️ pendentes**. [Dossiê](../EXACT-BINARY-SPELLS-1.2.0.md).


- ID: `ironsable:kinetic_barrier` — observed in pack runtime logs.
- Provider: IronSable `1.2.0`.
- School (default verificado no JAR): **Evocation**; a configuração realmente carregada no pack permanece ⚠️.
- Levels / rarity: **NÃO VERIFICADO**.
- Cast/channel timing: **NÃO VERIFICADO**.
- Mana / cooldown / damage: **NÃO VERIFICADO**.
- Barrier radius / force / duration / caps: **NÃO VERIFICADO**.

## Contract

Official behavior: raises a force sphere around the ship the caster is standing on and pushes away anything that drifts too close. The spell **only works while the caster is aboard a ship**.

The aboard-ship gate is part of spell identity. It must not be weakened into a generic player-centered knockback aura.

## Acquisition

Same Iron's loot ecosystem; Scroll Forge craftable; every level in IronSable creative tab. Exact values: **NÃO VERIFICADO**.

## Dedup / authority

Barrier admission and ship/object repulsion are provider-owned. Do not add an independent radial force layer.

## Fail-closed

If ship membership/ownership cannot be resolved through exact provider/Sable hooks, fail closed instead of treating nearby vanilla entities as equivalent ships.

## Evidence state

Exact release + runtime ID + official semantic contract; school/stats/bytecode pending.