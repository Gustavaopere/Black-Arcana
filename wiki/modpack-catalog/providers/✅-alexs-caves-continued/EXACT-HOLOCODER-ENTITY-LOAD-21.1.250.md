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

## Nova coleta delimitada — primeiro resultado pendente

`docs/qa/alexscaves_1010_holocoder_entity_load_250_probe.py` exige pins do publisher e quatro artefatos oficiais, seis classfiles e seis Code hashes previamente observados. Seleciona os handles acima e caminhos de load/save, UUID/CompoundTag, ResourceLocation, ListTag e wrappers. Nomes candidatos de outros métodos/classes são filtros de descoberta, não APIs afirmadas; o relatório registra declarações, ausência e Code quando existir. Exige os nomes de métodos já referenciados, projeta callsites, branches, operandos tipados e exception tables. CI exige replay idêntico antes de fixar novo selo. Não há execução das entidades, leitura de dados privados do jogador ou alteração de NBT no jogo.

Sem novo certificado, hook, QA física, resultado de captura, mundo ou Mastery. `NO_MUTATION`.
