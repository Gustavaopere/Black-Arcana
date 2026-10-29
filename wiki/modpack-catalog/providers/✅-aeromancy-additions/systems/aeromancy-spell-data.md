# Estado — AeromancySpellData

**Contrato:** suporte de Aeromancy Additions `1.2.8`, source fixo `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`. Não é nova identidade de magia. `hooks=NOT_VERIFIED`; `physical_runtime=NOT_TESTED`; **0 certificações / +0 magias / +0 adapters aprovados**. O JAR oficial de publicação foi adquirido separadamente; isso não comprova paridade com o JAR instalado historicamente (SHA-1 histórico de 35 caracteres inválido). [Proveniência e limites](../SOURCE-CONTRACTS-1.2.8.md).

## Dados e autoridade

`AeromancySpellData` mantém `serverPlayerId` final, referência opcional `livingEntity`, `isMob`, `syncedEffectFlags` (`long`) e `airStepHitsRemaining` (`int`). O construtor de entidade captura o ID ou `-1` quando nula; o vazio e o booleano usam `-999`. `getAeromancyData(entity)` retorna a [attachment](../attachments/aeromancy-magic-data.md) da própria entidade.

A representação de rede é **int ID → long flags → int contador**, nessa ordem; não transporta referência, UUID ou `isMob`. O objeto decodificado tem ID mas não referência `livingEntity`, de modo que seu `doSync()` não distribui outro pacote. NBT usa `putFloat`/`getInt` para o contador: anomalia de tipos observada na fonte, sem conclusão de falha física.

| Operação | Mutação e consequência local |
|---|---|
| `addEffects(mask)` | OR das flags, depois `doSync()`. |
| `removeEffects(mask)` | AND com complemento, depois `doSync()`. |
| `hasEffect(mask)` | Compara máscara; não sincroniza. |
| `getAirStepHitsRemaining()` | **Chama `doSync()` antes de retornar**, inclusive em leitura de `canJump`. |
| `subtractAirStepHits()` | Decrementa sem clamp, depois sync; o gate positivo pertence ao chamador de Airstep. |
| `setAirStepHitsRemaining(n)` | Atribui sem clamp, depois sync. |
| `setShapeshiftId(loc)` | Apenas sync; armazenamento e leitor de shapeshift estão comentados. |

`doSync()` distribui `AASyncPlayerDataPacket` aos tracking players e ao próprio player quando a referência é `ServerPlayer`. Há ramo para `IMagicEntity` que cria `AASyncEntityDataPacket`, mas [esse payload não é registrado e seu handler é vazio](../payloads/sync-entity-data.md). Demais referências não enviam. `syncToPlayer(recipient)` envia o snapshot diretamente ao destinatário, independentemente do ID interno.

## Leitores/escritores auditados

Os únicos escritores ativos do contador fora da classe são os callbacks de [Airstep](../spells/airstep.md): cast, queda/recarga, salto/decremento, remoção/expiração/reset. `canJump` lê a attachment; o [HUD](airstep-counter-bar.md) lê o snapshot separado de `AAClientData`.

Flags constantes `ASPHYXIATING=1`, `WIND_SHIELD=2` e `AIR_STEP=4` existem, porém não há chamadas ativas do provider a `addEffects`, `removeEffects` ou ao `hasEffect` desta classe. Os antigos escritores de Breathless/WindShield estão comentados. `WindySwirlRenderer.shouldRender` usa `entity.hasEffect(MobEffect)`; o valor `2` recebido escolhe qual MobEffect consultar, sem ler `syncedEffectFlags`. Portanto não atribuir lifetime/efeitos visuais à bitmask.

## Eixos para perks

| Eixo | Contrato |
|---|---|
| Dano | N/A: nenhum cálculo de dano nesta classe. |
| Alcance | N/A local; distribuição é tracking/self ou destinatário explícito. |
| Alvo | Entidade associada/holder; ID numérico da rede é lookup do cache cliente. |
| Tempo | Não tem tick/TTL/reset global; lifetime e resets delegados a Airstep/MobEffect. |
| Custo | N/A: sem mana/cooldown ou settlement de casting. |

Nenhum método desta classe é um hook de perk aprovado. [Lifetime e stores distintos](state-lifecycle-network-ui.md).


**Fonte imutável:** [Estado e codec](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/network/AeromancySpellData.java#L15-L71) · [Mutadores e distribuição](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/network/AeromancySpellData.java#L79-L143) · [Contador Airstep](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/airstep/AirstepSpell.java#L77-L131) · [HUD](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/airstep/AirstepCounterBar.java#L17-L26) · [Flags comentadas WindShield](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/wind_shield/WindShieldEffect.java#L14-L25) · [Flags comentadas Breathless](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/asphyxiate/BreathlessEffect.java#L29-L38) · [Renderer usa MobEffects](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/wind_shield/WindySwirlRenderer.java#L139-L143).
