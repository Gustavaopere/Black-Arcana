# Fronteiras nativas — cinco classes, publisher 1.0.10

Estado: DISCOVERY_NOT_CERTIFIED. Relatório SHA-256 ec96f80a27cd7c12b9bc114864290210574be7bc07f49b716d93ae14ce793490, job 136078291012. Replay inicial: quatro testes aprovados. O manifesto sela os seis owners adicionais e todas as referências de classe executáveis dos cinco alvos.

## AlwaysCombinableOnAnvil

Interface vazia implementada por RaygunItem e ShotGumItem, mas com uso real em CommonEvents.onUpdateAnvil(AnvilUpdateEvent)V: instanceof @7, identidade Java dos itens Left/Right @27, mapas de encantamento não vazios @40/@53. Copia Left, começa custo 0 e compatibilidade true. Para cada encantamento de Right, obtém níveis L, R, calcula R+1 quando iguais, max(L,R) quando diferentes; verifica compatibilidade com os demais holders na cópia, acrescenta 1 por incompatibilidade. **A flag de compatibilidade não é reinicializada por encantamento**: após a primeira incompatibilidade, as entradas posteriores também deixam de ser aplicadas; a ordem do iterador importa. Se a flag permanece true, limita ao máximo do encantamento e grava nível; custo soma peso convertido por tableswitch vezes nível resultante. Ao final chama setCost(long) @379 e setOutput(copy) @392, mesmo após incompatibilidade. Nenhum setMaterialCost, nenhum débito direto, nenhum reparo de durabilidade demonstrado. A análise da tabela de pesos e da anotação está em auditoria complementar. Não confundir o pedido de saída com transação aceita ou segurança de hook.

## BiomeTreatItem

Use exige presença do componente FOOD e ausência de chave CaveBiome, testa Player.canEat; startUsingItem e consume/pass/fail por bridges ACCompat. ACCompat lê FOOD diretamente, sem usar o argumento LivingEntity. getTag copia CUSTOM_DATA; setTag remove ou grava CustomData.of. finishUsingItem cria NOVA stack vinculada quando chave ausente e jogador com foodLevel zero ou criativo, sem chamar super nesse ramo. CaveInfoItem.create grava CaveBiome e substitui FOOD por BIOME_TREAT_DONE em BiomeTreat vinculado. unwrapKey().get e ResourceLocation.parse são fronteiras de validação sem tratamento comprovado nesse fluxo local. Conversão ambiental do crucible, cor, consumo e persistência exigem disposição individual; não presumir execução da alteração do bioma.

## Suportes de bloco

BlockItemWithISTER: factories 439 (propriedades padrão do helper) e 445 (UNCOMMON), callback getISTERProperties/Consumer.accept. BlockItemWithScaffolding: factory 438, updatePlacementContext com literal 12 e mustSurvive=false. MetalScaffoldingBlock.getDistance inicia em 12, herda distância vertical de scaffolding, retorna 0 para suporte tag ou face sturdy, minimiza distância horizontal +1 apenas para scaffolding compatível, encerra cedo quando 1. SupplierLore: factory 437 e bootstrap exato de concatenação, chave block.<namespace>.<path>.desc em cinza, super tooltip. Identidades concretas de registro e referência engine para colocação ainda precisam de validação; nenhuma nova raiz semântica presumida.

NO_MUTATION / NOT_VERIFIED / NOT_TESTED. Não há certificação de item ou provider nesta etapa.
