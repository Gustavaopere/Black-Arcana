# Long Stride

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:long_stride`
- **Iron's school:** Ender
- **Levels:** 1
- **Minimum rarity:** Rare
- **Cast type:** Continuous
- **Cooldown:** 12 s
- **Resource:** Iron's mana
- **Crafting:** disabled
- **Looting:** disabled
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 0`
- `spellPowerPerLevel = 0`
- `baseManaCost = 12`
- `manaCostPerLevel = -1` (irrelevant to the one-level registry range)
- `castTime = 1200 ticks = 60 s`
- effective cast time deliberately ignores cast-time reduction
- provider mobility effect refresh: every `5 ticks`
- level-1 movement bonus displayed by this spell: `10%`

## Provider behavior

Long Stride continuously refreshes the provider's `LONG_STRIDE_MOBILITY` effect while channelled. The public guide associates it with the Explorer's Cane and describes faster travel, treating water/lava as traversable surfaces and stepping over moderate obstacles.

The exact movement/surface hooks live in the provider effect/event layer rather than the spell class; this sheet does not invent those internals beyond the source-backed guide behavior.

## Acquisition

The spell is item-only in source: crafting and looting are both disabled. Registered presence does not imply survival-scroll availability.

## Causality

Continuous effect refresh is provider maintenance for one sustained cast. It must not generate per-tick RPG Mastery or Black Arcana hazard/proc chains.

## Deduplication

Occupies the **item-bound sustained exploration mobility / terrain-traversal channel** niche.

## Confidence

`SOURCE-PINNED SPELL / EXACT CHANNEL+COST+EFFECT REFRESH / SURFACE-TRAVERSAL EVENT INTERNALS + ITEM ACQUISITION + RUNTIME QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:long_stride` → `SpellRegistry.reg("long_stride", LongStride::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.longstride.LongStride`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/longstride/LongStride.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.

## Engenharia causal aprofundada — ofensiva/movimento (2026-10-14)

**Source:** [`longstride/LongStride.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/longstride/LongStride.java) · [`longstride/LongStrideFluidMovement.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/longstride/LongStrideFluidMovement.java).

- **Efeito temporário:** `LongStride.onServerCastTick` reaplica `LONG_STRIDE_MOBILITY` com duração de **5 ticks**; `getEffectiveCastTime` não permite extensão por redução de tempo de cast.
- **Movimento em fluido:** `LongStrideFluidMovement.onPlayerTick` requer efeito ativo, exclui spectator, passageiro, voo e `fallFlying`. Em fluido sem colisão sólida aplica subida `+0.03/tick` limitada a `0.1`; próximo à superfície, `findFluidSupport` pode corrigir posição Y, zerar velocidade vertical e marcar `onGround`, usando limites de snap de `0.35` abaixo e `0.65` acima.
- **QA:** água/lava rasas, waterlogged, chunks, cliente/servidor, fim de cast/relogin; sem duplicar perk, mana ou controle de movimento.

🟡 Source-level causal; ⚠️ bytecode do JAR, config e QA modpack/Survival não certificados; ⛔ RPG perks/Mastery sem adapter homologado. Iron's e Apprentice's mantêm mana/casting/efeitos; Black Arcana não duplica runtime.
