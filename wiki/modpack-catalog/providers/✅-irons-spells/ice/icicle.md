# Icicle

- **Status no modpack:** PRESENTE — ativo no catálogo atual
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **Spell ID:** `irons_spellbooks:icicle`
- **JAR/versão instalada:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Ice
- **Níveis:** 1–10
- **Raridade:** Common → Legendary
- **Cast:** Instant
- **Mana:** 10–28
- **Cooldown:** 1 s
- **Dano atual:** 6–10,5

## O que faz

Dispara um icicle perfurante de energia fria que causa dano e congela criaturas atravessadas.

## Source audit 3.16.3 — commit `e4056af...`

- cria `IcicleProjectile` na altura dos olhos, dispara no look angle e remove gravidade;
- spell power base 12, +1/level;
- damage = `spellPower * 0.5`;
- damage source adiciona 80 freeze ticks.

A propriedade de piercing é confirmada pelo catálogo atual; a implementação fina de multi-hit/piercing pertence ao projectile e não foi reconstruída nesta ficha.

## Targets / PvP / bosses / summons

- **Targeting:** projétil na direção de visão.
- **Players em PvP, bosses e summons:** friendly-fire/imunidades/piercing específicos `NÃO VERIFICADO`.
- Não inferir que todos os tipos de entidade aceitam freeze da mesma forma.

## Obtenção, requisitos e aprendizado

- pipeline geral de scrolls/spellbooks;
- rotas específicas `NÃO VERIFICADO`;
- requisitos adicionais `NÃO VERIFICADO`;
- itens/focus/rituais específicos `NÃO VERIFICADO`.

## Integrações / QA / fail-closed

- **Projectile authority:** `IcicleProjectile`.
- bridge específica `NÃO VERIFICADO`.
- VFX/áudio/precise piercing e QA client-real `NÃO VERIFICADO`.
- Não reaplicar dano/freeze por hit em segundo pipeline.

## Deduplicação

Já cobre fast piercing Ice bolt com freeze.

## Matriz obrigatória de verificação

- **Status/provider/mod ID/JAR/spell ID/escola/tipo:** confirmados; tipo funcional = projectile Ice piercing.
- **Descrição funcional:** confirmada pelo catálogo; multi-hit fino `NÃO VERIFICADO`.
- **Níveis/raridade:** 1–10 / Common → Legendary.
- **Cast type / cast time / channel:** `INSTANT` / 0 ticks / não channel.
- **Recurso/custo:** mana / 10–28; fórmula fina de custo `NÃO VERIFICADO`.
- **Cooldown:** 1 s.
- **Dano/cura/tipo de dano:** 6–10,5; cura não aplicável; freeze80 source-auditado; tipo/tag de dano exato `NÃO VERIFICADO`.
- **Alcance/raio/área/duração:** projectile forward; alcance/lifetime `NÃO VERIFICADO`; área nominal = projectile/piercing, raio/hitbox `NÃO VERIFICADO`.
- **Scaling/fórmulas/caps:** spell power base12 +1/level; damage `spellPower*0.5`; caps além de nível10 `NÃO VERIFICADO`.
- **Targets/PvP/bosses/summons:** conforme seção; immunity/friendly-fire `NÃO VERIFICADO`.
- **Condições/requisitos:** adicionais `NÃO VERIFICADO`.
- **Obtenção/fabricação/ganho/aprendizado:** pipeline geral; rotas específicas `NÃO VERIFICADO`.
- **Itens/focus/rituais:** específicos `NÃO VERIFICADO`.
- **VFX/partículas/textura/animação/áudio:** todos `NÃO VERIFICADO` nesta ficha além da entidade projectile conhecida.
- **Integrações/bridges:** projectile provider-owned; bridge específica `NÃO VERIFICADO`.
- **Deduplicação/sobreposição:** conclusão baseada no source pinado + catálogo.
- **Bugs/QA/fail-closed:** precise piercing e QA real `NÃO VERIFICADO`; não duplicar hit/damage/freeze.
- **Fonte/evidência/estado:** catálogo + source 3.16.3.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/` — consulta 2026-09-06.
- Source 3.16.3 `e4056af...`: `IcicleSpell.java` + `gradle.properties`.

## Parâmetros de implementação para perks — source auditado

- **Classe/commit:** [`IcicleSpell.java`](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/ice/IcicleSpell.java) (source fixo 1.21.1-3.16.3).
- **ID de spell lido na classe:** `irons_spellbooks:icicle` (NÃO EXTRAÍDO implica revisar registry).
- **Config:** minRarity `COMMON`; maxLevel `10`; cooldown `1` segundos; cast `INSTANT`.
- **Campos Java:** `baseManaCost`=`10`; `manaCostPerLevel`=`2`; `baseSpellPower`=`12`; `spellPowerPerLevel`=`1`; `castTime`=`0`.
- **Métodos no código:** `getUniqueInfo()`, `getCastType()`, `getDefaultConfig()`, `getSpellResource()`, `onCast()`, `getDamage()`, `getDamageSource()`.
- **Fórmulas numéricas com retorno direto:** `getDamage = getSpellPower(spellLevel, entity) * .5f`. Não são fórmulas completas de efeitos indiretos.
- **Pistas de execução (verificar semântica):** `SpellDamageSource`, `addFreshEntity`.

**Contrato de perks:** a escola `ice` não garante, sozinha, um damage type de gelo/frost nem status de freeze. Identificar classe que aplica efeitos, limites de duração/slow e colisão antes de propor modificadores. Atributo nativo de Iron's não é hook universal de raio/ângulo/quantidade. Exigir adapter comprovado, proteção contra duplicação e caps; caso contrário ⚠️ condicionado/fail-closed. Iron's mantém cast/efeitos/mana; RPG Skill Tree possui perks/Mastery/gates; Black Arcana mantém runtime próprio. QA real pendente. [Mapa global](../TECHNICAL-PERK-MAP.md).
