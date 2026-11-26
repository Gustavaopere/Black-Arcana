# Serene Salad

**Estado:** ⚠️ PARCIAL / STATIC_DISCOVERY_ONLY. `static_contract=NOT_CERTIFIED; mutating_hook=NOT_VERIFIED; physical_qa=NOT_TESTED; NO_MUTATION`. Não constitui nova raiz semântica certificada.

**Autoridade:** Alex's Caves Continued (alexscaves) 1.0.10, Minecraft 1.21.1 / NeoForge / Java 21; modlist sibling #19. Publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. [Replay](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45745854148/job/139661611420), HEAD `41b0080f4a161c9fa82fdb3dc5ed57c3b77f0d82`, dois relatórios byte-idênticos de 384.061 bytes, SHA-256 `4c9aefbfedf99868ae394f1a77dfaaa85cd3c5e8b6d1554b44ed41a902d569b1`. [Dossiê](../EXACT-ORTHOLANCE-MIXTURE-CLUB-1.0.10.md). Sem novo dump físico ou configuração efetiva.

## Identidade e descrição funcional

`alexscaves:serene_salad`; owner `PrehistoricMixtureItem`; factory `ACItemRegistry.lambda$static$35`, Code SHA-256 `06fad7a5b6e47e921cd25b041a9caad976b82bd0671c9f2c5021e8b4076e7c0e`. [Registro](../systems/item-registry.md). Consumível de nutrição e alimentação de criaturas, com comportamento específico do item. Descrição interpretativa do binário.

ACFoods.SERENE_SALAD: N=5, m=0.35, sem efeito declarado pelo builder, bowl. Remove Stunned em finishUsingItem e no ramo de alimentação genérica; exceção de Tremorsaurus atordoado permite alimentação.

## Caminho comum de alimentação e estado

interactLivingEntity(ItemStack,Player,LivingEntity,InteractionHand) resolve ACCompat.food(stack,target) @2. Exige lado não cliente, target Mob, canFeedMob e FoodProperties não nulas. Pede heal(nutrition) @48 (HP, não saturação) antes de callback DinosaurEntity.onFeedMixture(stack,player) @68; se dinosaur callback retorna true, pula aplicação genérica e remoção de Stunned. Caso contrário percorre ACCompat.foodEffects e pede addEffect @111, retornos descartados. Para identidade SERENE_SALAD pede removeEffect(STUNNED) @145. Partículas ITEM são apresentação; não são hit. Fora de creative shrink(1) @225, tenta inserir BOWL @239, se falhar drop @257; retorna SUCCESS. Caso inelegível delega Item.interactLivingEntity @271. Sem mana, cooldown, projétil, dano, AOE ou raio próprio demonstrado. Alvo é a criatura clicada; não há prova de alcance efetivo, autorização ou sucesso de cura/efeito por retorno SUCCESS.

canFeedMob: TremorsaurusEntity com Stunned e item SERENE_SALAD retorna true; RelicheirusEntity com getPushingTreesFor()>0 e item PRIMORDIAL_SOUP retorna false; demais caminhos permitem quando Mob.getTarget()==null ou alvo de ataque não é o jogador. finishUsingItem remove Stunned do consumidor se identidade SERENE_SALAD, depois delega Item.finishUsingItem; sem guarda explícita de lado nesse corpo.

## Integração, custo e pendências

Factory stacksTo(1), ACFoodBuilder.food com perfil específico; [ACFoods](../systems/foods.md) certifica parâmetros declarativos, não settlement. Alimentação de mob solicita cura igual à nutrição, não alimentação do jogador. Em consumo próprio, pipeline herdado decide fome, saturação, duração, recipiente e efeitos; não presumir equivalência com alimentação do mob. Investigar DinosaurEntity.onFeedMixture e overrides, Tremorsaurus/Relicheirus, ACCompat.foodEffects e engine, persistência de status, autoria da cura/XP, proteções PvP e custos/recipiente efetivos. NO_MUTATION: não reaplicar cura/status nem duplicar bowl/consumo ou Mastery.

Receita empacotada `data/alexscaves/recipe/serene_salad.json`, SHA-256 `e28b85927c754677750f61d8e27eda5ed95e7b34593e6086956d0c1c13ed1210`; ingredientes alexscaves:fiddlehead, alexscaves:tree_star, alexscaves:pine_nuts, minecraft:bowl. Não garante aquisição efetiva.

## Localizadores de evidência

Classfile SHA-256 `53a9a6fde7af563cc592bd05d081813bf22c3f0b628e83fb03ae7079b0cc1d56`.

| Método e descritor | Instruções | Code SHA-256 |
|---|---:|---|
| `<init>(Lnet/minecraft/world/item/Item$Properties;)V` | 4 | `405f81f0b51683db4ab14a729fb164a2c889439967d0bfe6248ebe8183a4873d` |
| `interactLivingEntity(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/InteractionHand;)Lnet/minecraft/world/InteractionResult;` | 126 | `502e616a07cf5867ab58bc1ffa79ab16a505a4ddd847b144f7628a06b85c70a9` |
| `finishUsingItem(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;)Lnet/minecraft/world/item/ItemStack;` | 17 | `92ba9838f2a3397d4111ee8c2eaf6277710f63ba8c45c7054eb52cbb3f70f890` |
| `canFeedMob(Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/entity/Mob;)Z` | 44 | `7fefc60255a63f0ded862e18e81e95d91de0bf529e1bf645f440b6785cc68f69` |
