# Treasure Divination

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:treasure_divination`
- **School:** Nature
- **Levels:** 1–3
- **Minimum rarity:** Epic
- **Cast type:** Continuous
- **Cooldown:** 30 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 400`
- `spellPowerPerLevel = 400`
- `baseManaCost = 20`
- `manaCostPerLevel = 0`
- `castTime = 600 ticks / 30 s`
- scan interval constant: **20 ticks**
- maximum search range: **32 blocks**
- maximum detectable target count before overload: **64**

Search range:

`max(0, min(32, floor(spellPower / 100)))`

## Bounded server scan

Only a `ServerPlayer` performs the scan. At each scan interval the provider:

1. computes the bounded cube around the player;
2. iterates only chunk coordinates intersecting that cube;
3. calls `getChunkNow(...)`, therefore **never synchronously loading an unloaded chunk**;
4. skips empty chunk sections;
5. checks only blocks tagged `TREASURE_DIVINATION_TARGETS`;
6. asks the Lootr compatibility bridge whether an already-opened target should be ignored;
7. counts detectable targets and aborts immediately if the count exceeds 64;
8. keeps the nearest result using **Manhattan distance**.

If overload/noise is detected, the spell tells the player the area is too noisy and cancels the channel.

### Source-comment discrepancy

The executable constant is `SEARCH_INTERVAL_TICKS = 20`, i.e. one second at 20 TPS. An inline developer comment later says the loaded area is scanned "every 2 seconds". The catalog treats the executable 20-tick constant as source behavior and records the comment mismatch for runtime QA instead of silently reconciling it.

## What it does

Provider guide semantics: focus mana to learn how far away the nearest valuable-looking target is. The spell intentionally does not promise that every detected object is actually valuable, and its detectable target set is provider/tag controlled.

## Performance/authority

This is a useful positive reference for Black Arcana Divination: bounded range, loaded-chunk-only access, periodic—not per-tick—scanning and an overload ceiling. Black Arcana must not launch a second treasure scan after observing this provider cast.

## Deduplication

Direct Divination overlap. One scan result/message is part of one continuous provider cast, not a separate magical action per found block.

## Confidence

`SOURCE-PINNED SCAN LOOP / TAG CONTENT + LOOTR EXACT PACK BEHAVIOR + 20-TICK VS COMMENT RUNTIME QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:treasure_divination` → `SpellRegistry.reg("treasure_divination", TreasureDivination::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.treasuredivination.TreasureDivination`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/treasuredivination/TreasureDivination.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.

## Engenharia causal aprofundada — fechamento das nove fichas (2026-10-14)

**Source:** [`treasuredivination/TreasureDivination.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/treasuredivination/TreasureDivination.java) · [`treasuredivination/TreasureDivination.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/treasuredivination/TreasureDivination.java).

- **Busca bounded, mas não gratuita:** `TreasureDivination.onServerCastTick` só varre para `ServerPlayer`, em intervalos de **20 ticks de cast**; o scanner `scanNearestTreasure` examina chunks já carregados com `getChunkNow`, pula seções vazias e inspeciona blocos em volume limitado ao range, máximo **32**. O limite **64** aplica-se a **alvos correspondentes detectados**, não ao total de blocos visitados; ao 65º retorna `ScanResult.overloaded` e `MagicTools.cancelCasting(...,true)`.
- **Contratos de resultado:** `isTarget` usa tag `TREASURE_DIVINATION_TARGETS` e filtro opcional `LootrTreasureDivinationCompatBridge.shouldIgnoreOpenedTarget`; `sendScanMessage` mostra distância **Manhattan** da posição mais próxima em action bar, sem coordenada. `CASTING_MOBILITY` é renovado por **5 ticks** durante o cast.
- **QA:** custo de scan em região com poucos tesouros, chunks após unload, filtro Lootr, 64/65 hits e cancelamento, cadência no tick sob TPS real; não considerar descoberta de loot como pagamento progressivo automático.

🟡 Dossiê causal source-level; ⚠️ equivalência bytecode/JAR/config, PvP/claims e QA Survival/dedicated pendentes; ⛔ sem adapter Mastery/perks real. Black Arcana não apropria casts, mana ou efeitos do provider.
