# Submarine

**Estado:** ⚠️ PARCIAL / STATIC_DISCOVERY_ONLY. `static_contract=NOT_CERTIFIED; mutating_hook=NOT_VERIFIED; physical_qa=NOT_TESTED; NO_MUTATION`. Sem nova raiz semântica certificada.

## Identidade e autoridade
`alexscaves:submarine`, owner `SubmarineItem`, factory `ACItemRegistry.lambda$static$98`, Code SHA-256 `230455d831544af1585d3aa7b09b67eae3496a0ea6e124691121a4427c13f618`. [Registro](../systems/item-registry.md). Alex's Caves Continued 1.0.10, Minecraft 1.21.1/NeoForge/Java21, modlist sibling #19; JAR publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, 75.279.314 bytes. [Dossiê](../EXACT-LATE-CONCRETE-ITEMS-1.0.10.md), [run/job](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45794089694/job/139820167569), HEAD `27c5bbc7780abbb2efe9bf2c4db615be5d0e7b3c`, dois replays byte-idênticos 425337 bytes, SHA-256 `aa6b3b052b975590f56dd2fa62773fe907346495093ef1842b0405de17b585a2`. Sem dump físico novo.

## Instalação, targeting e custo
Factory stacksTo(1), UNCOMMON. use(Level,Player,Hand) getPlayerPOVHitResult(Fluid.ANY), MISS pass. Consulta AABB jogador expandida pela visão×5D e inflada1D, filtro NO_SPECTATORS AND isPickable; bloqueia se olhos contidos em AABB candidata inflada pickRadius. Não é raycast de entidade; 5D não prova alcance do helper. Hit BLOCK cria SubmarineEntity via ACCompat.createEntity, posiciona no hit, yaw do Player; playSound SUBMARINE_PLACE @237 **antes** de noCollision @248. Colisão false -> useFail. Servidor addFreshEntity @270 retorno ignorado, GameEvent.ENTITY_PLACE, shrink1 se !instabuild; awardStat ITEM_USED fora do gate de lado @308; sidedSuccess. Sem guarda de null local antes do uso da entidade. Não supor instalação bem-sucedida por evento/consumo. Parâmetros de movimento, oxigênio, energia, assentos, owner, acesso, dano, efeitos e lifecycle/persistência da entidade são downstream pendentes. Sem mana/cooldown/XP próprios. World Safety/claims/veículo e compatibilidade não testadas, NO_MUTATION.

## Recursos e evidência reproduzível
- `assets/alexscaves/models/item/submarine.json` SHA-256 `1c2bdb0b64be2d9faa2c0534a95c703ab2486f8c353383316a32ed37d84edfaf`.
Classfile SHA-256 `0bff5f070c8b4d8b9fe681577a19202fe31455ffaf6ed3be96f327c68078dfe8`.

| Método e descritor | Instruções | Code SHA-256 |
|---|---:|---|
| `<init>(Lnet/minecraft/world/item/Item$Properties;)V` | 4 | `405f81f0b51683db4ab14a729fb164a2c889439967d0bfe6248ebe8183a4873d` |
| `use(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/InteractionHand;)Lnet/minecraft/world/InteractionResultHolder;` | 138 | `c6cdaf7b64a9608806b274c9fc9b14ac0a348a053f90b9d2e58247839cc37e9b` |
| `<clinit>()V` | 5 | `50cc42da834e2a59b05bbedd9a5ff23272c3caf3e0dd28d98a8076265fc1080d` |

Limites gerais: inspeção estática do publisher, sem prova de runtime transformado, aceitação de chamadas, compatibilidade ou proteção de mundo. `NO_MUTATION / FAIL_CLOSED / PHYSICAL_QA_NOT_TESTED`.
