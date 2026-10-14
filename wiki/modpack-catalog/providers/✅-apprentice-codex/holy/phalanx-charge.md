# Phalanx Charge

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:phalanx_charge`
- **Iron's school:** Holy
- **Levels:** 1–4
- **Minimum rarity:** Uncommon
- **Cast type:** Continuous
- **Cooldown:** 4 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 30`
- `baseManaCost = 15`
- `manaCostPerLevel = 5`
- `castTime = 200 ticks / 10 s`
- cast cannot be interrupted.

Raw thrust damage:

`3 + 6 * spellPower / 100`

then multiplied by `DamageMultiplierKey.PHALANX_CHARGE`.

Base thrust/beam length:

`6 + 1.5 * spellPower / 100` blocks.

## Guard state

The spell summons provider-owned spear/shield weaponry and continuously refreshes `Phalanx Stance` in 5-tick windows while channeling.

If **Protection Spell Supporter** is equipped:

- effective channel time is doubled;
- the provider chooses the movement-enabled Phalanx Stance amplifier instead of the fixed stance amplifier.

That accessory behavior is provider-owned and is not an RPG Skill Tree perk.

## Completion

On completion, the weapon begins its thrust sequence with current damage and beam length. The source performs the thrust even through the provider weapon entity rather than a second Black Arcana hit path.

Provider guide semantics: summon spear and shield, immediately assume a guarding stance, then thrust sharply forward when the stance ends.

## Deduplication

Occupies the **uninterruptible Holy guard-channel → forward thrust** niche. Black Arcana Order should not duplicate it with a differently named shield/spear stance.

## Confidence

`SOURCE-PINNED SPELL + GUARD STATE / WEAPON THRUST ENTITY + PACK CONFIG MULTIPLIER QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:phalanx_charge` → `SpellRegistry.reg("phalanx_charge", PhalanxCharge::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.phalanxcharge.PhalanxCharge`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/phalanxcharge/PhalanxCharge.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.
