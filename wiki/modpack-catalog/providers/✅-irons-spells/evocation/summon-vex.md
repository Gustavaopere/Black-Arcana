# Summon Vex

- **Status no modpack:** PRESENTE — provider instalado
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Evocation
- **Níveis:** 1–5
- **Raridade:** Rare → Legendary
- **Cast:** Long
- **Mana:** 50–90
- **Cooldown:** 150 s
- **Quantidade atual:** 3–7 summons

## O que faz

Conjura Vexes aliados que seguem, protegem e lutam pelo caster.

## Escalonamento

O catálogo atual lista 3–7 summons. A página histórica 1.19 listava 1–5; o valor antigo não é usado para a build atual. Vida, dano, duração e AI exata ficam `NÃO VERIFICADO`.

## Obtenção e aprendizado

Segue o pipeline geral de scrolls/spellbooks do Iron's. O Grimoire of Evokation atualmente pode vir com Summon Vex 4 já inscrito e é descrito como drop raro de Evokers ou Archevokers; outras rotas específicas continuam `NÃO VERIFICADO`.

## Deduplicação / causalidade

Já cobre summons voadores de proteção/combate. Black Arcana não deve recriar Vex-like servants apenas com outro visual. Dano dos summons deve manter ownership/causalidade do provider e não gerar crédito duplicado como novos casts raiz.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`
- Spellbook oficial atual: `https://iron.wiki/spellbooks/`
- Página 1.19 usada somente para detectar divergência histórica: `https://iron.wiki/1_19/spells/`
- Consulta: 2026-09-06.

## Parâmetros de implementação para perks — source auditado

- **Classe de referência:** [`SummonVexSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/evocation/SummonVexSpell.java) (`e4056af90302d37eb1739f5ff05020b020e6e252`, 3.16.3).
- **ID fonte:** `irons_spellbooks:summon_vex` (não inferir quando não extraído).
- **Config:** raridade `RARE`, maxLevel `5`, cooldown s `150`, cast `LONG`.
- **Campos Java:** `baseManaCost`=`50`; `manaCostPerLevel`=`10`; `baseSpellPower`=`1`; `spellPowerPerLevel`=`0`; `castTime`=`20`.
- **Métodos:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastStartSound()`, `getCastFinishSound()`, `getRecastCount()`, `onRecastFinished()`, `getEmptyCastData()`, `getSummonCount()`, `onCast()`.
- **Fórmulas de retorno simples:** `getRecastCount = 2`; `getSummonCount = spellLevel + 2`.
- **Pistas técnicas:** `SpellSummonEvent`, `SummonManager`, `addFreshEntity`.

**Para Codex:** seguir implementação e entidades auxiliares antes de gerar perks sobre alvo, status, duração, raio ou projéteis. Custo e spell power são provider-native com configs/atributos, não literais injetáveis em eventos. Sem hook comprovado manter ⚠️ condicionado/fail-closed e limites de custo/cap/deduplicação. Iron's: cast/custos. RPG Skill Tree: perks/Mastery/gates. Black Arcana: runtime próprio. Fonte estática, QA físico pendente. [Contrato geral](../TECHNICAL-PERK-MAP.md).
