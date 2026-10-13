# Manifestation Grimoire

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:manifestation_grimoire`
- **Iron's school:** Ender
- **Levels:** 1
- **Minimum rarity:** Legendary
- **Cast type:** Long
- **Cooldown:** 60 s
- **Resource:** Iron's mana
- **Crafting:** disabled by spell config
- **Looting:** explicitly disabled by spell implementation
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 0`
- `spellPowerPerLevel = 0`
- `baseManaCost = 100`
- `manaCostPerLevel = 0`
- `castTime = 50 ticks`

## Cast result

The provider creates an `ENDER_GRIMOIRE` item stack and spawns it as an item entity approximately `1.5` blocks forward from the caster eye direction.

At spawn the item entity:

- has gravity disabled;
- has zero velocity;
- cannot be picked up for `20 ticks`;
- receives provider particles.

The public guide describes the resulting grimoire as a linked manifestation whose stored spells are shared among manifested grimoires. The storage/link internals belong to the provider item system and are not inferred further here.

## Acquisition consequence

This spell is **not craftable and not lootable** through standard spell acquisition. That is stronger evidence than simply being registered. Black Arcana/RPG must not auto-inject it into generic scroll loot because the registry contains it.

## Causality

The spawned grimoire item is the result of one provider cast; item pickup/use is not a second Black Arcana cast/progression event by default.

## Deduplication

Occupies the **legendary item-only manifestation of a linked spell-storage grimoire** niche.

## Confidence

`SOURCE-PINNED SPELL / EXACT CAST+ACQUISITION EXCLUSIONS+ITEM SPAWN / GRIMOIRE SHARED-STORAGE INTERNALS + SURVIVAL REACHABILITY + RUNTIME QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:manifestation_grimoire` → `SpellRegistry.reg("manifestation_grimoire", ManifestationGrimoire::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.manifestationgrimoire.ManifestationGrimoire`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/manifestationgrimoire/ManifestationGrimoire.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.
