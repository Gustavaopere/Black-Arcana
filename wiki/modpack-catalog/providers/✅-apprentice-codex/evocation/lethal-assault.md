# Lethal Assault

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:lethal_assault`
- **Iron's school:** Evocation
- **Levels:** 1–5
- **Minimum rarity:** Uncommon
- **Cast type:** Instant
- **Cooldown:** 1.5 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 500`
- `spellPowerPerLevel = 200`
- `baseManaCost = 20`
- `manaCostPerLevel = 5`
- `castTime = 0`
- burst size: **3**
- range: **48 blocks**
- damage per burst projectile: `(spellPower / 300) * providerDamageMultiplier`

The source explicitly divides the spell-power contribution by three because the summoned rifle fires a three-shot burst.

## Provider lifecycle

An instant cast creates/reuses a summoned rifle entity through `AbstractSummonWeaponSpell`. At initial cast completion the provider snapshots the current damage into the rifle and starts the three-round firing sequence. Weapon presentation and burst execution remain provider-owned.

`IMagiAgentSuitAffectedSpell` means provider equipment may change interruption semantics; that compatibility is not reproduced by Black Arcana.

## Causality and progression

The three shots are one spell cast and one summoned-weapon burst. Do not award spell Mastery three times merely because the provider emits three attack resolutions.

## Deduplication

Occupies the **instant summoned 48-block three-round magical rifle burst** niche.

## Confidence

`SOURCE-PINNED SPELL / EXACT CONFIG+3-SHOT COUNT+RANGE+DAMAGE / RIFLE SHOT TIMING+COLLISION+MAGI AGENT SUIT DETAILS QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:lethal_assault` → `SpellRegistry.reg("lethal_assault", LethalAssault::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.lethalassault.LethalAssault`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/lethalassault/LethalAssault.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.
