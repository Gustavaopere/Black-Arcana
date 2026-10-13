# Fang Ward

- **Status no modpack:** PRESENTE — provider instalado
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Evocation
- **Níveis:** 1–8
- **Raridade:** Common → Legendary
- **Cast:** Long
- **Mana:** 45–80
- **Cooldown:** 15 s
- **Anéis:** 2–4
- **Dano:** 8–15

## O que faz

Conjura anéis protetores de Evoker Fangs ao redor do caster, formando uma defesa ofensiva de proximidade.

## Escalonamento

O catálogo atual confirma 2–4 anéis e 8–15 de dano. Raio exato dos anéis, persistência e regras de hit ficam `NÃO VERIFICADO`.

## Obtenção e aprendizado

Segue o pipeline geral de scrolls/spellbooks do Iron's. O Grimoire of Evokation atualmente pode vir com Fang Ward 4 já inscrito e é descrito como drop raro de Evokers ou Archevokers; outras rotas específicas continuam `NÃO VERIFICADO`.

## Deduplicação

Já cobre ward corporal ofensivo por anéis de fangs. Um futuro ward Black Arcana precisa de autoridade/regra distinta, não somente outra aparência.

## VFX / animação / áudio

`NÃO VERIFICADO` no runtime real do pack neste passe.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`
- Spellbook oficial atual: `https://iron.wiki/spellbooks/`
- Consulta: 2026-09-06.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`FangWardSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/evocation/FangWardSpell.java), fonte fixada no commit `e4056af90302d37eb1739f5ff05020b020e6e252` de Iron's 1.21.1-3.16.3.
- **ID local:** `irons_spellbooks:fang_ward` (não inferir caso não extraído); escola `evocation`.
- **DefaultConfig:** minRarity `COMMON`, maxLevel `8`, cooldown `15` s, cast `LONG`.
- **Campos Java:** `baseManaCost`=`45`; `manaCostPerLevel`=`5`; `baseSpellPower`=`8`; `spellPowerPerLevel`=`1`; `castTime`=`15`.
- **Métodos operacionais:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastStartSound()`, `onCast()`, `get2DAngle()`, `getGroundLevel()`, `getDamage()`, `getRings()`.
- **Fórmulas de retorno numérico direto:** `get2DAngle = Utils.getAngle(new Vec2((float) a.x, (float) a.z), new Vec2((float) b.x, (float) b.z))`; `getDamage = getSpellPower(spellLevel, entity)`; `getRings = 2 + (spellLevel - 1) / 3`. Não cobrem cálculos locais complexos.
- **Pistas de alvo, dano e entidade:** `addFreshEntity`.

**Codex / modificadores:** verificar corpo de `onCast`, validação de alvo e classe auxiliar antes de classificar tipo de dano, área, alcance ou efeito. Modificação por atributo nativo de Iron's é diferente de alteração de variável local. Hook de range/count/area não foi provado; sem hook, ⚠️ condicionado/fail-closed. Proteger custos, cooldown, casts duplicados, orçamento de entidades, Mastery e caps. RPG Skill Tree controla perks/Mastery/gates, Iron's controla seus spells e Black Arcana controla seu runtime. QA real não realizado. [Contrato transversal](../TECHNICAL-PERK-MAP.md).
