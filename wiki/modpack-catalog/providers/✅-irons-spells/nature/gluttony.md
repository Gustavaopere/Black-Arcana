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

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`GluttonySpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/nature/GluttonySpell.java) (source fixo 1.21.1-3.16.3).
- **ID de spell lido na classe:** `irons_spellbooks:gluttony`; o ID pode divergir do título de exibição.
- **Config:** minRarity `COMMON`; maxLevel `5`; cooldown `90` segundos; cast `INSTANT`.
- **Campos Java:** `baseManaCost`=`35`; `manaCostPerLevel`=`0`; `baseSpellPower`=`30`; `spellPowerPerLevel`=`0`; `castTime`=`0`.
- **Métodos no código:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `onCast()`, `getManaRatio()`, `getCastStartAnimation()`.
- **Fórmulas numéricas com retorno direto:** `getManaRatio = GluttonyEffect.ratioForAmplifier(spellLevel - 1)`. Não são fórmulas completas de efeitos indiretos.
- **Pistas de execução (verificar semântica):** `MobEffectInstance`, `addEffect`, `MobEffectRegistry`.

**Contrato de perks:** escola `nature` não implica toxicidade, dano ácido, status ou transformação automática. Verificar aplicação real por helper, entidade, efeito ou damage source. Separar atributo nativo de mudar geometria/status/quantidade; exigir contrato real, caps, segurança e dedup; sem hook ⚠️ condicionado/fail-closed. Iron's controla cast/efeitos/mana; RPG Skill Tree perks/Mastery/gates; Black Arcana seu runtime mágico. QA real pendente. [Mapa global](../TECHNICAL-PERK-MAP.md).
