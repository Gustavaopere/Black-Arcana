# Fang Swirl

- **Status no modpack:** PRESENTE — provider instalado
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Evocation
- **Níveis:** 1–8
- **Raridade:** Epic → Legendary
- **Cast:** Long
- **Mana:** 55–111
- **Cooldown:** 28 s
- **Dano:** 4,5–9,75
- **Raio:** 5–8,5 blocos

## O que faz

Ao selecionar uma criatura ou bloco, conjura uma zona espiral de Evoker Fangs que ocupa uma área circular em torno do alvo.

## Escalonamento

O catálogo atual confirma crescimento de dano e raio. Duração, densidade de fangs, cadência e possibilidade de múltiplos hits ficam `NÃO VERIFICADO`.

## Obtenção e aprendizado

Segue o pipeline geral de scrolls/spellbooks do Iron's. Rotas específicas permanecem `NÃO VERIFICADO`.

## Deduplicação

Já cobre área espiral de fangs centrada em alvo. Diferença meramente geométrica/visual não é gap suficiente para uma nova magia Black Arcana.

## VFX / animação / áudio

`NÃO VERIFICADO` no runtime real do pack neste passe.

## Fonte / evidência

Catálogo oficial atual: `https://iron.wiki/spells/` — consulta em 2026-09-06.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`FangSwirlSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/evocation/FangSwirlSpell.java), fonte fixada no commit `e4056af90302d37eb1739f5ff05020b020e6e252` de Iron's 1.21.1-3.16.3.
- **ID local:** `irons_spellbooks:fang_swirl` (não inferir caso não extraído); escola `evocation`.
- **DefaultConfig:** minRarity `EPIC`, maxLevel `8`, cooldown `28` s, cast `LONG`.
- **Campos Java:** `baseManaCost`=`55`; `manaCostPerLevel`=`8`; `baseSpellPower`=`6`; `spellPowerPerLevel`=`1`; `castTime`=`20`.
- **Métodos operacionais:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastStartSound()`, `checkPreCastConditions()`, `onCast()`, `getRange()`, `getSwirlRadius()`, `getSwirlDurationTicks()`, `getDamage()`.
- **Fórmulas de retorno numérico direto:** `getRange = 32`; `getSwirlRadius = 4.5f + 0.5f * spellLevel * getEntityPowerMultiplier(caster)`; `getSwirlDurationTicks = 8 * 20`; `getDamage = getSpellPower(spellLevel, caster) * .75f`. Não cobrem cálculos locais complexos.
- **Pistas de alvo, dano e entidade:** `RaycastBuilder`, `TargetEntityCastData`, `addFreshEntity`.

**Codex / modificadores:** verificar corpo de `onCast`, validação de alvo e classe auxiliar antes de classificar tipo de dano, área, alcance ou efeito. Modificação por atributo nativo de Iron's é diferente de alteração de variável local. Hook de range/count/area não foi provado; sem hook, ⚠️ condicionado/fail-closed. Proteger custos, cooldown, casts duplicados, orçamento de entidades, Mastery e caps. RPG Skill Tree controla perks/Mastery/gates, Iron's controla seus spells e Black Arcana controla seu runtime. QA real não realizado. [Contrato transversal](../TECHNICAL-PERK-MAP.md).
