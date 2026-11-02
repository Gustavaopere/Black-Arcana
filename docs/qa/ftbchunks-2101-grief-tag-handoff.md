# Handoff — FTB Chunks 2101.1.22 e a guarda de grief do Tremorzilla

## Proveniência

- A modlist física do sibling `neoforge-rpg-skilltree/main@59ff2a0e827fd08faa603f4482f8104ac433383c` declara `FTB Chunks (NeoForge)` **2101.1.22** na posição **#288**, `FTB Teams (NeoForge)` 2101.1.11 na #291 e o loader NeoForge 21.1.250 na #001. Não presumir configuração de equipe/claims implantada apenas pela presença do JAR.
- O código-fonte público de `FTBTeam/FTB-Chunks` apresenta `EntityMobGriefingEvent` e `ENTITY_MOB_GRIEFING_BLACKLIST_TAG` na branch móvel atual; fonte de outra revisão não é prova do JAR 2101.1.22. O FTB Chunks tem licença publicada All Rights Reserved. Nenhum código/asset dele deve ser transcrito para o Black Arcana.
- A [sonda de 2101.1.22](ftbchunks_2101_grief_tag_probe.py) usa `javap` Java 21 e arquivos do artefato Maven exato. A [CI](../../.github/workflows/ftbchunks-2101-grief-tag.yml) publica um recorte limitado de assinatura, bytecode simbólico/hashes e valores declarados no arquivo `ftbchunks:entity_mob_griefing_blacklist`. O resultado deve ser selado no manifesto `FTBCHUNKS-2101-GRIEF-TAG-ABI.json` antes de qualquer merge.

## Resultado do JAR publisher exato — 2101.1.22

A [CI exploratória](https://github.com/Gustavaopere/Black-Arcana/actions/runs/41448037634) examinou o `ftb-chunks-neoforge-2101.1.22.jar` publicado no Maven do FTB Team, com **655.807 bytes** e SHA-256 `4ba1b3352184fa7f6e2aa4bca76edd074867697d62344dfa50dcccdb4dab5217`. A sonda identificou a **classe efetiva dessa versão** `dev/ftb/mods/ftbchunks/neoforge/FTBChunksForge.class`, SHA-256 `64d32b0e46d2e9c454fb78ad656348965971fa4a443251bf8b9ecf465cc5f553`, e `mobGriefing(EntityMobGriefingEvent):void` (**28 instruções**, SHA-256 `1e39dbc72b8fcc54fb52e358a77361492d3b99f9a1f7ad6e407347f88be62bb2`). Não confundir com a classe `NeoEventListeners` de revisão posterior.

**A tag padrão no JAR é exatamente uma declaração de `minecraft:enderman`**, com `replace=false`. O JSON tem SHA-256 `55bbd2c02a21e46248894700d58b044ea8779a1885d170e3ead6b4b304eac7eb`. O tipo Tremorzilla **não está declarado nesse arquivo padrão**. A tag resolvida no servidor pode mudar por datapacks e mods, portanto ainda não há prova do seu conteúdo efetivo em jogo.

O método compilado lê `Entity.getType()`, verifica `EntityType.is(ENTITY_MOB_GRIEFING_BLACKLIST_TAG)` e consulta `Level.isClientSide()`; no ramo de servidor elegível instancia `ChunkDimPos` a partir de **`event.getEntity()`** e consulta `ClaimedChunkManagerImpl.getChunk`. Com chunk reivindicado e `allowMobGriefing()==false`, chama `EntityMobGriefingEvent.setCanGrief(false)`: o operando `iconst_0` imediatamente anterior ao setter foi confirmado no bytecode. O método também contém retornos antecipados nos ramos de tipo ausente da tag, cliente, chunk ausente e permissão habilitada. Isso identifica o comportamento estático do handler, não prova sua inscrição ativa no event bus nem a configuração real do servidor.

**Consequência para o feixe:** com apenas a tag padrão do JAR, o handler do FTB Chunks não oferece evidência de veto ao Tremorzilla via `EntityMobGriefingEvent`. Mesmo que uma configuração adicione esse tipo de entidade à tag, o check do handler observado usa o **chunk da entidade**, não cada `BlockPos` afetado pelo feixe. Não concluir que claims de outros eventos, explosões ou block protection também falham. A [evidência selável](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/FTBCHUNKS-2101-GRIEF-TAG-ABI.json) exige uma nova execução com `--seal` para fechamento técnico.

## Contratos pendentes

A cadeia estática anteriormente selada no Tremorzilla (`ACPlatform.canEntityGrief` → `EventHooks.canEntityGrief`) consulta um evento com dados de entidade e mundo. O evento do NeoForge 21.1.250 pode ser alterado por listeners externos.

Não afirmar proteção territorial antes de verificar no JAR físico:

1. se o listener real do FTB Chunks consulta a tag de entidade e usa `setCanGrief`;
2. o conteúdo **padrão** da tag no JAR, distinto da resolução final com datapacks e overrides;
3. se o evento usa coordenadas da entidade e qual é o limite para um feixe que afeta blocos fora do chunk da própria entidade;
4. se `alexscaves:TremorzillaEntity` está registrado na tag **resolvida** do servidor (ID de entidade exato não presumido);
5. se proteções de explosão, mutação de blocos e spawn são caminhos distintos da guarda de mob griefing;
6. se existem configs e claims ativadas na instância real.

**Fail-closed:** `NO_MUTATION`, `NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`. Este handoff não implementa um hook ou bridge; não atualiza os números de fichas ou providers.
