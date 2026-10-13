# Dragon's Breath

- **Provider:** Iron's Spells 'n Spellbooks
- **Escola:** Ender
- **Níveis:** 1–10
- **Raridade:** Common → Legendary
- **Cast:** Continuous
- **Mana:** 5–14
- **Cooldown:** 12 s
- **Dano:** 1–7.75

## O que faz

Canaliza um cone de dragon breath. Ao acertar criaturas há chance de criar uma poça de dragon breath aos pés do alvo, adicionando controle/dano de área persistente.

## Obtenção e aprendizado

Pipeline padrão do Iron's; Ender Pearl é o Focus Ender.

## Deduplicação

Ocupa cone Ender + criação condicional de área persistente.

## VFX / animação / áudio

A catalogar no runtime.

## Fonte

`https://iron.wiki/spells/`.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`DragonBreathSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/ender/DragonBreathSpell.java), pin `e4056af90302d37eb1739f5ff05020b020e6e252` (Iron's 1.21.1-3.16.3).
- **ID no source:** `irons_spellbooks:dragon_breath`; escola `ender`.
- **Config na classe:** minRarity `NÃO EXTRAÍDO`, maxLevel `NÃO EXTRAÍDO`, cooldown `NÃO EXTRAÍDO` segundos, cast `NÃO EXTRAÍDO`.
- **Campos Java:** `baseManaCost`=`5`; `manaCostPerLevel`=`1`; `baseSpellPower`=`0`; `spellPowerPerLevel`=`1`; `castTime`=`100`.
- **Métodos para localizar no Codex:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastStartSound()`, `getCastFinishSound()`, `onCast()`, `getDamage()`.
- **Fórmulas com retorno numérico direto verificadas nesta classe:** `getDamage = 1 + getSpellPower(spellLevel, caster) * .75f`. Essas fórmulas não cobrem cálculos imperativos ou de entidades auxiliares.
- **Pistas técnicas detectadas:** `addFreshEntity`; verificar semântica na classe.

**Orientação para perks:** estudar as chamadas de `onCast`, `checkPreCastConditions` e os métodos acima antes de alterar alvo/raio/duração/dano; `getSpellPower` e custo aplicam config/atributos nativos. A disponibilidade de eventos genéricos não comprova alteração de variáveis locais ou entidades. Sem adapter verificado, **⚠️ condicionado / fail-closed**. Preserve casting do Iron's, Mastery/perks/gates do RPG Skill Tree e runtime próprio do Black Arcana. Registro estático, sem QA físico. [Contrato de referência](../TECHNICAL-PERK-MAP.md).
