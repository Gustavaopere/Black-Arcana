# Harvest Moon

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:harvest_moon`
- **School:** Nature
- **Levels:** 1–4
- **Minimum rarity:** Uncommon
- **Cast type:** Long
- **Cooldown:** 20 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 12`
- `spellPowerPerLevel = 12`
- `baseManaCost = 60`
- `manaCostPerLevel = 20`
- `castTime = 50 ticks / 2.5 s`
- job budget: **32 harvest actions per tick**

Search range:

`8 * spellPower / 10`

The executable cast floors this range to an integer of at least 1 block before collecting targets.

## Target collection

The provider collects mature harvestable targets around the caster using a bounded cuboid:

- X/Z: `origin ± range`;
- Y: from one block below the player through three blocks above;
- out-of-world positions are skipped;
- already-visited positions are deduplicated;
- blocks in the provider `HARVEST_MOON_DENYLIST` are excluded.

The collector has provider-specific handling for mature vanilla crops, Nether Wart, Sweet Berry Bushes, Comfort Berry Bushes, attached melons/pumpkins, root-preserving columns such as sugar cane/cactus/bamboo, chorus clusters and supported generic age-based crops. Actions are sorted nearest-first before the job starts.

## Bounded harvesting job

On a successful server cast by a real `ServerPlayer`, the spell freezes a copy of the caster's current main-hand stack and submits the collected actions to `HarvestMoonJobManager`/`HarvestMoonJob` with a fixed **32-block/action budget per tick**.

That copied tool context is intentional: later job ticks do not silently adopt a different main-hand item after the cast.

The spell is therefore one cast followed by provider-owned bounded follow-up work. Individual harvested blocks/crops are not separate casts or separate progression-authority events.

## What it does

Provider semantics are mass harvesting rather than destructive area clearing. Mature plants are processed through specialized actions intended to preserve roots/stems or normal harvesting behavior where applicable.

## World safety / integration boundary

Harvest Moon is a provider-owned world-processing mechanic. Black Arcana must not reuse its collector/job as a bypass around Black Arcana `WorldEffectPolicy`, nor re-harvest the same targets after observing the provider cast.

Any future RPG/Mastery integration must collapse the entire submitted harvest job back to the single causal Harvest Moon cast unless a separate provider contract explicitly exposes a safer discrete milestone.

## Confidence

`SOURCE-PINNED CAST + TARGET COLLECTOR + JOB BUDGET / DATAPACK DENYLIST CONTENT + FULL MODPACK HARVEST COMPAT RUNTIME QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:harvest_moon` → `SpellRegistry.reg("harvest_moon", HarvestMoon::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.harvestmoon.HarvestMoon`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/harvestmoon/HarvestMoon.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.
