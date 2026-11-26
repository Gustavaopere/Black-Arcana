# Uranium

**Contrato estático:** ✅ `CERTIFIED_STATIC_7_AXES / STATIC_TECHNICAL_CATALOG_ONLY` (candidato à CI e merge), exclusivamente produtor passivo individual. `mutating_hook=NOT_VERIFIED; physical_qa=NOT_TESTED; perk_certification=NOT_CERTIFIED; NO_MUTATION`. Provider OPEN; zero novas raízes.

## Identidade e autoridade

`alexscaves:uranium`, item de suporte radioativo, classe `RadioactiveItem` (extends Item). Factory `ACItemRegistry.lambda$static$58`, Code SHA-256 `1e1c9e0dfea75205c2e2c0d0be0a2bf12982fc02d8ad825bb6b1dfd62e883a0f`. Parâmetro do construtor `0.001F`; raridade/stack defaults herdados, não definidos explicitamente pela factory. [Registry](../systems/item-registry.md). Minecraft 1.21.1 / NeoForge / Java 21; modlist sibling #19, publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, 75.279.314 bytes. [Run 45750603107/job 139677193397](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45750603107/job/139677193397), HEAD `afb4f82f63f94391648bf53803b1a297e6540dcb`, dois relatórios iguais 232.851 bytes, SHA-256 `b8fd8880d0f888ee137a436ec0aa81ea7916c6e6883acc0237d2915525499c97`. [Dossiê](../EXACT-RADIOACTIVE-ITEMS-1.0.10.md). Sem dump físico novo.

## Comportamento, ativação e parâmetros

Irradiação passiva do portador, não um cast. Construtor guarda `randomChanceOfRadiation` @7. `acInventoryTick(ItemStack,Level,Entity,boolean)V` retorna se cliente (@4), entidade não LivingEntity (@11), Player criativo (@40) ou presença de IRRADIATED (@87). O booleano de seleção não é lido. Não exige Player nos demais casos, não busca vizinhos nem consulta explicitamente tag resists_radiation. Calcula em float `q=(float)count×0.001F` @44–53; `m=1F−(float)HazmatArmorItem.getWornAmount(carrier)/4F` @55–66. Solicita aplicação se `nextFloat()<q×m` (@91–105). Sem clamp explícito; comparação com RNG limita efetivamente entrada no ramo para valores usuais. Com stack de 1 e zero peças, 0.1% nominal por chamada; exemplo stack de 64 sem proteção: 6.4% nominal. Não confundir chamada de tick com frequência efetiva do dispatcher. [Hazmat Mask](hazmat-mask.md) documenta contador por identidade e slot (0..4); quatro peças zeram o multiplicador deste produtor, não outras fontes.

Cria MobEffectInstance(IRRADIATED,1800) @129 (amp0 default da referência vanilla); pede addEffect @138 e descarta retorno. Envia UpdateEffectVisualityEntityMessage @160/163 com ambos IDs do portador, tipo 0 e duração da instância; não comprova aceitação do efeito. A presença do status impede novas tentativas deste caminho. [Irradiated](../effects/irradiated.md) documenta shouldTick amp<=0 falso e cancelamento de LivingHealEvent em não resistentes; [Radiation](../damage-types/radiation.md) pertence ao efeito, não há hurt próprio neste owner.

## Custos, estado e integração

Sem shrink, mana, cooldown fixo, custo de durabilidade, projétil, AOE, dano direto, alcance/LOS ou owner ofensivo próprio no corpo. Alvo é o portador LivingEntity; estado do efeito é da engine. Sem NBT/UUID persistente próprio demonstrado; sincronização visual não é settlement. Não repetir tick, aplicar status novamente, alterar proteção Hazmat ou conceder Mastery por tentativa. Possíveis parâmetros conceituais: exposição por stack, mitigação e duração; hook real não verificado. Limites: dispatcher de referência, aquisição e consumers declarativos aprofundados abaixo. Engine transformado, componentes/stack efetivos, aceitação e persistência de status, configuração, multiplayer e QA física NÃO VERIFICADOS. Outros produtores permanecem em seus próprios contratos.

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

## Fechamento individual de consumidores — #1238

[Run 45890629613/job 140152124649](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45890629613/job/140152124649), duas reproduções de 34.975 bytes SHA-256 `b3407f8baf4ce60a35f0ba7cc06cbf5d042e6d02f3d3781a4f48c8e45f267cf5`, 1.563 JSONs. [Dossiê e sete eixos](../EXACT-RADIOACTIVE-CONSUMER-CENSUS-1.0.10.md) · [selo](../EXACT-RADIOACTIVE-ITEM-CERTIFICATION-1.0.10.json). Registry `URANIUM` putstatic @1287 no <clinit> Code bb73db4c0f1d1c84abdf5ab1c07defd24db79e5e8c754b8c9f9ec8481a84a84a; creative tab lambda$static$10 getstatic @181, Code 4a6ee5775221aa148147d7baedc4aa322f92ac71ff99476dccb039250004171e. São os dois sites Fieldref exatos desse ID; não prova ausência de lookup dinâmico. Factory lambda$static$58, nenhuma raridade explícita, sem stack cap explicitado; construtor e tick são os dois únicos corpos próprios de RadioactiveItem. Sem novo scheduler ou raiz.

| Recurso publisher (path) | Localização / relação | SHA-256 |
|---|---|---|
| `data/alexscaves/advancement/alexscaves/uranium.json` | `["criteria","uranium","conditions","items",0,"items",0]` · DIRECT_ID | `2e6d5553588bc880b21d4cd4ad7ac9e4993b941492bde79b0eaad334641045c9` |
| `data/alexscaves/advancement/alexscaves/uranium.json` | `["display","icon","id"]` · DIRECT_ID | `2e6d5553588bc880b21d4cd4ad7ac9e4993b941492bde79b0eaad334641045c9` |
| `data/alexscaves/loot_table/blocks/radrock_uranium_ore.json` | `["pools",0,"entries",0,"children",1,"name"]` · DIRECT_ID | `becdff9650a01a57d34cebfbbbcc76f65353b5fd9815c8546d1693402319dc3d` |
| `data/alexscaves/loot_table/entities/tremorzilla.json` | `["pools",0,"entries",0,"name"]` · DIRECT_ID | `e5af3d07cb54d975d5df25db8d966e2895f695d7a7d6e9c2c3cceccea80f025c` |
| `data/alexscaves/recipe/block_of_uranium.json` | `["key","N","item"]` · DIRECT_ID | `99771f9748bf1ae78015ebb3925edfeebc2a77a3911c2ae8f9bdb1e5ae70e071` |
| `data/alexscaves/recipe/furnace/uranium_from_radrock_ore_blasting.json` | `["result","id"]` · DIRECT_ID | `de85a2c37a6c544283f5c92ca9a28bcc60d5e1001560e685d1ac46649c75be03` |
| `data/alexscaves/recipe/furnace/uranium_from_radrock_ore_smelting.json` | `["result","id"]` · DIRECT_ID | `6df9a2fbf5c309bf952c858a06a568e625ed72396340e26150e1a881917a791e` |
| `data/alexscaves/recipe/nuclear_furnace_component.json` | `["key","U","tag"]` · POTENTIAL_TAG_REFERENCE | `f084ca5773472b927d9a7887c22c3a5facdb194c23fa2a759cafea7f612c9133` |
| `data/alexscaves/recipe/nuclear_siren.json` | `["key","U","tag"]` · POTENTIAL_TAG_REFERENCE | `173f86a6edec05c6cc83faa5d06f9c73491d8aed32daaf0ae21a26fb58ae8981` |
| `data/alexscaves/recipe/uranium_from_block.json` | `["result","id"]` · DIRECT_ID | `1917b3f4af98eb1d27c449c30d13756de10288313f89adfdfa50bffc678e3249` |
| `data/alexscaves/recipe/uranium_from_shard.json` | `["result","id"]` · DIRECT_ID | `b8b3b77e00e6e6406af3e58fea493965b5dd0265da9d9cc2224767df671487b3` |
| `data/alexscaves/recipe/uranium_rod.json` | `["key","U","tag"]` · POTENTIAL_TAG_REFERENCE | `3ebac04bed9428bf988727236ef45bc407831ea2ada3efa2f2173627e854db35` |
| `data/alexscaves/recipe/uranium_shard_from_uranium.json` | `["ingredients",0,"item"]` · DIRECT_ID | `4215121770c453e01b84366646b0bef8e429185a473effe02998677a83354cc1` |
| `data/c/tags/item/raw_materials/uranium.json` | `["values",0]` · DIRECT_ID | `c071eddd2b2fd03508ac73d29772ea8c0395e27ab26f358223c62699a2b9f211` |

**Fronteira estática:** o [dispatcher ACTickingItem](../systems/ticking-item.md) encaminha stack, level, entity e selected no HEAD de ItemStack.inventoryTick; este produtor não usa selected. Hazmat é contador por identidade/slot; o coeficiente local não é redução universal de dano. Referência oficial do construtor MobEffectInstance(Holder,I) passa amplifier 0 @3 (Code SHA `24931801535be6734bb46587ae621201d1762f5143dfe56f82debdabe241bef0`, [job](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45797651887/job/139832340081)). [Irradiated](../effects/irradiated.md) não executa tick periódico para amp0; presença pode cancelar LivingHealEvent conforme resistência, sem provar bloqueio de toda cura. Efeito pode ser rejeitado; mensagem não é aceite. Campos locais não possuem configuração dinâmica per-player demonstrada; nenhum NBT próprio/owner ofensivo. Não reexecutar tick ou aplicar status, dano ou XP por conta própria. A aquisição referencial acima não fixa loot/receita selecionados nem custo em runtime. Sem hook seguro, `NO_MUTATION / fail-closed`.
