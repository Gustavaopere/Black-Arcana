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
