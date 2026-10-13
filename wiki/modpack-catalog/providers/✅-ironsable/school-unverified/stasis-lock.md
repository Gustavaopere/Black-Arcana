# Stasis Lock

**✅ Verificação física mais recente (2026-10-13):** `ironsable:stasis_lock` é registry estático do JAR físico/publicador 1.2.0 (SHA-1 `6ea9ce03144ec741a1e8d322f06985366d9ecc9e`), [Java 21 #38408009738](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38408009738) SUCCESS. **School default Ender** por `DefaultConfig.setSchoolResource` no bytecode. `COUNTED_EXACT` para identidade/escola de configuração default, **+0** raízes. As referências históricas abaixo de bytecode/escola não verificados foram superadas somente para symbols/IDs/default school. Config live, mana, cooldown, ship physics, Sable/Survival **⚠️ pendentes**. [Dossiê](../EXACT-BINARY-SPELLS-1.2.0.md).


- ID: `ironsable:stasis_lock` — observed in pack runtime logs.
- Provider: IronSable `1.2.0`.
- School (default verificado no JAR): **Ender**; a configuração realmente carregada no pack permanece ⚠️.
- Levels / rarity: **NÃO VERIFICADO**.
- Cast/channel: active while channeling; exact cast type/ticks **NÃO VERIFICADO**.
- Mana / cooldown / damage: **NÃO VERIFICADO**.
- Range / duration cap / target filters: **NÃO VERIFICADO**.

## Contract

Official behavior: freezes a ship completely in mid-air, including gravity, for as long as the caster channels. When released, the ship resumes from a **dead stop** rather than restoring prior motion.

The reset-to-zero motion state is semantically important. A bridge must not reapply cached pre-stasis velocity unless an exact provider hook proves otherwise.

## Acquisition

Same Iron's loot ecosystem; Scroll Forge craftable; all levels in IronSable creative tab. Exact values: **NÃO VERIFICADO**.

## Dedup / authority

IronSable owns freeze/gravity suppression and release cleanup. Do not stack a second motion-cancel loop.

## Fail-closed

If server-authoritative ship freeze cannot be proven, do not simulate with player/entity immobilization.

## Evidence state

Exact release + runtime ID + official semantic contract; school/stats/API internals pending.