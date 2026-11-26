# Sack Of Sating

**Estado:** ⚠️ PARCIAL / STATIC_DISCOVERY_ONLY. `static_contract=NOT_CERTIFIED; mutating_hook=NOT_VERIFIED; physical_qa=NOT_TESTED; NO_MUTATION`. Sem nova raiz semântica certificada.

## Identidade e autoridade
`alexscaves:sack_of_sating`, owner `SackOfSatingItem`, factory `ACItemRegistry.lambda$static$183`, Code SHA-256 `9dcd9c444f05df03a91cce7f516726bc079f55db87d018ef5a704b5d83365d9b`. [Registro](../systems/item-registry.md). Alex's Caves Continued 1.0.10, Minecraft 1.21.1/NeoForge/Java21, modlist sibling #19; JAR publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, 75.279.314 bytes. [Dossiê](../EXACT-LATE-CONCRETE-ITEMS-1.0.10.md), [run/job](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45794089694/job/139820167569), HEAD `27c5bbc7780abbb2efe9bf2c4db615be5d0e7b3c`, dois replays byte-idênticos 425337 bytes, SHA-256 `aa6b3b052b975590f56dd2fa62773fe907346495093ef1842b0405de17b585a2`. Sem dump físico novo.

## Ativação, armazenamento e efeitos
Stack máxima 1, RARITY_SWEET. Estado em tag da stack via ACCompat.getTag/getOrCreateTag/setTag: HungerValue int (0 sem tag), ChewTimestamp long, FeedTimestamp long (-1 se ausente), Exploding boolean (false se ausente). isChewing exige tag e chave e (gameTime−ChewTimestamp)<30, sem limite inferior demonstrado. Setters gravam valores recebidos sem clamp local. Tooltip getTooltipImage cria SackOfSatingTooltip(stack), getHungerValue delega ao leitor do item; não é armazenamento independente.

overrideOtherStackedOnMe: ClickAction.SECONDARY, tag da bolsa não nula e item não RESTRICTED_FROM_SACK_OF_SATING; retorna false se não elegível, stack vazia ou !ACCompat.isEdible. Se tag EXPLODES_SACK_OF_SATING, setExploding(true) @53. calculateWholeStackHungerValue(stack,player)=nutrition(food)×count (int) se food presente e não restrito, senão 0; soma ao HungerValue @71 sem cap/overflow guard local. Solicita devolução de bowls quando returnsBowl, bottles para HoneyBottleItem/DrinkableBottledItem, quantidade igual à stack de alimento; addItem false -> drop. setCount(0) @174, ChewTimestamp=current gameTime, true. Sem guarda local de lado nesse callback. Não aplica diretamente efeitos do alimento nessa rota.

acInventoryTick inicializa tag se ausente. Alimentação: servidor, HungerValue>0, portador Player, !Abilities.invulnerable, tickCount%100==0, canEat(false), FeedTimestamp==-1 ou gameTime−FeedTimestamp>40. Solicita FoodData.eat(1,0.05F) @121, setHunger(H−1) @129, timestamp atual, GameEvent.EAT, som GENERIC_EAT. Chewing com tickCount%6==0 emite som; não confundir áudio com débito. Se Exploding e !client, cria NuclearExplosionEntity via ACCompat.createEntity, posição portador+(0,4,0), size0.5F, intentionalGameDesign true; addFreshEntity @342 retorno ignorado, setExploding(false), shrink(1) @353. Não presume dano final, raio real, claims, autoria ou aceitação. [Nuke](../damage-types/nuke.md) e [Intentional Game Design](../damage-types/intentional-game-design.md) são efeitos distintos, não nova raiz.

## Integração
Target da alimentação é portador; sem alcance, projétil, mana ou cooldown mágico próprio. Não duplicar ingestão, recipientes, timestamp, débito, explosão, XP/Mastery. Gates: ACCompat tag/food e engine FoodData, dispatch e slots, tags de restrição/explosão, runtime de nuclear explosion, proteção de mundo, sincronização/duplicação e persistência. Sem hook seguro. Tooltip class SHA 3139f8b1c6f58d61365b6e426cec091e2b2202b5543f253272709834f722b21e; dois métodos, consumidor cliente ClientSackOfSatingTooltip ainda não fechado.

## Recursos e evidência reproduzível
- `assets/alexscaves/models/item/sack_of_sating.json` SHA-256 `a390e2ac17dcca0389b27ec806e25e5755eb3dbe5001aaf7b09f548246f04e27`.
- `data/alexscaves/recipe/sack_of_sating.json` SHA-256 `0bf0ea6a21d1b2d110ee41501f6e757afe2b1acd197d5e9e5ed629230023b3ee`; resultado 1 unidade(s).
Classfile SHA-256 `e368851433cbf0746f4cdfd70605c4e49e9841beb65bd4dd17df90cbea504c7e`.

| Método e descritor | Instruções | Code SHA-256 |
|---|---:|---|
| `<init>()V` | 10 | `b684f9568e1d4cd5ea0d4342f52a5ddd6403b1a57f309ecee16e1ac4c04fdee6` |
| `getHunger(Lnet/minecraft/world/item/ItemStack;)I` | 11 | `2a8ec1ec423d0ba82e5691cca27fb60401d93b7d5869a80e02319cafbb53a426` |
| `isChewing(Lnet/minecraft/world/item/ItemStack;J)Z` | 21 | `7a01a31fb909779978708f785de22611814b35bd18bad9c42bbebeaad2643172` |
| `isExploding(Lnet/minecraft/world/item/ItemStack;)Z` | 13 | `79c12c972b0b58fb3cfef186a0f0805e0964af328497ec5e592c0df96e8a77fb` |
| `getFeedTimestamp(Lnet/minecraft/world/item/ItemStack;)J` | 15 | `4d6295b8944055d002058d49ee5d3d2fa36b61743266b1f7cd45b9b98b99adfd` |
| `setHunger(Lnet/minecraft/world/item/ItemStack;I)V` | 11 | `aabc14ffe2b635b4a32774120bc0590ec9cb78844308311bd69a58f8df6cf525` |
| `setChewTimestamp(Lnet/minecraft/world/item/ItemStack;J)V` | 11 | `17aeb96733f350d351e89e4d9a36f1ac571fc7832103bde23ad435f683ee555b` |
| `setFeedTimestamp(Lnet/minecraft/world/item/ItemStack;J)V` | 11 | `490502cf8fa2acd3b7f57e697529cec184f5a61519548473b9265f2cf540f87e` |
| `setExploding(Lnet/minecraft/world/item/ItemStack;Z)V` | 11 | `1b7df584c08d1504086d9e06c69ee610cac23c51322bf68fd7decd38c0710dc9` |
| `getTooltipImage(Lnet/minecraft/world/item/ItemStack;)Ljava/util/Optional;` | 6 | `083001a0463f491ed9e91b86f4940b09ab724f30b78f2c4547de8e6ef978bda2` |
| `overrideOtherStackedOnMe(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/inventory/Slot;Lnet/minecraft/world/inventory/ClickAction;Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/entity/SlotAccess;)Z` | 90 | `e8ddd4f888f339fac8059e185c0a3d15a8c382514cbff07969d24403650d8516` |
| `acInventoryTick(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/Entity;Z)V` | 159 | `e4cb6c367dda30c3e8048d8df53ded688912c262a019b8183a4a67913eb08a49` |
| `calculateWholeStackHungerValue(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/LivingEntity;)I` | 18 | `0b120ae846686d32b61ad201d258d136266849b036133792440426957a601b92` |

Limites gerais: inspeção estática do publisher, sem prova de runtime transformado, aceitação de chamadas, compatibilidade ou proteção de mundo. `NO_MUTATION / FAIL_CLOSED / PHYSICAL_QA_NOT_TESTED`.
