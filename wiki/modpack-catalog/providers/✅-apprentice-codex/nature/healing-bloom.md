# Healing Bloom

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:healing_bloom`
- **School:** Nature
- **Levels:** 1–3
- **Minimum rarity:** Rare
- **Cast type:** Long
- **Cooldown:** 300 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 100`
- `baseManaCost = 100`
- `manaCostPerLevel = 20`
- `castTime = 50 ticks`
- placement/targeting range: **8 blocks**

Bloom max health:

`round(20 * spellPower / 100)`

Effect range:

`min(16, round(4 * spellPower / 100))` blocks.

Fruit maturation interval:

`max(600, round(1200 * (4 - spellPower / 100)))` ticks.

This preserves the exact source arithmetic: the floor is 600 ticks / 30 s.

## One-bloom-per-caster lifecycle

Server placement is resolved through `HealingBloomPlacementHelper` and rejected if invalid.

For ServerPlayers, `HealingBloomManager` enforces one managed bloom:

- if one already exists, ordinary casting is rejected;
- sneaking marks the cast as an explicit **force replace** operation;
- the force-replace flag and validated position are stored in cast data;
- successful spawn registers the new bloom through the provider manager, which owns replacement/lifecycle cleanup.

## Spawned bloom state

The entity is seeded with:

- owner;
- anchor block position;
- effect range;
- calculated maximum health;
- calculated Comfort Berry growth interval.

Provider guide semantics: the bloom softly lights its surroundings, heals nearby entities and produces Comfort Berries over time.

## Authority

The provider manager owns the single-instance invariant and replacement. Black Arcana must not create a parallel bloom registry or issue duplicate cleanup when the same provider entity is replaced/destroyed.

## Deduplication

Occupies the **one-per-caster placed healing/light/fruit-producing plant** niche.

## Confidence

`SOURCE-PINNED SPELL + PLACEMENT/MANAGER ENTRYPOINTS / BLOOM ENTITY HEAL-FRUIT CADENCE + PERSISTENCE RUNTIME QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:healing_bloom` → `SpellRegistry.reg("healing_bloom", HealingBloom::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.healingbloom.HealingBloom`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/healingbloom/HealingBloom.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.
