# Mystic Shield

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:mystic_shield`
- **Iron's school:** Holy
- **Levels:** 1–3
- **Minimum rarity:** Rare
- **Cast type:** Continuous
- **Cooldown:** 15 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 50`
- `spellPowerPerLevel = 25`
- `baseManaCost = 15`
- `manaCostPerLevel = 3`
- `castTime = 200 ticks / 10 s`

Counterattack multiplier:

`spellPower / 100 * DamageMultiplierKey.MYSTIC_SHIELD config multiplier`

If **Protection Spell Supporter** is equipped, the resulting reflect/counter multiplier is doubled.

## Defense lifecycle

On server cast start, `MysticShieldDefenseEvent.spawnShieldEntity(...)` creates the provider shield and resets its stored-damage state if spawning succeeds.

On cast completion/cancellation, `MysticShieldDefenseEvent.releaseStoredDamage(...)` owns release/cleanup and determines how accumulated attacks become the counterattack.

Provider guide semantics: deploy a magical barrier that blocks attacks from the front; when released, it fires a counterattack projectile based on attacks absorbed while active.

## Authority

The shield entity/event pair owns absorption, stored-damage bookkeeping and reflected projectile creation. Black Arcana must not maintain a second absorbed-damage ledger or emit a second counter projectile from the same blocked attack.

Protection Spell Supporter is a provider equipment modifier, not RPG Skill Tree authority.

## Deduplication

Direct overlap with Order/barrier/counter concepts. A BA barrier needs materially different law/seal/risk semantics rather than another frontal store-and-reflect shield.

## Confidence

`SOURCE-PINNED SPELL + DEFENSE EVENT ENTRY/EXIT / EXACT ABSORBABLE ATTACK SET + COUNTER PROJECTILE FORMULA QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:mystic_shield` → `SpellRegistry.reg("mystic_shield", MysticShield::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.mysticshield.MysticShield`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/mysticshield/MysticShield.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.
