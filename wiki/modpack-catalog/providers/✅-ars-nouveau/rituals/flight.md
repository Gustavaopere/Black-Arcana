# Flight

Status: `SOURCE-PINNED 5.13.1 / RANGE-EFFECT RITUAL`

- Registry id: `ars_nouveau:ritual_flight`
- Class: `RitualFlight`
- Effect: provider `FLIGHT_EFFECT`
- Effect duration per application: `60 × 20 = 1200 ticks`
- Range: `60` blocks
- Source cost declaration: `200`
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native lifecycle

`RitualFlight` extends Ars Nouveau's `RangeEffectRitual`. A player is eligible only server-side, within range, and while the ritual is not already waiting for Source. When `attemptRefresh` successfully applies the effect, the ritual marks itself as needing Source.

The ritual also exposes a jump-event path: when a `ServerPlayer` jumps without the Flight effect, it attempts to refresh/apply the ritual effect. Successful application synchronizes the player's prior flight state through `PacketUpdateFlight`.

## Authority / Black Arcana boundary

Flight capability, effect refresh and Source debit are Ars Nouveau authority. Black Arcana must not grant a second flight state, consume another resource or convert every jump into a new cast/mastery event.

This provider capability is distinct from Black Arcana mobility spells and from external glider/stamina systems; integration requires a real semantic boundary rather than presentation matching.

## QA

Source lifecycle is pinned to 5.13.1. Interaction with other flight providers, ability modifiers and full-pack movement systems remains runtime QA.

## Localizadores e parâmetros para Codex — fonte exata

- **Java:** [`RitualFlight.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualFlight.java) no commit `112920ff774831f204031da75b4c4e73d3765157` correspondente ao catálogo Ars 5.13.1.
- **Implementação:** `RitualFlight extends RangeEffectRitual`; `getEffect=FLIGHT_EFFECT`, `getDuration=1200 ticks`, `getRange=60 blocks`, `getSourceCost=200` no código-fonte desta versão.
- **Ativação e refresh:** `applyEffect(ServerPlayer)` salva estado `wasFlying`, chama `super.applyEffect(player,false)` e sincroniza `PacketUpdateFlight` só no sucesso. `onJumpEvent` tenta `attemptRefresh` somente para player sem efeito.
- **Perk de ritual:** alcance, duração, custo, recarga e elegibilidade são knobs conceitualmente separados; ampliar buff sem manter contrato de `RangeEffectRitual` e custo Source seria bypass.
- **Mastery:** evento de pulo não é automaticamente uma conclusão de ritual. Atribuir XP somente a uma ação canônica comprovada; nenhuma bridge nova foi implementada.

**Estado:** prova estática de parâmetros por leitura de código; habilidade de mutação por hook externo não verificada. Ars controla composição, execução, mana/Source e configurações; RPG Skill Tree controla perks/Mastery/gates; Black Arcana é autoridade somente de seu runtime próprio. [Padrão universal](../../../meta/PERK-READY-TECHNICAL-STANDARD.md).

## Certificação técnica estática de ritual — 25/10/2026

**✅ `STATIC_TECHNICAL_CATALOG_ONLY` para planejamento de perks e balanceamento; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** Documentação source-pinned não equivale a implementação de hook, aceitação de cliente, ou QA no modpack real.

| Campo obrigatório para perks | Evidência técnica e limite de aplicabilidade |
|---|---|
| Identidade e proveniência | `ars_nouveau:ritual_flight`, classe `RitualFlight`, release `ars_nouveau-1.21.1-5.13.1.jar`. [Source imutável](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualFlight.java); [IDs de 24 rituais comprovados no JAR SHA-exato](../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). |
| Causalidade, fases e settlement | `RitualFlight extends RangeEffectRitual extends RangeRitual`. Pai enfileira posição do ritual no `RitualEventQueue` no servidor a cada **20 game ticks**, se ainda não contida. Em refresh, `shouldApply` exige lado server, `!needsSourceNow()` e `BlockUtil.distanceFrom(level,ritualPos,playerPos)<=getRange()`; `getRange=60`. `applyEffect(ServerPlayer)` guarda `wasFlying`, chama `super.applyEffect(player,false)` e só no sucesso envia `PacketUpdateFlight(true,wasFlying)`. `onJumpEvent` só chama `attemptRefresh` para ServerPlayer **sem `FLIGHT_EFFECT`**; não é todo salto um cast. |
| Fórmulas, limites, duração, caps e gatilhos | `getDuration()=60×20=1200 ticks` e `getEffect()=ModPotions.FLIGHT_EFFECT`; amplifier fixo 0 no `RangeEffectRitual.applyEffect`. Range 60 é **distância computada por `BlockUtil.distanceFrom`**, não afirmamos sua métrica exata ou volumes de seleção sem ver helper. Fonte mostra `setNeedsSource(true)` em refresh bem-sucedido; cooldown do cast e caps de vuelo não estão no método. |
| Alvo, área/volume, dano, projétil e tempo | ServerPlayer dentro do alcance de 60 do ritual, não projeção/área genérica de caster; duração do MobEffect 1200 ticks. Sem DamageType, projétil ou dano intrínseco. Player abilities/flying dependem de consumidores e pacote do provider. |
| Fonte/custos/cooldowns e consumo de itens | `getSourceCost()=200` por exigência de Source do ritual; no executor `RangeEffectRitual.attemptRefresh`, **somente `applyEffect` bem-sucedido** causa `setNeedsSource(true)`. Não provar quantas retiradas efetivas ocorreram ao longo do tempo sem auditar `RitualBrazierTile.takeSource`. **Não aplicáveis como custo local:** mana de glyph, cooldown de ataque/Forms ou XP por hit. Ritual físico/ativação/receitas item são próprios do Ars; não inferir pagamento bem-sucedido, drops ou custos adicionais sem a implementação de brasier/recipes. |
| Integração e limites de authority | `PacketUpdateFlight` e salto são sinais downstream, não novas perícias por tick/salto. Não substituir habilidade de voo de outro mod, não estender Source/despesa sem preservar canApply e ownership; QA com outros providers de voo imprescindível. O Black Arcana detém seu runtime, rituais, hazards, Corruption, Strain e WorldEffectPolicy próprio; este ritual e sua persistência são provider-owned Ars. RPG Skill Tree fornece apenas Mastery/gates/perks através de bridge testado; não há adapter validado de mutação destes métodos. |
| Validação e pendências | Identidade e class-to-ID do publisher JAR 5.13.1 SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd` auditadas anteriormente; semântica de método provém do source fixo `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`. Essas são **provas distintas**: não se afirma equivalência de classfile completo, config efetiva, side/server do pack, snapshot persistence, proteção de mundo, multiplayer ou QA físico (`NOT_TESTED`). |

**Regra fail-closed:** qualquer alteração do ritual/custo/range/duração ou concessão de Mastery exige inspeção do ponto de mutação real, chamadas downstream de Source/settlement, bounds, deduplicação e testes específicos. Não promover Stage06.05/09 nem contar ticks/pacotes/partículas como casts.
