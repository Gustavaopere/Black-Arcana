# Galena Gauntlet — cadeia JVM distribuída de admissão de entidade (NeoForge 21.1.248)

**Estado:** ⚠️ **subcontrato JVM estático de interoperabilidade, limitado aos binários oficiais da distribuição `--installServer`**. Não houve carregamento pelo ModLauncher, inspeção dos mixins do modpack, efeito real no mundo ou QA física. `static_contract=NOT_CERTIFIED` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `NO_MUTATION` · `provider_universe_closed=false`.

## 1. Fonte de autoridade, versão exata e hashes

Esta etapa continua a [auditoria de ABI upstream](EXACT-GALENA-ENTITY-JOIN-ABI-21.1.248.md), a [localização de patches](EXACT-GALENA-ENTITY-JOIN-PATCHES-21.1.248.md) e a [ordem de cancelamento nos patches](EXACT-GALENA-JOIN-FLOW-21.1.248.md), com novo recorte independente: **os classfiles distribuídos** pelo instalador oficial NeoForge 21.1.248 para Minecraft 1.21.1.

- **Provider em estudo:** Alex's Caves Continued `alexscaves` **1.0.10**, Minecraft 1.21.1/NeoForge/Java 21; modlist sibling `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`. JAR publisher previamente analisado: SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. **Dump binário de nova instalação ainda não confrontado.**
- **Engine de compilação efetivamente fixada:** `neo_version=21.1.248` nos dois `gradle.properties`, em Java 21.
- **Instalador NeoForge Maven oficial:** `neoforge-21.1.248-installer.jar`, SHA-256 `68eeab77059ba53df1812f1afa5bf530ab2566a3cdcd5f924aa6e71be42e410c`, validado contra `.sha256` do Maven.
- **Overlay distribuído:** `neoforge-21.1.248-server.jar`, **5.675.624 bytes**, SHA-256 `1808fab692dc44b2d474295d1cdd9f1fe8a7dceab4f594210873646fafdf1359`.
- **Distribuição base Minecraft SRG:** `server-1.21.1-20240808.144430-srg.jar`, SHA-256 `26ca9c40d7e1681190b428583c38816852218e78df3f8bdb60a59a78503aec71`. Os JARs foram obtidos por instalação do pacote oficial em GitHub Actions, usando os verificadores de distribuição já selados no projeto.
- **Execução observacional:** [workflow #45211836269](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45211836269), job `137822418958`, HEAD `d7cfda2d7b79948433216798f7358eb27b4c98f9`, **success**.
- **Relatório determinístico:** `report.json`, **13.544 bytes**, SHA-256 `b83db649e207ae7edf4fe8cc6c4c8db935fbe8ef6ceaccc15859a1a535f15342`. Foram examinadas **4 classes**, selecionados **11 métodos com Code** e **16 callsites JVM tipados**. Fonte: [sonda](../../../../docs/qa/alexscaves_1010_galena_211248_distributed_spawn_probe.py), [manifesto SHA-exato](EXACT-GALENA-DISTRIBUTED-SPAWN-21.1.248.json), [checker adversarial](../../../../docs/qa/alexscaves_1010_galena_211248_distributed_spawn_checks.py) e [workflow](../../../../.github/workflows/alexscaves-1010-galena-neoforge-211248-distributed-spawn.yml). **A execução do checker posterior precisa aprovação na HEAD final antes de merge.**

O relatório conserva descritores JVM, offsets e opcodes de chamadas, índices de constant pool, hashes de classes/Code e contagens de desvios. **Nenhum corpo Java, código decompilado ou asset de terceiros é versionado.**

## 2. Quatro classes de engine e suas origens distribuídas

| Classe analisada | Origem na distribuição | SHA-256 do classfile | Métodos declarados / selecionados |
|---|---|---|---|
| `Level` | NeoForge server overlay | `74a062f0d480674152fa4665bd7b483fca52de8dd3b07178c1a6c40d3fae3fae` | 146 / **0** com nomes selecionados |
| `ServerLevel` | NeoForge server overlay | `19b42e51848fd27df3683dacf694baa5126ee9f0665f12afdc65f82493a1e5a3` | 168 / **6** |
| `LevelWriter` | Minecraft server SRG | `ff1c3d2a794c021a565e9213ae01b8b4a8e276975d780128d26994b472190b47` | 7 / **1** |
| `PersistentEntitySectionManager` | NeoForge server overlay | `6351fcb7c7370b77b8d9618474783b58ab3e037c224b5c83481c23908db1fbf4` | 55 / **4** |

Todos os classfiles examinados têm versão Java classfile major **65**. Zero métodos selecionados em `Level` significa apenas **ausência local dos nomes selecionados nessa classe distribuída**, não prova ausência de API via interfaces, herança, outros nomes ou transformers. `LevelWriter.addFreshEntity(Entity):boolean` foi identificado como membro tipado da distribuição SRG; seu corpo/método não é prova de execução pelo provider.

## 3. Grafo de chamadas JVM certificado apenas no recorte distribuído

<escape>A cadeia abaixo foi observada por invocações tipadas (não por correspondência de texto solto nem apenas referência no constant pool).</escape>

| Método caller com descritor JVM | Destino callee declarado | Offset da invocação |
|---|---|---:|
| `ServerLevel.addFreshEntity(Entity):Z` | `ServerLevel.addEntity(Entity):Z` | **2** |
| `ServerLevel.addEntity(Entity):Z` | `PersistentEntitySectionManager.addNewEntity(EntityAccess):Z` | **32** |
| `PersistentEntitySectionManager.addNewEntity(EntityAccess):Z` | `PersistentEntitySectionManager.addEntity(EntityAccess,Z):Z` | **3** |
| `PersistentEntitySectionManager.addEntity(EntityAccess,Z):Z` | `EntityJoinLevelEvent.<init>(Entity,Level,Z):V` | **25** |
| Mesmo método do manager | `EntityJoinLevelEvent.isCanceled():Z` | **36** |
| Mesmo método do manager | `PersistentEntitySectionManager.addEntityWithoutEvent(EntityAccess,Z):Z` | **47** |

**Causalidade delimitada:** os seis pares de caller/callee e seus offsets estão presentes no **bytecode oficial distribuído** 21.1.248. No recorte da classe, `ServerLevel.addEntity` também possui `Entity.onAddedToLevel():V` no offset **39**, enquanto `addFreshEntity` não introduz uma segunda chamada dessa rotina. Os corpos de Code têm hashes fixados no manifesto.

O [dossiê de patch-flow](EXACT-GALENA-JOIN-FLOW-21.1.248.md) documenta separadamente a ordenação dos ramos: o evento cancelável precede o encaminhamento ao registro do UUID, e o callback ordinário em `ServerLevel.addEntity` aparece no ramo de aceitação. **É a combinação de duas evidências estáticas correlatas**: o classfile distribuído identifica as chamadas; o patch oficial informa a intenção/ordem lexical. Não se declara equivalência com um runtime pós-ModLauncher sem validação própria.

### 3.1. Rota de jogadores não deve ser confundida com a arma

A rotina `ServerLevel.addPlayer(ServerPlayer):V` da distribuição possui invocações de construtor `EntityJoinLevelEvent(Entity,Level)` @**9**, `isCanceled()` @**20**, `addNewEntityWithoutEvent(EntityAccess)` @**83** e `ServerPlayer.onAddedToLevel()` @**88**. Essa é uma rota **específica de jogadores**; não usá-la para afirmar que `MagneticWeaponEntity` é um jogador ou que a emissão da arma é duplicada.

Em `ServerLevel.addDuringTeleport(Entity):V`, há duas chamadas tipadas, para `addPlayer` @**14** e `addEntity` @**22**. `ServerLevel.addWithUUID(Entity):Z` chama `addEntity` @**2**; `tryAddFreshEntityWithPassengers(Entity):Z` chama `addFreshEntityWithPassengers(Entity):V` @**40**. São caminhos de admissão adicionais observados, não prova de que a Galena os acione.

### 3.2. Rotas do manager e integridade do mundo

`PersistentEntitySectionManager.addNewEntityWithoutEvent(EntityAccess):Z` encaminha a `addEntityWithoutEvent(EntityAccess,Z):Z` @**3**, distinto da rota pública `addNewEntity` que encaminha a `addEntity`. No manager, `EntityJoinLevelEvent` é construído com parâmetro booleano adicional (flag de carregamento), coerente com o evento ABI observado. O comportamento final ao cancelar, a execução dos callbacks, o retorno `Z` e a disponibilidade de hooks devem ser validados com corpo transformado, listeners reais e, quando aplicável, QA física.

## 4. Relação com o contrato publisher da Galena

A auditoria do JAR publisher 1.0.10 já registrou que `GalenaGauntletItem.onUseTick` solicita `ItemStack.setCount(0)` **antes** de `ACCompat.createEntity` e de `Level.addFreshEntity`, ignorando o retorno booleano deste último. A nova evidência confirma que a implementação distribuída de `ServerLevel.addFreshEntity(Entity):Z` contém chamada direta a `ServerLevel.addEntity(Entity):Z`, e a rota distribuída desse método encadeia o manager e o evento cancelável.

**Não extrapolar:** a auditoria não capturou o estado da stack após falha, a criação bem-sucedida da `MagneticWeaponEntity`, o caminho realmente escolhido em gameplay, o resultado da inscrição da entidade, a ordem de mixins externos ou um cancelamento provocado por terceiros. Em especial, **não** prova perda de item, exploit, duplicação ou segurança de restituição. Os arquivos de distribuição oficial podem ser transformados posteriormente pelo ModLauncher; a instância do modpack e seu ordenamento de loaders/mixins permanecem desconhecidos.

A atribuição correta de owner, custos, durability, efeitos/dano, drops, NBT, cooldown, persistência, dimension change e callbacks exige provas específicas; não conceder XP, Mastery ou perks a partir de evento publicado ou pedido de spawn. Black Arcana mantém autoridade sobre o runtime mágico e `WorldEffectPolicy`; RPG Skill Tree permanece somente provedor sibling para progressão/atributos/Mastery/perks via contratos seguros.

## 5. Reprodução, verificações e pendências

```sh
python3 docs/qa/alexscaves_1010_galena_211248_distributed_spawn_probe.py \
  --server /caminho/neoforge-21.1.248-server.jar \
  --srg /caminho/server-1.21.1-20240808.144430-srg.jar \
  --javap /caminho/java21/bin/javap \
  --output /diretorio-novo/report.json

python3 docs/qa/alexscaves_1010_galena_211248_distributed_spawn_checks.py \
  --report /diretorio-novo/report.json \
  --manifest 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-GALENA-DISTRIBUTED-SPAWN-21.1.248.json' \
  --adversarial
```

A execução de CI baixa o instalador oficial, confere SHA, executa `--installServer`, confirma as duas distribuições pinadas e reconstitui o relatório de rosters/callsites. O checker valida relatório SHA-exato, versões, classes, Code SHAs, descritores, offsets, índices CP, limites estáticos e alterações adversariais. **Somente a execução desse checker na HEAD final pode encerrar este recorte estático; não promove o objeto inteiro.**

**Pendências para a Galena:** provar paridade do servidor efetivamente executado, método pós-ModLauncher, compatibilidade/cadeia de mixins e event listeners, entrada e cancelamento reais de `MagneticWeaponEntity`, rollback da stack, proteção territorial, persistência e QA física. Até então: `static_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`.

**Progresso preservado:** Galena ⚠️ parcial; Alex's Caves **130/134** contratos estáticos de objetos identificados no recorte, **4** fichas pendentes; global **269/2.446** contratos observados, **4/164** providers documentais concluídos e **0/164** integralmente perk-ready. Um novo nó de infraestrutura não é uma nova magia.
