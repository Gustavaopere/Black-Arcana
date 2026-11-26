# Quarry Smasher

**Estado:** ⚠️ PARCIAL / STATIC_DISCOVERY_ONLY. `static_contract=NOT_CERTIFIED; mutating_hook=NOT_VERIFIED; physical_qa=NOT_TESTED; NO_MUTATION`. Sem nova raiz semântica certificada.

**Autoridade:** Alex's Caves Continued (alexscaves) 1.0.10, Minecraft 1.21.1 / NeoForge / Java 21; modlist sibling #19. Publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c32e9f2e95bffae0e7c`. [Replay](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45748227744/job/139669398914), HEAD `247a4c7adec94b3c99a28fd1aadb668b07dc3ef3`, dois relatórios byte-idênticos de 156.541 bytes, SHA-256 `2bd27341d274f749e8c80b0a0e77e6f37571a92545293d910e7b47deb1cdb945`. [Dossiê](../EXACT-QUARRY-RADIANT-FOOD-1.0.10.md). Sem novo dump instalado ou configuração efetiva.

## Identidade e descrição funcional

`alexscaves:quarry_smasher`; owner `QuarrySmasherItem`; factory `ACItemRegistry.lambda$static$16`, Code SHA-256 `8eedb42718de2b1062ad616449d83c8b6577741845712c901bd1fbb73a7c70f6`. [Registro](../systems/item-registry.md). Item de instalação de entidade de mineração. Descrição interpretativa do binário.

## Ativação, targeting, posicionamento e custo

Factory stacksTo(1). use(Level,Player,InteractionHand) obtém stack da mão @2 e getPlayerPOVHitResult com ClipContext.Fluid.ANY @12 (alcance do helper herdado não certificado; não igualar aos 5 blocos da consulta abaixo). MISS retorna usePass @30. Consulta entidades em AABB do jogador expandida na direção da visão×5D e inflada 1D (@35–70), excluindo o jogador pelo argumento de getEntities; ENTITY_PREDICATE = NO_SPECTATORS AND Entity.isPickable (bootstrap @3 de <clinit>). Para cada entidade consultada, testa se a posição dos olhos do jogador está contida na AABB da entidade inflada por seu pickRadius; se sim retorna usePass @150. Não é um raycast de entidade nem prova de ausência de colisões no trajeto.

Somente hit BLOCK segue a criação: ACEntityRegistry.QUARRY_SMASHER → ACCompat.createEntity @187; cast QuarrySmasherEntity, setPos no ponto de hit, yaw do jogador, setInactive(true) @227. Level.noCollision(entidade, boundingBox) @238; false retorna useFail. Nenhuma guarda de null demonstrada antes do uso da entidade. Servidor: addFreshEntity @260 (booleano descartado), gameEvent ENTITY_PLACE @271, shrink(1) @287 se !instabuild. awardStat ITEM_USED @298 está fora do gate de lado; useSidedSuccess @307. Não confundir solicitação de spawn, evento, débito e resultado efetivo; falha de addFreshEntity não condiciona o débito no corpo observado.

## Efeitos e integração

O item produz uma solicitação de instalação da entidade QuarrySmasherEntity em estado inicialmente inativo. Não demonstrado neste owner: dano, tipo de dano, AOE de mineração, velocidade, dimensões, ativação subsequente, combustível, owner/UUID, NBT, despawn, persistência e permissões de quebra. Não extrapolar a AABB de detecção do jogador para a área de mineração. Sem mana/cooldown/XP próprios demonstrados. Auditar entidade, registry, bloco/estrutura, callbacks e bridge ACCompat, engine, WorldEffectPolicy/claims e settlement. Não repetir spawn, shrink ou evento, nem conceder Mastery por tentativa.

## Aquisição declarativa

`data/alexscaves/recipe/quarry_smasher.json` SHA-256 `e6f26cf2825ae031a4e830b9415b341b00422cdc90b57c6e4cecf3c0bf0166d6`. Padrão AAA/CCC/SHS; A=azure_neodymium_ingot, C=minecraft:chain, S=scarlet_neodymium_ingot, H=heavyweight. Resultado count=1. Não garante aquisição no modpack.

## Localizadores de evidência

Classfile SHA-256 `bf8fe4f6404e3d46f085bc708eb6a260f598cab0fc0a1dec0806bf066fd790d4`.

| Método e descritor | Instruções | Code SHA-256 |
|---|---:|---|
| `<init>(Lnet/minecraft/world/item/Item$Properties;)V` | 4 | `405f81f0b51683db4ab14a729fb164a2c889439967d0bfe6248ebe8183a4873d` |
| `use(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/InteractionHand;)Lnet/minecraft/world/InteractionResultHolder;` | 136 | `786b7fe42e93b146d38e303dbe59e941116448b5a22ecc189f35a3ed63387d7d` |
| `<clinit>()V` | 5 | `fef0684a920e2ab5723f466be061dd4b92fc7ea4ca22187244b6aa7c3c85988f` |
