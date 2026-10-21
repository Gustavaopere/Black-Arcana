# Spectral Hammer

- **Status no modpack:** PRESENTE — provider instalado
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Evocation
- **Níveis:** 1–5
- **Raridade:** Uncommon → Legendary
- **Cast:** Instant
- **Mana:** 15–35
- **Cooldown:** 2 s
- **Volume listado:** 3×3×2
- **Alcance:** 16 blocos

## O que faz

Conjura um martelo espectral no ponto mirado que minera blocos conectados do tipo pedra em um volume cúbico, deixando minérios e rubble para trás conforme a descrição pública atual.

## Escalonamento

O catálogo atual lista volume 3×3×2 e alcance 16 blocos. Quais tags/blocos contam como stone-type, custo por bloco, drops e comportamento exato com proteções permanecem `NÃO VERIFICADO`.

## Obtenção e aprendizado

Segue o pipeline geral de scrolls/spellbooks do Iron's. Rotas específicas permanecem `NÃO VERIFICADO`.

## Deduplicação / world safety

Já cobre mineração mágica volumétrica seletiva. Black Arcana não deve duplicar isso como world mutation genérica. Qualquer integração deve continuar submetida às próprias políticas de proteção/world safety e nunca usar o spell como justificativa para contornar blocos protegidos ou limites de mutação.

## Fonte / evidência

Catálogo oficial atual: `https://iron.wiki/spells/` — consulta em 2026-09-06.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`SpectralHammerSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/evocation/SpectralHammerSpell.java), fonte fixada no commit `e4056af90302d37eb1739f5ff05020b020e6e252` de Iron's 1.21.1-3.16.3.
- **ID local:** `irons_spellbooks:spectral_hammer` (não inferir caso não extraído); escola `evocation`.
- **DefaultConfig:** minRarity `UNCOMMON`, maxLevel `5`, cooldown `2` s, cast `INSTANT`.
- **Campos Java:** `baseManaCost`=`15`; `manaCostPerLevel`=`5`; `baseSpellPower`=`1`; `spellPowerPerLevel`=`1`; `castTime`=`0`.
- **Métodos operacionais:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `checkPreCastConditions()`, `onCast()`, `getDepth()`, `getRadius()`.
- **Fórmulas de retorno numérico direto:** `getDepth = (int) getSpellPower(spellLevel, caster)`; `getRadius = (int) Math.max(getSpellPower(spellLevel, caster) * .5f, 1)`. Não cobrem cálculos locais complexos.
- **Pistas de alvo, dano e entidade:** `addFreshEntity`.

**Codex / modificadores:** verificar corpo de `onCast`, validação de alvo e classe auxiliar antes de classificar tipo de dano, área, alcance ou efeito. Modificação por atributo nativo de Iron's é diferente de alteração de variável local. Hook de range/count/area não foi provado; sem hook, ⚠️ condicionado/fail-closed. Proteger custos, cooldown, casts duplicados, orçamento de entidades, Mastery e caps. RPG Skill Tree controla perks/Mastery/gates, Iron's controla seus spells e Black Arcana controla seu runtime. QA real não realizado. [Contrato transversal](../TECHNICAL-PERK-MAP.md).
