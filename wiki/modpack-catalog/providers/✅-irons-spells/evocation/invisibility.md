# Invisibility

- **Status no modpack:** PRESENTE — provider instalado
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Evocation
- **Níveis:** 1–6
- **Raridade:** Rare → Legendary
- **Cast:** Long
- **Mana:** 35–75
- **Cooldown:** 45 s
- **Duração:** 10–35 s

## O que faz

Concede invisibilidade verdadeira temporária ao caster, ocultando também armadura e itens empunhados. Mobs perdem aggro; o efeito termina imediatamente quando o caster causa dano.

## Escalonamento

A duração atual listada cresce de 10 para 35 segundos. Outras regras de detecção, partículas e exceções ficam `NÃO VERIFICADO`.

## Obtenção e aprendizado

Segue o pipeline geral de scrolls/spellbooks do Iron's. Rotas específicas permanecem `NÃO VERIFICADO`.

## Deduplicação / authority

Já cobre stealth real com perda de aggro e break-on-damage. Uma magia Black Arcana de invisibilidade precisa de contrato diferente; bridges não devem manter invisibilidade depois que o provider encerra o efeito por dano.

## QA / VFX

O changelog 3.16.2 registra VFX de cast para Invisibility. Detalhes visuais do runtime real do pack permanecem `NÃO VERIFICADO`.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`
- Changelog oficial atual: `https://iron.wiki/changelog/`
- Consulta: 2026-09-06.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`InvisibilitySpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/evocation/InvisibilitySpell.java), fonte fixada no commit `e4056af90302d37eb1739f5ff05020b020e6e252` de Iron's 1.21.1-3.16.3.
- **ID local:** `irons_spellbooks:invisibility` (não inferir caso não extraído); escola `evocation`.
- **DefaultConfig:** minRarity `RARE`, maxLevel `6`, cooldown `45` s, cast `LONG`.
- **Campos Java:** `baseManaCost`=`35`; `manaCostPerLevel`=`8`; `baseSpellPower`=`10`; `spellPowerPerLevel`=`5`; `castTime`=`40`.
- **Métodos operacionais:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastStartSound()`, `onCast()`, `getDuration()`.
- **Fórmulas de retorno numérico direto:** `getDuration = (int) (getSpellPower(spellLevel, source) * 20)`. Não cobrem cálculos locais complexos.
- **Pistas de alvo, dano e entidade:** `MobEffectInstance`, `addEffect`.

**Codex / modificadores:** verificar corpo de `onCast`, validação de alvo e classe auxiliar antes de classificar tipo de dano, área, alcance ou efeito. Modificação por atributo nativo de Iron's é diferente de alteração de variável local. Hook de range/count/area não foi provado; sem hook, ⚠️ condicionado/fail-closed. Proteger custos, cooldown, casts duplicados, orçamento de entidades, Mastery e caps. RPG Skill Tree controla perks/Mastery/gates, Iron's controla seus spells e Black Arcana controla seu runtime. QA real não realizado. [Contrato transversal](../TECHNICAL-PERK-MAP.md).
