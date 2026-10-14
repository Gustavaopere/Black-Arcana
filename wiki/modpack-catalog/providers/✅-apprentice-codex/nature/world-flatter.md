# World Flatter

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:world_flatter`
- **School:** Nature
- **Levels:** 1–3
- **Minimum rarity:** Rare
- **Cast type:** Continuous
- **Cooldown:** 20 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 50`
- `baseManaCost = 10`
- `manaCostPerLevel = 5`
- `castTime = 200 ticks / 10 s`
- block target range: **8 blocks**

Raw combat damage:

`3 + 2 * spellPower / 100`

then multiplied by `DamageMultiplierKey.WORLD_FLATTER`.

Entity reach:

`8 + 4 * spellPower / 100` blocks.

Armor-penetration/reduction tier:

- amplifier = `min(3, max(0, floor(spellPower / 200)))`;
- displayed armor-reduction percent = `(amplifier + 1) * 20`, bounded by implementation to 20–80% across amplifier values.

Base break speed:

`4 * spellPower / 100`

with optional provider Craftsman's Delight break-speed bonus.

## Tool semantics

Without Craftsman's Delight, the provider uses an **Iron Pickaxe / Iron tier** as the dummy tool/harvest baseline. With the accessory equipped it upgrades that baseline to **Netherite Pickaxe / Netherite tier** and may copy eligible main-hand enchantments.

The spell targets a valid living entity first; otherwise it resolves a provider-approved breakable block through outlined/raycast target paths. `WorldFlatterDrillEntity.canBreakTarget(...)` owns the block eligibility check.

## What it does

Provider guide semantics: summons a magical drill that pierces enemies through armor and, when aimed into the ground, excavates a large hole.

## World safety

The drill entity is authoritative for actual break scheduling/protection/drop behavior. Black Arcana must not replay or widen those breaks. Black Arcana-originated excavation remains subject to `WorldEffectPolicy`.

## Deduplication

Occupies the **armor-penetrating magical drill + terrain excavation** niche.

## Confidence

`SOURCE-PINNED SPELL + TOOL/TIER INPUT / DRILL BREAK JOB + PROTECTION/DROP QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:world_flatter` → `SpellRegistry.reg("world_flatter", WorldFlatter::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.worldflatter.WorldFlatter`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/worldflatter/WorldFlatter.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.
