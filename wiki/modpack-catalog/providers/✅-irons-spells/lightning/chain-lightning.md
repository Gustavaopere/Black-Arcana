# Chain Lightning

- **Status:** PRESENTE — ativo
- **Provider/mod ID:** Iron's Spells / `irons_spellbooks`
- **Spell ID:** `irons_spellbooks:chain_lightning`
- **JAR:** `irons_spellbooks-1.21.1-3.16.3.jar`
- **Escola:** Lightning
- **Níveis:** 1–10
- **Raridade:** Uncommon → Legendary
- **Cast:** Instant / 0 ticks
- **Mana:** 25–88
- **Cooldown:** 20 s
- **Dano:** 6–15
- **Máx. targets publicado/source:** 4–13
- **Connection range:** 4–8,5 blocos

## O que faz

Inicia uma cadeia em uma criatura alvo e propaga zaps para criaturas próximas.

## Source audit 3.16.3

- pre-cast target helper até 32 blocos, inflation 0.35;
- exige `TargetEntityCastData` válido;
- cria entity `ChainLightning` com owner e alvo inicial;
- damage = spell power 6 +1/level;
- `maxConnections = 3 + spellLevel`;
- `range = 1 + spellPower * 0.5`.

A seleção de próximos targets, deduplicação interna e descarte pertencem à entity `ChainLightning`.

## Targets / PvP / bosses / summons

- alvo inicial: living/entity elegível pelo helper do provider até 32;
- target propagation policy, friendly-fire, PvP, bosses e summons: `NÃO VERIFICADO` nesta ficha;
- bridges não devem reconstruir a cadeia por busca própria.

## Obtenção / requisitos

Pipeline scroll/spellbook geral; rotas específicas, focus/ritual/craft/loot/trade: `NÃO VERIFICADO`.

## Deduplicação / causalidade

Já cobre chain-zap Lightning multi-target. `ChainLightning` é authority do graph de conexões; não contar cada salto como novo cast raiz nem criar segunda propagação fora da entity.

## Matriz obrigatória

- status/provider/JAR/ID/escola/tipo: confirmado;
- níveis/raridade: 1–10 / Uncommon→Legendary;
- cast: Instant 0, não channel;
- mana/cooldown: 25–88 / 20 s;
- dano: 6–15; type fino `NÃO VERIFICADO`;
- alcance: target inicial 32; conexão 4–8,5;
- scaling: dano +1/level, max connections 3+level, range 1+0.5*power;
- targets/PvP/boss/summon: policy fina `NÃO VERIFICADO`;
- obtenção/requisitos/itens/VFX/QA: específicos `NÃO VERIFICADO`;
- authority: `ChainLightning`, fail-closed.

## Fonte

- `https://iron.wiki/spells/` — consulta 2026-09-06.
- Source 3.16.3: `ChainLightningSpell.java` em `e4056af90302d37eb1739f5ff05020b020e6e252`.
