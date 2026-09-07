# Summon Lunar Moth

- ID: `asterismarcanum:summon_lunar_moths`
- nome player-facing: Summon Lunar Moth
- escola: Astral
- rarity: Rare
- nível: 1
- cast: LONG, 30 ticks / 1.5 s base
- mana: 150
- cooldown: 150 s
- neutral spell power: 20
- summon count: 1
- duração: 10 minutos
- recast count: 2

## Efeito

Apesar do ID plural e de comentários antigos sobre swarm, a implementação 0.1.0 cria **um único `SummonedLunarMothEntity`** quando não existe recast ativo para a spell.

O summon passa por `SpellSummonEvent`, `SummonManager.initSummon`, `SummonedEntitiesCastData` e `RecastInstance` de Iron's.

### Entidade summon

- 15 Max Health;
- 24 Follow Range;
- 2 base Attack Damage;
- 15% Mana Rend;
- Flying Speed 1.3;
- segue/copia targets do owner;
- aplica Levitation por 40 ticks ao atacar;
- pode ser montada pelo summoner e usada para voo.

## Obtenção

Fonte concreta: Astral Scroll do Astromancer; crafting conforme config do Iron's.

## Authority e dedup

Authority = Iron's SummonManager + entidade. Não criar segundo owner map, segundo timer, segundo summon por recast ou recompensa de XP da criatura.

## QA

Duração/recast, mount/dismount, owner logout/death, allied targeting, chunk unload e cleanup.