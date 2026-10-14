# Apprentice's Codex 0.9.7.1 — engenharia causal: utilidades, persistência e recursos

**Checkpoint:** 2026-10-14 · Minecraft 1.21.1 / NeoForge / Java 21 · installed artifact segundo `Gustavaopere/neoforge-rpg-skilltree/main@63a41587ed91e6768a6b863e74dfaf44b9eb3a46`: `apprentice_codex-0.9.7.1+mc1.21.1.jar`, `apprenticecodex`, SHA-1 `b514315add32b93b0049c8673075627d7ef812e0` · source declarado 0.9.7.1 `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`.

✅ 83/83 magias já catalogadas no registry. 🟡 **64/83 com dossiês causais aprofundados** (54 integrados antes deste lote + **10 aqui**) e **19/83 pendentes**. **+0 magias semânticas**; **0 Java/runtime/adapters** neste lote.

| Spell ID | Ficha | Source class/método verificável | Contrato principal |
|---|---|---|---|
| `apprenticecodex:combustion_jet` | [combustion_jet](fire/combustion-jet.md) | `CombustionJetWaveEntity.tick/affectEntities` | collision, victimUuids, burning |
| `apprenticecodex:catch_flame` | [catch_flame](fire/catch-flame.md) | `CatchFlame.affectEntities/tryIgniteBlock` | ignition ownership, claims, VFX entity |
| `apprenticecodex:wizardlamp` | [wizardlamp](holy/wizardlamp.md) | `Wizardlamp.checkPreCastConditions/onCast` | waterlogged block placement, BE without ticker |
| `apprenticecodex:grind_runner` | [grind_runner](nature/grind-runner.md) | `GrindRunnerWheelEntity.tickOnServer/processNearbyItems` | item economy, recipe Create compat |
| `apprenticecodex:spectral_wing` | [spectral_wing](eldritch/spectral-wing.md) | `SpectralWingFlightEvent.onPlayerTick/deactivate` | flight state with environment gates |
| `apprenticecodex:mana_transcription` | [mana_transcription](eldritch/mana-transcription.md) | `ManaTranscription.onServerCastTick/onCast` | XP/item operation, hand lock |
| `apprenticecodex:servant_gaze` | [servant_gaze](ender/servant-gaze.md) | `ServantGazeStaffEntity.selectTargets/firePendingShot` | owner mana per shot, unsaved staff |
| `apprenticecodex:compound_phial` | [compound_phial](nature/compound-phial.md) | `CompoundPhialProjectileEntity.onImpact` | splash multipart/dedup |
| `apprenticecodex:extract` | [extract](nature/extract.md) | `Extract.onCast/consumeResolvedDose` | consume dose only on accepted spawn |
| `apprenticecodex:terra_resonance` | [terra_resonance](nature/terra-resonance.md) | `TerraResonanceJobManager.processSearches` | budget 40000/level tick, slices 4000 |

## Análise de contratos e QA

- **Recurso/ownership:** Servant Gaze retira mana do owner para targets selecionados e não salva a staff em restart (`shouldBeSaved=false`). Mana Transcription debita XP antes de modificar item, exigindo QA de crash/atomicidade de custo especial. Extract consome dose apenas após `addFreshEntity` aceito. Nenhum desses gastos é mana adicional do Black Arcana.
- **Efeito contínuo:** Grind Runner possui gasto/produção de itens com orçamento por entidade, inclusive Create opcional (com reflection para resultados de receita); múltiplos wheels não provam cap global. Terra Resonance usa `SEARCH_BLOCK_BUDGET_PER_TICK=40_000` por ServerLevel e `SEARCH_JOB_SLICE=4_000` por trabalho na rotação; pulsos de pre-cast/cast são UX, não cast duplicado.
- **Persistência/limpeza:** Wizardlamp coloca BlockEntity sem ticker próprio; CatchFlameImpactEntity é VFX ephemeral (`shouldBeSaved=false`); Combustion Jet deduplica vítimas por UUID na wave; Spectral Wing mantém estado de flight e restaura na desativação. Diferenciar objetos persistentes de estado de memória e da observação do mundo real.
- **Dano e proteção:** Compound Phial resolve targets multipart e deduplica splash; Catch Flame verifica caminhos de ignição player/modpack e invoca flint-and-steel usual após gates; o source não certifica cobertura de cada mod de claims/PvP nem substitui testes físicos.
- **Authority:** Iron's controla school/mana/casting; Apprentice's mantém execução, efeitos e recursos específicos. BA governa apenas próprio runtime, sem usar os helpers do provider para burlar WorldEffectPolicy; RPG Skill Tree só por adapter/receipt real.
- **⚠️ QA pendente:** bytecode do JAR instalado, config efetiva, ciclos de chunk e restart, NPC/automation, resource dupes, mala interação com inventários, claims/PvP, interface Create, speed e concorrência em dedicated/Survival.
- **⛔ Sem hook Mastery/perks real homologado.** Fail-closed: nenhuma segunda liquidação de cast, mana, dano, drop, XP, item, progresso ou efeito do provider. Stage 06.05 permanece sem promoção.

[Registry 83/83](README.md) · [High-risk](PERK-ENGINEERING-MATRIX-HIGH-RISK-0.9.7.1.md) · [Lifecycle](PERK-ENGINEERING-MATRIX-LIFECYCLE-0.9.7.1.md) · [Persistent](PERK-ENGINEERING-MATRIX-PERSISTENT-0.9.7.1.md) · [World](PERK-ENGINEERING-MATRIX-WORLD-COMBAT-0.9.7.1.md) · [Weapons](PERK-ENGINEERING-MATRIX-SUMMONED-WEAPONS-0.9.7.1.md).
