# Druid Shard — contrato estático 4.0.3

O selo cobre o ritual desde a montagem até o item no núcleo e seu transporte pelo Automator. O uso posterior do item tem referências próprias. Hooks mutadores, QA no modpack e universo integral do provider continuam em aberto. [Ficha](rituals/druid-shard.md) · [Selo SHA-exato](EXACT-4.0.3-DRUID-RITUAL.json)

## Receita e alcance do contrato

O JAR Alshanex 4.0.3, publisher 1171602/8675568, SHA-1 `e5051c2385a426d05bf203ba8081a23d891f6686`, contém `data/alshanex_familiars/recipe/ritual_recipes/druid_shard.json`, SHA-256 `157c741fe3875fe70d128b10faff8188c6f71c2297fee89923360a8ebb22bb4c`. O ID da receita é `alshanex_familiars:ritual_recipes/druid_shard`, com tipo `alshanex_familiars:ritual_recipe`, central `alshanex_familiars:pet_soul`, resultado `alshanex_familiars:druid_shard` e partícula `minecraft:composter`. A conferência do tipo/serializer e das classes de execução reaproveita o mesmo contrato SHA-exato do altar. [Evidência comum](EXACT-4.0.3-ARCHMAGE-RITUAL.md)

| Eixo | Prova no binário e no recurso |
|---|---|
| Matching | `RitualHelper.isValidRecipe` exige as quatro estátuas cardeais a dois blocos. `RitualRecipeType.matches` verifica o central e o total exato de quatro periféricos. Os quatro IDs distintos têm contagem 1. |
| Duração | `RitualCorePedestalEntity.tick @38` revalida a receita. Os incrementos válidos chegam a 100, com solicitação de partículas a cada 10. O contador fica pausado quando o central continua elegível e a montagem periférica deixa de corresponder. |
| Custos | `RitualHelper.clearItemsFromPedestals @143–149` lê `consume` e salta para o próximo requisito quando falso. A Spore Blossom é a única entrada com esse valor. O núcleo substitui a Familiar Soul por uma nova stack de uma unidade no final. |
| Recebedores e efeito | `RitualHelper.getParticleForRecipe` resolve `minecraft:composter` do recurso. O núcleo também solicita Blastwave visual de Evocation no final. O contrato é de inventário de bloco, com targeting vivo, dano e status inaplicáveis ao craft. |
| Persistência e autoridade | O núcleo persiste stack central, flags e contador. O Automator persiste seleção e transferências. O uso desses estados para um hook mutador ou para atribuir o ritual a um jogador continua `NOT_VERIFIED`. |

`matches` aplica a mesma lógica de contagem a cada requisito, incluindo o catalisador. A retenção acontece somente no settlement. Para esse recurso, o núcleo esvazia as três estátuas com ingredientes consumíveis e escreve a saída central. O algoritmo de matching trabalha em cópias e o de consumo limpa stacks reais, uma por requisito consumível. Os fatos acima cobrem a montagem canônica com uma unidade de cada item. Datapacks, estado recarregado e interferência entre jogadores são condições de QA do host. [Métodos comuns](EXACT-4.0.3-ARCHMAGE-RITUAL.md#settlement-e-limites-de-transação)

## Ritual Automator

A seleção compara `RecipeHolder.id` com o ID armazenado. No núcleo, o match continua por tipo e ingredientes. Para a receita Druid selecionada, `performCleanup @209–231` mantém o periférico se ele passar no teste de um ingrediente. `performSupply @135–152` considera a stack presente e chama `removeNeed`, que testa o ingrediente e remove sua exigência da lista de abastecimento (`@26–38`). Portanto, na montagem que concluiu Druid, a Spore Blossom retida e ainda disponível preenche o mesmo requisito na montagem seguinte.

Transporte e coleta usam o mesmo fluxo do Archmage, com **20 ticks de processamento por voo**, comparação de item/components com o resultado e retorno a inventário ou drop para itens que sobram. Confirmar retomada após unload, destino ocupado e alternância de receita exige QA. Escolher outra receita pode tornar o catalisador incompatível com a montagem nova e acionar a limpeza. [Fluxo comum](EXACT-4.0.3-ARCHMAGE-RITUAL.md#automação)

## Binding e uso do shard

`ItemRegistry.<clinit> @687–698` registra `druid_shard` em `DRUID_RUNE`. O bootstrap 38 do supplier aponta para `DruidShard.<init>()V`. `DruidShard` estende `AbstractRuneItem` do FamiliarsLib 1.7.1. O verificador confere esse JAR usando os hashes do selo comum. Sua chamada de uso reduz a stack (`useOn @25`), executa o override (`@33`) e encaminha o avanço para `ServerPlayer` no ramo próprio (`@52`).

`DruidShard.spawnFamiliar` vincula `DRUID_PET` (`@4`), seta impostor falso (`@21–25`), posiciona no centro do bloco clicado mais 1 em Y (`@31–40`) e aplica a rotação Y negada do jogador (`@46–50`). A chamada `Level.addFreshEntity @56` tem o retorno descartado (`@59`). Esse consumo e essa tentativa de spawn ocorrem após o craft. O override inspecionado não comprova domesticação, vínculo de dono ou entidade inserida.

## Reprodução

Com Java 21 e os JARs publisher 1171602/8675568 e 1316458/8059464:

```sh
python3 docs/qa/alshanex_403_archmage_ritual_contract.py \
  --jar /caminho/alshanex_familiars-1.21.1_v4.0.3.jar \
  --familiarslib /caminho/familiarslib-1.7.1.jar --ritual druid_shard --verify
```

O verificador reproduz o selo compartilhado de Archmage e confere o hash desse selo antes de comparar os fatos específicos de Druid. Os registros incluem hashes, assinaturas e pontos selecionados do bytecode. QA físico continua `NOT_TESTED`. Os cenários específicos de Druid são montagem sem flor, dois ciclos com a mesma flor, remoção da flor durante a contagem e troca de receita selecionada no Automator.
