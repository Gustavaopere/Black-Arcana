# Hot Chocolate Bottle — consumo, efeitos e estatísticas (NeoForge 21.1.250)

## Evidência física distribuída

Publisher alexscaves-1.0.10-neoforge+1.21.1.jar (75.279.314 bytes, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c32e9f2e95bffae0e7c`); distribuição oficial NeoForge 21.1.250 (installer `0e47a91ba2139a8db4bf7627af081f7b5789b508bb039ee8dea1272b79693d60`, overlay `1808fab692dc44b2d474295d1cdd9f1fe8a7dceab4f594210873646fafdf1359`, SRG `26ca9c40d7e1681190b428583c38816852218e78df3f8bdb60a59a78503aec71`, universal `1f9cc68fe9ec0416475d34ce76e95a696b9721d5d338168563dab0632c3d2956`).

[Run 45479066017](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45479066017), job 138746986320, artifact 14961422454. 113 registros semânticos em 27 owners; 647.857 bytes; SHA-256 `ac206f62678acd71876df7df3321eb16ee51832a15325515bf23db71bc566464`. Probe `docs/qa/alexscaves_1010_food_status_settlement_250_probe.py`; workflow `.github/workflows/alexscaves-1010-food-status-settlement-250.yml`. A execução inicial 45478737340 falhou por exigir getFoodProperties declarado diretamente em ItemStack. O método é herdado: o probe corrigido exige evidência em ItemStack, Item ou extensões efetivas, não inventa declaração própria.

## Contrato do consumidor

| Método | Code SHA-256 | Pivôs |
|---|---|---|
| HotChocolateBottleItem.<init> | `dfc1ffbfc583a3c1402c2edef5dad6f2ca6cd46585598219e7ed4cff4b415139` | stacksTo @10, HOT_CHOCOLATE_BOTTLE @13, food @16, base @19. |
| HotChocolateBottleItem.finishUsingItem | `a2fc12ac1f8c603a523c94c073c3273591cc9f489982a69985bb0c35fa7111fd` | base @4, guarda ServerPlayer, Stats.CUSTOM/TIME_SINCE_REST @24/27, resetStat @33. Não é o efeito Sugar Rush. |
| DrinkableBottledItem.finishUsingItem | `95b212e27bb63132d450ad19281398dd6166203c2326a8ad223eb89043a402c1` | Item.finishUsingItem @4; trigger @27, awardStat @39; stack vazia -> glass bottle; caso contrário Player sem instabuild -> Inventory.add, fallback drop. |
| LivingEntity.completeUsingItem | `9f4d4e894cc5c99d6b4a371927155f8c3121cf22f3ceba886a2a095d6dd1b1ba` | gates de uso e mão; copy @75; finishUsingItem @94, onItemUseFinish @97, resultado distinto -> setItemInHand @112, stop @116. |
| Player.eat | `25bdfd4dbbec87b9808405d5d3f99cefaa652060659076bae301ad026d7eee94` | FoodData.eat @5, awardStat @19, ConsumeItemTrigger @80, LivingEntity.eat @87; usingConvertsTo presente e sem materiais infinitos -> substituição ou add/drop. |
| LivingEntity.eat | `98feaac982f2135f5f25ce1e3ed245f2c76d9e14909a0634f93d675df1b7c585` | som, addEatEffect @53, consume @59, gameEvent EAT. |
| ItemStack.consume | `c43042f210a955b1d190873e3a0472ece115939bbcbf5eb94bdad5f37b59f8cb` | shrink exceto entidade com materiais infinitos. |

IItemStackExtension.getFoodProperties (Code `e4217757f7f7a5b2d478384e5ff8108e2406913e179c41e9dd83422d0719cc94`) encaminha stack e consumidor ao Item; IItemExtension default `9061420e58bd25d599e468b9ddb853d98b39c4905fb44d1e73044017cde4ed13` lê FOOD. Não assumir que a propriedade contextual é sempre o perfil declarado. O perfil publisher é nutrição 4, modificador 0,25, saturação 2, Sugar Rush 200 ticks com probabilidade 0,02, uso 40 ticks, stack 16, conforme ficha nativa. FoodData.eat(FoodProperties) lê nutrition/saturation e delega add.

LivingEntity.addEatEffect (Code `ae98757e8b6d7b824801569c0c07fb499d415baf124a38f12b46c1a25fb20dec`) lado servidor, percorre effects, nextFloat/probability, effect @58, addEffect @61. PossibleEffect.effect `9971d380c7d678a3f69f479a13e0bdebc01eac7ed26ef601c79c53f5b6436e5a` usa Supplier.get e construtor de cópia. Não converter chance declarada em efeito aceito. CommonHooks.canMobEffectBeApplied(instance,source) `178b8b602ee6b1006673a4a6a2683a70c4abb5fa15ddb7aed2a982491da2e6ed` posta Applicable e consulta resultado. Applicable.getApplicationResult `b652e3e28bc618170764f2ed264b8b5c9c2d3ab86913fab2dbbcbe6161753eb0`: APPLY aceita, DEFAULT depende de canBeAffected, demais rejeitam. EventHooks.onEffectRemoved posta Remove, retorna isCanceled. Nenhum listener real do pack é presumido.

O ciclo Start/Tick publica eventos canceláveis e consulta duração; Finish publica e consulta resultStack. A conclusão de uso não é uma transação única com todos os callbacks e retornos do publisher. Existem chamadas de estatística/criterion no caminho Player.eat e no corpo DrinkableBottledItem, sem prova de que sejam deduplicadas. Não implementar um segundo consumo, efeito, garrafa ou reset.

## TIME_SINCE_REST e spawn

ServerPlayer.resetStat `fb5edec1e490e46e3229adc88abd2c106d16e010e0610f0cf350188460686fc6` solicita setValue e atualiza scoreboard; ServerStatsCounter delega StatsCounter e marca dirty. StatsCounter.setValue `20419543254f871610a64d5b8d4fa38e777483d9a5c262a6a18d20a4afbce005` posta StatAwardEvent, verifica cancelamento e grava getStat/getValue. Evento permite setStat e setValue. Reset pedido não equivale a reset efetivo nem a ausência de phantoms.

EventHooks.firePlayerSpawnPhantoms `3d59aba364f20c2ea4e4d2d1f526efb96206bc002fe38050fbdc283bf2709c79` usa difficulty/random e posta evento; PlayerSpawnPhantomsEvent tem DEFAULT inicial, quantidade e result mutáveis. shouldSpawnPhantoms `a4f4660175e46ab82580df54221a5327bb42acc033ffe0cb2eece7cffedd085d` trata ALLOW e DEFAULT com dimensão, luz do céu e altitude/visibilidade. O spawner tem outras fronteiras já registradas no dossiê downstream; esse evento não demonstra imunidade absoluta.

## Sack of Sating

overrideOtherStackedOnMe `e8ddd4f888f339fac8059e185c0a3d15a8c382514cbff07969d24403650d8516` exige SECONDARY e tag presente; consulta restrição, vazio, edible, tag EXPLODES; calcula fome, retorna recipientes por count (bowl ou classe de garrafa), add/drop, setCount @174, chew timestamp. calculateWholeStackHungerValue `0b120ae846686d32b61ad201d258d136266849b036133792440426957a601b92` lê food, restrição, nutrition e count. Não chama finishUsingItem nem resetStat nesse corpo. O efeito do item ao ser ingerido e ao ser inserido no saco não é intercambiável.

## Estado

Auditoria estática distribuída, não runtime transformado, uso observado, round-trip, hook ou QA. Fichas e índices mantêm status anterior até integração do conjunto de evidências e certificação individual. NO_MUTATION; physical_qa=NOT_TESTED; magic_roots_delta=0.
