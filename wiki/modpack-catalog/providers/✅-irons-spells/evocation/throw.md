# Throw

- **Status no modpack:** PRESENTE — provider instalado
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Evocation
- **Níveis:** 1–5
- **Raridade:** Common → Legendary
- **Cast:** Long
- **Mana:** 10–30
- **Cooldown:** 8 s
- **Dano base listado:** 1–5

## O que faz

Arremessa o item empunhado, causando dano base do spell somado ao dano que o item normalmente causaria segundo a descrição pública atual.

## Escalonamento

O dano base listado cresce de 1 para 5. Fórmula exata de combinação com weapon damage, enchantments, retorno/perda do item e entidades elegíveis ficam `NÃO VERIFICADO`.

## Obtenção e aprendizado

Segue o pipeline geral de scrolls/spellbooks do Iron's. Rotas específicas permanecem `NÃO VERIFICADO`.

## Deduplicação / authority

Já cobre conversão de item empunhado em ataque arremessado com contribuição do dano nativo do item. Uma habilidade Black Arcana equivalente precisa de mecânica distinta e não pode recalcular o dano do item por fora do provider, evitando double-dip de atributos/enchantments.

## Fonte / evidência

Catálogo oficial atual: `https://iron.wiki/spells/` — consulta em 2026-09-06.

## Parâmetros de implementação para perks — source auditado

- **Classe de referência:** [`ThrowSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/evocation/ThrowSpell.java) (`e4056af90302d37eb1739f5ff05020b020e6e252`, 3.16.3).
- **ID fonte:** `irons_spellbooks:throw` (não inferir quando não extraído).
- **Config:** raridade `COMMON`, maxLevel `5`, cooldown s `8`, cast `LONG`.
- **Campos Java:** `baseManaCost`=`10`; `manaCostPerLevel`=`5`; `baseSpellPower`=`1`; `spellPowerPerLevel`=`1`; `castTime`=`5`.
- **Métodos:** `getUniqueInfo()`, `getEffectiveCastTime()`, `getCastStartAnimation()`, `getCastFinishAnimation()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastFinishSound()`, `onCast()`, `getDamage()`, `getDamageText()`.
- **Fórmulas de retorno simples:** `getDamage = getSpellPower(spellLevel, entity) + Utils.getWeaponDamage(entity)`.
- **Pistas técnicas:** `addFreshEntity`.

**Para Codex:** seguir implementação e entidades auxiliares antes de gerar perks sobre alvo, status, duração, raio ou projéteis. Custo e spell power são provider-native com configs/atributos, não literais injetáveis em eventos. Sem hook comprovado manter ⚠️ condicionado/fail-closed e limites de custo/cap/deduplicação. Iron's: cast/custos. RPG Skill Tree: perks/Mastery/gates. Black Arcana: runtime próprio. Fonte estática, QA físico pendente. [Contrato geral](../TECHNICAL-PERK-MAP.md).
