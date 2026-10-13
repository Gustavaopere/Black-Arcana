# Summoned Shattered

**✅ Registro estático exato:** `darkermagic:summoned_shattered`, classe `net.rev.darkermagic.spells.eldritch.SummonShatteredSpell`, `DDISSSpellRegistery.SUMMON_SHATTERED_SPELL` no JAR físico 1.3.3 Version B ([prova](../EXACT-BINARY-SUMMONS-1.3.3-VER-B.md), [run #38329132941](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38329132941)). **⚠️ Spawn, cooldown, fórmulas, config, obtenção e Survival não validados.**

## Release 1.3.3-ver.b confirmada

- Um dos quatro summon spells oficiais da release instalada.
- A release 1.3.3 corrige os summon spells para servidor; internals exatos desse fix não estão publicados no source GitHub disponível.

## Source 1.3.0 baseline — NÃO tratar como bytecode 1.3.3

- ID observado: `darkermagic:summoned_shattered`
- School: Eldritch
- Levels: 1–4
- Min rarity: Epic
- Cast: Long, 40 ticks
- Base mana: 100; `manaCostPerLevel=20`
- Base spell power: 6; `spellPowerPerLevel=1`
- Cooldown: 180 s
- Count baseline: `spellLevel + 1` = 2–5 summons
- Recast count: 2
- Lifetime: 12.000 ticks / 10 min
- HP baseline: `(40 + spellLevel) × entityPowerMultiplier`
- Attack Damage baseline: `getSpellPower(spellLevel, caster)`
- Baseline spawns around caster after moving to relative ground level, posts `SpellSummonEvent` and registers each entity with `SummonManager`.
- `requiresLearning=false` no source baseline.

## Bytecode 1.3.3 — campos pendentes

**ID no JAR: ✅ VERIFICADO ESTATICAMENTE.** Config, fórmulas, summon count, spawn/event order, learning, AI e owner behavior: **⚠️ NÃO VERIFICADOS FUNCIONALMENTE EM 1.3.3**. Dados do source acima são baseline.

## Dedup / authority

Sem ledger paralelo de swarm, owner ou despawn. Runtime 1.3.3 deve decidir lifecycle canônico.

## Fonte

Release: CurseForge `7897469` / Modrinth `oBllvIgO`.
Baseline: `SummonShatteredSpell.java` @ `df242888d...`.