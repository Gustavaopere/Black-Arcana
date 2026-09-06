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

## Source audit 3.16.3 — commit `e4056af...`

- cast time 20 ticks;
- usa `SummonedPolarBear`, `SummonManager`, `SummonedEntitiesCastData` e player recasts;
- recast count = 2; o helper de recast do summon resolve término/unsummon;
- summon lifetime = `20 * 60 * 10` ticks (10 min);
- HP = `(20 + level * 4) * entityPowerMultiplier`;
- damage = spell power (base 4, +1/level);
- publica `SpellSummonEvent<>(caster, polarBear, spellId, spellLevel)` antes de adicionar a criatura;
- define attack damage/max health, cura o summon ao máximo e registra no `SummonManager`;
- som inicial `EVOKER_PREPARE_SUMMON`.

## Targets / PvP / bosses / summons

- **Entidade criada:** `SummonedPolarBear` com owner/caster explícito.
- **PvP, bosses e seleção de targets pelo AI:** `NÃO VERIFICADO` nesta ficha; não reconstruir a AI ou friendly-fire policy por fora.
- **Summon lifecycle:** ownership/recast source-auditados; persistência/login/dimension behavior fino deve continuar provider-native e fica `NÃO VERIFICADO` nesta ficha quando não lido diretamente.

## Obtenção, requisitos e aprendizado

- pipeline geral de scrolls/spellbooks;
- rotas específicas `NÃO VERIFICADO`;
- requisitos adicionais `NÃO VERIFICADO`;
- itens/focus/rituais específicos `NÃO VERIFICADO`.

## Integrações / QA / fail-closed

- **Hooks/authority:** `SpellSummonEvent` + `SummonManager` + recast system.
- bridge específica `NÃO VERIFICADO`.
- mount/AI/persistence cross-dimension e QA client/modpack real `NÃO VERIFICADO` nesta ficha.
- Não spawnar segundo bear, manter summon após unsummon provider ou duplicar stats/eventos.

## Deduplicação

Já cobre summon Ice persistente/recastable de combat mount. Novos summons glaciais precisam de papel distinto, não apenas outro follower/tank/mount equivalente.

## Matriz obrigatória de verificação

- **Status/provider/mod ID/JAR/spell ID/escola/tipo:** confirmados; tipo funcional = summon/combat mount Ice.
- **Descrição funcional:** confirmada pelo catálogo; AI fina `NÃO VERIFICADO`.
- **Níveis/raridade:** 1–10 / Rare → Legendary.
- **Cast type / cast time / channel:** `LONG` / 20 ticks / não `CONTINUOUS`; interrupção fina `NÃO VERIFICADO`.
- **Recurso/custo:** mana / 50–140; fórmula fina de custo `NÃO VERIFICADO`.
- **Cooldown:** 180 s.
- **Dano/cura/tipo de dano:** bear attack damage 4–13; isso é atributo do summon, não dano direto do cast; tipo de ataques/mitigação `NÃO VERIFICADO`; cura apenas inicializa summon em max health, não é heal de target do spell.
- **Alcance/raio/área/duração:** summon nasce na posição do caster; lifetime source 10 min; follow/aggro range e área `NÃO VERIFICADO`.
- **Scaling/fórmulas/caps:** HP `(20+level*4)*entityPowerMultiplier`; damage = spell power base4 +1/level; recast count2; caps além de nível10 `NÃO VERIFICADO`.
- **Targets/PvP/bosses/summons:** summon ownership confirmada; AI/PvP/boss targeting `NÃO VERIFICADO`.
- **Condições/requisitos:** ausência de recast ativo é gate confirmado; demais requisitos `NÃO VERIFICADO`.
- **Obtenção/fabricação/ganho/aprendizado:** pipeline geral; rotas específicas `NÃO VERIFICADO`.
- **Itens/focus/rituais:** específicos `NÃO VERIFICADO`.
- **VFX/partículas/textura/animação/áudio:** `EVOKER_PREPARE_SUMMON` confirmado; partículas/textura/animação `NÃO VERIFICADO`.
- **Integrações/bridges:** `SpellSummonEvent`, `SummonManager`, recasts são hooks/authority; outras bridges `NÃO VERIFICADO`.
- **Deduplicação/sobreposição:** conclusão baseada no source 3.16.3 pinado; summon novo requer papel mecânico distinto.
- **Bugs/QA/fail-closed:** lifecycle cross-dimension/login e QA real `NÃO VERIFICADO`; não duplicar summon/stats/recast/event.
- **Fonte/evidência/estado:** catálogo + source 3.16.3.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/` — consulta 2026-09-06.
- Source 3.16.3 `e4056af...`: `SummonPolarBearSpell.java` + `gradle.properties`.
