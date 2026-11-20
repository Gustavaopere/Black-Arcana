# ACFoods — propriedades de alimentação e produtores de efeitos

**Contrato estático:** ✅ CERTIFIED_STATIC_7_AXES / STATIC_TECHNICAL_CATALOG_ONLY, candidato #1122. **Hook:** NOT_VERIFIED. **Runtime:** NOT_VERIFIED. **QA física:** NOT_TESTED. **Perk:** NOT_CERTIFIED. **Policy:** NO_MUTATION. Provider OPEN; zero novas raízes mágicas.

## Identidade e comportamento

Suporte declarativo global de FoodProperties de Alex's Caves Continued, mod ID alexscaves, versão publisher 1.0.10, Minecraft 1.21.1, Java 21 e referência NeoForge 21.1.250. Classe `com.github.alexmodguy.alexscaves.server.item.ACFoods`, SHA-256 `a52ec981fe51c97003383a46f7c0b2de06baa5e3ca3f73db988655abce51e12e`; artefato SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. Não é item registrado nem feitiço. O construtor trivial delega Object; a inicialização estática tem 606 instruções e escreve 63 campos public static final. Os outros 46 métodos produzem as instâncias de efeitos.

## Parâmetros individuais e causalidade

[Crosswalk alfabético completo](../EXACT-FOODS-DISCOVERY-1.0.10.md) — cada campo tem nutrição N, modificador m, flags, chance, duração, supplier e quantidade de consumidores; [manifesto verificável](../EXACT-FOODS-DISCOVERY-1.0.10.json) fixa os offsets, descriptors e hashes. 45 campos com efeito declarado, 18 sem efeito declarado pelo builder; 46 suppliers para 10 identidades de efeito. Todos usam MobEffectInstance(Holder,int), amplifier zero na referência vanilla. 33 campos declaram Sugar Rush (32 por 200 ticks, SUNDAE por 400). ALEX_MEAL declara duas instâncias, não dois casts: CONFUSION 200 e BAD_OMEN 48000 ticks, ambas p=1.

| Parâmetro | Semântica estática |
|---|---|
| nutrition / saturationMod | N inteiro, m float; saturação nominal ((float)N*m)*2F, clamp de FoodData no consumo |
| effect | supplier + p float; resolução eager durante build; aplicação externa por cópia, sorteio servidor u<p |
| fast | seis campos; referência 16 ticks em vez de 32 |
| bowl | seis campos; recipiente BOWL |
| alwaysEat | três campos; permissividade de fome |
| meat / sound | cinco e três declarações respectivamente; não lidas por resolve do builder |
| Duração/amplifier | duração específica em ticks, amplifier 0 no construtor de referência; não confundir com tempo de uso ou cooldown mágico |

## Grafo de consumidores e boundary

Censo tipado de 1555 classes, 121 sites em oito owners: ACBlockRegistry 75, ACItemRegistry 40, AlexMealItem, BiomeTreatItem, CaveInfoItem, DarkenedAppleItem, HotChocolateBottleItem e JellyBeanItem um cada. 63/63 campos lidos. O número de sites não prova quantos itens são registrados, quais IDs estão ativos ou a ordem de uso. ACFoods não registra por si os itens nem é prova de seus efeitos próprios. ACCompat.effect chama BuiltInRegistries.MOB_EFFECT.wrapAsHolder @4, não addEffect. Ver [prova e selo](../EXACT-FOODS-CONTRACT-1.0.10.md).

## Targeting, custos, owner e persistência

N/A para cast, dano direto, alcance, AOE, LOS, projétil, mana, cooldown, XP, owner e persistência própria de jogador; ACFoods constrói propriedades compartilhadas, sem argumento de entidade. Entidade consumidora, condições de uso, custo de stack, retorno de recipiente e aplicação de efeitos pertencem ao pipeline de [ACFoodBuilder e engine](food-builder.md) ou a consumidores específicos. Efeitos downstream, como campo temporal de Sugar Rush, não são redefinidos por ACFoods. Sem inferência de resultados aceitos, efeito somado, eligibility PvP ou world safety.

## Integração de perks e validação

Separar nutricional, tempo de ingestão, chance, magnitude, duração, recipiente e status downstream. Não alterar o objeto static final compartilhado, BUILT ou registry por jogador; não reaplicar status depois de Finish. getFoodProperties e eventos de uso são superfícies reais de referência, não hooks homologados. Black Arcana mantém runtime mágico e RPG Skill Tree só fornece progressão por contrato real. NÃO VERIFICADO: transformação instalada, configuração ativa, registro efetivo, overrides de consumo, segurança de mutation e QA física. NO_MUTATION/fail-closed.

[Contrato](../EXACT-FOODS-CONTRACT-1.0.10.md), [selo](../EXACT-FOODS-CONTRACT-1.0.10.json), [crosswalk](../EXACT-FOODS-DISCOVERY-1.0.10.json), [evidência](../EXACT-FOODS-DISCOVERY-1.0.10.md). Relatórios nativo e boundary reproduzíveis, hashes `8310d35563ee74028469f192aada383c35a6cd43f70b288ec5ad93de6d8dfed1` e `0fe3473bee455115e568c58f815cc223014ddf5202c828d2634e48d629733320`. CI final exigida. Próximo escopo alfabético: ACItemRegistry, reservado na #1123.

## Tabela individual de parâmetros e operandos binary32

**N** é o inteiro de nutrição solicitado. **m** e as chances abaixo são a grafia decimal **nominal** dos literais `float` exibidos por `javap`; percentuais são apresentação de `p × 100`, não uma representação decimal exata do float binário. O [selo do contrato](../EXACT-FOODS-NATIVE-CONTRACT-1.0.10.json) preserva valores binary32 e bits para reprodução. Os ticks pertencem ao argumento de duração de `MobEffectInstance(Holder,int)`, não à duração do uso nem à permanência efetiva de status. Essa sobrecarga não recebe amplifier explícito no corpo publisher; o valor resolvido externamente não é inferido como evidência nativa.

Os efeitos próprios referenciados incluem [Sugar Rush](../effects/sugar-rush.md), [Irradiated](../effects/irradiated.md), [Rage](../effects/rage.md) e [Stunned](../effects/stunned.md); seus consumidores/dano/targeting pertencem às fichas respectivas. **45 presets** declaram efeito, com **46 suppliers** porque `ALEX_MEAL` solicita dois; **18 presets** não passam efeito ao builder. A ausência nessa lista não prova ausência de comportamento adicional no item/bloco consumidor.

| Campo de `ACFoods` | N | m (nominal) | Flags declaradas | Efeito solicitado · chance nominal · ticks · supplier | `putstatic` @ | Sites |
|---|---:|---:|---|---|---:|---:|
| `ALEX_MEAL` | 40 | 5 | bowl | `CONFUSION` · 100% · 200 t · `lambda$static$44`; `BAD_OMEN` · 100% · 48000 t · `lambda$static$45` | 1634 | 1 |
| `BIOME_TREAT` | 20 | 0.1 | — | — | 1653 | 1 |
| `BIOME_TREAT_DONE` | 1 | 0.1 | — | — | 1671 | 1 |
| `BLOCK_OF_CHOCOLATE` | 2 | 0.1 | — | `SUGAR_RUSH` · 1% · 200 t · `lambda$static$9` | 582 | 4 |
| `BLOCK_OF_FROSTING` | 1 | 0.1 | — | `SUGAR_RUSH` · 2% · 200 t · `lambda$static$10` | 610 | 3 |
| `CAKE_LAYER` | 1 | 0.1 | — | `SUGAR_RUSH` · 2% · 200 t · `lambda$static$12` | 666 | 1 |
| `CANDY_CANE` | 2 | 0.1 | — | `SUGAR_RUSH` · 1% · 200 t · `lambda$static$25` | 1052 | 5 |
| `CANDY_CANE_POLE` | 1 | 0.1 | — | `SUGAR_RUSH` · 1% · 200 t · `lambda$static$26` | 1080 | 2 |
| `CARAMEL` | 2 | 0.3 | — | `SUGAR_RUSH` · 4% · 200 t · `lambda$static$41` | 1536 | 1 |
| `CARAMEL_APPLE` | 6 | 0.2 | — | `SUGAR_RUSH` · 2% · 200 t · `lambda$static$42` | 1565 | 1 |
| `CHOCOLATE_ICE_CREAM` | 4 | 0.2 | — | `SUGAR_RUSH` · 3% · 200 t · `lambda$static$21` | 918 | 1 |
| `COOKIE` | 2 | 0.1 | — | `SUGAR_RUSH` · 1% · 200 t · `lambda$static$13` | 694 | 2 |
| `COOKIE_HALF` | 1 | 0.05 | — | `SUGAR_RUSH` · 1% · 200 t · `lambda$static$14` | 722 | 3 |
| `DARKENED_APPLE` | 4 | 0.35 | alwaysEat | — | 554 | 1 |
| `DEEP_SEA_SUSHI_ROLL` | 7 | 0.4 | — | — | 446 | 1 |
| `DINOSAUR_NUGGETS` | 3 | 0.3 | meat, fast | — | 81 | 1 |
| `DOUGH` | 2 | 0.1 | — | `SUGAR_RUSH` · 1% · 200 t · `lambda$static$15` | 750 | 1 |
| `FROSTMINT` | 3 | 0.1 | — | `SUGAR_RUSH` · 1% · 200 t · `lambda$static$28` | 1136 | 1 |
| `GELATIN` | 3 | 0.25 | — | `SUGAR_RUSH` · 1% · 200 t · `lambda$static$38` | 1441 | 5 |
| `GIANT_SWEETBERRY` | 5 | 0.2 | — | — | 1024 | 1 |
| `GINGERBREAD` | 4 | 0.1 | — | `SUGAR_RUSH` · 1% · 200 t · `lambda$static$33` | 1294 | 4 |
| `GINGERBREAD_CRUMBS` | 1 | 0.1 | — | `SUGAR_RUSH` · 1% · 200 t · `lambda$static$35` | 1350 | 1 |
| `GINGERBREAD_HALF` | 2 | 0.1 | — | `SUGAR_RUSH` · 1% · 200 t · `lambda$static$34` | 1322 | 15 |
| `GUMBALL_PILE` | 3 | 0.2 | — | `SUGAR_RUSH` · 1% · 200 t · `lambda$static$43` | 1593 | 1 |
| `GUMMY_RING` | 3 | 0.15 | — | `SUGAR_RUSH` · 1% · 200 t · `lambda$static$31` | 1220 | 5 |
| `HOT_CHOCOLATE_BOTTLE` | 4 | 0.25 | sound:GENERIC_DRINK | `SUGAR_RUSH` · 2% · 200 t · `lambda$static$39` | 1476 | 1 |
| `JELLY_BEAN` | 1 | 0.05 | — | — | 1266 | 1 |
| `LANTERNFISH` | 1 | 0.175 | fast | — | 321 | 1 |
| `LANTERNFISH_COOKED` | 2 | 0.3 | fast | — | 342 | 1 |
| `LARGE_PEPPERMINT` | 5 | 0.15 | — | `SUGAR_RUSH` · 1% · 200 t · `lambda$static$19` | 862 | 1 |
| `LICOROOT` | 3 | 0.1 | — | `CONFUSION` · 10% · 200 t · `lambda$static$16` | 778 | 1 |
| `LICOROOT_VINE` | 1 | 0.1 | — | `CONFUSION` · 10% · 200 t · `lambda$static$17` | 806 | 2 |
| `LOLLIPOP_BUNCH` | 1 | 0.1 | — | `SUGAR_RUSH` · 1% · 200 t · `lambda$static$27` | 1108 | 1 |
| `MUSSEL_COOKED` | 4 | 0.3 | fast | — | 427 | 1 |
| `PEPPERMINT_POWDER` | 1 | 0.1 | fast | `SUGAR_RUSH` · 1% · 200 t · `lambda$static$40` | 1507 | 1 |
| `PINE_NUTS` | 2 | 0.175 | — | — | 57 | 1 |
| `PRIMORDIAL_SOUP` | 6 | 0.6 | bowl | `DIG_SPEED` · 100% · 800 t · `lambda$static$1` | 164 | 1 |
| `PURPLE_SODA_BOTTLE` | 2 | 0.1 | sound:GENERIC_DRINK | `SUGAR_RUSH` · 1% · 200 t · `lambda$static$36` | 1384 | 1 |
| `RADGILL` | 2 | 0.2 | — | `IRRADIATED` · 100% · 2000 t · `lambda$static$2` | 191 | 1 |
| `RADGILL_COOKED` | 5 | 0.3 | — | `IRRADIATED` · 10% · 1000 t · `lambda$static$3` | 219 | 1 |
| `ROCK_CANDY` | 2 | 0.1 | — | `SUGAR_RUSH` · 1% · 200 t · `lambda$static$32` | 1248 | 16 |
| `SEA_PIG` | 1 | 0.2 | — | `HUNGER` · 70% · 1200 t · `lambda$static$5` | 406 | 1 |
| `SEETHING_STEW` | 6 | 0.6 | bowl | `RAGE` · 100% · 2200 t · `lambda$static$0` | 133 | 1 |
| `SERENE_SALAD` | 5 | 0.35 | bowl | — | 102 | 1 |
| `SLAM` | 4 | 0.5 | meat | `DAMAGE_BOOST` · 100% · 400 t · `lambda$static$4` | 270 | 1 |
| `SMALL_PEPPERMINT` | 3 | 0.15 | — | `SUGAR_RUSH` · 1% · 200 t · `lambda$static$18` | 834 | 1 |
| `SOYLENT_GREEN` | 3 | 0.35 | alwaysEat, meat, sound:HONEY_DRINK | — | 300 | 1 |
| `SPELUNKIE` | 2 | 0.1 | fast | — | 240 | 1 |
| `SPRINKLES` | 1 | 0.1 | — | `SUGAR_RUSH` · 1% · 200 t · `lambda$static$24` | 1006 | 1 |
| `STINKY_FISH` | 1 | 0.1 | — | `STUNNED` · 100% · 100 t · `lambda$static$6` | 473 | 1 |
| `SUGAR_GLASS` | 1 | 0.1 | — | `SUGAR_RUSH` · 1% · 200 t · `lambda$static$29` | 1164 | 1 |
| `SUNDAE` | 12 | 0.35 | bowl | `SUGAR_RUSH` · 20% · 400 t · `lambda$static$23` | 978 | 1 |
| `SUNDROP` | 5 | 0.2 | — | `SUGAR_RUSH` · 5% · 200 t · `lambda$static$30` | 1192 | 1 |
| `SWEETBERRY_ICE_CREAM` | 4 | 0.2 | — | `SUGAR_RUSH` · 3% · 200 t · `lambda$static$22` | 946 | 1 |
| `SWEETISH_FISH` | 2 | 0.2 | — | `SUGAR_RUSH` · 1% · 200 t · `lambda$static$37` | 1412 | 5 |
| `SWEET_PUFF` | 1 | 0.1 | — | `SUGAR_RUSH` · 2% · 200 t · `lambda$static$11` | 638 | 1 |
| `TRILOCARIS_TAIL` | 2 | 0.3 | meat | — | 18 | 1 |
| `TRILOCARIS_TAIL_COOKED` | 5 | 0.5 | meat | — | 39 | 1 |
| `TRIPODFISH` | 2 | 0.2 | — | — | 360 | 1 |
| `TRIPODFISH_COOKED` | 5 | 0.34 | — | — | 378 | 1 |
| `VANILLA_ICE_CREAM` | 4 | 0.2 | — | `SUGAR_RUSH` · 3% · 200 t · `lambda$static$20` | 890 | 1 |
| `VESPER_SOUP` | 5 | 0.3 | alwaysEat, bowl | `NIGHT_VISION` · 100% · 2400 t · `lambda$static$8` | 533 | 1 |
| `VESPER_WING` | 3 | 0.2 | — | `HUNGER` · 100% · 1200 t · `lambda$static$7` | 500 | 1 |


## Prova binária complementar e limites

Os nomes dos campos não constituem prova de IDs de registry. A fronteira certificada dos 121 sites é a leitura e seu encaminhamento imediato, não a execução aceita do registro ou do consumo.

A [prova nativa complementar](../EXACT-FOODS-NATIVE-CONTRACT-1.0.10.md) e o [selo completo](../EXACT-FOODS-NATIVE-CONTRACT-1.0.10.json) preservam os 48 corpos do owner, os 63 perfis, os 46 suppliers e os bits binary32 dos parâmetros. A referência de amplifier zero do certificado anterior continua separada: o corpo nativo passa Holder e duração sem argumento explícito de amplifier.

[Auditor complementar](../../../../../docs/qa/alexscaves_1010_foods_contract_audit.py), [regressões binárias](../../../../../docs/qa/alexscaves_1010_foods_contract_audit_test.py), [regressões da ficha](../../../../../docs/qa/alexscaves_1010_foods_contract_cards_test.py) e [workflow](../../../../../.github/workflows/alexscaves-1010-foods-contract.yml). A conferência binária é reproduzível sem carregar classes do provider e não homologa hooks ou QA física.
