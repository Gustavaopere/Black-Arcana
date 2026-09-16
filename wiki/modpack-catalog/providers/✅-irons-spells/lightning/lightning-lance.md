# Lightning Lance

- **Status:** PRESENTE — ativo
- **Provider/mod ID:** Iron's Spells / `irons_spellbooks`
- **Spell ID:** `irons_spellbooks:lightning_lance`
- **JAR:** `irons_spellbooks-1.21.1-3.16.3.jar`
- **Escola:** Lightning
- **Níveis:** 1–10
- **Raridade:** Uncommon → Legendary
- **Cast:** Long
- **Cast time:** 40 ticks / 2 s
- **Mana:** 50–140
- **Cooldown:** 8 s
- **Dano:** 14–32

## O que faz

Carrega e arremessa uma lança elétrica como javelin, causando alto dano ao alvo atingido.

## Source audit 3.16.3

- spell power = 14 +2/level;
- cria `LightningLanceProjectile`, posiciona à frente/altura dos olhos, dispara no look angle e injeta spell power como damage;
- cast start sound `LIGHTNING_LANCE_CAST`;
- finish sound `LIGHTNING_WOOSH_01`;
- animação `ANIMATION_CHARGED_CAST`.

## Authority / targets / dedup

- projectile/hit authority: `LightningLanceProjectile`;
- alcance, velocidade, piercing, friendly-fire, PvP/boss/summon policy e hit settlement fino: `NÃO VERIFICADO` nesta ficha;
- não criar segundo projectile/hit damage em bridge.

## Matriz obrigatória

- status/provider/JAR/ID/escola/tipo: confirmado; charged projectile;
- níveis/raridade: 1–10 / Uncommon→Legendary;
- cast/channel: Long / 40 ticks / não continuous;
- mana/cooldown: 50–140 / 8 s;
- dano: 14–32; type fino `NÃO VERIFICADO`;
- alcance/raio/duração: projectile-native, `NÃO VERIFICADO`;
- scaling: 14 +2/level; caps extras `NÃO VERIFICADO`;
- targets/PvP/boss/summon: `NÃO VERIFICADO`;
- obtenção/requisitos/itens: específicos `NÃO VERIFICADO`;
- VFX/audio/animação: dois sons + charged animation confirmados; VFX final `NÃO VERIFICADO`;
- bridges/QA: projectile authority, fail-closed.

## Fonte

- `https://iron.wiki/spells/` — consulta 2026-09-06.
- Source 3.16.3: `LightningLanceSpell.java` em `e4056af90302d37eb1739f5ff05020b020e6e252`.
