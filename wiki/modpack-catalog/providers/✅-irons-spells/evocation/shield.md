# Shield

- **Status no modpack:** PRESENTE — provider instalado
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Evocation
- **Níveis:** 1–10
- **Raridade:** Common → Legendary
- **Cast:** Instant
- **Mana:** 35–80
- **Cooldown:** 8 s
- **Vida do shield:** 15–105 HP

## O que faz

Conjura um escudo estacionário de energia arcana no ponto mirado. O provider documenta que ele bloqueia projéteis e impede criaturas de atravessá-lo.

## Escalonamento

A vida listada cresce de 15 para 105 HP. Dimensões, duração máxima, regras de colisão e interações especiais permanecem `NÃO VERIFICADO`.

## Obtenção e aprendizado

Segue o pipeline geral de scrolls/spellbooks do Iron's. Rotas específicas permanecem `NÃO VERIFICADO`.

## Deduplicação / authority

Já cobre barreira estacionária com HP, bloqueio de projéteis e colisão de criaturas. Uma ward Black Arcana equivalente precisa de delta real. Iron's continua authority da vida e destruição do shield; bridges não devem manter uma segunda barreira depois que ele é removido.

## Fonte / evidência

Catálogo oficial atual: `https://iron.wiki/spells/` — consulta em 2026-09-06.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`ShieldSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/evocation/ShieldSpell.java), fonte fixada no commit `e4056af90302d37eb1739f5ff05020b020e6e252` de Iron's 1.21.1-3.16.3.
- **ID local:** `irons_spellbooks:shield` (não inferir caso não extraído); escola `evocation`.
- **DefaultConfig:** minRarity `COMMON`, maxLevel `10`, cooldown `8` s, cast `INSTANT`.
- **Campos Java:** `baseManaCost`=`35`; `manaCostPerLevel`=`5`; `baseSpellPower`=`5`; `spellPowerPerLevel`=`10`; `castTime`=`0`.
- **Métodos operacionais:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastStartSound()`, `getCastFinishSound()`, `onCast()`, `getShieldHP()`.
- **Fórmulas de retorno numérico direto:** `getShieldHP = 10 + getSpellPower(spellLevel, caster)`. Não cobrem cálculos locais complexos.
- **Pistas de alvo, dano e entidade:** `RaycastBuilder`, `addFreshEntity`.

**Codex / modificadores:** verificar corpo de `onCast`, validação de alvo e classe auxiliar antes de classificar tipo de dano, área, alcance ou efeito. Modificação por atributo nativo de Iron's é diferente de alteração de variável local. Hook de range/count/area não foi provado; sem hook, ⚠️ condicionado/fail-closed. Proteger custos, cooldown, casts duplicados, orçamento de entidades, Mastery e caps. RPG Skill Tree controla perks/Mastery/gates, Iron's controla seus spells e Black Arcana controla seu runtime. QA real não realizado. [Contrato transversal](../TECHNICAL-PERK-MAP.md).
