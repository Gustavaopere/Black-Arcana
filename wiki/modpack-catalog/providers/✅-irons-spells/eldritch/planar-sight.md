# Planar Sight

- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR:** `irons_spellbooks-1.21.1-3.16.3.jar`
- **Escola:** Eldritch
- **Níveis:** 1–3
- **Raridade:** Legendary
- **Tipo de cast:** Instant
- **Recurso:** mana do Iron's
- **Custo:** 150–250 mana
- **Cooldown:** 200 s
- **Duração:** 40 s–~80 s

## O que faz

Desloca a percepção do caster entre planos e permite enxergar criaturas através de material sólido durante a duração do efeito.

## Escalonamento

Duração e custo escalam com o nível. Alcance/limites de visão exatos ainda serão verificados.

## Obtenção e aprendizado

Ancient Knowledge Fragments → Eldritch Manuscript → aprendizado. Echo Shard é o Focus usado depois que a magia é desbloqueada.

## Deduplicação

Ocupa percepção através de blocos/planar sight. Deve ser comparado com Spirit Sight, Asterism e futura Divination antes de aprovar qualquer equivalente.

## VFX / animação / áudio

A catalogar visualmente.

## Fonte

`https://iron.wiki/spells/` · `https://iron.wiki/schools/`.

## Parâmetros de implementação para perks — mapa estático do source

- **Source pin 3.16.3:** [`PlanarSightSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/eldritch/PlanarSightSpell.java); classe `io.redspace.ironsspellbooks.spells.eldritch.PlanarSightSpell`.
- **Identidade de registro observada na classe:** `irons_spellbooks:planar_sight`; escola catalogada `eldritch`.
- **DefaultConfig local:** raridade mínima `LEGENDARY`, maxLevel `3`, cooldown segundos `200`, cast `INSTANT`. Ausências neste extrato não são valores zero.
- **Campos Java declarados:** `baseManaCost`=`150`; `manaCostPerLevel`=`50`; `baseSpellPower`=`40`; `spellPowerPerLevel`=`20`; `castTime`=`0`.
- **Métodos diretamente localizáveis:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastStartSound()`, `getCastFinishSound()`, `onCast()`, `getCastStartAnimation()`.
- **Expressões de retorno curtas extraídas (somente onde há retorno direto):** NÃO EXTRAÍDAS — efeitos podem usar outras classes ou cálculos imperativos.
- **Classes instanciadas na implementação (pistas, não classificação automática de efeito):** sem instâncias relevantes extraídas.

**Uso no Codex:** localizar `onCast`, `checkPreCastConditions` e helpers/entidades acima; distinguir modificadores de atributos nativos de alteração de geometria, alvo, duração e efeito. As fórmulas usam `AbstractSpell.getSpellPower` e custo efetivo de config quando aplicáveis. Não presumir que `SpellPreCastEvent` ou `SpellOnCastEvent` interceptem variáveis locais/projéteis: hook específico deve ser comprovado, ou usar **fail-closed**. O RPG Skill Tree responde por perks/Mastery/gates; casting permanece provider-owned. Registro documental estático, não teste de Survival. [Contrato global](../TECHNICAL-PERK-MAP.md).
