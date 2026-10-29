# Suporte de payload — aero_additions:sync_entity_data (não registrado)

**Contrato:** suporte de Aeromancy Additions `1.2.8`, source fixo `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`. Não é nova identidade de magia. `hooks=NOT_VERIFIED`; `physical_runtime=NOT_TESTED`; **0 certificações / +0 magias / +0 adapters aprovados**. O JAR oficial de publicação foi adquirido separadamente; isso não comprova paridade com o JAR instalado historicamente (SHA-1 histórico de 35 caracteres inválido). [Proveniência e limites](../SOURCE-CONTRACTS-1.2.8.md).

## Presença não equivale a rota ativa

`AASyncEntityDataPacket` declara TYPE `aero_additions:sync_entity_data`, codec e handler. **Não aparece nas três chamadas de registro de `AAPayloadHandler`**, portanto este catálogo não o classifica como payload ativo. `AeromancySpellData.doSync()` contém um ramo `livingEntity instanceof IMagicEntity` que tenta distribuir esta classe aos tracking players; existência do produtor não fecha registro/delivery.

O construtor de envio recebe `AeromancySpellData` e `IMagicEntity`, faz cast para `Entity` e captura seu ID. Wire exato: **int `entityId` → int ID de dados → long flags → int contador**. O handler enfileira uma lambda **vazia**. Não chama `AAClientData.handleAbstractCastingMobSyncedData`; mesmo esse callback auxiliar apenas busca a entidade e tem corpo vazio dentro do `instanceof`.

A attachment padrão de holders não `ServerPlayer` não conserva referência `livingEntity`; o serializer usa construtor booleano, também sem essa referência. Não foi encontrado chamador provider-owned que injete uma referência de mob nessa attachment ou uma atribuição de snapshot ao mob cliente. Assim, documentar o suporte como **presente, não registrado, aplicação cliente incompleta**; não afirmar que sincronização de mobs funciona, nem que uma exceção específica foi reproduzida.

| Eixo | Contrato para perks |
|---|---|
| Dano | N/A: nenhum cálculo/aplicação. |
| Alcance | Ramo produtor declara tracking da entidade; delivery não estabelecido por registro. |
| Alvo | ID de entidade e snapshot codificados, mas handler não os aplica. |
| Tempo | Não há tick/TTL ou conclusão de sync. |
| Custo | N/A: sem cast/mana/cooldown. |

Não usar esta classe como contrato de integração de mobs e não somá-la aos 3 registros ativos. [Registrador](../systems/payload-registration.md) · [attachment](../attachments/aeromancy-magic-data.md).


**Fonte imutável:** [Classe e handler vazio](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/network/AASyncEntityDataPacket.java#L12-L39) · [Lista completa de registros](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/network/AAPayloadHandler.java#L11-L21) · [Ramo produtor](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/network/AeromancySpellData.java#L118-L130) · [Factory attachment](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/network/AADataAttachments.java#L20-L21) · [Deserialização](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/network/AeromancyDataProvider.java#L11-L24) · [Callback de mob incompleto](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/network/AAClientData.java#L29-L40).
