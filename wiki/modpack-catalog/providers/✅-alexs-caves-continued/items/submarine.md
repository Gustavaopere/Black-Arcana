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

## Downstream nativo — #1236

[Run 45797529084/job 139831911308](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45797529084/job/139831911308), HEAD `39127f8fbc3fcf51c82e00956ea785f97d75df28`: dois relatórios SHA-256 `137a0235d3e00a4fbbe947d6da01ffb50572f57a8a43f62da63847aa81034ff9`, 3.762.090 bytes. [Dossiê](../EXACT-PROJECTILE-MACHINE-DOWNSTREAM-1.0.10.md).

Owner SubmarineEntity, class SHA-256 `fad2e7edf6fba8dffeb8bf3edfc23004f8fb7d4342c3a3d865bd10a4e4b93775`, Entity, 55/56 declarações projetadas, uma deferred. defineSynchedData (Code `c19cd0365f7906bf66791ed89b72c6ae9b74ccfcd6647b0c0cda66bc21406b60`): rotação de 3 hélices/ACCELERATION 0F, LIGHTS/WAXED false, OXIDIZATION_LEVEL/DAMAGE_LEVEL/DANGER_ALERT_TICKS 0. interact(Player,InteractionHand) (Code `edfe10d8a0a31f61d8360096ef162eade34cc511a13784f0468e96c38adec743`, 147 instruções): secondary use PASS; AXE_SCRAPE e oxidização positiva ou waxed solicita swing, desgaste 1 fora de creative e remove cera ou reduz oxidização, resetOxidizeTime; HONEYCOMB quando não encerado pede shrink1 fora de creative e setWaxed(true); COPPER_INGOT se damageLevel>0 pede shrink1 fora de creative, damageLevel=max(0,L−1) e damageSustained=0; caso restante no servidor damageLevel<4 tenta startRiding e retorna conforme aceite. hurt(DamageSource,F)Z Code `e383fe68d16365a3724a1d663398287980119f7716847d092beab7d0e2bd9b85`: acumula dano, limiar 10D, zera acumulador, incrementa nível ou destrói quando já >=4, solicita drops de cobre; não é HP de LivingEntity. save Code `dfbaf630b8b7cd207677b26996db93d898473d3d813ff056931f5fcdaf1787af` grava níveis, waxed, lights, oxidizeTime e damageSustained via putDouble; load Code `69cc3f7e54589d5a134b67c4f64deafd208210ae86daaab3df8eee2a0dc45768` lê damageSustained via ACCompat.getInt (assimetria a investigar), não presumir conservação fracionária. Movimento/assentos/oxigênio e acesso efetivo pendem; não reexecutar interações nem creditar Mastery por pedido de reparo.

Estado mantido: STATIC_DISCOVERY_ONLY / NOT_CERTIFIED / NO_MUTATION / NOT_TESTED. Sem nova raiz ou hook.

## Reconciliação de fronteiras distribuídas

onKeyPacket(Entity,int) Code `16db52cf2b418f783f6af7b24311599cb1ac052d7b45507c6a51e64cf3fa68c1`: gate isPassengerOfSameVehicle, não prova autenticação do remetente. Tipo 0 ajusta upTicks=10 e downTicks=0; tipo 1 downTicks=10; tipo 2 alterna luzes e cooldown=5, sem gate local desse cooldown. positionRider Code `29e1455eb5d10ae5f96af00c2c761d01addecdbe4ab39ee437d2114540c7bb7a`: condição de relação de montaria, LivingEntity e !touchingUnloadedChunk, Player recebe tickController, clampRotation, setAirSupply(min(current+2,max)) @174; damageLevel>=4 solicita stopRiding. clampRotation Code `a28b1ec36fb418f9edc5359f546af9ff5f7e5e7c4d435749adfc8d0ecc194338`: yaw relativo wrapped, clamp −105 a 105. tickController Code `32570c5ac82a3fda0091ee07976d4e6a57882abdcc7ae56a3e7c5c0a99c66738`: input lateral não zero, rotação 2.5F por sinal e timers 5; longitudinal aborda alvos de aceleração 1 ou −0.5 por .02. Não são velocidade final. isInvulnerableTo Code `e96935e5678140a841f44221c3b0224d0b9498188ba5f11d743e98ce6797d3f2` considera super e DROWN, DRY_OUT, CACTUS, HOT_FLOOR, IN_FIRE, ON_FIRE, FALL. canBeRiddenUnderFluidType delega supportsBoating; alerta para LivingEntity viva montada em Submarine com damageLevel<=3 ajusta danger ticks=100. tick principal (733 instruções, Code `df64cec69866944754a7d1c1a2c2e5eb4ebb22b7956427a35eadba47388372e6`) ainda não projetado integralmente. Perks de navegação, oxigênio, dano e acesso precisam de fronteiras separadas; não duplicar setAirSupply ou criar pacote sintético.

Evidência compartilhada: [matriz de reconciliação](../EXACT-CATALOG-INHERITED-BOUNDARIES-1.0.10.md). Mantidos NOT_CERTIFIED, NO_MUTATION e NOT_TESTED; nenhuma promoção por herança isolada.
