# Snowball

- **Status no modpack:** PRESENTE — ativo no catálogo atual
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **Spell ID:** `irons_spellbooks:snowball`
- **JAR/versão instalada:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Ice
- **Níveis:** 1–5
- **Raridade:** Uncommon → Legendary
- **Cast:** Long
- **Mana:** 40–48
- **Cooldown:** 12 s
- **Raio atual:** 4–6 blocos
- **Duração do frosty field atual:** 10 s

## O que faz

Conjura e lança uma grande snowball que explode em um frosty field e aplica Chilled às criaturas na área. Pela semântica atual, alvos Chilled que se tornam fully frozen são entombados em gelo.

## Source audit 3.16.3 — commit `e4056af...`

- cast time 20 ticks;
- cria entidade `Snowball`, dispara pelo look angle e adiciona componente vertical ao movimento;
- radius = `3.5 + level * 0.5`;
- duration = `200 * sqrt(entityPowerMultiplier)` ticks;
- o spell passa a duration para o campo `damage` da entidade Snowball — detalhe interno da entidade, não dano nominal do spell;
- animação `ANIMATION_CHARGED_CAST`, som inicial `FROSTWAVE_PREPARE`.

O changelog oficial 3.14.2 registra que a explosão inicial de Snowball aplica Chilled, não freeze direto, e que Chilled fully-frozen gera Ice Tomb hostil.

## Targets / PvP / bosses / summons

- **Targeting:** projectile forward; área definida pela `Snowball` no impacto.
- **Players em PvP, bosses e summons:** friendly-fire/imunidades/Chilled eligibility `NÃO VERIFICADO` nesta ficha.
- A implementação fina do field pertence à entidade `Snowball` e permanece `NÃO VERIFICADO` além do outcome público.

## Obtenção, requisitos e aprendizado

- pipeline geral de scrolls/spellbooks;
- rotas específicas `NÃO VERIFICADO`;
- requisitos adicionais `NÃO VERIFICADO`;
- itens/focus/rituais específicos `NÃO VERIFICADO`.

## Integrações / QA / fail-closed

- **Projectile/field authority:** entidade `Snowball`.
- bridge específica `NÃO VERIFICADO`.
- field settlement/VFX finais e QA client-real `NÃO VERIFICADO`.
- Não duplicar explosion, Chilled ou field ticks.

## Deduplicação

Já cobre projectile Ice de impacto que cria frosty field + Chilled.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/` — consulta 2026-09-06.
- Changelog oficial 3.14.2.
- Source 3.16.3 `e4056af...`: `SnowballSpell.java` + `gradle.properties`.
