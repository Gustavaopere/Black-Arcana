# Tiro Volley

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:tiro_volley`
- **Iron's school:** Evocation
- **Levels:** 1–3
- **Minimum rarity:** Rare
- **Cast type:** Continuous
- **Cooldown:** 20 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 100`
- `baseManaCost = 13`
- `manaCostPerLevel = 3`
- `castTime = 200 ticks`
- damage per musket shot: `(4 + spellPower / 1000) * providerDamageMultiplier`
- musket spawn rate: `clamp(2 + (spellPower - 100) * 6 / 400, 1, 10)` muskets/s
- look-target chance: **2/3**
- look-target range: **32 blocks**
- nearest-target fallback range: **12 blocks**
- random-target range: **32 blocks**
- maximum due spawns processed in one cast callback: **32**

The source schedules ideal musket spawn times against integer server ticks so average rate remains stable instead of assuming fractional ticks.

## Provider lifecycle

The server initializes serializable cast timing state once and then spawns only the muskets whose scheduled times are due. Target selection and musket entities remain provider-owned. The bounded `MAX_SPAWNS_PER_CAST_CALL = 32` prevents a lag spike from producing an unbounded catch-up burst in one callback.

## Causality and progression

Every spawned musket belongs to one continuous provider cast. Neither catch-up spawning nor multiple autonomous shots may be treated as independent Black Arcana casts or Mastery grants.

## Deduplication

Occupies the **continuous spell-power-scaled volley of independently spawned magical muskets with bounded catch-up scheduling** niche.

## Confidence

`SOURCE-PINNED SPELL / EXACT CONFIG+DAMAGE+SPAWN RATE+TARGETING BOUNDS+PER-CALL CAP / MUSKET ENTITY HIT SEMANTICS QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:tiro_volley` → `SpellRegistry.reg("tiro_volley", TiroVolley::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.tirovolley.TiroVolley`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/tirovolley/TiroVolley.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.
