# Astral Transferring 1.0.10 — contrato individual SHA-exato

A [ficha individual](enchantments/astral-transferring.md) conclui somente `alexscaves:astral_transferring` como **`STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`**. O [manifesto individual](EXACT-ASTRAL-TRANSFERRING-CONTRACT-1.0.10.json) sela dados publicados, janelas causais do consumidor, os demais corpos declarados do Totem e auxiliares selecionados de tags, serialização, mensagem e mixins. `onUseTick` e os inicializadores compartilhados de registros/configuração continuam **PARTIAL**. A conclusão individual delimita o comportamento estático descrito, sem promover o Totem, seus encantamentos irmãos ou o provider integralmente. `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, **`NO_MUTATION`**. Transferir o vínculo durante a possessão nativa acrescenta **zero raízes mágicas** às oito existentes.

A autoridade é o publisher CurseForge projeto `1645389`, arquivo `8856293`, `alexscaves-1.0.10-neoforge+1.21.1.jar`, **75.279.314 bytes**, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 **`36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`**. O TOML empacotado declara `alexscaves` **1.0.10**, para Minecraft 1.21.1 / NeoForge / Java 21. A fonte pública [`Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37`](https://github.com/Codx-org/AlexsCavesContinued/tree/523308608422ab8e31974befa7111ecdf495dd37) declara **1.1.1**: serve como corroboração adjacente, sem provar paridade de build. Os valores deste contrato vêm do JAR publisher 1.0.10, sem nova auditoria da engine base ou execução do jogo transformado.

O recorte contém **1 ficha, 10 classes, 13 recursos, 50 métodos e 1.045 âncoras**: **46 corpos completos / 773 instruções** e **quatro corpos PARTIAL / 272 âncoras**. Os **22 métodos declarados do Totem** estão identificados: **21 corpos completos / 502 instruções** e `onUseTick` com **254/478 instruções**, somando **756 âncoras** do Totem. Os demais métodos selam contexto selecionado de helpers/mensagem/mixins e registro/configuração. Os caminhos de classe abaixo partem de `com/github/alexmodguy/alexscaves/`.

| Artefato local selado | Bytes | SHA-256 |
|---|---:|---|
| [`enchantments/astral-transferring.md`](enchantments/astral-transferring.md) | 25.470 | `7355cb82745b9f41c0f79d30209c6cfc45b9be857f3adb32415414753292fd8b` |
| [`EXACT-ASTRAL-TRANSFERRING-CONTRACT-1.0.10.json`](EXACT-ASTRAL-TRANSFERRING-CONTRACT-1.0.10.json) | 206.346 | `322d3926e7771007c5b52df1461fd23ad27572806ea9af0991ef1d9b2a159bfc` |

| Classfile | Métodos | Âncoras | SHA-256 da entrada completa |
|---|---:|---:|---|
| `server/item/TotemOfPossessionItem.class` | 22 | 756 | `bad9dd8b88eb621b558d1ede477d2b4ba6a21befdec31b4a0233adcac701773e` |
| `server/misc/ACCompat.class` | 13 | 98 | `333738f324e6e9d77a488e14b7e81b169c2b2d4f6db5171206a016ad0271f57b` |
| `server/misc/ACPlatform.class` | 1 | 5 | `662a4d2593fe515ed8790bad06d8184d1eb921423033dfd11b3b44142dedc3e6` |
| `server/message/UpdateItemTagMessage.class` | 4 | 102 | `bda52d12e8cce7e010b3d4cd2db7d83000e78b35657c55773a8ba91a070478c8` |
| `server/item/UpdatesStackTags.class` | 1 | 4 | `1ba03e1d244a0a6ad49a888cb406bf518858c52988b4210db204c0bbd1e6e0ad` |
| `mixin/IllagerMixin.class` | 2 | 19 | `e0a1238a15f9b9e28da425afbe5eb77eef9398d8833dcda143f7b8d4bab9aa85` |
| `mixin/LivingEntityMixin.class` | 2 | 33 | `be00e16d63ca7aa3f79da91af47560b6397fe6b9b86d95148dfeb78d481cdc01` |
| `server/enchantment/ACEnchantmentRegistry.class` | 2 | 9 | `60006fab1b3b29f5f93c8365416815a12770cf8877a059298cb4ee82f7a92f32` |
| `server/item/ACItemRegistry.class` | 2 | 9 | `114e4a3576d56cb66d240fa9df9db7693b1df576ebfa86631ef751dd1e7b5bb1` |
| `server/config/ACServerConfig.class` | 1 | 10 | `67abf51943537e735a08c268607ca08901c2b197f0b278fa4b464887d40ea129` |
| **Total selecionado** | **50** | **1.045** | — |

Os hashes de classe identificam entradas completas do JAR; não ampliam a cobertura de métodos/instruções. Os recursos abaixo são entradas completas. Seus valores efetivos ainda dependem da composição externa do pack.

| Recurso empacotado | Bytes | SHA-256 da entrada completa |
|---|---:|---|
| `META-INF/neoforge.mods.toml` | 1.066 | `54dfb8cdba886fd5ef8e64d2a51c487ce4bf2400995884937ee5fd6d89df68fa` |
| `assets/alexscaves/lang/en_us.json` | 121.372 | `a2a3fab567b07ec10b3d946d4e4ce3e65417b6f9348bd49478d8a253a4232d1f` |
| `assets/alexscaves/lang/pt_br.json` | 84.238 | `080bfaf05b6d710383579dfd0d3c01443f9fa873b0c697f5e6ee0740931018a7` |
| `data/alexscaves/enchantment/astral_transferring.json` | 379 | `41133c10af9c9e8d5e33d1b8339b734f81547b141f83fc0144aa9cf89f1f04c2` |
| `data/alexscaves/enchantment/detonating_death.json` | 439 | `8402461954ff5b249ae675b51d7dcc23d933b2b06c494b327bf608371298646e` |
| `data/alexscaves/tags/item/enchantable/totem_of_possession.json` | 59 | `185a085206993877d91ca6d8c697273c14f945b1d55cb6179e3236c138c357cf` |
| `data/alexscaves/tags/entity_type/resists_totem_of_possession.json` | 287 | `6ae5d98cd4b12739d3d1d7dc78d37053b2e5b0eb3b1093e3f8a9a6d9768df209` |
| `data/alexscaves/recipe/totem_of_possession.json` | 415 | `66abfc1425daee7e89b87f145c4148747a00a29fd45b96222869783e42ed710b` |
| `data/minecraft/tags/enchantment/in_enchanting_table.json` | 1.631 | `6472c976d755f1481506f3f113368081aa487eaff3ce977a1f7c93a400f39bb1` |
| `data/minecraft/tags/enchantment/non_treasure.json` | 1.631 | `6472c976d755f1481506f3f113368081aa487eaff3ce977a1f7c93a400f39bb1` |
| `data/minecraft/tags/enchantment/on_random_loot.json` | 1.631 | `6472c976d755f1481506f3f113368081aa487eaff3ce977a1f7c93a400f39bb1` |
| `data/minecraft/tags/enchantment/tradeable.json` | 1.631 | `6472c976d755f1481506f3f113368081aa487eaff3ce977a1f7c93a400f39bb1` |
| `alexscaves.mixins.json` | 5.312 | `6e120e2d2cf226a25cbe3d0605968a184384194354eac0b1153108f74632c140` |

A tabela de métodos combina o roster selecionado com o fingerprint de cada corpo **integral**. As assinaturas/descritores JVM exatos constam no manifesto. O fingerprint usa JSON UTF-8, `ensure_ascii=False`, `sort_keys=True`, `separators=(',',':')`, do objeto **`{owner,name,descriptor,instructions}`**, com `owner` como caminho de classfile e linhas completas `{offset,opcode,operand,symbol}` em ordem crescente. É um digest deste normalizador, distinto dos digests do parser histórico e do hash do classfile. Para os quatro corpos PARTIAL, incluir instruções omitidas no fingerprint apenas identifica o corpo; não as transforma em evidência selecionada.

| Classe / método | Selecionadas / nativas / omitidas | SHA-256 normalizado do corpo integral |
|---|---:|---|
| `TotemOfPossessionItem.<init>()` | 36/36/0 | `66e5a2e0811daa41cc08c6e08a36ff0b85f3276dcfaeb729c3e5ede56dd99550` |
| `TotemOfPossessionItem.getEnchantmentValue` | 2/2/0 | `95e4f2678888187ebee41052931d625d5cedf57d5813671604b771db05ccf4d9` |
| `TotemOfPossessionItem.isEnchantable` | 8/8/0 | `b7ec5ccee502514ff2f11861da5be05733376b76989bf11590a0ca42a83bbd96` |
| `TotemOfPossessionItem.use` | 66/66/0 | `2ea3020538311780b38d871be2108511fb3a37022252b9c65f9c4e265330de77` |
| `TotemOfPossessionItem.releaseUsing` | 29/29/0 | `90b104ae1d7090a6f2b0436497f62a4c9a656cf194939f3532f3f0a8cb40a50b` |
| `TotemOfPossessionItem.onUseTick` | **254/478/224, PARTIAL** | `8c294569f9123b88a02553c9be4a1a8a927c266f814b871e65ad9b92329a0863` |
| `TotemOfPossessionItem.getUseAnimation` | 2/2/0 | `a8b4e3e554771147f5fa8d56c4fbad76e1d5e61ab846bd8df1ac6cec028ce79b` |
| `TotemOfPossessionItem.getUseDuration` | 2/2/0 | `2a026c299a362700ee69b70291f2f80bbba36140dbb2ea08a5b01b9e3f17292a` |
| `TotemOfPossessionItem.acModifiers` | 8/8/0 | `45135cc74f0030482ca992bcc79718d3bca2402e6b98581ce324d173279b5790` |
| `TotemOfPossessionItem.getDefaultAttributeModifiers` | 8/8/0 | `ad73046dd80b755e0a89897505ba5f028bb223186c17f2872c1066d380555c4e` |
| `TotemOfPossessionItem.resetBound` | 16/16/0 | `9febbdd3ea863d18035859b315b02dd24254b0e59342319850a1173325096c03` |
| `TotemOfPossessionItem.appendHoverText` | 37/37/0 | `ccd784c2c444885e2cf62ddb5313df942f1204631a69415b9e8f8b5ab76e9b1f` |
| `TotemOfPossessionItem.getBoundEntityUUID` | 17/17/0 | `6efe4835d113732efb588c2a0da962816867a459cef7b89d3e7d0c2d724ed08c` |
| `TotemOfPossessionItem.updateEntityIdFromServer` | 49/49/0 | `66ce23a0c1683f643eaded82d209f215ce7252616274b737c0aba93615a3530e` |
| `TotemOfPossessionItem.getControlledEntity` | 44/44/0 | `6e71e9bb9ac2421ed61db7f2fa28c9c4af90ec88c50670f9111dd9b58d40b93f` |
| `TotemOfPossessionItem.isEntityLookingAt` | 70/70/0 | `709b2a6f62d5201111c3987716376cbd0ee90eec3168342c7b2521162dad72d7` |
| `TotemOfPossessionItem.isBound` | 7/7/0 | `75290bc794055efe45b380730a654a00959b8acd5663f9605e46525fa08d2306` |
| `TotemOfPossessionItem.hurtEnemy` | 6/6/0 | `2fd2218f0434370e6a6b544f6db2729b9b0bd08e56e4d5b108d90b962ce2781d` |
| `TotemOfPossessionItem.acHurtEnemy` | 64/64/0 | `248a7be65bf45a71f854f6b5a80a6d30d14f24cff9610669320b05a10aad9b00` |
| `TotemOfPossessionItem.setPossessed` | 16/16/0 | `3f84fee7bf99f56c1812ebc43e365bdf73dd086b028e0e889190bd0e7973eac2` |
| `TotemOfPossessionItem.lambda$getDefaultAttributeModifiers$1` | 4/4/0 | `b88dc1fbfad7942caf0418b0b4553a87e4bd603a720c3c869f9c6a05b6fd1751` |
| `TotemOfPossessionItem.lambda$onUseTick$0` | 11/11/0 | `4c89c4788e0645f48fccd2c94be95c47f350eaac24eb677d2c7d916b06d3d019` |
| `ACCompat.getTag` | 12/12/0 | `ed54484beb5dcf23176b20a752b8620897193509f897c3c917d004d46ae2347e` |
| `ACCompat.getOrCreateTag` | 14/14/0 | `34d32986e34c6c8e649e59c81cba84f9bd571486179cdb7fdad04e0a075d71bd` |
| `ACCompat.setTag` | 14/14/0 | `e8f70228c61359a5ce1e687f588f6929c31edc12c2a2846b258725381c358006` |
| `ACCompat.enchantLevel` | 24/24/0 | `b4dddfa6748810de27f35ac6fa8be385fb913c992c9248e1b93f64ccbee79ed0` |
| `ACCompat.getBoolean` | 4/4/0 | `c1bd7e403909b9f0cfbe5b5ccf21eaf8cc70b54f7edfb9666cd0e1ddb0a280bf` |
| `ACCompat.getInt` | 4/4/0 | `bc04cc936088f7dbc5a542670d00c1652f95a9ebd072d8cd3670b8a835633ca1` |
| `ACCompat.getUUID` | 4/4/0 | `f7def6409e62b0ccdb9cda94c0536e9cae7160559be6efb37af978155cbe343b` |
| `ACCompat.putUUID` | 5/5/0 | `b682a67886ab5eed794adcd637c9d6964403ce5cf856c25e0e1beb4103bb19ee` |
| `ACCompat.getPersistentData` | 3/3/0 | `c7a996562abd0ecda3cedd5104783ab237362f06fa37ebbb3dbfb34dcf292760` |
| `ACCompat.useConsume` | 3/3/0 | `9f1fb2e55495cef2fe4e9bd58ac824f17793c714fbc45a5009b05ab6847935fc` |
| `ACCompat.usePass` | 3/3/0 | `dd0293b7d3bafdfece3f5160943bface068ab9d07430f0143d1c711cc34c441a` |
| `ACCompat.entityTypeFrom` | 3/3/0 | `86402ecfd590742322d29400e32ff0dc8b186c3947bc5b0b2fd3e057a50bb253` |
| `ACCompat.displayClientMessage` | 5/5/0 | `2fe94224bca28ea02a88fa1129a74db640b920c823811bdd2190010b6f394ddf` |
| `ACPlatform.serializeEntity` | 5/5/0 | `ed6da4ee3262af1b33b02a7f1feff6dcd4bbbf15cf3250d210ecb734dae02b04` |
| `UpdateItemTagMessage.<init>(int,ItemStack)` | 9/9/0 | `b86216606b9f743f3081210f1d773fe9908f72c371f0025193c872030588d1e9` |
| `UpdateItemTagMessage.read` | 8/8/0 | `d086920c0d29c37f72939c7e48410ec7df74131dcbff9c0b3243ff0f90c96156` |
| `UpdateItemTagMessage.write` | 10/10/0 | `1f8b22ffe54cca0d075153df0e378ff37a64e063490792372eb24b3f3c102011` |
| `UpdateItemTagMessage.handle` | 75/75/0 | `244ab8d4c854d443cc272c710f28fad0a7cd07f0b4eaf07f7148f51e2d561d65` |
| `UpdatesStackTags.updateTagFromServer` | 4/4/0 | `88647266c5c7e1b9b87f513bded4dbc1d8d876a9a633b0899c387ef18ea7b019` |
| `IllagerMixin.ac_isAlliedTo` | 14/14/0 | `d4dbf795788e865246917a038f7dd770e8508f33d3904a12759461a776e395f8` |
| `IllagerMixin.isPossessed` | 5/5/0 | `30aa935db051b3f7d55632d092ef4836b03902c58b37fb35b4ce67f2b5bca694` |
| `LivingEntityMixin.ac_onSetLastHurtByMob` | 28/28/0 | `e67ea46502ec2c61c767a13a2575246db54ee0727674126b6aff8af121cf97f0` |
| `LivingEntityMixin.isPossessed` | 5/5/0 | `ff4655d1fb9c55ba2c6aba9131f7a9ebb5d161b833784a5ea4979a3dc20be038` |
| `ACEnchantmentRegistry.key` | 6/6/0 | `a799dcf53ccb63505688c2c16882adb617d91613c6f677fdc0fe03dffc462f35` |
| `ACEnchantmentRegistry.<clinit>` | **3/182/179, PARTIAL** | `1ba929dc075622139847f3388c5d9a5b946d20088a59c3e242aeb8164879ebd0` |
| `ACItemRegistry.lambda$static$126` | 4/4/0 | `68bcc44ec91645b292beef9adb590fc63b32f0be11f2905c0647cadecfc286f3` |
| `ACItemRegistry.<clinit>` | **5/1382/1377, PARTIAL** | `9c28d234b1512f04688b1b8231966f5bad8872f3b3fbeca88be5f25758359b39` |
| `ACServerConfig.<init>(Builder)` | **10/502/492, PARTIAL** | `eff3f7d75813a883c95508be44b8012f492339047435ff1096137eeca62ff8d1` |

| Janela de `TotemOfPossessionItem.onUseTick` | Âncoras | Fronteira selada |
|---|---:|---|
| `0–39` | 19 | Resolução do controlado original; gates iniciais de vínculo, existência, vida e dano |
| `106–284` | 83 | Limpeza/stop/sync, visão/Player, desgaste no cliente e definição do tempo decorrido |
| `651–655` | 3 | Guard de lado que desvia ao servidor |
| `714–1084` | 149 | Saída do cliente; consulta e loop inteiros; transferência e alternativa Player |
| **Total** | **254/478** | **PARTIAL; 224 instruções omitidas** |

As regiões omitidas de `onUseTick` são **`41–103`** (construção/execução de Detonating Death e seu desvio condicional), **`286–648`** (ramp/navegação/movimento) e **`658–711`** (partículas). O inicializador de encantamentos seleciona somente **`347,350,353`**; o de itens, **`2310,2313,2316,2321,2324`**; o construtor de configuração, **`668–686`** (dez instruções). Os quatro corpos PARTIAL somam **272 selecionadas / 2.544 nativas / 2.272 omitidas**. Arestas podem entrar/sair de regiões omitidas; o roster histórico de branches é um cross-check separado, sem tornar estas janelas um CFG fechado ou executado. Os limites genéricos de **256 âncoras por método** e **8.192 por manifesto** permanecem preservados.

O censo fresh percorreu **1.555 classfiles**, interpretando o `Fieldref` exato **`ACEnchantmentRegistry.ASTRAL_TRANSFERRING:Lnet/minecraft/resources/ResourceKey;`**; encontrou somente `ACEnchantmentRegistry.class` e `TotemOfPossessionItem.class`. O registro liga literal **`astral_transferring@347`**, `key@350` e `putstatic ASTRAL_TRANSFERRING@353`; o reader direto está em **`onUseTick@920–923`**. Isso delimita referências diretas no publisher, sem excluir reflexão, mixins, transformadores ou consumidores externos. O censo separado de constantes `TotemPossessed` encontra o Totem e os dois mixins descritos adiante; não é confundido com um scan de `Fieldref` de campo.

O registro do item liga o literal **`totem_of_possession@2313`**, o invokedynamic de supplier **`@2316`**, o registro **`@2321`** e `putstatic TOTEM_OF_POSSESSION@2324`. O bootstrap **131** aponta a **`lambda$static$126`**; seu corpo completo de quatro instruções cria `TotemOfPossessionItem`. O helper completo `ACEnchantmentRegistry.key` cria a chave no namespace `alexscaves`. Essas ligações identificam item e encantamento, sem cobrir integralmente os inicializadores compartilhados.

O texto inglês publicado é **“Astral Transferring”** / **“Mobs possessed by the Totem of Possession can swap possessed status with other, healthier mobs they fight”**. O `pt_br.json` contém o nome do Totem, mas não contém nome nem descrição deste encantamento; a redação técnica em português da ficha é uma paráfrase. A descrição literal precisa ser lida com os gates compilados: o caminho Astral parte de um **Mob controlado**, exige candidato `LivingEntity` e não possui ali exclusão universal de Player.

O JSON próprio tem **379 bytes**, SHA-256 `41133c10af9c9e8d5e33d1b8339b734f81547b141f83fc0144aa9cf89f1f04c2`: máximo **I**, peso **2**, custos mínimo `1+12(L−1)` e máximo `41+10(L−1)`, bigorna **4**, slot `mainhand` e suporte `#alexscaves:enchantable/totem_of_possession`. No nível I, os custos declarados são **1/41**. O recurso não contém `effects` nem `exclusive_set` próprios. O reader completo `ACCompat.enchantLevel` retorna o primeiro nível correspondente ou zero, sem clamp próprio ao máximo I e sem validar ali slot/tag. O consumidor exige somente nível **positivo**; I e níveis positivos forçados percorrem o mesmo ramo, sem chance, escala por nível ou benefício de nível II demonstrados.

A tag nativa de suporte contém somente `alexscaves:totem_of_possession`. As quatro tags `in_enchanting_table`, `non_treasure`, `on_random_loot` e `tradeable` contêm Astral; cada uma tem **1.631 bytes**, SHA-256 `6472c976d755f1481506f3f113368081aa487eaff3ce977a1f7c93a400f39bb1`. Isso documenta disponibilidade publicada, sem medir probabilidade de mesa, loot ou comércio. O scan dos **51 JSONs nativos de definição de encantamento**, separado das quatro tags de aquisição, encontra uma exclusão reversa: `detonating_death.json` menciona `alexscaves:astral_transferring` em seu `exclusive_set`. A ausência de exclusividade no JSON de Astral não elimina essa referência reversa. Dados efetivos, compatibilidade e níveis forçados dependem também de datapacks e mods.

A receita empacotada do Totem usa **`DED / DBD / DBD`**: seis `moth_dust`, dois `thornwood_branch` e um `occult_gem`, resultando em um Totem. O construtor completo declara durabilidade **1.000**, raridade de item **UNCOMMON**, modificadores de equipamento **+2** de dano e **−2.4000000953674316** de velocidade de ataque. `getEnchantmentValue()` retorna **1** e `isEnchantable(stack)` testa **`stack.count==1`**. São parâmetros do equipamento/aquisição, sem fórmula de dano de Astral nem custo por transferência. `getUseDuration` retorna **72.000 ticks** e `getUseAnimation` retorna **BLOCK**; essa duração declarada não garante possessão efetiva por 72.000 ticks.

O vínculo inicial é um caminho próprio: `hurtEnemy` delega a `acHurtEnemy`, cujo corpo completo consulta a resistência `@7–13` e, para Player, a configuração `@26–38`; só o caminho permitido chama `setPossessed(target,true)@71`, escreve UUID, serializa o alvo e confirma o `CUSTOM_DATA` do item `@135`. O método termina retornando `true` também depois do caminho de rejeição; esse retorno não é recibo de possessão aceita ou de dano. O contrato individual de Astral não transforma esse callback em cast separado nem certifica a liquidação do ataque herdado.

`use` atualiza o ID quando alcança o ramo servidor/`ServerLevel`, resolve a entidade e verifica vínculo/vida. A limpeza selecionada chama `setPossessed(entity,false)@75` e `resetBound(stack)@80` no servidor quando o vínculo está inválido. Para iniciar uso, exige entidade resolvida e o helper de visão com **`5D`**, ou nível positivo de Sightless; toca som e chama `startUsingItem`. `ACCompat.useConsume` e `usePass` somente produzem os respectivos `InteractionResultHolder`, sem `shrink` próprio. A assinatura/retorno de interação não constitui débito de inventário.

`onUseTick` resolve a entidade controlada **uma vez**, guardando-a no **local 5 `@6`**. As janelas de entrada/limpeza selam os gates de vínculo, existência, vida e dano do item e o encerramento `setPossessed(false)@109`, `resetBound@113`, `stopUsingItem@117`, com mensagem ao servidor somente no ramo cliente. A fronteira entre a âncora `@39` e a continuação `@106` omite `@41–103`, incluindo o desvio condicional `ifnull@41→106` e a região do encantamento irmão Detonating Death; a nova seleção não certifica a construção/explosão dessa região. Os caminhos gerais de interrupção não substituem uma limpeza transacional do vínculo anterior durante a transferência Astral.

A continuação exige o helper de visão ou Sightless e aplica o gate geral de Player/configuração: `instanceof Player@179`, leitura `totemOfPossessionPlayers@188`, rejeição até `stopUsingItem@204` quando false. O construtor de configuração selecionado define `totem_of_possession_works_on_players` com default publisher **true** em `@675–686`; a configuração carregada não foi observada. `isEntityLookingAt` tem corpo completo: ajusta o argumento por `1+0.1×distanceTo`, normaliza os vetores, testa um limiar de produto escalar dependente da distância e exige LOS. Portanto **`5D` não é raio de cinco blocos**, e LOS deste gate do usuário não pode ser transferida automaticamente a cada candidato da consulta.

O desgaste geral está em **`onUseTick@230–272`**: só quando **`timeLeft % 2 == 0` e `Level.isClientSide==true`**, aumenta `ItemStack.damageValue` em **1**; Player criativo pula o incremento. A paridade usa o **tempo restante**, enquanto a condição Astral usa o tempo decorrido. O corpo observado é um pedido de desgaste no **cliente**, sem débito autoritativo no servidor demonstrado e sem cobrança por transferência. A sequência de mensagens/tags é contexto de autoridade, sem provar liquidação física desse desgaste. Não converter durabilidade, peso, custo de mesa ou bigorna em mana, stamina, XP ou consumo por cast.

Em **`@275–284`**, o local 6 recebe **`elapsed = 72.000 − timeLeft`**. O gate Astral usa **`elapsed % 4 == 0`** (`iload@881`, `iconst_4@883`, `irem@884`, `ifne@885→1081`): é uma condição do contador deste uso, sem cooldown persistido, quatro segundos ou limite de uma transferência por intervalo comprovados. As regiões de ramp/navegação/movimento e partículas omitidas não definem o volume de transferência nem são promovidas por esta prova.

A divisão de lado está selada: **`Level.isClientSide@652; ifeq@655→717`** envia o ramo servidor à consulta; o trecho cliente termina por **`goto@714→1084`**. Assim, a consulta de candidatos, os pedidos de ataque e a sequência Astral a partir de `@717` estão atrás desse guard nativo de servidor. Esse fato local não certifica autenticação de pacote, ordem de handlers, código final transformado ou resultado aceito no servidor.

A consulta usa a **AABB da entidade originalmente controlada inflada em 3 por eixo** (`@717–725`) e `Level.getEntities` exclui a própria entidade recebida. É uma caixa de busca de candidatos, sem raio esférico, dano em área ou aumento de hitbox. O invokedynamic desta consulta usa bootstrap **1**, cujo method handle é `Entity.canBeHitByProjectile()Z`. O bootstrap **0** da consulta pelo vetor de visão corresponde ao helper completo `lambda$onUseTick$0(Entity,Entity)Z`: candidato apto a projétil e diferente da entidade capturada. São predicados de consultas distintas; a inspeção dos bootstraps não sela integralmente o caminho de movimento omitido que usa a consulta de visão.

O loop rejeita identidade com o controlado, **`controlled.isAlliedTo(candidate)`**, identidade com o usuário, **`candidate.isAlliedTo(controlled)`**, veículo compartilhado e entidade que não seja `LivingEntity` (`@788–850`). As duas direções de aliança são explícitas. Só o ramo em que o **controlado é `Mob`** (`@852–878`) chama `Mob.setTarget@871` e `setLastHurtByMob@878` e chega aos gates de Astral. Se o controlado é Player, segue a alternativa `Player.attack@1073` / reset do ticker, fora do ramo Astral. Esses pedidos de target/ataque não comprovam hit, dano aceito, morte ou crédito.

Depois do gate de módulo, lê a **vida atual do candidato `@890`** e a **vida atual do Mob original `@895`**; `fcmpl@898` / `ifle@899→1081` exigem candidato com vida **estritamente maior**, para valores normais finitos. Não compara vida máxima, nível, atributos ou raridade. Rejeita o candidato cujo tipo pertence a `RESISTS_TOTEM_OF_POSSESSION` (`@904–916`) e exige `ASTRAL_TRANSFERRING` de nível positivo (`getstatic@920`, `enchantLevel@923`, `ifle@926→1081`). Nesse ramo não há teste independente repetido da configuração de Player; o gate inicial e a interrupção em tick posterior não constituem autorização transacional para uma transferência a Player.

A tag de resistência publisher declara `#c:bosses`, `minecraft:warden`, `minecraft:armor_stand`, `alexscaves:hullbreaker`, `alexscaves:forsaken`, `alexscaves:atlatitan` e `alexscaves:tremorzilla`. A resolução de `#c:bosses` e alterações por datapacks continuam desconhecidas; a lista literal não é inventário final de entidades proibidas no modpack.

A sequência de troca chama **`setPossessed(candidate,true)@932`**, obtém tag copiada/nova do item, grava **`BoundEntityUUID@951`**, serializa o candidato por **`ACPlatform.serializeEntity@956`**, insere o `id` do tipo em **`@982`**, armazena **`BoundEntityTag@992`** e confirma o estado do stack com **`ACCompat.setTag@999`**. Pede o som `TOTEM_OF_POSSESSION_USE` e, somente para `ServerLevel` + usuário Player, chama **`updateEntityIdFromServer@1048`**. O helper de serialização tem cinco instruções e delega a `Entity.serializeNBT(entity.registryAccess())`; não é spawn, remoção da entidade ou confirmação de gravação em disco.

O salto **`goto@1081→766`** continua a iteração; não existe `break` após a primeira gravação e nenhuma comparação de menor distância. O **local 5 continua sendo a entidade original**, mesmo depois de trocar o UUID no item; portanto os candidatos seguintes ainda comparam saúde e usam o Mob original neste tick. A ordem da lista não é fixada aqui. Múltiplas gravações são possíveis no bytecode; múltiplas transferências aceitas no pack permanecem sem teste. Não declarar escolha do mais próximo, somente um candidato ou transação atômica.

O ramo Astral não contém débito próprio de mana/munição, escrita de cooldown ou chamada direta de `hurt`. Os calls de target e o caminho Player pertencem ao runtime nativo de ataque; esse limite local não prova custo global zero, dano zero ou ausência de trabalho em callbacks externos.

`setPossessed(Entity,boolean)` tem corpo completo de **16 instruções**, tolera null e escreve/remove **`TotemPossessed` nos dados persistentes da entidade**. A sequência local de transferência chama esse helper somente com **true** para o novo candidato, sem limpar ali o marcador do anterior. `resetBound` tem **16 instruções** e remove **`BoundEntityTag`**, **`BoundEntityUUID`** e **`ControllingEntityID` do item**, depois confirma a tag. Esse reset não remove por si o marcador de uma entidade. Os caminhos de limpeza gerais existem; não demonstram a transação `unset(old)→set(new)` no ramo Astral nem excluem limpeza externa. A persistência simultânea de marcadores é uma possibilidade inferida, sem bug físico reproduzido.

`ACCompat.getTag` e `getOrCreateTag` leem **`DataComponents.CUSTOM_DATA`** e retornam uma **cópia** do composto ou null/novo composto. A escrita posterior requer `setTag`, que usa **`CustomData.of(tag)`** ou remove o componente quando recebe null. `getPersistentData` delega ao estado da **entidade**; não é a mesma authority do item. Os helpers de UUID/int/boolean são leituras/escritas de `CompoundTag`, sem autenticação, ownership ou estabilidade pública de API próprios. Encontrar chaves e métodos chamáveis não autoriza mutá-los por perk.

`getControlledEntity` usa **`ControllingEntityID` numérico no cliente**, com sentinela **−1**, e **`BoundEntityUUID` resolvido no `ServerLevel` corrente no servidor**. `isBound` testa a presença de UUID; não prova entidade carregada/resolvida. `updateEntityIdFromServer` resolve o UUID, grava ID encontrado ou **−1**, confirma a tag e só chama **`sendMSGToAll` quando o ID anterior difere do novo**. A mensagem leva o ID do usuário e o stack. A sequência não prova entrega, destinatário correto, recuperação após unload/reload, continuidade entre dimensões ou persistência de IDs numéricos.

`releaseUsing` consulta a entidade atualmente resolvida, limpa seu glowing quando presente e, no cliente, envia `UpdateItemTagMessage` ao servidor; depois **encolhe uma unidade do stack se `damageValue>=maxDamage`**. Não chama `resetBound` nem `setPossessed(false)` nesse corpo. Limpar glowing não equivale a limpar `TotemPossessed`; encolher o item não prova reconciliação de um vínculo anterior nem liquidação autoritativa do desgaste observado no cliente.

Os corpos completos de `UpdateItemTagMessage` selam construtor, leitura, escrita e handler. O handler obtém sender ou jogador cliente, busca **o `entityId` fornecido no nível desse jogador**, exige uma `LivingEntity`, prefere a mão principal com o mesmo **tipo de item** e depois considera a outra mão. Se o item implementa `UpdatesStackTags` e a tag recebida existe, chama `updateTagFromServer`. Totem herda o default completo de **quatro instruções**, que delega diretamente a `ACCompat.setTag`. Receber a stack não prova aplicar seu componente de dano/durabilidade: esse default confirma apenas `CUSTOM_DATA`. O handler selecionado não contém teste explícito `entityId==sender` nem identidade do mesmo stack além do tipo de item. É observação local do corpo, sem afirmar exploração de rede, ausência de validação em outras camadas ou assentamento seguro do custo. Registro/transporte da rede, destinatários, autenticação, replay e concorrência permanecem sem certificação.

Os consumidores publicados do marcador também importam para targeting. `alexscaves.mixins.json` lista **IllagerMixin** e **LivingEntityMixin**. A anotação de `IllagerMixin.ac_isAlliedTo`, para `AbstractIllager`/`Evoker`, injeta no **HEAD de `isAlliedTo(Entity)Z`**, com **`cancellable=true` / `remap=true`**; seu corpo completo de **14 instruções** retorna false quando self ou o outro não null está possuído. O helper completo de cinco instruções lê `TotemPossessed`. A anotação de `LivingEntityMixin.ac_onSetLastHurtByMob`, para `LivingEntity`, injeta no **TAIL de `setLastHurtByMob`**, com **`cancellable=true` / `remap=true`**; seu corpo de **28 instruções**, sob os testes Raider/AbstractIllager/Mob e atacante Raider possuído, pode chamar `Mob.setTarget` para esse atacante. Seu helper também lê o marcador em cinco instruções. Isso documenta consumidores empacotados que podem alterar a interpretação de aliança/target; não prova aplicação/ordem efetiva dos mixins, proteção de outros mods ou execução física dos callbacks.

As chaves homônimas `BoundEntityUUID`/`BoundEntityTag` em Holocoder/Hologram não tornam esses objetos parte de Astral. As ocorrências de `CommonEvents` examinadas no handoff são condicionadas a **HOLOCODER**. Esta prova individual seleciona os consumers do Totem e do marcador pertinentes, sem promover contratos não relacionados por igualdade de string.

Reprodução a partir da raiz do repositório, com **Java 21** no `PATH` e o mesmo JAR publisher:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 docs/qa/alexscaves_1010_action_contract_audit.py \
  --profile astral_transferring \
  --jar /caminho/para/alexscaves-1.0.10-neoforge+1.21.1.jar \
  --manifest 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-ASTRAL-TRANSFERRING-CONTRACT-1.0.10.json' \
  --provider-root 'wiki/modpack-catalog/providers/✅-alexs-caves-continued' \
  --javap "$JAVA_HOME/bin/javap" \
  --output /tmp/astral-transferring-evidence.json

PYTHONDONTWRITEBYTECODE=1 python3 docs/qa/alexscaves_1010_astral_transferring_cards_test.py -v

PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s docs/qa -p 'alexscaves_1010_action_contract_audit_test.py' -v

PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s docs/qa -p 'alexscaves*_test.py'

PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s scripts/catalog -p '*_test.py'

PYTHONDONTWRITEBYTECODE=1 python3 scripts/catalog/generate_perk_ready_indexes.py --check

PYTHONDONTWRITEBYTECODE=1 python3 scripts/catalog/check_perk_ready_indexes.py
```

Validações estáticas executadas sobre a ficha e o manifesto selados:

| Verificação | Resultado observado |
|---|---|
| CLI real `--profile astral_transferring`, JAR publisher e selo final | **PASS**: 1 ficha, 10 classes, 13 recursos, 50 métodos e 1.045 âncoras |
| Duas reconstruções completas e sequenciais do manifesto | Bytes idênticos: 206.346 bytes, SHA-256 `322d3926e7771007c5b52df1461fd23ad27572806ea9af0991ef1d9b2a159bfc` |
| Rejeições reais de CLI com mutações de JAR, classe, recurso, ficha, guard de servidor, elapsed, saúde, laço, cópia CUSTOM_DATA e promoção de QA | **10/10 rejeitadas**, exit code 1 com motivo específico |
| Auditor compartilhado | **261/261 PASS**, incluindo 12 novos casos e os 249 anteriores preservados |
| Regressões semânticas e certificado/contabilidade Astral | **27/27 PASS**, incluídos na suíte Alex's Caves |
| Suíte `docs/qa/alexscaves*_test.py`, após incorporar a PR #1078 de Bonking | **1.237/1.237 PASS**, Java 21 disponível |
| Suíte `scripts/catalog/*_test.py` | **165/165 PASS**; total pertinente das duas suítes **1.402/1.402 PASS** |
| Índices gerados e verificadores | **544 índices**, **2.393 candidatos**, **198 contratos estáticos**, **448 fichas catalogadas**, **0 erros** |

Os 261 e 27 testes já estão incluídos nos 1.237; não são somados outra vez. Os resultados são de catálogo/parser/selos e não de combate ou sessão física. As duas provas históricas conservam limites parciais; o teste de lifecycle agora distingue essas provas históricas do certificado estático atual, sem promover hooks ou QA.

Os manifestos anteriores de [consumidor selecionado](EXACT-ASTRAL-TRANSFERRING-1.0.10.json) e [roster/lifecycle](EXACT-ASTRAL-TRANSFERRING-LIFECYCLE-1.0.10.json) conservam seus bytes e seus limites históricos. O primeiro tem **44.539 bytes**, SHA-256 `8fa111defb03eb30c9bd9284fa7aa76d913236d5c7d66d11238b66d9ae669fcb`; o segundo, **49.379 bytes**, SHA-256 `9590b337d7c186acb970edc1834adec637a74c375083ac640e328a5dbe206b52`. O roster antigo cobre **22/22 identidades de métodos**, seus digests e as **59 branches** de `onUseTick`, além das **69 âncoras selecionadas** de transferência. Isso identifica corpos/arestas sem cobrir integralmente suas instruções ou executar CFG. A reaplicação do parser histórico confirmou os **22 digests e contagens** anteriores, incluindo o digest de `onUseTick`, `4d366c998c89884f53bc9554f52c6477c5c6bbb8e6aea1bf0f93867dc1b41d39`. Ele pertence àquele parser; não é hash do classfile nem o fingerprint normalizado novo `8c294569f9123b88a02553c9be4a1a8a927c266f814b871e65ad9b92329a0863`. A diferença de encoding não é drift do corpo nativo. As duas provas anteriores permanecem evidência parcial histórica mesmo com o contrato individual novo concluído.

Uma ficha individual e **+0 raízes mágicas** não promovem o Totem integral, as fichas parciais irmãs, Stage, provider integral ou adapter executável. Black Arcana conserva seu runtime mágico e Alex's Caves conserva possessão, seleção, movimento, pedidos de ataque e liquidação nativos. Enshrouded e RPG Skill Tree requerem boundary demonstrado, owner autorizado no servidor e crédito único após resultado válido. Gravação de UUID/tag, marcador, target pedido, mensagem enviada, dano aceito e kill/Mastery são estados distintos; nenhum deles serve sozinho como recibo dos demais. Não reexecutar transferência ou dano nativo para conceder perk/XP.

QA física permanece pendente para níveis **0/I/forçados**, tags/config efetivos, cliente/dedicado e assentamento do desgaste; visão/LOS/Sightless; controlado Mob/Player e candidato Player, PvP/claims; alianças e ordem/aplicação dos mixins; múltiplos candidatos e preservação do local original; limpeza do marcador antigo e dois totems; sender/destinatário/replay e identidade de stack; morte, unload/reload, troca de dimensão e estabilidade de UUID/ID; dano realmente aceito, kills, XP e Mastery únicos. Métodos privados, NBT observado e chamadas de engine não são hooks mutadores certificados. Estado final: **`STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`**, **`NOT_VERIFIED` / `NOT_TESTED` / `NO_MUTATION`**.
