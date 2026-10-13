# Stomp

- **Status:** PRESENTE — ativo
- **Spell ID:** `irons_spellbooks:stomp`
- **Provider/JAR:** Iron's Spells / `1.21.1-3.16.3`
- **Escola:** Nature
- **Níveis/raridade:** 1–5 / Uncommon → Legendary
- **Cast:** Long, 10 ticks
- **Mana/cooldown:** 50–90 / 16 s
- **Dano:** 8–16
- **Range:** 5–9 blocos com multiplier neutro
- **Interrupção:** `canBeInterrupted=false`

## Função e source audit

Cria uma tremor entity à frente do caster, alinhada ao ground level.

- spell power = 8 +2 por nível após o primeiro;
- damage = spell power;
- range = `floor(4 + spellLevel*entityPowerMultiplier)`;
- `StompAoe` recebe range, yaw, damage, owner e explosion radius usado para knockback;
- cast-time attribute é deliberadamente ignorado: `getEffectiveCastTime` retorna o cast time puro para preservar timing de animação;
- emite block particles do bloco do chão;
- finish sound `EARTHQUAKE_CAST`;
- animação `STOMP`.

## Authority / dedup

`StompAoe` é authority de path/hits/knockback. Não criar segundo tremor ou scan de targets. Friendly-fire, PvP/boss/summon policy, width/hit cadence e damage type fino: `NÃO VERIFICADO`.

## Verificação obrigatória

- dano 8–16; range 5–9; duração/lifetime da AoE `NÃO VERIFICADO`;
- scaling acima; caps extras `NÃO VERIFICADO`;
- obtenção/requisitos/focus/ritual: específicos `NÃO VERIFICADO`;
- VFX/som/animação source-auditados; textura/QA client-real `NÃO VERIFICADO`;
- fail-closed: provider AoE única.

## Fonte

- `https://iron.wiki/spells/` — consulta 2026-09-06.
- `StompSpell.java` — source 3.16.3.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`StompSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/nature/StompSpell.java) (source fixo 1.21.1-3.16.3).
- **ID de spell lido na classe:** `irons_spellbooks:stomp`; o ID pode divergir do título de exibição.
- **Config:** minRarity `UNCOMMON`; maxLevel `5`; cooldown `16` segundos; cast `LONG`.
- **Campos Java:** `baseManaCost`=`50`; `manaCostPerLevel`=`10`; `baseSpellPower`=`8`; `spellPowerPerLevel`=`2`; `castTime`=`10`.
- **Métodos no código:** `getUniqueInfo()`, `getCastFinishSound()`, `getCastType()`, `getEffectiveCastTime()`, `getDefaultConfig()`, `getSpellResource()`, `onCast()`, `getDamage()`, `getRange()`, `getCastStartAnimation()`, `getCastFinishAnimation()`.
- **Fórmulas numéricas com retorno direto:** `getDamage = getSpellPower(spellLevel, caster)`; `getRange = (int) (4 + spellLevel * getEntityPowerMultiplier(caster))`. Não são fórmulas completas de efeitos indiretos.
- **Pistas de execução (verificar semântica):** `addFreshEntity`.

**Contrato de perks:** escola `nature` não implica toxicidade, dano ácido, status ou transformação automática. Verificar aplicação real por helper, entidade, efeito ou damage source. Separar atributo nativo de mudar geometria/status/quantidade; exigir contrato real, caps, segurança e dedup; sem hook ⚠️ condicionado/fail-closed. Iron's controla cast/efeitos/mana; RPG Skill Tree perks/Mastery/gates; Black Arcana seu runtime mágico. QA real pendente. [Mapa global](../TECHNICAL-PERK-MAP.md).
