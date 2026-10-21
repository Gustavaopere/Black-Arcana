# Arrow Volley

- **Status no modpack:** PRESENTE — provider instalado
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Evocation
- **Níveis:** 1–6
- **Raridade:** Uncommon → Legendary
- **Cast:** Long
- **Mana:** 40–90
- **Cooldown:** 15 s
- **Dano atual listado:** 2
- **Projéteis:** 25–80

## O que faz

Ao redor de uma criatura ou bloco alvo, invoca uma onda progressiva de flechas mágicas que cai do céu.

## Escalonamento

O catálogo oficial atual mantém dano listado em 2 e escala a quantidade de projéteis de 25 para 80. A página histórica 1.19 listava dano 2–3,2; esse valor antigo não é usado para a build atual.

## Obtenção e aprendizado

Segue o pipeline geral de scrolls/spellbooks do Iron's. Fontes específicas de loot/crafting permanecem `NÃO VERIFICADO`.

## Deduplicação

Já cobre bombardeio aéreo de flechas mágicas sobre alvo/área. Uma futura chuva de projéteis Black Arcana precisa de regra própria além de trocar o tipo visual dos projéteis.

## VFX / animação / áudio

`NÃO VERIFICADO` no runtime real do pack neste passe.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`
- Página 1.19 usada somente para detectar divergência histórica: `https://iron.wiki/1_19/spells/`
- Consulta: 2026-09-06.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`ArrowVolleySpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/evocation/ArrowVolleySpell.java), fonte fixada no commit `e4056af90302d37eb1739f5ff05020b020e6e252` de Iron's 1.21.1-3.16.3.
- **ID local:** `irons_spellbooks:arrow_volley` (não inferir caso não extraído); escola `evocation`.
- **DefaultConfig:** minRarity `UNCOMMON`, maxLevel `6`, cooldown `15` s, cast `LONG`.
- **Campos Java:** `baseManaCost`=`40`; `manaCostPerLevel`=`10`; `baseSpellPower`=`8`; `spellPowerPerLevel`=`0`; `castTime`=`30`.
- **Métodos operacionais:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastStartSound()`, `getCastFinishSound()`, `checkPreCastConditions()`, `onCast()`, `getCount()`, `getRows()`, `getArrowsPerRow()`, `getDamage()`, `getDamageSource()`, `getCastStartAnimation()`.
- **Fórmulas de retorno numérico direto:** `getCount = getRows(spellLevel, entity) * getArrowsPerRow(spellLevel, entity)`; `getRows = 4 + spellLevel`; `getArrowsPerRow = 5 + spellLevel / 2`; `getDamage = this.getSpellPower(spellLevel, entity) * .25f`. Não cobrem cálculos locais complexos.
- **Pistas de alvo, dano e entidade:** `RaycastBuilder`, `TargetEntityCastData`, `SpellDamageSource`, `addFreshEntity`.

**Codex / modificadores:** verificar corpo de `onCast`, validação de alvo e classe auxiliar antes de classificar tipo de dano, área, alcance ou efeito. Modificação por atributo nativo de Iron's é diferente de alteração de variável local. Hook de range/count/area não foi provado; sem hook, ⚠️ condicionado/fail-closed. Proteger custos, cooldown, casts duplicados, orçamento de entidades, Mastery e caps. RPG Skill Tree controla perks/Mastery/gates, Iron's controla seus spells e Black Arcana controla seu runtime. QA real não realizado. [Contrato transversal](../TECHNICAL-PERK-MAP.md).
