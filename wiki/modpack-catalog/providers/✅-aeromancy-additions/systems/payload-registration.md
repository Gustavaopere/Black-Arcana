# Rede — registro dos payloads

**Contrato:** suporte de Aeromancy Additions `1.2.8`, source fixo `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`. Não é nova identidade de magia. `hooks=NOT_VERIFIED`; `physical_runtime=NOT_TESTED`; **0 certificações / +0 magias / +0 adapters aprovados**. O JAR oficial de publicação foi adquirido separadamente; isso não comprova paridade com o JAR instalado historicamente (SHA-1 histórico de 35 caracteres inválido). [Proveniência e limites](../SOURCE-CONTRACTS-1.2.8.md).

## Rotas ativas

`AAPayloadHandler.register(RegisterPayloadHandlersEvent)` cria `event.registrar(Aeromancy.MOD_ID).versioned("1.0.0").optional()`. O protocolo declarado é `1.0.0`, distinto da versão do mod `1.2.8`. A anotação `@EventBusSubscriber` usa `modid=aero_additions`; o source não traz outro branch de registro de payloads. A opção `.optional()` é declarativa; não certifica conexão física entre clientes/servidores diferentes.

| ID | Direção registrada | Codec e callback | Ficha |
|---|---|---|---|
| `aero_additions:dash_particles` | `playToClient` | `DashParticlesPacket.STREAM_CODEC` / `handle` | [Partículas de Dash](../payloads/dash-particles.md) |
| `aero_additions:airstep` | `playToServer` | `AirstepPacket.STREAM_CODEC` / `handle` | [Input Airstep](../payloads/airstep.md) |
| `aero_additions:sync_magic_data` | `playToClient` | `AASyncPlayerDataPacket.STREAM_CODEC` / `handle` | [Snapshot de player](../payloads/sync-magic-data.md) |
| `aero_additions:sync_entity_data` | **Não registrado** | Classe/codec presentes; handler vazio | [Suporte incompleto de entidade](../payloads/sync-entity-data.md) |

São **3 registros ativos**, incluindo somente **1 rota C2S provider-owned**. `sync_entity_data` não é uma quarta rota ativa. Todos os handlers ativos usam `context.enqueueWork` antes da ação. Nenhuma rota substitui a infraestrutura de cast, mana ou cooldown de Iron's. Não inventar um pacote de lançamento de magia, spell ID, seleção de nível, alvo arbitrário ou settlement financeiro neste protocolo.

## Eixos para perks

| Eixo | Contrato |
|---|---|
| Dano | N/A no registrador; nenhuma rota ativa transporta valor de dano. |
| Alcance | Distribuição definida nos produtores (tracking/self ou envio direto); não é raio de ataque. |
| Alvo | Direções fixadas por `playToClient`/`playToServer`; C2S usa `ctx.player()`. |
| Tempo | Registro por evento; execução dos callbacks enfileirada. Sem rate limit local adicional. |
| Custo | N/A: protocolo não cobra mana/cooldown; cast pertence a Iron's. |

Perks não devem recriar/proxyar estes payloads. Validação de Airstep está no callback chamado, com gates exatos documentados na ficha individual. [Integração de lifetime/UI](state-lifecycle-network-ui.md).


**Fonte imutável:** [AAPayloadHandler.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/network/AAPayloadHandler.java#L11-L21) · [IDs e handler Airstep](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/airstep/AirstepPacket.java#L10-L37) · [ID Dash](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/dash/DashParticlesPacket.java#L21-L25) · [ID sync player](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/network/AASyncPlayerDataPacket.java#L10-L33) · [Sync entidade não efetivo](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/network/AASyncEntityDataPacket.java#L12-L35).
