# Apprentice's Codex 0.9.7.1 — matriz de engenharia causal: mundo, channel e defesa

**Checkpoint:** 2026-10-14; source declarado `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`; modlist sibling `Gustavaopere/neoforge-rpg-skilltree/main@96d31fdc4e881589bc087cdf2a983a44c2588a88`, artefato `apprentice_codex-0.9.7.1+mc1.21.1.jar`, mod ID `apprenticecodex`, SHA-1 `b514315add32b93b0049c8673075627d7ef812e0`.

**Resultado:** ✅ 83/83 identidades source-catalogadas · 🟡 44/83 dossiês causalmente aprofundados (34 anteriores + 10 neste lote) · 39/83 restantes · +0 identidades · sem alterações Java/runtime.

| Spell ID | Ficha | Métodos no source pin | QA e limitação principal |
|---|---|---|---|
| `apprenticecodex:frost_rune` | [frost_rune](ice/frost-rune.md) | `FrostRuneTrapBlockEntity.serverTick/detonate/applyBlast` | NBT, arming, trigger e explosion once |
| `apprenticecodex:inscribe_ice` | [inscribe_ice](ice/inscribe-ice.md) | `InscribeIceDaggerThrowJob.tick; InscribeIceBurst.burstChain` | jobs, chain dedup e remote caster |
| `apprenticecodex:harvest_moon` | [harvest_moon](nature/harvest-moon.md) | `HarvestMoonJob.tick; HarvestMoonJobManager.onLevelTick` | 32 ações/unidade por job, não teto total |
| `apprenticecodex:field_overseer` | [field_overseer](lightning/field-overseer.md) | `FieldOverseerStaffEntity.tickServer/transferOwnerMana` | mana player/staff, owner e recast |
| `apprenticecodex:graced_rain` | [graced_rain](nature/graced-rain.md) | `GracedRainCloudEntity.tickOnServer/applyHealingEffect` | crescimento, cura e dano invertido |
| `apprenticecodex:mage_light` | [mage_light](holy/mage-light.md) | `MageLight.resolveCastTarget; BlockTools.tryPlaceBlockByEntity` | placement autorizado e block lifecycle |
| `apprenticecodex:mystic_shield` | [mystic_shield](holy/mystic-shield.md) | `MysticShieldDefenseEvent.onLivingAttack/releaseStoredDamage` | damage ledger, ID de escudo e counterspell |
| `apprenticecodex:mirage_avoidance` | [mirage_avoidance](ender/mirage-avoidance.md) | `MirageAvoidanceEvents.onPlayerTick/isInputLocked` | game-time repair, movement, client intent |
| `apprenticecodex:feather_rush` | [feather_rush](evocation/feather-rush.md) | `FeatherRushGravityControlEvent.onPlayerTick` | wing owner, gravity e channel projectiles |
| `apprenticecodex:phalanx_charge` | [phalanx_charge](holy/phalanx-charge.md) | `PhalanxWeaponryEntity.tickThrust; PhalanxStanceGuardEvent.onPlayerTick` | virtual shield, counterspell e single beam |

## Engenharia e confiança

- **Uma identidade causal:** uma magia Iron's pode gerar projéteis, jobs, drops, status, strikes e blocos. Esses efeitos derivados não viram novos casts ou procs de XP/Mastery por inferência.
- **Durabilidade:** Frost Rune armazena dados em BlockEntity NBT; Mystic Shield armazena dano em PersistentData; Mirage Avoidance e Feather Rush usam estado temporal de spell. Jobs do Harvest Moon e Inscribe Ice estão em coleções em memória. Nada disso certifica persistência transacional/recuperação após crash no modpack.
- **Orçamentos:** Harvest Moon limita processamento por job, não a quantidade de jobs ativos na lista verificada. Outras entities e canais também requerem QA de densidade e performance.
- **World safety:** cada operação externa é do provider, mesmo quando usa BlockTools. Isso não comprova proteção integral de claim nem transfere autoridade ao WorldEffectPolicy do Black Arcana; esta política rege efeitos BA-owned.
- **⚠️** Equivalência do corpo dos métodos ao JAR instalado, configurações, cliente/servidor real, Survival, PvP, claims, logout/relog, reload, crash, correção de input e performance ainda sem testes físicos.
- **⛔** Nenhuma assinatura de integração Mastery/perks com RPG Skill Tree homologada. Não criar segundo débito de mana, dano, cura, world effect ou recompensa; fail-closed. Stage 06.05 sem promoção.

[Registry 83/83](README.md) · [Matriz high-risk](PERK-ENGINEERING-MATRIX-HIGH-RISK-0.9.7.1.md) · [Matriz lifecycle](PERK-ENGINEERING-MATRIX-LIFECYCLE-0.9.7.1.md) · [Matriz persistent](PERK-ENGINEERING-MATRIX-PERSISTENT-0.9.7.1.md).
