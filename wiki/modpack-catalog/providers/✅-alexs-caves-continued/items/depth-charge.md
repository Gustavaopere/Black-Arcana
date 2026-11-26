# Depth Charge

**Estado:** ⚠️ PARCIAL / STATIC_DISCOVERY_ONLY. `static_contract=NOT_CERTIFIED; mutating_hook=NOT_VERIFIED; physical_qa=NOT_TESTED; NO_MUTATION`. Sem nova raiz semântica certificada.

## Identidade e autoridade
`alexscaves:depth_charge`, owner `ThrownProjectileItem`, factory `ACItemRegistry.lambda$static$113`, Code SHA-256 `5b5396ac73dc271445003cefeda4e6066978b2df1997228de0b035949d3a39f8`. [Registro](../systems/item-registry.md). Alex's Caves Continued 1.0.10, Minecraft 1.21.1/NeoForge/Java21, modlist sibling #19; JAR publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, 75.279.314 bytes. [Dossiê](../EXACT-TERMINAL-ITEM-HELPERS-1.0.10.md), [run/job](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45794089646/job/139820166475), HEAD `27c5bbc7780abbb2efe9bf2c4db615be5d0e7b3c`, dois replays byte-idênticos 439138 bytes, SHA-256 `7d70e29eb4bd2df5df5fe73720d1bd6213b61e7a950b43494f3efd416830e66f`. Sem dump físico novo.

## Lançamento e parâmetros
Factory define throwAngle=-10F, throwSpeed=0.65F, throwRandomness=1.5F (ordem do construtor Properties,Function,FFF; campos em @7/13/19). Bootstrap liga ACItemRegistry.lambda$static$112(Player)ThrowableItemProjectile, Code SHA `620d93b80cee080c5a16582cdc36b279266c396c9c32312ab22b450cb5394f5c`, que chama new DepthChargeEntity(player.level(),player), conforme [contrato certificado de registro](../systems/item-registry.md). Identidade do shooter passado não prova owner persistido.

use(Level,Player,Hand): stack da mão; som SNOWBALL_THROW/PLAYERS, volume 0.5F, pitch (0.7F×nextFloat()+0.25F)×0.5F, antes da guarda de lado. Servidor: projectileSupplier.apply(player), cast ThrowableItemProjectile, setItem(stack) @79, shootFromRotation(player,XRot,YRot,throwAngle,throwSpeed,throwRandomness) @105, addFreshEntity @111 (retorno ignorado). Depois awardStat ITEM_USED @123, shrink(1) @139 se !instabuild; sidedSuccess. Débito/estatística fora da guarda servidor; não inferir dupla cobrança efetiva sem engine. Sem guard de null local para supplier. Valores de speed/randomness são argumentos de lançamento, não distância/velocidade final comprovada.
## Targeting, efeitos e integração
Nenhum dano, filtro, impacto, alcance, AOE, status, velocidade residual, persistência, owner, dano/tipo ou cooldown próprios demonstrados por este corpo; estão na entidade DepthChargeEntity e engine. Para scoops, setItem permite identidade de sabor distinta, mas downstream do sabor não certificado. Sem mana/XP próprios. Não duplicar spawn, débito, dano ou Mastery; sem hook mutador. Validar entity, collision, dispatch, tags/receitas, proteção, multiplayer e QA física.

## Recursos e evidência reproduzível
- `assets/alexscaves/models/item/depth_charge.json` SHA-256 `f8ae5ab1ee385e03594e596f8664f500223ebf9b0edeccd3e4ca8ce5d9aece48`.
Classfile SHA-256 `925fb7047dddc8044929b0a581af2a4dcf5c6688dd277f445c9bc0dbd1f9d57d`.

| Método e descritor | Instruções | Code SHA-256 |
|---|---:|---|
| `<init>(Lnet/minecraft/world/item/Item$Properties;Ljava/util/function/Function;FFF)V` | 16 | `345b98693241a891e89a97e3cae2a358d6b5a6fc0d7c9db9aadeb83dda5a3d0f` |
| `use(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/InteractionHand;)Lnet/minecraft/world/InteractionResultHolder;` | 72 | `701c3024e6172ec05c20f680119cbced8923fba307c9a639f493ad273394038a` |

Limites gerais: inspeção estática do publisher, sem prova de runtime transformado, aceitação de chamadas, compatibilidade ou proteção de mundo. `NO_MUTATION / FAIL_CLOSED / PHYSICAL_QA_NOT_TESTED`.

## Downstream nativo — #1236

[Run 45797529084/job 139831910862](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45797529084/job/139831910862), HEAD `39127f8fbc3fcf51c82e00956ea785f97d75df28`: dois relatórios SHA-256 `f8d679937def972ac001dd8d9517fb46d3f7f5a4a0580db4e128e5b21cd94557`, 1.535.579 bytes. [Dossiê](../EXACT-PROJECTILE-MACHINE-DOWNSTREAM-1.0.10.md).

Owner DepthChargeEntity, class SHA-256 `d9ecff8deceecb68e066b3675a8835206698180d77a846150dba94eea96094ca`, 10/10 métodos próprios; ThrowableItemProjectile. onHitEntity solicita 2F+nextInt(2) via thrown(projétil,getOwner()) @34 (Code `1e7d5a900fd8da9e27d893763a32fcadd7b9bd426854838017d674a04887dc8c`); onHit chama super e marca hitGround=true. tick()V (93 instruções, Code `f3a759eb6e57e9860d47b3e0645e537dadead702da4c82e845f688743de17f76`): baseTick/checkInsideBlocks, gravidade −0.05000000074505806D no Y se habilitada, move SELF, updateRotation, escala de movimento 0.9900000095367432D. Contato com chão/colisão marca hitGround; em água solicita quatro partículas de bolha; quando hitGround zera movimento, incrementa groundTime e solicita explode se >30 ticks no servidor. explode()V Code `c70fccde78085e05a063ce7d8e63fdd1b217f6ada0aa2861cea26b02eab48d23`: remove KILLED @4, canEntityGrief @12, seleção DESTROY_WITH_DECAY/DESTROY/KEEP pelo gate e gamerule, consulta fluido WATER, instancia MineExplosion @104 (posição Y+0.5D, argumento 2F), explode @109 e finalizeExplosion(true) @114. Dano/área de MineExplosion, owner atribuído e aceite de efeitos não inferidos desse argumento. Não ampliar raio, detonação ou duplicar callbacks; world safety pendente.

Estado mantido: STATIC_DISCOVERY_ONLY / NOT_CERTIFIED / NO_MUTATION / NOT_TESTED. Sem nova raiz ou hook.
