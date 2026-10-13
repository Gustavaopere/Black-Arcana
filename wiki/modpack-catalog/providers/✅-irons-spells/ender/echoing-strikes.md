# Echoing Strikes

- **Provider:** Iron's Spells 'n Spellbooks
- **Escola:** Ender
- **Níveis:** 1–5
- **Raridade:** Rare → Legendary
- **Cast:** Instant
- **Mana:** 50–90
- **Cooldown:** 60 s
- **Dano dos ecos:** 75% do ataque original
- **Ecos:** 3–7 hits

## O que faz

Imbui ataques não mágicos para gerar ecos ofensivos: espadas espectrais de área ou flechas mágicas contra o mesmo alvo. Cada eco reproduz uma fração do dano original.

## Obtenção e aprendizado

Pipeline padrão do Iron's; Ender Pearl é o Focus Ender.

## Deduplicação

Ocupa proc/echo de ataques físicos. Não confundir com duplicação temporal/causal futura de Ordem ou Caos.

## VFX / animação / áudio

A catalogar no runtime.

## Fonte

`https://iron.wiki/spells/`.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`EchoingStrikesSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/ender/EchoingStrikesSpell.java), pin `e4056af90302d37eb1739f5ff05020b020e6e252` (Iron's 1.21.1-3.16.3).
- **ID no source:** `irons_spellbooks:echoing_strikes`; escola `ender`.
- **Config na classe:** minRarity `RARE`, maxLevel `5`, cooldown `60` segundos, cast `INSTANT`.
- **Campos Java:** `baseManaCost`=`50`; `manaCostPerLevel`=`10`; `baseSpellPower`=`20`; `spellPowerPerLevel`=`5`; `castTime`=`0`.
- **Métodos para localizar no Codex:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastFinishSound()`, `onCast()`, `onClientCast()`, `getHitCount()`, `getAmplifierForLevel()`, `getCastStartAnimation()`, `getDamageSource()`.
- **Fórmulas com retorno numérico direto verificadas nesta classe:** `getHitCount = spellLevel + 2`; `getAmplifierForLevel = (int) (.75 / EchoingStrikesEffect.PERCENT_PER_AMPLIFIER)`. Essas fórmulas não cobrem cálculos imperativos ou de entidades auxiliares.
- **Pistas técnicas detectadas:** `MobEffectInstance`, `SpellDamageSource`, `addEffect`; verificar semântica na classe.

**Orientação para perks:** estudar as chamadas de `onCast`, `checkPreCastConditions` e os métodos acima antes de alterar alvo/raio/duração/dano; `getSpellPower` e custo aplicam config/atributos nativos. A disponibilidade de eventos genéricos não comprova alteração de variáveis locais ou entidades. Sem adapter verificado, **⚠️ condicionado / fail-closed**. Preserve casting do Iron's, Mastery/perks/gates do RPG Skill Tree e runtime próprio do Black Arcana. Registro estático, sem QA físico. [Contrato de referência](../TECHNICAL-PERK-MAP.md).
