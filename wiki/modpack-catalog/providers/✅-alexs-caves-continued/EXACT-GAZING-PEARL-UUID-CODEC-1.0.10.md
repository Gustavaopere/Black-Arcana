# Gazing Pearl — fronteira UUID de reputação ACCompat / ACWorldData (publisher 1.0.10)

**Estado:** ⚠️ **subcontrato estático SHA-exato de serialização UUID e consumidores tipados**, sem certificação individual integral de `alexscaves:gazing_pearl`. `static_contract=NOT_CERTIFIED` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `NO_MUTATION` · `provider_universe_closed=false`.

## 1. Autoridade e versão exata

- **Provider:** Alex's Caves Continued `alexscaves` **1.0.10** (Minecraft 1.21.1 / NeoForge / Java 21). Na [modlist física do RPG Skill Tree](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/main/PROJECT-INSTRUCTIONS/modlist/World%20Gen/%E2%9C%85-alexs-caves-continued%20v1.0.10.md), o item #19 registra `alexscaves-1.0.10-neoforge+1.21.1.jar` e SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`.
- **Publisher JAR auditado:** `alexscaves-1.0.10-neoforge+1.21.1.jar`, **75.279.314 bytes**, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. Foram inspecionados **1.555 classfiles** exatos, sem executar classes do mod. A igualdade dos bytes com uma cópia do modpack instalado continua **NOT_VERIFIED**.
- **Execução inicial:** [GitHub Actions #45227358098](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45227358098), job `137877321301`, `success`, HEAD observacional `2628fe90cd9185b77fdc0405e94480810a81119b`.
- **Relatório `report.json`:** **49.616 bytes**, SHA-256 `3db0c1c42736c6d4c67ab1b0682646d6ba499756ac15f83b7c8e3132548afa3e`. As evidências versionadas incluem [sonda read-only](../../../../docs/qa/alexscaves_1010_gazing_pearl_uuid_codec_probe.py), [manifesto de hashes](EXACT-GAZING-PEARL-UUID-CODEC-1.0.10.json), [checker adversarial](../../../../docs/qa/alexscaves_1010_gazing_pearl_uuid_codec_checks.py) e [workflow](../../../../.github/workflows/alexscaves-1010-gazing-pearl-uuid-codec.yml). **A conclusão da descoberta anterior não substitui a CI do checker acrescentado posteriormente.**

## 2. Métodos UUID de ACCompat: delegação estática direta

**`com/github/alexmodguy/alexscaves/server/misc/ACCompat`** (classfile SHA-256 `333738f324e6e9d77a488e14b7e81b169c2b2d4f6db5171206a016ad0271f57b`) tem **200 métodos declarados** no publisher. O recorte selecionou **dois** wrappers relevantes:

| Wrapper do publisher | Code SHA-256 | Instruções | Invocação JVM direta |
|---|---|---:|---|
| `getUUID(CompoundTag,String):UUID` | `c4c782b1bfa2a9c3d587ec79d9629edf2c3516a4b088cd215692e4c4fe039dcb` | 4 | `CompoundTag.getUUID(String):UUID` — `invokevirtual` @**2**, CP#1090 |
| `putUUID(CompoundTag,String,UUID):void` | `9bc59b9d44f0f1f9bd48ed6c0f36b83d58b706dc72c694b139e3d333fa3640e2` | 5 | `CompoundTag.putUUID(String,UUID):void` — `invokevirtual` @**3**, CP#1094 |

Os dois corpos do wrapper são lineares no recorte disassemblado, sem branches locais, com um retorno. Os descritores e invocações foram confrontados com o **constant pool tipado e o Code**, não apenas por busca de texto.

**Limite:** o fato de ACCompat delegar a `CompoundTag.putUUID/getUUID` **não prova** o tipo concreto de `Tag` gravado, o payload UUID, a serialização real em disco ou a recuperação pós-restart. Essa próxima fronteira depende de inspeção própria dos métodos da engine distribuída **NeoForge 21.1.248**, seguida de QA física quando possível.

## 3. Consumidor causal da Gazing Pearl: ACWorldData

A ficha [Gazing Pearl](items/gazing-pearl.md) já documenta que `GazingPearlItem.acInventoryTick` consulta `ACWorldData.getDeepOneReputation(entity.getUUID())`, somente construindo/atualizando **snapshot** `HasReputation` / `Reputation` / `LastReputationTimestamp` na `ItemStack`. O item não grava nem altera a reputação autoritativa do mundo.

O classfile `ACWorldData` tem SHA-256 `ddb140795a4a38e077575effb858c2f7664780f11046475335ca132200b031f5`. O [dossiê do armazenamento 1.0.10](EXACT-GAZING-PEARL-WORLDDATA-1.0.10.md) já provou a estrutura de lista `DeepOneReputations` e entradas com campos `UUID` e `Reputation`. Esta sonda fixa as **chamadas exatas** desse codec:

| Método de ACWorldData | Code SHA-256 | Chamada tipada |
|---|---|---|
| `acSave(CompoundTag):CompoundTag` | `fc86c0bf51203469f869f5144f9b3b690b6c0cd6bb5d97258fb24e821a62d587` | `ACCompat.putUUID`, `invokestatic` @**78**, CP#206 |
| `load(CompoundTag):ACWorldData` | `064fbae435ec957a69aa659ff02248ecd37a9c2fd9132f36228d13b73cb666a5` | `ACCompat.getUUID`, `invokestatic` @**51**, CP#106 |

O caminho estaticamente demonstrado é: **`ACWorldData.acSave → ACCompat.putUUID → CompoundTag.putUUID`**; e, para recuperar, **`ACWorldData.load → ACCompat.getUUID → CompoundTag.getUUID`**. Não há garantia física de salvamento/ordem de escrita, cópia instalada compatível ou persistência de arquivo após reinício. O setter do `ACWorldData` aplica clamp de reputação −100..100, mas `load` **não** aplica clamp: não confundir semântica de valor com o formato do UUID.

## 4. Censo reprodutível de consumidores do mesmo wrapper

A análise de **todos os 1.555 classfiles** do publisher encontrou **27 classes**, **56 métodos** e **63 callsites invocadores tipados** de `ACCompat.putUUID` e/ou `ACCompat.getUUID`. O roster completo fica no relatório com SHA exato de **44.289 bytes**, SHA-256 `9c6440ab63af01c68ff8b2a1f69e8cf45b16f639d7a6847609303bdf95b00eab`; o manifesto fixa seu hash, contagens e fronteira de classes de interesse.

Entre os consumidores estão tanto `ACWorldData` quanto `MagneticWeaponEntity`, cuja serialização de UUID é **um contrato independente da Galena Gauntlet**. Este censo se restringe a referências diretas presentes no JAR publisher, por assinatura e invocação, sem assumir outros mods, reflexão, MethodHandles, calls indiretas ou a execução dos caminhos. As 63 chamadas não constituem 63 objetos mágicos nem certificação de cada consumidor.

## 5. Repetição, testes de adulteração e limites

```sh
python3 docs/qa/alexscaves_1010_gazing_pearl_uuid_codec_probe.py \
  --jar /caminho/alexscaves-1.0.10-neoforge+1.21.1.jar \
  --javap /caminho/java21/bin/javap \
  --output /diretorio-novo/report.json

python3 docs/qa/alexscaves_1010_gazing_pearl_uuid_codec_checks.py \
  --report /diretorio-novo/report.json \
  --manifest 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-GAZING-PEARL-UUID-CODEC-1.0.10.json' \
  --adversarial
```

O checker verifica SHA/tamanho de `report.json`, SHA Code e desc das duas funções, offset/CP/owner da delegação, ambos os callsites `ACWorldData`, roster completo das 27 classes/56 métodos/63 invocações, e rejeição de adulterações em classfiles, callsites e estados. Somente após **CI da HEAD final com resultado observável** o subcontrato de UUID poderá ser considerado reproduzido; não promover o contrato completo da Gazing Pearl.

**Pendências:** método exato `CompoundTag.putUUID/getUUID` no classpath distribuído 21.1.248, tipo `Tag` e métodos de criação/decodificação de UUID, extensão do censo de writers apenas quando ligada causalmente a dados reais, paridade de JAR/modpack, componentes da `ItemStack` efetiva, estado de arquivo `alexscaves_world_data.dat` após save/restart, sincronização e UI/render física, efeitos indiretos de consumidores e listeners. Sem hook seguro: `NO_MUTATION`, *fail-closed*; Black Arcana mantém autoridade da magia e RPG Skill Tree apenas dos boundaries de progressão/Mastery realmente verificados.

**Contadores:** sem incremento; os números 130/134 e 269/2.446 pertenciam ao recorte histórico da descoberta. Os índices canônicos da base consolidada prevalecem. Gazing Pearl permanece parcial; universo integral não comprovado.

## Reuso explícito da engine 21.1.250 e checker adversarial

[Run 45228520204, job 137881430924](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45228520204/job/137881430924), HEAD `2f98919933c1ae657cbad4c1f7a26f3c0f0b49e1`: o checker selou o mesmo relatório de 49.616 bytes e rejeitou 106 adulterações (ADVERSARIAL_REJECTED 106); artifact 14846556082. O workflow dedicado passou; Black Arcana CI na mesma HEAD falhou por HTTP 429 na resolução de Gson 2.10.1, não por falha comportamental observada. Nova CI da base consolidada necessária.

A lacuna histórica sobre formato UUID da engine tem evidência posterior reutilizável: [Holocoder — UUID e rejeições estruturais](EXACT-HOLOCODER-ENTITY-LOAD-21.1.250.md) prova CompoundTag.putUUID (Code SHA `acd677efba9098f461f9fa26e60294c51154ed6520a4c80f4937c9bf5f415330`) → NbtUtils.createUUID @6 → UUIDUtil.uuidToIntArray → IntArrayTag de quatro ints. CompoundTag.getUUID (Code SHA `4a7e01f28d3bce4fe1c5f5e70343d417d90e8fbdba5a14c1cbf4d760b8d87483`) lê tag e chama NbtUtils.loadUUID @5, sem hasUUID; tipo/length inválido pode alcançar IllegalArgumentException. A [paridade distribuída](EXACT-ENGINE-248-250-PARITY.md) fixa a engine selecionada. Os wrappers ACCompat e callsites ACWorldData deste dossiê compõem o caminho estático de UUID, sem repetir análise do JAR compartilhada. A forma do valor na tag não prova Tag.write, arquivo físico, recuperação de erro, integridade do mapa completo, stack sincronizada ou efeito efetivo. Não se transfere certificado de Holocoder a Gazing Pearl. NO_MUTATION / NOT_CERTIFIED / NOT_TESTED.
