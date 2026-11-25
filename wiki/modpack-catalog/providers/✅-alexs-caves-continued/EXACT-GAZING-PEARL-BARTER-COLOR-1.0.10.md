# Gazing Pearl — ingresso nativo de barter e fronteira de cor (1.0.10)

**DISCOVERY_ONLY / NO_MUTATION.** Publisher 1.0.10, 75.279.314 bytes, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c32e9f2e95bffae0e7c`, modlist física #019.

## Reuso, não duplicação

[Deep One ingress](EXACT-INK-BOMB-DEEP-ONE-INGRESS-1.0.10.md) já prova generateBarterLoot()List, Code SHA `d3df12394c1f7c4a7f78109c323ba56c1616f02aa2f329dbcb33deb941b09022` e classfile DeepOneBaseEntity SHA `185df23946292e403300849222018480a3cc1397ee6d6d60e0b28abc40e97470`. O método solicita getBarterLootTable @8, ACCompat.lootTable @11, parâmetros THIS_ENTITY/PIGLIN_BARTER @30/37 e getRandomItems @43. Run 45514153339. Não presumir que esse método é chamado por uma interação específica ou entrega item.

A descoberta Gazing Pearl [#1214](https://github.com/Gustavaopere/Black-Arcana/pull/1214), consolidada em [#1213](https://github.com/Gustavaopere/Black-Arcana/pull/1213), observou lambda de tintIndex 0 → getPearlColor → ACColors.opaque(I)I; tintIndex diferente de zero retorna -1. A transformação concreta de opaque ainda não foi examinada. A entrada deep_one_barter declara peso 26/646, sem chance efetiva garantida.

## Recorte novo

A [sonda](../../../../docs/qa/alexscaves_1010_gazing_pearl_barter_color_probe.py) percorre 1.555 classfiles e resolve família Deep One por herança declarada, Methodref/InterfaceMethodref de generateBarterLoot()List, getBarterLootTable()ResourceLocation, ACColors.opaque(I)I e ACCompat.lootTable(MinecraftServer,ResourceLocation)LootTable. Procura calls tipadas, não nomes aproximados. Registra corpos delimitados das definições e dos callers de generateBarterLoot; outros usuários têm apenas callsites, corpos grandes somente janelas e digests. Não afirma cobertura reflexiva, runtime dispatch ou engine de loot. Se o corpo de opaque é pequeno, registra pivôs opcode/operandos sem incorporar implementação ao runtime.

Primeira execução, replay e interpretação ainda pendentes. Nenhum novo certificado, raiz, hook, mutação ou QA física.
