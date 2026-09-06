# Ball Lightning

- **Status:** PRESENTE — ativo
- **Provider/mod ID:** Iron's Spells / `irons_spellbooks`
- **Spell ID:** `irons_spellbooks:ball_lightning`
- **JAR:** `irons_spellbooks-1.21.1-3.16.3.jar`
- **Escola:** Lightning
- **Níveis:** 1–10
- **Raridade:** Common → Legendary
- **Cast:** Instant / 0 ticks
- **Mana:** 20–56
- **Cooldown:** 1 s
- **Dano:** 5–9,5

## O que faz

Conjura uma orb de lightning que avança lentamente, causa dano ao atravessar criaturas e ricocheteia em blocos, conforme o catálogo atual.

## Source audit 3.16.3

- `baseSpellPower=10`, `spellPowerPerLevel=1`;
- dano = `getSpellPower * 0.5`;
- cria `BallLightning`, posiciona na altura dos olhos, dispara na direção de visão, injeta o dano e adiciona a entity ao mundo;
- movimento, bounce, hit cadence, lifetime e seleção fina pertencem à `BallLightning` e não são reimplementados pela spell class.

## Authority / targets / fail-closed

- **Entity authority:** `BallLightning`.
- PvP, bosses, summons, friendly-fire, número de hits por entidade, lifetime e bounce fino: `NÃO VERIFICADO` nesta ficha.
- Não criar segunda orb, segundo bounce solver ou settlement paralelo de dano.

## Obtenção / requisitos

Pipeline geral de scroll/spellbook confirmado; rota específica, focus obrigatório, craft/loot/trade e requisitos extras: `NÃO VERIFICADO`.

## Matriz obrigatória

- status/provider/JAR/ID/escola/tipo: confirmado; projectile/entity Lightning;
- descrição: catálogo + spell class;
- níveis/raridade: 1–10 / Common→Legendary;
- cast/channel: Instant / 0 / não channel;
- mana: 20–56; cooldown 1 s;
- dano/tipo: 5–9,5; damage type fino da entity `NÃO VERIFICADO`;
- alcance/raio/duração: `NÃO VERIFICADO` na spell class;
- scaling: `(10 + level - 1) * 0.5`; caps extras `NÃO VERIFICADO`;
- targets/PvP/boss/summon: `NÃO VERIFICADO`;
- obtenção/requisitos/itens: específicos `NÃO VERIFICADO`;
- VFX/áudio/animação: `NÃO VERIFICADO` nesta ficha;
- bridge/QA: entity-native, demais `NÃO VERIFICADO`.

## Fonte

- `https://iron.wiki/spells/` — consulta 2026-09-06.
- Source 3.16.3: `BallLightningSpell.java` em `e4056af90302d37eb1739f5ff05020b020e6e252`.
