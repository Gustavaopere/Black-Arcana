# Breaching Enemy

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:breaching_enemy`
- **Iron's school:** Lightning
- **Levels:** 1–5
- **Minimum rarity:** Rare
- **Cast type:** Long
- **Cooldown:** 12 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 100`
- `baseManaCost = 60`
- `manaCostPerLevel = 15`
- `castTime = 20 ticks`
- pellet count: **12**
- range: **8 blocks**

Raw per-provider damage input is `spellPower / 100`, then multiplied by `DamageMultiplierKey.BREACHING_ENEMY` before being seeded into the summoned shotgun entity.

## Cast lifecycle

The spell summons the shotgun during the cast. On successful completion it refreshes the weapon damage from current spell power, fires once and keeps the weapon only for its provider firing animation/lifecycle. Cancelling the cast releases the weapon without firing.

The spell is marked as affected by the provider's Magi Agent Suit contract, which may modify interruptibility. That equipment behavior is provider-owned and is not an RPG Skill Tree perk.

## What it does

Provider guide semantics: summons a magical shotgun and fires a short-range 12-pellet blast. Its defining behavior is extremely strong knockback at close range.

The exact pellet spread/individual hit/knockback settlement lives in the provider shotgun entity. Black Arcana must not independently replay 12 damage/proc events from one completed cast.

## Acquisition

Registered through Iron's spell registry. Exact 0.9.7.1 scroll/loot availability remains in the provider-wide acquisition audit.

## Deduplication

Occupies the **short-range magical shotgun / multi-pellet / heavy knockback** niche. A Chaos-force shotgun would not be distinct merely by changing damage school or VFX.

## Confidence

`SOURCE-PINNED SPELL + PROVIDER GUIDE / SHOTGUN PELLET ENTITY SETTLEMENT + PACK CONFIG MULTIPLIER QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:breaching_enemy` → `SpellRegistry.reg("breaching_enemy", BreachingEnemy::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.breachingenemy.BreachingEnemy`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/breachingenemy/BreachingEnemy.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.

## Engenharia causal aprofundada — armas conjuradas e efeitos derivados (2026-10-14)

**Registry ID:** `apprenticecodex:breaching_enemy`. **Source fixado:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e` (versão declarada 0.9.7.1). Classe e helpers: [BreachingEnemy.java](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/breachingenemy/BreachingEnemy.java); [BreachingEnemyShotgunEntity.java](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/breachingenemy/BreachingEnemyShotgunEntity.java).

**Cadeia causal verificada no source:** BreachingEnemy.onCastNoWeapon instancia a shotgun e parâmetros de dano/range/count; onCastCompleteWithWeapon recalcula dano e chama fire apenas sem cancelamento, preservando entidade durante liberação. BreachingEnemyShotgunEntity.fire faz um raycast por pellet, agrega contagens de pellets por entity ID e block position, resolve multipart e chama CombatTools.applyDamage uma vez por entrada com dano multiplicado pelo total de pellets. Tracers e efeitos de impacto por pellet são visuais, não casts.

**QA direcionado (pendente):** Amplificação de dano/knockback e agregação multipart, prova do impacto em bloco sob claims, volume de packets tracer por pellet, cancelamento/reload.

**Authority/boundary:** o cast, mana, recast e cooldown base permanecem no Iron's; armas, projetos e efeitos são do Apprentice's Codex. Uma rajada, hit, hitbox, tracer, loot extra ou counterspell derivado **não é novo cast** e não autoriza recompensa/XP/Mastery independente. Black Arcana não replica custos, damage, loot, hit ou efeitos externos. Integração com RPG Skill Tree ⛔ fail-closed até receipt/callback server-side unívoco e homologado. ⚠️ Esta inspeção source-level não comprova o corpo dos métodos no JAR compilado, configs ativas ou QA físico de modpack.
