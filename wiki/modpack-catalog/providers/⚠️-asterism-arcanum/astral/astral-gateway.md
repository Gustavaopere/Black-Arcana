# Astral Gateway

- ID: `asterismarcanum:astral_gateway`
- escola: Astral
- rarity: Legendary
- nível: 1
- mana: 300
- cooldown: 60 s
- cast: LONG, 40 ticks / 2 s, sem cast-time scaling
- radius: 8
- registry: **ativo**
- estado de catálogo: `EXACT REGISTRY / NON-SURVIVAL / REACHABILITY CONDITIONAL`

## Efeito

A implementação registrada transporta o `ServerPlayer` entre a dimensão Astral Sea e o destino de retorno mantido pelo provider.

O spell existe no registry atual, mas a própria release o trata como creative-only e o lang file o descreve como `not fully implemented or craftable`. Isso impede promovê-lo para a progressão survival canônica.

## Aquisição e condição

Há uma inconsistência real entre intenção editorial e superfícies estáticas de aquisição:

- a classe não sobrescreve `allowLooting()`;
- o `DefaultConfig` não desabilita crafting;
- a escola Astral usa `allowLooting=true` por default;
- o Astromancer gera scrolls aleatórios filtrados pela escola Astral.

Portanto o spell pode possuir caminho estático de loot/crafting se nenhum config/datapack efetivo do pack o bloquear. Como esse estado implantado não está fechado, a reachability permanece `CONDITIONAL`.

## Authority e dedup

Authority = Asterism Arcanum + pipeline de casting/teleport de Iron's. Black Arcana não deve criar segundo gateway, segunda cobrança de mana, perk dependente desse spell ou nova fonte de aquisição enquanto a condição survival não estiver fechada.

## Cobertura

`Astral Gateway` é o 11º registration do provider, mas permanece fora do strict count. Os outros 10 spells Astral possuem reachability survival catalogada separadamente.

Fonte: `../NON-SURVIVAL.md` e `../TECHNICAL-AUDIT.md`.
