# Raygun — fronteira C2S e registro de rede, Alex's Caves Continued 1.0.10

**Estado:** 🟡 descoberta técnica read-only em andamento; **não** é auditoria de segurança
concluída, certificação de perks, evidência de exploit ou QA em cliente/servidor.

## Escopo e autoridade

- Artefato da modlist física: `alexscaves-1.0.10-neoforge+1.21.1.jar`,
  mod ID `alexscaves`, Minecraft 1.21.1 / Java 21.
- SHA-1 do publisher: `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`.
- SHA-256: `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- Evidência anterior: [manifesto receiver SHA-exato](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-RAYGUN-RECEIVER-1.0.10.json),
  [manifesto de munição/C2S](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-RAYGUN-PACKET-AMMO-1.0.10.json),
  [ficha Raygun](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/damage-types/raygun.md).
- Nova coleta: [probe read-only](alexscaves_1010_raygun_registration_probe.py),
  [regressões sintéticas](alexscaves_1010_raygun_registration_probe_test.py) e
  [workflow](../../.github/workflows/alexscaves-1010-raygun-registration.yml).

O receiver já documentado consulta o contexto, resolve uma entidade por ID,
confere o tipo de item na mão e chama `UpdatesStackTags.updateTagFromServer`.
A implementação default observada encaminha o `CompoundTag` ao setter de
`DataComponents.CUSTOM_DATA`. **Nenhuma dessas referências isoladas prova**
a direção registrada do pacote, a autorização server-side do entity ID,
sanitização do conteúdo, replay protection ou execução em sessão de jogo.

## Lacuna técnica fechável sem reauditar os contratos existentes

O probe novo usa **somente o JAR SHA-exato**, uma busca limitada de candidatos
pelo constant pool e `javap` em classes selecionadas. Exporta:
caminho e hash da classe, nome/descritor JVM, hash do método extraído,
offset/opcode/símbolo de referências a `UpdateItemTagMessage` ou
`ACNetworkContext`, mais contadores de orçamento de inspeção.

**Limite metodológico:** uma classe com token não significa registrar,
receber ou autorizar o pacote. Referências compiladas são candidatas,
não prova de execução, direção, threading ou identidade de remetente.
Não copiar implementação Java do provider; somente fatos de ABI e referências
simbólicas relevantes para interoperabilidade.

## Resultado observado do probe de descoberta

- Execução no publisher 1.0.10: [GitHub Actions — run 41328521835](https://github.com/Gustavaopere/Black-Arcana/actions/runs/41328521835), **sucesso** no head inicial da PR #993; a CI do head atualizado deve repetir a conferência.
- **32 classes candidatas** encontradas por referências no constant pool; **47 métodos com referências simbólicas** selecionados, sem implicar 32 registries ou 47 handlers do Raygun.
- No conjunto, `com/github/alexmodguy/alexscaves/server/message/ACNetwork.class` apresenta métodos candidatos `registerMessages()` e `lambda$registerPayloads$0(ACNetwork$ACPayload, IPayloadContext)`, extraídos da versão exata.
- Outras classes retornadas incluem handlers de mensagens não relacionadas e classes de `citadel`; apenas a presença do nome `ACNetworkContext` não demonstra acoplamento causal ao Raygun.
- A regressão nova exige as **duas referências de método** no `ACNetwork` real além dos sender e receiver já selados; **não** declara direção de registro, autorização, threading, vínculo de item ou segurança de recepção comprovados.

Esta prova delimita onde examinar o registro do payload e evita reiterar auditorias já incorporadas. Uma certificação futura precisa revisar os opcodes do `ACNetwork` e reconstruir os guards pertinentes, sem tratar o relatório de candidatos como call graph completo.

## Traçado de ABI de registro do pacote — verificação dirigida

Após a descoberta limitada da PR #993, a auditoria adicional
[`alexscaves_1010_raygun_network_abi_probe.py`](alexscaves_1010_raygun_network_abi_probe.py)
seleciona três métodos nativos de `ACNetwork.class`:

- `registerMessages`: registro de mensagens — exige referência binária direta a `UpdateItemTagMessage`;
- `registerPayloads`: interface do registro de payloads;
- `lambda$registerPayloads$0`: callback que referencia o contexto de payload.

A coleta confere o JAR publisher exato, SHA do `UpdateItemTagMessage.class` selado
no receiver, classe JVM major 65 e digests por método; publica somente
descritores, offsets e janelas reduzidas de símbolos ABI. O
[workflow dedicado](../../.github/workflows/alexscaves-1010-raygun-network-abi.yml)
executa regressões sintéticas e a inspeção real Java 21.

**Resultado da auditoria direcionada no JAR exato:** a [execução 41333238689](https://github.com/Gustavaopere/Black-Arcana/actions/runs/41333238689) concluiu com sucesso. O `ACNetwork.class` observado tem SHA-256 `8544a3436444be3248f9176bbcdee5fa30ee45ec2fbcf7a35a5e4fe4d9d88482` e oito métodos declarados. Os fatos compilados foram selados no [manifesto de ABI JVM](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-RAYGUN-NETWORK-ABI-1.0.10.json); novos CI devem comparar SHA, três digests de métodos, descritores e sete âncoras críticas, rejeitando qualquer alteração.

| Método | Âncora JVM real | Conclusão estritamente apoiada |
| --- | --- | --- |
| `registerMessages()` | `ldc UpdateItemTagMessage @151`, seguida por `register(Class,BiConsumer,Function,BiConsumer) @168` | Existe entrada nativa da mensagem na tabela de `ACNetwork`; os três lambdas adjacentes pertencem ao registro, sem prova independente de autorização por remetente |
| `registerPayloads(RegisterPayloadHandlersEvent)` | `registerMessages @0`, `registrar @12`, `PayloadRegistrar.playBidirectional @22` | O provider registra **um payload/envelope NeoForge bidirecional**; não confundir com registro isolado de `UpdateItemTagMessage` por `playBidirectional` |
| `lambda$registerPayloads$0(ACPayload,IPayloadContext)` | `ACNetwork$NeoForgeContext.<init> @24`, `ACNetwork$Entry.handle @27` | O callback do envelope encaminha a mensagem por uma entrada nativa usando um wrapper de contexto |

**Interpretação de segurança:** `playBidirectional` descreve a direção permitida do envelope registrado. Não comprova que um `entityId` de mensagem individual esteja vinculado ao remetente, que `ChargeUsed`/`UseTime` sejam saneados ou que qualquer alteração de `CUSTOM_DATA` seja legítima. Também não autoriza declarar vulnerabilidade explorável sem reprodução e análise de contexto. `NO_MUTATION`, `NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED` permanecem.

**Escopo:** `ABI_REFERENCE_OBSERVED_ONLY`. Uma chamada simbólica a
`registerMessages` ou a uma classe de payload não basta para confirmar
direção registrada do canal, threading, validação do remetente,
persistência ou segurança da atualização de `CUSTOM_DATA`. Apenas
evidência exata dos opcodes e revisão do contexto permite melhorar RN-02
e RN-03, sem automaticamente homologar perks. Um snapshot SHA-exato, quando
publicado, deve ser revalidado pelo mesmo workflow.

## Auditoria da identidade do receptor (PR #995)

O [probe read-only de identidade](alexscaves_1010_raygun_receiver_identity_probe.py)
com [manifesto SHA-exato do contexto/receptor](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-RAYGUN-RECEIVER-IDENTITY-1.0.10.json)
(pin de quatro classes, seis métodos, nove desvios e sete âncoras; 14 regressões sintéticas em CI)
confirma, em execução Java 21 no publisher JAR SHA-exato 1.0.10, o
`UpdateItemTagMessage.handle` previamente selado, seu contexto
`ACNetwork$NeoForgeContext` e o dispatch do
`ACNetwork$Entry`. Evidência de [execução real em CI](https://github.com/Gustavaopere/Black-Arcana/actions/runs/41334822025).

| Componente nativo | Evidência exata do bytecode | Limite da conclusão |
| --- | --- | --- |
| `ACNetwork$NeoForgeContext.getSender` | Invoca `IPayloadContext.player @4`; testa `instanceof ServerPlayer @11` e `ifeq @14` | Resolve o player de contexto quando é servidor; não vincula automaticamente esse player ao `entityId` arbitrário presente no payload |
| `ACNetwork$NeoForgeContext.isClientSide` | `IPayloadContext.flow @4` seguido de `PacketFlow.isClientbound @9` | Define o lado lógico conforme fluxo; não comprova que campos de mensagem estejam autorizados |
| `ACNetwork$NeoForgeContext.enqueueWork` | `IPayloadContext.enqueueWork @5` | Um helper oferece enfileiramento; o seu uso efetivo pelo Raygun precisa ser provado no call graph |
| `ACNetwork$Entry.handle` | `BiConsumer.accept @6` | Dispatch nativo da tabela; não é validação semântica da tag |
| `UpdateItemTagMessage.handle` | Nove desvios JVM em `@20, @31, @50, @84, @97, @116, @131, @146, @161`; branch de escape até `@179` em vários caminhos | São guardas compilados do handler, não evidência de QA física nem autenticação de cada identificador/valor |

**Decisão técnica:** o contexto usa o player provido por
`IPayloadContext` e a direção real do fluxo, mas é
necessário reconstruir os dados que atravessam `getSender`,
`Level.getEntity` e `UpdatesStackTags.updateTagFromServer`.
Uma validação de tipo de item e presença de tag não basta para confirmar
ownership do alvo, saneamento de `ChargeUsed` /
`UseTime` ou proteção contra replay.
O envelope e o contexto do provider são observados estaticamente;
**nenhuma vulnerabilidade é afirmada** sem análise dos caminhos externos,
reprodução controlada e avaliação de permissões. O Black Arcana mantém
`NO_MUTATION`, sem hooks mutadores ou QA física presumidos.

## Fluxo normal de entidade, mãos e tag — selo da PR #996

O [manifesto de CFG exata do receptor](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-RAYGUN-RECEIVER-CFG-1.0.10.json)
e o [probe read-only](alexscaves_1010_raygun_receiver_cfg_probe.py) acrescentam
a auditoria intra-método do `UpdateItemTagMessage.handle`, selada contra os
dois manifestos anteriores de receiver e identidade.
O levantamento utiliza o JAR publisher 1.0.10, SHA-256 da classe e digest do
método. Os desdobramentos abaixo são limitados a callsites/operandos JVM:

| Recorte | Observação compilada | Limite |
| --- | --- | --- |
| Remetente e fluxo | `ACNetworkContext.getSender @8`; `isClientSide @15` | O caminho de servidor usa o player do contexto, mas o player obtido não demonstra por si autorização de `entityId` |
| Entidade informada | **`getfield entityId:I @39`** seguido de `Level.getEntity(I) @42`; `instanceof LivingEntity @47` | Lookup do ID recebido no nível da entidade/player escolhido. Não foi demonstrada equivalência entre entityId e remetente |
| Item informado | **`getfield itemStackFrom:ItemStack @60`**; depois lookup do item nas mãos e `ItemStack.is(Item) @81/@113` | As chamadas de comparação são de **tipo de item**. Correspondência de classe não estabelece identidade de `ItemStack`, autorização da posse ou proteção contra troca de mão |
| Item resolvido | `getItemInHand` nas mãos principal/secundária; `instanceof UpdatesStackTags @143` | Há seleção de stack atual e teste de interface, mas o método não comprova autorização do conteúdo da tag |
| Atualização | `ACCompat.getTag @158/@171` e chamada `UpdatesStackTags.updateTagFromServer @174` | O setter nativo de `CUSTOM_DATA` já foi selado separadamente. Nada aqui demonstra saneamento de `ChargeUsed`/`UseTime` |

**Origem dos operandos da atualização — verificação adicional do JAR:**
o campo `itemStackFrom` é lido em `@60` e armazenado
no **slot 5 em `@63`**. A seleção nativa de mão principal
(`getItemInHand @92`) armazena a stack em
**slot 6 em `@95`**; a seleção alternativa
da mão secundária armazena a stack no **slot 6 em `@127`**.
No caminho de atualização, `@156 aload 5`
alimenta `ACCompat.getTag @158` (checagem de presença).
Em `@167 aload 6` é passada a stack
selecionada; `@169 aload 5` alimenta
`ACCompat.getTag @171`, cujo retorno vai
para `UpdatesStackTags.updateTagFromServer @174`.
Os **nove vínculos locais de origem/destino** são conferidos junto
das 17 âncoras nativas pelo manifesto e testes.

**Implicação de interoperabilidade:** o `CompoundTag`
recebido pelo método de atualização provém da stack
**transportada no pacote**; a stack modificável é a selecionada
**na entidade resolvida**. Identificar as duas origens ajuda a
desenhar um adaptador seguro, mas não demonstra validação dos
campos, autoria nem que esse fluxo possa ser alterado por perks.
Não foi executado teste físico nem ataque controlado.

No grafo de fluxo **normal intra-método** (sem exception edges,
despacho interprocedural ou análise formal de valores), as referências a
`getSender @8`, `entityId @39`,
`Level.getEntity @42`, `itemStackFrom @60`
e `updateTagFromServer @174` dominam o ponto de
atualização, enquanto a chamada alternativa `ItemStack.is @113`
não o domina. **Dominância de instruções não constitui validação
de origem, identidade, permissões nem proteção contra replay**.

O [workflow SHA-exato](../../.github/workflows/alexscaves-1010-raygun-receiver-cfg.yml)
compara branch targets, hashes, acessos de campo e 17 âncoras de ABI
com o manifesto selado. Sem certificado de sete eixos: `NOT_CERTIFIED`,
`NO_MUTATION`, `mutating_hook=NOT_VERIFIED` e
`physical_qa=NOT_TESTED`. Nenhum exploit
é alegado sem análise mais ampla e reprodução controlada.

## Codec nativo de `UpdateItemTagMessage` — prova do wire format 1.0.10

O [manifesto SHA-exato de codec](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-RAYGUN-PACKET-CODEC-1.0.10.json) é reproduzido pelo [probe read-only](alexscaves_1010_raygun_packet_codec_probe.py) no JAR publisher instalado 1.0.10, comparado com as evidências anteriores do receiver/CFG. Os quatro métodos compilados da mensagem (`UpdateItemTagMessage`, `read`, `write`, `handle`) estão selados por descritor e hash de método, com **nove referências ABI de codec**.

| Fronteira nativa observada | Referência JVM | Implicação permitida |
| --- | --- | --- |
| Construtor | `putfield entityId @6`; `putfield itemStackFrom @11` | Estrutura de dois campos da mensagem |
| Leitura de ID | `FriendlyByteBuf.readInt @5` | Identificador serializado como inteiro; não há prova de vínculo com remetente |
| Leitura de stack | `PacketBufferUtils.readItemStack @9` | Stack reconstruída a partir de buffer de rede; integridade e NBT continuam sem avaliação semântica |
| Escrita de ID | `getfield entityId @2`; `FriendlyByteBuf.writeInt @5` | A mensagem envia o valor de ID armazenado, sem comprovar autorização |
| Escrita de stack | `getfield itemStackFrom @11`; `PacketBufferUtils.writeItemStack @14` | A mensagem envia stack via helper do provider; a validação dos campos não foi demonstrada |

O `PacketBufferUtils` observado está sob o namespace `com.github.alexmodguy.alexscaves.citadel`; isso comprova apenas o símbolo compilado usado pela mensagem, não a validação/limites de leitura da tag dentro do helper. Em particular, o wire format **não** demonstra `entityId == sender.getId()`, identidade do stack, validação de `ChargeUsed` / `UseTime`, whitelist de NBT, threading ou proteção contra replay. Esses critérios exigem análise semântica adicional do helper/handler e testes direcionados.

**Gate mantido:** `NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`. A auditoria não altera nem endossa mecanismos nativos, não afirma exploit e não promove qualquer índice, Stage ou contrato de perk.
## Implementação exata do helper de ItemStack — versão sombreada no JAR 1.0.10

Reavaliado o callsite `PacketBufferUtils.readItemStack` que aparece em `UpdateItemTagMessage.read`. O [novo manifesto SHA-exato](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-RAYGUN-ITEMSTACK-HELPER-1.0.10.json) fixa `com/github/alexmodguy/alexscaves/citadel/server/message/PacketBufferUtils.class` (SHA-256 `3f203404344653e77167846c967635f930f84cad355f60b084358f826c7ae3db`), os métodos `readItemStack(ByteBuf)` e `writeItemStack(ByteBuf,ItemStack)` e sete callsites simbólicos. Cada método tem **seis instruções de bytecode e zero branches locais**.

| Método no JAR instalado | Operações selecionadas | Limite da evidência |
| --- | --- | --- |
| `readItemStack` | `ItemStack.OPTIONAL_STREAM_CODEC @0`, cast para `RegistryFriendlyByteBuf @4`, `StreamCodec.decode @7`, cast para `ItemStack @12` | A leitura é delegada ao codec opcional **do Minecraft**; não há validação NBT própria nesse método de helper, e o comportamento interno do codec não foi auditado aqui |
| `writeItemStack` | `ItemStack.OPTIONAL_STREAM_CODEC @0`, cast para `RegistryFriendlyByteBuf @4`, `StreamCodec.encode @8` | A escrita também é delegada ao codec opcional do Minecraft; não há prova de saneamento de dados do Raygun nessa delegação |

A ausência de branches nesses dois métodos específicos **não** implica ausência de controles dentro do `OPTIONAL_STREAM_CODEC`, da camada NeoForge, nem do processamento posterior. Os limites efetivos de bytes/componentes/NBT, o tratamento de dados malformados, o vínculo sender–`entityId` e a autorização de `ChargeUsed`/`UseTime` continuam não verificados. O cast exige um buffer compatível em execução, mas a auditoria estática não substitui um teste de sessão real.

A verificação automatizada pelo [workflow do helper](../../.github/workflows/alexscaves-1010-raygun-shaded-itemstack-helper.yml) cruza o SHA do publisher com o manifesto do pacote anterior, hashes nativos de classe e métodos, os sete callsites e as proibições de promoção. Aplicar `NO_MUTATION` e manter `NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED` e `physical_qa=NOT_TESTED`.

## Aceite antes de concluir contrato estático Raygun

| Gate | Evidência necessária | Estado atual |
| --- | --- | --- |
| RN-01 | JAR exato + SHA de classes e métodos pertinentes; conflito entre manifestos falha | ✅ descoberta SHA-exata passou no head final da PR #993; traçado dirigido pendente |
| RN-02 | Identificar no binário a inscrição efetiva do tipo de mensagem, direção e handler, sem inferir da classe sender | ⚠️ registro de entrada `UpdateItemTagMessage` e envelope `playBidirectional` comprovados; direção do wrapper observada, autorização de mensagem individual não verificada |
| RN-03 | Verificar semântica de threading e as condições de leitura/edição de estado no receiver | ⚠️ `IPayloadContext.enqueueWork` e `flow/isClientbound` selados estaticamente; threading do handler e update de stack ainda não verificados |
| RN-04 | Confirmar integridade de `entityId`, item, hand swap, `ChargeUsed`/`UseTime` e limites de `CUSTOM_DATA` | ⚠️ offsets/CFG exatos identificam campos de origem e comparação por tipo de item; **binding remetente–entityId, sanitização e replay continuam NOT_VERIFIED/NOT_TESTED** |
| RN-05 | Vincular cobrança nativa, alvo, dano, status e retorno de `hurt` a uma identidade causal única | ⚠️ parcial nos manifestos anteriores |
| RN-06 | Verificar migração/salvamento, reconexão, multiplayer e casos negativos no cliente + servidor dedicado | ⚠️ QA física não testada |
| RN-07 | Certificar os sete eixos de evidência estática num manifesto com hash de fichas e em CI antes de mexer nos índices | ⚠️ não certificado |

**Nenhum campo** de RN-02 a RN-07 deve ser promovido por a coleta RN-01
terminar com CI verde. O probe serve de entrada técnica para fechamento
posterior, não substitui uma revisão semântica dos callsites.

## Segurança da integração

Até contrato seguro do provider (inclusive autorização real e limites de
atribuição/targeting) e homologação apropriada, aplicar **`NO_MUTATION`**.
Não alterar `ChargeUsed`, `UseTime`, `CUSTOM_DATA`, dano, raio, tempo,
aplicação de Irradiated nem o fluxo C2S por perks. Manter
`NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED` e `physical_qa=NOT_TESTED`.
Nenhuma raiz mágica, ficha certificada, porcentagem ou Stage é promovido aqui.
