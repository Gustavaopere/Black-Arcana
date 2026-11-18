# ACFoods — inventário de construção e consumidores (1.0.10)

**Estado:** descoberta SHA-exata executada, disposição individual ainda candidata; não certifica os alimentos, blocos, registries, efeitos downstream ou hooks. NO_MUTATION / provider OPEN.

## Identidade e escopo
- Artefato publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, 75.279.314 bytes.
- Classe `com.github.alexmodguy.alexscaves.server.item.ACFoods`, SHA-256 `a52ec981fe51c97003383a46f7c0b2de06baa5e3ca3f73db988655abce51e12e`. 63 campos public static final FoodProperties, 48 métodos (construtor, <clinit> com 606 instruções, 46 suppliers), vinculados sem executar/disparar as classes.
- Censo tipado de 1.555 classfiles: 8 classes consumidoras da referência a campos, 121 sites, 63/63 campos com site observado. 45 campos declaram efeito, 46 chamadas e 46 suppliers; 18 campos sem efeito declarado pelo builder, não prova ausência de comportamento adicional.
- A tabela registra literais de nutrição, modificador de saturação e chance, não valores de runtime alterados. Duração de efeito em ticks. Chamada `MobEffectInstance(Holder,int)` não fornece amplifier explícito. Referência oficial de consumo/limites no [ACFoodBuilder](systems/food-builder.md).

## Propriedades e efeitos — ordem alfabética

| Campo | N | m | Flags declaradas | Efeito(s) solicitado(s), chance, duração | Sites diretos |
|---|---:|---:|---|---|---:|
| `ALEX_MEAL` | 40 | 5 | bowl | CONFUSION · 100% · 200 t (lambda$static$44); BAD_OMEN · 100% · 48000 t (lambda$static$45) | 1 |
| `BIOME_TREAT` | 20 | 0.1 | — | — | 1 |
| `BIOME_TREAT_DONE` | 1 | 0.1 | — | — | 1 |
| `BLOCK_OF_CHOCOLATE` | 2 | 0.1 | — | SUGAR_RUSH · 1% · 200 t (lambda$static$9) | 4 |
| `BLOCK_OF_FROSTING` | 1 | 0.1 | — | SUGAR_RUSH · 2% · 200 t (lambda$static$10) | 3 |
| `CAKE_LAYER` | 1 | 0.1 | — | SUGAR_RUSH · 2% · 200 t (lambda$static$12) | 1 |
| `CANDY_CANE` | 2 | 0.1 | — | SUGAR_RUSH · 1% · 200 t (lambda$static$25) | 5 |
| `CANDY_CANE_POLE` | 1 | 0.1 | — | SUGAR_RUSH · 1% · 200 t (lambda$static$26) | 2 |
| `CARAMEL` | 2 | 0.3 | — | SUGAR_RUSH · 4% · 200 t (lambda$static$41) | 1 |
| `CARAMEL_APPLE` | 6 | 0.2 | — | SUGAR_RUSH · 2% · 200 t (lambda$static$42) | 1 |
| `CHOCOLATE_ICE_CREAM` | 4 | 0.2 | — | SUGAR_RUSH · 3% · 200 t (lambda$static$21) | 1 |
| `COOKIE` | 2 | 0.1 | — | SUGAR_RUSH · 1% · 200 t (lambda$static$13) | 2 |
| `COOKIE_HALF` | 1 | 0.05 | — | SUGAR_RUSH · 1% · 200 t (lambda$static$14) | 3 |
| `DARKENED_APPLE` | 4 | 0.35 | alwaysEat | — | 1 |
| `DEEP_SEA_SUSHI_ROLL` | 7 | 0.4 | — | — | 1 |
| `DINOSAUR_NUGGETS` | 3 | 0.3 | meat, fast | — | 1 |
| `DOUGH` | 2 | 0.1 | — | SUGAR_RUSH · 1% · 200 t (lambda$static$15) | 1 |
| `FROSTMINT` | 3 | 0.1 | — | SUGAR_RUSH · 1% · 200 t (lambda$static$28) | 1 |
| `GELATIN` | 3 | 0.25 | — | SUGAR_RUSH · 1% · 200 t (lambda$static$38) | 5 |
| `GIANT_SWEETBERRY` | 5 | 0.2 | — | — | 1 |
| `GINGERBREAD` | 4 | 0.1 | — | SUGAR_RUSH · 1% · 200 t (lambda$static$33) | 4 |
| `GINGERBREAD_CRUMBS` | 1 | 0.1 | — | SUGAR_RUSH · 1% · 200 t (lambda$static$35) | 1 |
| `GINGERBREAD_HALF` | 2 | 0.1 | — | SUGAR_RUSH · 1% · 200 t (lambda$static$34) | 15 |
| `GUMBALL_PILE` | 3 | 0.2 | — | SUGAR_RUSH · 1% · 200 t (lambda$static$43) | 1 |
| `GUMMY_RING` | 3 | 0.15 | — | SUGAR_RUSH · 1% · 200 t (lambda$static$31) | 5 |
| `HOT_CHOCOLATE_BOTTLE` | 4 | 0.25 | sound:undefined | SUGAR_RUSH · 2% · 200 t (lambda$static$39) | 1 |
| `JELLY_BEAN` | 1 | 0.05 | — | — | 1 |
| `LANTERNFISH` | 1 | 0.175 | fast | — | 1 |
| `LANTERNFISH_COOKED` | 2 | 0.3 | fast | — | 1 |
| `LARGE_PEPPERMINT` | 5 | 0.15 | — | SUGAR_RUSH · 1% · 200 t (lambda$static$19) | 1 |
| `LICOROOT` | 3 | 0.1 | — | CONFUSION · 10% · 200 t (lambda$static$16) | 1 |
| `LICOROOT_VINE` | 1 | 0.1 | — | CONFUSION · 10% · 200 t (lambda$static$17) | 2 |
| `LOLLIPOP_BUNCH` | 1 | 0.1 | — | SUGAR_RUSH · 1% · 200 t (lambda$static$27) | 1 |
| `MUSSEL_COOKED` | 4 | 0.3 | fast | — | 1 |
| `PEPPERMINT_POWDER` | 1 | 0.1 | fast | SUGAR_RUSH · 1% · 200 t (lambda$static$40) | 1 |
| `PINE_NUTS` | 2 | 0.175 | — | — | 1 |
| `PRIMORDIAL_SOUP` | 6 | 0.6 | bowl | DIG_SPEED · 100% · 800 t (lambda$static$1) | 1 |
| `PURPLE_SODA_BOTTLE` | 2 | 0.1 | sound:undefined | SUGAR_RUSH · 1% · 200 t (lambda$static$36) | 1 |
| `RADGILL` | 2 | 0.2 | — | IRRADIATED · 100% · 2000 t (lambda$static$2) | 1 |
| `RADGILL_COOKED` | 5 | 0.3 | — | IRRADIATED · 10% · 1000 t (lambda$static$3) | 1 |
| `ROCK_CANDY` | 2 | 0.1 | — | SUGAR_RUSH · 1% · 200 t (lambda$static$32) | 16 |
| `SEA_PIG` | 1 | 0.2 | — | HUNGER · 70% · 1200 t (lambda$static$5) | 1 |
| `SEETHING_STEW` | 6 | 0.6 | bowl | RAGE · 100% · 2200 t (lambda$static$0) | 1 |
| `SERENE_SALAD` | 5 | 0.35 | bowl | — | 1 |
| `SLAM` | 4 | 0.5 | meat | DAMAGE_BOOST · 100% · 400 t (lambda$static$4) | 1 |
| `SMALL_PEPPERMINT` | 3 | 0.15 | — | SUGAR_RUSH · 1% · 200 t (lambda$static$18) | 1 |
| `SOYLENT_GREEN` | 3 | 0.35 | alwaysEat, meat, sound:undefined | — | 1 |
| `SPELUNKIE` | 2 | 0.1 | fast | — | 1 |
| `SPRINKLES` | 1 | 0.1 | — | SUGAR_RUSH · 1% · 200 t (lambda$static$24) | 1 |
| `STINKY_FISH` | 1 | 0.1 | — | STUNNED · 100% · 100 t (lambda$static$6) | 1 |
| `SUGAR_GLASS` | 1 | 0.1 | — | SUGAR_RUSH · 1% · 200 t (lambda$static$29) | 1 |
| `SUNDAE` | 12 | 0.35 | bowl | SUGAR_RUSH · 20% · 400 t (lambda$static$23) | 1 |
| `SUNDROP` | 5 | 0.2 | — | SUGAR_RUSH · 5% · 200 t (lambda$static$30) | 1 |
| `SWEETBERRY_ICE_CREAM` | 4 | 0.2 | — | SUGAR_RUSH · 3% · 200 t (lambda$static$22) | 1 |
| `SWEETISH_FISH` | 2 | 0.2 | — | SUGAR_RUSH · 1% · 200 t (lambda$static$37) | 5 |
| `SWEET_PUFF` | 1 | 0.1 | — | SUGAR_RUSH · 2% · 200 t (lambda$static$11) | 1 |
| `TRILOCARIS_TAIL` | 2 | 0.3 | meat | — | 1 |
| `TRILOCARIS_TAIL_COOKED` | 5 | 0.5 | meat | — | 1 |
| `TRIPODFISH` | 2 | 0.2 | — | — | 1 |
| `TRIPODFISH_COOKED` | 5 | 0.34 | — | — | 1 |
| `VANILLA_ICE_CREAM` | 4 | 0.2 | — | SUGAR_RUSH · 3% · 200 t (lambda$static$20) | 1 |
| `VESPER_SOUP` | 5 | 0.3 | alwaysEat, bowl | NIGHT_VISION · 100% · 2400 t (lambda$static$8) | 1 |
| `VESPER_WING` | 3 | 0.2 | — | HUNGER · 100% · 1200 t (lambda$static$7) | 1 |

## Consumidores diretos

| Owner | Métodos com sites | Sites | Campos distintos |
|---|---:|---:|---:|
| `ACBlockRegistry` | 75 | 75 | 26 |
| `ACItemRegistry` | 40 | 40 | 32 |
| `AlexMealItem` | 1 | 1 | 1 |
| `BiomeTreatItem` | 1 | 1 | 1 |
| `CaveInfoItem` | 1 | 1 | 1 |
| `DarkenedAppleItem` | 1 | 1 | 1 |
| `HotChocolateBottleItem` | 1 | 1 | 1 |
| `JellyBeanItem` | 1 | 1 | 1 |

O [manifesto de descoberta](EXACT-FOODS-DISCOVERY-1.0.10.json) registra todos os campos, offsets do putstatic, hashes dos segmentos, supplier/offset/probabilidade, parâmetros do construtor e todos os sites por owner/método/descriptor/offset. O auditor reproduz referências tipadas completas e associa o BootstrapMethods à implementação de cada supplier. Sites de factories/constructors não são provas de identidade de registry executada nem de consumo real.

## Interoperabilidade e segurança

- Separar estado da construção (estático/global) de estado de consumo por entidade. O builder resolve os suppliers na construção, não a cada ingestão. Não mutar objetos globais por jogador.
- N e m alimentam a fórmula nominal `((float)N*m)*2F`; a referência oficial FoodData clampa fome em 0–20 e saturação à fome atualizada. `fast` altera tempo nominal de uso de 32 para 16 ticks, `bowl` encaminha recipiente, `alwaysEat` libera a condição de fome. Os setters `meat` e `sound` são declarados mas não chegam ao resolve do builder.
- Chance e duração específicas são distintas de efeitos aceitos e do seu ciclo de vida. Sugar Rush, Irradiated, Rage e Stunned são efeitos já inventariados; não contar instâncias de alimento como novas raízes mágicas. A [ficha de Sugar Rush](effects/sugar-rush.md) documenta consumidores temporais e riscos próprios; o [contrato Irradiated](effects/irradiated.md) distingue amplifier e tick.
- O helper não possui targeting/AOE, cast, mana, cooldown, owner ou persistência de jogador. Custos e interação de blocos/itens, registry binding, eventos, modificação de componente e runtime transformado são escopos distintos. Não reexecutar efeitos após Finish; NO_MUTATION/fail-closed.

## Evidência e próximos gates

Relatório SHA-256 `8310d35563ee74028469f192aada383c35a6cd43f70b288ec5ad93de6d8dfed1`, [job de descoberta](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44332664446/job/134900918644). [Auditor](../../../../docs/qa/alexscaves_1010_foods_probe.py) e regressões específicas. Antes de certificado: testar manifesto contra relatório, conferir limite do bridge ACCompat/efeitos e reconciliar índices gerados (sem edição manual) com a main e o marcador #1121. Nenhum contador promovido.
