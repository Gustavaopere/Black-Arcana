# Blight

- **Status:** PRESENTE — ativo
- **Spell ID:** `irons_spellbooks:blight`
- **Provider/JAR:** Iron's Spells / `1.21.1-3.16.3`
- **Escola:** Nature
- **Níveis/raridade:** 1–8 / Rare → Legendary
- **Cast:** Long, 50 ticks
- **Mana/cooldown:** 60–200 / 90 s
- **Target helper:** até 32 blocos
- **Reduced Healing:** 10%–80%
- **Reduced outgoing Damage:** 5%–40%
- **Duração:** 30 s

## Source audit

Pre-cast usa `Utils.preCastTargetHelper(...,32,.35f)`. Com `TargetEntityCastData` válido, aplica `MobEffectRegistry.BLIGHT` por `spellPower*20*30`, amplifier `level-1`.

`BlightEffect` usa dois hooks:
- `LivingHealEvent`: healing multiplier = `1 - 0.10*level`;
- `LivingIncomingDamageEvent`: quando o atacante está Blighted, outgoing damage multiplier = `1 - 0.05*level`.

## Authority / dedup

`BLIGHT`/`BlightEffect` é authority dos dois debuffs. Não reduzir heal ou damage novamente em bridge. A ordem com outros modifiers/event listeners e floors finais: `NÃO VERIFICADO`.

## Verificação obrigatória

- dano direto/cura do cast: não aplicável;
- target/PvP/boss/summon: helper confirmado; eligibility final específica `NÃO VERIFICADO`;
- área: single target; range 32;
- scaling: amplifier level-1, duração 30 s; caps/floors adicionais `NÃO VERIFICADO`;
- obtenção/focus/ritual: específicos `NÃO VERIFICADO`;
- sons `BLIGHT_BEGIN`/`POISON_CAST`; VFX/animação final `NÃO VERIFICADO`;
- QA client-real: `NÃO VERIFICADO`; fail-closed pelo effect nativo.

## Fonte

- `https://iron.wiki/spells/` — consulta 2026-09-06.
- `BlightSpell.java` + `BlightEffect.java` — source 3.16.3.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`BlightSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/nature/BlightSpell.java) (source fixo 1.21.1-3.16.3).
- **ID de spell lido na classe:** `irons_spellbooks:blight`; o ID pode divergir do título de exibição.
- **Config:** minRarity `RARE`; maxLevel `8`; cooldown `90` segundos; cast `LONG`.
- **Campos Java:** `baseManaCost`=`60`; `manaCostPerLevel`=`20`; `baseSpellPower`=`1`; `spellPowerPerLevel`=`0`; `castTime`=`50`.
- **Métodos no código:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastStartSound()`, `getCastFinishSound()`, `checkPreCastConditions()`, `onCast()`, `getAmplifier()`, `getDuration()`.
- **Fórmulas numéricas com retorno direto:** `getAmplifier = (int) (spellLevel - 1)`; `getDuration = (int) (getSpellPower(spellLevel, caster) * 20 * 30)`. Não são fórmulas completas de efeitos indiretos.
- **Pistas de execução (verificar semântica):** `TargetEntityCastData`, `MobEffectInstance`, `addEffect`, `MobEffectRegistry`.

**Contrato de perks:** escola `nature` não implica toxicidade, dano ácido, status ou transformação automática. Verificar aplicação real por helper, entidade, efeito ou damage source. Separar atributo nativo de mudar geometria/status/quantidade; exigir contrato real, caps, segurança e dedup; sem hook ⚠️ condicionado/fail-closed. Iron's controla cast/efeitos/mana; RPG Skill Tree perks/Mastery/gates; Black Arcana seu runtime mágico. QA real pendente. [Mapa global](../TECHNICAL-PERK-MAP.md).
