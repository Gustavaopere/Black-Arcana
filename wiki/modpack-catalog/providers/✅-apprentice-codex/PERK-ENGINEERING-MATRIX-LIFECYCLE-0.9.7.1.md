# Apprentice's Codex 0.9.7.1 — matriz causal de entidades, inventários e jobs

**Checkpoint:** 2026-10-13, Minecraft 1.21.1, NeoForge, Java 21. **✅ 83/83 spells já catalogadas por registry**, **🟡 24/83 spells com fichas causais aprofundadas** (seis originais + oito no [lote anterior](PERK-ENGINEERING-MATRIX-HIGH-RISK-0.9.7.1.md) + **dez nesta matriz**). **59/83** ainda não têm este mesmo nível de engenharia. **+0 novas identidades semânticas.**

**Fonte de instalação:** sibling modlist `Gustavaopere/neoforge-rpg-skilltree/main@f5d31633186a004ada41557220dcafa94a75546e`, caminho `PROJECT-INSTRUCTIONS/modlist/Addons + Armor, Tools, and Weapons + Magic/✅-apprentices-codex v0.9.7.1.md`. JAR declarado `apprentice_codex-0.9.7.1+mc1.21.1.jar`, mod ID `apprenticecodex`, SHA-1 `b514315add32b93b0049c8673075627d7ef812e0`.

**Prova de comportamento:** source `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e` declarado 0.9.7.1. Os 10 dossiês citam classes e métodos concretos e diferenciam defaults/formulas de estado runtime. **⚠️ A presença e a versão do JAR não demonstram equivalência de cada corpo de método compilado**, nem execução física da versão instalada no modpack.

| Spell registry ID | Dossiê individual | Localizador source verificado | Limite prioritário |
|---|---|---|---|
| `apprenticecodex:auto_turret` | [auto_turret](evocation/auto-turret.md) | `AutoTurretEntity.tickOnServer/mobInteract/fire` | spawn com alvo validado; restock com mana owner; ataques não são novos casts |
| `apprenticecodex:companion_trunk` | [companion_trunk](evocation/companion-trunk.md) | `CompanionTrunkManager.toggle/tryDeactivate/deactivateBecauseOwnerDied` | baú não pode despawnar cheio; inventário owner e drop na morte |
| `apprenticecodex:call_broom` | [call_broom](evocation/call-broom.md) | `CallBroomDeploymentManager.validate/execute/onUnequip` | única broom Curios, owner, ride, recall, cleanup |
| `apprenticecodex:bound_sword` | [bound_sword](evocation/bound-sword.md) | `BoundSwordManager.activate/deactivate/validateActiveSwordLocation` | UUID por sessão, dual wield condicionado, restauração de hand slots |
| `apprenticecodex:bound_bow` | [bound_bow](evocation/bound-bow.md) | `BoundBowManager.activate/deactivate/validateActiveBowLocation` | UUID por sessão, filtro anti-cópia e reconstituição da mão |
| `apprenticecodex:archer_multiple` | [archer_multiple](evocation/archer-multiple.md) | `ArcherMultipleManager.validate/expire/finishRecast` | entidade validada contra recast; cleanup percorre níveis e entidades |
| `apprenticecodex:search_beacon` | [search_beacon](evocation/search-beacon.md) | `SearchBeaconSearchService.createSession/advance; SearchBeaconRefundManager.claim` | 48 steps/tick, targets datapack, reserva única de instant brazier |
| `apprenticecodex:tamers_pocket` | [tamers_pocket](evocation/tamers-pocket.md) | `TamersPocket.withdrawLockedPets/deployStoredPets` | NBT de pet, owner, spawn confirmado antes de remover entry |
| `apprenticecodex:personal_shelf` | [personal_shelf](ender/personal-shelf.md) | `PersonalShelfChestBlockEntity.serverTick/exportItem` | owner range XYZ, export via item handler simulado/real |
| `apprenticecodex:tiny_lumberjack` | [tiny_lumberjack](nature/tiny-lumberjack.md) | `TinyLumberjackJob.tick; TinyLumberjackJobManager.onLevelTick` | budget logsPorTick por job e vários jobs possíveis no servidor |

## Contabilidade causal e riscos concretos

- **Entidades e combate:** Auto Turret e Archer Multiple produzem ataques e entidades originadas de um cast. Cada tiro, impacto ou cleanup não é uma segunda spell. `ArcherMultipleManager.discardOwnedBows` percorre níveis/entidades como cleanup de provider; não replicar essa varredura por tick em Black Arcana.
- **Itens gerados e stored equipment:** Bound Sword, Bound Bow e Call Broom associam temporários a UUIDs (de sessão ou de deployment). O estado inclui recast Iron's, Curios, inventories e container cursor; políticas de anti-dupe/relog precisam teste com outros providers.
- **Inventários e perda de itens:** Companion Trunk inibe despawn quando há conteúdo e possui caminho de drop na morte; Personal Shelf importa/exporta através de item handler em duas fases, sem receipt external certificado. Tamer's Pocket serializa pets e só remove entries quando o spawn foi aceito. Não assumir ACID/durabilidade plena entre falhas de servidor sem testes.
- **Busca e tarefas:** Search Beacon limita o orçamento a `SEARCH_STEPS_PER_TICK=48` por sessão e mantém reserva para instant brazier. Tiny Lumberjack limita `logsPerTick` **por job**, mas seu manager não impõe cap global no método local examinado. Verificar escalabilidade, chunks e claims.
- **Perk design:** nenhum método descrito concede autoridade a BA para intervir no runtime de Iron's/Apprentice's. O RPG Skill Tree é progressão via contrato real; não adicionar segunda mana, cast, world mutation, loot, XP, Mastery ou recompensa por callback secundário.
- **QA ⚠️:** versão real de classes/binário do JAR, configuração, client/server no modpack, PvP, entidades, chunk lifecycle, claims, reload, persistência NBT, inventários terceiros e owner inválido. **Adapter de perks/Mastery ⛔**. Stage 06.05 sem promoção.

[Registry fonte](README.md) · [Matriz de oito spells anterior](PERK-ENGINEERING-MATRIX-HIGH-RISK-0.9.7.1.md) · [Integration rules](INTEGRATION-RULES.md) · [Ledger global](../../meta/PERK-READY-COVERAGE-LEDGER.md).
