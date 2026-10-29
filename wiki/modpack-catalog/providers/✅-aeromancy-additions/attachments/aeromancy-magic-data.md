# Attachment — aero_additions:aeromancy_magic_data

**Contrato:** suporte de Aeromancy Additions `1.2.8`, source fixo `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`. Não é nova identidade de magia. `hooks=NOT_VERIFIED`; `physical_runtime=NOT_TESTED`; **0 certificações / +0 magias / +0 adapters aprovados**. O JAR oficial de publicação foi adquirido separadamente; isso não comprova paridade com o JAR instalado historicamente (SHA-1 histórico de 35 caracteres inválido). [Proveniência e limites](../SOURCE-CONTRACTS-1.2.8.md).

## Registro, posse e serialização

`AADataAttachments.AEROMANCY_DATA` é um `AttachmentType<AeromancySpellData>` registrado no registry NeoForge de attachments com o namespace `aero_additions`. O construtor do mod registra esse deferred register no mod event bus. Não é `MagicData` de Iron's, nem capacidade de RPG Skill Tree.

O factory cria `new AeromancySpellData(serverPlayer)` somente para holder `ServerPlayer`; os demais recebem o construtor vazio, com ID `-999` e referência de entidade nula. O serializer `AeromancyDataProvider.read` reconstrói a referência para `ServerPlayer`; para outros holders usa o construtor booleano `true`, também sem referência de entidade. O campo `isMob` assim marcado não tem leitor ativo nesta classe; não prova sync de mobs.

| Campo persistido | Escrita | Leitura | Limite demonstrado |
|---|---|---|---|
| `effectFlags` | `putLong` | `getLong` | Flags preservadas como `long` no código. |
| `airStepHitsRemaining` | **`putFloat`** a partir do `int` | **`getInt`** | Divergência de tipo fonte-fixada; não há teste de save/reload neste contrato que comprove perda ou erro em runtime. |
| Identidade/referência | Não gravadas no NBT | Recriadas a partir do holder | Não serializa UUID, `serverPlayerId`, `livingEntity` ou `isMob`. |

`write` cria um `CompoundTag` novo e delega `saveNBTData`; `read` chama `loadNBTData`. O builder ativa `.serialize(...)` e não apresenta `.copyOnDeath(...)`. Não há handler `PlayerEvent.Clone` neste provider que ligue `clone()`/`getPersistentData()` da classe de dados. Os dois métodos criam objetos novos sem copiar flags/contador; sua existência não estabelece retenção em morte/respawn. Os eventos de respawn apenas enviam o estado disponível, sem efetuar cópia. [Fluxo completo](../systems/state-lifecycle-network-ui.md).

## Eixos para perks

| Eixo | Contrato |
|---|---|
| Dano | N/A: armazena estado, não causa dano. |
| Alcance | N/A: attachment é local ao holder; alcance de tracking pertence à distribuição de payloads. |
| Alvo | Holder da attachment; factory só conserva referência para `ServerPlayer`. |
| Tempo | Persistência NBT; não implementa tick, expiração ou cópia na morte. Lifetime de Airstep pertence ao MobEffect e seus eventos. |
| Custo | N/A: não cobra mana/cooldown; casting permanece em Iron's. |

Não há API aprovada para perks escreverem diretamente o contador de outro provider. O tipo NBT, restauração por holder, morte/respawn, logout/relogin e mudança de dimensão são verificações físicas pendentes.


**Fonte imutável:** [AADataAttachments.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/network/AADataAttachments.java#L13-L22) · [AeromancyDataProvider.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/network/AeromancyDataProvider.java#L11-L25) · [NBT e cópia](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/network/AeromancySpellData.java#L57-L71) · [clone/persistentData](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/network/AeromancySpellData.java#L134-L143) · [Eventos de sync](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/AAServerEvents.java#L92-L119) · [Bootstrap](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/Aeromancy.java#L30-L40).
