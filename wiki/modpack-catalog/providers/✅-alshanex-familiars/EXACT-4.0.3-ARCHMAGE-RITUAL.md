# Archmage Shard — contrato estático do ritual 4.0.3

**Escopo:** `STATIC_TECHNICAL_CATALOG_ONLY`, grau `SHA_EXACT_BINARY_BEHAVIOR`, limitado à cadeia de recursos **insumos do altar → ritual → Archmage Shard**. O resultado desta ficha não inclui usar a shard para invocar/domesticar um familiar, controlar AI, ações de combate, Mastery ou todos os outros rituais. `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`; universo integral do provider aberto. Configuração/datapacks efetivos, execução do jogo e sucesso transacional permanecem eixos separados.

A [ficha individual](rituals/archmage-shard.md) usa o [manifesto SHA-exato](EXACT-4.0.3-ARCHMAGE-RITUAL.json). A matriz anterior de [esquema/ABI](EXACT-4.0.3-RITUAL-SCHEMA-SPELL-ABI-20261029.md) prova a identidade dos onze recursos; este documento amplia o rito Archmage com fatos de execução e não promove os demais dez por analogia. A seção manual abaixo não atribui automaticamente seu contrato ao automator; a automação tem consumidores e inventários próprios e exige sua evidência específica.

## Autoridade, identidade e reexecução

- Provider `alshanex_familiars`, nome Alshanex's Familiars; metadata do JAR: versão **`1.21.1_v4.0.3`**, Minecraft 1.21.1, NeoForge, Java 21; licença **All Rights Reserved**.
- Artefato físico histórico/publisher: `alshanex_familiars-1.21.1_v4.0.3.jar`, CurseForge projeto/file **1171602/8675568**, **21.848.062 bytes**; SHA-1 **`e5051c2385a426d05bf203ba8081a23d891f6686`**, SHA-256 **`ed006afb15a68bee9685ddac45c0f8bfc2a16e3a8a05004c6e1a3373f5f9a284`**. Reconsultar o publisher confirma o fingerprint documentado, sem equivaler a abrir um perfil instalado atual.
- Receita examinada: `data/alshanex_familiars/recipe/ritual_recipes/archmage_shard.json`, SHA-256 **`af31603a46719a7b09e4a4f21844fb2fa0f72ea999880f5e4d6102310b6ef46d`**; type `alshanex_familiars:ritual_recipe`; resultado `alshanex_familiars:archmage_shard`.
- As evidências retêm nomes, hashes, descritores, operandos/offsets limitados e paráfrases causais. Nenhum JAR, asset, fonte, JSON integral ou corpo completo de implementação de terceiros é publicado ou transplantado. A licença não transforma observação factual em autorização de reutilização.

Reexecução do contrato no JAR correspondente, com Java 21 disponível no ambiente:

```sh
python3 docs/qa/alshanex_403_archmage_ritual_contract.py \
  --jar /caminho/alshanex_familiars-1.21.1_v4.0.3.jar \
  --familiarslib /caminho/familiarslib-1.7.1.jar --verify
```

O verificador/CI e o lock JSON são autoridade para identidade e deriva do recorte. PASS estático não é teste físico nem permissão de um hook mutador.

## Recurso e autoridade de itens

O central é `alshanex_familiars:pet_soul`. Há quatro exigências periféricas distintas, **uma unidade de cada**, `consume=true`: `irons_spellbooks:legendary_ink`, `irons_spellbooks:arcane_essence`, `irons_spellbooks:arcane_rune` e `irons_spellbooks:magic_cloth`. A combinação de identificadores/contagens é fato de interoperabilidade; não se reproduz aqui a representação JSON. Resultado declarado: `alshanex_familiars:archmage_shard`; partícula declarada `minecraft:end_rod`.

Alshanex é dono da receita e do resultado; os quatro IDs periféricos são recursos Iron's. A autoridade de registry/tags/dados carregados permanece nos respectivos providers e no RecipeManager, não em uma cópia Black Arcana. Overrides de datapack e substituição de receita são uma alteração do estado efetivo, não uma razão para renomear ou multiplicar a identidade ritual. O procedimento inicia com a Familiar Soul disponível. A fonte de obtenção dessa alma fica fora do recorte. A automação é descrita na seção própria abaixo.

## Objetos binários do procedimento manual

Prefixo das classes: `net/alshanex/alshanex_familiars/`.

| Classe | SHA-256 do classfile | Papel |
|---|---|---|
| `block/RitualCorePedestal.class` | `a28605b944477d9c46b449ac560fe0be36adebca3e5f7bbe066713431419cd92` | Entrada de mão, troca de item, ticker e remoção do core |
| `block/entity/RitualCorePedestalEntity.class` | `1167d4c17cb840c567c93d89d43d2e9d3fadd049a52c52c8a3e150ada5cb5d36` | Estado, relógio, resultado, NBT e atualização |
| `util/rituals/RitualHelper.class` | `f54c779f990f45341280d30689b6b412040aa956c08b5231e829be20e53fc33f` | Geometria, seleção de receita e consumo periférico |
| `recipe_types/RitualRecipeType.class` | `c8e6523f9b7c24088bb1dd9459f0d2c3df5025cc8bd6864d8136b8d84df8faf8` | Central, multiset de ingredientes e quantidades |
| `block/entity/FamiliarStatueEntity.class` | `71a7c61f69a40d51adb8a359c784df84251a9219eccbf26165e7a0aa4a8bac66` | Base comum das quatro entidades periféricas aceitas |

## Entrada, mão e seleção de blocos

`RitualCorePedestal.useItemOn(ItemStack,BlockState,Level,BlockPos,Player,InteractionHand,BlockHitResult)` só altera o estado no ramo **servidor** (`Level.isClientSide @1`, desvio@4) e quando o BlockEntity do local tem o tipo esperado. Consulta o heldItem do core e o stack da mão. Se a mão está vazia ou contém uma unidade, devolve o item anterior à mão (`@55–79`); com stack maior, usa `dropItem` para o anterior (`@82–87`). Depois limpa o heldItem (`@92–95`), copia a entrada original, força count 1, coloca essa cópia e diminui a entrada original em 1 (`@100–129`). Atualiza o bloco com flags 2 (`@137–138`) e retorna sidedSuccess (`@142–145`).

As classes manuais `ArchmageStatue`, `HunterStatue`, `DruidStatue` e `ClericStatue` têm a mesma sequência de interação observada (`useItemOn @0–148`). Esse caminho não contém exceção própria de creative/instabuild, owner, sneak, cooldown ou ritual em progresso. Não tratar o acesso ao bloco como autorização individual Black Arcana. A mão/contexto e as restrições externas do host precisam continuar válidos no momento da mutação.

`FamiliarStatueEntity.setHeldItem(ItemStack)` guarda o argumento sem impor count 1; a interação manual, e não esse setter genérico, é quem limita a inserção normal a uma unidade. `RitualCorePedestalEntity.setHeldItem` grava o central, zera counter/isValidRitual/itemInRecipe (`@0–17`), recalcula se o central participa de alguma receita (`@21–40`) e chama `setChanged @44`. Trocar/retirar o central reinicia o progresso por esse caminho.

## Geometria cardinal e seleção de receita

Não há vínculo persistente entre core e estátuas no helper manual. `RitualHelper.getSurroundingPedestals(BlockPos,Level)` constrói somente **north(2), south(2), east(2), west(2)** do core, na mesma altura (`@0–35`), nessa ordem. Para cada posição aceita BlockEntity **`instanceof FamiliarStatueEntity`** (`@70–89`). Não é busca por raio, caixa, diagonal, estátua de um familiar específico, facing ou pedestal genérico Iron's.

`isValidRecipe(Level,BlockPos,ItemStack)` exige level/stack presentes, pelo menos quatro estátuas aceitas (`size @17`, comparação com 4 @22–23) e um matching recipe presente (`@31–34`). Como só existem quatro posições candidatas, requer as quatro. `getItemStacksFromPedestals` copia os stacks não vazios das estátuas (`@49–67`). Estátua vazia pode contar para a geometria, mas não fornece ingrediente.

`findMatchingRecipe` monta `RitualRecipeType.Input`, consulta `RecipeRegistry.RITUAL_RECIPE_TYPE` no RecipeManager, filtra por `matches` e usa **findFirst** (`@34–87`). Não seleciona pelo nome Archmage nem por ownership do jogador. Havendo dados externos com receitas sobrepostas, a ordem efetiva do RecipeManager faz parte do contrato; a ficha não inventa prioridade entre IDs.

`RitualRecipeType.matches(Input,Level)`:

- testa o central com `Ingredient.test @8`, rejeitando a falha (`@11–15`);
- copia os periféricos não vazios, soma suas contagens e exige **igualdade** com a soma das contagens da receita (`@80–137`), não apenas “pelo menos quatro itens”;
- percorre requisitos e cópias, usa `Ingredient.test`, retira `min(restante,stackCount)` dessas cópias e rejeita se restar quantidade (`@138–288`). É matching de multiset, não ordem fixa norte/sul/leste/oeste para cada ingrediente.

Para o recurso Archmage, total exigido 4 e quatro requisitos distintos de 1 determinam uma unidade de cada no estado correspondente. `consume` não dispensa o requisito no matching; sua decisão é aplicada depois no consumo. Não generalizar a correção do custo desta receita aos outros dez rituais ou a receitas modificadas.

## Ticker, pausa e duração

`RitualCorePedestal.getTicker` retorna sem ticker no cliente (`isClientSide @1–4`); no servidor vincula `BlockEntityRegistry.RITUAL_CORE` ao callback que chama `RitualCorePedestalEntity.tick(Level,BlockPos,BlockState)` (`@10–26`, lambda@4). A própria rotina `tick` também retorna no cliente (`@1–7`).

Defaults do core: heldItem EMPTY, itemInRecipe false, isValidRitual false, counter 0. No tick, central ainda elegível e não vazio levam a **nova validação de receita** (`@9–41`). Se o central ficou vazio/inapto, zera validade e counter (`@47–54`). Se apenas os periféricos deixarem de formar receita, isValidRitual fica false e o ramo de progresso é pulado: **o counter é preservado, não reiniciado**, até o central mudar ou uma rota explícita o zerar.

Com ritual válido e counter<100, incrementa em 1 (`@65–80`); em múltiplos de 10 faz as consultas/partículas (`@84–129`). Ao atingir counter>=100, chama `completeRitual` (`@133–145`). Portanto 100 é o limiar de ticks válidos do contador, **não promessa de 100 ticks consecutivos de parede** com chunk parado, montagem alterada, lag ou estado recarregado. Partícula não é um token servidor de resultado aceito.

Não há custo próprio de mana, XP, dano, nível de magia, cooldown por jogador, chance de sucesso, hora/clima/moon gate, linha de visão ou alvo vivo nesses métodos manuais. Esses eixos são **N/A nesta rota própria**, não zero garantido em qualquer addon/automação/host.

## Settlement e limites de transação

`RitualCorePedestalEntity.completeRitual(Level,BlockPos,BlockState)` reconsulta o item de resultado (`getResultForRecipe @6`), solicita blastwave de apresentação (`MagicManager.spawnParticles @65`), chama `clearItemsFromPedestals @70`, cria **new ItemStack(resultItem)** e grava no core (`@80–89`), atualiza o bloco (`@105`) e zera counter/itemInRecipe/isValidRitual (`@108–120`). O central é substituído pelo resultado; não existe débito adicional Black Arcana.

`getResultForRecipe` converte o ItemStack da receita em **Item** e usa `ItemStack.EMPTY.getItem()` como fallback (`@37–46`), não null. Assim, a checagem `ifnull @13` em completeRitual **não é teste de rejeição de AIR/resultado vazio**. O gate de matching anterior deve ser distinguido desse teste; não supor rollback ou reserva transacional por causa do nome do método. Na rota manual, o construtor novo não transporta automaticamente count/components arbitrários do result stack da receita. O recurso Archmage declara somente o ID da shard, e a saída manual é uma unidade.

`clearItemsFromPedestals(Level,BlockPos)` consulta novamente core/receita (`@2–42`), obtém estátuas não vazias e percorre requisitos. `consume=false` pula o débito (`@143–149`). Para consume=true, exige Ingredient.test e stackCount>=count (`@192–213`), então chama **setHeldItem(EMPTY)** (`@225–228`), atualiza o bloco (`@249`) e remove aquela estátua da lista de candidatos (`@254`), usando uma por requisito. Não executa shrink(count) no stack vivo. Isso é compatível com a montagem manual exata de Archmage (quatro unidades distintas), mas é distinto do algoritmo de matching em cópias e não promete suporte a toda divisão/empilhamento que um setter/automação/receita externa possa produzir.

São operações ordenadas no thread do servidor, não um contrato de commit/rollback, efeito exatamente uma vez ou event hook de perk. Não duplicar consumo, shard, partículas ou progressão a partir do tick, da atualização NBT, do setter ou de cada pedestal. Qualquer adapter precisa conhecer o estado final nativo; não basta ver o contador 100 ou uma animação.

## Salvamento, remoção e sincronização

Core `writeNBT` guarda heldItem, itemInRecipe, isValidRitual e counter (`@11–69`); `readNBT` restaura os mesmos (`@1–50`). Estatutos e contador serializados não provam duração persistida exatamente em todos os save/unload/restarts. O corpo de tick não chama diretamente setChanged a cada incremento; não inferir a política de gravação efetiva do host a partir da existência dos campos.

`setChanged()` próprio chama `BlockEntity.setChanged @1` e, se level não-null, `sendBlockUpdated(...,2) @28`. `getUpdatePacket/getUpdateTag` integram a sincronização nativa de BlockEntity. `RitualCorePedestal.onRemove` só pede `drops @32` quando o bloco mudou, depois delega a Iron's PedestalBlock.onRemove; `drops()` encaminha o heldItem a `Containers.dropContents @28`. A base FamiliarStatueEntity também possui heldItem/NBT/drops/setChanged. Nenhum desses callsites sozinho prova cleanup sem duplicação sob destruição cancelada, troca de blockstate, unload ou proteção de terceiros.

O estado manual observado não possui UUID de caster/proprietário nem um ledger de ações aceitas por jogador. Não atribuir a shard ou Mastery automaticamente ao último jogador próximo ou ao responsável pela última interação. Drops/obtenção, ritual, uso da shard e comportamento do familiar são autoridades e fases distintas.

## Fronteira de integração e QA pendente

- **API não é seam homologada:** setters de heldItem, RecipeManager, dados consume/count e o contador são implementação nativa; nenhum mutador de custo/tempo/chance/resultado foi certificado. RPG Skill Tree não passa a executar ou liquidar o ritual.
- **Estado final mutável:** inserir/trocar item, retirar central/periférico, quebrar core/estátua e recarregar receitas devem continuar sujeitos aos gates reais do provider/host. WorldEffectPolicy Black Arcana não intercepta automaticamente drops, substituição de inventário ou automator de outro mod.
- **QA física `NOT_TESTED`:** quatro posições corretas/erradas, vazios/contagens excedentes, permutação dos quatro ingredientes, central trocado, pausa e retomada de periféricos, creative/offhand, save/unload/restart próximo do limiar, destruição cancelada e execução com múltiplos jogadores. Medir os stacks antes/depois, a contagem final da shard, o core/estátuas e os callbacks de atualização; nenhum resultado desse plano foi executado nesta auditoria.
- **Recorte do certificado:** shard é o resultado ritual. O uso posterior do shard tem referências no final deste relatório. A ficha certifica o craft, incluindo o fluxo de inventário do Automator, e mantém a obtenção da Familiar Soul e o ciclo de vida do familiar fora do recorte. O universo completo Alshanex continua aberto; hooks mutadores e QA não são promovidos por um selo de bytecode.

## Automação

`RitualAutomatorBlockEntity.tick` separa a atualização das transferências da rotina de trabalho do servidor. Usa cooldown interno de 10 com retorno durante a contagem (`@13–34`, um ciclo de consulta a cada 11 ticks ativos após o primeiro). `findCore` procura primeiro pelo menor offset na ordem X, Y, Z dentro da caixa X/Z −10 a +10 e Y −5 a +5. Armazena a primeira posição ocupada por `RitualCorePedestalEntity`. O inventário de entrada e saída é a capability `ItemHandler.BLOCK` no bloco imediatamente abaixo (`tick @119–141`).

A seleção compara `RecipeHolder.id` com `selectedRecipeId` em `lambda$tick$0`. Para Archmage o ID completo é `alshanex_familiars:ritual_recipes/archmage_shard`, e o item de saída é `alshanex_familiars:archmage_shard`. A seleção governa limpeza, abastecimento e recolhimento. A execução do craft continua em `RitualCorePedestalEntity.tick`, com reconhecimento da receita pelos ingredientes atuais. Alterar o ID selecionado não constitui um contrato de cancelamento do núcleo.

- `performCleanup` envia stacks incompatíveis de volta ao inventário. `performSupply` usa o ingrediente central e os requisitos periféricos da receita. `extractItemForIngredient @39` usa `IItemHandler.extractItem`, e o abastecimento agenda a entrega. `isTargeted` evita nova entrega para posição já atendida por uma transferência de ida.
- `spawnFlyingItem @11` inicia um voo de **20 ticks de processamento**. `processFlyingItems` avança o registro `FlyingItem`; quando chega, o servidor chama `completeFlight`. O destino é preenchido se ainda for a entidade de bloco esperada e estiver vazio. Um destino ocupado ou removido devolve a stack ao armazenamento ou solicita drop.
- `performCollection @20–48` compara item e components, limpa o núcleo e agenda a transferência da cópia da saída. `returnToStorageOrDrop @37` tenta inserção efetiva. Sem capability ou com resto, solicita drop na posição do Automator com Y+1 (`@79/116`). O efeito final depende do inventário e do mundo.
- `saveAdditional` e `loadAdditional` guardam a receita selecionada e a lista de `FlyingItem` em NBT. Em cada registro, stack, posições de origem/destino, ticks restantes/totais e direção são salvos. Isso sustenta a análise de estado em trânsito e deixa a recuperação após restart, quebra ou armazenamentos cheios para QA físico.

O Automator não fornece atribuição de Mastery por jogador. O contrato de autorização de mudança da seleção e a operação com modpacks de proteção precisam de validação própria antes de qualquer ponte mutadora.

## Consumidor do shard

`ItemRegistry.ARCHMAGE_RUNE` usa o literal de registro `archmage_shard` e o construtor de `ArchmageShard`. `RecipeRegistry` registra tipo e serializer `ritual_recipe`. No uso posterior, `FamiliarsLib 1.7.1` (CurseForge **1316458/8059464**, SHA-1 `7fa3f3116e35c12456425ae195924ced33fcc2eb`) reduz a stack em uma unidade em `AbstractRuneItem.useOn @25` e chama o override `@33`. Em `ArchmageShard.spawnFamiliar`, o tipo é `ARCHMAGE_PET`, com flag de impostor falsa, coordenadas no centro do bloco clicado mais (0,1,0) e yaw igual ao negativo de `Player.getYRot()` (`@46–50`). `Level.addFreshEntity @56` devolve um booleano descartado pelo override. A atribuição de propriedade, o comportamento posterior e a aceitação da entidade pelo host continuam fora do certificado do ritual.
