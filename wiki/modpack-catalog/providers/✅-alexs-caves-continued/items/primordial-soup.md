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

### Primeira execução: falha de orçamento, correção do recorte

[Run 46097698910 / job 140832759965](https://github.com/Gustavaopere/Black-Arcana/actions/runs/46097698910/job/140832759965), HEAD `4698c2b442629bf2d79388cda66b28f0d6ef875d`: compilação/autoteste e download passaram; projeção falhou em analyze/refs com `AuditError: bounded typed member census` (limite 180); segundo replay foi pulado. O log inicial não identifica o método causador, portanto não atribuir a falha conclusivamente ao inicializador ACFoods. Schema 2 no commit `ae077e01d525f2a735a65d8a810c51e45fb0ee0a` remove a reprojeção redundante do inicializador já documentado em [Foods](../systems/foods.md), mantém seu hash de classe pinado, registra explicitamente essa reutilização e imprime o owner/método/descritor imediatamente antes de cada projeção. Preserva o limite do auditor compartilhado e todos os demais pins. Não é aprovação: nova execução e interpretação pendentes. `NOT_CERTIFIED / NO_MUTATION / NOT_TESTED`.

### Schema 2 — coleta aprovada: callbacks e alimentação manual

[Run 46098019418 / job 140833792490](https://github.com/Gustavaopere/Black-Arcana/actions/runs/46098019418/job/140833792490), HEAD `0d919b38e4a662585b76e174da042a11d1412f75`: todas as etapas do job específico success, dois relatórios byte-idênticos de 89.931 bytes, SHA-256 `ad683a0c8729d933f7d9229077fad9a7078e5a15cf083d2a407ce04a60299489`. Reproduz os pins anteriores e confirma o roster de 1555 classes. O RED de orçamento foi superado pelo recorte, sem afrouxar o limite compartilhado.

**Contexto alimentar:** ACCompat.food Code `49c3062c4a6ee9829b530154697caa1dd8dc98766d46b57c24b5f08d61a3ab0c` lê DataComponents.FOOD @1/4 e retorna o valor; não usa o parâmetro LivingEntity nesse corpo. foodEffects Code `80c87f04f2edac76d7e5b98161ad563b34e5337fa39e2ade0e6cf0f6a227fd80`: se food=null retorna List.of, senão effects @17 → stream @20 → bootstrap #4 @25 vincula PossibleEffect.effect() → map @30 → toList @35. Não há sorteio de probability nessa rota manual. A probabilidade do consumo próprio não deve ser aplicada automaticamente à alimentação de Mob. A leitura do componente da stack pode divergir do default de ACFoods.

| Declaração própria onFeedMixture(ItemStack,Player)Z no publisher | Code SHA-256 | Resultado do ramo |
|---|---|---|
| DinosaurEntity | `42ca1f85243342bd41983ab86f2235408fa46ded7466d4525196f66b9dbb5f3e` | retorna false. |
| AtlatitanEntity | `23838db2fc5224e6148c338dc0393b9d364b314e3cabc2c574fab705c59e16a8` | SERENE_SALAD → setRideableFor(12000), true; outros itens false. |
| RelicheirusEntity | `a0ef71f1ac4a371c3831a21909523f6a812e0d57bc7b5875045a8e8fed39df8b` | PRIMORDIAL_SOUP @1–15 → setPushingTreesFor(1200) @22, true @26; outros itens false @28. |
| TremorsaurusEntity | `e22a2a8f14a204e7f9a6d9bf52961e490073b77451f841bea3b2d74106ce191e` | exige SERENE_SALAD e STUNNED; não é efeito da sopa. |
| VallumraptorEntity | `653ce79958bdc518eff99951937a2cd86dc7655e51b699edbcae735b4e74cf84` | exige SERENE_SALAD, relaxedFor>0 e !isTame; não é efeito da sopa. |

O censo localiza cinco declarações no roster, não comprova dispatch de subclasses externas. Para a identidade nominal da sopa, o override Relicheirus retorna true e faz interactLivingEntity saltar de @71 a @149, suprimindo o loop genérico addEffect e a remoção de STUNNED, mas preservando partículas e liquidação do item. O pedido de heal(nutrition) @48 antecede esse callback. Portanto não atribuir Haste automaticamente ao Relicheirus alimentado por essa rota. O timer inicial 1200 é valor inteiro de estado; equivaleria a 60 s somente se decrementado uma vez por tick sem pausa/redefinição. getPushingTreesFor Code `ab032076a06067673326b98ae36aec0adcf6fad8df25c375803f3eaebcafca71` lê PUSHING_TREES_FOR; setter Code `edc925281dc6cfe63dff588a9acec0631f125dc7ce4d900641a5f86094c3dcdf` grava SynchedEntityData @11 sem clamp explícito. Ainda faltam decremento, consumidores AI, regras de quebra/queda das árvores, atribuição, persistência e settlement. A existência de setter não o torna API de perk segura.

Censo de 1563 JSON data/: dois recursos literais, receita já pinada e `data/alexscaves/advancement/alexscaves/feed_relicheirus.json` SHA `8837ef0429fbac955e4c7bf32da1a9f7e7aa19ae29d5b87fe7d956ce5905a9fa`: trigger player_interacted_with_entity, filtro alexscaves:relicheirus e item primordial_soup. Não prova sucesso da cura, estado, desbloqueio obrigatório nem receipt de Mastery. Censo literal não exclui tags/datapacks indiretos.

**Conclusão parcial:** a coleta específica passou; o contrato da alimentação do Relicheirus ainda não está fechado no downstream. Nenhuma promoção de certificado, índice, raiz, hook, QA ou Stage. NO_MUTATION.

### Continuação — schema 3: consumidores do timer

Base atual `5dc7cbb683e8cdce9a2cc8c37a29fd00fcd4fe77` (sete contratos de Evocation do sibling provider preservados); merge de sincronização `1faa32a1488c05506822fed7a0491c2bda58e6fb`. A HEAD documental anterior `3738a524382941cf42b9c5384a082fbdb6b295f8` passou 42/42 workflows observados, inclusive coleta 46098220420; não transferir esse PASS para nova HEAD. O commit `7415981e29400a7929ca0fc7bb83878ef4bdea5a` amplia a coleta existente para censo dos Fieldref/Methodref/InterfaceMethodref pelos pares exatos nome+descritor de PUSHING_TREES_FOR e getter/setter, inclusive owners herdados candidatos; separa candidatos no constant pool de instruções diretas, preserva todas as ocorrências e janelas locais, hashes Code/class e handles candidatos. Não presume que um homônimo seja dispatch real, nem que janela local prove efeitos downstream de AI. O objetivo é localizar decremento, persistência e consumidores de quebra de árvores; execução e interpretação ainda pendentes. Sem relaxar limites compartilhados; `NOT_CERTIFIED / NO_MUTATION / NOT_TESTED`.

### Schema 3 — censo de consumidores confirmado

[Run 46151519358/job 140998981800](https://github.com/Gustavaopere/Black-Arcana/actions/runs/46151519358/job/140998981800), HEAD 8ff291785bc851ff3b4d8a4b118d4ec48791956b: 42/42 workflows observados success, relatório de 137.782 bytes SHA-256 `3f2338eb3d6007aee556daf9ef92dc042e0f1659c3cf60036856458b7fc7fcb3`, replay idêntico. Sincronização posterior com main `7c5d7c9b43ffc91bc394aa5fed5b5be8af5ed631` em 996ac7a216f296cddfe1c237a71595745b6bec1f; CI anterior não certifica nova HEAD.

Censo de 1555 classfiles: três owners com referências diretas aos pares exatos do timer; nenhum handle candidato nesse recorte. RelicheirusEntity class SHA `50ba008765f00653c630f9c8e4fd28ab45f8c7e97a054a9858995676f007651f`: defineSynchedData Code `06413255be5f3e7a7f56ed1f017afa88a8b5679a1df4e24781c133558c43cd1c`, inicializa PUSHING_TREES_FOR=0 @30–37; tick Code `e2fbb728287e9f002a20db59869ff33a08d3ee1730b3d469eb4bf55bdb1c73aa`, @382–395, se T>0, T'=T−1. A carga nominal de 1200 corresponde a 60 s a 20 TPS se o ramo executar uma vez por tick sem pausa ou reinicialização. A janela não prova toda autoridade de lado nem comportamento após unload. Nenhuma referência direta ao trio de membros em método NBT foi encontrada; isso não exclui persistência indireta por superclass, transformação ou dados externos.

RelicheirusPushTreesGoal class SHA `9307599bad3302757d4848a25eb74ded440b5bd127d981d234b36df2cbefc3c3`, canUse Code `3495e712e9b5d7dc3955eb23727bc62b68cb2890a33f6b17cd7b03e563dfe458`: T>0 @4–7, !isBaby @14–17 e MoveToBlockGoal.canUse @21–24. O timer autoriza tentativa de início de goal, não demonstra término, quebra, drop, owner ou execução contínua. PrehistoricMixtureItem.canFeedMob @55–74 rejeita nova sopa enquanto T>0. Falta o corpo completo do goal, sua inscrição, continuação, filtros de árvore e settlement de mundo. NOT_CERTIFIED / NO_MUTATION / NOT_TESTED.

### Continuação — schema 4, goal e ciclo de estado

Base 7c5d7c9b43ffc91bc394aa5fed5b5be8af5ed631, sem alteração de versão. A coleta específica da revisão 0ceea7b75d933a9a94828822aa11664d8db01d8d (run 46154120572) retornou success. O schema 4 acrescenta a declaração integral e corpos próprios de RelicheirusPushTreesGoal, pinando a classe e canUse, e projeta o tick, registro de goals, save/load e métodos relacionados a árvores/estado de RelicheirusEntity, com pin da classe e Code do tick. Localiza ainda chamadas diretas do goal a corpos declarados no namespace publisher, separando candidato CP de dispatch; os métodos herdados/indiretos continuam explícitos. O coletor é read-only, com roster, Code hashes, orçamento e dois replays. Não cria comportamento nem relaxa a guarda global. Nova execução pendente; o escopo continua NOT_CERTIFIED / NO_MUTATION / NOT_TESTED.
