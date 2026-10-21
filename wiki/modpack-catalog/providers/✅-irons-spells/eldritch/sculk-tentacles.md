# Sculk Tentacles

- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR:** `irons_spellbooks-1.21.1-3.16.3.jar`
- **Escola:** Eldritch
- **Níveis:** 1–4
- **Raridade:** Legendary
- **Tipo de cast:** Long
- **Recurso:** mana do Iron's
- **Custo:** 150–300 mana
- **Cooldown:** 30 s
- **Dano:** 8
- **Raio:** 2.5–6.5 blocos

## O que faz

Faz irromper tentáculos/energia de sculk na área visada, causando dano e cegueira às criaturas apanhadas no efeito.

## Escalonamento

O raio e o custo aumentam com o nível. Duração da cegueira, frequência de dano e scaling por spell power ainda serão normalizados.

## Obtenção e aprendizado

Ancient Knowledge Fragments → Eldritch Manuscript → aprendizado; Echo Shard é o Focus posterior.

## Deduplicação

Ocupa AOE Eldritch/sculk com dano + blind. Deeper and Darker/Discerning e demais addons Eldritch precisam ser comparados antes de criar efeitos similares.

## VFX / animação / áudio

A catalogar visualmente.

## Fonte

`https://iron.wiki/spells/` · `https://iron.wiki/schools/`.

## Parâmetros de implementação para perks — mapa estático do source

- **Source pin 3.16.3:** [`SculkTentaclesSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/eldritch/SculkTentaclesSpell.java); classe `io.redspace.ironsspellbooks.spells.eldritch.SculkTentaclesSpell`.
- **Identidade de registro observada na classe:** `irons_spellbooks:sculk_tentacles`; escola catalogada `eldritch`.
- **DefaultConfig local:** raridade mínima `LEGENDARY`, maxLevel `4`, cooldown segundos `30`, cast `LONG`. Ausências neste extrato não são valores zero.
- **Campos Java declarados:** `baseManaCost`=`150`; `manaCostPerLevel`=`50`; `baseSpellPower`=`8`; `spellPowerPerLevel`=`3`; `castTime`=`20`.
- **Métodos diretamente localizáveis:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastStartSound()`, `getCastFinishSound()`, `checkPreCastConditions()`, `onCast()`, `getDamage()`, `getRings()`.
- **Expressões de retorno curtas extraídas (somente onde há retorno direto):** `getDamage = baseSpellPower * getEntityPowerMultiplier(entity)`; `getRings = 1 + spellLevel`.
- **Classes instanciadas na implementação (pistas, não classificação automática de efeito):** `VoidTentacle`.

**Uso no Codex:** localizar `onCast`, `checkPreCastConditions` e helpers/entidades acima; distinguir modificadores de atributos nativos de alteração de geometria, alvo, duração e efeito. As fórmulas usam `AbstractSpell.getSpellPower` e custo efetivo de config quando aplicáveis. Não presumir que `SpellPreCastEvent` ou `SpellOnCastEvent` interceptem variáveis locais/projéteis: hook específico deve ser comprovado, ou usar **fail-closed**. O RPG Skill Tree responde por perks/Mastery/gates; casting permanece provider-owned. Registro documental estático, não teste de Survival. [Contrato global](../TECHNICAL-PERK-MAP.md).
