# Apprentice's Codex 0.9.7.1 — fechamento da engenharia causal de 83 magias

**Checkpoint:** 2026-10-14 · Minecraft 1.21.1 / NeoForge / Java 21 · sibling modlist `Gustavaopere/neoforge-rpg-skilltree/main@63a41587ed91e6768a6b863e74dfaf44b9eb3a46` · `apprentice_codex-0.9.7.1+mc1.21.1.jar`, mod ID `apprenticecodex`, SHA-1 `b514315add32b93b0049c8673075627d7ef812e0` · source `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`.

✅ **83/83** identidades previamente source-catalogadas. 🟡 **83/83** fichas com dossiês causais source-level aprofundados (74 na branch dependente #804 +9 finais). Restam **0** na lacuna específica de engenharia **documental**; isto **não** equivale a QA físico, equivalência binária de métodos, adapter homologado ou sistema de perks implementado. **+0** novas raízes semânticas, **0 Java/runtime/adapters**.

| Spell ID | Ficha | Entrada source-auditada | Causalidade / QA condicionado |
|---|---|---|---|
| `apprenticecodex:illuminate_stellar` | [illuminate_stellar](holy/illuminate-stellar.md) | `IlluminateStellarStarEntity.tickServer/updateLaunchDirection` | 3–4 estrelas; DRIFT→WAIT→LAUNCH, TargetEntityId NBT |
| `apprenticecodex:unite_luna` | [unite_luna](holy/unite-luna.md) | `UniteLunaMoonEntity.onAntiMagic/explodeByAntiMagic` | Counterspell → explosão ampliada e 3× dano no source |
| `apprenticecodex:mana_mending` | [mana_mending](holy/mana-mending.md) | `ManaMending.mendTarget/ManaMendingCastData.matchesTarget` | lock ItemStack por identidade, saldo fracionário |
| `apprenticecodex:sky_edge` | [sky_edge](lightning/sky-edge.md) | `SkyEdge.onCast/SkyEdgeProjectileEntity.tick` | count power-gated, standby e impactos cancelados |
| `apprenticecodex:quick_arms` | [quick_arms](lightning/quick-arms.md) | `QuickArms.onCastWithWeapon/QuickArmsHandgunEntity.tickOnServer` | recast da arma, primeira shot adiada |
| `apprenticecodex:shock` | [shock](lightning/shock.md) | `Shock.onCast/ShockBoltEntity.tick` | dano instantâneo host + raio visual sem segundo hit |
| `apprenticecodex:treasure_divination` | [treasure_divination](nature/treasure-divination.md) | `TreasureDivination.scanNearestTreasure/shouldScanThisTick` | chunks carregados; 64 targets antes de cancelar |
| `apprenticecodex:palette_shift` | [palette_shift](eldritch/palette-shift.md) | `PaletteShiftReceptionEvent.onSpellPreCast` | PastelStaff recebe afinidade e cancela próximo cast |
| `apprenticecodex:deep_sensor` | [deep_sensor](eldritch/deep-sensor.md) | `SenseSensorVibrationEvent.onVanillaGameEvent/DeepSensorObservationBuffer.record` | silêncio seletivo; 64 retidas, 8 exibidas |

## Achados e bloqueios

- **Unite Luna:** ao contrário de uma neutralização esperada, `UniteLunaMoonEntity.onAntiMagic` chama `explodeByAntiMagic`, que usa `COUNTERSPELL_DAMAGE_MULTIPLIER=3.0`. Isto é comportamento **do código-fonte declarado**, não reprodução contra o JAR instalado; testar antimagia/PvP antes de atribuir segurança à integração.
- **Palette Shift:** `SpellPreCastEvent` sob `EventPriority.HIGHEST` altera cor/escola da Pastel Staff, consome o efeito `PALETTE_RECEPTION` e **cancela** o próximo cast caso a transferência tenha ocorrido. Nem toda tentativa de cast interrompida é uma magia efetivamente executada; perks precisam distinguir pré-cast cancelado de execução.
- **Mana Mending:** `ManaMendingCastData` referencia o `ItemStack` transientemente com `==`; não salva o ponteiro no NBT. Validar hand swaps, relog, retomada, lock de reparo e saldo fracionário de durabilidade.
- **Recursos e limites:** `TreasureDivination` corta após o 65º bloco-alvo detectado, mas percorre volume para achá-los. `DeepSensorObservationBuffer` mantém 64 registros / 8 exibidos. `IlluminateStellarStarEntity` guarda ID numérico de alvo em NBT; QA necessário em restart para interpretação dos IDs.
- **Autoridade/clean-room:** Iron's Spellbooks determina casts/escola/mana. Apprentice's Codex é dono dos projéteis, efeitos, atributos adicionais e transações de repair/equipamentos. Black Arcana mantém apenas próprio runtime; o RPG Skill Tree continua sibling e apenas progressão via **contrato real futuro**. Não efetuar segunda liquidação por recast, dano, summon, trajetória ou item.
- **⚠️ Critérios não satisfeitos:** bytecode dos métodos do JAR instalado, configuração efetiva, dedicated/Survival, lifecycle NBT, multiplayer, claims/PvP, opções de mods, GameTests físicos, stress/latência e compatibilidades. **⛔** Adapter Mastery/perks inexistente/não homologado; Stage 06.05 sem promoção. A cobertura 83/83 aqui é de leitura de source, **não** de implementação/teste.

[Registro 83/83](README.md) · [matriz anterior 74/83](PERK-ENGINEERING-MATRIX-OFFENSE-MOVEMENT-0.9.7.1.md).
