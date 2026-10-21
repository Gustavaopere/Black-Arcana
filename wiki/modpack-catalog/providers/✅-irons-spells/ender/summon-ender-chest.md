# Summon Ender Chest

- **Status no modpack:** PRESENTE — provider instalado
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Ender
- **Níveis:** 1
- **Raridade:** Rare
- **Cast:** Instant
- **Mana:** 25
- **Cooldown:** 5 s

## O que faz

Disponibiliza ao caster o seu inventário pessoal de Ender Chest no momento do cast. O catálogo oficial atual descreve diretamente essa função; não se infere um segundo inventário ou armazenamento próprio do spell.

## Escalonamento

Spell de nível único. Forma exata da UI/manifestação, alcance de interação e lifecycle interno ficam `NÃO VERIFICADO` neste passe.

## Obtenção e aprendizado

Segue o pipeline geral de scrolls/spellbooks do Iron's. Fontes específicas de loot/crafting permanecem `NÃO VERIFICADO`.

## Deduplicação

Já cobre acesso mágico portátil ao Ender Chest. Uma futura utilidade Black Arcana de armazenamento remoto precisa usar outro contrato/authority ou oferecer comportamento materialmente distinto.

## Authority / segurança

O inventário Ender do jogador continua sendo a authority. Black Arcana não deve copiar, espelhar ou manter um segundo storage para reproduzir esta função.

## VFX / animação / áudio

`NÃO VERIFICADO` no runtime real do pack neste passe.

## Fonte / evidência

Catálogo oficial atual: `https://iron.wiki/spells/` — consulta em 2026-09-06.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`SummonEnderChestSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/ender/SummonEnderChestSpell.java), fixado em `e4056af90302d37eb1739f5ff05020b020e6e252` (versão 1.21.1-3.16.3).
- **ID declarado:** `irons_spellbooks:summon_ender_chest` (se NÃO EXTRAÍDO, consultar registry).
- **Config na classe:** minRarity `RARE`, maxLevel `1`, cooldown segundos `5`, cast `INSTANT`.
- **Campos Java:** `baseManaCost`=`25`; `manaCostPerLevel`=`1`; `baseSpellPower`=`1`; `spellPowerPerLevel`=`1`; `castTime`=`0`.
- **Métodos-chave:** `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `onCast()`, `getCastStartAnimation()`.
- **Fórmulas numéricas de retorno direto:** não extraídas; rastrear corpo de métodos e entidades auxiliares. Não são fórmulas completas de efeitos condicionais.
- **Pistas de efeito e targeting no source:** nenhuma das pistas-padrão extraída.

**Para o Codex:** seguir `onCast` e métodos auxiliares até as classes que realmente aplicam dano/efeito. Campos extraídos documentam defaults, não a configuração efetiva no servidor. `getSpellPower` consulta atributos e escola nativos; eventos genéricos não demonstram modificabilidade de raio, quantidade ou alvo. Requer adapter/contrato real, cap, causalidade e fail-closed. Iron's mantém cast/custo/cooldown; RPG Skill Tree, perks/Mastery/gates; Black Arcana, o runtime mágico próprio. ⚠️ Auditoria estática sem testes físicos. [Especificação](../TECHNICAL-PERK-MAP.md).
