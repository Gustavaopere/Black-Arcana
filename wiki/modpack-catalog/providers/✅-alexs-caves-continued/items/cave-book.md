# Cave Book — `alexscaves:cave_book`

**Catálogo** ✅ Contrato técnico estático do item de consulta, da abertura da interface, da leitura do progresso, dos pedidos de critério e estatística e da receita publisher. Hook `NOT_VERIFIED`, QA física `NOT_TESTED`, perk `NOT_CERTIFIED` e `NO_MUTATION`.

## 1. Identidade e descrição funcional

O registro `alexscaves:cave_book` usa `com.github.alexmodguy.alexscaves.server.item.CaveBookItem`, que herda `Item`. JAR publisher `alexscaves-1.0.10-neoforge+1.21.1.jar` (Minecraft 1.21.1, NeoForge, Java 21), 75.279.314 bytes, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. A modlist sibling documenta a versão 1.0.10. A paridade binária com a instalação continua pendente.

A classe tem SHA-256 `84177c0ff1fdb42d766262624f877874c7c6db22a16036faf4dd6fe0540fcacf`, zero campos próprios e três métodos (`<init>`, `use` e `appendHoverText`). O construtor solicita `stacksTo(1)` e `Rarity.UNCOMMON`. O registro estático usa `ACItemRegistry.CAVE_BOOK` e `lambda$static$3()Item` (Code SHA-256 `be573644231006f03d2c5b21d6f8184ad86d1b1686ac563df66c68cf3c130113`). A aceitação pelo registro em execução continua pendente.

## 2. Ativação, condições e retorno

`use(Level,Player,InteractionHand)` recupera a stack da mão usada (68 bytes de Code, SHA-256 `afa18cf3478e81ccec190b5a0da07a59c9fbfe6066df6af7d3871a364415ef95`). Para `ServerPlayer`, solicita `CriteriaTriggers.CONSUME_ITEM.trigger` com a stack e `awardStat(Stats.ITEM_USED)` com o item. Em seguida solicita `Player.swing`. No cliente, passa a stack a `AlexsCaves.PROXY.openBookGUI`. O método retorna `ACCompat.usePass(stack)` em todos os ramos, sem decremento da stack ou desgaste de durabilidade. A concessão de avanço e estatística depende da engine e do servidor.

`ClientProxy.openBookGUI` chama `Minecraft.setScreen(new CaveBookScreen())` e deixa o argumento `ItemStack` sem uso. Em `CommonProxy`, `openBookGUI` retorna imediatamente. A tela lê o progresso do jogador local e inicia em `alexscaves:books/root.json`. `readBookEntry` solicita o recurso ao `ResourceManager`, abre o leitor e chama `BookEntry.deserialize`. Um recurso ausente produz retorno nulo.

## 3. Efeitos, fórmulas e parâmetros

- Em `en_us`, o item aparece como “Cave Compendium”. `appendHoverText` usa a chave `item.alexscaves.cave_book.desc` e a cor `GRAY`, com o texto inglês “By Dr. Prof. Alexander Caverns, PhD.” Renderização, som e temporização de virada de página pertencem ao cliente.
- A stack tem limite 1 e raridade `UNCOMMON`. O item usa a mão indicada pelo `InteractionHand`. Alvo externo, dano, cura, efeitos de status, projéteis, área, duração de uso, cooldown, mana, XP e escalonamento são `N/A` no fluxo local.
- A receita publisher `minecraft:crafting_shapeless` usa um `minecraft:book`, um `alexscaves:cave_tablet` e uma entrada da tag `#alexscaves:nuggets/gold` para gerar um `alexscaves:cave_book`. O campo `result.count` é omitido e recebe o padrão 1 do codec de referência. Receitas e tags efetivas dependem do datapack carregado. [Receita e hash publisher](../EXACT-CAVE-BOOK-CAUSAL-1.0.10.md#recursos-nativos-declarativos)
- A tag publisher inclui `minecraft:gold_nugget` e a referência opcional `#c:nuggets/gold`. `data/alexscaves/tags/item/nuggets/gold.json` · SHA-256 `db047553ccfeb39752feff34cf226aee9025443c8dfbad935a2bd2c3ea50670b`.
- O advancement publisher tem parent `alexscaves:alexscaves/cave_tablet` e critério `minecraft:inventory_changed` para obtenção do `alexscaves:cave_book`. O pedido de `CONSUME_ITEM` pertence ao fluxo de uso da seção 2.

## 4. Grafo técnico e limites de autoridade

`ACItemRegistry.lambda$static$3` → `CaveBookItem.<init>` → `CaveBookItem.use` → `ServerPlayer` (critério e estatística) ou `AlexsCaves.PROXY.openBookGUI` → `ClientProxy` → `CaveBookScreen` → `BookEntry`, `CaveBookProgress` e recursos de páginas. `BookEntry.getVisibility` lê `requiredProgress` e produz um estado de apresentação no cliente. Retorna 0 sem requisito ou com progresso já desbloqueado, 2 para `SECRETS` bloqueado e 1 para os demais requisitos bloqueados.

O diretório `assets/alexscaves/books/` do JAR publisher contém **68 definições JSON de páginas**. O selo registra o caminho e o SHA-256 de cada definição. [Censo e reprodução](../EXACT-BURROWING-CAVE-ITEMS-CATALOG-1.0.10.md)

| Grupo | Definições JSON |
|---|---:|
| `root.json` | 1 |
| `abyssal_chasm` | 13 |
| `candy_cavity` | 13 |
| `forlorn_hollows` | 10 |
| `magnetic_caves` | 9 |
| `primordial_caves` | 12 |
| `toxic_caves` | 10 |

`CaveBookProgress` lê de `CitadelEntityData` o NBT `AlexsCavesBookProgress` e a lista `Pages`, com as chaves `Category` e `SubCategory`. Os seis valores de subcategoria são `EMPTY`, `GENERAL`, `RESOURCES`, `MOBS`, `UTILITIES` e `SECRETS`. Quando a entrada de progresso está ausente, `getCaveBookProgress` cria o objeto com NBT vazio. O estado pertence ao jogador. No fluxo de gravação, `saveCaveBookProgress` solicita `CitadelTagUpdate` por `PropertiesMessage` para todos os clientes quando executado no servidor, ou para o servidor quando executado no cliente. Persistência, validação no receptor e proteção contra replay continuam pendentes.

O fluxo de pesquisa pertence ao `CaveInfoItem` para `alexscaves:cave_codex`. O Codex chama `unlockNextFor` e solicita `saveCaveBookProgress` no ramo servidor. Quando a etapa avança, solicita uma unidade do Codex para jogadores fora do modo criativo. `onlyOneResearchNeeded` altera as etapas dessa pesquisa.

## 5. Interoperabilidade e segurança

Potenciais dados relevantes para atributos, Mastery e perks: categorias desbloqueadas, etapa de pesquisa e elegibilidade de páginas; esses dados não criam um ponto mutador confiável por si. Não usar `ClientProxy`, clique no livro, tooltip, `CONSUME_ITEM` nominal nem `PropertiesMessage` como grant autoritativo. Não duplicar o caminho do Cave Codex. Black Arcana mantém seu runtime e seus recursos; RPG Skill Tree pode apenas fornecer progressão por boundary seguro. **Nenhum hook mutador seguro foi homologado; `NO_MUTATION`/fail-closed.**

## 6. Evidências e pendências

A descoberta histórica do job `136641421513` (run `44838694224`) capturou 23 classfiles candidatos e três recursos de nome `cave_book`. Artefato `14679244215`, ZIP SHA-256 `25ec78c0d3caa017d6d61d6ba8c91ab0c35816d14082285d7367e54c7669155d`. [Relatório causal](../EXACT-CAVE-BOOK-CAUSAL-1.0.10.md) · [Manifesto SHA-exato](../EXACT-CAVE-BOOK-DISCOVERY-1.0.10.json) · [Auditor de classes](../../../../../docs/qa/alexscaves_1010_cave_book_probe.py) · [Checks estáticos](../../../../../docs/qa/alexscaves_1010_cave_book_static_checks.py)

Acesso em multiplayer, concessão efetiva de progresso, receptor Citadel e validação cliente-servidor, persistência após restart, renderização no cliente instalado, hooks e comportamento com configurações e datapacks alterados continuam pendentes. O universo integral do provider permanece aberto.
