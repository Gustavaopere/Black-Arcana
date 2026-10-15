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

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`ThunderstormSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/lightning/ThunderstormSpell.java) (source fixo 1.21.1-3.16.3).
- **ID de spell lido na classe:** `irons_spellbooks:thunderstorm` (NÃO EXTRAÍDO implica revisar registry).
- **Config:** minRarity `RARE`; maxLevel `8`; cooldown `120` segundos; cast `LONG`.
- **Campos Java:** `baseManaCost`=`70`; `manaCostPerLevel`=`10`; `baseSpellPower`=`8`; `spellPowerPerLevel`=`1`; `castTime`=`40`.
- **Métodos no código:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastStartSound()`, `onCast()`, `getAmplifierForLevel()`, `getDurationTicks()`.
- **Fórmulas numéricas com retorno direto:** `getAmplifierForLevel = 8 + (int) ((spellLevel - 1) * getEntityPowerMultiplier(caster))`; `getDurationTicks = (int) ((20 + (2 * (spellLevel - 1) * getEntityPowerMultiplier(caster))) * 20)`. Não são fórmulas completas de efeitos indiretos.
- **Pistas de execução (verificar semântica):** `MobEffectInstance`, `addEffect`.

**Contrato de perks:** escola `lightning` não prova, sozinha, dano elétrico, arcos em cadeia ou stun. Conferir classe de descarga/targeting, i-frames, limites de saltos, duração e efeitos de bloco. Atributo nativo ≠ hook para raio, count ou chain. Exigir contrato de provider, cap e anti-proc-recursivo; caso contrário ⚠️ condicionado/fail-closed. Iron's controla cast/mana/efeitos, RPG Skill Tree perks/Mastery/gates, Black Arcana runtime mágico próprio. QA real pendente. [Mapa global](../TECHNICAL-PERK-MAP.md).
