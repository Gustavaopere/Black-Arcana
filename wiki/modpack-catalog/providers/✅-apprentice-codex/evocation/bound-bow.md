# Bound Bow

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:bound_bow`
- **Iron's school:** Evocation
- **Levels:** 1
- **Minimum rarity:** Rare
- **Cast type:** Long
- **Cooldown:** 30 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 50`
- `baseManaCost = 50`
- `manaCostPerLevel = 150`
- `castTime = 30 ticks`
- duration: `2400 ticks = 120 s`
- recast count: `2`
- Power-enchantment progression starts at **130 spell power**
- one additional Power level per **30 spell power** above that threshold
- resulting level is clamped by provider config `boundBowMaxPowerEnchantmentLevel()`
- arrow-forging mana cost is provider-configured through `boundBowForgeArrowManaCost()`
- summon-damage attribute is snapshotted into the provider activation path

## Provider lifecycle

The first cast activates a temporary provider-owned bound bow through `BoundBowManager`; a recast deactivates it. The manager receives spell level, Power enchantment level and current Iron's `SUMMON_DAMAGE` multiplier.

Greater Conjurer's Talisman can suppress the spell's cooldown on provider-defined deactivation/timeout paths. Black Arcana must not reproduce that cooldown mutation.

## Causality and progression

Activating the bow is one provider cast. Forged arrows and bow shots belong to the temporary equipment lifecycle and are not independent spell casts unless the provider exposes a distinct causal event.

## Deduplication

Occupies the **two-minute bound magical bow with spell-power-derived Power enchantment and mana-funded arrow forging** niche.

## Confidence

`SOURCE-PINNED SPELL / EXACT CONFIG+DURATION+RECAST+POWER THRESHOLDS / CONFIGURED ARROW COST+BOUND ITEM PROJECTILE DETAILS REQUIRE MANAGER/CONFIG QA`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:bound_bow` → `SpellRegistry.reg("bound_bow", BoundBow::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.boundbow.BoundBow`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/boundbow/BoundBow.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.
