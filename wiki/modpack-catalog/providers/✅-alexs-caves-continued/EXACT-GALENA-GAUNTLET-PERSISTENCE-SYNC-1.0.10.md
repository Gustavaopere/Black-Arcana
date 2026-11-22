# Galena Gauntlet — persistência NBT, dados sincronizados e controlador (Alex's Caves Continued 1.0.10)

**Estado:** ⚠️ **subcontrato estático SHA-exato, somente leitura**. O objeto `alexscaves:galena_gauntlet` mantém `static_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`, `provider_universe_closed=false`. Esta prova **não** certifica recuperação da arma, integridade transacional, reload, sincronização física, Mastery/XP ou lifecycle multijogador.

## 1. Proveniência, identidade e escopo

- **Fonte física de versão:** [modlist do sibling](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/main/PROJECT-INSTRUCTIONS/modlist/World%20Gen/%E2%9C%85-alexs-caves-continued%20v1.0.10.md), registro da instalação 1.21.1/NeoForge do JAR `alexscaves-1.0.10-neoforge+1.21.1.jar`, mod ID `alexscaves`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570` (modlist datada de setembro de 2026). **Paridade byte a byte com um novo dump da instalação: `NOT_VERIFIED`**.
- **JAR publisher examinado:** 75.279.314 bytes; SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **Classe:** `com/github/alexmodguy/alexscaves/server/entity/item/MagneticWeaponEntity`; classfile SHA-256 `a26794c9eba89c554e812078886beda6129d5298219f685f6d0e2be315fbf071`. O censo encontrado: **17 campos, 24 métodos executáveis**, dentre 1.555 classfiles varridos no JAR.
- **Relatório original reutilizado:** [CI #45071358036](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45071358036), [artefato #14773961125](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45071358036/artifacts/14773961125); `report.json` de 1.780.492 bytes SHA-256 `c91a48f9892be09c4ab951c8083703b0c5ffbb026fc43e7d808c2033dde8bba9`. A auditoria atual verifica **12 corpos de método, 126 pivôs JVM**, descritores, hashes Code e da desassemblagem, nomes/descritores de campos e 16 mutações adversariais que devem ser rejeitadas causalmente. A prova anterior sobre o raycast, dano e mineração não substitui a certificação independente destas chamadas.
- **Arquivos reproduzíveis:** [manifesto](EXACT-GALENA-GAUNTLET-PERSISTENCE-SYNC-1.0.10.json), [verificador e testes negativos](../../../../docs/qa/alexscaves_1010_galena_persistence_sync_checks.py), [workflow dedicado](../../../../.github/workflows/alexscaves-1010-galena-persistence-sync.yml). A CI baixa o JAR publisher, verifica SHA-256 e reproduz o relatório antes de comparar os pivôs; nenhuma implementação proprietária é incluída no mod.

## 2. Dois canais de identidade do controlador — não intercambiáveis

`getController():Entity` usa **ramos diferentes por lado**. O método consulta `Level.isClientSide()` @4–7:

| Contexto do método | Origem da identidade | Caminho JVM | Resultado observável |
|---|---|---|---|
| Servidor (`isClientSide=false`) | `getControllerUUID()` @11, que lê `CONTROLLER_UUID` via `SynchedEntityData.get` e `Optional.orElse(null)` @4–20 | Se UUID nulo, retorna `null` @16–20; se presente, pede `ServerLevel.getEntity(UUID)` @27–31 | **Solicita** lookup por UUID na dimensão atual. Retorno positivo após unload/restart/mudança de dimensão **não demonstrado**. |
| Cliente (`isClientSide=true`) | `CONTROLLER_ID` @39, `Integer.intValue` @48 | Se `id == -1`, retorna `null` @53–58; caso contrário, pede `Level.getEntity(int)` @65–66 | Lookup por **ID de entidade**, não UUID. O ID não é identidade durável para persistência nem prova de owner resolvido. |

`setControllerUUID(UUID)` escreve `Optional.ofNullable(uuid)` no accessor `CONTROLLER_UUID` @4–11; `getControllerUUID()` lê seu `Optional` @4–20. **`CONTROLLER_UUID` e `CONTROLLER_ID` são accessors diferentes**, de semântica e estabilidade distintas. É incorreto vincular uma perk persistente ao ID transitório do cliente ou tratar o resultado de `getController()` como prova de autoria de um hit.

No ramo **Teletor** de `tick`, a entidade solicita `CONTROLLER_ID = TeletorEntity.getId()` @185–195; na rota do **Player** solicita `CONTROLLER_ID = Entity.getId()` @490–500. Para Teletor, o `TARGET_ID` é preenchido a partir de seu `getTarget()`, condicionado a alvo não nulo e `isAlive()` @216–254, senão `-1`. O ramo de destino do jogador não herda automaticamente essa seleção de target. O código local **não demonstra** quando o pacote de sincronização chega ao cliente.

## 3. Estrutura de dados sincronizados, tipos e defaults

`<clinit>()` constrói os cinco accessors por `SynchedEntityData.defineId` usando os serializers citados no classfile. `defineSynchedData(Builder)` pede exatamente estas inicializações **locais**:

| Accessor | Serializer indicado no `<clinit>` | Valor declarado em `defineSynchedData` | Evidência JVM |
|---|---|---|---|
| `ITEMSTACK` | `EntityDataSerializers.ITEM_STACK` | Novo `ItemStack(Items.IRON_SWORD)` | `<clinit>` @2–8; `defineSynchedData` @1–14 |
| `CONTROLLER_UUID` | `ACEntityDataRegistry.OPTIONAL_UUID.get()` → `EntityDataSerializer` | `Optional.empty()` | `<clinit>` @13–27; `defineSynchedData` @19–25 |
| `CONTROLLER_ID` | `EntityDataSerializers.INT` | `Integer.valueOf(-1)` | `<clinit>` @32–38; `defineSynchedData` @30–37 |
| `TARGET_ID` | `EntityDataSerializers.INT` | `Integer.valueOf(-1)` | `<clinit>` @43–49; `defineSynchedData` @42–49 |
| `IDLING` | `EntityDataSerializers.BOOLEAN` | `Boolean.TRUE` | `<clinit>` @54–60; `defineSynchedData` @54–61 |

`getItemStack()` devolve a stack do accessor `ITEMSTACK` @4–13; `setItemStack(stack)` solicita sua escrita por `SynchedEntityData.set` @4–11. `getTarget()` lê `TARGET_ID` @4–16: **−1 → `null`** @17–23; outro ID → `Level.getEntity(id)` @26–31. O nome `TARGET_ID` e sua leitura não certificam targeting, legitimidade do alvo ou persistência.

**Atenção:** `Items.IRON_SWORD` é o **valor inicial declarado do builder**, e não uma prova de qual arma reaparece após desserialização parcial. Não presumir fallback seguro se o campo `WeaponStack` estiver ausente/corrompido; não foi testado.

## 4. O que os métodos NBT realmente solicitam

`addAdditionalSaveData(CompoundTag)` escreve condicionalmente **duas chaves** neste corpo:

1. Se `getItemStack().isEmpty()` for **false** @1–7, escreve `"WeaponStack"` @11, obtém `level().registryAccess()` @15–18, solicita `ACCompat.saveStack(provider,stack)` @21–25 e passa o resultado a `CompoundTag.put` @28.
2. Se `getControllerUUID() != null` @33–36, escreve a chave `"ControllerUUID"` @40, via `ACCompat.putUUID(tag,key,uuid)` @47.

`readAdditionalSaveData(CompoundTag)` espelha as duas presenças, sem afirmar equivalência física:

1. Se `CompoundTag.contains("WeaponStack")` @1–7, solicita `ACCompat.getCompound`, `ACCompat.loadStack` com registry access e `setItemStack` @19–28.
2. Se `ACCompat.hasUUID(tag,"ControllerUUID")` @32–38, solicita `ACCompat.getUUID` e `setControllerUUID` @41–49.

**Campos não escritos por esses dois overrides:** `CONTROLLER_ID`, `TARGET_ID`, `IDLING`, `playerUseCooldown`, `comingBack`, `strikeProgress`, `returnProgress`, `destroyBlockProgress`, `totalMiningTime`, `hadPlayerController`, `spawnedItem`, `returnFlag` e os demais campos transientes do censo. O construtor `<init>` inicializa explicitamente `playerUseCooldown`, `comingBack`, `totalMiningTime`, `hadPlayerController`, `spawnedItem` e `returnFlag` como zero/false @6–33. **Isso não demonstra se/ou quando a engine salva outros dados por herança, repovoa IDs, reconstitui entidades nem garante conservação após restart**. A semântica dos métodos de `ACCompat` ainda exige observação isolada.

## 5. Consequências para integração, segurança e Mastery

- **Autoria:** UUID do controller no servidor é um candidato de identidade persistente, mas `getEntity(UUID)` pode retornar `null`. Não conceder Mastery/XP com base isolada no ID de cliente, no alvo sincronizado, em `setLastHurtByPlayer` ou no trigger de conquista. A causalidade de dano/abate final permanece `NOT_VERIFIED`.
- **Item original:** `onUseTick` do item coloca `setCount(0)` antes da tentativa `addFreshEntity` (auditoria anterior). As rotas de retorno `Player.addItem`/`ACCompat.spawnAtLocation` não provam recuperação após falhas de spawn, inventário cheio, crash ou desconexão. Este subcontrato NBT **não fecha atomicidade** nem evita duplicação ou perda.
- **Vida útil e reconexão:** progresso/temporizadores não aparecem no override NBT; é necessário testar reinício/dimensão, target stale, recomposição de UUID/ID, estado de cooldown, item quebrado e colisão/entidade ausente. Não assumir que defaults de `SynchedEntityData` são defaults de restaurar mundo.
- **Boundary e autoridade:** nenhum hook de modificação segura por jogador, rede ou lifecycle foi demonstrado; Black Arcana é autoridade de seu próprio runtime e policy, RPG Skill Tree é sibling/provider de progressão, atributos, Mastery e gates apenas por contrato real. Permanece **`NO_MUTATION` / fail-closed**.

## 6. Validação, limites e próximos gates

Execução reproduzível contra o relatório verificado:

```sh
python3 docs/qa/alexscaves_1010_galena_persistence_sync_checks.py \
  --report build/galena-persistence-1010/report.json \
  --manifest 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-GALENA-GAUNTLET-PERSISTENCE-SYNC-1.0.10.json' \
  --adversarial
```

É obrigatório baixar o publisher SHA-exato e reconstruir o `report.json` via `docs/qa/alexscaves_1010_galena_gauntlet_discovery.py` antes da comparação em CI. Os testes adversariais re-selam os hashes de relatório/instruções para garantir rejeição **causal** de 16 alterações de opcode e destino de salto, não apenas rejeição pela diferença de SHA.

**Pendências não certificadas:** corpos de `ACCompat.saveStack`, `ACCompat.loadStack`, `ACCompat.hasUUID/getUUID/putUUID`, `SynchedEntityData`/serialização real da engine, salvamento de entidade por herança, cancelamentos, restart/dimension travel, chunk unload, inventário e drop, persistência física, targeting e autoria de kill. A operação é apenas de análise estática; **sem mudança de runtime, casts, índices gerados, certificados ou numeradores**.

**Clean-room:** descrições originais de observações e callsites de interoperabilidade; não foram copiados source, bytecode, assets nem implementações proprietárias para o runtime Black Arcana.
