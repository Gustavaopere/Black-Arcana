# Reconciliação das classes externas finais de itens — 1.0.10

**Reuso de disposição existente, sem novos certificados.** Base main `9eeb5db432e5c9c552e8866214d34ec9fd20da73`. Artefato publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, modlist sibling #19. Conferidas as fichas e [índice do provider](INDEX.md) na base; a classe consta no conteúdo de cada ficha correspondente, não somente no título.

| Classe | Fichas existentes | Estado |
|---|---|---|
| `RainbounceBootsItem` | [items/rainbounce-boots.md](items/rainbounce-boots.md) | CERTIFIED_STATIC (fichas existentes) |
| `RaygunItem` | [damage-types/raygun.md](damage-types/raygun.md) | CERTIFIED_STATIC (fichas existentes) |
| `RemoteDetonatorItem` | [items/remote-detonator.md](items/remote-detonator.md) | PARTIAL (ficha existente) |
| `ResistorShieldItem` | [items/resistor-shield.md](items/resistor-shield.md) | CERTIFIED_STATIC (fichas existentes) |
| `SeaStaffItem` | [actions/sea-staff-water-bolt.md](actions/sea-staff-water-bolt.md) | CERTIFIED_STATIC (fichas existentes) |
| `ShotGumItem` | [equipment/shot-gum.md](equipment/shot-gum.md) | CERTIFIED_STATIC (fichas existentes) |
| `SugarStaffItem` | [actions/sugar-staff-hex-cast.md](actions/sugar-staff-hex-cast.md) · [actions/sugar-staff-peppermint-cast.md](actions/sugar-staff-peppermint-cast.md) | CERTIFIED_STATIC (fichas existentes) |
| `TotemOfPossessionItem` | [actions/totem-possession-remote-control.md](actions/totem-possession-remote-control.md) | CERTIFIED_STATIC (fichas existentes) |

Oito classes externas e nove fichas já presentes (oito certificadas, uma parcial). RaygunItem tem os 26 métodos próprios abrangidos por sua ficha consolidada em damage-types/raygun.md; não criar duplicata por categoria. Sea Staff e Sugar Staff/Totem estão cobertos pelas ações existentes, sem inferir cobertura integral de outros consumidores. Remote Detonator tem lacuna de World Safety e permanece parcial. Resistor Shield e Rainbounce Boots preservam os selos existentes. Nenhum incremento de fichas ou certificados por esta reconciliação.

## Restante do recorte

59/81 disposições documentadas na main base. Esta reconciliação acrescenta oito classes ao recorte candidato: 67/81, antes de contabilizar a PR #1233 (um owner direto mapeado e dois de bloco com identidade pendente). O trabalho em #1233 e os dois novos probes são deliberadamente separados dos índices compartilhados para evitar concorrência e números obsoletos. Se os três radioativos e os 11 owners finais forem reconciliados, o roster de 81 classes externas terá disposição registrada; isso não fecha o universo semântico ou certifica todas as fichas.

- [Late concrete items](EXACT-LATE-CONCRETE-ITEMS-1.0.10.md): sete classes, dez factories diretas.
- [Terminal helpers](EXACT-TERMINAL-ITEM-HELPERS-1.0.10.md): quatro classes, seis factories diretas.

NO_MUTATION / FAIL_CLOSED / PHYSICAL_QA_NOT_TESTED. Sem novo certificado, índice, alteração de runtime ou avanço de Stage.
