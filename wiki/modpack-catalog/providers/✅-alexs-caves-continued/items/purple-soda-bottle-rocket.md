# Purple Soda Bottle Rocket

**Estado:** ⚠️ PARCIAL / STATIC_DISCOVERY_ONLY. `static_contract=NOT_CERTIFIED; mutating_hook=NOT_VERIFIED; physical_qa=NOT_TESTED; NO_MUTATION`. Sem nova raiz semântica certificada.

## Identidade e autoridade
`alexscaves:purple_soda_bottle_rocket`, owner `SodaBottleRocketItem`, factory `ACItemRegistry.lambda$static$191`, Code SHA-256 `4dc589cd486b67dc65677e0388911cb53182ffdfb49ca2459bf226a07bb96d72`. [Registro](../systems/item-registry.md). Alex's Caves Continued 1.0.10, Minecraft 1.21.1/NeoForge/Java21, modlist sibling #19; JAR publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, 75.279.314 bytes. [Dossiê](../EXACT-LATE-CONCRETE-ITEMS-1.0.10.md), [run/job](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45794089694/job/139820167569), HEAD `27c5bbc7780abbb2efe9bf2c4db615be5d0e7b3c`, dois replays byte-idênticos 425337 bytes, SHA-256 `aa6b3b052b975590f56dd2fa62773fe907346495093ef1842b0405de17b585a2`. Sem dump físico novo.

## Ativação e custo
Construtor Item.Properties default. useOn(UseOnContext) servidor: stack, click location C e face normal d, cria SodaBottleRocketEntity(level,player,C+0.15D*d,stack) @87; addFreshEntity @95 retorno descartado; getPlayer().isCreative() @103 sem guarda explícita de null, shrink(1) se não criativo; sidedSuccess. use(Level,Player,Hand): se !isFallFlying retorna usePass; caso contrário no servidor cria SodaBottleRocketEntity(level,stack,player) @30, addFreshEntity @33 retorno ignorado, shrink1 se !instabuild; useSidedSuccess. Rotas possuem gates de lado distintos e ambas debito condicionado à criatividade, não à aceitação de spawn. Parâmetros de aceleração/voo, detonação, alcance, targeting, AOE, dano e tipo, owner, lifecycle, colisão, persistência e efeito de mundo estão na entidade downstream ainda não fechada. Sem mana/cooldown próprios. Perks de propulsão apenas conceituais; não duplicar entidade, débito ou XP; NO_MUTATION.

## Recursos e evidência reproduzível
- `assets/alexscaves/models/item/purple_soda_bottle_rocket.json` SHA-256 `5a55d5e37caa97ec7770df46f53651c7675c66f1d8367ab2ee4e6415e2df14b0`.
- `data/alexscaves/recipe/purple_soda_bottle_rocket.json` SHA-256 `7717bf0d3c751da91753396ce37b5f7cfed578b139c956c11b5e490139ad7962`; resultado 3 unidade(s).
Classfile SHA-256 `bbc633c61e6226a10cbf00bce158c2a272d3a7f1ee40dd03b3a049d8c957fb42`.

| Método e descritor | Instruções | Code SHA-256 |
|---|---:|---|
| `<init>()V` | 6 | `8be36d6241481f2aa744705cb8bf58543a3d2d603628b0a2626b73949973458c` |
| `useOn(Lnet/minecraft/world/item/context/UseOnContext;)Lnet/minecraft/world/InteractionResult;` | 62 | `c5221cffe368acde6d7703a50cdac5d9ea5b8ff4419e09330f4d42c697a1d488` |
| `use(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/InteractionHand;)Lnet/minecraft/world/InteractionResultHolder;` | 38 | `1c75677a6269c8119f804f5fac20e9acfc4cbf61f66758045b3dd49bdc3a9159` |

Limites gerais: inspeção estática do publisher, sem prova de runtime transformado, aceitação de chamadas, compatibilidade ou proteção de mundo. `NO_MUTATION / FAIL_CLOSED / PHYSICAL_QA_NOT_TESTED`.

## Downstream nativo — #1236

[Run 45797529084/job 139831910862](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45797529084/job/139831910862), HEAD `39127f8fbc3fcf51c82e00956ea785f97d75df28`: dois relatórios SHA-256 `f8d679937def972ac001dd8d9517fb46d3f7f5a4a0580db4e128e5b21cd94557`, 1.535.579 bytes. [Dossiê](../EXACT-PROJECTILE-MACHINE-DOWNSTREAM-1.0.10.md).

Owner SodaBottleRocketEntity, class SHA-256 `73a4d9bb64f255503ffeca52e8576aa4570052a75ba7c87767bb9ff8b9d53877`, FireworkRocketEntity, 8/8 métodos próprios. tick()V Code `bd67a7ad6729d27559db4d396e51b3e0ce1c4a44a4327adbf31103d5e909ec7f` chama super.tick @1, incrementa phageAge, no cliente solicita cinco partículas PURPLE_SODA_BUBBLE; não equivale a propulsão. handleEntityEvent(B)V Code `96191cb135d3dc51c8fbf3edb9a38a7bcdc1b65774daf5deff2953112796838a` trata evento 17 com apresentação FROSTMINT_EXPLOSION, SNOWFLAKE, PURPLE_SODA_BUBBLE e som de foguete dependente da câmera; não comprova dano, AOE ou congelamento real. getItem retorna stack PURPLE_SODA_BOTTLE_ROCKET. Pendem construtores e dados herdados de FireworkRocketEntity, propulsão, explosão, duração, owner/attachment, NBT e liquidação do uso. Não transformar efeitos visuais em status ou dano adicional.

Estado mantido: STATIC_DISCOVERY_ONLY / NOT_CERTIFIED / NO_MUTATION / NOT_TESTED. Sem nova raiz ou hook.

## Reconciliação de fronteiras distribuídas

Receita shapeless direta (SHA-256 `7717bf0d3c751da91753396ce37b5f7cfed578b139c956c11b5e490139ad7962`): três purple_soda_bottle mais um frostmint, saída três foguetes. Isso não prova dano, duração de propulsão nem componentes de explosão. Herança de FireworkRocketEntity deve ser auditada separadamente de apresentação de partículas e de lançamento de ThrowableProjectile. Não incrementar Mastery por efeito cosmético.

Evidência compartilhada: [matriz de reconciliação](../EXACT-CATALOG-INHERITED-BOUNDARIES-1.0.10.md). Mantidos NOT_CERTIFIED, NO_MUTATION e NOT_TESTED; nenhuma promoção por herança isolada.
