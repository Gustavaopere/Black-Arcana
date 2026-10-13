# Frost Rune

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:frost_rune`
- **Iron's school:** Ice
- **Levels:** 1–5
- **Minimum rarity:** Uncommon
- **Cast type:** Long
- **Cooldown:** 8 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 1200`
- `spellPowerPerLevel = 200`
- `baseManaCost = 50`
- `manaCostPerLevel = 10`
- `castTime = 20 ticks`

Effective spell power/mana by level remains settled by Iron's `AbstractSpell` semantics; this catalog preserves the provider coefficients rather than duplicating the upstream formula.

## Placement and lifetime

The spell performs placement validation before casting and stores the chosen block position/support orientation as cast data. Server-side placement is validated again before the rune block is created.

Source formulas:

- raw blast damage: `spellPower / 100`, then multiplied by `DamageMultiplierKey.FROST_RUNE`;
- rune lifetime: `round(20 * spellPower / 2)` ticks;
- placement range: `4 + spellPower / 150` blocks.

The exact runtime multiplier from the user's server config remains runtime/config QA.

## Trap lifecycle

The exact trap block entity establishes:

- arm delay: **60 ticks**;
- detonation animation/removal delay: **20 ticks**;
- trigger detection tangent half-extent: **1.5 blocks**;
- trigger detection normal extent: **2 blocks**;
- blast half-extent: **2.5 blocks** (a 5×5×5 AABB around the rune center);
- movement-slow duration: **40 ticks**;
- Slowness amplifier: **4**;
- `frost_trapped` duration: **100 ticks**.

After arming, owner is excluded from triggering. Valid combat targets can trigger the rune; item entities and projectiles can also trigger it. The blast itself damages only provider-valid combat targets and applies the Ice-school damage source without knockback.

If the block is removed before it naturally expires, its block entity owns the removal/detonation behavior. Black Arcana must not add a second detonation or second damage settlement for the same rune removal.

## What it does

Provider guide semantics: carve a frost rune into terrain; after arming, contact by something other than the caster can detonate it and attack targets in range. The rune is intentionally difficult to see but remains detectable by the provider's documented Jade-facing interaction.

## Acquisition

Registered as an Iron's spell. Exact 0.9.7.1 scroll/loot/recipe availability is tracked in the provider-wide acquisition audit rather than inferred here.

## Deduplication

This occupies the **server-validated terrain rune / proximity trap / cold burst / slow** niche. Black Arcana should not create an equivalent Ice rune merely with different VFX. A Black Arcana ritual/rune must differ materially in authority, persistence, trigger contract or magical domain.

## Confidence

`SOURCE-PINNED SPELL + TRAP BLOCK ENTITY / PACK CONFIG MULTIPLIER + FULL RUNTIME QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:frost_rune` → `SpellRegistry.reg("frost_rune", FrostRune::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.frostrune.FrostRune`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/frostrune/FrostRune.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.
