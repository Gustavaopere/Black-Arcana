# Counterspell

- **Provider:** Iron's Spells 'n Spellbooks
- **Escola:** Ender
- **Nível:** 1
- **Raridade:** Rare
- **Cast:** Instant
- **Mana:** 50
- **Cooldown:** 10 s

## O que faz

Interrompe casting de jogadores e mobs e remove/banishes várias entidades/efeitos mágicos reconhecidos pelo provider. A documentação atual cita summons, Shield, Blood Slash, creeper heads, Root e efeitos como Fortify/Evasion entre os casos tratados.

## Escalonamento

Sem níveis adicionais publicados.

## Obtenção e aprendizado

Pipeline padrão do Iron's; Ender Pearl é o Focus da escola Ender.

## Deduplicação

É a referência principal antes de qualquer counterspell de Ordem. Uma nova magia só é justificável se usar provenance/authority mais amplo e comprovado, não se apenas cancelar casts do Iron's novamente.

## VFX / animação / áudio

A catalogar no runtime.

## Fonte

`https://iron.wiki/spells/`.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`CounterspellSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/ender/CounterspellSpell.java), pin `e4056af90302d37eb1739f5ff05020b020e6e252` (Iron's 1.21.1-3.16.3).
- **ID no source:** `irons_spellbooks:counterspell`; escola `ender`.
- **Config na classe:** minRarity `RARE`, maxLevel `1`, cooldown `10` segundos, cast `INSTANT`.
- **Campos Java:** `baseManaCost`=`50`; `manaCostPerLevel`=`1`; `baseSpellPower`=`1`; `spellPowerPerLevel`=`1`; `castTime`=`0`.
- **Métodos para localizar no Codex:** `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `onCast()`.
- **Fórmulas com retorno numérico direto verificadas nesta classe:** não extraídas (inspecionar onCast/helpers/entidades). Essas fórmulas não cobrem cálculos imperativos ou de entidades auxiliares.
- **Pistas técnicas detectadas:** `RaycastBuilder`; verificar semântica na classe.

**Orientação para perks:** estudar as chamadas de `onCast`, `checkPreCastConditions` e os métodos acima antes de alterar alvo/raio/duração/dano; `getSpellPower` e custo aplicam config/atributos nativos. A disponibilidade de eventos genéricos não comprova alteração de variáveis locais ou entidades. Sem adapter verificado, **⚠️ condicionado / fail-closed**. Preserve casting do Iron's, Mastery/perks/gates do RPG Skill Tree e runtime próprio do Black Arcana. Registro estático, sem QA físico. [Contrato de referência](../TECHNICAL-PERK-MAP.md).
