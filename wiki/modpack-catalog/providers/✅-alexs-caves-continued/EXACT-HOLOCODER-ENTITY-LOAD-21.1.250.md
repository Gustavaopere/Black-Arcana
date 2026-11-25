# Holocoder — representação recursiva, NBT e UUID (NeoForge 21.1.250)

**DISCOVERY_ONLY / NO_MUTATION**. Publisher Alex's Caves Continued 1.0.10 (SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, 75.279.314 bytes). Minecraft 1.21.1, Java 21. Distribuição oficial 21.1.250, não bytes carregados na instância. Modlist sibling reconsultada em `18144e8318978b8904b584b80b4ddd630f22f8f0`: entrada física #19, mesmo publisher/versão.

## Reuso de evidência existente

Releitura do [run 45471957912, job 138721970278](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45471957912/job/138721970278), relatório de 1.956.222 bytes, SHA-256 `5a5c4a201604224306a2b5cded87cb82523bce8cf0e82aaf998954125afe0c65`.

| Método | Code SHA-256 | Limite causal observado |
|---|---|---|
| EntityType.by(CompoundTag) | `7805295fd5281c3f0fa3b347af587a0609a4bb2e2d0aa9eb0b9002db7e38b745` | getString @7, ResourceLocation.parse @10, BuiltInRegistries.ENTITY_TYPE.getOptional @13. Optional não demonstra captura de exceção de parse. |
| EntityType.create(CompoundTag,Level) | `0a5cac55bbb389687a277d8126d51488c6d7d4f495905364f5210faa15b5f49e` | by @1; Optional.map @10, Util.ifElse @25; bootstrap #7/#8/#9 resolve lambdas create$4/$5/$6, corpos ainda não projetados. |
| EntityType.loadEntityRecursive | `3a63201fa9087a793c3f872c58d7dcedfde2bd5a8481cce2ac0a2e9e33376d91` | loadStaticEntity @2, Optional.map @6, lambda handle #10 @12, map @17, orElse @21. O corpo da lambda ainda não foi projetado. |
| Entity.load | `776e21588ffb8384705ac584255b82bdb9a471e89e49bc8949048d60e0fbbe88` | hasUUID @280 precede getUUID @291, grava uuid @294/stringUUID @305; readAdditionalSaveData @637 é despacho virtual para tipo concreto. |
| Entity.saveWithoutId | `04ba844cbcb8c70d4ec427dfe8f56bfeef10cb0a564066cd679f63bdeec5ab5d` | getUUID @231, putUUID @234, addAdditionalSaveData @497, getPassengers @517, saveAsPassenger @562. |
| ACCompat.entityTypeFrom | `ccffa1ba52333413dbc8952ba9eb956bfed3448c7eea64746c64c5ba5eeceeec` | delega EntityType.by @1. |

O Holocoder chama ACPlatform.serializeEntity para não-player, mas os campos concretos e callbacks de cada espécie não são uniformes. A representação chama loadEntityRecursive com Function.identity. O helper markDisplayEntity observado no run 45478556000 devolve o argumento, sem flag de isolamento. Não interpretar criação de objeto Java como spawn no mundo, nem ausência de chamada de spawn no corpo local como ausência de efeitos colaterais de callbacks externos.

## Nova coleta delimitada — observação distribuída concluída

`docs/qa/alexscaves_1010_holocoder_entity_load_250_probe.py` exige pins do publisher e quatro artefatos oficiais, seis classfiles e seis Code hashes previamente observados. Seleciona os handles acima e caminhos de load/save, UUID/CompoundTag, ResourceLocation, ListTag e wrappers. Nomes candidatos de outros métodos/classes são filtros de descoberta, não APIs afirmadas; o relatório registra declarações, ausência e Code quando existir. Exige os nomes de métodos já referenciados, projeta callsites, branches, operandos tipados e exception tables. CI exige replay idêntico; o novo selo é documentado abaixo. Não há execução das entidades, leitura de dados privados do jogador ou alteração de NBT no jogo.

Sem novo certificado, hook, QA física, resultado de captura, mundo ou Mastery. `NO_MUTATION`.

## Resultado da coleta e selo

[Run 45517198076, job 138879583331](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45517198076/job/138879583331), HEAD `fa63d05a74c3e4da7c72c00f8af3220743a30551`: cinco checks de escopo/política e duas projeções idênticas aprovadas; **13 classes, 60 declarações selecionadas, 58 métodos com Code, 2 sem Code**. Relatório de **485.099 bytes**, SHA-256 `0ee9ec7fb5d4e31f53cd24be22d1b5cf7cc43879ede2c1a86699e145480b4667`. Novo HEAD fixa também tamanho e digest; CI final ainda exigida.

### Serialização do alvo, representação e passageiros

| Corpo | Code SHA-256 | Limite estático observado |
|---|---|---|
| IEntityExtension.serializeNBT(Provider)CompoundTag | `2d9987b5b42294cc79831cabe208e21b58192be512164311c34f5781092ca04a` | Nova tag, getEncodeId @14; id não nulo é escrito @34; saveWithoutId @44. Não é criação de summon. |
| IEntityExtension.deserializeNBT(Provider,CompoundTag)V | `1c154b6d86bfb555594f3ba6ec3fd6e7b1951fbd60942c169f57f58223c05215` | self @1, Entity.load @7. |
| EntityType.lambda$create$4 | `f661422e8f7768c1510b0ab63281d9b6fa297642277481d62e232738f3914160` | chama create(Level) @2; esse corpo consulta enabledFeatures e chama factory ou retorna null. |
| EntityType.lambda$create$5 | `1947a3d035bd74987fac5bdff0f6bd46b4750d5639a974a512f948073348f0da` | Entity.load(tag) @2, portanto callback virtual readAdditionalSaveData pode ser alcançado. |
| EntityType.lambda$create$6 | `068be2c01394fe1777e30dc2f1e278f2a51c7a46567c6cb02a517b5452060006` | registra warning de id pulado; não é fallback de criação. |
| EntityType.loadStaticEntity | `c8382a747a36bd65e57e65e1aa6482d5b8d1db5a8edeeffba6470a0912b12c13` | create @2; handler RuntimeException [0,5) -> @6, warning e Optional.empty @19. Não cobre automaticamente exceções do callback fornecido ou da recursão posterior. |
| EntityType.lambda$loadEntityRecursive$7 | `13a627377ce8e3ac6f64c9ca1c136f2cc95ec7f85d5687b76ae11a3eda066fec` | Passengers tipo 9, getList tipo 10; loop por size, getCompound @40, recursão @45 com mesma Function; retorno não nulo pede startRiding(parent,true) @59 e descarta booleano. Sem contador de profundidade explícito neste corpo. |
| Entity.startRiding(Entity,Z)Z | `aa9b975911feea0d4d8c97dc60b31418d295ddfda56cd74217ff52c153249c20` | rejeita mesmo veículo, couldAcceptPassenger false, ciclos de veículo e EventHooks.canMountEntity @49 false; flag true pula canRide/canAddPassenger, não o evento. Se aceito, stopRiding condicional, pose STANDING, escreve vehicle @97, addPassenger @105, processa stream de passageiros. |

A função passada pelo HologramProjectorBlockEntity é Function.identity, não callback de inserção no Level. No recorte estático há criação/carregamento de representação, possível recursão de passageiros e solicitação de montagem, não um summon registrado. `markDisplayEntity` não modifica estado no publisher. Não garantir ausência de callbacks externos, limites transitivos de NBT, isolamento da representação ou proteção de dados.

### UUID e rejeições estruturais

| Corpo | Code SHA-256 | Resultado observado |
|---|---|---|
| CompoundTag.putUUID | `acd677efba9098f461f9fa26e60294c51154ed6520a4c80f4937c9bf5f415330` | NbtUtils.createUUID @6, Map.put @9. |
| NbtUtils.createUUID | `f12baf745119643d128a34a88585e2586299605a5ac8a5370edeffb1276a4d05` | UUIDUtil.uuidToIntArray @5, IntArrayTag([I) @8. |
| CompoundTag.hasUUID | `5e29b58ba66584774aebec567a7fd26dd96ba513ca21e365e485478d34c71568` | tag não nula, tipo IntArrayTag.TYPE e length=4. |
| CompoundTag.getUUID | `4a7e01f28d3bce4fe1c5f5e70343d417d90e8fbdba5a14c1cbf4d760b8d87483` | get @2 -> NbtUtils.loadUUID @5; não chama hasUUID. |
| NbtUtils.loadUUID | `dbe178b679ba72a4b07fc04234a08cea44e3824fcdb96c7a038c887439166f4a` | Tag.getType @1; tipo incorreto ou length diferente de 4 solicita IllegalArgumentException @40/@69; UUIDUtil.uuidFromIntArray @74. Não há guarda nula nem handler próprio. |
| UUIDUtil.uuidToIntArray | `55a499f8c305ede0532d5fb84bc99aef3930d1b0243545fba0b989eb9838fc41` | getMostSignificantBits/getLeastSignificantBits e conversão para array de quatro ints. |
| UUIDUtil.uuidFromIntArray | `6c57b7ea3dd78907efc83dd7f8a0306a2ab0063897014bf4b9c4a1f7dce1cf1b` | reconstrói os dois longs usando posições 0/1 e 2/3, deslocamento 32 e máscara 4294967295 para os baixos; UUID(JJ) @36. |

O `HolocoderItem.getBoundEntityUUID` chama ACCompat.getTag, testa contains(String) @13 (não hasUUID) e chama getUUID @25, sem handler. A tag presente com tipo/length inválidos pode alcançar rejeição excepcional. A ausência da chave no ramo normal retorna null; não equiparar ausência a NBT malformado. `isBound` testa apenas o retorno não nulo, sem tratamento de exceção local. Entity.load usa hasUUID antes de ler seu próprio UUID, um gate diferente do wrapper do item. Isso não demonstra que uma stack malformada seja admitida pelo transporte ou que um erro cause falha física do servidor.

ResourceLocation.parse (Code `73d47019b092d9806af85c4cd4fa33a77429fcacb4362d4fa387f4f8ddf2ab77`) usa separador ':' e bySeparator; funções assertValidNamespace/assertValidPath têm ramos que constroem ResourceLocationException. A captura de RuntimeException em loadStaticEntity é limitada à chamada create; o uso direto de ACCompat.entityTypeFrom/EntityType.by fora desse contexto não ganha automaticamente essa captura. Não assumir fallback para todo id malformado.

**Integração:** registro de UUID não é ownership; não duplicar entidade, invocar load em paralelo, alterar payload por perk ou creditar Mastery por objeto construído, mount request ou render. A evidência de UUID é compartilhável com outras fichas após revisão individual, sem alterar a PR reservada da Gazing Pearl. Runtime carregado, callbacks concretos dos outros tipos de entidade, permissões, inventário e QA permanecem abertos; nenhum novo certificado ou raiz.
