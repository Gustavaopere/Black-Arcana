# Summoned Sculk Centipede

## Release 1.3.3-ver.b confirmada

- Um dos quatro summon spells oficiais do provider instalado.
- 1.3.3 é o hotfix de dedicated-server para os summons; não há source público 1.3.3 disponível no repositório vinculado.

## Source 1.3.0 baseline — NÃO tratar como bytecode 1.3.3

- ID observado: `darkermagic:summoned_sculk_centipede`
- School: Eldritch
- Levels: 1–4
- Min rarity: Rare
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
- Lifecycle baseline: create entity near caster, set stats, post `SpellSummonEvent`, add entity, `SummonManager.initSummon`.

## Bytecode 1.3.3 — campos pendentes

ID/config/formulas/spawn placement/event ordering/learning/AI/owner behavior: **NÃO VERIFICADOS POR BYTECODE 1.3.3**.

## Dedup / authority

Não recontar nem reaplicar stats ao summon em bridge. O provider deve permanecer autoridade após validação do hotfix 1.3.3.

## Fonte

Release: CurseForge `7897469` / Modrinth `oBllvIgO`.
Baseline: `SummonSculkCentipedeSpell.java` @ `df242888d...`.