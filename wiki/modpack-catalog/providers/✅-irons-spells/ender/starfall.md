# Starfall

- **Status no modpack:** PRESENTE — provider instalado
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Ender
- **Níveis:** 1–10
- **Raridade:** Uncommon → Legendary
- **Cast:** Continuous
- **Mana:** 5–14
- **Cooldown:** 16 s
- **Dano:** 4–8,5
- **Raio:** 6 blocos

## O que faz

Mantém uma chuva contínua de projéteis/cometas arcanos sobre uma área escolhida, causando dano dentro de um raio listado de 6 blocos.

## Escalonamento

O dano listado cresce de 4 para 8,5 e o custo de mana de 5 para 14. Cadência dos impactos, duração efetiva do channel e regras de reacerto ficam `NÃO VERIFICADO` neste passe.

## Obtenção e aprendizado

Segue o pipeline geral de scrolls/spellbooks do Iron's. Fontes específicas de loot/crafting permanecem `NÃO VERIFICADO`.

## Deduplicação

Já cobre bombardeio arcano contínuo de uma área marcada. Chuva de projéteis celestiais/caóticos de outro provider só é gap se alterar regra, recurso, targeting ou consequência de forma material.

## VFX / animação / áudio

`NÃO VERIFICADO` no runtime real do pack neste passe.

## Fonte / evidência

Catálogo oficial atual: `https://iron.wiki/spells/` — consulta em 2026-09-06.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`StarfallSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/ender/StarfallSpell.java), fixado em `e4056af90302d37eb1739f5ff05020b020e6e252` (versão 1.21.1-3.16.3).
- **ID declarado:** `irons_spellbooks:starfall` (se NÃO EXTRAÍDO, consultar registry).
- **Config na classe:** minRarity `UNCOMMON`, maxLevel `10`, cooldown segundos `16`, cast `CONTINUOUS`.
- **Campos Java:** `baseManaCost`=`5`; `manaCostPerLevel`=`1`; `baseSpellPower`=`8`; `spellPowerPerLevel`=`1`; `castTime`=`160`.
- **Métodos-chave:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastStartSound()`, `getCastFinishSound()`, `onCast()`, `onServerCastTick()`, `getDamage()`, `getRadius()`, `getCastStartAnimation()`.
- **Fórmulas numéricas de retorno direto:** `getDamage = getSpellPower(spellLevel, caster) * .5f`; `getRadius = 6`. Não são fórmulas completas de efeitos condicionais.
- **Pistas de efeito e targeting no source:** `RaycastBuilder`, `DamageSources`, `addFreshEntity`.

**Para o Codex:** seguir `onCast` e métodos auxiliares até as classes que realmente aplicam dano/efeito. Campos extraídos documentam defaults, não a configuração efetiva no servidor. `getSpellPower` consulta atributos e escola nativos; eventos genéricos não demonstram modificabilidade de raio, quantidade ou alvo. Requer adapter/contrato real, cap, causalidade e fail-closed. Iron's mantém cast/custo/cooldown; RPG Skill Tree, perks/Mastery/gates; Black Arcana, o runtime mágico próprio. ⚠️ Auditoria estática sem testes físicos. [Especificação](../TECHNICAL-PERK-MAP.md).
