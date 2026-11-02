# Handoff — FTB Chunks 2101.1.22 e a guarda de grief do Tremorzilla

## Proveniência

- A modlist física do sibling `neoforge-rpg-skilltree/main@59ff2a0e827fd08faa603f4482f8104ac433383c` declara `FTB Chunks (NeoForge)` **2101.1.22** na posição **#288**, `FTB Teams (NeoForge)` 2101.1.11 na #291 e o loader NeoForge 21.1.250 na #001. Não presumir configuração de equipe/claims implantada apenas pela presença do JAR.
- O código-fonte público de `FTBTeam/FTB-Chunks` apresenta `EntityMobGriefingEvent` e `ENTITY_MOB_GRIEFING_BLACKLIST_TAG` na branch móvel atual; fonte de outra revisão não é prova do JAR 2101.1.22. O FTB Chunks tem licença publicada All Rights Reserved. Nenhum código/asset dele deve ser transcrito para o Black Arcana.
- A [sonda de 2101.1.22](ftbchunks_2101_grief_tag_probe.py) usa `javap` Java 21 e arquivos do artefato Maven exato. A [CI](../../.github/workflows/ftbchunks-2101-grief-tag.yml) publica um recorte limitado de assinatura, bytecode simbólico/hashes e valores declarados no arquivo `ftbchunks:entity_mob_griefing_blacklist`. O resultado deve ser selado no manifesto `FTBCHUNKS-2101-GRIEF-TAG-ABI.json` antes de qualquer merge.

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
