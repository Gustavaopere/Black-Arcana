# Alex's Mobs Continued — divergência entre JAR 2.1.13 e fonte público atual (2026-10-29)

Estado: `EXACT_BINARY_IDENTITY_CLOSED / PUBLIC_SOURCE_VERSION_MISMATCH / NO_2.2.3_PARAMETER_PROMOTION`.

## Autoridade instalada e reprodutível

A ficha física atual do sibling `Gustavaopere/neoforge-rpg-skilltree` identifica `alexsmobs-2.1.13-neoforge+1.21.1.jar`, `alexsmobs`, Minecraft 1.21.1 / NeoForge e SHA-1 `50ddafdf3d12b33331e4eecb4ab514ae451baadd`.

A auditoria NON-MERGE PR #511 / run `36949047824` baixou o artefato publisher CurseForge file `8856498` e comprovou **SHA-1 física = publisher**. Inventário do artefato: 1.270 classes; **26** classes de itens e **11** de blocos com entradas interativas auditadas; três raízes sobrenaturais exatas, das quais **uma** alcançável sem o gate de summon e **duas** `CONDITIONAL`. A evidência está em [auditoria do artefato](EXACT-2.1.13-ARTIFACT-AUDIT.md) e [disposição de interações](INTERACTION-DISPOSITION-2.1.13.md).

## O fonte público consultável não corresponde à versão instalada

O repositório público [`Codx-org/AlexsMobsContinued`](https://github.com/Codx-org/AlexsMobsContinued) expõe a revisão `e0dda181b999b3df09c4a4f7fd41e55f1b621ed8`. Em `stonecutter.properties.toml` dessa revisão, o campo `mod.version` declara explicitamente **`2.2.3`**, não `2.1.13`; o único branch exposto pela consulta foi `main`, sem um commit histórico da release 2.1.13 encontrado no histórico público acessível. Isso **não prova que a lógica mudou**, apenas impede declarar igualdade de fonte ou números com o build físico.

Fontes de conferência: [revisão pública](https://github.com/Codx-org/AlexsMobsContinued/tree/e0dda181b999b3df09c4a4f7fd41e55f1b621ed8), [metadata de versão](https://github.com/Codx-org/AlexsMobsContinued/blob/e0dda181b999b3df09c4a4f7fd41e55f1b621ed8/stonecutter.properties.toml), [publisher 2.1.13 NeoForge 1.21.1](https://modrinth.com/mod/alexs-mobs-continued/version/Ok0b9L76).

## Não promover do fonte 2.2.3 para o JAR 2.1.13

Sem correspondência compilada comprovada, permanecem `NOT_VERIFIED` em 2.1.13 quando não constarem da auditoria exata: cooldown, números de XP, raios, vida de portais, damage, profundidade de summon, limites/valores de config, autorização do pacote de menu, eventos e hooks mutadores. Não substituir as configurações efetivamente implantadas por defaults de uma árvore posterior.

Os nomes de `ItemDimensionalCarver`, `ItemMysteriousWorm`, `AMConfig.voidWormSummonable`, `AMConfig.voidWormSpawnDimensions`, `BlockTransmutationTable` e as relações causais **já constam do audit de bytecode exato**; não dependem do fonte público 2.2.3.

## Reabertura futura

1. Priorizar cópia/bytecode do JAR instalado verificada pelo SHA-1 acima; opcionalmente recuperar os arquivos de evidência do workflow 36949047824 sem alterar o artefato distribuído.
2. Resolver fonte histórico 2.1.13 só se houver revisão/tag/código identificável e contrastar com os três métodos de controle do binário exato; não presumir que mudar `mod.version` reproduz a release.
3. Capturar `AMConfig` efetivo, overrides datapack e sessões no servidor dedicado; depois validar o grafo de gates em [`SEMANTIC-REACHABILITY-GATES-2.1.13.json`](SEMANTIC-REACHABILITY-GATES-2.1.13.json).
4. Nenhuma condição descrita aqui promove `COMPLETE_PERK_READY`, libera hook mutador, registra QA física como PASS nem altera o denominador (3 raízes / +1 estrita).
