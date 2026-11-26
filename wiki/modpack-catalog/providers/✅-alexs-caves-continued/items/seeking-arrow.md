# Seeking Arrow

**Estado:** ⚠️ PARCIAL / STATIC_DISCOVERY_ONLY. `static_contract=NOT_CERTIFIED; mutating_hook=NOT_VERIFIED; physical_qa=NOT_TESTED; NO_MUTATION`. Sem nova raiz semântica certificada.

## Identidade e autoridade
`alexscaves:seeking_arrow`, owner `SeekingArrowItem`, factory `ACItemRegistry.lambda$static$18`, Code SHA-256 `f8ce2e07f40753612f56ebe56edb49e12174a8c1042dbf16864db018597cf438`. [Registro](../systems/item-registry.md). Alex's Caves Continued 1.0.10, Minecraft 1.21.1/NeoForge/Java21, modlist sibling #19; JAR publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, 75.279.314 bytes. [Dossiê](../EXACT-LATE-CONCRETE-ITEMS-1.0.10.md), [run/job](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45794089694/job/139820167569), HEAD `27c5bbc7780abbb2efe9bf2c4db615be5d0e7b3c`, dois replays byte-idênticos 425337 bytes, SHA-256 `aa6b3b052b975590f56dd2fa62773fe907346495093ef1842b0405de17b585a2`. Sem dump físico novo.

## Ativação e efeitos
Subclasse ArrowItem, construtor Properties default. createArrow(Level,ItemStack,LivingEntity,ItemStack) cria SeekingArrowEntity(level,shooter) @6 e retorna; os dois argumentos stack não são lidos nesse corpo. Não escolhe alvo, consome munição ou chama spawn localmente. ACItemRegistry.setup registra behavior $1 (dispenser): cria entidade na posição fornecida, pickup=ALLOWED; [registro](../systems/item-registry.md) certifica este trecho e não o débito/velocidade herdados. Projétil, homing/targeting, filtros, velocidade, dano/tipo, owner, NBT, pickup e colisão dependem de SeekingArrowEntity e engine de arma/dispenser. Sem mana/cooldown próprios. Não confundir com Soak Seeking ou Targeted Ricochet; nomes de encantamentos não atribuem mecanismos ao item. Perks de munição/homing somente conceituais, sem hook; evitar duplicação de projétil, custos e Mastery.

## Recursos e evidência reproduzível
- `assets/alexscaves/models/item/seeking_arrow.json` SHA-256 `c783d57b52cb7d4aefb74f3682e97d1e3f232e60369a54b385d89e9c49e2b3d3`.
- `data/alexscaves/recipe/seeking_arrow.json` SHA-256 `e5fd8fe020f1cbab2fa360bcc644e32b4cd0be82a73018e036c38b505847ae6d`; resultado 8 unidade(s).
Classfile SHA-256 `f80ae3ca44d5cdd7dd1b359d4a44a74acbb1edc4a7d526dd6d41a0e8433b5327`.

| Método e descritor | Instruções | Code SHA-256 |
|---|---:|---|
| `<init>()V` | 6 | `8be36d6241481f2aa744705cb8bf58543a3d2d603628b0a2626b73949973458c` |
| `createArrow(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/item/ItemStack;)Lnet/minecraft/world/entity/projectile/AbstractArrow;` | 6 | `b006d85505577c41d8f4be8729e6a7ad6c8b7c06da12829286a202a314b89a07` |

Limites gerais: inspeção estática do publisher, sem prova de runtime transformado, aceitação de chamadas, compatibilidade ou proteção de mundo. `NO_MUTATION / FAIL_CLOSED / PHYSICAL_QA_NOT_TESTED`.

## Downstream nativo — #1236

[Run 45797529084/job 139831910862](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45797529084/job/139831910862), HEAD `39127f8fbc3fcf51c82e00956ea785f97d75df28`: dois relatórios SHA-256 `f8d679937def972ac001dd8d9517fb46d3f7f5a4a0580db4e128e5b21cd94557`, 1.535.579 bytes. [Dossiê](../EXACT-PROJECTILE-MACHINE-DOWNSTREAM-1.0.10.md).

Owner SeekingArrowEntity, class SHA-256 `1102754436829c3dcadb1450d6ab15efb354a3f4e58a2a262a78c5013d7f0e25`, AbstractArrow, 13/13 declarações projetadas. defineSynchedData define ARC_TOWARDS_ENTITY_ID=-1. tick()V Code `76d06bfb3e8ebaacab0bc2866c839ec1cf0b7d091a0b82c5a156aa5565c10e98` (185 instruções): super.tick, não executa homing quando inGround ou stopSeeking. Busca alvo no servidor enquanto ID=-1; consulta AABB inflada com valor min(10,3+tickCount/4) observado nos operandos (divisão inteira no recorte), predicado canHitEntity, comparação de distância, exclui ownedBy e aliado do owner quando presente. Ao selecionar toca som de lock-on e grava ID; quando há alvo resolve Level.getEntity, calcula vetor até posição+0.65F*altura em Y, exige distância > largura do alvo; solicita movimento = movimento anterior×0.30000001192092896D + vetor normalizado×0.699999988079071D. doPostHurtEffects marca stopSeeking=true; NBT desse estado não comprovado. Sem afirmar alcance esférico, velocidade final, acerto garantido, dano ou custo do arco. Perks de homing, targeting e velocidade devem manter filtros e autoridade. Pendem limites de AbstractArrow/EntityType, tags, eventos, persistência e compatibilidade.

Estado mantido: STATIC_DISCOVERY_ONLY / NOT_CERTIFIED / NO_MUTATION / NOT_TESTED. Sem nova raiz ou hook.
