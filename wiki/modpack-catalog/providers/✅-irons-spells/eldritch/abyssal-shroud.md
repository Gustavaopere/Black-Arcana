# Abyssal Shroud

- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR:** `irons_spellbooks-1.21.1-3.16.3.jar`
- **Escola:** Eldritch
- **Níveis:** 1–3
- **Raridade:** Legendary
- **Tipo de cast:** Instant
- **Recurso:** mana do Iron's
- **Custo:** 300–340 mana
- **Cooldown:** 200 s
- **Duração:** 6–18 s

## O que faz

Envolve o caster em energia abissal e concede uma janela curta de evasão absoluta contra ataques.

## Escalonamento

Duração e custo escalam com o nível. Regras exatas do que conta como ataque/evadível ainda serão verificadas no runtime.

## Obtenção e aprendizado

Eldritch não segue o crafting comum inicial: Ancient Knowledge Fragments são encontrados no mundo, reconstruídos em um Eldritch Manuscript com Echo Shard, e o manuscrito ensina um Eldritch spell. Após aprendido, Echo Shard atua como Focus da escola.

## Deduplicação

Bloqueia duplicatas de invulnerabilidade/evasion Eldritch sem custo/semântica distinta. Comparar com Heartstop e Evasion.

## VFX / animação / áudio

A catalogar visualmente.

## Fonte

`https://iron.wiki/spells/` · `https://iron.wiki/schools/`.

## Parâmetros de implementação para perks — mapa estático do source

- **Source pin 3.16.3:** [`AbyssalShroudSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/eldritch/AbyssalShroudSpell.java); classe `io.redspace.ironsspellbooks.spells.eldritch.AbyssalShroudSpell`.
- **Identidade de registro observada na classe:** `irons_spellbooks:abyssal_shroud`; escola catalogada `eldritch`.
- **DefaultConfig local:** raridade mínima `LEGENDARY`, maxLevel `3`, cooldown segundos `200`, cast `INSTANT`. Ausências neste extrato não são valores zero.
- **Campos Java declarados:** `baseManaCost`=`300`; `manaCostPerLevel`=`20`; `baseSpellPower`=`6`; `spellPowerPerLevel`=`6`; `castTime`=`0`.
- **Métodos diretamente localizáveis:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastStartSound()`, `getCastFinishSound()`, `onCast()`, `getCastStartAnimation()`.
- **Expressões de retorno curtas extraídas (somente onde há retorno direto):** NÃO EXTRAÍDAS — efeitos podem usar outras classes ou cálculos imperativos.
- **Classes instanciadas na implementação (pistas, não classificação automática de efeito):** sem instâncias relevantes extraídas.

**Uso no Codex:** localizar `onCast`, `checkPreCastConditions` e helpers/entidades acima; distinguir modificadores de atributos nativos de alteração de geometria, alvo, duração e efeito. As fórmulas usam `AbstractSpell.getSpellPower` e custo efetivo de config quando aplicáveis. Não presumir que `SpellPreCastEvent` ou `SpellOnCastEvent` interceptem variáveis locais/projéteis: hook específico deve ser comprovado, ou usar **fail-closed**. O RPG Skill Tree responde por perks/Mastery/gates; casting permanece provider-owned. Registro documental estático, não teste de Survival. [Contrato global](../TECHNICAL-PERK-MAP.md).
