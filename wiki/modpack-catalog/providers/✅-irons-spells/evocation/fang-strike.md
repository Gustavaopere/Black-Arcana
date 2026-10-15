# Fang Strike

- **Status no modpack:** PRESENTE — provider instalado
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Evocation
- **Níveis:** 1–10
- **Raridade:** Common → Legendary
- **Cast:** Long
- **Mana:** 30–57
- **Cooldown:** 5 s
- **Evoker Fangs:** 8–17
- **Dano:** 6–15

## O que faz

Conjura uma linha de Evoker Fangs à frente do caster, seguindo o arquétipo de ataque dos illagers.

## Escalonamento

O catálogo oficial atual confirma crescimento de 8 para 17 fangs e de 6 para 15 de dano. Espaçamento, comprimento geométrico exato e regras de hit múltiplo permanecem `NÃO VERIFICADO`.

## Obtenção e aprendizado

Segue o pipeline geral de scrolls/spellbooks do Iron's. O Grimoire of Evokation atualmente pode vir com Fang Strike 6 já inscrito e é descrito como drop raro de Evokers ou Archevokers; outras rotas específicas continuam `NÃO VERIFICADO`.

## Deduplicação

Já cobre linha frontal de fangs como ataque terrestre/evocation. Um candidato Black Arcana equivalente precisa alterar materialmente targeting, resource contract ou consequência.

## VFX / animação / áudio

`NÃO VERIFICADO` no runtime real do pack neste passe.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`
- Spellbook oficial atual / Grimoire of Evokation: `https://iron.wiki/spellbooks/`
- Consulta: 2026-09-06.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`FangStrikeSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/evocation/FangStrikeSpell.java), fonte fixada no commit `e4056af90302d37eb1739f5ff05020b020e6e252` de Iron's 1.21.1-3.16.3.
- **ID local:** `irons_spellbooks:fang_strike` (não inferir caso não extraído); escola `evocation`.
- **DefaultConfig:** minRarity `COMMON`, maxLevel `10`, cooldown `5` s, cast `LONG`.
- **Campos Java:** `baseManaCost`=`30`; `manaCostPerLevel`=`3`; `baseSpellPower`=`6`; `spellPowerPerLevel`=`1`; `castTime`=`15`.
- **Métodos operacionais:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastStartSound()`, `onCast()`, `getGroundLevel()`, `getCount()`, `getDamage()`.
- **Fórmulas de retorno numérico direto:** `getCount = 7 + spellLevel`; `getDamage = getSpellPower(spellLevel, entity)`. Não cobrem cálculos locais complexos.
- **Pistas de alvo, dano e entidade:** `addFreshEntity`.

**Codex / modificadores:** verificar corpo de `onCast`, validação de alvo e classe auxiliar antes de classificar tipo de dano, área, alcance ou efeito. Modificação por atributo nativo de Iron's é diferente de alteração de variável local. Hook de range/count/area não foi provado; sem hook, ⚠️ condicionado/fail-closed. Proteger custos, cooldown, casts duplicados, orçamento de entidades, Mastery e caps. RPG Skill Tree controla perks/Mastery/gates, Iron's controla seus spells e Black Arcana controla seu runtime. QA real não realizado. [Contrato transversal](../TECHNICAL-PERK-MAP.md).
