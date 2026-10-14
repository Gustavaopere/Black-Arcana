# Mana Charge

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:mana_charge`
- **Iron's school:** Holy
- **Levels:** 1–3
- **Minimum rarity:** Legendary
- **Cast type:** Continuous
- **Cooldown:** 120 s
- **Cast mana cost:** 0
- **Recovered resource:** canonical Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 50`
- `spellPowerPerLevel = 25`
- `baseManaCost = 0`
- `manaCostPerLevel = 0`
- `castTime = 100 ticks / 5 s`

Displayed mana recovery per second:

`spellPower * DamageMultiplierKey.MANA_CHARGE config multiplier`

The configuration plumbing reuses the provider's damage-multiplier infrastructure name, but the resulting value is mana recovery, not damage.

## Exact recovery cadence

Every **10 cast ticks / 0.5 s**, the spell computes half of the per-second recovery value and calls `MagicTools.recoverManaSafely(...)` against the same `MagicData` that owns the caster's Iron's mana.

Therefore, over an uninterrupted second, two half-second recovery settlements equal the displayed recovery-per-second value, subject to the provider's safe recovery/cap semantics.

## Authority

This spell proves that Apprentice's Codex does **not** introduce a parallel mana resource for this capability. It writes into canonical Iron's `MagicData` mana.

Black Arcana/RPG integrations must never mirror the recovered amount into another mana channel or independently reimburse mana from the same Mana Charge ticks.

## What it does

Provider guide semantics: rapidly recover mana while channeling. The long cooldown is part of the provider's balance identity.

## Deduplication

Occupies the **zero-cast-cost, long-cooldown active mana regeneration channel** niche.

## Confidence

`SOURCE-PINNED SPELL + RECOVERY CADENCE / PACK RECOVERY MULTIPLIER + IRON'S CAP RUNTIME QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:mana_charge` → `SpellRegistry.reg("mana_charge", ManaCharge::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.manacharge.ManaCharge`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/manacharge/ManaCharge.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.

## Engenharia causal aprofundada — ofensiva/movimento/sensoriamento (2026-10-14)

**Source:** [`manacharge/ManaCharge.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/manacharge/ManaCharge.java) · [`manacharge/ManaCharge.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/manacharge/ManaCharge.java).

- **Liquidação de mana:** `ManaCharge.onServerCastTick` usa `playerMagicData.getCastDurationRemaining() % 10 == 0` para recuperar `getManaRechargePerSecond(...)/2` via `MagicTools.recoverManaSafely`. O recurso é `MagicData` de Iron's, sem mana/credito próprio do Black Arcana.
- **Visual independente:** `spawnManaChargeParticles` envia **10 partículas** a cada **3 ticks** da idade da entidade, independente da cadência econômica de **10 ticks**. Partícula não é receipt de recuperação.
- **QA:** extremos de mana, custo zero, cast cancelado e ticks exatos do início/fim; sem hook homologado não alterar recarga com perk e não liquidar o mesmo recurso duas vezes.

🟡 Source-level causal; ⚠️ bytecode do JAR, config e QA modpack/Survival não certificados; ⛔ RPG perks/Mastery sem adapter homologado. Iron's e Apprentice's mantêm mana/casting/efeitos; Black Arcana não duplica runtime.
