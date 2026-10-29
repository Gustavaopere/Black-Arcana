# Cache cliente — AAClientData

**Contrato:** suporte de Aeromancy Additions `1.2.8`, source fixo `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`. Não é nova identidade de magia. `hooks=NOT_VERIFIED`; `physical_runtime=NOT_TESTED`; **0 certificações / +0 magias / +0 adapters aprovados**. O JAR oficial de publicação foi adquirido separadamente; isso não comprova paridade com o JAR instalado historicamente (SHA-1 histórico de 35 caracteres inválido). [Proveniência e limites](../SOURCE-CONTRACTS-1.2.8.md).

## Entrada e leitura

`AAClientData` mantém um `HashMap<Integer, AeromancySpellData>` estático por ID numérico de entidade, um objeto fallback com ID `-999` e um campo `playerMagicData` sem leitor/escritor ativo externo neste source. `handlePlayerSyncedData(snapshot)` substitui a entrada do map para `snapshot.getServerPlayerId()`; não mistura campos e não chama `entity.setData`.

`getAeroSpellData(livingEntity)` devolve a entrada/fallback se for `Player`; para outros tipos cria `new AeromancySpellData(null)` com ID `-1`. Não resolve UUID ou mundo. Nenhum caminho de limpeza do map em logout, desconexão, remoção de entidade ou mudança de mundo aparece no provider auditado; não se afirma vazamento físico ou problema reproduzido.

O [payload S2C ativo](../payloads/sync-magic-data.md) enfileira a inserção. O [contador HUD](airstep-counter-bar.md) lê esse map. O caminho de salto cliente consulta `AeromancySpellData.getAeromancyData(entity)`, que lê **outra store: a attachment da entidade**. Não há ponte source-visível que aplique o snapshot recebido à attachment cliente. A apresentação de um número no HUD, por si só, não demonstra que a predição cliente aceita o mesmo número de saltos.

`handleAbstractCastingMobSyncedData` apenas obtém o mundo, retorna se nulo, busca a entidade por ID e faz um `instanceof IMagicEntity` com corpo vazio. Não atualiza mob nem map. O payload de entidade também tem corpo vazio e não está registrado.

## Eixos para perks

| Eixo | Contrato |
|---|---|
| Dano | N/A: cache de apresentação, sem dano. |
| Alcance | N/A: consulta local por ID; não faz busca espacial. |
| Alvo | Apenas players no map; não é repositório de estado de mobs. |
| Tempo | Vida estática da classe, sem limpeza/TTL explícitos no source auditado. |
| Custo | N/A: sem mana/cooldown/cast. |

Não promover o cache a autoridade de validação ou de progressão. Client attachment/cache, reconnect, reuso de entity ID e atraso de sync exigem QA físico; nenhum adapter está certificado.


**Fonte imutável:** [AAClientData.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/network/AAClientData.java#L10-L40) · [Entrada S2C](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/network/AASyncPlayerDataPacket.java#L26-L33) · [Leitura HUD](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/airstep/AirstepCounterBar.java#L17-L26) · [Leitura de validação](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/airstep/AirstepSpell.java#L98-L130) · [Attachment lookup](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/network/AeromancySpellData.java#L118-L130) · [Entidade sem aplicação](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/network/AASyncEntityDataPacket.java#L23-L35).
