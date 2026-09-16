# Bloodlines 3.0.9 — magias e poderes

Source authority: `TheDrOfDoctoring/bloodlines@c8fd517d204d09dfcb9a544c17d7df87755eaa5c`.

## Resultado do inventário

Bloodlines **não registra spells próprios** em um spell registry como Iron's Spells 'n Spellbooks ou Ars Nouveau. A superfície sobrenatural provider-owned da versão 3.0.9 é implementada como:

- **29 Actions** registradas em `VampirismRegistries.Keys.ACTION`;
- **101 Skills** registradas em `VampirismRegistries.Keys.SKILL`;
- efeitos passivos/event-driven, atributos e estados das cinco Bloodlines;
- Gravebound Souls/Phylactery e Vampirism blood como recursos distintos.

Portanto, para esta pasta, `MAGIAS.md` funciona como o índice canônico da superfície de poderes sem renomear Actions/Skills como spells. Os números de cooldown, duração, custo, dano, alcance e demais parâmetros abaixo permanecem provider-owned/configuráveis; a especificação source-level completa está em [`ACTION-CATALOG.md`](ACTION-CATALOG.md), [`SKILL-CATALOG.md`](SKILL-CATALOG.md) e [`RESOURCE-AUTHORITY.md`](RESOURCE-AUTHORITY.md).

## Actions — 29/29

### Noble — 5

| Poder | ID | Contrato principal |
|---|---|---|
| Celerity | `bloodlines:noble_celerity_action` | 60 s cooldown; 5 s; velocidade por rank 0/20/40/60%; Step Height +0.5 a partir do rank configurado 3. |
| Mesmerise | `bloodlines:noble_mesmerise_action` | 60 s cooldown; 20 s; alterna o estado provider-owned de mesmerise. |
| Leeching | `bloodlines:noble_leeching_action` | 120 s cooldown; 10 s; ativa leeching, aumenta Blood Exhaustion e liquida sangue/heal no hook de dano do provider. |
| Invisibility | `bloodlines:noble_invisibility_action` | Deduplica com a invisibilidade base do Vampirism; quando combinada, defaults efetivos 10 s cooldown / 45 s duração. |
| Flank | `bloodlines:noble_flank_action` | 15 s cooldown; teleporte atrás de alvo visível; range configurado 300 e refinements do Vampirism podem modificá-lo. |

### Zealot — 4

| Poder | ID | Contrato principal |
|---|---|---|
| Shadowwalk | `bloodlines:zealot_shadowwalk_action` | Teleporte em baixa luz; cooldown por rank 15/8/5/3 s; usa range do teleport do Vampirism no source auditado. |
| Dark Cloak | `bloodlines:zealot_darkcloak_action` | Toggle condicionado a luz; cooldown 0; timer default clamped para 2,147,483,620 ticks. |
| Wall Climb | `bloodlines:zealot_wall_climb_action` | 20 s cooldown; 15 s; climb speed 0.3; movimento observado no caminho client-side, exigindo QA dedicado. |
| Frenzy | `bloodlines:zealot_frenzy_action` | 60 s cooldown; 15 s; Block Break Speed +10/15/20/25% por rank. |

### Ectotherm — 3

| Poder | ID | Contrato principal |
|---|---|---|
| Lord of Frost | `bloodlines:ectotherm_frostlord_action` | 15 s cooldown; duração 15/30/60/120 s por rank; pode dobrar; habilita Ice/Frozen/Slowness hooks e dano configurável. |
| Dolphin Leap | `bloodlines:ectotherm_dolphin_leap_action` | Requer água; 7 s cooldown; 5 s; leap via packet e Movement Speed II periódico. |
| Ink Splash | `bloodlines:ectotherm_ink_splash_action` | Requer água; 60 s cooldown; Blindness 150 ticks em LivingEntities num volume inflado em 3 blocos, sem filtro de facção observado. |

### Bloodknight — 5

| Poder | ID | Contrato principal |
|---|---|---|
| Crimson Leap | `bloodlines:bloodknight_crimson_leap_action` | 20 ticks cooldown; 50 ticks; custo 8 sangue; gate mantém reserva positiva; movimento via packet. |
| Sanguine Infusion | `bloodlines:bloodknight_sanguine_infusion_action` | 30 s cooldown; 3000 s; custo inicial 3 sangue; upkeep real 2 sangue/160 ticks; buffs de movimento/jump e sibling infusion. |
| Blood Hunt | `bloodlines:bloodknight_blood_hunt_action` | 30 s cooldown; 3000 s; custo inicial 3 sangue; upkeep real 2 sangue/140 ticks; invisibilidade e Hidden Strike causal. |
| Daywalker | `bloodlines:bloodknight_day_walker_action` | 300 s cooldown; 180 s; custo inicial 5 sangue; upkeep real 2 sangue/45 ticks; mantém Sunscreen enquanto ativo. |
| Blood Extraction | `bloodlines:bloodknight_blood_extraction_action` | 900 s cooldown; converte 3 unidades do sangue da criatura-alvo + Glass Bottle em Vampire Blood Bottle quando todos os gates provider-native passam. |

### Gravebound — 12

| Poder | ID | Contrato principal |
|---|---|---|
| Devour Soul | `bloodlines:gravebound_devour_soul_action` | Cooldown 75/60/40/20 s; sem custo de Soul; elegibilidade via `canDevour`; invalid LivingEntity pode ainda reportar success no source auditado. |
| Soul Infusion | `bloodlines:gravebound_soul_infusion_action` | 4 Souls; 30 s cooldown; 10 s; cura 5 e mantém Regeneration II + Resistance I. |
| Lingering Devour | `bloodlines:gravebound_lingering_devour` | 2 Souls; 250 s cooldown; entidade por 30 s; raio ~4.5→8; Poison II/50 ticks. |
| Soul Claiming | `bloodlines:gravebound_soul_claiming` | 3000 s cooldown; 20 s; devora Souls de mortes qualificadas; modo passivo pode substituir a Action selecionável. |
| Sorcerous Strike | `bloodlines:gravebound_crit_action` | 90 s cooldown; janela 10 s; próximo critical elegível recebe +1.25 adicional e Wither; survival reachability não comprovada no tree atual. |
| Mist Form | `bloodlines:gravebound_mist_form_action` | Resurrection state automático; 20 s; cooldown 90 s ou 30 s com Faster Resurrection; custo por rank 15/12/8/5 ou 10/8/6/3; exige Souls estritamente maiores que o custo para sobreviver à saída. |
| End Mist Form | `bloodlines:gravebound_end_mist_form_action` | 20 ticks; só durante Mist Form; aborta a forma reaplicando dano letal/matando o player. |
| Phylactery Teleport | `bloodlines:gravebound_phylactery_teleport_action` | Teleporte provider-native até a Phylactery; custos e gates de Souls/Mist Form permanecem detalhados em `ACTION-CATALOG.md`. |
| Ghost Walk | `bloodlines:gravebound_ghost_walk_action` | Mobilidade/estado espiritual provider-native; custo, timer e gates completos no catálogo de Actions. |
| Phylactery Soul Transfer | `bloodlines:gravebound_phylactery_soul_transfer_action` | Transfere Souls entre estado Gravebound/Phylactery conforme autoridade do provider. |
| Possession | `bloodlines:gravebound_possession_action` | Inicia possessão somente nos alvos/estados autorizados pelo provider. |
| Possession Swap | `bloodlines:gravebound_possession_swap_action` | Troca a entidade/estado possuído dentro do lifecycle de Possession; não deve ser emulado por estado paralelo. |

## Dano e efeitos passivos

Nem todo dano/efeito de Bloodlines nasce de uma Action. Diversas Skills são passivas ou hooks causais sobre ataques, crítico, morte, luz, água, sangue, Souls e estado da Bloodline. O inventário completo de 101 Skills e sua topologia está em `SKILL-CATALOG.md`; os pipelines de dano/recursos e pontos estáticos que exigem QA estão em `TECHNICAL-AUDIT.md`.

## Regra de integração Black Arcana

- Não criar um spell duplicado para representar uma Action Bloodlines.
- Não liquidar novamente sangue, Souls, heal, dano, cooldown ou reward que o provider já liquidou.
- Gates de Bloodline, rank, Skill e recurso devem consultar a autoridade do provider.
- Qualquer integração que dependa de movimento client-sensitive, settlement ambíguo ou mismatch estático permanece **fail-closed até runtime QA**.
- A combinação instalada com Vampirism 1.10.13 ainda requer runtime/addon-interoperability QA antes de promover hooks sensíveis a internals como runtime-confirmed.
