# Lob Creeper

- **Status no modpack:** PRESENTE — provider instalado
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **JAR/versão:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Evocation
- **Níveis:** 1–10
- **Raridade:** Uncommon → Legendary
- **Cast:** Instant
- **Mana:** 20–38
- **Cooldown:** 2 s
- **Dano:** 6–10,5

## O que faz

Arremessa uma cabeça de Creeper que explode em uma área média no ponto de impacto. O catálogo atual registra que a velocidade do projétil cresce com o nível.

## Escalonamento

O dano listado cresce de 6 para 10,5. A fórmula exata da velocidade, raio de explosão e interação com terreno ficam `NÃO VERIFICADO`.

## Obtenção e aprendizado

Segue o pipeline geral de scrolls/spellbooks do Iron's. Rotas específicas permanecem `NÃO VERIFICADO`.

## Deduplicação

Já cobre projétil explosivo lobado com velocidade escalável. Uma variante Black Arcana não é lacuna apenas por mudar o projétil ou o VFX da explosão.

## VFX / animação / áudio

`NÃO VERIFICADO` no runtime real do pack neste passe.

## Fonte / evidência

Catálogo oficial atual: `https://iron.wiki/spells/` — consulta em 2026-09-06.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`LobCreeperSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/evocation/LobCreeperSpell.java), fonte fixada no commit `e4056af90302d37eb1739f5ff05020b020e6e252` de Iron's 1.21.1-3.16.3.
- **ID local:** `irons_spellbooks:lob_creeper` (não inferir caso não extraído); escola `evocation`.
- **DefaultConfig:** minRarity `UNCOMMON`, maxLevel `10`, cooldown `2` s, cast `INSTANT`.
- **Campos Java:** `baseManaCost`=`20`; `manaCostPerLevel`=`2`; `baseSpellPower`=`12`; `spellPowerPerLevel`=`1`; `castTime`=`0`.
- **Métodos operacionais:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `getCastStartSound()`, `getCastFinishSound()`, `onCast()`, `getDamage()`, `getDamageSource()`.
- **Fórmulas de retorno numérico direto:** `getDamage = this.getSpellPower(spellLevel, entity) * .5f`. Não cobrem cálculos locais complexos.
- **Pistas de alvo, dano e entidade:** `SpellDamageSource`, `addFreshEntity`.

**Codex / modificadores:** verificar corpo de `onCast`, validação de alvo e classe auxiliar antes de classificar tipo de dano, área, alcance ou efeito. Modificação por atributo nativo de Iron's é diferente de alteração de variável local. Hook de range/count/area não foi provado; sem hook, ⚠️ condicionado/fail-closed. Proteger custos, cooldown, casts duplicados, orçamento de entidades, Mastery e caps. RPG Skill Tree controla perks/Mastery/gates, Iron's controla seus spells e Black Arcana controla seu runtime. QA real não realizado. [Contrato transversal](../TECHNICAL-PERK-MAP.md).
