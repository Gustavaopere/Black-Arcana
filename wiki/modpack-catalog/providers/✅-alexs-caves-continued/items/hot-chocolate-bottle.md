# Hot Chocolate Bottle — `alexscaves:hot_chocolate_bottle`

**Contrato técnico estático:** ✅ `STATIC_TECHNICAL_CATALOG_ONLY` · grau `SHA_EXACT_BINARY_BEHAVIOR` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `NO_MUTATION` · provider `OPEN`. Nenhuma nova raiz semântica certificada.

## Identidade e parâmetros

Publisher `alexscaves-1.0.10-neoforge+1.21.1.jar` (CurseForge file 8856293), 75.279.314 bytes, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c32e9f2e95bffae0e7c`. Minecraft 1.21.1, Java 21; modlist física #001 registra NeoForge 21.1.250, gradle do sibling 21.1.248. Sem novo dump instalado. `HotChocolateBottleItem.class` SHA-256 `69f1d7676c60ede59dc3cb552b7877914d95fa94b89e6d8ce753bdec41191d39`. Dois métodos próprios, zero campos; estende DrinkableBottledItem (SHA `2d51cafe21c91f964887b30b3ebf262bd8d5944d0879fd08df668623763bd713`, sete corpos). ACItemRegistry.HOT_CHOCOLATE_BOTTLE, lambda$static$164 Code `f18af631ec58d5bf8d6b350215a8fab261c218eac2b135b5d8c4fced5e106d53`. Construtor Code `dfc1ffbfc583a3c1402c2edef5dad6f2ca6cd46585598219e7ed4cff4b415139` declara stack 16 @10 e usa ACFoods.HOT_CHOCOLATE_BOTTLE @13 através de ACFoodBuilder.food @16.

Consumível que solicita nutrição, possível Sugar Rush e reset da estatística de tempo desde descanso. Perfil certificado de [ACFoods](../systems/foods.md): nutrição 4, saturationMod 0.25F, saturação nominal 4×0.25×2=2, chance 0.02F (2%) de Sugar Rush durante 200 ticks via lambda$static$39, som GENERIC_DRINK. A aceitação real e composição com efeitos existentes pertencem à engine. [Sugar Rush](../effects/sugar-rush.md).

## Ativação, efeitos e custos

O contrato do ancestral [DrinkableBottledItem / Purple Soda Bottle](purple-soda-bottle.md) fixa uso instantâneo via ItemUtils.startUsingInstantly, animação DRINK, duração 40 ticks, som GENERIC_DRINK. O método base chama Item.finishUsingItem e descarta o retorno; usa stack de entrada para recipiente: vazia devolve garrafa, não vazia pode pedir inserção/drop de garrafa para Player sem instabuild. Herda solicitações de consumo, stats e avanço; não duplicar liquidação. O override `finishUsingItem(ItemStack,Level,LivingEntity)ItemStack` (19 instruções, Code SHA `a2fc12ac1f8c603a523c94c073c3273591cc9f489982a69985bb0c35fa7111fd`) chama ancestral @4, armazena retorno, exige consumidor instanceof ServerPlayer @10–13, solicita resetStat(Stats.CUSTOM.get(TIME_SINCE_REST)) @33 e devolve retorno ancestral @38. Isso não comprova que a bebida simula sono ou elimina todos os spawns de Phantom; consumidor de estatística/efeitos e runtime precisam de QA.

Alvo é o próprio consumidor; dano, projétil, AOE próprio, mana e cooldown próprio N/A nos corpos locais. Não é magia de cura. A receita shapeless exige 2 blocos de chocolate, 1 açúcar, 1 garrafa de vidro; resultado ID hot_chocolate_bottle, quantidade omitida no JSON, default 1 pelo STRICT_CODEC (prova abaixo). SHA `d9973d88982f4e0d3cefa31987dd087d56250a79a5f6da7a32bb2d9bd1d3ff49`. Modelo generated. Aba criativa ACCreativeTabRegistry lambda$static$24 @361.

## Integração e pendências

Sack of Sating tem rota própria por classe DrinkableBottledItem, cujo cálculo de nutrição e recipiente não chama finishUsingItem; não transferir automaticamente reset de TIME_SINCE_REST. A certificação individual delimita o suporte de comida: fornecedor de efeito e fronteira da estatística aprofundados; aquisição e consumidores da tag foram aprofundados nos dossiês abaixo; efeitos físicos permanecem pendentes. QA física: fome cheia, cancelamento, último item, criativo, inventário cheio, reset de estatística e efeito, reload. Nenhum hook seguro para alterar efeito/custo/XP demonstrado. [Dossiê SHA-exato](../EXACT-HOLOCODER-HOT-CHOCOLATE-INK-BOMB-1.0.10.md) · [registro individual de factories](../systems/item-registry.md).

## Evidência downstream adicional — NeoForge 21.1.250

ACFoods.lambda$static$39 cria Sugar Rush por 200 ticks. ServerPlayer.resetStat solicita valor 0, reseta scoreboard; StatsCounter.setValue passa por StatAwardEvent, pode cancelar ou usar stat/value alterados. PhantomSpawner lê TIME_SINCE_REST, clamp [1,INT_MAX]; sem ALLOW do PlayerSpawnPhantomsEvent, nextInt(clamped) precisa ser >=72000 no ramo de insônia. Outros gates permanecem. Reset não garante proteção absoluta. O censo JSON encontrou licowitch_tower loot e gingerbread_man_steals tag, mais referência da receita em livro. [Dossiê downstream 21.1.250](../EXACT-FOUR-ITEMS-DOWNSTREAM-21.1.250.md).


## Liquidação de consumo, efeito e estatística — contrato distribuído adicional

Evidência read-only da PR #1199: [dossiê de consumo e status 21.1.250](../EXACT-FOOD-STATUS-SETTLEMENT-21.1.250.md), [execução 45479066017](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45479066017), relatório de 647.857 bytes, SHA-256 `ac206f62678acd71876df7df3321eb16ee51832a15325515bf23db71bc566464`. Escopo: 113 registros semânticos em 27 owners; classes distribuídas, não runtime transformado.

| Eixo para perks | Fronteira comprovada no recorte | Restrição |
|---|---|---|
| Nutrição e saturação | `IItemStackExtension.getFoodProperties` delega ao Item com stack e consumidor; o default de `IItemExtension` lê FOOD; `FoodData.eat` lê nutrition/saturation e delega add. | Perfil contextual pode divergir do perfil publisher; 4 e 2 são valores nominais, não ganho efetivo garantido. |
| Duração e custo de uso | `LivingEntity.completeUsingItem`: copy @75, finishUsingItem @94, onItemUseFinish @97, setItemInHand @112 quando resultado distinto, stop @116. Eventos Start/Tick consultam duração e podem cancelar; Finish admite resultStack. | Não criar segundo consumo nem substituição de stack; não presumir transação atômica ou material debitado. |
| Chance e duração de Sugar Rush | `LivingEntity.addEatEffect`: servidor, nextFloat/probability, effect @58, addEffect @61. `FoodProperties.PossibleEffect.effect` obtém Supplier e copia a instância. | 0,02 e 200 ticks são parâmetros de solicitação; não equivalem a aplicação ou duração efetiva. |
| Admissão de status | `CommonHooks.canMobEffectBeApplied` publica Applicable; APPLY aceita, DEFAULT depende de canBeAffected e demais resultados rejeitam. Remove também publica evento cancelável. | Não conceder Mastery por tentativa, nem aplicar efeito paralelo ao nativo. |
| Descanso / phantoms | `HotChocolateBottleItem.finishUsingItem` chama ancestral @4 e resetStat @33 apenas para ServerPlayer; `StatsCounter.setValue` publica StatAwardEvent e usa stat/value do evento quando aceito. `PlayerSpawnPhantomsEvent` possui resultado e quantidade mutáveis. | Reset é independente de Sugar Rush; não é imunidade absoluta nem garantia de reset físico. |
| Recipiente e autoria | `DrinkableBottledItem.finishUsingItem` chama Item.finishUsingItem, trata stack vazia e inserção/drop; `Player.eat` também tem caminhos de conversão, estatística e criterion. | Chamadas de estatística/criterion não têm deduplicação comprovada; preservar o consumidor nativo e materiais infinitos. |
| Sack of Sating | `overrideOtherStackedOnMe` usa SECONDARY, tags e gates, calcula fome e retorna recipientes; setCount @174. `calculateWholeStackHungerValue` lê perfil e quantidade. | Não chama finishUsingItem ou resetStat nos corpos examinados; não tratar inserção como ingestão da bebida. |

**Estado desta evidência histórica de descoberta:** `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`. O dossiê permite planejar atributos de nutrição, tempo de uso, chance e duração de efeito, mas não demonstra um hook mutador seguro nem um resultado efetivo no modpack. A aquisição/tag e os consumidores concretos de inventário foram examinados nos complementos abaixo. Nenhuma nova raiz semântica.

## Aquisição, clamp e ciclo de vida — complemento individual

- [Aquisição](../EXACT-FOUR-ITEMS-ACQUISITION-1.0.10.md): licowitch_tower, entrada 15, peso 10/153, rolls 3–8, set_count 1–2; não é chance física sem contexto e modificadores. Tag gingerbread_man_steals: 12 valores, índice 5. [Ingresso e inventário](../EXACT-HOLOCODER-INGRESS-1.0.10.md): handler ENTITY_AUTOMATION, Direction.DOWN; extração solicitada via extractItem(slot,1,false). Não equivale a débito confirmado.
- [Ciclo de vida](../EXACT-CHOCOLATE-EFFECT-LIFECYCLE-21.1.250.md): filtro de roubo exclui Player criativo e GingerbreadManEntity. FoodData.add limita foodLevel a [0,20] e saturação a [0,foodLevel atualizado]; 4/2 são ganhos nominais, não cura. MobEffectInstance.update substitui duração pelo valor maior para mesmo amplifier, não soma. Efeito oculto e expiração têm fluxo próprio; Added não é recibo de liquidação.
- [Defaults e codec](../EXACT-ITEM-ENTITY-DEFAULTS-21.1.250.md): serializer shapeless lê STRICT_CODEC para result. O corpo ItemStack.lambda$static$3 possui count em [1,99], orElse(1); a ligação do inicializador ao STRICT_CODEC foi resolvida no complemento abaixo. Não presumir quantidade efetivamente obtida. `NO_MUTATION / perk_certification=NOT_CERTIFIED / physical_qa=NOT_TESTED`.

### Codec estrito da receita — fechamento do campo nominal

[Run 45525743293](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45525743293), 380.596 bytes SHA-256 `aab3ae48b827b010a92197e8c0c56bc9be8cbb35cadb1e8c0809a9542cc5bcdb`. ItemStack.<clinit> liga CODEC -> lambda$static$4 -> RecordCodecBuilder.create(lambda$static$3); STRICT_CODEC = CODEC.validate(validateStrict). Campo count [1,99] com orElse(1), components opcional EMPTY; validateStrict rejeita componentes inválidos ou count superior ao máximo. Portanto a receita publisher fornece uma unidade nominal. O resultado efetivo ainda depende de registry, datapacks e execução. Nenhum hook ou QA promovido.

## Contrato individual delimitado e sete eixos

A certificação proposta nesta revisão abrange somente o comportamento binário estático do consumível publisher 1.0.10, com distribuição oficial NeoForge 21.1.250. Não afirma paridade com novo dump instalado, runtime transformado, listeners efetivos, execução física, hook ou provider fechado. `perk_certification=NOT_CERTIFIED; runtime_dispatch=NOT_VERIFIED; mutating_hook=NOT_VERIFIED; physical_qa=NOT_TESTED; NO_MUTATION`.

| Eixo | Evidência individual e limite |
|---|---|
| Identidade | Dois corpos próprios e sete do ancestral, factory $164, FOOD perfil HOT_CHOCOLATE_BOTTLE, modelo e receita SHA-exatos. O censo tipado do owner e consumers é limitado ao publisher, não exclui usos externos. |
| Comportamento | Início via ItemUtils.startUsingInstantly, sem teste canEat próprio do Item.use de comida; o perfil do chocolate não declara alwaysEat. Lifecycle Start/Tick/Finish controla duração e resultado. O ancestral solicita ingestão, stats/criterion e retorno de recipiente; o override apenas acrescenta reset de descanso para ServerPlayer e devolve o resultado ancestral. |
| Parâmetros | Stack 16, DRINK 40 ticks, 4 nutrition e 2 saturation nominal, chance 0.02F, Sugar Rush 200 ticks, amplifier padrão 0; clamps de FoodData e MobEffectInstance, merge, cooldown próprio N/A. |
| Targeting | Próprio consumidor (LivingEntity); reset somente ServerPlayer. Sem targeting remoto, dano/tipo, projétil, AOE própria, invocação ou cura direta. O campo temporal eventual é consumidor de Sugar Rush, não efeito incondicional da bebida. |
| Custos | Uma unidade solicitada no pipeline de comida sob regras de materiais infinitos, retorno de garrafa ou inserção/drop; sem segundo shrink próprio no ancestral. Receita 2 blocos de chocolate, 1 açúcar, 1 garrafa -> 1 unidade nominal. Loot e extração por AI não são consumo do player. Mana/durabilidade/stamina própria N/A. |
| Integração | Eventos de uso, stats e efeito são fronteiras distintas e não recibos atômicos. Não modificar FOOD global, chance, duração, stat, retorno da garrafa ou Mastery sem boundary por jogador com causalidade e dedupe; não converter Added ou reset request em cast/XP. |
| Validação | Relatórios publisher 45464509190, downstream 45471957912, aquisição 45473794747, ingresso 45478556000, settlement 45479066017, lifecycle 45513909141 e codec 45525743293. Cada dossiê vincula hashes, corpos, escopo e replay. O CI final do HEAD candidato precisa reproduzir selos e índices. |

### Efeito secundário e fórmula de insônia

ACFoods.lambda$static$39 (Code SHA-256 `3f170597f2af332912135c02914fd01d330cd72ce22a380f3b7d8fea9e8ccbe9`) chama MobEffectInstance(Holder,I) com 200 @18–21. Essa overload (Code `06a69552697053160dd15a4a46255187e61416a95e4cb00e7229ec8849852e06`) passa amplifier=0 @3; o construtor terminal clampa amplifier em [0,255]. O [contrato Sugar Rush](../effects/sugar-rush.md) separa modifier MOVEMENT_SPEED +0.699999988079071D ADD_MULTIPLIED_TOTAL, e evento de aplicação para Player adicionado ao mundo com config sugar_rush_slows_time: solicita campo temporal de raio 10D, multiplier 2F e ceil(duration×2F), nominal 400 para a instância de 200 ticks. O ramo de refresh altera maxDuration, não reinicia a idade; a aplicação efetiva depende dos gates, merge e scheduler. Não multiplicar velocidade efetiva ou tempo real por esses argumentos.

PhantomSpawner.tick Code `b63e8bc63bd4827bf4c1ed42499eca13f5f09130585f7a9246d6f9465ef24d1f`: no ramo não ALLOW que alcança a verificação de insônia, S=clamp(TIME_SINCE_REST,1,2147483647), nextInt(S) @254, comparação com 72000 @259–261. Sob sorteio uniforme, fração favorável desse gate é max(0,S−72000)/S. Não é probabilidade total de spawn: outros gates de dificuldade, ambiente, eventos e tentativa de criação permanecem. O pedido resetStat não é sono nem imunidade.

Persistência própria: nenhum campo na subclasse, nenhum estado/owner customizado do objeto; FOOD e contagem pertencem à stack e duração/status à entidade; TIME_SINCE_REST pertence ao StatsCounter do ServerPlayer. Não declarar round-trip de saves. QA física: fome cheia, cancelamentos Start/Tick/Finish, stack final e múltipla, criativo, inventário cheio, aplicação/refresh/remoção de Sugar Rush, config on/off, stat modificado/cancelado, spawn de phantom, reload e interoperabilidade. Nenhum novo cast/raiz.
