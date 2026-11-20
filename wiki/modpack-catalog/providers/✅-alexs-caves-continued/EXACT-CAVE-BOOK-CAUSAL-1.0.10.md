# Alex's Caves Continued 1.0.10 — Cave Book: cadeia causal item → GUI → progresso

**Estado:** ⚠️ `PARTIAL_STATIC_CAUSAL` / `DISCOVERY_NOT_CERTIFIED`. Os corpos inspecionados pertencem ao **JAR publisher SHA-exato**; não constituem QA física, demonstração de configuração ativa ou autorização de hook. `NO_MUTATION`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `provider_universe_closed=false`. A raiz `CaveBookItem` é utilitário de informação/progressão, **não um novo feitiço/cast**.

## Artefato e escopo reproduzível

- Mod ID: `alexscaves`; versão `1.0.10` (Minecraft 1.21.1 / NeoForge / Java 21). Modlist sibling: `alexscaves-1.0.10-neoforge+1.21.1.jar`; última modlist consultada em `neoforge-rpg-skilltree/main@2b730debc77e60d94a2da9a3f3d8e889c71d2852`.
- Artefato publisher inspecionado: 75.279.314 bytes, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, 8.898 entradas, 1.555 classes.
- `CaveBookItem.class`: `com/github/alexmodguy/alexscaves/server/item/CaveBookItem`, SHA-256 `84177c0ff1fdb42d766262624f877874c7c6db22a16036faf4dd6fe0540fcacf`. `Item` direto; campos próprios: **zero**. Três métodos com Code: `<init>` (22 bytes, SHA do Code `b684f9568e1d4cd5ea0d4342f52a5ddd6403b1a57f309ecee16e1ac4c04fdee6`), `use` (68 bytes, `afa18cf3478e81ccec190b5a0da07a59c9fbfe6066df6af7d3871a364415ef95`), `appendHoverText` (19 bytes, `ef270f2394233336f8dfcc5084378b014cc6221dbcaf5d068680fe5f413ae765`).
- Captura: [script de descoberta](../../../../docs/qa/alexscaves_1010_cave_book_probe.py), [regressão local SHA-pinned](../../../../docs/qa/alexscaves_1010_cave_book_static_checks.py), [workflow](../../../../.github/workflows/alexscaves-1010-cave-book-probe.yml), [manifesto de hashes](EXACT-CAVE-BOOK-DISCOVERY-1.0.10.json). CI run `44838694224`, job `136641421513` obteve transcrições `javap -v -p -c -s` de **23 classes**; 23 candidatos encontrados na classe física. Artefato temporário `14679244215`, ZIP SHA-256 `25ec78c0d3caa017d6d61d6ba8c91ab0c35816d14082285d7367e54c7669155d`, expira em 04/12/2026. Hashes dos classfiles/transcrições preservados no manifesto.

## Item — identidade, ativação e efeitos aceitos

`ACItemRegistry.CAVE_BOOK`, registro estático `alexscaves:cave_book` através de `lambda$static$3()Item` (Code SHA-256 `be573644231006f03d2c5b21d6f8184ad86d1b1686ac563df66c68cf3c130113`), instancia `CaveBookItem`. O construtor configura `Item.Properties.stacksTo(1)` e `Rarity.UNCOMMON`; não há armazenamento próprio no item. A aceitação real do registro pelo loader depende de runtime não executado neste relatório.

`CaveBookItem.use(Level,Player,InteractionHand)`:

1. `@0–5` lê `player.getItemInHand(hand)`; não faz seleção adicional de alvo ou entidade.
2. `@7–42`: **somente quando o Player é `ServerPlayer`**, solicita `CriteriaTriggers.CONSUME_ITEM.trigger(serverPlayer,stack)` e `ServerPlayer.awardStat(Stats.ITEM_USED.get(this))`. O nome do critério não equivale a consumo de stack. Os efeitos efetivamente aceitos por advancement/statistics dependem da engine.
3. `@42–47` solicita `player.swing(hand)`; em `level.isClientSide==true` solicita `AlexsCaves.PROXY.openBookGUI(stack)` (`@47–62`). Em servidor não chama esse método pelo ramo de uso.
4. `@62–67` retorna `ACCompat.usePass(stack)` em todos os ramos locais; nenhum `ItemStack.shrink`, `hurtAndBreak`, dano, mundo alterado ou atribuição de mana é declarado em `use`. `PASS` é valor de retorno da interação local, **não sucesso de concessão de progresso**.

`appendHoverText` adiciona `Component.translatable("item.alexscaves.cave_book.desc")` com `ChatFormatting.GRAY` (`@0–18`), apenas apresentação; a tradução exibida depende do idioma ativo. A chamada local não contém custos, targeting de combate, AOE, tempo de canal, cooldown ou projéteis. A não aplicabilidade vale para **o corpo do item**, não para eventuais consumers externos.

## GUI e limiar de autoridade

- `CommonProxy.openBookGUI(ItemStack)` é `return` sem efeito próprio (`@0`); `ClientProxy.openBookGUI(ItemStack)` realiza `Minecraft.getInstance().setScreen(new CaveBookScreen())` (`@0–13`). O argumento `ItemStack` não é usado pelo corpo sobrescrito no ClientProxy; a tela é construída no cliente. **Abrir tela não executa autorização de progressão.**
- `CaveBookScreen()` delega a `CaveBookScreen("books/root.json")`; o construtor principal obtém `Minecraft.player`, constrói um snapshot `CaveBookProgress.getCaveBookProgress(localPlayer)` e inicializa o resource `alexscaves:books/root.json`. `getBookFileDirectory()` devolve `alexscaves:books/`; os recursos efetivamente presentes e o reload/fallback do ResourceManager devem ser examinados além dos três arquivos `cave_book` especificamente inventariados.
- `CaveBookScreen.readBookEntry(ResourceLocation)` usa `Minecraft.getResourceManager().getResource`, `Resource.openAsReader` e `BookEntry.deserialize(Reader)`; a ausência do resource resulta em retorno nulo neste corpo. Tratamento de entradas e experiência visual devem ser validados separadamente.
- `BookEntry.getVisibility(CaveBookScreen)` devolve `0` sem `requiredProgress` ou com progresso desbloqueado; devolve `2` quando o requisito é `SECRETS` bloqueado, e `1` quando outro requisito está bloqueado. São **estados de apresentação no cliente**, não provas de gates em servidor ou autorização da API. `CaveBookScreen.attemptChangePage(...)` é operação da UI e não salva progressão.

## Progresso, NBT e sincronização (consumidores distintos)

`CaveBookProgress.getCaveBookProgress(Player)` lê `CitadelEntityData.getOrCreateCitadelTag(player)`; interpreta a entrada `AlexsCavesBookProgress` se presente e, na ausência, constrói `CompoundTag` vazio. O construtor privado percorre lista `Pages`, cada elemento com string `Category` e inteiro `SubCategory`, e monta `Map<String, Subcategory> unlockedPages`. As categorias compiladas são `EMPTY`, `GENERAL`, `RESOURCES`, `MOBS`, `UTILITIES` e `SECRETS` (enum). `Subcategory.getByOrdinal(int)` aplica clamp entre `0` e `values().length-1`, o que exige atenção a NBT inválido/migração.

`saveCaveBookProgress(progress,player)` reserializa `Pages` em `AlexsCavesBookProgress`, chama `CitadelEntityData.setCitadelTag` e solicita mensagem `PropertiesMessage("CitadelTagUpdate", tag, playerId)` via `Citadel.sendMSGToAll` **se servidor**, ou `Citadel.sendMSGToServer` **se cliente** (`@0–70`). Autenticação do pacote, permissões do receptor, replay, sincronização de clients e persistência após logout/reload dependem de outros métodos da infraestrutura Citadel **NÃO VERIFICADOS**.

`unlockNextFor(biomeCategory)` verifica etapa anterior e `Subcategory.canUnlockNext`; se `ACServerConfig.onlyOneResearchNeeded==true`, seleciona `Subcategory.getLastUnlockableFor`, senão avança um ordinal. Retorna booleano e modifica `unlockedPages` **nesse objeto em memória**; não chama sozinho `saveCaveBookProgress`. Os métodos `isUnlockedFor` comparam ordem de categorias, e `getBiomeFromPage` separa a string no último `_`. Conteúdo concreto de páginas/biomas e aplicação de datapacks condicionais permanecem pendentes.

### Cave Codex não é Cave Book

A fábrica `ACItemRegistry.CAVE_CODEX` é `CaveInfoItem`, não `CaveBookItem`. No `CaveInfoItem.use` para a stack `CAVE_CODEX` e um cave biome válido, há `CaveBookProgress.getCaveBookProgress`, `unlockNextFor`, e **somente no ramo não-cliente** `saveCaveBookProgress` (`@48–82`). Quando a etapa é desbloqueada, solicita `shrink(1)` se `!player.isCreative()` e retorna `ACCompat.useConsume`; quando não há etapa, retorna PASS após mensagem de fim. O método pode atualizar o objeto de progresso em memória antes do `isClientSide` local; **não** presumir que uma chamada cliente persista concessão autorizada. É consumidor adjacente útil para o contrato do livro, mas tem **identidade e custo diferentes**. Seu próprio contrato individual continua pendente.

## Recursos nativos declarativos

| Recurso | SHA-256 | Evidência |
|---|---|---|
| `data/alexscaves/recipe/cave_book.json` | `550c905d6dac50a87c249c53c221379b7878edc2586e654c60d6013feef6e45a` | `crafting_shapeless` com `minecraft:book`, `alexscaves:cave_tablet`, tag `alexscaves:nuggets/gold`, output `alexscaves:cave_book` |
| `data/alexscaves/advancement/alexscaves/cave_book.json` | `68fb42ba802827edf2db87a9fb82c09ae3c0747d7d1d2b6b70dc4f06cf2ee726` | Parent `alexscaves:alexscaves/cave_tablet`; criterion `minecraft:inventory_changed` para `alexscaves:cave_book` |
| `assets/alexscaves/models/item/cave_book.json` | `803c11bd6eade5e560240e94858272fb8bc337dce55342ea27999b8bde600557` | Parent `minecraft:item/generated`; textura de apresentação |

O critério `minecraft:inventory_changed` na **definição de advancement** não é o `CONSUME_ITEM` emitido por `use`, e nenhum deles prova que a stack foi subtraída pelo item. Recipe runtime, recipes condicionalmente alteradas e expansão da tag de nuggets de ouro ainda NÃO VERIFICADAS.

## Consequências para integração e pendências de certificação

**Alvos conceituais de integração:** concessão de páginas, categoria de biome, last-unlocked subcategory e eligibility das páginas; dados de UI não são um ponto mutador seguro. Não reexecutar `unlockNextFor` de fora, não enviar `CitadelTagUpdate` não-autenticado, não conceder XP por abertura de GUI ou pelo nome de um critério. Para qualquer perk/Mastery, localizar evento real de server authority, evitar double processing e manter os dados próprios do Black Arcana separados do progress Citadel. **Sem API/hook seguro e verificado: `NO_MUTATION`.**

**Faltam:** universo de JSONs `assets/alexscaves/books/` e seus requisitos, consumidores além do censo lexical de 23 classes, classes Citadel de persistência/transporte e validators, comportamento em multiplayer, logs de network, sync e save-restart, configuração/datapacks do modpack, aceitação de critérios, GameTest/in-world, situações de swap/duplicação de stack. `STATIC_CONTRACT=PARTIAL` e fichas/índices não devem receber ✅ estático por esse relatório.
