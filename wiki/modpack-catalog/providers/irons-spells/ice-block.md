# Ice Block

- **Status no modpack:** PRESENTE — ativo no catálogo atual
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **Spell ID:** `irons_spellbooks:ice_block`
- **JAR/versão instalada:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Ice
- **Níveis:** 1–6
- **Raridade:** Rare → Legendary
- **Cast:** Long
- **Mana:** 40–90
- **Cooldown:** 15 s
- **Dano atual:** 14–24

## O que faz

Conjura um grande bloco de gelo acima de uma criatura ou bloco; após atraso ele cai e explode em dano frost em área, com dano adicional às criaturas atingidas durante a queda.

## Source audit 3.16.3 — commit `e4056af...`

- cast time 25 ticks;
- pre-cast target helper 48 blocos; fallback raycast de 32 blocos;
- cria `IceBlockProjectile` acima do target/ponto, com spawn height adaptado;
- airtime 35 ticks com target e 25 sem target;
- damage = spell power (base 14, +2/level);
- damage source adiciona 100 freeze ticks e `iFrames(0)`;
- som de cast `ICE_BLOCK_CAST`.

A liquidação fina do impacto/explosão pertence a `IceBlockProjectile` e não foi auditada nesta ficha.

## Targets / PvP / bosses / summons

- **Targeting:** helper 48 / fallback raycast 32 no source.
- **Players em PvP, bosses e summons:** policy específica de impacto `NÃO VERIFICADO`.
- **World collision:** o projectile pode usar `noPhysics` quando nasce em colisão; demais world-mutation semantics `NÃO VERIFICADO`.

## Obtenção, requisitos e aprendizado

- pipeline geral de scrolls/spellbooks;
- rotas específicas `NÃO VERIFICADO`;
- requisitos adicionais `NÃO VERIFICADO`;
- itens/focus/rituais específicos `NÃO VERIFICADO`.

## Integrações / QA / fail-closed

- **Projectile authority:** `IceBlockProjectile`.
- bridge específica `NÃO VERIFICADO`.
- impacto/AoE interno, VFX finais e QA client-real `NÃO VERIFICADO`.
- Não reaplicar queda, freeze, hit ou explosão por fora da entidade provider.

## Deduplicação

Já cobre falling Ice projectile com impacto + AoE frost e freeze semantics.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/` — consulta 2026-09-06.
- Source 3.16.3 `e4056af...`: `IceBlockSpell.java` + `gradle.properties`.
