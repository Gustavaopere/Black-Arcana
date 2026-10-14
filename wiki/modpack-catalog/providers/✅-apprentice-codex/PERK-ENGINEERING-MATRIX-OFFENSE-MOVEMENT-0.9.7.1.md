# Apprentice's Codex 0.9.7.1 — engenharia causal de ofensiva, movimento e detecção

**Checkpoint:** 2026-10-14 · Minecraft 1.21.1 / NeoForge / Java 21 · sibling modlist `main@63a41587ed91e6768a6b863e74dfaf44b9eb3a46` · instalado `apprentice_codex-0.9.7.1+mc1.21.1.jar`, mod ID `apprenticecodex`, SHA-1 `b514315add32b93b0049c8673075627d7ef812e0` · source declarado `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`.

✅ **83/83 identidades** source-catalogadas; 🟡 **74/83 dossiês causais aprofundados** (64 na main de partida +10 fichas existentes atualizadas aqui); **9/83** restantes. +0 novas magias semânticas; docs-only, 0 Java/adapters.

| Spell ID | Ficha | Source code auditado | Contrato adicional |
|---|---|---|---|
| `apprenticecodex:arcane_beam` | [arcane_beam](ender/arcane-beam.md) | `ArcaneBeamEntity.tick/damageHitTarget` | comentário 1/5 vs condição 4/5; cleanup owner |
| `apprenticecodex:mantis_leap` | [mantis_leap](ender/mantis-leap.md) | `MantisLeapMovementEvent.onPlayerTick/onLivingAttack` | watchdog, landing fallback, janela Mob-only |
| `apprenticecodex:mana_slash` | [mana_slash](ender/mana-slash.md) | `ManaSlash.resolveCatalystWeaponDamage/ManaSlashProjectileEntity.tick` | atributos dinâmicos, dedup, Crystal Bladed Staff |
| `apprenticecodex:long_stride` | [long_stride](ender/long-stride.md) | `LongStrideFluidMovement.apply/findFluidSupport` | mob effect + fluid movement |
| `apprenticecodex:slash_blade` | [slash_blade](evocation/slash-blade.md) | `SlashBladeKatanaEntity.slash` | oclusão, box horizontal e dano reduzido |
| `apprenticecodex:tiro_volley` | [tiro_volley](evocation/tiro-volley.md) | `TiroVolley.spawnDueMuskets/TiroVolleyMusketEntity.tryFire` | 32 spawns/call, muzzle line-of-sight, tiro pós-cancel |
| `apprenticecodex:magic_spear` | [magic_spear](fire/magic-spear.md) | `MagicSpear.nextSide/MagicSpearMissileEntity.tickServer` | lado persistente, homing, phases e anti-magic |
| `apprenticecodex:artisan_smash` | [artisan_smash](fire/artisan-smash.md) | `ArtisanSmashLauncherEntity.fire/ArtisanSmashShellEntity.applyBlastDamage` | UUID owner, splash com oclusão e policy |
| `apprenticecodex:mana_charge` | [mana_charge](holy/mana-charge.md) | `ManaCharge.onServerCastTick/spawnManaChargeParticles` | mana canônica vs partículas |
| `apprenticecodex:sense_evil` | [sense_evil](holy/sense-evil.md) | `SenseEvil.collectUndeadSpawners/collectHighlights` | chunks loaded-only, snapshot, highlights sem cap explícito |

## Riscos e critérios para o próximo QA

- **Divergência código/comentário:** `ArcaneBeamEntity.tick` contém comentário de dano a cada cinco ticks, mas executa `damageHitTarget` quando `tickCount % 5 != 0`. Diferença source-only; reproduzir em JAR físico antes de classificar bug runtime.
- **Causalidade:** uma execução de magia host pode originar hits periódicos, efeitos de locomoção, muitos summons, splash e partículas; não se deve premiar cada entidade, evento ou hit como novo cast, nem cobrar mana duas vezes.
- **Limites locais vs globais:** `TiroVolley` tem máximo de 32 spawns por callback, não máximo global de muskets; `SenseEvil` inspeciona chunks carregados sem cap visível de highlights no coletor analisado. Stress de servidor, pacotes e limpeza de entidades exige QA.
- **Mundo e proteção:** `SlashBlade` causa dano reduzido atravessando oclusão; `ArtisanSmash` filtra seu splash com clip por parede; `MantisLeap` mantém fallback de pouso no alvo original quando nenhum offset está livre. Tais decisões do provider não autorizam ignorar `WorldEffectPolicy` no Black Arcana.
- ⚠️ Testes de física, configuração ativa, bytecode do JAR instalado, PvP/claims, ciclo de vida NBT, dedicated, restart e coexistência ainda pendentes. ⛔ Sem adapter/hook real homologado de perks/Mastery com RPG Skill Tree; fail-closed. Não avançar Stage 06.05.

[Registry 83/83](README.md) · [lote anterior](PERK-ENGINEERING-MATRIX-UTILITY-LIFECYCLE-0.9.7.1.md).
