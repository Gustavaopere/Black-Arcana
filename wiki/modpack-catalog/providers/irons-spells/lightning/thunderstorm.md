# Thunderstorm

- **Status:** PRESENTE — ativo
- **Provider/mod ID:** Iron's Spells / `irons_spellbooks`
- **Spell ID:** `irons_spellbooks:thunderstorm`
- **JAR:** `irons_spellbooks-1.21.1-3.16.3.jar`
- **Escola:** Lightning
- **Níveis:** 1–8
- **Raridade:** Rare → Legendary
- **Cast:** Long
- **Cast time:** 40 ticks / 2 s
- **Mana:** 70–140
- **Cooldown:** 120 s
- **Dano publicado:** 8–15
- **Raio publicado/source-facing:** 20 blocos
- **Duração:** 20–34 s
- **Cadência pública:** pequeno lightning strike a cada 2 s

## O que faz

Aplica ao caster um estado de thunderstorm persistente que atinge criaturas próximas e visíveis periodicamente.

## Source audit 3.16.3

- aplica `MobEffectRegistry.THUNDERSTORM` ao caster;
- amplifier = `8 + floor((level-1)*entityPowerMultiplier)`;
- duração = `(20 + 2*(level-1)*entityPowerMultiplier)*20` ticks;
- dano exibido é resolvido por `ThunderstormEffect.getDamageFromAmplifier(...)`;
- radius exposto no tooltip = 20;
- cast start sound `THUNDERSTORM_PREPARE`;
- cast VFX cria fog thunder light/dark e zap particles ao redor do caster.

A seleção periódica de targets, LOS, cadence e damage settlement pertencem ao `ThunderstormEffect`; o catálogo oficial confirma raio 20 e strike a cada 2 s.

## Targets / dedup

- effect owner: caster;
- target selection fine/PvP/boss/summon/friendly-fire dentro do effect: `NÃO VERIFICADO` nesta ficha;
- não criar scheduler paralelo de lightning. `THUNDERSTORM`/`ThunderstormEffect` é a authority temporal.

## Matriz obrigatória

- status/provider/JAR/ID/escola/tipo: confirmado; timed self-effect/AoE;
- níveis/raridade: 1–8 / Rare→Legendary;
- cast: Long 40 ticks;
- mana/cooldown: 70–140 / 120 s;
- dano: 8–15 player-facing, helper do effect source; damage type fino `NÃO VERIFICADO`;
- raio/duração: 20 / 20–34 s com multiplier source;
- scaling: amplifier e duration formulas acima;
- targets/PvP/boss/summon: effect-native, detalhes `NÃO VERIFICADO`;
- obtenção/requisitos/itens: específicos `NÃO VERIFICADO`;
- VFX/audio: cast VFX e prepare sound confirmados; efeitos periódicos finais `NÃO VERIFICADO`;
- bridges/QA: effect authority, não duplicar scheduler/strike.

## Fonte

- `https://iron.wiki/spells/` — consulta 2026-09-06.
- Changelog 3.16.2 registra VFX de cast para Thunderstorm.
- Source 3.16.3: `ThunderstormSpell.java` em `e4056af90302d37eb1739f5ff05020b020e6e252`.
