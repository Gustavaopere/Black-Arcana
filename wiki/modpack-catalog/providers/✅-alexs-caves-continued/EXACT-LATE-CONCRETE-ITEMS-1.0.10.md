# Late concrete item families — descoberta 1.0.10

**STATIC_DISCOVERY_ONLY / NO_MUTATION / NOT_CERTIFIED / NOT_TESTED.** Base main `9eeb5db432e5c9c552e8866214d34ec9fd20da73`, modlist sibling #19, publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, 75.279.314 bytes. Novo replay pendente. Não há dump da instalação nem confirmação de runtime.

## Roster de classes físicas selecionadas

- `server/item/SackOfSatingItem`
- `server/item/SeekingArrowItem`
- `server/item/SharpenedCandyCaneItem`
- `server/item/SodaBottleRocketItem`
- `server/item/SubmarineItem`
- `server/item/SweetishFishBucketItem`
- `server/item/tooltip/SackOfSatingTooltip`

## Factories diretas previamente seladas

| ID | Owner | Factory | Code SHA-256 |
|---|---|---|---|
| `alexscaves:purple_soda_bottle_rocket` | `SodaBottleRocketItem` | `ACItemRegistry.lambda$static$191` | `4dc589cd486b67dc65677e0388911cb53182ffdfb49ca2459bf226a07bb96d72` |
| `alexscaves:sack_of_sating` | `SackOfSatingItem` | `ACItemRegistry.lambda$static$183` | `9dcd9c444f05df03a91cce7f516726bc079f55db87d018ef5a704b5d83365d9b` |
| `alexscaves:seeking_arrow` | `SeekingArrowItem` | `ACItemRegistry.lambda$static$18` | `f8ce2e07f40753612f56ebe56edb49e12174a8c1042dbf16864db018597cf438` |
| `alexscaves:sharpened_candy_cane` | `SharpenedCandyCaneItem` | `ACItemRegistry.lambda$static$172` | `8566af6220458047a5bcd4b371172601c61fac9f8574338bf463d0220a9469f1` |
| `alexscaves:submarine` | `SubmarineItem` | `ACItemRegistry.lambda$static$98` | `230455d831544af1585d3aa7b09b67eae3496a0ea6e124691121a4427c13f618` |
| `alexscaves:sweetish_fish_blue_bucket` | `SweetishFishBucketItem` | `ACItemRegistry.lambda$static$151` | `2cf146833c4613f3c6038bd925527e834d419dad1399b796fa484062d7341773` |
| `alexscaves:sweetish_fish_green_bucket` | `SweetishFishBucketItem` | `ACItemRegistry.lambda$static$150` | `a90039a60a0bc10b2d11d2ccc0faa534b6c9e1bc6dc48daf9f42f409fae8a3d1` |
| `alexscaves:sweetish_fish_pink_bucket` | `SweetishFishBucketItem` | `ACItemRegistry.lambda$static$153` | `b679636ea7c47b3b75cebed47103963c4c5088e28c3e89d1d572e5bbea20c813` |
| `alexscaves:sweetish_fish_red_bucket` | `SweetishFishBucketItem` | `ACItemRegistry.lambda$static$149` | `ef1b8448d9d33e5c71ab2d445960e3321419a7113df99662978c5bb17b49dfe2` |
| `alexscaves:sweetish_fish_yellow_bucket` | `SweetishFishBucketItem` | `ACItemRegistry.lambda$static$152` | `55645415c36c0551bd0e31b7bafcc45d52cdd5d7ecd1107c5ed0e48e936b6d79` |

[Registro](systems/item-registry.md). Owners sem factory direta nessa tabela são helpers/abstrações ou consumidores que requerem reconciliação separada. Não presumir que um owner equivale a um novo objeto ou raiz semântica. Itens de arremesso existentes podem já ter fichas; nenhuma duplicação automática.

## Recorte e validação

[Probe](../../../../docs/qa/alexscaves_1010_late_concrete_items_probe.py) fixa o artefato e roster de 1555 classfiles, Code das factories, todos os corpos próprios das classes selecionadas, censo tipado e janelas de consumidores, JSONs por filename. [Workflow](../../../../.github/workflows/alexscaves-1010-late-concrete-items.yml) exige dois replays idênticos. O relatório distingue owners abstratos/interfaces e helpers; consumidores e recursos indiretos podem escapar do recorte, sem fechar universo. Não copia implementação de terceiros.

SackOfSatingItem e tooltip: custos alimentares, inventário, estado e sincronização; SeekingArrowItem: construção, targeting e entidade downstream; SharpenedCandyCaneItem: ataques, atributos e custos; SodaBottleRocketItem: ativação, projétil e movimento; SubmarineItem: posicionamento, spawn, autoria e lifecycle; SweetishFishBucketItem: cinco factories, variante, bucket data, spawn e consumidores.

Sem novas fichas ou certificados, sem alteração dos índices compartilhados e sem Stage promotion nesta proposta; integração somente após CI e consolidação com a PR #1233.

## Resultado observado

Run 45794089694/job 139820167569, HEAD `27c5bbc7780abbb2efe9bf2c4db615be5d0e7b3c`, 42 declarações (32 próprias e 10 factories), 11 owners tipados, 35 JSON, 8 checks e dois replays de 425337 bytes SHA-256 `aa6b3b052b975590f56dd2fa62773fe907346495093ef1842b0405de17b585a2`. [CI](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45794089694/job/139820167569). Dez fichas parciais, incluindo cinco variantes de Sweetish Fish; tooltip de SackOfSating reconciliado como componente, não raiz. Cada ficha fixa métodos e parâmetros; nenhuma certificação.

- [Sack Of Sating](items/sack-of-sating.md)
- [Seeking Arrow](items/seeking-arrow.md)
- [Sharpened Candy Cane](items/sharpened-candy-cane.md)
- [Purple Soda Bottle Rocket](items/purple-soda-bottle-rocket.md)
- [Submarine](items/submarine.md)
- [Sweetish Fish Red Bucket](items/sweetish-fish-red-bucket.md)
- [Sweetish Fish Green Bucket](items/sweetish-fish-green-bucket.md)
- [Sweetish Fish Blue Bucket](items/sweetish-fish-blue-bucket.md)
- [Sweetish Fish Yellow Bucket](items/sweetish-fish-yellow-bucket.md)
- [Sweetish Fish Pink Bucket](items/sweetish-fish-pink-bucket.md)
