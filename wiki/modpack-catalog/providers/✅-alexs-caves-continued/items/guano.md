# Guano

**Estado:** ⚠️ PARCIAL / STATIC_DISCOVERY_ONLY. `static_contract=NOT_CERTIFIED; mutating_hook=NOT_VERIFIED; physical_qa=NOT_TESTED; NO_MUTATION`. Sem nova raiz semântica certificada.

## Identidade e autoridade
`alexscaves:guano`, owner `ThrownProjectileItem`, factory `ACItemRegistry.lambda$static$121`, Code SHA-256 `279cb235c5eba0d207bae281636c396354915b06416eb9bec09335bdb108cd6d`. [Registro](../systems/item-registry.md). Alex's Caves Continued 1.0.10, Minecraft 1.21.1/NeoForge/Java21, modlist sibling #19; JAR publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, 75.279.314 bytes. [Dossiê](../EXACT-TERMINAL-ITEM-HELPERS-1.0.10.md), [run/job](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45794089646/job/139820166475), HEAD `27c5bbc7780abbb2efe9bf2c4db615be5d0e7b3c`, dois replays byte-idênticos 439138 bytes, SHA-256 `7d70e29eb4bd2df5df5fe73720d1bd6213b61e7a950b43494f3efd416830e66f`. Sem dump físico novo.

## Lançamento e parâmetros
Factory define throwAngle=0F, throwSpeed=1F, throwRandomness=1F (ordem do construtor Properties,Function,FFF; campos em @7/13/19). Bootstrap liga ACItemRegistry.lambda$static$120(Player)ThrowableItemProjectile, Code SHA `34ecf715b0867f36fc58398b0de7571f4d01dbf5d44995fd6b7e3396729576d1`, que chama new GuanoEntity(player.level(),player), conforme [contrato certificado de registro](../systems/item-registry.md). Identidade do shooter passado não prova owner persistido.

use(Level,Player,Hand): stack da mão; som SNOWBALL_THROW/PLAYERS, volume 0.5F, pitch (0.7F×nextFloat()+0.25F)×0.5F, antes da guarda de lado. Servidor: projectileSupplier.apply(player), cast ThrowableItemProjectile, setItem(stack) @79, shootFromRotation(player,XRot,YRot,throwAngle,throwSpeed,throwRandomness) @105, addFreshEntity @111 (retorno ignorado). Depois awardStat ITEM_USED @123, shrink(1) @139 se !instabuild; sidedSuccess. Débito/estatística fora da guarda servidor; não inferir dupla cobrança efetiva sem engine. Sem guard de null local para supplier. Valores de speed/randomness são argumentos de lançamento, não distância/velocidade final comprovada. ACItemRegistry.setup tem dispenser callback próprio que cria entidade na posição de saída; não usa esses parâmetros por si, custo e velocidade do dispenser são herdados.
## Targeting, efeitos e integração
Nenhum dano, filtro, impacto, alcance, AOE, status, velocidade residual, persistência, owner, dano/tipo ou cooldown próprios demonstrados por este corpo; estão na entidade GuanoEntity e engine. Para scoops, setItem permite identidade de sabor distinta, mas downstream do sabor não certificado. Sem mana/XP próprios. Não duplicar spawn, débito, dano ou Mastery; sem hook mutador. Validar entity, collision, dispatch, tags/receitas, proteção, multiplayer e QA física.

## Recursos e evidência reproduzível
- `assets/alexscaves/models/item/guano.json` SHA-256 `44b059c49c984d04155d9c70d2445daed232eca41a9bcd9d2f93ea115cfaa0c2`.
Classfile SHA-256 `925fb7047dddc8044929b0a581af2a4dcf5c6688dd277f445c9bc0dbd1f9d57d`.

| Método e descritor | Instruções | Code SHA-256 |
|---|---:|---|
| `<init>(Lnet/minecraft/world/item/Item$Properties;Ljava/util/function/Function;FFF)V` | 16 | `345b98693241a891e89a97e3cae2a358d6b5a6fc0d7c9db9aadeb83dda5a3d0f` |
| `use(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/InteractionHand;)Lnet/minecraft/world/InteractionResultHolder;` | 72 | `701c3024e6172ec05c20f680119cbced8923fba307c9a639f493ad273394038a` |

Limites gerais: inspeção estática do publisher, sem prova de runtime transformado, aceitação de chamadas, compatibilidade ou proteção de mundo. `NO_MUTATION / FAIL_CLOSED / PHYSICAL_QA_NOT_TESTED`.

## Downstream nativo — #1236

[Run 45797529084/job 139831910862](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45797529084/job/139831910862), HEAD `39127f8fbc3fcf51c82e00956ea785f97d75df28`: dois relatórios SHA-256 `f8d679937def972ac001dd8d9517fb46d3f7f5a4a0580db4e128e5b21cd94557`, 1.535.579 bytes. [Dossiê](../EXACT-PROJECTILE-MACHINE-DOWNSTREAM-1.0.10.md).

Owner GuanoEntity, class SHA-256 `beb2cbe91f41a812179257a3b1b02d65fb0d619194be7b1accc1aa5c96f72d02`, ThrowableItemProjectile, 8/8 métodos próprios. ACEntityRegistry literal guano @911, bootstrap $52 @914, register @919 e GUANO @922. onHitEntity(EntityHitResult)V, 15 instruções, Code SHA `0358e2974d98fcf4e99e70a3e7b6138beacdf63c0ca739a4ba3dd94ffe9a7cf9`: super @2, alvo do hit, DamageSources.thrown(projétil,getOwner()) @18, hurt com 0F @22; nenhum status/dano positivo próprio demonstrado nesse corpo. Não equiparar a FallingGuanoEntity. onHit(HitResult)V Code `1c1de233c682ab30af82e751550f802c6ce536942db64e5076f4e3e383f4512d`: super, servidor broadcast 3 e discard. Evento 3: oito partículas ITEM, velocidade de apresentação (nextFloat−0.5)×0.08 por eixo; não física do projétil. Pendentes: EntityType, owner, hitbox, física, registry ativo, event/dano zero aceito, dispenser, custo efetivo e recursos transitivos. Não conceder Mastery por mero hit visual.

Estado mantido: STATIC_DISCOVERY_ONLY / NOT_CERTIFIED / NO_MUTATION / NOT_TESTED. Sem nova raiz ou hook.
