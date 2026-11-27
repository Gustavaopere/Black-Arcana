# Gazing Pearl — vínculo ACPlatform invokeddynamic/BootstrapMethods 1.0.10

**Estado:** ⚠️ PARCIAL — análise de bytecode, sem certificação do item. `static_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`. O adaptador é infraestrutura de persistência, não uma magia, cast, buff ou hook de escrita.

## Proveniência e reprodução

Provider da modlist sibling: `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 registrado `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`; publisher auditado de **75.279.314 bytes**, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, 1.555 classfiles. Identidade SHA-256 do JAR físico instalado ainda **NOT_VERIFIED**.

[Run #45013296440](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45013296440), [artifact #14750956691](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45013296440/artifacts/14750956691), `report.json` de **6.664 bytes**, SHA-256 `5c78b78eba2c51073ff606d8f7b5389b2a5dbfc895877109284a7a2dd9ddca16`. Classfile `com/github/alexmodguy/alexscaves/server/misc/ACPlatform` SHA-256 `662a4d2593fe515ed8790bad06d8184d1eb921423033dfd11b3b44142dedc3e6`; tabela `BootstrapMethods` tem **3 entradas**, digest normalizado `39f12f4b2cc048839381d6964b36bbea75c183cc80e9e86b9dc29c984bfee75f`.

[Probe read-only](../../../../docs/qa/alexscaves_1010_gazing_pearl_acplatform_bootstrap_probe.py), [manifesto de ligação JVM](EXACT-GAZING-PEARL-ACPLATFORM-BOOTSTRAP-1.0.10.json), [checker fail-closed](../../../../docs/qa/alexscaves_1010_gazing_pearl_acplatform_bootstrap_checks.py) e [workflow](../../../../.github/workflows/alexscaves-1010-gazing-pearl-bootstrap-discovery.yml). A primeira coleta do JAR já passou; a CI integral da HEAD do manifesto/checker ainda exige execução separada.

## Vinculação causal de fábrica — classfile 1.0.10

- `ACPlatform.computeIfAbsent(DimensionDataStorage,Function,Function,Supplier,String):SavedData`, **11 instruções**, Code SHA-256 `66492d422ecbe213c0fc8b337f300693b25341c69690610806b86b906c4e78b3`, instruction SHA `625899b736db7a61455db4301becd6996444ea6f58c897da47084cb7a44a3903`. Contém um único `invokedynamic` no offset **@7**, operando JVM `#136, 0`, nome/descriptor `apply:(Function)BiFunction`. O índice **136** do constant pool é do tipo `CONSTANT_InvokeDynamic` e referencia a entrada **0** de `BootstrapMethods`.
- **Bootstrap #0:** handler `REF_invokeStatic java/lang/invoke/LambdaMetafactory.metafactory`. Argumentos: MethodType genérico `(Object,Object):Object`; MethodHandle `REF_invokeStatic ACPlatform.lambda$computeIfAbsent$1`; MethodType adaptado `(CompoundTag,HolderLookup.Provider):SavedData`. O vínculo exato ao loader local é, portanto, diretamente suportado pelo classfile, não só inferido a partir de coincidência de nomes.
- **Loader implementado:** `ACPlatform.lambda$computeIfAbsent$1(Function,CompoundTag,HolderLookup.Provider):SavedData`, **5 instruções**, Code SHA `5cbb0594bcb4ff83d01c6b409af2de04871b173a69c6ec087c18f4e6f44af60e`, instruction SHA `664d874cd05f359896963334f4c5b3cf81137b1723d2aa4e500aa717979df553`. Executa `Function.apply(CompoundTag)` @2, `checkcast SavedData` @7, retorna @10. Não lê o `HolderLookup.Provider` local 2.
- **Encaminhamento do wrapper:** `Supplier` local 3 @5 e primeira `Function` local 1 @6 alimentam `invokedynamic`; a segunda `Function` local 2 não é lida em nenhum offset. Cria `SavedData.Factory(Supplier,BiFunction,null)` em @13, fornecendo `DataFixTypes=null`, depois delega a `DimensionDataStorage.computeIfAbsent` @18 com a chave de storage.

O checker verifica hash SHA-exato do classfile e das instruções, operando do constant pool, índice do bootstrap, tipos e identidade do MethodHandle, descritores e pivôs de execução. O relatório não carrega classes do publisher nem executa a JVM do mod.

## Consumidores e limites

O grafo de chamadas já auditado nos dossiês [ACPlatform/SavedData](EXACT-GAZING-PEARL-ACPLATFORM-1.0.10.md) e [ACWorldData reputacional](EXACT-GAZING-PEARL-WORLDDATA-1.0.10.md) permanece: `GazingPearlItem.acInventoryTick → ACWorldData.get(Level) → ACPlatform.computeIfAbsent → DimensionDataStorage.computeIfAbsent`. A Gazing Pearl lê a reputação do UUID e atualiza um snapshot na ItemStack; a ponte genérica **não** adiciona efeito mágico nem direito de alteração por perk.

`CitadelServerData.get` é o segundo caller direto do helper genérico, com chave `alexscaves_citadel_world_data`, mas isso não representa um segundo cast ou fonte de reputação da pérola.

**Dano, mana, custo, AOE, projectile, cooldown e targeting ofensivo:** **N/A** para a ponte de storage. A análise estática **não confirma** a execução da lambda no mundo, a política efetiva da engine `SavedData.Factory`, cache, salvamento/rollback, arquivo `.dat` real, sincronização de `CUSTOM_DATA`, comportamento de renderização, exposição de hook seguro por jogador ou QA no modpack. Necessário examinar a versão exata de NeoForge e o arquivo instalado, além de testes físicos no cliente/servidor. **NO_MUTATION / fail-closed**; sem incremento nos objetos ou certificados.
