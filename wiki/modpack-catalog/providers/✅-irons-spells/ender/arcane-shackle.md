# Arcane Shackle

- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR:** `irons_spellbooks-1.21.1-3.16.3.jar`
- **Escola:** Ender
- **Níveis:** 1–8
- **Raridade:** Rare → Legendary
- **Cast:** Long
- **Mana:** 40–96
- **Cooldown:** 45 s
- **HP das correntes:** 15
- **Duração:** 11–25 s
- **Alcance listado:** 5 blocos

## O que faz

Lança correntes arcanas que prendem uma criatura ao chão. Em caso de erro do disparo, correntes podem buscar criaturas próximas distintas. As correntes podem ser danificadas ou dissipadas.

## Obtenção e aprendizado

Pipeline padrão do Iron's: scroll/progressão, spell book e Inscription Table; Ender usa Ender Pearl como Focus no Scroll Forge.

## Deduplicação

Ocupa tether/immobilization por objetos quebráveis. Ordem/Vínculo precisam de semântica de lei/contrato real para não duplicar este spell.

## VFX / animação / áudio

A catalogar no runtime.

## Fonte

`https://iron.wiki/spells/` · `https://iron.wiki/schools/` · `https://iron.wiki/progression/`.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`ArcaneShackleSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/ender/ArcaneShackleSpell.java), pin `e4056af90302d37eb1739f5ff05020b020e6e252` (Iron's 1.21.1-3.16.3).
- **ID no source:** `irons_spellbooks:arcane_shackle`; escola `ender`.
- **Config na classe:** minRarity `NÃO EXTRAÍDO`, maxLevel `NÃO EXTRAÍDO`, cooldown `NÃO EXTRAÍDO` segundos, cast `NÃO EXTRAÍDO`.
- **Campos Java:** `baseManaCost`=`40`; `manaCostPerLevel`=`8`; `baseSpellPower`=`6`; `spellPowerPerLevel`=`2`; `castTime`=`10`.
- **Métodos para localizar no Codex:** `getUniqueInfo()`, `getDefaultConfig()`, `getCastType()`, `getSpellResource()`, `getCastStartSound()`, `getCastFinishSound()`, `onCast()`, `getChainHealth()`, `getChainDuration()`, `getLashRadius()`, `getCastStartAnimation()`, `getCastFinishAnimation()`.
- **Fórmulas com retorno numérico direto verificadas nesta classe:** `getChainHealth = 15 * getEntityPowerMultiplier(entity)`; `getChainDuration = (int) (100 + getSpellPower(spellLevel, entity) * 20)`; `getLashRadius = 5f`. Essas fórmulas não cobrem cálculos imperativos ou de entidades auxiliares.
- **Pistas técnicas detectadas:** `addFreshEntity`; verificar semântica na classe.

**Orientação para perks:** estudar as chamadas de `onCast`, `checkPreCastConditions` e os métodos acima antes de alterar alvo/raio/duração/dano; `getSpellPower` e custo aplicam config/atributos nativos. A disponibilidade de eventos genéricos não comprova alteração de variáveis locais ou entidades. Sem adapter verificado, **⚠️ condicionado / fail-closed**. Preserve casting do Iron's, Mastery/perks/gates do RPG Skill Tree e runtime próprio do Black Arcana. Registro estático, sem QA físico. [Contrato de referência](../TECHNICAL-PERK-MAP.md).
