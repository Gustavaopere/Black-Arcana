# Uranium

**Estado:** ⚠️ PARCIAL / STATIC_DISCOVERY_ONLY. `static_contract=NOT_CERTIFIED; mutating_hook=NOT_VERIFIED; physical_qa=NOT_TESTED; NO_MUTATION`. Sem nova raiz semântica certificada.

## Identidade e autoridade

`alexscaves:uranium`, item de suporte radioativo, classe `RadioactiveItem` (extends Item). Factory `ACItemRegistry.lambda$static$58`, Code SHA-256 `1e1c9e0dfea75205c2e2c0d0be0a2bf12982fc02d8ad825bb6b1dfd62e883a0f`. Parâmetro do construtor `0.001F`; raridade/stack defaults herdados, não definidos explicitamente pela factory. [Registry](../systems/item-registry.md). Minecraft 1.21.1 / NeoForge / Java 21; modlist sibling #19, publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, 75.279.314 bytes. [Run 45750603107/job 139677193397](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45750603107/job/139677193397), HEAD `afb4f82f63f94391648bf53803b1a297e6540dcb`, dois relatórios iguais 232.851 bytes, SHA-256 `b8fd8880d0f888ee137a436ec0aa81ea7916c6e6883acc0237d2915525499c97`. [Dossiê](../EXACT-RADIOACTIVE-ITEMS-1.0.10.md). Sem dump físico novo.

## Comportamento, ativação e parâmetros

Irradiação passiva do portador, não um cast. Construtor guarda `randomChanceOfRadiation` @7. `acInventoryTick(ItemStack,Level,Entity,boolean)V` retorna se cliente (@4), entidade não LivingEntity (@11), Player criativo (@40) ou presença de IRRADIATED (@87). O booleano de seleção não é lido. Não exige Player nos demais casos, não busca vizinhos nem consulta explicitamente tag resists_radiation. Calcula em float `q=(float)count×0.001F` @44–53; `m=1F−(float)HazmatArmorItem.getWornAmount(carrier)/4F` @55–66. Solicita aplicação se `nextFloat()<q×m` (@91–105). Sem clamp explícito; comparação com RNG limita efetivamente entrada no ramo para valores usuais. Com stack de 1 e zero peças, 0.1% nominal por chamada; exemplo stack de 64 sem proteção: 6.4% nominal. Não confundir chamada de tick com frequência efetiva do dispatcher. [Hazmat Mask](hazmat-mask.md) documenta contador por identidade e slot (0..4); quatro peças zeram o multiplicador deste produtor, não outras fontes.

Cria MobEffectInstance(IRRADIATED,1800) @129 (amp0 default da referência vanilla); pede addEffect @138 e descarta retorno. Envia UpdateEffectVisualityEntityMessage @160/163 com ambos IDs do portador, tipo 0 e duração da instância; não comprova aceitação do efeito. A presença do status impede novas tentativas deste caminho. [Irradiated](../effects/irradiated.md) documenta shouldTick amp<=0 falso e cancelamento de LivingHealEvent em não resistentes; [Radiation](../damage-types/radiation.md) pertence ao efeito, não há hurt próprio neste owner.

## Custos, estado e integração

Sem shrink, mana, cooldown fixo, custo de durabilidade, projétil, AOE, dano direto, alcance/LOS ou owner ofensivo próprio no corpo. Alvo é o portador LivingEntity; estado do efeito é da engine. Sem NBT/UUID persistente próprio demonstrado; sincronização visual não é settlement. Não repetir tick, aplicar status novamente, alterar proteção Hazmat ou conceder Mastery por tentativa. Possíveis parâmetros conceituais: exposição por stack, mitigação e duração; hook real não verificado. Pendentes: dispatcher/engine efetivos, contexto de inventário, componentes/stack defaults, efeitos de outros produtores, aquisição e consumers indiretos (inclusive usos de crafting e loot), proteção, persistência de status, multiplayer, QA física.

## Recursos observados

Modelo `assets/alexscaves/models/item/uranium.json`, SHA-256 `3bf06c51a263c24b25e727d84b932d6912122d11f72d9a622856431588c86cb1`.
- `data/alexscaves/recipe/furnace/uranium_from_radrock_ore_blasting.json` SHA-256 `de85a2c37a6c544283f5c92ca9a28bcc60d5e1001560e685d1ac46649c75be03`; resultado 1 unidade(s), tipo minecraft:blasting.
- `data/alexscaves/recipe/furnace/uranium_from_radrock_ore_smelting.json` SHA-256 `6df9a2fbf5c309bf952c858a06a568e625ed72396340e26150e1a881917a791e`; resultado 1 unidade(s), tipo minecraft:smelting.
- `data/alexscaves/recipe/uranium_from_block.json` SHA-256 `1917b3f4af98eb1d27c449c30d13756de10288313f89adfdfa50bffc678e3249`; resultado 9 unidade(s), tipo minecraft:crafting_shapeless.
- `data/alexscaves/recipe/uranium_from_shard.json` SHA-256 `b8b3b77e00e6e6406af3e58fea493965b5dd0265da9d9cc2224767df671487b3`; resultado 1 unidade(s), tipo minecraft:crafting_shaped. Não atribuir XP/Mastery a receita declarativa.

## Localizadores

Classfile SHA-256 `6a46aa885ce5e5728c22691033b0a0f892d69f6c6fa7dd86a96c8f33c81d9436`.

| Método e descritor | Instruções | Code SHA-256 |
|---|---:|---|
| `<init>(Lnet/minecraft/world/item/Item$Properties;F)V` | 7 | `93f4d18041315ae466b5ad1ce20b90499a83ae756a7ad294dca4c80b70aa0ba3` |
| `acInventoryTick(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/Entity;Z)V` | 73 | `a98c07b15db89b72116500877e23e3f95db45ec8223dfeaa00fb76980bacc47d` |
