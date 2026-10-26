# Ars Nouveau — Spell Books & Glyph Learning

State: `SOURCE-PINNED 5.13.1 / LEARNING FLOW VERIFIED`.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`.

## Spell-book tiers

The exact 5.13.1 item registry binds:

- `ars_nouveau:novice_spell_book` -> `SpellTier.ONE` (value 1)
- `ars_nouveau:apprentice_spell_book` -> `SpellTier.TWO` (value 2)
- `ars_nouveau:archmage_spell_book` -> `SpellTier.THREE` (value 3)
- `ars_nouveau:creative_spell_book` -> `SpellTier.CREATIVE` (value 99)

The normal progression surface is Tier I/II/III; Creative is a distinct provider tier for creative tooling.

Using a non-Creative `SpellBook` on the server updates the player's Ars mana capability so `bookTier` is at least the book's tier, and updates `glyphBonus` to at least the number of known glyphs, then syncs mana data to the client when changed.

## Learning a glyph

Each registered spell part exposes a provider Glyph item. `Glyph#use` is server-side authoritative for learning:

1. reject if the glyph is disabled by Ars config;
2. read the Ars player-data capability;
3. reject if already known or if it belongs to the default-starting glyph set;
4. call `unlockGlyph(spellPart)` on the Ars player capability;
5. sync player capability;
6. raise mana `glyphBonus` to the new known-glyph count when required and sync it;
7. consume one Glyph item in non-infinite-material mode;
8. report the learned glyph to the player.

Known glyphs are therefore persistent Ars player progression, not merely possession of an item or a client-side book state.

## Glyph crafting / XP

`GlyphRecipeProvider` generates the provider-native glyph recipes. The generated recipe XP requirement is based on the spell part's default tier:

- Tier 1 -> 27 XP
- Tier 2 -> 55 XP
- Tier 3 -> 160 XP

Each individual spell-part page is being linked to its exact generated ingredient recipe. This XP is Ars glyph-recipe progression; it is not RPG Skill Tree XP/Mastery unless a real bridge explicitly says so.

## Authority boundary

- Ars owns known-glyph state, spell-book tier and glyph-learning consumption.
- RPG Skill Tree may gate progression only through a real provider contract; it must not write Ars known-glyph capability by inference.
- Black Arcana must not auto-learn Ars glyphs because a thematically similar Black Arcana spell was unlocked.
- Registry namespace remains decisive for addon glyph ownership: Ars' guide/UI may display addon entries, but `ars_elemental:*`, `ars_controle:*`, `ars_zero:*`, etc. remain their own providers.

## Auditoria de engenharia — Spellbooks, Glyph Learning e progresso (2026-10-26; PR independente)

**⚠️ Documento source-pinned ampliado, certificação no manifesto ainda pendente.** JAR físico `ars_nouveau-1.21.1-5.13.1.jar`, mod ID `ars_nouveau`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`; source `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`. Auditoria binária dos 109 IDs identifica glyphs/rituais, mas **não valida métodos de `Glyph`, `SpellBook` ou capabilities**, nem receita física carregada. Fontes: [Glyph.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/items/Glyph.java), [SpellBook.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/items/SpellBook.java), [IPlayerCap.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/capability/IPlayerCap.java), [ANPlayerData.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/capability/ANPlayerData.java), [GlyphRecipeProvider.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java), [GlyphRecipe.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/crafting/recipes/GlyphRecipe.java), [ManaCap.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/capability/ManaCap.java), [SpellResolver.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellResolver.java).

| Eixo de progressão | Evidência real e restrições |
|---|---|
| **IDs/tier de books** | O registro dos books usa `ars_nouveau:novice_spell_book`, `ars_nouveau:apprentice_spell_book`, `ars_nouveau:archmage_spell_book`, `ars_nouveau:creative_spell_book`, com `SpellTier.ONE/TWO/THREE/CREATIVE`. `SpellBook.use` atualiza `iMana.setBookTier(this.tier.value)` se o tier usado for superior ao atual e o book **não** for Creative; atualiza `glyphBonus` até a contagem `cap.getKnownGlyphs().size()` e envia `syncToClient` se mudou. O `SpellTier.CREATIVE` não promove tier via esse branch; não igualar Creative a progressão normal nem a permissão de spells RPG. |
| **Servidor x cliente** | No `SpellBook.use`, o ramo de `ServerPlayer` atualiza mana e retorna `InteractionResultHolder.pass(stack)`. A chamada `caster.castOnServer(handIn,...)` está no **ramo do cliente**, enviando intenção ao servidor em vez de executar cast diretamente nesse branch; lógica completa de validação e custos está no `SpellResolver`. Não tratar clique na GUI ou book usado como conclusão de magia. |
| **Aprendizado via item** | `Glyph.use` retorna cedo no cliente; no servidor verifica `Config.isGlyphEnabled(spellPart.getRegistryName())`, procura `CapabilityRegistry.getPlayerDataCap(player)`, rejeita `knowsGlyph` e `GlyphRegistry.getDefaultStartingSpells().contains(spellPart)`. Somente se `playerDataCap.unlockGlyph(spellPart)` retorna true, executa `CapabilityRegistry.EventHandler.syncPlayerCap`, eventualmente aumenta `iMana.setGlyphBonus(cap.getKnownGlyphs().size())`, sincroniza e faz `getItemInHand(handIn).shrink(1)` quando `!hasInfiniteMaterials`. Consumir o item de glyph não equivale automaticamente a ganhar Mastery RPG. |
| **Caso capability nula** | O branch de sucesso em `Glyph.use` acessa `iMana.getGlyphBonus()` sem check explícito de null quando `playerIn instanceof ServerPlayer`; `SpellBook.use` também acessa `cap.getKnownGlyphs()` quando `iMana!=null`, sem guarda local de cap. Isso é **risco condicionado na inspeção da fonte**, não prova de NPE durante o gameplay padrão (capabilities são previstas no provider). |
| **Persistência e registry reload** | `ANPlayerData.serializeNBT` grava glyphs conhecidos por `getRegistryName().toString()` em `glyph0..glyphN` e `size`. `deserializeNBT` consulta `GlyphRegistry.getSpellPart(id)` e **não restaura entradas desconhecidas** (`part==null`); logo remoção de addon/namespace pode afetar a retenção daquele glyph em saves regravados. `ManaData` mantém `glyphBonus` e `book_tier` em attachment separado; a relação entre saldo antigo de glyphBonus e glyphs carregados precisa QA. |
| **Receita/XP** | `GlyphRecipeProvider.getExpFromTier(AbstractSpellPart)` usa `spellPart.defaultTier().value`: Tier1 `27`, Tier2 `55`, Tier3 `160`, demais `0`; `GlyphRecipe` armazena `output`, `inputs` e `exp`, com `RecipeRegistry.GLYPH_TYPE` e serializer próprios. Essa é **geração padrão do provider**: datapacks e recipes carregados podem alterar quantidade, ingredientes e XP real, e alguns addon glyphs são de namespace externo (não Ars). `Glyph.getCreatorModId` consulta o namespace do spellPart no `ModList`, não o nome visível na interface. |
| **Authority/gates** | A aquisição de glyphs é progresso do próprio Ars, não habilidade de Black Arcana. RPG Skill Tree só pode conceder gates, perks e Mastery por contratos reais, sem escrever diretamente `IPlayerCap`, `ManaCap` ou auto-consumir glyph items por correspondência de nome. `WorldEffectPolicy` do Black Arcana não intercepta UnlockGlyph nem GUI do Ars. `mutating_hook=NOT_VERIFIED`. |

**QA pendente:** learning de glyph de addon removido, data migration de `ANPlayerData`, evento de clique duplo e sync, null capability durante login/relog, permissões de book Creative, tier config e disponibilidade de datapack, bypass de recipes do Scribes Table, namespace de addons e comparação com Mastery RPG. `physical_qa=NOT_TESTED`. Sem promoção de Stage 06.05/09. A ficha permanece ⚠️ até manifesto reconciliado.
