# Waystone Warp / Teleport

**Prova binária física (2026-10-13):** ✅ `COUNTED_EXACT` — `WaystonesAPI.tryTeleportAsync` confirmado no JAR físico `21.1.45`; shared provider teleport pipeline. [Java21 #38460510230](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38460510230), [dossiê](../EXACT-BINARY-ACTIONS-21.1.45.md). Sem promoção de custo, multiplayer, persistência ou Survival (⚠️); +0 nova ação.

- Provider: **Waystones** (`waystones`)
- Version: `21.1.45`
- Classificação: **supernatural player action**
- Semantic state: `COUNTED_EXACT` (**identidade física estática somente**)
- Strict contribution: `1`

## Identidade semântica

Uma única raiz provider-owned cobre o ato sobrenatural de transportar o jogador por uma destination Waystones validada.

As superfícies Waystone, Sharestone, Portstone, Warp Stone, Warp Scroll, Bound Scroll, Return Scroll, inventory-button, Warp Plate traversal e Warp Portal traversal convergem para o mesmo pipeline de teleport settlement e são deduplicadas nesta identidade.

## Causalidade

A reconciliação source-pinned fecha o settlement central do provider através do pipeline que termina em `WaystonesAPI.tryTeleportAsync(...)`.

As diferentes superfícies de entrada não criam magias independentes porque reutilizam a mesma causalidade de validação, requirements e teleport provider-native.

## Evidence boundary

Esta ficha fecha identidade, ownership, deduplicação e source-level reachability. Costs, cooldowns, permission policy, deny lists, multiplayer settlement e valores efetivamente implantados permanecem runtime QA.

Source: `../SOURCE-21.1.45-SEMANTIC-CLOSURE.md`.

## Auditoria técnica para perks — 17/10/2026

**Evidência:** source oficial 21.1.45 em TwelveIterations/Waystones@c540cfdbb9c1d790fbff397beea7c83f0c6f035f (read-only, licença All Rights Reserved); caminhos binários principais do JAR físico SHA-1 6ec1a176a102212db4f6391886db52ed103c830f já verificados em EXACT-BINARY-ACTIONS-21.1.45.md. A API detalhada abaixo é **SOURCE-PINNED**, sem prova específica de ABI binária, event registration, adapter RPG ou gameplay. A modlist física #564 / NeoForge 21.1.250 é authority da presença, não dos valores da configuração instalada.

### Matriz causal por eixo

| Eixo | Fato verificável da versão 21.1.45 | Estado de mutação por perk |
|---|---|---|
| Ingresso | Waystone, Sharestone, Portstone, Warp Stone, scrolls, inventory button, Warp Plate e Warp Portal chegam à ação canônica. Warp Stone usa getUseDuration com **warpStoneUseTime=32 ticks** como default de config; scrolls usam **scrollUseTime=32 ticks** e Warp Plate **warpPlateUseTime=15 ticks**, sujeitos ao caminho e configuração efetiva. | **CONFIG_NATIVE** apenas tempos globais de uso; não há hook per-player homologado. |
| Distância/seleção | O destino é um Waystone identificado, não um alvo arbitrário em raycast. A validação de origem chama isSourceWaystoneInRange; o alcance numérico de cada variante e a distância máxima de destino **não foram medidos** nesta ficha. | **SEM_HOOK_SEGURO** para aumentar range/redefinir seleção de Waystones sem contornar descoberta e autorização. |
| Alvo e destino | WaystoneTeleportContext expõe setTargetWaystone, setFromWaystone e addAdditionalEntity; WaystoneTeleportEntityEvent.Pre expõe setTargetLevel, setTargetPosition, setDirection e overrideResult. São superfícies reais em **source**, não autorização para converter target em AOE. | **HOOK_VERIFICADO no source / ADAPTER NÃO TESTADO** para alteração de posição de cada entidade; fail-closed até validar espaço, claims, dimensão, proteção e causalidade. |
| Área/projétil | Não há projétil mágico de ataque nem AOE como componente de dano deste root. Entidades adicionais são uma lista causal de transporte, não um raio de colisão. | **N/A** dano/raio/hitbox/velocidade de projétil. Fan-out requer caps e QA. |
| Dano/tipo | O caminho catalogado é transporte, sem damage formula ou DamageType ofensivo inerente demonstrado. | **N/A** dano e conversão elemental. |
| Custo | Defaults de warpRequirements: custo XP proporcional à distância 0,01 no ramo não interdimensional; +27 XP no interdimensional; zerar em Warp Plate/destino global/Fleeting Memorial, com clamp 0..27 XP. Flags **enableCosts** e **enableCooldowns** default true. **Não** são valores da config instalada nem prova de XP efetivamente gasto. | **CONFIG_NATIVE** da policy global; WaystoneTeleportEvent.Pre possui setRequirements e addAdditionalEntity no source. **CONTRATO CONDICIONAL** para descontos com revalidação no server e sem pagamento duplo. |
| Cooldown | Regra default inventory-button add_cooldown(inventory_button,300) [unidade a homologar no parser]; não transferir este número às demais superfícies. | **CONFIG_NATIVE**; perk por usuário não comprovada. |
| Execução e evento | tryTeleportAsync retorna CompletableFuture de resultado; Pre é publicado antes da validação inicial, Prepare antes do carregamento de chunks, Entity.Pre por entidade antes da aplicação; Post depende de sucesso, Complete é emitido também em falhas normais. Após preparação, requirements são revalidados e consumidos antes de performTeleport. | **HOOK_VERIFICADO no source / QA PENDENTE**. Observação de Pre/Post/Complete não é prova de transporte efetivo nem de Mastery once-only. |

### Contratos concretos e cautelas de ordem

- [WaystoneTeleportContext.java](https://github.com/TwelveIterations/Waystones/blob/c540cfdbb9c1d790fbff397beea7c83f0c6f035f/common/src/main/java/net/blay09/mods/waystones/api/WaystoneTeleportContext.java#L15-L64): setters de destino, requirements, entidades extras e flags.
- [WaystoneTeleportEvent.java](https://github.com/TwelveIterations/Waystones/blob/c540cfdbb9c1d790fbff397beea7c83f0c6f035f/common/src/main/java/net/blay09/mods/waystones/api/event/WaystoneTeleportEvent.java#L17-L150): Pre (setRequirements/addAdditionalEntity), Prepare (chunks e tasks), Post/Complete (observação e resultados).
- [WaystoneTeleportEntityEvent.java](https://github.com/TwelveIterations/Waystones/blob/c540cfdbb9c1d790fbff397beea7c83f0c6f035f/common/src/main/java/net/blay09/mods/waystones/api/event/WaystoneTeleportEntityEvent.java#L18-L105): mutação de nível, posição e direção por entidade, além de veto/override. Um Post também pode representar tentativa cancelada e **não** deve disparar XP/Mastery automaticamente.
- [WaystoneTeleportManager.java — Pre e requirements](https://github.com/TwelveIterations/Waystones/blob/c540cfdbb9c1d790fbff397beea7c83f0c6f035f/common/src/main/java/net/blay09/mods/waystones/core/WaystoneTeleportManager.java#L434-L485) e [async settlement](https://github.com/TwelveIterations/Waystones/blob/c540cfdbb9c1d790fbff397beea7c83f0c6f035f/common/src/main/java/net/blay09/mods/waystones/core/WaystoneTeleportManager.java#L333-L366): requirements revisados após prepare, cobrados antes de performTeleport. Falha posterior ainda requer QA sobre refund; **não presumir atomicidade perfeita**.
- [WaystonesConfigData.java](https://github.com/TwelveIterations/Waystones/blob/c540cfdbb9c1d790fbff397beea7c83f0c6f035f/common/src/main/java/net/blay09/mods/waystones/config/WaystonesConfigData.java#L15-L25) e [tempos/toggles](https://github.com/TwelveIterations/Waystones/blob/c540cfdbb9c1d790fbff397beea7c83f0c6f035f/common/src/main/java/net/blay09/mods/waystones/config/WaystonesConfigData.java#L68-L116): defaults, não política efetiva do servidor.

**Próximo gate:** observar os eventos no JAR físico 21.1.45 com provider carregado, validar ordem, cancelamento, custo debitado/refund, regras do servidor, reaproveitamento do mesmo cast entre portal/placa/scroll, proteção e sincronismo em cliente/modpack real. RPG Skill Tree só pode aplicar perks e Mastery por adapter validado; Black Arcana não assume runtime Waystones nem gera um segundo teleport para produzir efeito.
