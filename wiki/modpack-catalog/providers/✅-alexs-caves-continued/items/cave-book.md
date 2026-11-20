# Cave Book — `alexscaves:cave_book`

**Estado:** ⚠️ **contrato técnico estático parcial**, embora a identidade e o corpo próprio do item estejam auditados. Hooks mutadores: `NOT_VERIFIED`; QA física: `NOT_TESTED`; provider integral: `OPEN`; operação autorizada: `NO_MUTATION`. **Não é cast mágico separado.**

## 1. Identidade e descrição funcional

Item de consulta que solicita abertura da interface *Cave Book* no cliente e sinaliza uso do item ao servidor. Descrição redigida da análise do binário, **não texto oficial**. Mod ID `alexscaves`; item `alexscaves:cave_book`; classe `com.github.alexmodguy.alexscaves.server.item.CaveBookItem`, herda `Item`. JAR publisher `alexscaves-1.0.10-neoforge+1.21.1.jar` (Minecraft 1.21.1, NeoForge, Java 21), 75.279.314 bytes, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. Na modlist sibling a versão é 1.0.10, mas não foi feito novo dump da pasta instalada.

Classe física SHA-256 `84177c0ff1fdb42d766262624f877874c7c6db22a16036faf4dd6fe0540fcacf`; zero campos próprios; três métodos: `<init>`, `use`, `appendHoverText`. Construtor solicita `stacksTo(1)` e `Rarity.UNCOMMON`. Registro estático por `ACItemRegistry.CAVE_BOOK` / `lambda$static$3()Item` (Code SHA-256 `be573644231006f03d2c5b21d6f8184ad86d1b1686ac563df66c68cf3c130113`); aceitação no registry runtime NÃO VERIFICADA.

## 2. Ativação, condições e retorno

`use(Level,Player,InteractionHand)` (68 bytes de Code, SHA-256 `afa18cf3478e81ccec190b5a0da07a59c9fbfe6066df6af7d3871a364415ef95`): recupera a stack da mão. Se `ServerPlayer`, solicita `CriteriaTriggers.CONSUME_ITEM.trigger` e `awardStat(Stats.ITEM_USED)`. Depois solicita `Player.swing`; **somente no cliente**, passa a stack a `AlexsCaves.PROXY.openBookGUI`. Retorna `ACCompat.usePass(stack)` em todos os ramos do corpo. **Não há decremento de stack em `use`**, apesar do nome `CONSUME_ITEM` do critério; resultados reais de avanço/stat seguem as regras da engine/servidor.

No proxy de cliente, o método `ClientProxy.openBookGUI` faz `Minecraft.setScreen(new CaveBookScreen())`; não lê o argumento `ItemStack` no corpo local. Em `CommonProxy`, `openBookGUI` retorna sem efeito. A tela inicia em `books/root.json`, com namespace `alexscaves` e recursos do gerenciador local de assets. Isso comprova o **pedido de interface**, não a disponibilidade final dos assets nem concessão de conhecimento.

## 3. Efeitos, fórmulas e parâmetros

- **Principal:** pedido de abrir o livro no cliente. **Secundários:** pedido de swing e de estatística/criterion no servidor; tooltip via chave de tradução `item.alexscaves.cave_book.desc`, cor `GRAY`. Aceitação final dos disparos ainda NÃO VERIFICADA.
- **Stack máxima:** 1; **raridade solicitada:** `UNCOMMON`. A mão utilizada é a do `InteractionHand` recebido, sem target de outra entidade no corpo do item.
- **Dano/tipo, cura, status, projectile, AOE ofensiva, alcance de combate, duration, cooldown, mana, XP e escalonamento:** `N/A` **para o corpo local do CaveBookItem**, sem afirmar inexistência de outros sistemas consumidores; o objeto é utilitário de informação. Renderização, som e temporização de virada de página pertencem ao cliente, sem dano ou custo de cast comprovado.
- **Receita publisher:** `minecraft:crafting_shapeless` com `minecraft:book`, `alexscaves:cave_tablet` e tag `alexscaves:nuggets/gold`. Confirmação de receitas ativas e itens substitutos no datapack do modpack: NÃO VERIFICADA.
- **Advancement publisher:** parent `alexscaves:alexscaves/cave_tablet`, criterion `minecraft:inventory_changed` para obtenção do `alexscaves:cave_book`. Distinto do criterion `CONSUME_ITEM` usado em `use`.

## 4. Grafo técnico e limites de autoridade

`ACItemRegistry.lambda$static$3` → `CaveBookItem.<init>` → `CaveBookItem.use` → `ServerPlayer` (criterion/stat) **ou** `AlexsCaves.PROXY.openBookGUI` → `ClientProxy` → `CaveBookScreen` → `BookEntry`/`CaveBookProgress`/recursos de páginas. O manifesto registra os classfiles, transcrições e consumidores examinados. `BookEntry.getVisibility` usa `requiredProgress` para produzir estados 0 (visível), 1 (bloqueado) ou 2 (`SECRETS` bloqueado). Esse gate é **apresentação cliente**, não API de autorização de progresso.

`CaveBookProgress` tem mapa de categorias e seis subcategorias (`EMPTY`, `GENERAL`, `RESOURCES`, `MOBS`, `UTILITIES`, `SECRETS`), serializado como `AlexsCavesBookProgress` / lista `Pages` (chaves `Category` e `SubCategory`) por `CitadelEntityData`. `saveCaveBookProgress` solicita `CitadelTagUpdate` através de `PropertiesMessage` para all/server conforme o lado. A persistência real, validação de mensagens e proteção contra replay continuam NÃO VERIFICADAS. Não há persistência própria no `CaveBookItem` além da stack do item; o progresso do jogador pertence a outro objeto/serviço.

**Separação essencial:** `CaveInfoItem` para `alexscaves:cave_codex` é quem chama `unlockNextFor` e, no ramo servidor, `saveCaveBookProgress`. Aí há custo solicitado de 1 codex para não-criativo quando desbloqueio avança. **Não é efeito nem custo do Cave Book.** A opção `onlyOneResearchNeeded` altera as etapas desse consumidor, não a abertura do livro.

## 5. Interoperabilidade e segurança

Potenciais dados relevantes para atributos, Mastery e perks: categorias desbloqueadas, etapa de pesquisa e elegibilidade de páginas; esses dados não criam um ponto mutador confiável por si. Não usar `ClientProxy`, clique no livro, tooltip, `CONSUME_ITEM` nominal nem `PropertiesMessage` como grant autoritativo. Não duplicar o caminho do Cave Codex. Black Arcana mantém seu runtime e seus recursos; RPG Skill Tree pode apenas fornecer progressão por boundary seguro. **Nenhum hook mutador seguro foi homologado; `NO_MUTATION`/fail-closed.**

## 6. Evidências e pendências

A análise é reproduzível pelo [relatório causal](../EXACT-CAVE-BOOK-CAUSAL-1.0.10.md), [manifesto SHA-exato](../EXACT-CAVE-BOOK-DISCOVERY-1.0.10.json), [auditor de classes](../../../../../docs/qa/alexscaves_1010_cave_book_probe.py) e [checks estáticos](../../../../../docs/qa/alexscaves_1010_cave_book_static_checks.py). Job de descoberta `136641421513` (run `44838694224`) capturou 23 classfiles candidatos e três recursos de nome `cave_book`; artefato `14679244215`, ZIP SHA-256 `25ec78c0d3caa017d6d61d6ba8c91ab0c35816d14082285d7367e54c7669155d`.

Pendências: censo completo de páginas `books/`/datapacks, consumo/acesso em multiplayer, commit de progression real, recebedor Citadel e validação C2S, persistência/save+restart e renderização em cliente real, event hooks, tolerância a configs/recipes alterados. Sem garantia de alcance do universo; contrato estático **⚠️ PARCIAL**, QA **NOT_TESTED** e mutação **BLOQUEADA**.
