# Inscribe Ice

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:inscribe_ice`
- **Iron's school:** Ice
- **Levels:** 1–5
- **Minimum rarity:** Uncommon
- **Cast type:** Instant
- **Cooldown:** 2 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 30`
- `baseManaCost = 30`
- `manaCostPerLevel = 15`
- `castTime = 0`

Iron's owns the effective per-level spell-power/mana settlement. The provider's raw formulas are:

- dagger hit damage: `1 + 2 * spellPower / 100`, then `DamageMultiplierKey.INSCRIBE_ICE`;
- burst damage: `12 * spellPower / 100`, then the same server multiplier;
- projectile count: `round(3 * spellPower / 100)`, forced to the next odd number when even;
- fan arc: `clamp(60 + (projectileCount - 3) * 10, 60, 120)` degrees.

The user's configured damage multiplier remains runtime/config QA.

## Projectile lifecycle

Exact dagger entity behavior:

- projectile speed: **1.68 blocks/tick**;
- maximum life: **100 ticks / 5 s**;
- initial block-collision grace: **4 ticks**;
- no gravity;
- valid combat-target filtering is provider-owned;
- projectile is anti-magic susceptible and discards on anti-magic;
- successful dagger damage applies/advances `Notched Frozen`.

## Notched Frozen and third-hit burst

Exact `NotchedFrozenEffect` values:

- duration: **300 ticks / 15 s**;
- maximum stack amplifier: **1**.

Therefore the first successful dagger hit applies amplifier 0, the second advances to amplifier 1, and the next successful application triggers the burst. This matches the provider guide's "third successful inscription" description.

While active, the effect extends existing frozen ticks by 2 each effect tick; the effect itself is provider-owned and is not a Black Arcana Corruption/Strain channel.

## Burst and chain propagation

Exact burst implementation:

- blast half-extent: **2.5 blocks** (5×5×5 AABB);
- direct burst uses the spell's full burst damage;
- chain propagation starts at **50%** of the original burst damage;
- chained bursts continue using that chain damage value;
- a processed-entity set prevents the same entity from recursively bursting twice within one chain;
- burst removes `Notched Frozen` from the origin;
- nearby valid living targets carrying `Notched Frozen` can chain-burst after receiving damage;
- players are explicitly excluded from secondary burst candidates by this burst helper;
- no knockback is applied by the burst damage settlement.

This causality is one provider-owned chain. Black Arcana must not treat each chained detonation as a new independent proc source or generate additional offensive proc chains from it.

## What it does

The provider guide describes a fan of ice daggers that inscribe ice magic into damaged mobs. On the third successful inscription the mark bursts for heavy damage, and that burst can trigger nearby inscriptions in turn.

## Acquisition

Registered through Iron's spell registry. Exact 0.9.7.1 scroll/loot/recipe availability remains in the provider-wide acquisition audit.

## Deduplication

Occupies the **multi-projectile Ice mark → third-hit burst → bounded chain propagation** niche. Black Arcana should not reproduce the same stack/burst identity under a new name or particle set.

## Confidence

`SOURCE-PINNED SPELL + PROJECTILE + EFFECT + BURST CHAIN / PACK CONFIG MULTIPLIER + FULL RUNTIME QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:inscribe_ice` → `SpellRegistry.reg("inscribe_ice", InscribeIce::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.inscribeice.InscribeIce`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/inscribeice/InscribeIce.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.

## Engenharia causal aprofundada — mundo, channel e defesa (2026-10-14)

**ID causal:** `apprenticecodex:inscribe_ice` — uma magia Iron's-native; ticks/jobs/entidades/impactos são efeitos-filhos, nunca um novo cast.

**Source pin:** [InscribeIce.java](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/inscribeice/InscribeIce.java); [InscribeIceDaggerThrowJob.java](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/inscribeice/InscribeIceDaggerThrowJob.java); [InscribeIceDaggerThrowJobManager.java](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/inscribeice/InscribeIceDaggerThrowJobManager.java); [InscribeIceBurst.java](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/inscribeice/InscribeIceBurst.java).

**Cadeia verificada em source:** InscribeIce.onCast cria o job, faz tick imediato e submete remanescentes; a geometria de RemoteOwnerCastContext é congelada porque o contexto só vive dentro de onCast. InscribeIceDaggerThrowJob.tick/releaseBucket separa os disparos por tick; encerra após conclusão, caster inválido ou deadline. Manager.onLevelTick retira jobs terminados. InscribeIceBurst.burst/burstChain remove marca NOTCHED_FROZEN na origem, deduplica IDs processados e só encadeia após dano aplicado a alvo marcado.

**QA prioritário (não executado):** Concorrência de jobs por nível, cadeia recursiva, caster inválido, targets multipart, PvP e tiros remote.

**Boundary:** mana/casting Iron's e efeitos Apprentice's; nenhuma segunda liquidação/XP/Mastery por Black Arcana; contrato RPG sem hook comprovado: ⛔ fail-closed. ⚠️ Sem prova de bytecode do JAR instalado, config nem QA físico.
