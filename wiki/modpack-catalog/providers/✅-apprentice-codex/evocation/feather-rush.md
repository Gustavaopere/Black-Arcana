# Feather Rush

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:feather_rush`
- **School:** Evocation
- **Levels:** 1–5
- **Minimum rarity:** Epic
- **Cast type:** Continuous
- **Cooldown:** 12 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 75`
- `baseManaCost = 4`
- `manaCostPerLevel = 2`
- `castTime = 100 ticks / 5 s`

Damage per feather:

`(1 + 2.5 * spellPower / 100) * FEATHER_RUSH damage multiplier`

The provider derives a target fire rate from spell power, linearly mapping 100 spell power to 300 RPM and 400 spell power to 900 RPM. It then chooses an integer burst interval/projectile count combination with a minimum **2-tick interval** and **2 projectiles per burst** that best approximates that rate.

## Channel and projectile lifecycle

The cast summons a provider-owned wing entity and records an active Feather Rush state on the caster. While channeling, bursts alternate left/right wing emission.

Each feather projectile:

- has a maximum lifetime of **100 ticks / 5 s**;
- initially travels backward for **10 ticks plus 1–3 additional delay ticks** at speed `0.05`;
- then locks its forward direction from the owner's current look and travels at speed `1.75`;
- performs server-side collision/damage resolution;
- discards on a valid entity hit or block hit.

The cast clears the provider active state and releases the wing when the channel ends.

## Causality / deduplication

A single Feather Rush channel can create many child projectiles. Those projectiles are downstream effects of one provider cast, not independent casts or independent Mastery triggers.

Black Arcana must not duplicate the volley, re-settle feather damage, or treat the provider's temporary movement/gravity state as Black Arcana-owned mobility state.

## Confidence

`SOURCE-PINNED CAST + BURST RATE + PROJECTILE LIFECYCLE / FULL MODPACK RUNTIME QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:feather_rush` → `SpellRegistry.reg("feather_rush", FeatherRush::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.featherrush.FeatherRush`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/featherrush/FeatherRush.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.
