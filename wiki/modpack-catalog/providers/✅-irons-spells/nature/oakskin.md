# Oakskin

- **Status:** PRESENTE — ativo
- **Spell ID:** `irons_spellbooks:oakskin`
- **Provider/JAR:** Iron's Spells / `1.21.1-3.16.3`
- **Escola:** Nature
- **Níveis/raridade:** 1–8 / Common → Legendary
- **Cast:** Instant, 0 ticks
- **Mana/cooldown:** 25–95 / 90 s
- **Damage Reduction:** 20% com power multiplier neutro
- **Speed:** -25%
- **Duração:** 20–41 s

## Source audit

Antes de aplicar o spell, remove OAKSKIN/OakskinData preexistentes para limpar efeitos colaterais de elixir. Aplica `MobEffectRegistry.OAKSKIN` por `spellPower*20`, amplifier fixo 2, envia `OakskinParticlesPacket`.

- spell power = 20 +3/level;
- `OakskinEffect`: base reduction .10 + .05*amplifier, portanto 20% em amplifier 2, multiplicado por entity power e capado em 75%;
- `SLOWNESS_MAGNITUDE=.25`;
- intercepta `LivingIncomingDamageEvent` e multiplica incoming damage por `1-reduction`;
- elixir força multiplier 1 para impedir scaling por spell power;
- partículas de oak log/firefly são emitidas ao reduzir dano.

## Authority / dedup

`OAKSKIN`/`OakskinEffect` é authority de mitigation e slow. Não aplicar 20% de redução novamente fora do event. Interação/ordem com armor, resistances e outros listeners: `NÃO VERIFICADO`.

## Verificação obrigatória

- dano/cura: não aplicável;
- targets/range: self;
- scaling/cap: duration 20–41s; reduction formula + cap75%; amplifier fixo;
- obtenção/focus/ritual: específicos `NÃO VERIFICADO`;
- som `OAKSKIN_CAST`, animação `SELF_CAST_ANIMATION`, packet/impact particles confirmados; textura/QA final `NÃO VERIFICADO`;
- fail-closed: usar effect/data provider, sem segunda mitigation ledger.

## Fonte

- `https://iron.wiki/spells/` — consulta 2026-09-06.
- `OakskinSpell.java` + `OakskinEffect.java` — source 3.16.3.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`OakskinSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/nature/OakskinSpell.java) (source fixo 1.21.1-3.16.3).
- **ID de spell lido na classe:** `irons_spellbooks:oakskin`; o ID pode divergir do título de exibição.
- **Config:** minRarity `COMMON`; maxLevel `8`; cooldown `90` segundos; cast `INSTANT`.
- **Campos Java:** `baseManaCost`=`25`; `manaCostPerLevel`=`10`; `baseSpellPower`=`20`; `spellPowerPerLevel`=`3`; `castTime`=`0`.
- **Métodos no código:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastStartSound()`, `getCastFinishSound()`, `onCast()`, `getAmplifier()`, `getPercentDamage()`, `getCastStartAnimation()`.
- **Fórmulas numéricas com retorno direto:** `getAmplifier = 2`; `getPercentDamage = OakskinEffect.getReductionAmount(getAmplifier(spellLevel, entity), entity) * 100`. Não são fórmulas completas de efeitos indiretos.
- **Pistas de execução (verificar semântica):** `MobEffectInstance`, `addEffect`, `MobEffectRegistry`.

**Contrato de perks:** escola `nature` não implica toxicidade, dano ácido, status ou transformação automática. Verificar aplicação real por helper, entidade, efeito ou damage source. Separar atributo nativo de mudar geometria/status/quantidade; exigir contrato real, caps, segurança e dedup; sem hook ⚠️ condicionado/fail-closed. Iron's controla cast/efeitos/mana; RPG Skill Tree perks/Mastery/gates; Black Arcana seu runtime mágico. QA real pendente. [Mapa global](../TECHNICAL-PERK-MAP.md).
