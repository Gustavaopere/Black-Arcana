# Acid Spit

- **Status:** PRESENTE — ativo
- **Provider/mod ID:** Iron's Spells / `irons_spellbooks`
- **Spell ID real:** `irons_spellbooks:acid_orb`
- **Classe:** `AcidOrbSpell`
- **JAR:** `irons_spellbooks-1.21.1-3.16.3.jar`
- **Escola:** Nature
- **Níveis/raridade:** 1–8 / Common → Legendary
- **Cast:** Long, 15 ticks
- **Mana/cooldown:** 40–110 / 15 s
- **Raio:** 3 blocos com multiplier neutro
- **Rend:** 20%–55% armor reduction
- **Duração:** 20 s com multiplier neutro

## Função e source audit 3.16.3

Spita uma orb de ácido que explode e aplica Rend. O source cria `AcidOrb`, dispara no look angle, adiciona componente vertical, injeta radius, rend amplifier e duration e então delega impacto/splash à entity.

- spell power base 1, sem scaling por nível;
- radius = `spellPower * 3`;
- rend amplifier = `level + 2`; tooltip converte `(amplifier+1)*5%`;
- duration = `spellPower * 20 * 20` ticks;
- sons `ACID_ORB_CHARGE`/`ACID_ORB_CAST`;
- animações `CHARGE_SPIT_ANIMATION`/`SPIT_FINISH_ANIMATION`;
- AI evita usar contra target com armor < 4.

## Authority / targets / deduplicação

`AcidOrb` é authority do impacto/splash; Rend effect é authority da redução de armor. Friendly-fire, PvP, boss/summon eligibility e impacto fino: `NÃO VERIFICADO`. Não criar segunda explosão nem reaplicar Rend por bridge.

## Verificação obrigatória

- recurso: mana; dano direto numérico: `NÃO VERIFICADO` na spell class;
- damage type: `NÃO VERIFICADO`;
- alcance/lifetime da orb: `NÃO VERIFICADO`;
- scaling/caps: radius/duration acima; Rend por nível; caps extras `NÃO VERIFICADO`;
- obtenção/loot/craft/trade/focus/ritual: pipeline geral scroll/spellbook; rota específica `NÃO VERIFICADO`;
- VFX/textura/QA client-real: `NÃO VERIFICADO` além de sons/animações auditados;
- fail-closed: preservar entity/effect provider-native.

## Fonte

- `https://iron.wiki/spells/` — consulta 2026-09-06.
- `AcidOrbSpell.java` — source 3.16.3 pinado.
