# Slow

- **Status no modpack:** PRESENTE — provider instalado
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Evocation
- **Níveis:** 1–4
- **Raridade:** Epic → Legendary
- **Cast:** Long
- **Mana:** 50–80
- **Cooldown:** 80 s
- **Magical Slow:** 20%
- **Duração:** 20–32 s

## O que faz

Aplica o efeito Slowed a uma criatura alvo. O catálogo atual documenta redução de movement speed, attack speed, mining speed e cast time reduction durante o efeito.

## Escalonamento

A build atual lista 20% de Magical Slow e duração de 20–32 segundos em quatro níveis. A página histórica 1.19 descrevia outro contrato, incluindo até 60% e cinco alvos; esses números antigos não são usados aqui.

## Obtenção e aprendizado

Segue o pipeline geral de scrolls/spellbooks do Iron's. Rotas específicas permanecem `NÃO VERIFICADO`.

## Deduplicação

Já cobre slow mágico multiestatístico, inclusive redução de cast-time reduction. Uma magia Black Arcana de lentidão precisa de semântica adicional, e integrações não devem aplicar uma segunda redução equivalente sobre o mesmo efeito sem contrato explícito.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/`
- Página histórica 1.19 usada apenas para detectar divergência: `https://iron.wiki/1_19/spells/`
- Consulta: 2026-09-06.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`SlowSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/evocation/SlowSpell.java), fonte fixada no commit `e4056af90302d37eb1739f5ff05020b020e6e252` de Iron's 1.21.1-3.16.3.
- **ID local:** `irons_spellbooks:slow` (não inferir caso não extraído); escola `evocation`.
- **DefaultConfig:** minRarity `EPIC`, maxLevel `4`, cooldown `80` s, cast `LONG`.
- **Campos Java:** `baseManaCost`=`50`; `manaCostPerLevel`=`10`; `baseSpellPower`=`20`; `spellPowerPerLevel`=`4`; `castTime`=`30`.
- **Métodos operacionais:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastStartSound()`, `checkPreCastConditions()`, `onCast()`, `getAmplifier()`, `getDuration()`, `getTargetingColor()`.
- **Fórmulas de retorno numérico direto:** `getDuration = (int) (getSpellPower(spellLevel, caster) * 20)`. Não cobrem cálculos locais complexos.
- **Pistas de alvo, dano e entidade:** `TargetEntityCastData`, `MobEffectInstance`, `DamageSources`, `addEffect`, `ParticleHelper`.

**Codex / modificadores:** verificar corpo de `onCast`, validação de alvo e classe auxiliar antes de classificar tipo de dano, área, alcance ou efeito. Modificação por atributo nativo de Iron's é diferente de alteração de variável local. Hook de range/count/area não foi provado; sem hook, ⚠️ condicionado/fail-closed. Proteger custos, cooldown, casts duplicados, orçamento de entidades, Mastery e caps. RPG Skill Tree controla perks/Mastery/gates, Iron's controla seus spells e Black Arcana controla seu runtime. QA real não realizado. [Contrato transversal](../TECHNICAL-PERK-MAP.md).
