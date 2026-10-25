# Sunrise

Status: `SOURCE-PINNED 5.13.1 / GLOBAL-TIME RITUAL`

- Registry id: `ars_nouveau:ritual_sunrise`
- Class: `RitualSunrise`
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native behavior

Sunrise operates on the server Overworld because Ars Nouveau treats time as global. While the world is outside the provider's daytime target window, it advances Overworld day time by `100` ticks and synchronizes time packets to Overworld players.

Once per 20 server ticks it also increments ritual progress. At progress `18`, it snaps the Overworld to the provider helper's next day time, synchronizes clients and marks the ritual finished.

Provider description: sets the time to day.

## Authority / Black Arcana boundary

Time mutation and synchronization are Ars Nouveau authority for this ritual. Black Arcana must not reapply them or credit repeated time packets as separate magical actions.

Any independent Black Arcana solar/time ritual must occupy a distinct semantic role and remain server-authoritative/bounded.

## QA

Exact source lifecycle is pinned to 5.13.1. Interaction with other global time-control providers remains full-pack runtime QA.

## Engenharia para perks — contrato de ritual

- **Fonte exata:** [`RitualSunrise.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualSunrise.java) no Ars 5.13.1.
- **Dimensão e relógio:** `tick()` opera em `ServerLevel` e redireciona ao `server.overworld()`. Se `dayTime%24000<1000` ou `>=12000`, incrementa dayTime em 100 por tick e sincroniza `ClientboundSetTimePacket` com todos players Overworld.
- **Progresso não linear:** quando o mundo **já está** dentro da janela de dia, o `else` chama `incrementProgress()` a cada tick; separadamente, a cada `gameTime%20==0` incrementa novamente. Ao atingir progress>=18, fixa `MathUtil.getNextDaysTime(...DAY_TIME)`, sincroniza e finaliza. Assim não declarar duração fixa de `18*20` ticks.
- **Perks:** alteração global do relógio tem conflitos potenciais com outros providers de tempo, autoridade é Ars e não deve ser replicada; pacotes são sincronização e não novos casts/credit de progressão.
- **Estado:** ✅ identidade/métodos/source pin; ⚠️ valores no modpack, proteções, Save/Restart e multiplayer não testados nesta branch. ⛔ adapter RPG para mutation, bônus de recursos ou acompanhamento de um cast por ritual não implementado; Ars conserva Source e world authority.

## Certificação técnica estática de ritual — 25/10/2026

**✅ `STATIC_TECHNICAL_CATALOG_ONLY` para planejamento de perks e balanceamento; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** Documentação source-pinned não equivale a implementação de hook, aceitação de cliente, ou QA no modpack real.

| Campo obrigatório para perks | Evidência técnica e limite de aplicabilidade |
|---|---|
| Identidade e proveniência | `ars_nouveau:ritual_sunrise`, classe `RitualSunrise`, release `ars_nouveau-1.21.1-5.13.1.jar`. [Source imutável](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualSunrise.java); [IDs de 24 rituais comprovados no JAR SHA-exato](../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). |
| Causalidade, fases e settlement | `tick` gera VFX e, em servidor, redireciona `ServerLevel` para `server.overworld()`. Enquanto `dayTime % 24000 < 1000` ou `>=12000`, incrementa relógio de dia global em **100 ticks por ritual tick** e envia `ClientboundSetTimePacket` aos jogadores do Overworld. Na janela alvo, o `else` chama `incrementProgress()` por tick; além disso a cada `overworld.gameTime % 20 == 0` incrementa novamente e **somente dentro dessa condição** finaliza quando progresso ≥18, fixa `MathUtil.getNextDaysTime(...DAY_TIME)` e ressincroniza. |
| Fórmulas, limites, duração, caps e gatilhos | `dayTime modulo 24000`, limiares 1000/12000, passo +100; conclusão com progress ≥18 verificada **somente no ramo a cada 20 game ticks**, embora incrementos adicionais ocorram por tick na janela. Portanto **não** afirmar duração fixa de `18×20` ticks nem cota de mudança temporal desacoplada de gamerule/gametime. A `GameRules.RULE_DAYLIGHT` aparece no pacote de sincronização, não como gate local de `setDayTime`. |
| Alvo, área/volume, dano, projétil e tempo | Target é o **relógio global Overworld**, não entidade/bloco selecionados por spell Form; nenhuma área, projétil, tipo de dano ou cooldown de ataque intrínseco. ClientboundSetTimePacket é apresentação/sincronização, não cast. |
| Fonte/custos/cooldowns e consumo de itens | `AbstractRitual.getSourceCost()` default = **0**; esta classe não sobrescreve o getter. Não concluir que ritual não tem nenhum custo de setup/item, apenas que Source-cost local é 0 na herança. **Não aplicáveis como custo local:** mana de glyph, cooldown de ataque/Forms ou XP por hit. Ritual físico/ativação/receitas item são próprios do Ars; não inferir pagamento bem-sucedido, drops ou custos adicionais sem a implementação de brasier/recipes. |
| Integração e limites de authority | Conflito com outros providers de tempo, dimensão de ativação e proteções exigem QA; não emitir Mastery por pacote/tick nem injetar outro `setDayTime`. Autoridade e ritmo são do Ars; helper de relógio é do provider. O Black Arcana detém seu runtime, rituais, hazards, Corruption, Strain e WorldEffectPolicy próprio; este ritual e sua persistência são provider-owned Ars. RPG Skill Tree fornece apenas Mastery/gates/perks através de bridge testado; não há adapter validado de mutação destes métodos. |
| Validação e pendências | Identidade e class-to-ID do publisher JAR 5.13.1 SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd` auditadas anteriormente; semântica de método provém do source fixo `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`. Essas são **provas distintas**: não se afirma equivalência de classfile completo, config efetiva, side/server do pack, snapshot persistence, proteção de mundo, multiplayer ou QA físico (`NOT_TESTED`). |

**Regra fail-closed:** qualquer alteração do ritual/custo/range/duração ou concessão de Mastery exige inspeção do ponto de mutação real, chamadas downstream de Source/settlement, bounds, deduplicação e testes específicos. Não promover Stage06.05/09 nem contar ticks/pacotes/partículas como casts.
