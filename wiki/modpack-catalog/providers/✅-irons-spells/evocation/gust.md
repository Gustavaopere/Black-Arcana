# Gust

- **Status no modpack:** PRESENTE — provider instalado
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Evocation
- **Níveis:** 1–10
- **Raridade:** Uncommon → Legendary
- **Cast:** Long
- **Mana:** 30–75
- **Cooldown:** 12 s
- **Força listada:** 100%–190%
- **Dano por impacto:** 4,5–9

## O que faz

Conjura uma rajada forte de vento em cone que arremessa criaturas para trás. O dano listado ocorre quando a criatura arremessada colide com uma parede.

## Escalonamento

O catálogo atual confirma crescimento da força de 100% para 190% e do dano de impacto de 4,5 para 9. Alcance, ângulo do cone e fórmula física exata ficam `NÃO VERIFICADO`.

## Obtenção e aprendizado

Segue o pipeline geral de scrolls/spellbooks do Iron's. Rotas específicas permanecem `NÃO VERIFICADO`.

## Deduplicação / causalidade

Já cobre forced movement com dano causal por colisão. Black Arcana não deve transformar o empurrão e o impacto em dois casts/ofensive credits independentes; qualquer integração precisa preservar a relação causal original.

## VFX / animação / áudio

`NÃO VERIFICADO` no runtime real do pack neste passe.

## Fonte / evidência

Catálogo oficial atual: `https://iron.wiki/spells/` — consulta em 2026-09-06.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`GustSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/evocation/GustSpell.java), fonte fixada no commit `e4056af90302d37eb1739f5ff05020b020e6e252` de Iron's 1.21.1-3.16.3.
- **ID local:** `irons_spellbooks:gust` (não inferir caso não extraído); escola `evocation`.
- **DefaultConfig:** minRarity `UNCOMMON`, maxLevel `10`, cooldown `12` s, cast `LONG`.
- **Campos Java:** `baseManaCost`=`30`; `manaCostPerLevel`=`5`; `baseSpellPower`=`10`; `spellPowerPerLevel`=`1`; `castTime`=`15`.
- **Métodos operacionais:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastStartSound()`, `getCastFinishSound()`, `onCast()`, `getRange()`, `getStrength()`, `getDamage()`, `getCastStartAnimation()`, `getCastFinishAnimation()`.
- **Fórmulas de retorno numérico direto:** `getRange = 8`; `getStrength = getSpellPower(spellLevel, caster) * .2f`; `getDamage = getSpellPower(spellLevel, caster)`. Não cobrem cálculos locais complexos.
- **Pistas de alvo, dano e entidade:** `addFreshEntity`.

**Codex / modificadores:** verificar corpo de `onCast`, validação de alvo e classe auxiliar antes de classificar tipo de dano, área, alcance ou efeito. Modificação por atributo nativo de Iron's é diferente de alteração de variável local. Hook de range/count/area não foi provado; sem hook, ⚠️ condicionado/fail-closed. Proteger custos, cooldown, casts duplicados, orçamento de entidades, Mastery e caps. RPG Skill Tree controla perks/Mastery/gates, Iron's controla seus spells e Black Arcana controla seu runtime. QA real não realizado. [Contrato transversal](../TECHNICAL-PERK-MAP.md).
