# Payload S2C — aero_additions:sync_magic_data

**Contrato:** suporte de Aeromancy Additions `1.2.8`, source fixo `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`. Não é nova identidade de magia. `hooks=NOT_VERIFIED`; `physical_runtime=NOT_TESTED`; **0 certificações / +0 magias / +0 adapters aprovados**. O JAR oficial de publicação foi adquirido separadamente; isso não comprova paridade com o JAR instalado historicamente (SHA-1 histórico de 35 caracteres inválido). [Proveniência e limites](../SOURCE-CONTRACTS-1.2.8.md).

## Snapshot e aplicação

`AASyncPlayerDataPacket` é registrado `playToClient`, com `STREAM_CODEC` que delega a `AeromancySpellData.write/read`. Wire exato: **int `serverPlayerId` → long `syncedEffectFlags` → int `airStepHitsRemaining`**. O construtor que recebe dados guarda a referência do objeto; não faz clone local. O decoder cria uma nova instância com ID e campos, sem referência de entidade. Não transporta UUID, dimensão, tick/sequence number ou `isMob`.

`handle` enfileira `AAClientData.handlePlayerSyncedData(packet.data)`, que substitui a entrada do map estático pela chave ID. Não há `setData` da attachment cliente nem validação de entidade existente no nível. O [HUD Airstep](../systems/airstep-counter-bar.md) lê esse map; a validação de salto lê a attachment, portanto a recepção não prova convergência dos dois stores.

## Produtores observados

- `AeromancySpellData.doSync()` com referência `ServerPlayer`: tracking players e self. É chamado por mutadores e pelo **getter** do contador.
- `AeromancySpellData.syncToPlayer(recipient)`: destinatário direto, sem dependência do tipo de referência interna.
- Login, respawn e dimension change: attachment do próprio jogador enviada a ele.
- `StartTracking`: literal fonte envia **dados do tracker/event.getEntity() ao target/event.getTarget()**, ambos `ServerPlayer`; não trocar silenciosamente os papéis no contrato.

| Eixo | Contrato para perks |
|---|---|
| Dano | N/A: snapshot sem operação de dano. |
| Alcance | Tracking/self ou receptor explícito; não é alcance de spell. |
| Alvo | Cache cliente identificado por ID inteiro, sem lookup obrigatório da entidade. |
| Tempo | Envios por chamadas/eventos; não há tick periódico, confirmação ou versão por snapshot. |
| Custo | N/A: não lança magia nem debita mana/cooldown. |

Flags não têm escritores ativos externos no provider; não inferir aplicações de efeitos pela presença dos campos no wire. [Lifetime e limitações](../systems/state-lifecycle-network-ui.md). Reconnect, tracking tardio, ordem dos snapshots e ID reuse são QA físico pendente.


**Fonte imutável:** [Payload](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/network/AASyncPlayerDataPacket.java#L10-L34) · [Codec de dados](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/network/AeromancySpellData.java#L42-L54) · [Envios](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/network/AeromancySpellData.java#L79-L130) · [Cache](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/network/AAClientData.java#L14-L26) · [Eventos de lifecycle](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/AAServerEvents.java#L92-L119).
