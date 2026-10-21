# Pocket Dimension

- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR:** `irons_spellbooks-1.21.1-3.16.3.jar`
- **Escola:** Eldritch
- **Níveis:** 1
- **Raridade:** Legendary
- **Tipo de cast:** Long
- **Recurso:** mana do Iron's
- **Custo:** 300 mana
- **Cooldown:** 60 s

## O que faz

Transporta o caster para uma dimensão pessoal de acesso exclusivo, oferecendo uma pequena área privada temporariamente acessível pelo spell.

## Escalonamento

Sem escala de nível publicada. Duração, regras de saída, persistência e restrições de dimensão ainda serão verificadas no runtime/config da versão instalada.

## Obtenção e aprendizado

Ancient Knowledge Fragments → Eldritch Manuscript → aprendizado; Echo Shard é o Focus posterior.

## Deduplicação

Ocupa o nicho de pocket-space pessoal. É especialmente relevante para Black Arcana Domains: Forbidden Domains não devem virar uma cópia deste spell nem criar dimensões temporárias paralelas.

## VFX / animação / áudio

A catalogar visualmente.

## Fonte

`https://iron.wiki/spells/` · `https://iron.wiki/schools/`.

## Parâmetros de implementação para perks — mapa estático do source

- **Source pin 3.16.3:** [`PocketDimensionSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/eldritch/PocketDimensionSpell.java); classe `io.redspace.ironsspellbooks.spells.eldritch.PocketDimensionSpell`.
- **Identidade de registro observada na classe:** `irons_spellbooks:pocket_dimension`; escola catalogada `eldritch`.
- **DefaultConfig local:** raridade mínima `LEGENDARY`, maxLevel `1`, cooldown segundos `60`, cast `LONG`. Ausências neste extrato não são valores zero.
- **Campos Java declarados:** `baseManaCost`=`300`; `manaCostPerLevel`=`0`; `baseSpellPower`=`0`; `spellPowerPerLevel`=`0`; `castTime`=`40`.
- **Métodos diretamente localizáveis:** `getEffectiveCastTime()`, `checkPreCastConditions()`, `getCastFinishSound()`, `getCastStartSound()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getEmptyCastData()`, `onCast()`, `getCastStartAnimation()`.
- **Expressões de retorno curtas extraídas (somente onde há retorno direto):** NÃO EXTRAÍDAS — efeitos podem usar outras classes ou cálculos imperativos.
- **Classes instanciadas na implementação (pistas, não classificação automática de efeito):** `ClientboundSetActionBarTextPacket`, `SerializedTargetData`, `PortalData`, `DimensionTransition`.

**Uso no Codex:** localizar `onCast`, `checkPreCastConditions` e helpers/entidades acima; distinguir modificadores de atributos nativos de alteração de geometria, alvo, duração e efeito. As fórmulas usam `AbstractSpell.getSpellPower` e custo efetivo de config quando aplicáveis. Não presumir que `SpellPreCastEvent` ou `SpellOnCastEvent` interceptem variáveis locais/projéteis: hook específico deve ser comprovado, ou usar **fail-closed**. O RPG Skill Tree responde por perks/Mastery/gates; casting permanece provider-owned. Registro documental estático, não teste de Survival. [Contrato global](../TECHNICAL-PERK-MAP.md).
