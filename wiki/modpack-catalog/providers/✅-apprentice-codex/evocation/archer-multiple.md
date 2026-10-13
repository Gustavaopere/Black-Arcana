# Archer Multiple

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:archer_multiple`
- **Iron's school:** Evocation
- **Levels:** 1–5
- **Minimum rarity:** Rare
- **Cast type:** Long
- **Cooldown:** 30 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 200`
- `spellPowerPerLevel = 50`
- `baseManaCost = 70`
- `manaCostPerLevel = 30`
- `castTime = 30 ticks`
- summoned bows: **4** fixed
- duration: `600 ticks = 30 s`
- recast count: `2`
- bow damage: `spellPower / 100 * providerDamageMultiplier`
- optional pre-cast target helper range: `64 blocks`

## Provider lifecycle

The spell succeeds even when no priority target is resolved. On first cast the server creates four owner-linked bow entities, snapshots a priority target if one was selected, stores their UUIDs in serializable recast data and runs a 30-second provider session. Recast cleanup is provider-owned.

The guide describes the bows as following magical archers that attack the designated or nearby enemy.

## Causality and progression

Four bows do not represent four player casts. Their autonomous attacks belong to one provider summon lifecycle. RPG/Black Arcana must not award cast Mastery per bow spawn or per autonomous scan/shot without an explicit causal attribution contract.

## Deduplication

Occupies the **four autonomous owner-bound magical bows with optional priority target** niche.

## Confidence

`SOURCE-PINNED SPELL / EXACT COUNT+DURATION+DAMAGE+RECAST / BOW FIRE CADENCE+TARGET FALLBACK+MULTIPLAYER QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:archer_multiple` → `SpellRegistry.reg("archer_multiple", ArcherMultiple::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.archermultiple.ArcherMultiple`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/archermultiple/ArcherMultiple.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.
