# ACRepairableItem — elegibilidade de materiais de reparo

**Contrato técnico estático:** ✅ CERTIFIED_STATIC_7_AXES / STATIC_TECHNICAL_CATALOG_ONLY, candidato #1124. **Hook:** NOT_VERIFIED. **Runtime:** NOT_VERIFIED. **QA física:** NOT_TESTED. **Perk:** NOT_CERTIFIED. **Policy:** NO_MUTATION. Provider OPEN; zero novas raízes mágicas.

## Identidade e ativação

Interface com.github.alexmodguy.alexscaves.server.item.ACRepairableItem, mod ID alexscaves, publisher 1.0.10, Minecraft 1.21.1, Java 21, referência NeoForge 21.1.250. SHA-256 classe 04a9b942d2459794503eebc1415a29c245710a0625f1a126f5df2714266d6a05; JAR SHA-1 6960b299a39a039ac8a5eb9b07be4ad0e3e0a570, SHA-256 36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c, 75279314 bytes. Dossiê físico confirmado na main do sibling ce8c5e30237ce9bc5c258a0de26f8a08c22c88aa. Não é magia ou item de registry independente. Ativação: chamada isValidRepairItem(equipamento, material); loader em execução não observado.

## Métodos, consumidores e parâmetros

| Superfície | Contrato |
|---|---|
| acExtraRepairMaterials()[Lnet/minecraft/world/item/Item; | abstrato; cinco implementadores criam array novo e resolvem supplier |
| acReplacesTierRepairMaterials()Z | default false; DesolateDagger true; nenhum member ref nativo comprovado |
| isExtraRepairMaterial(ACRepairableItem,ItemStack)Z | getter @1, loop, ItemStack.is(Item) @28, true @35 no primeiro match e false @43 sem match; nenhuma guarda local de null |
| isValidRepairItem(ItemStack,ItemStack)Z | override dagger só extra @2; outros extra ou super @11, curto-circuito |

| Equipamento | Material | Identidades | Fallback |
|---|---|---:|---|
| DesolateDaggerItem | pure_darkness | 1 | nenhum |
| ExtinctionSpearItem | tectonic_shard | 1 | SpearItem -> Item |
| GalenaGauntletItem | packed_galena (Block.asItem) | 1 | Item |
| PrimitiveClubItem | heavy_bone | 1 | Item |
| ResistorShieldItem | scarlet_neodymium_ingot, azure_neodymium_ingot | 2 | ShieldItem |

Cinco caminhos de item vinculados no [ACItemRegistry](item-registry.md), packed_galena no helper de bloco. Ver [offsets, hashes e descriptors](../EXACT-REPAIRABLE-ITEM-DISCOVERY-1.0.10.json) e [fronteira](../EXACT-REPAIRABLE-ITEM-BOUNDARY-1.0.10.md). Censo de 1555 classes: cinco diretos, zero indiretos, seis owners tipados incluindo a interface e um ancestral nativo. A regra extra usa identidade de Item (referência vanilla), não NBT, count ou tag nesse overload. ShieldItem usa PLANKS ou super; Item=false na referência oficial não transformada.

## Custos, efeitos e integração

A interface não restaura durabilidade por si; não consome material, experiência ou mana e não tem cooldown próprio. Na referência vanilla AnvilMenu.createResult, após damageable e isValidRepairItem aceito, cada unidade pede r=min(D,floor(M/4)), D dano acumulado, M durabilidade máxima; r<=0 invalida o ramo inicial; loop até r<=0 ou count atingido, incrementando custo base e contador de unidades. onTake solicita débito de níveis quando não instabuild e liquida slots; custo total inclui outros caminhos externos. Não extrapolar o helper para XP, Mending ou grindstone.

AnvilUpdateEvent (CommonHooks.onAnvilChange) pode substituir output/custo/materialCost ou cancelar; AnvilRepairEvent (CommonHooks.onAnvilRepair) retorna breakChance da bigorna. Referências oficiais, não integração autorizada. Perks de materiais alternativos, custo ou potência precisam de contrato server-side com transação e dedupe; não repetir reparo após onTake. Mastery não é creditada pela consulta de elegibilidade. Black Arcana autoridade de magia; RPG Skill Tree provider de progressão. NO_MUTATION/fail-closed.

N/A justificado: cast, targeting de entidade, dano direto/tipo, AOE, LOS, duração, projétil, summons, owner, persistência própria, cooldown e aplicação de efeitos. Equipamento/stack e regra booleana são o recorte; player aparece na transação externa. NÃO VERIFICADO: registry ativo, tags, transforms, listeners, transação real, resultado final, segurança PvP/world, QA física.

[Contrato](../EXACT-REPAIRABLE-ITEM-CONTRACT-1.0.10.md) · [selo](../EXACT-REPAIRABLE-ITEM-CONTRACT-1.0.10.json) · [descoberta](../EXACT-REPAIRABLE-ITEM-DISCOVERY-1.0.10.md) · [boundary](../EXACT-REPAIRABLE-ITEM-BOUNDARY-1.0.10.json). Relatórios 6b930d9bc296c736278df961dea6db3b0af31789b39fd623df4cdea232016b2f e 03519b95b38412c1efccba0157f83c59dffc0e865dd55efe05c7c779ed2e789a reproduzidos no job 135321798629 (9 testes). Próximo ACSwingControlItem; CI final exigida.
