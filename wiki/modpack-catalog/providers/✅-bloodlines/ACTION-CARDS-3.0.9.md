# Bloodlines 3.0.9 — fichas individuais de 29 Actions

Estado: **✅ 29/29 registros individualizados e SHA-exatos** · **28 `COUNTED_EXACT`** para identidade compilada na métrica do projeto · **1 `EXCLUDED`** (Sorcerous Strike sem grant normal provado) · **⚠️ Runtime/Survival e configuração implantada pendentes**.

**Prova Java21 #38673548806**: [dossiê físico](EXACT-BINARY-PLAYER-ACTIONS-3.0.9.md). A menção histórica `COUNTED_SOURCE_PINNED` nas 28 linhas abaixo é o status anterior de cada ficha; sua identidade de registro compilado agora é `COUNTED_EXACT`. O `EXCLUDED` Sorcerous Strike permanece excluído. Sem validação de gameplay/Survival.

## Escopo e proveniência

- Este índice representa `IAction` do **Bloodlines/Vampirism**, e não feitiços autônomos de Iron's ou Ars.
- Instalação documentada: `bloodlines-1.21-3.0.9.jar`, mod ID `bloodlines`, Vampirism `1.10.13`.
- Fonte exata da linha instalada: `TheDrOfDoctoring/bloodlines@c8fd517d204d09dfcb9a544c17d7df87755eaa5c` (registro de 29 Actions).
- O [catálogo de Actions](ACTION-CATALOG.md) é a fonte canônica dos contratos e valores source-pinned. Cada página individual preserva a seção pertinente desse catálogo, sem inferir resultados físicos.
- A contagem semântica **já inclui as 28 Actions elegíveis**. Materialização de fichas = **+0 identidades novas**; mínimos globais mantidos em **1.851 / 1.849 no escopo**, com denominador final aberto.
- A Action `gravebound_crit_action` (Sorcerous Strike) é **registrada**, mas **excluída do numerador**: o skill node fica fora da árvore Gravebound efetivamente configurada e dos grants por rank. Não presumir que normal Survival a desbloqueia.
- Recursos, cooldowns, causas de dano, Soul/Blood, skills, estado de possessão, timers e PHYL/restore continuam provider-owned. Nenhum adapter ou pipeline novo é criado.

## Índice — 29/29

| # | Bloodline | Action | Registry ID | Situação | Ficha |
|---:|---|---|---|---|---|
| 1 | Noble | Celerity | `bloodlines:noble_celerity_action` | ✅ COUNTED_EXACT (static) | [Abrir](actions/noble-celerity-action.md) |
| 2 | Noble | Mesmerise | `bloodlines:noble_mesmerise_action` | ✅ COUNTED_EXACT (static) | [Abrir](actions/noble-mesmerise-action.md) |
| 3 | Noble | Leeching | `bloodlines:noble_leeching_action` | ✅ COUNTED_EXACT (static) | [Abrir](actions/noble-leeching-action.md) |
| 4 | Noble | Noble Invisibility | `bloodlines:noble_invisibility_action` | ✅ COUNTED_EXACT (static) | [Abrir](actions/noble-invisibility-action.md) |
| 5 | Noble | Flank | `bloodlines:noble_flank_action` | ✅ COUNTED_EXACT (static) | [Abrir](actions/noble-flank-action.md) |
| 6 | Zealot | Shadowwalk | `bloodlines:zealot_shadowwalk_action` | ✅ COUNTED_EXACT (static) | [Abrir](actions/zealot-shadowwalk-action.md) |
| 7 | Zealot | Dark Cloak | `bloodlines:zealot_darkcloak_action` | ✅ COUNTED_EXACT (static) | [Abrir](actions/zealot-darkcloak-action.md) |
| 8 | Zealot | Wall Climb | `bloodlines:zealot_wall_climb_action` | ✅ COUNTED_EXACT (static) | [Abrir](actions/zealot-wall-climb-action.md) |
| 9 | Zealot | Frenzy | `bloodlines:zealot_frenzy_action` | ✅ COUNTED_EXACT (static) | [Abrir](actions/zealot-frenzy-action.md) |
| 10 | Ectotherm | Lord of Frost | `bloodlines:ectotherm_frostlord_action` | ✅ COUNTED_EXACT (static) | [Abrir](actions/ectotherm-frostlord-action.md) |
| 11 | Ectotherm | Dolphin Leap | `bloodlines:ectotherm_dolphin_leap_action` | ✅ COUNTED_EXACT (static) | [Abrir](actions/ectotherm-dolphin-leap-action.md) |
| 12 | Ectotherm | Ink Splash | `bloodlines:ectotherm_ink_splash_action` | ✅ COUNTED_EXACT (static) | [Abrir](actions/ectotherm-ink-splash-action.md) |
| 13 | Bloodknight | Crimson Leap | `bloodlines:bloodknight_crimson_leap_action` | ✅ COUNTED_EXACT (static) | [Abrir](actions/bloodknight-crimson-leap-action.md) |
| 14 | Bloodknight | Sanguine Infusion | `bloodlines:bloodknight_sanguine_infusion_action` | ✅ COUNTED_EXACT (static) | [Abrir](actions/bloodknight-sanguine-infusion-action.md) |
| 15 | Bloodknight | Blood Hunt | `bloodlines:bloodknight_blood_hunt_action` | ✅ COUNTED_EXACT (static) | [Abrir](actions/bloodknight-blood-hunt-action.md) |
| 16 | Bloodknight | Daywalker | `bloodlines:bloodknight_day_walker_action` | ✅ COUNTED_EXACT (static) | [Abrir](actions/bloodknight-day-walker-action.md) |
| 17 | Bloodknight | Blood Extraction | `bloodlines:bloodknight_blood_extraction_action` | ✅ COUNTED_EXACT (static) | [Abrir](actions/bloodknight-blood-extraction-action.md) |
| 18 | Gravebound | Devour Soul | `bloodlines:gravebound_devour_soul_action` | ✅ COUNTED_EXACT (static) | [Abrir](actions/gravebound-devour-soul-action.md) |
| 19 | Gravebound | Soul Infusion | `bloodlines:gravebound_soul_infusion_action` | ✅ COUNTED_EXACT (static) | [Abrir](actions/gravebound-soul-infusion-action.md) |
| 20 | Gravebound | Lingering Devour | `bloodlines:gravebound_lingering_devour` | ✅ COUNTED_EXACT (static) | [Abrir](actions/gravebound-lingering-devour.md) |
| 21 | Gravebound | Soul Claiming | `bloodlines:gravebound_soul_claiming` | ✅ COUNTED_EXACT (static) | [Abrir](actions/gravebound-soul-claiming.md) |
| 22 | Gravebound | Sorcerous Strike | `bloodlines:gravebound_crit_action` | ⚠️ EXCLUDED | [Abrir](actions/gravebound-crit-action.md) |
| 23 | Gravebound | Mist Form | `bloodlines:gravebound_mist_form_action` | ✅ COUNTED_EXACT (static) | [Abrir](actions/gravebound-mist-form-action.md) |
| 24 | Gravebound | End Mist Form | `bloodlines:gravebound_end_mist_form_action` | ✅ COUNTED_EXACT (static) | [Abrir](actions/gravebound-end-mist-form-action.md) |
| 25 | Gravebound | Phylactery Teleport | `bloodlines:gravebound_phylactery_teleport_action` | ✅ COUNTED_EXACT (static) | [Abrir](actions/gravebound-phylactery-teleport-action.md) |
| 26 | Gravebound | Ghost Walk | `bloodlines:gravebound_ghost_walk_action` | ✅ COUNTED_EXACT (static) | [Abrir](actions/gravebound-ghost-walk-action.md) |
| 27 | Gravebound | Phylactery Soul Transfer | `bloodlines:gravebound_phylactery_soul_transfer_action` | ✅ COUNTED_EXACT (static) | [Abrir](actions/gravebound-phylactery-soul-transfer-action.md) |
| 28 | Gravebound | Possession | `bloodlines:gravebound_possession_action` | ✅ COUNTED_EXACT (static) | [Abrir](actions/gravebound-possession-action.md) |
| 29 | Gravebound | Possession Swap | `bloodlines:gravebound_possession_swap_action` | ✅ COUNTED_EXACT (static) | [Abrir](actions/gravebound-possession-swap-action.md) |

## Gate de runtime

**⚠️ Condicionado:** esses registros e seus parâmetros foram auditados em código/fonte correspondente à versão; não houve teste físico de 29/29 Actions no modpack real nesta materialização. A validação exigirá configuração implantada, timers, pagamento inicial/upkeep, movimento client-sensitive, reconexão, persistência, cancelamentos, Phylactery, Soul conservation e QA de compatibilidade. Sorcerous Strike não pode virar `COUNTED` sem novo caminho de aquisição verificável.

**Limite clean-room:** nenhum código, recurso, texto proprietário de outro mod ou implementação de runtime foi transportado; a individualização reutiliza apenas documentação técnica mantida pelo próprio Black Arcana.
