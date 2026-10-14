# Tiny Lumberjack

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:tiny_lumberjack`
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
- `castTime = 400 ticks / 20 s`
- block/log target range: **8 blocks**
- combat-entity target range: **3 blocks**
- entity raycast width: **0.5**
- summoned saw reach-speed setting: **10**

Raw combat damage is `spellPower / 100`, then multiplied by `DamageMultiplierKey.TINY_LUMBERJACK`.

Base block break-speed input:

`2 + 1.5 * spellPower / 100`

If provider **Craftsman's Delight** break-speed bonuses are enabled, it modifies that speed. The spell can also build a dummy Iron Axe carrying eligible main-hand enchantments through that provider accessory path.

Displayed best-case log break time is:

`round(60 / breakSpeed)` ticks.

## Targeting and world interaction

During channeling the summoned saw prefers a still-valid locked combat target. Otherwise it checks for a nearby valid living target, then a log block target through the provider's log classifier/raycast/outlined-target path.

The saw entity owns the actual tree/block-break workflow and its protection/drop semantics. The spell itself does not directly replace blocks.

Provider guide semantics: shred the entity in line of sight or aim the saw at a tree to fell/process it.

## Authority

This is a provider-native magical tool. Black Arcana must not replay block breaks, drops or durability/enchantment effects after the saw has already processed them. Any Black Arcana-originated destructive magic still needs Black Arcana `WorldEffectPolicy`.

## Deduplication

Occupies the **continuous magical saw / log-felling + close combat** niche.

## Confidence

`SOURCE-PINNED SPELL TARGETING + BREAK-SPEED INPUT / SAW BLOCK-JOB + PROTECTION/DROP QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:tiny_lumberjack` → `SpellRegistry.reg("tiny_lumberjack", TinyLumberjack::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.tinylumberjack.TinyLumberjack`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/tinylumberjack/TinyLumberjack.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.
