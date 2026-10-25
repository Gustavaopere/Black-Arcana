# Ars Nouveau 5.13.1 — segundo lote de Rituals: mundo, captura e controle

**Cinco contratos estáticos adicionais; rituais certificados 10/24.** Com os 35/67 Effects atualmente na main, o resultado desta branch é **63/138 fichas Ars Nouveau**, **63/2075 fichas globais candidatas** e **0/164 providers integralmente certificados**. Futuras certificações de Effects por outro executor podem aumentar esses numeradores; esta tabela é um checkpoint, não uma constante do runtime.

Source `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` e JAR publisher `ars_nouveau-1.21.1-5.13.1.jar` SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd` para ID/classe. **Sem equivalência integral de métodos no binário ou QA físico.**

| Ritual | Contrato causal source-pinned | Bloqueio de perk |
|---|---|---|
| [Gravity](rituals/gravity.md) | `GRAVITY_EFFECT`, 1200 ticks, range60, Source getter 200; renewInterval20/renewThreshold200 apenas declarados, não provar agendamento com os campos | ⛔ hook de refresh/gravity não comprovado |
| [Restoration](rituals/restoration.md) | AABB5/100 ticks, zombie villager converts, inverted sofre playerAttack fake-player de 10, outro alvo ferido recebe heal 10; Source getter200 por trabalho observado | ⛔ não duplicar heal/dano/conversão |
| [Warping](rituals/warping.md) | Consome WarpScroll válido e compatível, em progress>=3 teleporta entidades na AABB5 via `teleportTo(x,y,z)`; Source getter herdado 0, não é ritual sem ingredientes | ⛔ cross-dim e safety não validados |
| [Containment](rituals/containment.md) | 60 ticks: jars em cubo 7³, entidades AABB inflate5 por jar; whitelist tem prioridade, serializa 1 entidade por jar/execução, Source getter500 após sucesso | ⛔ não duplicar NBT ou Mastery |
| [Harvest](rituals/harvest.md) | 200 ticks: 9×3×9 candidatas, eventual Y+2; maturidade, seed replant, InventoryManager/drop e Source getter100; proteção/atomicidade não garantida pelo método | ⛔ não duplicar drop/alteração mundo |

**Proveniência e restrições:** o código do ritual é provider-owned. WorldEffectPolicy do Black Arcana não controla automaticamente mundo/claims do Ars. Os métodos `RangeEffectRitual`, `MobJarTile`, `InventoryManager`, `WarpScrollData` e brasier permanecem consumidores/autoridades próprias a auditar end-to-end antes de alterar comportamento. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`.

**Não executado:** perks mutadoras, servidor físico com todos os mods, compatibilidade com claims, energia/Source efetivamente debitada, NBT durante save/restart e Stage 06.05/09. Nenhum ID novo de ritual foi registrado.
