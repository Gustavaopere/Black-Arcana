# Cinder Brick

**Estado:** ⚠️ PARCIAL / STATIC_DISCOVERY_ONLY. `static_contract=NOT_CERTIFIED; mutating_hook=NOT_VERIFIED; physical_qa=NOT_TESTED; NO_MUTATION`. Sem nova raiz semântica certificada.

## Identidade e autoridade
`alexscaves:cinder_brick`, owner `ThrownProjectileItem`, factory `ACItemRegistry.lambda$static$63`, Code SHA-256 `6170bbfd08b2836ed9e776a6faf4682e4f9708646716c0160e13bcc32986c125`. [Registro](../systems/item-registry.md). Alex's Caves Continued 1.0.10, Minecraft 1.21.1/NeoForge/Java21, modlist sibling #19; JAR publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, 75.279.314 bytes. [Dossiê](../EXACT-TERMINAL-ITEM-HELPERS-1.0.10.md), [run/job](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45794089646/job/139820166475), HEAD `27c5bbc7780abbb2efe9bf2c4db615be5d0e7b3c`, dois replays byte-idênticos 439138 bytes, SHA-256 `7d70e29eb4bd2df5df5fe73720d1bd6213b61e7a950b43494f3efd416830e66f`. Sem dump físico novo.

## Lançamento e parâmetros
Factory define throwAngle=-20F, throwSpeed=0.65F, throwRandomness=0.9F (ordem do construtor Properties,Function,FFF; campos em @7/13/19). Bootstrap liga ACItemRegistry.lambda$static$62(Player)ThrowableItemProjectile, Code SHA `bac38bfbe1e84aa5e44899e89c1c1f99fb192995ee71d1ea50d65e1c155b1c6b`, que chama new CinderBrickEntity(player.level(),player), conforme [contrato certificado de registro](../systems/item-registry.md). Identidade do shooter passado não prova owner persistido.

use(Level,Player,Hand): stack da mão; som SNOWBALL_THROW/PLAYERS, volume 0.5F, pitch (0.7F×nextFloat()+0.25F)×0.5F, antes da guarda de lado. Servidor: projectileSupplier.apply(player), cast ThrowableItemProjectile, setItem(stack) @79, shootFromRotation(player,XRot,YRot,throwAngle,throwSpeed,throwRandomness) @105, addFreshEntity @111 (retorno ignorado). Depois awardStat ITEM_USED @123, shrink(1) @139 se !instabuild; sidedSuccess. Débito/estatística fora da guarda servidor; não inferir dupla cobrança efetiva sem engine. Sem guard de null local para supplier. Valores de speed/randomness são argumentos de lançamento, não distância/velocidade final comprovada. ACItemRegistry.setup tem dispenser callback próprio que cria entidade na posição de saída; não usa esses parâmetros por si, custo e velocidade do dispenser são herdados.
## Targeting, efeitos e integração
Nenhum dano, filtro, impacto, alcance, AOE, status, velocidade residual, persistência, owner, dano/tipo ou cooldown próprios demonstrados por este corpo; estão na entidade CinderBrickEntity e engine. Para scoops, setItem permite identidade de sabor distinta, mas downstream do sabor não certificado. Sem mana/XP próprios. Não duplicar spawn, débito, dano ou Mastery; sem hook mutador. Validar entity, collision, dispatch, tags/receitas, proteção, multiplayer e QA física.

## Recursos e evidência reproduzível
- `assets/alexscaves/models/item/cinder_brick.json` SHA-256 `7d738ea07d4d3f596242aa02220dabce47a6d420d98b6510e1793bf20e319769`.
- `data/alexscaves/recipe/cinder_brick.json` SHA-256 `6f9e801364c5eb742faa4586ef6af12bd1ec911772921f059f105657de705738`; resultado 16 unidade(s).
Classfile SHA-256 `925fb7047dddc8044929b0a581af2a4dcf5c6688dd277f445c9bc0dbd1f9d57d`.

| Método e descritor | Instruções | Code SHA-256 |
|---|---:|---|
| `<init>(Lnet/minecraft/world/item/Item$Properties;Ljava/util/function/Function;FFF)V` | 16 | `345b98693241a891e89a97e3cae2a358d6b5a6fc0d7c9db9aadeb83dda5a3d0f` |
| `use(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/InteractionHand;)Lnet/minecraft/world/InteractionResultHolder;` | 72 | `701c3024e6172ec05c20f680119cbced8923fba307c9a639f493ad273394038a` |

Limites gerais: inspeção estática do publisher, sem prova de runtime transformado, aceitação de chamadas, compatibilidade ou proteção de mundo. `NO_MUTATION / FAIL_CLOSED / PHYSICAL_QA_NOT_TESTED`.

## Downstream nativo — #1236

[Run 45797529084/job 139831910862](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45797529084/job/139831910862), HEAD `39127f8fbc3fcf51c82e00956ea785f97d75df28`: dois relatórios SHA-256 `f8d679937def972ac001dd8d9517fb46d3f7f5a4a0580db4e128e5b21cd94557`, 1.535.579 bytes. [Dossiê](../EXACT-PROJECTILE-MACHINE-DOWNSTREAM-1.0.10.md).

Owner CinderBrickEntity, class SHA-256 `d09510632ca5e4dbb367227830291074fb6f94c1d39bc8fce368db0bf3a76a53`, 8/8 métodos próprios, ThrowableItemProjectile. ACEntityRegistry literal cinder_brick @605, bootstrap $34 @608, register @613 e CINDER_BRICK @616. onHitEntity(EntityHitResult)V, 21 instruções, Code SHA `205c098af1b8b6052cbd3a3861a3061e593a232ada8df6054085cb3d0e306305`: super @2, DamageSources.thrown(projétil,getOwner()) @18, dano solicitado 2F+nextInt(2), isto é 2 ou 3 pontos @34 (retorno não condiciona outro efeito local). onHit(HitResult)V, 47 instruções, Code `9ac286cd7ceb83cf24d022c40cd52ee3fa784e1f9f798c1d05df25591e14e1d1`: super @2; servidor envia evento 3 @21 e discard @25; hit de bloco consulta estado, resistência à explosão <5F, exclui tag UNMOVEABLE e ar, solicita destroyBlock(pos,true) @91. Sem gate próprio de claims ou aceite, não inferir destruição bem-sucedida. Evento 3 solicita oito partículas ITEM. Perks de dano e destruição são caminhos separados; world safety exige boundary real. Restam parâmetros de EntityType, tags efetivas, física, autorização e engine de colisão/owner.

Estado mantido: STATIC_DISCOVERY_ONLY / NOT_CERTIFIED / NO_MUTATION / NOT_TESTED. Sem nova raiz ou hook.

## Reconciliação de fronteiras distribuídas

Referência de engine NeoForge 21.1.250: [downstream](../EXACT-FOUR-ITEMS-DOWNSTREAM-21.1.250.md) e [impacto](../EXACT-INK-BOMB-IMPACT-21.1.250.md). O construtor ThrowableProjectile(LivingEntity) posiciona em x, eyeY−0.10000000149, z e chama setOwner; Projectile.setOwner conserva UUID/cache para owner não nulo e getOwner pode resolver o UUID no servidor. shootFromRotation deriva a direção trigonométrica, normaliza, adiciona dispersão triangular por eixo com desvio 0.0172275×inaccuracy, escala por speed e soma movimento conhecido do lançador (com componente Y condicionado a não estar no chão). Assim speed não é alcance. ThrowableItemProjectile.setItem (Code `342ca58804f1d89ec96ff7c5359e827563c025ca2af343d8ae8c8d6c252aa621`) copia stack com count 1 para dados sincronizados. As factories de ThrownProjectileItem usam Item.Properties sem override; componentes comuns distribuídos (ver [defaults](../EXACT-ITEM-ENTITY-DEFAULTS-21.1.250.md)) declaram stack nominal 64 e nenhuma durabilidade explícita. Isso não prova componentes após patches externos.

No caminho herdado ThrowableProjectile.tick (Code `1a43e9d55ff6e07f0c7a778cfeb9e2734274a899ed0861189658714b7cd2d51c`), colisão por vetor de movimento precede o dispatch: MISS ou EventHooks.onProjectileImpact cancelado não chama hitTargetOrDeflectSelf. ProjectileUtil.getHitResultOnMoveVector (Code `05bfaca7efca85062520a23cf5b4b8f536ba7993e66bfbb84591fdd707758630`) faz clip COLLIDER, limita segmento pelo bloco, margem 0.3F e busca AABB expandida por delta e inflada 1D; não equivale a raio de área. canHitEntity exige canBeHitByProjectile e exclui veículo compartilhado antes de leftOwner. Deflect pode alterar owner no servidor. Drag de referência .8 em água/.99 fora, gravidade .03; trajetória depende de colisão e ambiente. DamageSources.thrown (Code `6b46209a49fb0bb1ec39473978a8f425b03edc561f4fa5f6413a42f07093170b`) resolve minecraft:thrown, projétil direto e owner atual. Não garantir dano ou aceite de hit pela existência da chamada.

Dispenser: AbstractProjectileDispenseBehavior de referência usa power 1.1, uncertainty 6, ajuste +0.1Y, dispara, solicita spawn e reduz uma unidade sem verificar aceite de spawn. O callback próprio do registry tem de ser distinguido de uso manual; não importar a velocidade manual ao dispenser. ACItemRegistry$2 é callback de CINDER_BRICK: criação posicional, sem setItem local identificado. Receita auditada (SHA-256 `6f9e801364c5eb742faa4586ef6af12bd1ec911772921f059f105657de705738`): CCC/C C/CCC com oito entradas #alexscaves:concrete, saída 16. Tag efetiva e autorização de destroyBlock não estabelecidas. Custo de crafting e custo por lançamento são fronteiras separadas.

Evidência compartilhada: [matriz de reconciliação](../EXACT-CATALOG-INHERITED-BOUNDARIES-1.0.10.md). Mantidos NOT_CERTIFIED, NO_MUTATION e NOT_TESTED; nenhuma promoção por herança isolada.
