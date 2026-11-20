# Alex's Caves Continued 1.0.10 — CaveBookItem: proveniência e auditoria em andamento

**Estado:** 🟡 descoberta nativa / ⚠️ contrato individual parcial. `NO_MUTATION`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; `provider_universe_closed=false`; sem alterações de runtime. Não há cast mágico independente certificado.

## Identidade e base de autoridade

O sibling `Gustavaopere/neoforge-rpg-skilltree` mantém na modlist o mod `alexscaves` versão 1.0.10, item físico `alexscaves-1.0.10-neoforge+1.21.1.jar`, Minecraft 1.21.1/NeoForge/Java 21. O publisher tem tamanho 75.279.314 bytes, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570` e SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. Um novo dump físico do disco do jogador não foi testado.

A descoberta anterior [EXACT-BURROWING-CAVE-MAP-DISCOVERY-1.0.10](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-BURROWING-CAVE-MAP-DISCOVERY-1.0.10.md) localizou `CaveBookItem.class`, SHA-256 `84177c0ff1fdb42d766262624f877874c7c6db22a16036faf4dd6fe0540fcacf`, herança `Item`, três corpos próprios: `<init>()`, `use(Level,Player,InteractionHand)` e `appendHoverText(...)`. O método construtor utiliza `stacksTo(1)` e rarity UNCOMMON. O binding de registro de `alexscaves:cave_book` parte de `ACItemRegistry.CAVE_BOOK` via `lambda$static$3` (hash Code `be573644231006f03d2c5b21d6f8184ad86d1b1686ac563df66c68cf3c130113`). Trata-se de pedido de registro, não confirmação autônoma de registry em execução.

## Efeitos localmente observados, a confirmar no grafo

A inspeção prévia da janela de `use` mostra que a chamada em `ServerPlayer` dispara um *criterion* `CONSUME_ITEM` e solicita `Stats.ITEM_USED`; o método também solicita swing e chama `openBookGUI` na rota client-side. Retorna `PASS` no corpo observado. **O critério `CONSUME_ITEM` não demonstra que houve subtração de item da stack**. Não há `shrink()` no corpo local. UI aberta, dados desbloqueados, servidor aceitando progressão e efeitos de outros mods são escopos distintos; **não** atribuir concessão de progressão à simples abertura visual.

A tooltip cinza é apenas apresentação e não constitui efeito do servidor. Nenhum parâmetro de dano, projétil, mana, cooldown ou AOE é demonstrado nesse corpo local; os caminhos de GUI, progresso, persistência e o contrato completo do livro ainda estão abertos.

### Recursos publisher SHA-exatos já observados

- `assets/alexscaves/models/item/cave_book.json`: SHA-256 `803c11bd6eade5e560240e94858272fb8bc337dce55342ea27999b8bde600557`, modelo com parent `minecraft:item/generated`.
- `data/alexscaves/recipe/cave_book.json`: SHA-256 `550c905d6dac50a87c249c53c221379b7878edc2586e654c60d6013feef6e45a`, `minecraft:crafting_shapeless`, ingredientes declarados `minecraft:book`, `alexscaves:cave_tablet` e tag `alexscaves:nuggets/gold`, output `alexscaves:cave_book`. Condições de datapack, equivalência/expansão da tag e craft efetivamente disponível não foram testados.
- `data/alexscaves/advancement/alexscaves/cave_book.json`: SHA-256 `68fb42ba802827edf2db87a9fb82c09ae3c0747d7d1d2b6b70dc4f06cf2ee726`, parent `alexscaves:alexscaves/cave_tablet`, criterion `minecraft:inventory_changed` verificando o item `alexscaves:cave_book`. Isso **não** é o mesmo evento que o criterion `CONSUME_ITEM` disparado em `use`.

## Descoberta read-only proposta

O script `docs/qa/alexscaves_1010_cave_book_probe.py` valida o artefato SHA-exato, censo de 1555 classes e 8898 arquivos, identifica os classfiles com marcadores `CaveBookItem`, `openBookGUI`, `LecternBooks`, `cave_book`, `BookProgress` etc., e captura `javap -v -p -c -s` dos 26 candidatos prioritários. O relatório guarda **todos** os candidatos com hashes, e transcrições SHA-pinned dos capturados; o limite da coleta não é prova de que o grafo transitivo esteja fechado. O workflow de CI armazena as transcrições em artefato temporário, sem publicar JAR nem código-fonte de terceiros.

**Pendências de certificação:** corpo e chamadas exatas de `use`, constructor e tooltip, autoridade da GUI/proxy e dados de tela; todos os consumidores de progresso, eventos, recursos, tags, persistência e permissão; handler de networking quando houver; comportamento aceito do critério; hand/offhand, custo, multiplayer, save/reload, servidor dedicado; boundary real de perks/Mastery. Sem hooks seguros: `NO_MUTATION`, sem `PERK-READY-CERTIFICATIONS` e sem promoção de Stage ou QA física.