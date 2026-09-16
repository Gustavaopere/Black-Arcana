# Charge

- **Status:** PRESENTE — ativo
- **Provider/mod ID:** Iron's Spells / `irons_spellbooks`
- **Spell ID:** `irons_spellbooks:charge`
- **JAR:** `irons_spellbooks-1.21.1-3.16.3.jar`
- **Escola:** Lightning
- **Níveis:** 1–3
- **Raridade:** Rare → Legendary
- **Cast:** Instant / 0 ticks
- **Mana:** 50–100
- **Cooldown:** 40 s
- **Duração publicada:** 30 s
- **Buffs publicados:** +5%→+15% Speed, Attack Damage e Lightning Spell Power

## O que faz

Aplica ao caster o estado `CHARGED`, reforçando mobilidade e capacidade ofensiva Lightning.

## Source audit 3.16.3

- `baseSpellPower=30`, `spellPowerPerLevel=8`;
- aplica `MobEffectRegistry.CHARGED` com amplifier `spellLevel-1`;
- duração = `30*20*entityPowerMultiplier` ticks;
- percentuais são resolvidos por constantes de `ChargeEffect` para speed, attack damage e lightning spell power;
- animação de início: `SELF_CAST_ANIMATION`.

O catálogo oficial atual publica 5% por nível para os três atributos; `ChargeEffect` permanece authority da aplicação real.

## Targets / integração

- target: self;
- PvP/boss/summon: não são targets diretos;
- não replicar os três attribute modifiers fora de `CHARGED`;
- interações com outros modifiers/stacking/caps: `NÃO VERIFICADO`.

## Matriz obrigatória

- status/provider/JAR/ID/escola/tipo: confirmado; self-buff;
- níveis/raridade: 1–3 / Rare→Legendary;
- cast/channel: Instant / 0 / não channel;
- mana/cooldown: 50–100 / 40 s;
- dano/cura: não aplicável diretamente;
- duração: 30 s com entity-power multiplier no source;
- scaling: amplifier level-1; +5% por nível player-facing; caps extras `NÃO VERIFICADO`;
- targets: self;
- obtenção/requisitos/itens: específicos `NÃO VERIFICADO`;
- VFX/animação/áudio: animação confirmada; VFX/áudio `NÃO VERIFICADO`;
- bridges/QA: `CHARGED`/`ChargeEffect` authority; demais `NÃO VERIFICADO`.

## Fonte

- `https://iron.wiki/spells/` — consulta 2026-09-06.
- Source 3.16.3: `ChargeSpell.java` em `e4056af90302d37eb1739f5ff05020b020e6e252`.
