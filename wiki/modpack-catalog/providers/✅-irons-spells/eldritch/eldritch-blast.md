# Eldritch Blast

- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR:** `irons_spellbooks-1.21.1-3.16.3.jar`
- **Escola:** Eldritch
- **Níveis:** 1–5
- **Raridade:** Legendary
- **Tipo de cast:** Instant
- **Recurso:** mana do Iron's
- **Custo:** 90–150 mana
- **Cooldown:** 15 s
- **Dano:** 15 por blast listado
- **Blasts:** 3–7
- **Alcance:** 30 blocos

## O que faz

Dispara vários raios concentrados de energia Eldritch em direção aos alvos/linha de mira, funcionando como burst multihit de longo alcance.

## Escalonamento

A quantidade de blasts e o custo escalam com o nível. Multiplicadores de spell power e targeting exato serão normalizados no runtime.

## Obtenção e aprendizado

Usa o pipeline especial Eldritch: Ancient Knowledge Fragments → Eldritch Manuscript → aprendizado; Echo Shard atua como Focus após o spell ser aprendido.

## Deduplicação

Ocupa burst Eldritch multiray de longo alcance; novas magias de Caos/Ordem não devem recriar apenas “feixe devastador” com outra cor.

## VFX / animação / áudio

A catalogar visualmente.

## Fonte

`https://iron.wiki/spells/` · `https://iron.wiki/schools/`.

## Parâmetros de implementação para perks — mapa estático do source

- **Source pin 3.16.3:** [`EldritchBlastSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/eldritch/EldritchBlastSpell.java); classe `io.redspace.ironsspellbooks.spells.eldritch.EldritchBlastSpell`.
- **Identidade de registro observada na classe:** `irons_spellbooks:eldritch_blast`; escola catalogada `eldritch`.
- **DefaultConfig local:** raridade mínima `LEGENDARY`, maxLevel `5`, cooldown segundos `15`, cast `INSTANT`. Ausências neste extrato não são valores zero.
- **Campos Java declarados:** `baseManaCost`=`90`; `manaCostPerLevel`=`15`; `baseSpellPower`=`15`; `spellPowerPerLevel`=`0`; `castTime`=`0`.
- **Métodos diretamente localizáveis:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastStartSound()`, `getCastFinishSound()`, `getRecastCount()`, `onCast()`, `getRange()`, `getDamage()`, `getDamageSource()`.
- **Expressões de retorno curtas extraídas (somente onde há retorno direto):** `getRecastCount = 2 + spellLevel`; `getRange = 30`; `getDamage = getSpellPower(spellLevel, caster)`.
- **Classes instanciadas na implementação (pistas, não classificação automática de efeito):** `RecastInstance`, `EldritchBlastVisualEntity`.

**Uso no Codex:** localizar `onCast`, `checkPreCastConditions` e helpers/entidades acima; distinguir modificadores de atributos nativos de alteração de geometria, alvo, duração e efeito. As fórmulas usam `AbstractSpell.getSpellPower` e custo efetivo de config quando aplicáveis. Não presumir que `SpellPreCastEvent` ou `SpellOnCastEvent` interceptem variáveis locais/projéteis: hook específico deve ser comprovado, ou usar **fail-closed**. O RPG Skill Tree responde por perks/Mastery/gates; casting permanece provider-owned. Registro documental estático, não teste de Survival. [Contrato global](../TECHNICAL-PERK-MAP.md).
