# Moonfall

Status: `SOURCE-PINNED 5.13.1 / GLOBAL-TIME RITUAL`

- Registry id: `ars_nouveau:ritual_moonfall`
- Class: `RitualMoonfall`
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native behavior

Moonfall operates on the server Overworld because Ars Nouveau treats time as global. While daytime is before the night threshold, it advances Overworld day time by `100` ticks per ritual tick. It also increments ritual progress once per 20 server ticks.

When progress reaches `18`, it snaps the Overworld to the provider helper's next night time and sends time synchronization packets to Overworld players, then marks the ritual finished.

The provider description is simply: sets the time to night.

## Authority / Black Arcana boundary

Global time mutation belongs to Ars Nouveau for this ritual. Black Arcana must not duplicate the time advance, completion or synchronization merely because it observes ritual completion.

Any future Black Arcana celestial/time ritual must be compared mechanically against Moonfall and remain server-authoritative and bounded rather than becoming a cosmetic duplicate.

## QA

Source lifecycle is pinned to 5.13.1. Runtime interaction with other time-control mods/game rules in the full pack remains pending.

## Engenharia para perks — execução do ritual

- **Source pin:** [`RitualMoonfall.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualMoonfall.java), versão Ars Nouveau 5.13.1.
- **Authority temporal:** `RitualMoonfall.tick()` usa `ServerLevel.getServer().overworld()`, mesmo quando o ritual está em outro lugar; isso é alteração do tempo global do servidor, não de dimensão local.
- **Relógio:** se `dayTime%24000<13000` adiciona `100` day ticks por tick do ritual e envia `ClientboundSetTimePacket` aos players Overworld. **Detalhe corrigido do ciclo:** no `else`, `incrementProgress()` ocorre **a cada tick** quando a condição de dia deixou de ser atendida; separadamente, se `getGameTime()%20==0`, incrementa outra vez. Em progress `>=18`, define `MathUtil.getNextDaysTime(...NIGHT_TIME)`, sincroniza e `setFinished`.
- **Perks/segurança:** progresso não tem uma cadência única fixa de 20 ticks; não duplicar atualização de tempo nem tratar observação visual como confirmação de conclusão. Qualquer magia temporal própria exige autoridade de mundo e limites.
- **Status:** ✅ código fonte exato; ⚠️ configurações e comportamento físico dos providers adicionais pendentes; ⛔ mutabilidade em ritual ou integração com Mastery não é provada pelos eventos de glyph. Ritual runtime permanece Ars Nouveau.

## Certificação técnica estática de ritual — 25/10/2026

**✅ `STATIC_TECHNICAL_CATALOG_ONLY` para planejamento de perks e balanceamento; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** Documentação source-pinned não equivale a implementação de hook, aceitação de cliente, ou QA no modpack real.

| Campo obrigatório para perks | Evidência técnica e limite de aplicabilidade |
|---|---|
| Identidade e proveniência | `ars_nouveau:ritual_moonfall`, classe `RitualMoonfall`, release `ars_nouveau-1.21.1-5.13.1.jar`. [Source imutável](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualMoonfall.java); [IDs de 24 rituais comprovados no JAR SHA-exato](../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). |
| Causalidade, fases e settlement | `tick` apenas em servidor obtém `server.overworld()`. Se `dayTime % 24000 <13000 && >=0`, avança o relógio global em **100** por tick e envia `ClientboundSetTimePacket` aos jogadores Overworld; fora da condição acelera progresso com `incrementProgress()` a cada tick. Adicionalmente, a cada `gameTime%20==0` incrementa e, se progresso ≥18, fixa `MathUtil.getNextDaysTime(...NIGHT_TIME)`, sincroniza e `setFinished()`. |
| Fórmulas, limites, duração, caps e gatilhos | Limiar alvo de noite em **13000** day ticks, passo de 100, progress threshold **18**; condição de conclusão aninhada no tick de 20 e incrementos não lineares. Não calcular duração fixa como 18×20 ticks nem equiparar `GameRules.RULE_DAYLIGHT` ao gate de autorização (usado no pacote). |
| Alvo, área/volume, dano, projétil e tempo | Modificar relógio do Overworld global, sem target de Form, AoE, projétil, dano, duração própria de status ou tipo de dano. Nenhum dado de entidade é avaliado para seleções de vítimas; efeitos são de world-time. |
| Fonte/custos/cooldowns e consumo de itens | `AbstractRitual.getSourceCost()` default **0**, não sobrescrito aqui; custo de setup e consumo externo ao getter ainda não auditados. **Não aplicáveis como custo local:** mana de glyph, cooldown de ataque/Forms ou XP por hit. Ritual físico/ativação/receitas item são próprios do Ars; não inferir pagamento bem-sucedido, drops ou custos adicionais sem a implementação de brasier/recipes. |
| Integração e limites de authority | Não dobrar relógio por perk ou evento de sync, nem prometer efeitos de lua em modpack com outros sistemas; integração com Black Arcana ou RPG Skill Tree deve respeitar ownership temporal Ars. O Black Arcana detém seu runtime, rituais, hazards, Corruption, Strain e WorldEffectPolicy próprio; este ritual e sua persistência são provider-owned Ars. RPG Skill Tree fornece apenas Mastery/gates/perks através de bridge testado; não há adapter validado de mutação destes métodos. |
| Validação e pendências | Identidade e class-to-ID do publisher JAR 5.13.1 SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd` auditadas anteriormente; semântica de método provém do source fixo `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`. Essas são **provas distintas**: não se afirma equivalência de classfile completo, config efetiva, side/server do pack, snapshot persistence, proteção de mundo, multiplayer ou QA físico (`NOT_TESTED`). |

**Regra fail-closed:** qualquer alteração do ritual/custo/range/duração ou concessão de Mastery exige inspeção do ponto de mutação real, chamadas downstream de Source/settlement, bounds, deduplicação e testes específicos. Não promover Stage06.05/09 nem contar ticks/pacotes/partículas como casts.
