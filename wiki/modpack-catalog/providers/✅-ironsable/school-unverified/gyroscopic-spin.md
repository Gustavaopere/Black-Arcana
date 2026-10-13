# Gyroscopic Spin

**✅ Verificação física mais recente (2026-10-13):** `ironsable:gyroscopic_spin` é registry estático do JAR físico/publicador 1.2.0 (SHA-1 `6ea9ce03144ec741a1e8d322f06985366d9ecc9e`), [Java 21 #38408009738](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38408009738) SUCCESS. **School default Lightning** por `DefaultConfig.setSchoolResource` no bytecode. `COUNTED_EXACT` para identidade/escola de configuração default, **+0** raízes. As referências históricas abaixo de bytecode/escola não verificados foram superadas somente para symbols/IDs/default school. Config live, mana, cooldown, ship physics, Sable/Survival **⚠️ pendentes**. [Dossiê](../EXACT-BINARY-SPELLS-1.2.0.md).


- ID: `ironsable:gyroscopic_spin` — observed in pack runtime logs.
- Provider: IronSable `1.2.0`.
- School (default verificado no JAR): **Lightning**; a configuração realmente carregada no pack permanece ⚠️.
- Levels / rarity: **NÃO VERIFICADO**.
- Cast/channel: channel-dependent behavior confirmed; exact cast type/ticks **NÃO VERIFICADO**.
- Mana / cooldown / damage: **NÃO VERIFICADO**.
- Range / rotation speed formula / caps: **NÃO VERIFICADO**.

## Contract

Official behavior: rotates a ship in place without translating it. Holding/channeling longer makes it spin faster; aiming left or right of the ship center selects rotation direction.

The public description establishes orientation-sensitive directional control and channel scaling, but not the exact angular velocity function or target/ownership rules.

## Acquisition

Same Iron's loot ecosystem; Scroll Forge craftable; every level in IronSable creative tab. Exact loot/crafting values: **NÃO VERIFICADO**.

## Dedup / authority

Rotation is provider-owned. A bridge must not also write yaw/angular velocity after IronSable handles the ship.

## Fail-closed

Do not approximate with teleport/position rotation or client-only visual rotation.

## Evidence state

Exact 1.2.0 release + runtime ID + official semantic contract; school/stats/bytecode pending.