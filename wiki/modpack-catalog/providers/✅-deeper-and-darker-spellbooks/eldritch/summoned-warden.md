# Summoned Warden

## Release 1.3.3-ver.b confirmada

- Provider instalado: `darkermagic-1.3.3-1.21.1-ver.b.jar`
- Integração temática: Deeper and Darker + Iron's Spells
- Pertence ao conjunto oficial de quatro summon spells.
- A release 1.3.3 corrige comportamento/crash dos summon spells em servidor; bytecode exato não foi extraído nesta auditoria.

## Source 1.3.0 baseline — NÃO tratar como bytecode 1.3.3

- ID observado: `darkermagic:summoned_warden`
- School: Eldritch
- Max level: 1
- Min rarity: Legendary
- Cast type: Long
- Cast time: 70 ticks
- Base mana: 250; `manaCostPerLevel=20`
- Base spell power: 6; `spellPowerPerLevel=1`
- Cooldown: 180 s
- Summon count: 1
- Recast count: 2
- Summon lifetime: 12.000 ticks / 10 min
- HP formula baseline: `(175 + spellLevel) × entityPowerMultiplier`
- Attack Damage baseline: `getSpellPower(spellLevel + 10, caster)`
- Baseline lifecycle: create `SummonedWarden`, set attack/max-health, `finalizeSpawn`, post `SpellSummonEvent`, add entity, `SummonManager.initSummon`.

## Bytecode 1.3.3 — campos pendentes

- ID exato no JAR: **NÃO VERIFICADO POR BYTECODE 1.3.3**
- fórmulas HP/damage: **NÃO VERIFICADAS EM 1.3.3**
- ordem de spawn/event/initSummon: **NÃO VERIFICADA EM 1.3.3** e especialmente sensível ao hotfix de servidor
- owner/friendly-fire/AI fino: **NÃO VERIFICADO EM 1.3.3**
- obtenção/aprendizado/loot: **NÃO VERIFICADO EM 1.3.3**

## Dedup / authority

Não criar um segundo lifecycle de Warden summon nem compensar o fix de servidor em bridge. A autoridade deve permanecer no provider 1.3.3 + Iron's `SummonManager` após runtime validation.

## Fonte

Release exata: CurseForge `7897469` / Modrinth `oBllvIgO`.
Baseline: `SummonWardenSpell.java` @ `df242888d16e580a8f76e0d937fe50d66bbed8ed`.