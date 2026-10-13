# Personal Shelf

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:personal_shelf`
- **Iron's school:** Ender
- **Levels:** 1
- **Minimum rarity:** Rare
- **Cast type:** Long
- **Cooldown:** 5 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 0`
- `spellPowerPerLevel = 0`
- `baseManaCost = 50`
- `manaCostPerLevel = 0`
- `castTime = 20 ticks`
- targeting/placement range: `8 blocks`

## Server-authoritative placement

The client can provide targeting/preview intent, but the provider validates the target again on the server before casting. The server rejects non-placeable locations and creates `PERSONAL_SHELF_CHEST` only after validation.

Sneaking at cast time records an **export mode** plus placement facing in serialized cast data. The created block entity is initialized with the caster/player identity and the provider's shelf/export state.

This is a concrete example of provider-owned client-preview/server-settlement separation; Black Arcana must not add a second placement transaction.

## What it does

The guide describes a temporary personal/private storage interface and a sneaking transfer/export mode toward a container. The exact inventory persistence/storage backing remains provider implementation authority.

## World-effect boundary

Personal Shelf changes the world by creating a provider block. That mutation is already settled by Apprentice's Codex. It is not retroactively re-run through Black Arcana `WorldEffectPolicy`.

A Black Arcana-originated analogous world effect would still require Black Arcana policy and a real semantic gap.

## Acquisition

Registered through Iron's spell registry. Exact survival acquisition remains provider-wide audit work.

## Deduplication

Occupies the **temporary personal magical storage/block interface with export mode** niche.

## Confidence

`SOURCE-PINNED SPELL / EXACT COST+RANGE+SERVER TARGET VALIDATION / STORAGE LIFETIME+INVENTORY BACKING+PACK RUNTIME QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:personal_shelf` → `SpellRegistry.reg("personal_shelf", PersonalShelf::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.personalshelf.PersonalShelf`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/personalshelf/PersonalShelf.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.
