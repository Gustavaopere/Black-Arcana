# Scapegoat

- **Status no modpack:** PRESENTE — provider instalado
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Evocation
- **Níveis:** 1–3
- **Raridade:** Rare → Legendary
- **Cast:** Instant
- **Mana:** 30–60
- **Cooldown:** 45 s
- **Taunt range:** 12 blocos
- **Vida:** 20–40 HP

## O que faz

Conjura um decoy mágico em forma de cabra. Ele toma o aggro de mobs hostis próximos e corre para longe, atraindo-os durante sua existência.

## Escalonamento

O catálogo atual confirma 12 blocos de alcance de taunt e 20–40 HP. Duração, velocidade, regras de seleção de mobs e AI exatas ficam `NÃO VERIFICADO`.

## Obtenção e aprendizado

Segue o pipeline geral de scrolls/spellbooks do Iron's. Scapegoat foi adicionado na linha 3.16.2; rotas específicas permanecem `NÃO VERIFICADO`.

## Deduplicação / authority

Já cobre summon/decoy de transferência de aggro. Um sistema Black Arcana de protetor/decoy precisa de delta real. Iron's permanece authority da AI, vida e taunt do summon; integrações não devem aplicar um segundo taunt para a mesma conjuração.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`
- Changelog 3.16.2: `https://iron.wiki/changelog/`
- Consulta: 2026-09-06.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`ScapegoatSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/evocation/ScapegoatSpell.java), fonte fixada no commit `e4056af90302d37eb1739f5ff05020b020e6e252` de Iron's 1.21.1-3.16.3.
- **ID local:** `irons_spellbooks:scapegoat` (não inferir caso não extraído); escola `evocation`.
- **DefaultConfig:** minRarity `RARE`, maxLevel `3`, cooldown `45` s, cast `INSTANT`.
- **Campos Java:** `baseManaCost`=`30`; `manaCostPerLevel`=`15`; `baseSpellPower`=`20`; `spellPowerPerLevel`=`10`; `castTime`=`0`.
- **Métodos operacionais:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `onCast()`, `getRange()`, `getGoatHealth()`.
- **Fórmulas de retorno numérico direto:** `getRange = 18`; `getGoatHealth = getSpellPower(spellLevel, entity)`. Não cobrem cálculos locais complexos.
- **Pistas de alvo, dano e entidade:** `addFreshEntity`.

**Codex / modificadores:** verificar corpo de `onCast`, validação de alvo e classe auxiliar antes de classificar tipo de dano, área, alcance ou efeito. Modificação por atributo nativo de Iron's é diferente de alteração de variável local. Hook de range/count/area não foi provado; sem hook, ⚠️ condicionado/fail-closed. Proteger custos, cooldown, casts duplicados, orçamento de entidades, Mastery e caps. RPG Skill Tree controla perks/Mastery/gates, Iron's controla seus spells e Black Arcana controla seu runtime. QA real não realizado. [Contrato transversal](../TECHNICAL-PERK-MAP.md).
