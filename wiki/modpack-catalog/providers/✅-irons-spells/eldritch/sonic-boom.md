# Sonic Boom

- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR:** `irons_spellbooks-1.21.1-3.16.3.jar`
- **Escola:** Eldritch
- **Níveis:** 1–3
- **Raridade:** Legendary
- **Tipo de cast:** Long
- **Recurso:** mana do Iron's
- **Custo:** 110–210 mana
- **Cooldown:** 25 s
- **Dano:** 20–36
- **Alcance:** 20–30 blocos

## O que faz

Projeta uma onda sônica Eldritch de alto dano que atravessa material sólido e atinge criaturas ao longo da trajetória.

## Escalonamento

Dano, alcance e custo aumentam com o nível. Largura da trajetória e regras de penetração ainda serão verificadas.

## Obtenção e aprendizado

Ancient Knowledge Fragments → Eldritch Manuscript → aprendizado; Echo Shard é o Focus posterior.

## Deduplicação

Ocupa ataque penetrante de alto dano através de blocos. Qualquer nova magia de Ordem/Caos com linha perfurante deve demonstrar mecânica diferente.

## VFX / animação / áudio

A catalogar visualmente.

## Fonte

`https://iron.wiki/spells/` · `https://iron.wiki/schools/`.

## Parâmetros de implementação para perks — mapa estático do source

- **Source pin 3.16.3:** [`SonicBoomSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/eldritch/SonicBoomSpell.java); classe `io.redspace.ironsspellbooks.spells.eldritch.SonicBoomSpell`.
- **Identidade de registro observada na classe:** `irons_spellbooks:sonic_boom`; escola catalogada `eldritch`.
- **DefaultConfig local:** raridade mínima `LEGENDARY`, maxLevel `3`, cooldown segundos `25`, cast `LONG`. Ausências neste extrato não são valores zero.
- **Campos Java declarados:** `baseManaCost`=`110`; `manaCostPerLevel`=`50`; `baseSpellPower`=`20`; `spellPowerPerLevel`=`8`; `castTime`=`30`.
- **Métodos diretamente localizáveis:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastStartSound()`, `getCastFinishSound()`, `onCast()`, `getRange()`, `getDamage()`, `getCastStartAnimation()`.
- **Expressões de retorno curtas extraídas (somente onde há retorno direto):** `getRange = 15 + 5 * level`; `getDamage = getSpellPower(spellLevel, caster)`.
- **Classes instanciadas na implementação (pistas, não classificação automática de efeito):** `CameraShakeData`.

**Uso no Codex:** localizar `onCast`, `checkPreCastConditions` e helpers/entidades acima; distinguir modificadores de atributos nativos de alteração de geometria, alvo, duração e efeito. As fórmulas usam `AbstractSpell.getSpellPower` e custo efetivo de config quando aplicáveis. Não presumir que `SpellPreCastEvent` ou `SpellOnCastEvent` interceptem variáveis locais/projéteis: hook específico deve ser comprovado, ou usar **fail-closed**. O RPG Skill Tree responde por perks/Mastery/gates; casting permanece provider-owned. Registro documental estático, não teste de Survival. [Contrato global](../TECHNICAL-PERK-MAP.md).
