# Ars Nouveau — Redstone Signal

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_redstone_signal`
- Display name: Redstone Signal
- School: Manipulation
- Default tier: 1
- Default mana cost: 0
- Compatible augments: Amplify, AOE, Dampen, Extend Time, Reduce Time (`glyph_duration_down`), Sensitive
- Source default signal baseline: 10 before Amplify/Dampen, clamped 1..15
- Source default duration: 5 ticks, minimum 2
- Source default duration bonus: 10 ticks per duration multiplier

## Provider-native behavior

Without Sensitive, the spell places a temporary Ars block that mimics a Redstone Block and stores configured power/duration. With Sensitive, it instead records the targeted existing block in `RedstoneSavedData` as a temporary power source and updates neighbors. Placement uses NeoForge entity-place protection events.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:manipulation_essence` + `#c:storage_blocks/redstone` ×3.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns this temporary redstone-power capability and persistence. Black Arcana must not create a second redstone state ledger or replay provider block updates. Independent Black Arcana world mutations still pass through `WorldEffectPolicy`.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectRedstone`).

## Engenharia para perks — caminho causal individual

- **Código exato:** [`EffectRedstone.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectRedstone.java), Ars 5.13.1.
- **Potência/duração:** `signalModifier=clamp((int)getAmpMultiplier()+10,1,15)` e `delay=max(GENERIC_INT.get()+(int)durationMultiplier*BONUS_TIME.get(),2)`; defaults base duration 5 **ticks**, Extend Time bonus 10 ticks. Mana default 0.
- **Sensitive path:** para cada posição AOE/Pierce válida, armazena `RedstoneSavedData.SIGNAL_MAP.put(pos,new Entry(pos,power,delay))`, chama `neighborChanged` e `updateNeighborsAt`; o path não cria um bloco adicional. **Ramo normal:** desloca candidato para a face hit, checa replaceable/bounds, publica `BlockEvent.EntityPlaceEvent` cancelável e coloca `TEMPORARY_BLOCK` com `POWER`, gravando `TemporaryTile.gameTime`, `tickDuration` e `mimicState=REDSTONE_BLOCK`.
- **Risco de proteção:** Sensitive path não publica `EntityPlaceEvent` nesta classe e não exibe claim check local. Isto exige testar `RedstoneSavedData`, carregamento de chunks e providers de proteção; não declarar bypass sem pipeline completo. Também não repetir sinais como procs de magia.
- **Estado:** ✅ assinatura/source; ⚠️ integração de plugins proteção, configs e gameplay pending; ⛔ nenhum adapter RPG testado nem permissão para duplicar a cadeia causal/perk/mastery.
