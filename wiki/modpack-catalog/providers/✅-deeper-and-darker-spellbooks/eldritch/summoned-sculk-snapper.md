# Summoned Sculk Snapper

**✅ Registro estático exato:** `darkermagic:summoned_sculk_snapper`, classe `net.rev.darkermagic.spells.eldritch.SummonSculkSnapperSpell`, `DDISSSpellRegistery.SUMMON_SCULK_SNAPPER_SPELL` no JAR físico 1.3.3 Version B ([prova](../EXACT-BINARY-SUMMONS-1.3.3-VER-B.md), [run #38329132941](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38329132941)). **⚠️ Spawn, cooldown, fórmulas, config, obtenção e Survival não validados.**

## Release 1.3.3-ver.b confirmada

- Um dos quatro summon spells oficiais do provider instalado.
- O changelog 1.3.3 cobre justamente a correção dos summon spells em servidor.

## Source 1.3.0 baseline — NÃO tratar como bytecode 1.3.3

- ID observado: `darkermagic:summoned_sculk_snapper`
- School: Eldritch
- Levels: 1–4
- Min rarity: Epic
- Cast: Long, 40 ticks
- Base mana: 100; `manaCostPerLevel=20`
- Base spell power: 6; `spellPowerPerLevel=1`
- Cooldown: 180 s
- Count baseline: `spellLevel + 1` = 2–5
- Recast count: 2
- Lifetime: 12.000 ticks / 10 min
- HP baseline: `(12 + spellLevel) × entityPowerMultiplier`
- Attack Damage baseline: `(4 + spellLevel) × entityPowerMultiplier`
- `requiresLearning=false` no source baseline.
- Lifecycle baseline: spawn at caster, set stats, post `SpellSummonEvent`, add entity, register with `SummonManager`.

## Bytecode 1.3.3 — campos pendentes

**ID no JAR: ✅ VERIFICADO ESTATICAMENTE.** Config, fórmulas, summon count, spawn/event order, learning, AI e owner behavior: **⚠️ NÃO VERIFICADOS FUNCIONALMENTE EM 1.3.3**. Dados do source acima são baseline.

## Dedup / authority

Sem lifecycle ou stat assignment paralelo no Black Arcana. O hotfix 1.3.3 deve ser validado provider-native.

## Fonte

Release: CurseForge `7897469` / Modrinth `oBllvIgO`.
Baseline: `SummonSculkSnapperSpell.java` @ `df242888d...`.