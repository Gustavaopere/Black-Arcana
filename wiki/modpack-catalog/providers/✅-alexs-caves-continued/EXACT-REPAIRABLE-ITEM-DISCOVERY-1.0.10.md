# ACRepairableItem — descoberta SHA-exata 1.0.10

**Estado:** DISCOVERY_NOT_CERTIFIED / NO_MUTATION. Escopo da elegibilidade de material, não do reparo executado.

Artefato publisher Alex's Caves Continued 1.0.10, Minecraft 1.21.1, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, 75.279.314 bytes. A [prova executável](../../../../docs/qa/alexscaves_1010_repairable_item_probe.py) verificou o JAR e censou 1.555 classfiles. Interface `server/item/ACRepairableItem`, SHA-256 `04a9b942d2459794503eebc1415a29c245710a0625f1a126f5df2714266d6a05`, flags 1537, zero campos e três métodos.

## API e causalidade

| Método | Contrato observado |
|---|---|
| acExtraRepairMaterials()[Lnet/minecraft/world/item/Item; | abstrato; cada implementador fornece array de itens |
| acReplacesTierRepairMaterials()Z | default retorna false; DesolateDaggerItem retorna true |
| isExtraRepairMaterial(ACRepairableItem,ItemStack)Z | chama o getter @1, itera array e testa ItemStack.is(Item) @28; retorna true no primeiro match @35, false sem match @43 |

Não há consumo, alteração de durabilidade, XP, cálculo de custo ou validação de jogador no helper. Não há guarda local de array/stack nulo, nem deduplicação. O getter de cada implementador observado produz array novo; suppliers do registry são consultados durante o getter.

## Cinco implementadores diretos

| Classe | Campo de material observado | isValidRepairItem |
|---|---|---|
| DesolateDaggerItem | ACItemRegistry.PURE_DARKNESS | somente extra, @2; sem super |
| ExtinctionSpearItem | ACItemRegistry.TECTONIC_SHARD | extra OR super SpearItem @11 |
| GalenaGauntletItem | ACBlockRegistry.PACKED_GALENA → Block.asItem @17 | extra OR Item @11 |
| PrimitiveClubItem | ACItemRegistry.HEAVY_BONE | extra OR Item @11 |
| ResistorShieldItem | ACItemRegistry.SCARLET_NEODYMIUM_INGOT e AZURE_NEODYMIUM_INGOT | extra OR ShieldItem @11 |

Nos quatro últimos, extra true desvia diretamente para true; o super só é consultado se extra false. Os campos referenciados não são prova de IDs de registry executados. SpearItem é ancestral nativo; resolução do fallback e fronteiras Item/ShieldItem/ItemStack e do anvil ainda exigem auditoria de referência. O nome do booleano acReplacesTierRepairMaterials não prova dispatch: zero member refs nativos a esse método no censo exato; o override de reparo do dagger implementa a substituição diretamente.

## Evidência e limites

Censo: seis owners com referências tipadas a membros da interface (ela própria e os cinco implementadores), zero implementadores indiretos, um ancestral nativo. [Manifesto](EXACT-REPAIRABLE-ITEM-DISCOVERY-1.0.10.json) fixa as declarações, hashes de métodos e sites de material/delegação. [Job](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44452078303/job/135318206682) aprovado, relatório SHA-256 `6b930d9bc296c736278df961dea6db3b0af31789b39fd623df4cdea232016b2f`.

Não é uma habilidade mágica adicional, não certifica os cinco equipamentos completos ou o repair settlement. Aplicabilidade de perks de custo/durabilidade, quantidade consumida, XP/anvil, sidedness, eventos e segurança por jogador permanecerão separados. Sem hook real verificado: NO_MUTATION/fail-closed. Próximos gates: replay de evidência, boundary oficial vanilla/NeoForge, registry e reconciliação das PRs #1122/#1123 antes de qualquer promoção de ledger.
