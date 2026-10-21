# Firecracker

- **Status no modpack:** PRESENTE — provider instalado
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Evocation
- **Níveis:** 1–10
- **Raridade:** Common → Legendary
- **Cast:** Instant
- **Mana:** 20–38
- **Cooldown:** 1 s
- **Dano:** 4–13

## O que faz

Conjura instantaneamente um firework no ponto mirado, que explode em uma pequena área ao redor da manifestação.

## Escalonamento

O dano listado cresce de 4 para 13. Raio exato, falloff e interação com entidades/blocos permanecem `NÃO VERIFICADO`.

## Obtenção e aprendizado

Segue o pipeline geral de scrolls/spellbooks do Iron's. Rotas específicas permanecem `NÃO VERIFICADO`.

## Deduplicação

Já cobre explosão instantânea de baixo cooldown no ponto mirado. Uma futura magia explosiva Black Arcana precisa de mecânica/custo/causalidade própria além de VFX distinto.

## VFX / animação / áudio

A própria semântica pública identifica apresentação de firework; detalhes do runtime real permanecem `NÃO VERIFICADO`.

## Fonte / evidência

Catálogo oficial atual: `https://iron.wiki/spells/` — consulta em 2026-09-06.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`FirecrackerSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/evocation/FirecrackerSpell.java), fonte fixada no commit `e4056af90302d37eb1739f5ff05020b020e6e252` de Iron's 1.21.1-3.16.3.
- **ID local:** `irons_spellbooks:firecracker` (não inferir caso não extraído); escola `evocation`.
- **DefaultConfig:** minRarity `COMMON`, maxLevel `10`, cooldown `1.5` s, cast `INSTANT`.
- **Campos Java:** `baseManaCost`=`20`; `manaCostPerLevel`=`2`; `baseSpellPower`=`4`; `spellPowerPerLevel`=`1`; `castTime`=`0`.
- **Métodos operacionais:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `onCast()`, `getRange()`, `getDamage()`.
- **Fórmulas de retorno numérico direto:** `getRange = 15 + (int) (getSpellPower(spellLevel, entity) * 2)`; `getDamage = getSpellPower(spellLevel, entity)`. Não cobrem cálculos locais complexos.
- **Pistas de alvo, dano e entidade:** `RaycastBuilder`, `addFreshEntity`.

**Codex / modificadores:** verificar corpo de `onCast`, validação de alvo e classe auxiliar antes de classificar tipo de dano, área, alcance ou efeito. Modificação por atributo nativo de Iron's é diferente de alteração de variável local. Hook de range/count/area não foi provado; sem hook, ⚠️ condicionado/fail-closed. Proteger custos, cooldown, casts duplicados, orçamento de entidades, Mastery e caps. RPG Skill Tree controla perks/Mastery/gates, Iron's controla seus spells e Black Arcana controla seu runtime. QA real não realizado. [Contrato transversal](../TECHNICAL-PERK-MAP.md).
