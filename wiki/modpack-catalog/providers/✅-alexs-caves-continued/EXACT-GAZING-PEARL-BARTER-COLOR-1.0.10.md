# Gazing Pearl — ingresso nativo de barter e fronteira de cor (1.0.10)

**DISCOVERY_ONLY / NO_MUTATION.** Publisher 1.0.10, 75.279.314 bytes, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c32e9f2e95bffae0e7c`, modlist física #019.

## Reuso, não duplicação

[Deep One ingress](EXACT-INK-BOMB-DEEP-ONE-INGRESS-1.0.10.md) já prova generateBarterLoot()List, Code SHA `d3df12394c1f7c4a7f78109c323ba56c1616f02aa2f329dbcb33deb941b09022` e classfile DeepOneBaseEntity SHA `185df23946292e403300849222018480a3cc1397ee6d6d60e0b28abc40e97470`. O método solicita getBarterLootTable @8, ACCompat.lootTable @11, parâmetros THIS_ENTITY/PIGLIN_BARTER @30/37 e getRandomItems @43. Run 45514153339. Não presumir que esse método é chamado por uma interação específica ou entrega item.

A descoberta Gazing Pearl [#1214](https://github.com/Gustavaopere/Black-Arcana/pull/1214), consolidada em [#1213](https://github.com/Gustavaopere/Black-Arcana/pull/1213), observou lambda de tintIndex 0 → getPearlColor → ACColors.opaque(I)I; tintIndex diferente de zero retorna -1. A transformação concreta de opaque é demonstrada abaixo. A entrada deep_one_barter declara peso 26/646, sem chance efetiva garantida.

## Recorte novo

A [sonda](../../../../docs/qa/alexscaves_1010_gazing_pearl_barter_color_probe.py) percorre 1.555 classfiles e resolve família Deep One por herança declarada, Methodref/InterfaceMethodref de generateBarterLoot()List, getBarterLootTable()ResourceLocation, ACColors.opaque(I)I e ACCompat.lootTable(MinecraftServer,ResourceLocation)LootTable. Procura calls tipadas, não nomes aproximados. Registra corpos delimitados das definições e dos callers de generateBarterLoot; outros usuários têm apenas callsites, corpos grandes somente janelas e digests. Não afirma cobertura reflexiva, runtime dispatch ou engine de loot. Se o corpo de opaque é pequeno, registra pivôs opcode/operandos sem incorporar implementação ao runtime.

## Evidência reproduzida e interpretação

[Run 45545268484, job 138973257924](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45545268484/job/138973257924): seis self-checks, dois relatórios idênticos de **46.022 bytes**, SHA-256 `e1ce5e046ce7744c19dc09cf1bd3b4ccf1bb78e42ee7828f41376f4c2a3f231e`. Censo: 14 owners, 22 métodos, quatro classes da família Deep One. A atualização fixa tamanho e digest no workflow; o replay na HEAD consolidada é um gate independente.

- **Cor:** `ACColors.opaque(I)I`, 10 instruções, Code SHA `f241dcfb42ccbd9090e3f0034ea4954962ec3d738c5923b1df4956a40bd7af62`. Testa `c & -67108864` (máscara 0xFC000000) @3. Se não zero, retorna c @14/15; senão, aplica `c | -16777216` (0xFF000000) @10. Em ARGB, força alfa FF somente quando alfa original está entre 0 e 3; não torna arbitrariamente toda cor opaca. Não há call ou escrita própria; sem prova de renderização física.
- **Caller da geração:** `DeepOneBaseEntity.tick`, 360 instruções, Code SHA `a13dfc83b87151ebe13eada286458372f213433d7f091d19becdcaea04107048`, único caller direto de generateBarterLoot observado neste censo tipado. Janela @466–535: getBlockEntity @470; instanceof AbyssalAltarBlockEntity @477 com desvio @480; spawnedLootItem @491 com desvio @494; generateBarterLoot @498; List.isEmpty @505, ItemStack.EMPTY @513 ou List.get(0) @522; guarda local 7 @530, altar.getItem(0) @535. A janela comprova ingresso no ramo do altar e seleção da primeira stack, não a liquidação, custo, transferência, flags posteriores, condições completas do tick ou frequência da troca.
- **Tabela:** `getBarterLootTable` retorna BARTER_LOOT nas variantes regular, Knight e Mage (Code SHA respectivamente `813d36c21c6110844abd17f82e359e22df47fce3f468b12e23428106df384781`, `c8a78a0a746f12f90f35c7261d75ec9b298189a74dd20b616fff94eab7974fb6`, `9e9b09a56b2f944d54bedee44f1cfba2565169ae6a240bb554c1961ee2f67858`). O vínculo com os três literais distintos já está em EXACT-INK-BOMB-DEEP-ONE-INGRESS-1.0.10.md. `ACCompat.lootTable`, seis instruções, Code SHA `0a84a8a5705d6819fb45a3ff9601da0ce3556e6a18c217203c9bd408be4498e2`, solicita MinecraftServer.reloadableRegistries @1, lootKey @5, getLootTable @8. Datapacks/loot efetivo, sorteio real e entrega não foram observados.

A pérola continua sendo um indicador passivo; a troca pertence ao mob/altar, não constitui efeito da pérola. Nenhum novo certificado, raiz, hook, mutação ou QA física.
