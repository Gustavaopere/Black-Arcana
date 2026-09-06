# Summon Polar Bear

- **Status no modpack:** PRESENTE — ativo no catálogo atual
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **Spell ID:** `irons_spellbooks:summon_polar_bear`
- **JAR/versão instalada:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Ice
- **Níveis:** 1–10
- **Raridade:** Rare → Legendary
- **Cast:** Long
- **Mana:** 50–140
- **Cooldown:** 180 s
- **HP atual:** 24–60
- **Dano atual:** 4–13

## O que faz

Invoca um polar bear que segue, protege e luta pelo caster, além de servir como montaria.

## Snapshot upstream `e4056af...` — NÃO tratado como tag 3.16.3

- cast time 20 ticks;
- usa `SummonedPolarBear`, `SummonManager`, `SummonedEntitiesCastData` e player recasts;
- recast count = 2; o helper de recast do summon resolve término/unsummon;
- summon lifetime do snapshot = `20 * 60 * 10` ticks (10 min);
- HP = `(20 + level * 4) * entityPowerMultiplier`;
- damage = spell power (base 4, +1/level);
- publica `SpellSummonEvent<>(caster, polarBear, spellId, spellLevel)` antes de adicionar a criatura;
- define attack damage/max health, cura o summon ao máximo e registra no `SummonManager`;
- som inicial `EVOKER_PREPARE_SUMMON`.

## Targets / PvP / bosses / summons

- **Entidade criada:** `SummonedPolarBear` com owner/caster explícito.
- **PvP, bosses e seleção de targets pelo AI:** `NÃO VERIFICADO` nesta ficha; não reconstruir a AI ou friendly-fire policy por fora.
- **Summon lifecycle:** ownership/recast comprovados no snapshot; persistência/login/dimension behavior exato do JAR instalado deve continuar provider-native.

## Obtenção, requisitos e aprendizado

- pipeline geral de scrolls/spellbooks;
- rotas específicas `NÃO VERIFICADO`;
- requisitos adicionais `NÃO VERIFICADO`;
- itens/focus/rituais específicos `NÃO VERIFICADO`.

## Integrações / QA / fail-closed

- **Hooks/authority no snapshot:** `SpellSummonEvent` + `SummonManager` + recast system.
- bridge específica `NÃO VERIFICADO`.
- mount/AI/persistence cross-dimension e QA client/modpack real `NÃO VERIFICADO` nesta ficha.
- Não spawnar segundo bear, manter summon após unsummon provider ou duplicar stats/eventos.

## Deduplicação

Já cobre summon Ice persistente/recastable de combat mount. Novos summons glaciais precisam de papel distinto, não apenas outro follower/tank/mount equivalente.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/` — consulta 2026-09-06.
- Snapshot upstream `e4056af...`: `SummonPolarBearSpell.java`.
