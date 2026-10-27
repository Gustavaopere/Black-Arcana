# Ars Nouveau — livros, conhecimentos de glyph e crafting

**Estado:** ✅ `STATIC_TECHNICAL_CATALOG_ONLY`; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.

Fonte `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`, Ars Nouveau **5.13.1**. JAR de referência `ars_nouveau-1.21.1-5.13.1.jar`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`. Grau `PINNED_SOURCE_WITH_RELEASE_SHA_ONLY`: source imutável e proveniência da release; os109 IDs compilados de glyphs/rituais não provam a identidade ou os corpos binários deste sistema. Esta ficha agrega contratos, sem criar um glyph, Thread ou registry ID autônomo.

## Identidade e mapa de estado

Sistema agregado de `com.hollingsworth.arsnouveau.common.items.SpellBook/Glyph`, `common.capability.ANPlayerDataCap/ANPlayerData`, `api.registry.GlyphRegistry` e `common.block.tile.ScribesTile`. As identidades abaixo são itens e entradas de configuração reais; a ficha não inventa um registry ID único para o sistema. Os ingredientes específicos de cada glyph estão em [ACQUISITION](../ACQUISITION.md).

| Campo de certificação | Contrato estático e limite |
|---|---|
| Identidade e versão | Quatro itens SpellBook, Glyph ligado a AbstractSpellPart e set persistente de conhecimentos; source5.13.1, proveniência da release sem prova binária de todos os consumidores. |
| Comportamento e causalidade | Receita produz item Glyph; use servidor desbloqueia conhecimento e consome item; bookuse pode elevar caches de mana. Livro/recipe armazenados, conhecimento, starter e tier são estados separados. |
| Parâmetros e caps | Tiers1/2/3 eCreative99; SpellBook padrão contém SpellCaster(10) slots de spells. Glyph recipe XP27/55/160 pelo defaultTier, não pelo tier efetivo da config em runtime. |
| Targeting e resultado | Aprendizagem atua no Player que usa o item; crafting em ScribesTile usa blocos/itens próximos. Sem dano, projétil, alcance de spell ou duração de status próprios deste sistema. |
| Custos e aquisição | Glyph.use consome um item se sucesso e não infinite; não cobra XP diretamente. Scribes setRecipe cobra pontos de XP e ingredientes antes de produzir output em120ticks processados. Livros têm receitas próprias. |
| API e integração | unlockGlyph/setKnownGlyphs, book/caster componentes e config existem. Conhecimento ou validação na GUI não é um gate servidor universal; bridgeRPG deve provar fase, autorização, custos e persistência. |
| Evidência e validação | Sete campos documentados com source pinado e SHA da release; mutating_hook NOT_VERIFIED/physical_qa NOT_TESTED. Não homologa automaticamente aprendizagem, packet ou recipes no modpack real. |

## Livros, tier e slots armazenados

| Item Ars | Constante de SpellTier | Valor |
|---|---|---|
| ars_nouveau:novice_spell_book | ONE |1 |
| ars_nouveau:apprentice_spell_book | TWO |2 |
| ars_nouveau:archmage_spell_book | THREE |3 |
| ars_nouveau:creative_spell_book | CREATIVE |99 |

[ItemsRegistry][items], [nomes][names] e [SpellTier][tier] fixam essas associações. SpellTier tem mapa extensível e rejeita valores>99 no construtor; não impor um catálogo universal de apenas quatro tiers a addons.

O [construtor padrão SpellBook][book] põe SpellCaster(10) no componente SPELL_CASTER: são dez slots de **magias armazenadas**, não dez glyphs por receita nem dez perks. [SpellCaster][caster] guarda maxSlots no objeto; outros casters/componentes podem ter valores próprios. Uma regra de comprimento de composição é outro consumidor.

`SpellBook.use` em ServerPlayer eleva mana.bookTier até o tier do livro não Creative e glyphBonus até o tamanho do set conhecido, se maior, e sincroniza somente quando alterou. Retorna PASS nessa fase. No caminho cliente pede cast por `castOnServer`; elevar cache não confirma cast, pagamento ou aprendizado. Creative não grava99 no cache de mana por esse método. Livro na mão, maior tier registrado em mana e tier de cada glyph são eixos diferentes.

## Conhecimento, starter e configuração

[ANPlayerData][save] inicia um HashSet de glyphs vazio. [ANPlayerDataCap][knowledge] usa contains/add nesse set; unlockGlyph só escreve o attachment se add retorna true. setKnownGlyphs copia a coleção para HashSet. NBT guarda cada registry ID e tamanho; ao carregar, IDs parseados que não resolvem no GlyphRegistry são omitidos. Invalidade de texto de ID não é recuperada por tryParse nesse laço. [PLAYER_DATA][attachment] é serializable/copyOnDeath; sync por packet é etapa separada.

Starter não precisa estar no set persistido: [GlyphRegistry.getDefaultStartingSpells][registry] filtra as parts por [Config.isStarterEnabled][starter]. Cada part tem config servidor por namespace/path.toml; [AbstractSpellPart][part-config] declara enabled, cost, starter, per_spell_limit e glyph_tier (1…99). Default tier usado no datagen, config tier lido pelos validadores e starter efetivo não devem ser confundidos.

[Glyph.use][glyph], no servidor, faz: enabled → playercap → rejeitar known ou starter → unlockGlyph → sync → elevar glyphBonus quando necessário → consumir um item da mão se não infinite → mensagem. **Não há check de tier do livro, XP ou nível RPG nesse método.** [Config.isGlyphEnabled][config] resolve a part no registry e pode lançar erro para ID ausente. Possuir um Glyph item não é possuir conhecimento, e um unlock de Black Arcana não autoriza unlockGlyph do Ars.

## Receita, pontos de XP e crafting do glyph

[GlyphRecipeProvider][xp] deriva exp de `spellPart.defaultTier().value`: I27,II55,III160, default0 para outros valores. São **pontos de XP**, não níveis, mana, Source ou Mastery. Alterar glyph_tier na config não regenera os JSONs de receita já produzidos. [GlyphRecipe][recipe] contém output/inputs/exp; seu matches vanilla retorna false, e o consumidor real é a ScribesTile. O [codec][recipe-codec] serializa ingredientes, item e exp.

[ScribesTile.setRecipe][refund] compara o total de pontos do player, desconta exp se não creative e só depois busca o logicTile. Não é uma reserva transacional: logicTile ausente não é acompanhado de reembolso nesse ramo. Trocar/cancelar receita chama refundConsumed, que emite itens e XP em orbs do mundo, não uma devolução direcionada ao player original.

O [tick da mesa][scribes] no servidor tenta consumir uma unidade de item próximo a cada5worldticks em AABB de bloco inflada2; se não encontra e autoYoink ativo, a cada20worldticks tenta inventários na região ±6 horizontal/±2 vertical, uma extração. Com ingredientes completos inicia craftingTicks120; o contador é decrementado por tick processado e o servidor emite um Glyph output ao chegar a0. addFreshEntity não tem retorno conferido nesse trecho. [NBT da mesa][scribes-save] guarda recipe, consumed, craftingTicks, crafting e autoYoink; não tratar isso como timer absoluto em chunks descarregados.

[PacketSetScribeRecipe][scribe-packet] recebe posição e recipeID, busca GlyphRecipe e chama setRecipe; o método mostrado não verifica ali livro/tier/known ou distância. Essa é uma ausência limitada ao handler inspecionado, não um exploit reproduzido ou declaração sobre toda proteção do pack.

## Livros: receitas e componentes

[Novice][novice] é shapeless: book ou worn_notebook + iron_shovel + iron_pickaxe + iron_axe + iron_sword. O datagen declara critério has_journal para desbloqueio de recipe; isso não foi convertido em gate mágico de conhecimento.

[Upgrade Apprentice][book-recipes]: novice book, obsidian,3diamonds,2quartz_blocks e2blaze_rods. Archmage: apprentice book,3ender_pearls,2emeralds,totem_of_undying,nether_star e wilden_tribute. São defaults de receitas, sujeitos a datapack. [BookUpgradeRecipe.assemble][upgrade] aplica o componentsPatch de cada ingrediente SpellBook ao output; não ensina glyphs nem executa uma migração universal de estado do player. Não inventar custo fixo adicional de mana/XP para o upgrade.

## Gates de composição e fronteiras de segurança

[GuiSpellBook][gui] constrói validators de tier para editar e também de known glyph no paste; creative pode passar playerCap null ao known validator. [GlyphKnownValidator][known-gate] aceita starter separadamente; [GlyphMaxTierValidator][tier-gate] compara configTier ao tier informado. **Essas funções não demonstram um gate global servidor de aprendizagem/casting.**

[PacketUpdateCaster][write-packet] verifica ferramenta ICasterTool e recipe não null, então grava receita/nome/slot no componente; não chama os dois validadores nesse handler. [StandardSpellValidator][standard] tem estrutura e políticas de composição/caps, com flags diferentes entre crafting e cast. [SpellResolver.canCast][resolver] usa o validador fornecido pela API e depois enoughMana; o conjunto padrão mostrado não acrescenta automaticamente GlyphKnown/GlyphMaxTier. Addons podem trocar validators. Um gate de progressão RPG precisa ser comprovado no caminho servidor relevante, sem confiar apenas na GUI ou replay de unlock/custo.

## Autoridade e validade

Ars Nouveau mantém composição, recursos, itens, atributos e dados do jogador. RPG Skill Tree governa sua progressão por contrato real; Black Arcana mantém casting, Corruption, Strain, WorldEffectPolicy e causalidade próprios; Enshrouded mantém seus sistemas ambientais. APIs nativas existem, mas um adapter que preserve fase, caps, custos, persistência e deduplicação não foi validado. Não duplicar cast, cobrança, XP ou Mastery por tick, refresh, item equipado ou alteração de metadados.

Mudança de source, JAR, config, receitas, listeners ou codecs exige reauditoria. Config instalada, compatibilidade de addons, multiplayer, cliente/servidor, reload e persistência física permanecem pendentes. Não houve alteração de runtime, implementação de bridge ou promoção de Stage.

[items]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/registry/ItemsRegistry.java#L76-L79
[names]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/lib/LibItemNames.java#L13-L29
[tier]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellTier.java#L10-L39
[book]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/items/SpellBook.java#L60-L109
[caster]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellCaster.java#L25-L46
[glyph]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/items/Glyph.java#L43-L72
[knowledge]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/capability/ANPlayerDataCap.java#L27-L50
[save]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/capability/ANPlayerData.java#L15-L58
[attachment]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/registry/AttachmentsRegistry.java#L22-L33
[registry]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/registry/GlyphRegistry.java#L35-L58
[config]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/config/Config.java#L87-L97
[starter]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/config/Config.java#L179-L181
[part-config]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L226-L244
[xp]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L142-L157
[recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/crafting/recipes/GlyphRecipe.java#L82-L126
[recipe-codec]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/crafting/recipes/GlyphRecipe.java#L129-L158
[scribes]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/block/tile/ScribesTile.java#L70-L144
[refund]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/block/tile/ScribesTile.java#L146-L192
[scribes-save]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/block/tile/ScribesTile.java#L273-L305
[scribe-packet]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/network/PacketSetScribeRecipe.java#L33-L43
[gui]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/client/gui/book/GuiSpellBook.java#L112-L124
[known-gate]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/validation/GlyphKnownValidator.java#L16-L31
[tier-gate]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/validation/GlyphMaxTierValidator.java#L9-L33
[write-packet]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/network/PacketUpdateCaster.java#L49-L62
[standard]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/validation/StandardSpellValidator.java#L38-L66
[resolver]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellResolver.java#L74-L112
[novice]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/RecipeDatagen.java#L48-L52
[book-recipes]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/OneOffRecipesProvider.java#L39-L66
[upgrade]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/crafting/recipes/BookUpgradeRecipe.java#L17-L30

## Auditoria de engenharia — Spellbooks, Glyph Learning e progresso (checkpoint de 26/10/2026, reconciliado)

**No checkpoint de 26/10/2026, este documento source-pinned ainda não tinha certificação no manifesto.** A certificação documental atual está descrita acima; ela não homologa hooks ou QA físico. JAR físico `ars_nouveau-1.21.1-5.13.1.jar`, mod ID `ars_nouveau`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`; source `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`. Auditoria binária dos 109 IDs identifica glyphs/rituais, mas **não valida métodos de `Glyph`, `SpellBook` ou capabilities**, nem receita física carregada. Fontes: [Glyph.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/items/Glyph.java), [SpellBook.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/items/SpellBook.java), [IPlayerCap.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/capability/IPlayerCap.java), [ANPlayerData.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/capability/ANPlayerData.java), [GlyphRecipeProvider.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java), [GlyphRecipe.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/crafting/recipes/GlyphRecipe.java), [ManaCap.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/capability/ManaCap.java), [SpellResolver.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellResolver.java).

| Eixo de progressão | Evidência real e restrições |
|---|---|
| **IDs/tier de books** | O registro dos books usa `ars_nouveau:novice_spell_book`, `ars_nouveau:apprentice_spell_book`, `ars_nouveau:archmage_spell_book`, `ars_nouveau:creative_spell_book`, com `SpellTier.ONE/TWO/THREE/CREATIVE`. `SpellBook.use` atualiza `iMana.setBookTier(this.tier.value)` se o tier usado for superior ao atual e o book **não** for Creative; atualiza `glyphBonus` até a contagem `cap.getKnownGlyphs().size()` e envia `syncToClient` se mudou. O `SpellTier.CREATIVE` não promove tier via esse branch; não igualar Creative a progressão normal nem a permissão de spells RPG. |
| **Servidor (server-side) x cliente** | No `SpellBook.use`, o ramo de `ServerPlayer` atualiza mana e retorna `InteractionResultHolder.pass(stack)`. A chamada `caster.castOnServer(handIn,...)` está no **ramo do cliente**, enviando intenção ao servidor em vez de executar cast diretamente nesse branch; lógica completa de validação e custos está no `SpellResolver`. Não tratar clique na GUI ou book usado como conclusão de magia. |
| **Aprendizado via item** | `Glyph.use` retorna cedo no cliente; no servidor verifica `Config.isGlyphEnabled(spellPart.getRegistryName())`, procura `CapabilityRegistry.getPlayerDataCap(player)`, rejeita `knowsGlyph` e `GlyphRegistry.getDefaultStartingSpells().contains(spellPart)`. Somente se `playerDataCap.unlockGlyph(spellPart)` retorna true, executa `CapabilityRegistry.EventHandler.syncPlayerCap`, eventualmente aumenta `iMana.setGlyphBonus(cap.getKnownGlyphs().size())`, sincroniza e faz `getItemInHand(handIn).shrink(1)` quando `!hasInfiniteMaterials`. Consumir o item de glyph não equivale automaticamente a ganhar Mastery RPG. |
| **Caso capability nula** | O branch de sucesso em `Glyph.use` acessa `iMana.getGlyphBonus()` sem check explícito de null quando `playerIn instanceof ServerPlayer`; `SpellBook.use` também acessa `cap.getKnownGlyphs()` quando `iMana!=null`, sem guarda local de cap. Isso é **risco condicionado na inspeção da fonte**, não prova de NPE durante o gameplay padrão (capabilities são previstas no provider). |
| **Persistência e registry reload** | `ANPlayerData.serializeNBT` grava glyphs conhecidos por `getRegistryName().toString()` em `glyph0..glyphN` e `size`. `deserializeNBT` consulta `GlyphRegistry.getSpellPart(id)` e **não restaura entradas desconhecidas** (`part==null`); logo remoção de addon/namespace pode afetar a retenção daquele glyph em saves regravados. `ManaData` mantém `glyphBonus` e `book_tier` em attachment separado; a relação entre saldo antigo de glyphBonus e glyphs carregados precisa QA. |
| **Receita/XP** | `GlyphRecipeProvider.getExpFromTier(AbstractSpellPart)` usa `spellPart.defaultTier().value`: Tier1 `27`, Tier2 `55`, Tier3 `160`, demais `0`; `GlyphRecipe` armazena `output`, `inputs` e `exp`, com `RecipeRegistry.GLYPH_TYPE` e serializer próprios. Essa é **geração padrão do provider**: datapacks e recipes carregados podem alterar quantidade, ingredientes e XP real, e alguns addon glyphs são de namespace externo (não Ars). `Glyph.getCreatorModId` consulta o namespace do spellPart no `ModList`, não o nome visível na interface. |
| **Authority/gates** | A aquisição de glyphs é progresso do próprio Ars, não habilidade de Black Arcana. RPG Skill Tree só pode conceder gates, perks e Mastery por contratos reais, sem escrever diretamente `IPlayerCap`, `ManaCap` ou auto-consumir glyph items por correspondência de nome. `WorldEffectPolicy` do Black Arcana não intercepta UnlockGlyph nem GUI do Ars. `mutating_hook=NOT_VERIFIED`. |

**QA pendente:** learning de glyph de addon removido, data migration de `ANPlayerData`, evento de clique duplo e sync, null capability durante login/relog, permissões de book Creative, tier config e disponibilidade de datapack, bypass de recipes do Scribes Table, namespace de addons e comparação com Mastery RPG. `physical_qa=NOT_TESTED`. Sem promoção de Stage 06.05/09. O manifesto atual reconcilia a certificação documental; integração e QA física continuam pendentes.
