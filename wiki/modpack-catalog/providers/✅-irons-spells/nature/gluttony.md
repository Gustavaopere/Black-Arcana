# Gluttony

- **Status:** PRESENTE — ativo
- **Spell ID:** `irons_spellbooks:gluttony`
- **Provider/JAR:** Iron's Spells / `1.21.1-3.16.3`
- **Escola:** Nature
- **Níveis/raridade:** 1–5 / Common → Legendary
- **Cast:** Instant, 0 ticks
- **Mana/cooldown:** 35 fixo / 90 s
- **Mana Recovery:** 2–4 por ponto de nutrition
- **Duração:** 30 s

## Source audit

Aplica `GLUTTONY` por 600 ticks, amplifier `level-1`. `GluttonyEffect` escuta `LivingEntityUseItemEvent.Finish`; server-side, se o item consumido possui FoodProperties e o eater tem GLUTTONY, obtém `MagicData`, adiciona `food.nutrition() * ratioForAmplifier(amplifier)` mana e sincroniza `SyncManaPacket` para ServerPlayer.

`ratioForAmplifier = (4 + amplifier)*0.5`, portanto 2.0–4.0.

**Limitação source explícita:** cake blocks não entram nesse evento/pipeline; o próprio comentário do provider reconhece isso.

## Authority / dedup

`LivingEntityUseItemEvent.Finish` + `GluttonyEffect` + `MagicData` são authority. Não creditar mana por hunger delta ou por tick, nem duplicar ganho ao observar o consumo em bridge.

## Verificação obrigatória

- dano/cura: não aplicável; recurso produzido = mana;
- targets: self; PvP/boss/summon não aplicável como target direto;
- range/área: self; duração 30 s;
- caps de mana/overflow: comportamento de `MagicData.addMana` `NÃO VERIFICADO` nesta ficha;
- obtenção/focus/ritual: específicos `NÃO VERIFICADO`;
- animação `SELF_CAST_ANIMATION`; áudio/VFX `NÃO VERIFICADO`;
- QA real: cake exclusion source-confirmed; demais foods/modded foods dependem de FoodProperties e ficam provider-native.

## Fonte

- `https://iron.wiki/spells/` — consulta 2026-09-06.
- `GluttonySpell.java` + `GluttonyEffect.java` — source 3.16.3.
