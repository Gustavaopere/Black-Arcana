# Ars Nouveau — Wololo

Status: `SOURCE-PINNED 5.13.1 / STATIC TECHNICAL CONTRACT / RUNTIME QA PENDING`

- Registry id: **`ars_nouveau:wololo`**, sem prefixo glyph; classe `com.hollingsworth.arsnouveau.common.spell.effect.EffectWololo` [wololo-id].
- Tier default **I herdado**, mana default **30**; a classe não declara escola nativa (`getSchools` herdado vazio), embora sua família editorial seja transformação cromática [defaults] [school].
- Compatíveis: Randomize e Sensitive; limite de configuração default Sensitive1 [wololo-config]. Isso não prova enforcement em todas as formas de cast ou configuração instalada.

## Seleção de cor e efeitos por ramo

[getDye][dye] usa primeiro referência de DyeItem no InventoryManager de TileCaster, ou offhand contendo DyeItem para os demais casters. A busca `findItem(...EXTRACT)` é consulta de referência, não extração [find]. Um dye real encontrado **precede Randomize**. Sem ele, Randomize escolhe um dos16 dyes da tabela; caso contrário escolhe a cor da paleta vanilla mais próxima por distância euclidiana à timeline Wololo [palette]. Não há probabilidade percentual por augment nem ponderação por quantidade de Randomize neste método.

[Entidades][wololo-entity]: ItemEntity com BASE_COLOR troca esse componente. Senão, se a stack é BlockItem, monta receita dye+bloco e, se o resultado também é BlockItem, substitui a stack preservando **a contagem original**, sem transferir componentes antigos explicitamente. Não usa a receita de oito blocos nesse ramo. Sheep recebe cor diretamente e tem prioridade sobre Sensitive. Sensitive ou ArmorStand altera os equipamentos que já possuam DYED_COLOR ou BASE_COLOR; não cria DYED_COLOR em qualquer armadura por tag. Outros Mob usam fake player com o dye na mainhand e `MobAccessor.callMobInteract`; depois limpa a mão do fake player. LivingEntity que não entra nesses ramos pode não mudar, mas ainda recebe o som final. Não há shrink/extract de dye explícito nesses ramos; o callback vanilla/modded de interação pode consumir/mutar a referência, portanto não prometer custo zero universal de item.

[Blocos][wololo-block]: `IWololoable` tem prioridade e recebe `setColor` com a **cor contínua da timeline** ou RGB aleatório; esse caminho não consulta getDye e não segue a prioridade de dye físico. A [interface pública][iwololoable] é uma API real de cor do objeto, não autoridade genérica de transformação. Signs usam `DyeItem.tryApplyToSign`. Outros blocos não-air tentam receita de dye+1bloco e, sem resultado BlockItem, dye cercado de8blocos. Copiam propriedades compatíveis via `newBlock.withPropertiesOf(hitBlock)` e chamam `setBlockAndUpdate`; se a block entity nova tiver a mesma classe da antiga, carregam `saveWithoutMetadata` para preservar seus dados. O retorno da colocação é ignorado: não tratar a sequência como transação comprovada de substituição/restauração.

## Cache, recursos e limites

`MAX_RECIPE_CACHE=16` cria FixedStack, mas [getDyedResult][recipes] **não popula cache no miss**: retorna diretamente a consulta do RecipeManager. Em hit chama `recipeCache.add(recipe)`, herdado, não `FixedStack.push`. O [cap do FixedStack][fixed-stack] só foi implementado em push. Portanto este recorte não prova cache efetivo limitado a16: com estado inicial vazio não se aquece pelo miss; entradas externas/hits podem acumular duplicatas por add. Não usar16 como work budget da pesquisa de receitas do servidor.

Sem AOE/Pierce, raio, damage source, status ou TTL próprios. Claims, LOS e ownership não são checados explicitamente nesses callbacks; proteção externa continua por auditar. O dye/crafting usado como transformação não corresponde a uma receita consumida com todos os seus insumos: a classe monta containers sintéticos [recipes]. Perks devem separar seleção de cor, quantidade da stack e mutação do mundo; VFX/som não confirmam transformação.

Receita de aprendizagem [recipe]: `ars_nouveau:abjuration_essence + #c:dyes×3`, **27XP**, starter **não** [xp] [starter]. TierI herdado e mana30 default não são custo/config efetivos [defaults] [wololo-config]. Sem cooldown autônomo; [aquisição85/85](../../ACQUISITION.md).

## Certificação estática individual — 25/10/2026

| Campo | Contrato e limite verificado |
|---|---|
| Identidade e versão | `ars_nouveau:wololo`, EffectWololo, Ars5.13.1, tierI herdado; escola nativa não declarada. |
| Comportamento e causalidade | Recolore por componentes, sheep, equipamento, interação de Mob, interface, sign ou receita; cada ramo tem precedência própria [wololo-entity] [wololo-block]. |
| Parâmetros e caps | Paleta16 ou RGB contínuo; Sensitive flag e Randomize flag, não scalars de potência. MAX_RECIPE_CACHE16 não é limite efetivo comprovado [recipes] [fixed-stack]. |
| Targeting e resultado | Entidade/bloco único entregue pela Form; slots de armadura podem ser múltiplos, stack inteira conserva contagem. Sem dano/TTL/raio/projétil próprio. |
| Custos e aquisição | Mana30, tierI, 27XP, essência+3dyes, starter não; consumo de dye não é garantido pela consulta e depende também do callback downstream. |
| Integração e autoridade | `IWololoable.setColor` é API consumida; não permite presumir acesso a inventário, claims ou conversão arbitrária. Sem perk bridge validada, dedup por transformação efetiva. |
| Evidência e validação | `PINNED_SOURCE_PLUS_SHA_EXACT_BINARY_IDENTITY`; source pinado, identidade compilada, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`. |

## Fronteira de perks e validade

`SpellModifierEvent` oferece uma API pública real no [builder original][builder]; mutação *in-place* é uma superfície distinta de substituir `event.builder`, que não é relido no retorno. [EffectResolveEvent.Pre no resolver][resolve] permite veto; trocar campos do payload não substitui os locais de alvo, effect, stats ou contexto. `Post` pode ocorrer sem aplicação efetiva. Uma lista de augments modificada não recalcula automaticamente scalars/flags já construídos.

Ars governa composição, estados, inventários e aprendizagem; RPG Skill Tree fornece progressão por contrato comprovado. Black Arcana mantém casting, Corruption, Strain e WorldEffectPolicy próprios; Enshrouded mantém seus sistemas ambientais. Aplicação, tick, renderização, atualização de tile e callback não são novos casts pagos ou créditos de Mastery. [Admissão e pagamento][payment] são separados; custo default de um glyph não é preço final da composição e mana de jogador não é Source.

**✅ `claim_scope=STATIC_TECHNICAL_CATALOG_ONLY`; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** Fonte oficial `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`, release **5.13.1**. Publisher `ars_nouveau-1.21.1-5.13.1.jar`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`; a [auditoria compilada](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md) prova **ID/classe**, sem correspondência integral dos métodos Java/bytecode. Config instalada, addons, proteção, persistência física, cliente/servidor e gameplay em modpack não foram validados. Mudanças de JAR, configuração, código ou consumidores exigem reauditoria.

[costs]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L127-L150
[starter]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L307-L310
[xp]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L142-L157
[builder]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L138-L152
[resolve]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellResolver.java#L203-L270
[payment]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellResolver.java#L273-L298
[wololo-id]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectWololo.java#L61-L69
[wololo-entity]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectWololo.java#L71-L113
[dye]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectWololo.java#L115-L134
[wololo-block]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectWololo.java#L136-L175
[recipes]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectWololo.java#L177-L230
[palette]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectWololo.java#L232-L240
[wololo-config]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectWololo.java#L243-L285
[fixed-stack]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/debug/FixedStack.java#L5-L20
[iwololoable]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/IWololoable.java#L5-L9
[find]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/item/inv/InventoryManager.java#L186-L208
[defaults]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L145-L150
[school]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L189-L195
[recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L125-L125
