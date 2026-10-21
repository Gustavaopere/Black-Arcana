# Telekinesis

- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR:** `irons_spellbooks-1.21.1-3.16.3.jar`
- **Escola:** Eldritch
- **Níveis:** 1–5
- **Raridade:** Legendary
- **Tipo de cast:** Continuous
- **Recurso:** mana do Iron's
- **Custo:** 25 mana
- **Cooldown:** 35 s
- **Alcance:** 12–20 blocos
- **Dano:** sem dano mágico direto listado; deslocamento pode resultar em dano cinético

## O que faz

Agarra uma criatura com força espectral e a força em direção ao ponto indicado pelo olhar do caster. O alvo continua sujeito a consequências cinéticas do deslocamento.

## Escalonamento

O alcance cresce com o nível; o custo listado permanece 25. Intensidade/velocidade de deslocamento e fórmula cinética serão verificadas separadamente.

## Obtenção e aprendizado

Ancient Knowledge Fragments → Eldritch Manuscript → aprendizado; Echo Shard é o Focus posterior.

## Deduplicação

É o principal bloqueio contra uma “telecinese genérica” nova. A Magia do Caos só deverá usar telecinese se acrescentar causalidade/entropia/regras próprias, não apenas puxar/empurrar entidades.

## VFX / animação / áudio

A catalogar visualmente; futuras melhorias devem preservar feedback de alvo e direção.

## Fonte

`https://iron.wiki/spells/` · `https://iron.wiki/schools/`.

## Parâmetros de implementação para perks — mapa estático do source

- **Source pin 3.16.3:** [`TelekinesisSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/eldritch/TelekinesisSpell.java); classe `io.redspace.ironsspellbooks.spells.eldritch.TelekinesisSpell`.
- **Identidade de registro observada na classe:** `irons_spellbooks:telekinesis`; escola catalogada `eldritch`.
- **DefaultConfig local:** raridade mínima `LEGENDARY`, maxLevel `5`, cooldown segundos `35`, cast `CONTINUOUS`. Ausências neste extrato não são valores zero.
- **Campos Java declarados:** `baseManaCost`=`25`; `manaCostPerLevel`=`0`; `baseSpellPower`=`8`; `spellPowerPerLevel`=`4`; `castTime`=`140`.
- **Métodos diretamente localizáveis:** `getUniqueInfo()`, `getCastTime()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastStartSound()`, `getCastFinishSound()`, `checkPreCastConditions()`, `onCast()`, `onServerCastTick()`, `handleTelekinesis()`, `getTargetingColor()`, `getRange()`, `getCastStartAnimation()`.
- **Expressões de retorno curtas extraídas (somente onde há retorno direto):** `getCastTime = castTime + 20 * (spellLevel - 1)`; `getRange = 12 + (spellLevel - 1) * 2`.
- **Classes instanciadas na implementação (pistas, não classificação automática de efeito):** `TelekinesisData`, `Vector3f`.

**Uso no Codex:** localizar `onCast`, `checkPreCastConditions` e helpers/entidades acima; distinguir modificadores de atributos nativos de alteração de geometria, alvo, duração e efeito. As fórmulas usam `AbstractSpell.getSpellPower` e custo efetivo de config quando aplicáveis. Não presumir que `SpellPreCastEvent` ou `SpellOnCastEvent` interceptem variáveis locais/projéteis: hook específico deve ser comprovado, ou usar **fail-closed**. O RPG Skill Tree responde por perks/Mastery/gates; casting permanece provider-owned. Registro documental estático, não teste de Survival. [Contrato global](../TECHNICAL-PERK-MAP.md).
