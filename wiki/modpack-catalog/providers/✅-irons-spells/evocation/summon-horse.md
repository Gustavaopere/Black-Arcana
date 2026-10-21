# Summon Horse

- **Status no modpack:** PRESENTE — provider instalado
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Evocation
- **Níveis:** 1–5
- **Raridade:** Common → Legendary
- **Cast:** Long
- **Mana:** 50–58
- **Cooldown:** 20 s

## O que faz

Conjura um cavalo espectral que acompanha o caster e aceita somente ele como cavaleiro. A documentação atual afirma que velocidade, vida e altura de salto escalam com spell power.

## Escalonamento

A fórmula exata de speed/health/jump versus spell power, duração e regras de respawn/despawn ficam `NÃO VERIFICADO`.

## Obtenção e aprendizado

Segue o pipeline geral de scrolls/spellbooks do Iron's. Rotas específicas permanecem `NÃO VERIFICADO`.

## Deduplicação / authority

Já cobre montaria espectral invocada com stats escalados por spell power. Uma montaria Black Arcana só é gap se possuir sistema ou custo materialmente diferente. Iron's permanece authority da entidade, ownership e stats.

## Fonte / evidência

Catálogo oficial atual: `https://iron.wiki/spells/` — consulta em 2026-09-06.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`SummonHorseSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/evocation/SummonHorseSpell.java), fonte fixada no commit `e4056af90302d37eb1739f5ff05020b020e6e252` de Iron's 1.21.1-3.16.3.
- **ID local:** `irons_spellbooks:summon_horse` (não inferir caso não extraído); escola `evocation`.
- **DefaultConfig:** minRarity `COMMON`, maxLevel `5`, cooldown `20` s, cast `LONG`.
- **Campos Java:** `baseManaCost`=`50`; `manaCostPerLevel`=`2`; `baseSpellPower`=`100 - 15`; `spellPowerPerLevel`=`15`; `castTime`=`20`.
- **Métodos operacionais:** `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastStartSound()`, `getCastFinishSound()`, `getEmptyCastData()`, `getRecastCount()`, `onRecastFinished()`, `onCast()`.
- **Fórmulas de retorno numérico direto:** `getRecastCount = 2`. Não cobrem cálculos locais complexos.
- **Pistas de alvo, dano e entidade:** `addFreshEntity`, `SpellSummonEvent`.

**Codex / modificadores:** verificar corpo de `onCast`, validação de alvo e classe auxiliar antes de classificar tipo de dano, área, alcance ou efeito. Modificação por atributo nativo de Iron's é diferente de alteração de variável local. Hook de range/count/area não foi provado; sem hook, ⚠️ condicionado/fail-closed. Proteger custos, cooldown, casts duplicados, orçamento de entidades, Mastery e caps. RPG Skill Tree controla perks/Mastery/gates, Iron's controla seus spells e Black Arcana controla seu runtime. QA real não realizado. [Contrato transversal](../TECHNICAL-PERK-MAP.md).
