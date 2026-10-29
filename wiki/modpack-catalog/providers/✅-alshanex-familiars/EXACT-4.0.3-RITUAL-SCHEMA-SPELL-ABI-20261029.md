# Alshanex 4.0.3 — ABI de sete spells e esquema de onze rituais (evidência exata)

Estado: `EXACT_ARTIFACT_SHA1_CONFIRMED / SPELL_ABI_7_OF_7 / RITUAL_SCHEMA_11_OF_11 / NO_MUTATORS_CERTIFIED`.

## Proveniência e limite clean-room

O run [`40933045252`](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40933045252) do GitHub Actions concluiu **SUCCESS** no job `exact_alshanex_contracts` (`123656242857`). Validou o arquivo do fornecedor `alshanex_familiars-1.21.1_v4.0.3.jar` com SHA-1 físico/publisher `e5051c2385a426d05bf203ba8081a23d891f6686` **antes** da inspeção, executou seis regressões sintéticas e emitiu artifact `12922838095` (`evidence.json`, SHA-256 `631d0fdde9d88950a016b86c81455368117574aa2e8eab0cbee75c65218e04cd`). Script reproduzível: `docs/qa/alshanex_403_exact_ritual_spell_abi.py` e workflow `.github/workflows/alshanex-403-exact-ritual-spell-abi.yml`.

O provider é **All Rights Reserved**. Os fatos aqui expostos são identificadores de registro, nomes/descritores **declarados** (`javap -p -s`, sem `-c`) e chaves/flags de recursos. Nenhum JAR, corpo de método, JSON integral, combinação de ingredientes, código ou asset é redistribuído.

## ABI registrada: sete classes de spell

| Registro | Classe exata | Métodos relevantes declarados |
|---|---|---|
| `alshanex_familiars:summon_shadows` | `ShadowSummonSpell` | `getRecastCount(int, LivingEntity): int`; `onRecastFinished(ServerPlayer, RecastInstance, RecastResult, ICastDataSerializable): void`; `getEmptyCastData(): ICastDataSerializable`; `onCast(Level, int, LivingEntity, CastSource, MagicData): void` |
| `alshanex_familiars:ice_age` | `IceAgeSpell` | `getCastTime(int): int`; `onServerCastTick(Level, int, LivingEntity, MagicData): void`; `onServerCastComplete(Level, int, LivingEntity, MagicData, boolean): void`; `freezeAround(Level, int, LivingEntity, int): void`; `getDamage(int, LivingEntity): float`; `getRadius(int, LivingEntity): float`; `getDamageSource(Entity, Entity): SpellDamageSource` |
| `alshanex_familiars:ice_chamber` | `IceChamberSpell` | `getRange(int, LivingEntity): float`; `getDamage(int, LivingEntity): float`; `getFreezeTime(int, LivingEntity): int` |
| `alshanex_familiars:megido` | `MegidoSpell` | `checkPreCastConditions(Level, int, LivingEntity, MagicData): boolean`; `getDamage(int, LivingEntity): float`; `getRadius(): float`; `getRange(): float`; `getMaxConnections(int, LivingEntity): int` |
| `alshanex_familiars:fire_fist` | `HikenSpell` | `getDamage(int, LivingEntity): float`; `getRadius(int, LivingEntity): int` |
| `alshanex_familiars:end_mayhem` | `EndMayhemSpell` | `getAmplifierForLevel(int, LivingEntity): int`; `getDurationTicks(int, LivingEntity): int` |
| `alshanex_familiars:switcheroo` | `SwitcherooSpell` | `checkPreCastConditions(Level, int, LivingEntity, MagicData): boolean`; `getDistance(int, LivingEntity): float` |

As sete classes também declaram `getDefaultConfig()`, `getCastType()` e `onCast(...)` (as últimas duas quando não repetidas na tabela). **Detalhes de ABI não são hooks integráveis aprovados**: `getRadius` de Megido não recebe parâmetros, enquanto o de Fire Fist recebe nível/caster e retorna `int`; Ice Age retorna `float`. Isto impede gerar genericamente uma perk `radius` sem analisar consumidores/ordem e sem API mutadora efetiva.

## Recursos exatos: onze rituais

Todos os **11** JSONs do JAR 4.0.3 estão sob `data/alshanex_familiars/recipe/ritual_recipes/`, usam `type=alshanex_familiars:ritual_recipe` e contêm exatamente as chaves `central_item`, `inputs`, `particle_type`, `result`, `type`. `central_item` é objeto; `inputs` são quatro objetos, cada um com `ingredient` objeto, `count` e `consume` explícitos; `result` é objeto com `id` canônico; `particle_type` é string.

| ID de receita no JAR | Pedestais | Contagens explícitas | Entradas com `consume=false` |
|---|---:|---:|---|
| `alshanex_familiars:archmage_shard` | 4 | 4/4 | 0 |
| `alshanex_familiars:druid_shard` | 4 | 4/4 | 1 (posição 4) |
| `alshanex_familiars:frostling_shard` | 4 | 4/4 | 0 |
| `alshanex_familiars:hunter_shard` | 4 | 4/4 | 0 |
| `alshanex_familiars:lightning_mage_shard` | 4 | 4/4 | 0 |
| `alshanex_familiars:magic_power_tier_2` | 4 | 4/4 | 0 |
| `alshanex_familiars:magic_power_tier_3` | 4 | 4/4 | 1 (posição 1) |
| `alshanex_familiars:magic_resist_tier_2` | 4 | 4/4 | 0 |
| `alshanex_familiars:magic_resist_tier_3` | 4 | 4/4 | 1 (posição 1) |
| `alshanex_familiars:summoner_shard` | 4 | 4/4 | 0 |
| `alshanex_familiars:truth_mirror` | 4 | 4/4 | 0 |

Cada `result.id` no **JAR exato** permanece `alshanex_familiars:<nome_da_receita>`; a wiki do fornecedor sem pin de release menciona alguns outputs de ovo de familiar, **mas não comprova esses outputs em 4.0.3**. Esta auditoria desambigua a comparação para a versão instalada, sem alterar o ledger dos **18** objetos semânticos.

## Restrições para perks e QA

A presença de `getDamage/getRadius/getRange/getFreezeTime/getDistance/getDurationTicks/getMaxConnections` é somente ABI declarada; **não** informa valores, escala, clientes/servidor, consumidores ou mecanismo de alteração externa. `onServerCastTick` e `onRecastFinished` também **não** são autorização para interceptar, repetir ou liquidar efeitos do provider.

`consume=false` é uma flag da receita publicada dentro do JAR, **não** resultado físico observado de um rito executado. Custos, ingredientes específicos, montagem, comportamento com `consume=false` sob rollback, automação, multiplayer, proteção de blocos, outputs finais e gameplay exigem QA posterior. Black Arcana não deve cobrar componentes ou executar ritual de Alshanex pela segunda vez.

**Estados finais desta tranche:** `7` spells e `11` rituais com informação estática adicional; `18` identidades já catalogadas **inalteradas**; `COMPLETE_PERK_READY=0`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`; sem alteração de fila alfabética nem stage de implementação.
