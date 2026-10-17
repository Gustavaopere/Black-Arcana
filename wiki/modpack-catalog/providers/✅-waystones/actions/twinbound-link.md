# Twinbound Link

**Prova binária física (2026-10-13):** ✅ `COUNTED_EXACT` — `TwinboundFeatherItem.onUseTick → TwinboundFeatherLinksComponent.with` confirmado no JAR físico `21.1.45`; reciprocal cooperative link without teleport. [Java21 #38460510230](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38460510230), [dossiê](../EXACT-BINARY-ACTIONS-21.1.45.md). Sem promoção de custo, multiplayer, persistência ou Survival (⚠️); +0 nova ação.

- Provider: **Waystones** (`waystones`)
- Version: `21.1.45`
- Classificação: **cooperative ritual-like supernatural action**
- Semantic state: `COUNTED_EXACT` (**identidade física estática somente**)
- Strict contribution: `1`
- Provider surface: **Twinbound Feather**

## Identidade semântica

Ação cooperativa independente em que dois jogadores usam Twinbound Feathers de forma sincronizada e mutuamente direcionada.

A conclusão persiste estado recíproco de vínculo provider-owned. Uma Feather vinculada pode então expor o parceiro como destination dinâmica no ecossistema Waystones.

## Deduplicação

Criar o vínculo não executa o teleport e não duplica a raiz **Waystone Warp / Teleport**. O vínculo prepara estado persistente de destino; o eventual transporte continua pertencendo ao pipeline normal do provider.

## Evidence boundary

A identidade, persistência causal e source-level reachability estão fechadas. Timing da interação, edge cases multiplayer, reconnect/persistence e policy de servidor permanecem QA de runtime.

Source: `../SOURCE-21.1.45-SEMANTIC-CLOSURE.md`.

## Auditoria técnica para perks — 17/10/2026

**Evidência:** fonte oficial 21.1.45 em TwelveIterations/Waystones@c540cfdbb9c1d790fbff397beea7c83f0c6f035f; vínculo recíproco já comprovado como raiz estática no JAR físico SHA-1 6ec1a176a102212db4f6391886db52ed103c830f. Esses detalhes são **SOURCE-CAUSALITY**; não atestam uso multiplayer real ou mutabilidade por perks.

### Matriz causal por eixo

| Eixo | Fato do source | Estado de integração |
|---|---|---|
| Ingresso | Dois ServerPlayers devem usar Twinbound Feather. use inicia uso de item; onUseTick opera **somente ServerLevel/ServerPlayer**. | Provider-owned; hook de progressão por uso **NÃO VERIFICADO**. |
| Alvo/distância | findTargetedPlayer usa raycast de entidade em visão de **2 blocos** (TARGETING_RANGE=2), caixa de busca inflada em **1 bloco** e predicado ServerPlayer+isPickable. Exige que o alvo esteja usando a Feather **e aponte de volta**. | **SEM_HOOK_SEGURO** para aumento de alcance, seleção múltipla, direcionamento por entidade genérica ou AOE. |
| Tempo | TWINNING_DURATION é **20 iterações de onUseTick** com parceiro válido e persistente. getUseDuration retorna **72000 ticks**, teto de uso sustentado do item, **não** duração do ritual. Se perde alvo, troca parceiro ou solta, o progresso local é reiniciado. | **SEM_HOOK_SEGURO** para redução de tempo por perk sem modificação provider-native aprovada. |
| Efeito terminal | becomeBesties atribui UUID a cada Feather se necessário e persiste referências recíprocas usando TwinboundFeatherLinksComponent.with; vínculo já existente retorna false. A Feather pode expor parceiro como destino Waystones, sem teletransportar neste momento. | **HOOK NÃO HOMOLOGADO**. Método público da implementação não é contrato aprovado para rescrever links. |
| Estado e persistência | TwinboundFeatherLinksComponent possui Codec de lista de UUID; **links são estado de ItemStack**, enquanto twinningProgress é mapa estático ConcurrentHashMap **somente RAM**. | Reconnect/restart, troca de item e duplicação de link precisam QA física. |
| Área/projétil/dano/tipo | Ritual cooperativo de alvo único; sem projétil, AOE ofensivo, DamageType ou damage settlement observado. | **N/A** para perks de dano, projectile hitbox e explosão. |
| Custo/cooldown | Não há consumo de Feather ou débito de mana/XP diretamente no fluxo onUseTick→becomeBesties examinado. **Não** é prova de custo global zero sob modpack e outros componentes. | **NÃO VERIFICADO** como boundary de descontos; não criar recurso paralelo. |

### Âncoras auditáveis

- [TwinboundFeatherItem.java linhas 33–90](https://github.com/TwelveIterations/Waystones/blob/c540cfdbb9c1d790fbff397beea7c83f0c6f035f/common/src/main/java/net/blay09/mods/waystones/item/TwinboundFeatherItem.java#L33-L90): range constante, ticks máximos do item, use/release e sync indireto do grupo Players.
- [TwinboundFeatherItem.java linhas 93–148](https://github.com/TwelveIterations/Waystones/blob/c540cfdbb9c1d790fbff397beea7c83f0c6f035f/common/src/main/java/net/blay09/mods/waystones/item/TwinboundFeatherItem.java#L93-L148): ticks acumulados, targeting mútuo, reinicializações e limiar 20. A duração depende de condições **contínuas**, não é garantia de conclusão em 1 segundo cronológico.
- [TwinboundFeatherItem.java linhas 159–190](https://github.com/TwelveIterations/Waystones/blob/c540cfdbb9c1d790fbff397beea7c83f0c6f035f/common/src/main/java/net/blay09/mods/waystones/item/TwinboundFeatherItem.java#L159-L190): idempotência e duas gravações de ItemStack.
- [TwinboundFeatherLinksComponent.java](https://github.com/TwelveIterations/Waystones/blob/c540cfdbb9c1d790fbff397beea7c83f0c6f035f/common/src/main/java/net/blay09/mods/waystones/component/TwinboundFeatherLinksComponent.java#L10-L27): Codec persistente e helper with.
- [WaystonesAPI.java](https://github.com/TwelveIterations/Waystones/blob/c540cfdbb9c1d790fbff397beea7c83f0c6f035f/common/src/main/java/net/blay09/mods/waystones/api/WaystonesAPI.java#L48-L93): teleporte posterior usa pipeline distinto da raiz de vínculo.

**QA e fail-closed:** testar 2 clientes conectados, ambos mirando, perda de mira antes/depois do limiar, reconnect/logout, mudança de dimensão, clone/troca de Feather, item já vinculado, links múltiplos, save/restart e tentativa simultânea. Não atribuir duas recompensas de Mastery ao mesmo vínculo recíproco; sem evento causal apropriado ou settlement comprovado, não implementar perk de alcance/duração nem contagem de XP. Waystones continua dono da interação, RPG Skill Tree apenas do progresso via contrato real.
