# Primordial Soup

**Estado:** ⚠️ PARCIAL / STATIC_DISCOVERY_ONLY. `static_contract=NOT_CERTIFIED; mutating_hook=NOT_VERIFIED; physical_qa=NOT_TESTED; NO_MUTATION`. Não constitui nova raiz semântica certificada.

**Autoridade:** Alex's Caves Continued (alexscaves) 1.0.10, Minecraft 1.21.1 / NeoForge / Java 21; modlist sibling #19. Publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. [Replay](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45745854148/job/139661611420), HEAD `41b0080f4a161c9fa82fdb3dc5ed57c3b77f0d82`, dois relatórios byte-idênticos de 384.061 bytes, SHA-256 `4c9aefbfedf99868ae394f1a77dfaaa85cd3c5e8b6d1554b44ed41a902d569b1`. [Dossiê](../EXACT-ORTHOLANCE-MIXTURE-CLUB-1.0.10.md). Sem novo dump físico ou configuração efetiva.

## Identidade e descrição funcional

`alexscaves:primordial_soup`; owner `PrehistoricMixtureItem`; factory `ACItemRegistry.lambda$static$37`, Code SHA-256 `5814d536831c0df71d18745af3571e2420a7881043c4011999201da8e21dc26e`. [Registro](../systems/item-registry.md). Consumível de nutrição e alimentação de criaturas, com comportamento específico do item. Descrição interpretativa do binário.

ACFoods.PRIMORDIAL_SOUP: N=6, m=0.6, DIG_SPEED 800 ticks p=1; bowl. Exceção de Relicheirus durante pushingTreesFor>0.

## Caminho comum de alimentação e estado

interactLivingEntity(ItemStack,Player,LivingEntity,InteractionHand) resolve ACCompat.food(stack,target) @2. Exige lado não cliente, target Mob, canFeedMob e FoodProperties não nulas. Pede heal(nutrition) @48 (HP, não saturação) antes de callback DinosaurEntity.onFeedMixture(stack,player) @68; se dinosaur callback retorna true, pula aplicação genérica e remoção de Stunned. Caso contrário percorre ACCompat.foodEffects e pede addEffect @111, retornos descartados. Para identidade SERENE_SALAD pede removeEffect(STUNNED) @145. Partículas ITEM são apresentação; não são hit. Fora de creative shrink(1) @225, tenta inserir BOWL @239, se falhar drop @257; retorna SUCCESS. Caso inelegível delega Item.interactLivingEntity @271. Sem mana, cooldown, projétil, dano, AOE ou raio próprio demonstrado. Alvo é a criatura clicada; não há prova de alcance efetivo, autorização ou sucesso de cura/efeito por retorno SUCCESS.

canFeedMob: TremorsaurusEntity com Stunned e item SERENE_SALAD retorna true; RelicheirusEntity com getPushingTreesFor()>0 e item PRIMORDIAL_SOUP retorna false; demais caminhos permitem quando Mob.getTarget()==null ou alvo de ataque não é o jogador. finishUsingItem remove Stunned do consumidor se identidade SERENE_SALAD, depois delega Item.finishUsingItem; sem guarda explícita de lado nesse corpo.

## Integração, custo e pendências

Factory stacksTo(1), ACFoodBuilder.food com perfil específico; [ACFoods](../systems/foods.md) certifica parâmetros declarativos, não settlement. Alimentação de mob solicita cura igual à nutrição, não alimentação do jogador. Em consumo próprio, pipeline herdado decide fome, saturação, duração, recipiente e efeitos; não presumir equivalência com alimentação do mob. Investigar DinosaurEntity.onFeedMixture e overrides, Tremorsaurus/Relicheirus, ACCompat.foodEffects e engine, persistência de status, autoria da cura/XP, proteções PvP e custos/recipiente efetivos. NO_MUTATION: não reaplicar cura/status nem duplicar bowl/consumo ou Mastery.

Receita empacotada `data/alexscaves/recipe/primordial_soup.json`, SHA-256 `02968ed3e6687885654aab4e93562f63a814bb6fbcc830cfcb099bc9a65bfb31`; ingredientes alexscaves:cooked_trilocaris_tail, alexscaves:cooked_trilocaris_tail, alexscaves:tree_star, minecraft:bowl. Não garante aquisição efetiva.

## Localizadores de evidência

Classfile SHA-256 `53a9a6fde7af563cc592bd05d081813bf22c3f0b628e83fb03ae7079b0cc1d56`.

| Método e descritor | Instruções | Code SHA-256 |
|---|---:|---|
| `<init>(Lnet/minecraft/world/item/Item$Properties;)V` | 4 | `405f81f0b51683db4ab14a729fb164a2c889439967d0bfe6248ebe8183a4873d` |
| `interactLivingEntity(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/InteractionHand;)Lnet/minecraft/world/InteractionResult;` | 126 | `502e616a07cf5867ab58bc1ffa79ab16a505a4ddd847b144f7628a06b85c70a9` |
| `finishUsingItem(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;)Lnet/minecraft/world/item/ItemStack;` | 17 | `92ba9838f2a3397d4111ee8c2eaf6277710f63ba8c45c7054eb52cbb3f70f890` |
| `canFeedMob(Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/entity/Mob;)Z` | 44 | `7fefc60255a63f0ded862e18e81e95d91de0bf529e1bf645f440b6785cc68f69` |

## Reconciliação de consumo próprio e alimentação de criatura — coleta complementar

Base Black Arcana `81dbec3021492e8862b36bb6bbb844d956d742d9`; modlist sibling [b05e253](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/b05e2536461bc0a9c526dc47a38e3b9af62d941c/PROJECT-INSTRUCTIONS/modlist/modlist.md), linhas físicas #001 NeoForge 21.1.250 e #019 publisher Alex's Caves Continued 1.0.10, confirmadas documentalmente. Não houve dump físico da instalação.

### Contratos compartilhados reutilizáveis (sem transferência de certificado)

A [auditoria distribuída do consumo/status](../EXACT-FOOD-STATUS-SETTLEMENT-21.1.250.md) registra o engine 21.1.250, run 45479066017 / job 138746986320, 647.857 bytes, SHA-256 `ac206f62678acd71876df7df3321eb16ee51832a15325515bf23db71bc566464`. Os seguintes limites são úteis para a rota de consumo próprio, condicionados ao dispatch e às propriedades contextuais do item:

| Fronteira | Evidência anterior | Implicação para perks |
|---|---|---|
| IItemStackExtension.getFoodProperties | Code `e4217757f7f7a5b2d478384e5ff8108e2406913e179c41e9dd83422d0719cc94` | Encaminha stack e consumidor ao Item; perfil declarativo não prova resolução contextual. |
| Player.eat | Code `25bdfd4dbbec87b9808405d5d3f99cefaa652060659076bae301ad026d7eee94` | Fome, estatística, criterion, consumo herdado e usingConvertsTo; não repetir débito ou recipiente. |
| LivingEntity.addEatEffect | Code `ae98757e8b6d7b824801569c0c07fb499d415baf124a38f12b46c1a25fb20dec` | Rota server-side com chance e addEffect; não é prova do caminho manual de alimentação de Mob. |
| CommonHooks.canMobEffectBeApplied | Code `178b8b602ee6b1006673a4a6a2683a70c4abb5fa15ddb7aed2a982491da2e6ed` | Applicable e resultado externo podem afetar a aceitação; nenhuma configuração/listener real presumido. |
| LivingEntity.completeUsingItem | Code `9f4d4e894cc5c99d6b4a371927155f8c3121cf22f3ceba886a2a095d6dd1b1ba` | Finish, substituição de stack e encerramento do uso são fronteiras distintas; não confundir com interactLivingEntity. |

O heal(nutrition) do caminho de Mob solicita 6 HP para o perfil declarado da sopa; não é garantia de cura efetiva nem de saturação. O callback onFeedMixture ocorre depois do pedido de cura, e seu retorno pode suprimir a aplicação genérica de efeitos. A exceção do Relicheirus depende de estado mutável (pushingTreesFor), não de um cooldown comprovado do item. Não conceder XP/Mastery pela mera execução do callback, SUCCESS ou consumo. Amplificador efetivo, filtros/contexto da alimentação e tratamento de efeitos no ramo manual ainda exigem a nova leitura.

### Coleta read-only preparada

[Probe](../../../../../docs/qa/alexscaves_1010_primordial_soup_probe.py) e [workflow](../../../../../.github/workflows/alexscaves-1010-primordial-soup.yml) pinam o publisher e o roster de 1555 classes, quatro hashes de classe, quatro hashes Code já evidenciados e a receita. A coleta busca declarações homônimas de onFeedMixture em todo o roster (não implica dispatch), projeta corpos próprios selecionados, métodos ACCompat.food/foodEffects, getters/setters de pushingTreesFor e inicializador ACFoods. Censo literal de recursos JSON e dois replays byte-idênticos. Não executa código do provider nem amplia o escopo certificado de outros itens. A prova de callsites, hierarquia, branches e settlement deverá ser interpretada após a coleta; não inferir efeitos dos overrides pelo nome.

Resultado da nova coleta: PENDENTE. Não foram promovidos índice, ledger, hooks, raiz semântica, QA física ou Stage. `STATIC_DISCOVERY_ONLY / NOT_CERTIFIED / NO_MUTATION / NOT_TESTED`.
