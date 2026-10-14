# Linear Build

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:linear_build`
- **Iron's school:** Evocation
- **Levels:** 1
- **Minimum rarity:** Uncommon
- **Cast type:** Instant
- **Cooldown:** 0.5 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 0`
- `spellPowerPerLevel = 0`
- `baseManaCost = 20`
- `manaCostPerLevel = 0`
- `castTime = 0`
- base targeting range: **24 blocks**
- range with provider `Craftsman's Delight`: **32 blocks**
- additional placed-block mana cost comes from provider server config `linearBuildConfig().manaCostPerBlock()`
- that additional cost may be discounted by `CraftsmansDelight.applyManaCostDiscount(...)`

## Provider lifecycle

Pre-cast validates that the player is holding a usable block template and resolves a server-side block target before locking hit position/face into serializable cast data. The implementation contains explicit sourcing paths for player inventory and supported containers, plus optional Create toolbox and Malum pouch bridges.

This is provider-native construction logic, not a generic permission to mutate blocks. Item retrieval, mana settlement, placement eligibility and provider deny lists remain inside the spell's own transaction.

## Causality and progression

A single Linear Build cast may place more than one block while charging its provider-configured per-block cost. Those placements are consequences of one provider action and must not be replayed through Black Arcana `WorldEffectPolicy` as a second settlement layer after the provider has already accepted them.

Black Arcana-originated building/destructive spells still require Black Arcana's own world-safety policy; this provider behavior is not an exemption.

## Deduplication

Occupies the **inventory/container-backed linear construction spell with per-extra-block mana cost and optional Create/Malum storage sourcing** niche.

## Confidence

`SOURCE-PINNED SPELL / EXACT CONFIG+RANGES+TARGET LOCK+CONFIGURED PER-BLOCK COST+OPTIONAL STORAGE BRIDGES / FULL PLACEMENT SIZE+DENY-LIST+CONTAINER PRIORITY QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:linear_build` → `SpellRegistry.reg("linear_build", LinearBuild::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.linearbuild.LinearBuild`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/linearbuild/LinearBuild.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.
