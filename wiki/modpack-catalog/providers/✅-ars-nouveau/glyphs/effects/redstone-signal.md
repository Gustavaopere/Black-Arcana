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

## Certificação técnica estática — Redstone Signal (25/10/2026)

**✅ `STATIC_TECHNICAL_CATALOG_ONLY` · ⛔ `mutating_hook=NOT_VERIFIED` · ⚠️ `physical_qa=NOT_TESTED`.** Registry `ars_nouveau:glyph_redstone_signal` ↔ `EffectRedstone` provado na auditoria binária de ID/classe do JAR 5.13.1 SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd` (não prova de igualdade de métodos). Fontes `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`: [EffectRedstone.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectRedstone.java), [RedstoneSavedData.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/world/saved_data/RedstoneSavedData.java), [TemporaryTile.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/block/tile/TemporaryTile.java).

| Eixo de perk | Contrato e perigos verificáveis do source |
|---|---|
| Parâmetros | `signalModifier=Mth.clamp((int)getAmpMultiplier()+10,1,15)`; `timeBonus=(int)getDurationMultiplier()`; `delay=Math.max(GENERIC_INT.get()+timeBonus*BONUS_TIME.get(),2)`. Defaults: `GENERIC_INT=5` ticks, `BONUS_TIME=10` ticks, `getDefaultManaCost()=0` (não equivale a cast grátis). `SpellUtil.calcAOEBlocks` seleciona candidatos; o cast para `ServerLevel` ocorre antes dos ramos. |
| Sensitive → injeção no estado do bloco existente | Se `spellStats.isSensitive()`, primeiro checa `world.isInWorldBounds(pos1)`; **se falhar, `return` encerra todo o método**, não apenas o candidato. Depois `RedstoneSavedData.from((ServerLevel)world).SIGNAL_MAP.put(pos1.immutable(),new Entry(pos1,signalModifier,delay))`, `neighborChanged`, `updateNeighborsAt`. **Não** cria `TEMPORARY_BLOCK`, não publica `BlockEvent.EntityPlaceEvent` e **não chama `destroyRespectsClaim` nesse ramo**. Portanto a classificação “redstone injetado” não equivale a placement sob o mesmo preflight. |
| Padrão → bloco temporário | Quando `!Sensitive`, desloca `pos1.relative(hitDirection)`, checa bounds (também com **`return` global**), `canBeReplaced` e `NeoForge.EVENT_BUS.post(new BlockEvent.EntityPlaceEvent(...,fakePlayer))`; evento cancelado faz `continue`. Chama `world.setBlockAndUpdate` com `TemporaryBlock.POWER` **sem conferir retorno**; se encontra `TemporaryTile`, define `tile.gameTime=world.getGameTime()`, `tile.tickDuration=delay`, `tile.mimicState=Blocks.REDSTONE_BLOCK`, `tile.updateBlock()`; `sendBlockUpdated` sempre chamado após tentativa. |
| SavedData e tick/unload | `RedstoneSavedData.from` usa `computeIfAbsent(factory(),"an_redstone_signals")`. `SIGNAL_MAP` serializa `SignalList` com `x/y/z/power/ticks`; `isDirty()` retorna true. `LevelTickEvent.Post` servidor itera `SIGNAL_MAP`: se `!serverLevel.isLoaded(pos)`, **não decrementa os ticks**; senão executa `if(signal.ticks--<=0)` para remover e notificar vizinhos. `SIGNAL_MAP.put` na mesma posição sobrescreve entrada anterior; não há fila histórica de sinais por posição. |
| TemporaryTile lifecycle | `TemporaryTile.tick` guarda `gameTime` e `tickDuration` em NBT; expira quando `level.getGameTime()>=gameTime+tickDuration`, tentando `level.setBlock(pos,AIR,2)` seguido de neighbor updates. É **tempo absoluto de game ticks** do nível, diferentemente de um contador que pausa quando unloaded. Não trocar as duas semânticas em perk de duração e não presumir rollback de bloco original. |
| Integração/proteções | `WorldEffectPolicy` cobre efeitos próprios BA, não intercepta `RedstoneSavedData` do Ars. O provider é dono do sinal, NBT, vizinhos e custos; RPG Skill Tree só fornece perks/gates por hook verificado, sem segunda `SIGNAL_MAP`, double-notify nem cap arbitrário. Exige QA de claims/protection no ramo Sensitive antes de integração mutadora. |

**QA física necessária:** claim do bloco Sensitive, posição fora dos bounds e efeito do `return`, chunks unloaded e reloaded, servidor reiniciado com sinal ativo, delay negativo/config, reacender same-pos, tile ausente, callbacks de redstone modded, TPS/loops e multiplayer. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`. Stage 06.05/09 não promovido.
