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

## Snapshot upstream `e4056af...` — NÃO tratado como tag 3.16.3

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

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/` — consulta 2026-09-06.
- Snapshot upstream `e4056af...`: `IcicleSpell.java`.
