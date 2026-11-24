# Galena Gauntlet — restituição e fallback de drop (NeoForge 21.1.248)

## Autoridade e reprodução

Recorte read-only da distribuição oficial Minecraft 1.21.1/Java 21, NeoForge 21.1.248 e Alex's Caves Continued publisher 1.0.10 (SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c32e9f2e95bffae0e7c`, 75.279.314 bytes, versão declarada na modlist sibling). Overlay server `1808fab692dc44b2d474295d1cdd9f1fe8a7dceab4f594210873646fafdf1359`, SRG `26ca9c40d7e1681190b428583c38816852218e78df3f8bdb60a59a78503aec71`, universal `90a56f70425711b4e1a4b94ff0c2904ae9f6d74ca6478b3b2152ac794a07b8e5`. Não é runtime transformado. [Sonda](../../../../docs/qa/alexscaves_1010_galena_return_settlement_probe.py), [workflow](../../../../.github/workflows/alexscaves-1010-galena-return-settlement.yml); [run 45447946764](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45447946764), job 138636784511, artifact 14947725355, HEAD inicial `2fde4396475d804da3bdf511ae515128426bd55d`: relatório de **417.931 bytes**, SHA-256 `cd82ce46cb90d9a4bfb6989a06792619d3207faaeb6c73c55156326cf1951803`, 7 owners. Replay selado na HEAD final exigido.

## Restituição direta

Reutiliza [contrato de retorno publisher](EXACT-GALENA-GAUNTLET-RETURN-DROP-1.0.10.md), Player.addItem @1516 no tick, plopItem @1538 na rota de fallback; proximidade <1,4, entidade não removida e flag de item ainda falsa condicionam a tentativa direta.

| Método e Code SHA-256 | Pivôs |
|---|---|
| Player.addItem(ItemStack):Z — `18211861ab66f18ff7f87baa0d49679e0011b1a2287aab21602b5034c86e284f` | inventory @1, Inventory.add @5, ireturn @8 |
| Inventory.add(ItemStack):Z — `88a803df4e6bc05899284392dd06a9ba323e27736f2c9c0b8b01bc762b9caf54` | slot -1 @1; delega @3 |
| Inventory.add(int,ItemStack):Z — `537ef561768bbce8d07322489e48bb88172711595ab50e6f3c0ed377c0c4c0c1` | vazio -> false @8; danificado: free slot @22, copyAndClear @36, set @39, true @59; sem slot: materiais infinitos -> setCount(0) @72, true @76, senão false @78 |
| Inventory.addResource(int,ItemStack):I — `7a43967e66092ff4087bc15e55bc15b2104e08f6d362535342e4e1fb9d3c4dc9` | count @1, slot @7, vazio copyWithCount(0) @22/setItem @31, min @51, grow @72, retorna quantidade remanescente @82 |
| MagneticWeaponEntity.getItemStack():ItemStack — `5a7e108b8aa00f1f517f5f1658b8b76438a7fd5c3e8de0392319a52a1a0ca0d3` | lê ITEMSTACK de SynchedEntityData @7, cast, retorna sem cópia explícita |

Rota não danificada: contador antes de cada tentativa @80, addResource @92 ou @105, setCount @95 ou @108. Loop @123 continua se não vazio e contagem reduzida. Na saída sem progresso, branch @131 distingue igualdade; materiais infinitos podem zerar @146, true @150. Último teste @156 retorna true apenas se contagem menor que a lida na tentativa anterior. Logo existe mutação parcial antes do booleano; última tentativa sem progresso pode retornar false depois de inserção parcial anterior. Fallback deve considerar remanescente, não quantidade inicial. Aliasing de SynchedEntityData, listeners e conservação de componentes não observados fisicamente.

## Fallback e pickup

- MagneticWeaponEntity.plopItem()V — Code SHA `e8cba231f5515acb557aed34f2ad0b28fb377c7e33b10edfd6be600a213f21cf`: flag @1, ifne @4 ->29; flag true @9 antes de getItemStack @14 e ACCompat.spawnAtLocation @17; ifnull @22 ->29, caso não nulo setNoPickUpDelay @26. Ambas as rotas chegam a DISCARDED @30/remove @33.
- ACCompat.spawnAtLocation(Entity,ItemStack):ItemEntity — `505d89864837abd20cf36829273586fcff20e07d7cbe828010d73481e2311ed6` delega @2; Entity.spawnAtLocation(ItemStack) — `ad2381445c0158ed7f18d3ea18cdde937b4e60871c649a9b2909bc6c3d7945d5` encaminha offset vertical 0F @2.
- Entity.spawnAtLocation(ItemStack,F) — `66b52346286507a13530b4a79e609d513767ec284728f159f4a35c9fa7cbcbd9`: vazio @1/4 retorna null @8; cliente @13/16 retorna null @20; constrói ItemEntity @45 em X/Y+offset/Z com stack passada; setDefaultPickUpDelay @50; captureDrops @54; se não nulo Collection.add @65 com pop @70; caso nulo Level.addFreshEntity @79 com booleano descartado antes do areturn @84. **Referência não nula não certifica admissão:** objeto pode estar na coleção de captura ou ter recebido false de spawn. Reutiliza [guardas de recusa](EXACT-GALENA-SPAWN-DENIAL-GUARDS-21.1.248.md), sem afirmar que recusa ocorreu fisicamente.
- ItemEntity.playerTouch(Player) — `385f37f0782198e1f91514efebabd9dce69540057d5b429d1e4a9341edc87b4a`: guarda cliente @4/7; Pre @28, canPickup @31, false @38/41 retorna; cópia @46; isTrue @53 ou pickupDelay @60/target UUID @67–81; Inventory.add @92/95; Post @102, diferença de contagem e take @121; vazio -> discard @132; estatística @142 e seguintes. Pickup posterior é distinto da inserção direta. Pre/Post, referência retornada, flag e remoção não são recibo de restituição.

## Limites e QA

Owners adicionais ItemStack e CommonHooks (toss distinto). Não comprova execução pós-ModLauncher, listeners, captura real de drops, atomicidade, owner/claims, save/reload, perdas ou duplicação. QA dedicada: mão cheia, inserção parcial, arma danificada, materiais infinitos, cancelamento do spawn inicial/drop/pickup, captura, troca de dimensão/reload; contabilizar quantidade antes/depois em mãos, inventário, entidade controlada, drop e descarte. Não presumir compensação externa. `static_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`, `provider_universe_closed=false`. Sem alteração de runtime ou ledger.
