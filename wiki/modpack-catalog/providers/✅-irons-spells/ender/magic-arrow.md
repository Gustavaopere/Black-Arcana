# Magic Arrow

- **Status no modpack:** PRESENTE — provider instalado
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Ender
- **Níveis:** 1–10
- **Raridade:** Rare → Legendary
- **Cast:** Long
- **Mana:** 40–85
- **Cooldown:** 8 s
- **Dano:** 10–28

## O que faz

Carrega e dispara uma flecha de energia arcana sem gravidade. O catálogo atual documenta que o projétil pode atravessar blocos.

## Escalonamento

O dano listado cresce de 10 para 28 ao longo dos 10 níveis. Velocidade, largura de hitbox, penetração em entidades e regra exata de atravessamento de blocos permanecem `NÃO VERIFICADO`.

## Obtenção e aprendizado

Segue o pipeline geral de scrolls/spellbooks do Iron's. Fontes específicas de loot/crafting permanecem `NÃO VERIFICADO`.

## Deduplicação

Já cobre projétil arcano carregado, sem gravidade e com penetração de terreno. Não aprovar um projétil Black Arcana equivalente apenas com VFX diferente.

## VFX / animação / áudio

`NÃO VERIFICADO` no runtime real do pack neste passe.

## Fonte / evidência

Catálogo oficial atual: `https://iron.wiki/spells/` — consulta em 2026-09-06.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`MagicArrowSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/ender/MagicArrowSpell.java), fixado em `e4056af90302d37eb1739f5ff05020b020e6e252` (versão 1.21.1-3.16.3).
- **ID declarado:** `irons_spellbooks:magic_arrow` (se NÃO EXTRAÍDO, consultar registry).
- **Config na classe:** minRarity `RARE`, maxLevel `10`, cooldown segundos `8`, cast `LONG`.
- **Campos Java:** `baseManaCost`=`40`; `manaCostPerLevel`=`5`; `baseSpellPower`=`10`; `spellPowerPerLevel`=`2`; `castTime`=`30`.
- **Métodos-chave:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastStartSound()`, `getCastFinishSound()`, `onCast()`, `getCastStartAnimation()`, `getCastFinishAnimation()`.
- **Fórmulas numéricas de retorno direto:** não extraídas; rastrear corpo de métodos e entidades auxiliares. Não são fórmulas completas de efeitos condicionais.
- **Pistas de efeito e targeting no source:** `addFreshEntity`.

**Para o Codex:** seguir `onCast` e métodos auxiliares até as classes que realmente aplicam dano/efeito. Campos extraídos documentam defaults, não a configuração efetiva no servidor. `getSpellPower` consulta atributos e escola nativos; eventos genéricos não demonstram modificabilidade de raio, quantidade ou alvo. Requer adapter/contrato real, cap, causalidade e fail-closed. Iron's mantém cast/custo/cooldown; RPG Skill Tree, perks/Mastery/gates; Black Arcana, o runtime mágico próprio. ⚠️ Auditoria estática sem testes físicos. [Especificação](../TECHNICAL-PERK-MAP.md).
