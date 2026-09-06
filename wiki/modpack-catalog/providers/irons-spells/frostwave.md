# Frostwave

- **Status no modpack:** PRESENTE — ativo no catálogo atual
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **Spell ID:** `irons_spellbooks:frostwave`
- **JAR/versão instalada:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Ice
- **Níveis:** 1–8
- **Raridade:** Common → Legendary
- **Cast:** Long
- **Mana:** 50–85
- **Cooldown:** 45 s
- **Duração atual:** 10–31 s
- **Raio atual:** 6,75–12 blocos

## O que faz

Emana uma onda radial de frost que aplica Chilled. Pela semântica atual do provider, criaturas Chilled que se tornam fully frozen são entombadas em gelo.

## Source audit 3.16.3 — commit `e4056af...`

- cast time 20 ticks;
- raio `6 + level * 0.75`;
- duração `spellPower * 20`, com spell power base 10 e +3/level;
- busca entidades em bounding box expandida e filtra `!DamageSources.isFriendlyFireBetween(target, caster)` + line of sight;
- aplica `MobEffectRegistry.CHILLED` às living entities dentro do raio;
- VFX: blastwave Ice, `ShockwaveParticlesPacket` e snowflakes;
- animações `CHARGE_RAISED_HAND` → `TOUCH_GROUND_ANIMATION`.

O changelog oficial 3.14.2 documenta a semântica atual de Chilled: ao ficar fully frozen, o efeito é consumido para encasar a criatura em um Ice Tomb hostil.

## Targets / PvP / bosses / summons

- **Friendly-fire e LOS:** filtros explícitos no source 3.16.3.
- **Players em PvP, bosses e summons:** resultado específico de `DamageSources.isFriendlyFireBetween`/imunidades de freeze `NÃO VERIFICADO`.
- Não substituir esses gates por lógica própria.

## Obtenção, requisitos e aprendizado

- pipeline geral de scrolls/spellbooks;
- rotas específicas `NÃO VERIFICADO`;
- requisitos adicionais `NÃO VERIFICADO`;
- itens/focus/rituais específicos `NÃO VERIFICADO`.

## Integrações / QA / fail-closed

- authorities: friendly-fire provider + `CHILLED`.
- bridge específica `NÃO VERIFICADO`.
- QA client/modpack real e imunidades/caps de freeze `NÃO VERIFICADO`.
- Não duplicar Chilled, tomb proc ou a wave radial.

## Deduplicação

Já cobre radial Ice debuff → Chilled → fully-frozen tomb semantics.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/` — consulta 2026-09-06.
- Changelog oficial 3.14.2.
- Source 3.16.3 `e4056af...`: `FrostwaveSpell.java` + `gradle.properties`.
