# Field Overseer

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:field_overseer`
- **Iron's school:** Lightning
- **Levels:** 1–5
- **Minimum rarity:** Uncommon
- **Cast type:** Long + recast lifecycle
- **Cooldown:** 30 s
- **Resource:** Iron's mana; summoned staff also carries provider-owned internal mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 1200`
- `spellPowerPerLevel = 200`
- `baseManaCost = 50`
- `manaCostPerLevel = 20`
- `castTime = 40 ticks`
- targeting/attack radius: **24 blocks**
- placement range: **12 blocks**
- recast count: **2**
- lifetime: **6000 ticks / 5 minutes**

Raw strike damage is `spellPower / 100`, then multiplied by `DamageMultiplierKey.FIELD_OVERSEER`.

Staff health by level:

`10 + (spellLevel - 1) * 5`

Mana cost per attack sequence:

`40 + (spellLevel - 1) * 20`

Initial/max internal staff mana:

`attackManaCost * 5`

## Placement and lifecycle

Initial placement is resolved server-side and rejects invalid placement or a nearby conflicting Field Overseer staff. Cast data binds the placement, spawned staff UUID and dimension to the provider recast lifecycle.

The staff is saved persistently while its bounded provider lifetime remains active; provider manager logic owns expiration, destruction and recast cleanup.

## Target selection and attack timing

Exact staff entity behavior:

- scans/selects every **40 ticks** while idle;
- requires line of sight and provider-valid hostile combat targets;
- sorts candidates by health descending;
- selects at most **3 targets**;
- consumes one configured attack-mana cost before starting the attack sequence;
- charge time: **10 ticks**;
- consecutive selected targets are struck every **3 ticks**;
- each strike affects valid targets within **1 block** of that selected impact point;
- provider damage uses no knockback.

The attack-mana cost is consumed for the selected attack sequence, not independently by Black Arcana for each child lightning strike.

## Owner-mana transfer

The internal staff pool is not a new global player resource. It is a bounded provider buffer that can be refilled directly from the **owner's Iron's mana**:

- transfer check every **5 ticks**;
- owner must be a ServerPlayer in the same level;
- owner must be within **8 blocks**;
- at most **20 mana** is transferred per check;
- transfer amount is capped by missing staff capacity and current player Iron's mana;
- player Iron's mana is reduced server-side and explicitly synced;
- staff internal mana increases by exactly that transferred amount.

This is a strict no-double-resource case. Black Arcana must never introduce another mana pool/payment for Field Overseer attacks or owner-to-staff recharge.

## What it does

Provider guide semantics: summons an autonomous staff that watches an area and attacks nearby enemies with Lightning magic, prioritizing higher-health targets. The staff has its own bounded mana storage and can replenish from the caster when the caster approaches.

## Acquisition

Registered through Iron's spell registry. Exact 0.9.7.1 scroll/loot availability remains in the provider-wide acquisition audit.

## Deduplication

Occupies the **placed autonomous Lightning turret / bounded internal mana / owner-mana recharge / multi-target strikes** niche. A Black Arcana familiar/ward should not reproduce this lifecycle without a materially different persistent contract.

## Confidence

`SOURCE-PINNED SPELL + STAFF ENTITY RESOURCE/LIFECYCLE / MANAGER EDGE CASES + PACK CONFIG MULTIPLIER QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:field_overseer` → `SpellRegistry.reg("field_overseer", FieldOverseer::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.fieldoverseer.FieldOverseer`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/fieldoverseer/FieldOverseer.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.
