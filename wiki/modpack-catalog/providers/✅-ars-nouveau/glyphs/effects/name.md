# Ars Nouveau — Name

Status: `SOURCE-PINNED 5.13.1 / STATIC TECHNICAL CONTRACT / RUNTIME QA PENDING`

- Registry id: `ars_nouveau:glyph_name`; classe `com.hollingsworth.arsnouveau.common.spell.effect.EffectName`.
- Escola: Manipulation; tier default **II**; mana default **25**; nenhum augment compatível [name-config].
- O glyph escolhe um texto e altera nomes/estado de persistência nativos. Alvo de entidade e bloco têm efeitos colaterais diferentes; não é somente uma versão remota de Name Tag.

## Seleção e consumo do nome

[getName][name-value] consulta `spellContext.getCaster().getInvManager().findItem(NAME_TAG,EXTRACT)` e lê `getDisplayName().plainCopy()` da referência retornada. **Não extrai nem diminui a Name Tag nesse método**; até uma tag sem nome customizado pode fornecer seu display name padrão. `EXTRACT` é o modo de filtragem da busca, não comprovação de consumo. [InventoryManager.findItem][find] devolve referência sem mutação; prioridade, filtros e acesso dos handlers definem o que é encontrado [preference]. Não prometer busca universal em qualquer inventário ou apenas na hotbar com base na descrição. O helper de prioridade inicia cada wrapper com LOW e pode escolher um handler sem item compatível; a busca posterior pode devolver vazio mesmo havendo match em outro handler.

Se nenhum nome foi obtido, `StackUtil.getHeldCasterToolOrEmpty` prefere ICasterTool da mão principal e depois da offhand [held-tool]. O registro fornece o caster; `getSpellName()` não vazio vira `Component.literal`. Sem tag e sem nome de spell válido, o caminho nominal devolve **null**, usado para remover nomes em vez de ignorar o Effect. Depois de `SpellCasterRegistry.from(stack)`, a classe não testa caster==null antes de getSpellName; um caster tool/componente inválido não tem fallback seguro comprovado nessa função. O texto vem do item/caster provider-owned; SpellStats não contém um campo genérico de nome para perks.

## Execução, targeting e persistência

[onResolveEntity][name-entity] normalmente chama `entity.setCustomName(newName)`. A exceção é atingir o próprio shooter quando sua offhand não está vazia: nesse caso não renomeia a entidade. Em **qualquer alvo de entidade**, a offhand não vazia do shooter também recebe/remove `DataComponents.CUSTOM_NAME`, mesmo se o alvo é outra entidade. Se o alvo é ItemEntity, altera igualmente o nome da stack inteira, não uma unidade. Se é Mob, chama `setPersistenceRequired()` **incondicionalmente**, inclusive quando newName é null. Isso é persistência nativa de mob, não imortalidade nem proteção universal contra remoção.

[onResolveBlock][name-block] usa o bloco atingido. SkullBlockEntity recebe `ResolvableProfile` com nome opcional, UUID ausente e PropertyMap vazio; BaseContainerBlockEntity recebe `name`, update flag3 e `setChanged()`. Ambos retornam antes da busca de entidades. Outros blocos procuram **todas as entidades** em `new AABB(pos).inflate(0.08)`: caixa do bloco expandida em0,08 por eixo, não um raio de aquisição. Renomeia cada entidade; Mob só recebe persistência nesse ramo se `hasCustomName()` após a operação. ItemEntity também tem CUSTOM_NAME da stack atualizado. O caminho de bloco não renomeia a offhand do shooter.

Nenhum desses callbacks impõe alcance da Form, LOS, filtro de aliados, limite de entidades ou checagem local de claims/evento específico de renomeação. Isso delimita o source inspecionado; não prova bypass da política externa. Campos vanilla de nome/profile e persistência mantêm seus contratos próprios de save/sync; esta classe não implementa um ledger reversível ou TTL de nome.

## Custos e aprendizagem

Receita [datagen][recipe]: `ars_nouveau:manipulation_essence + minecraft:name_tag`; **55 XP** default [xp], starter default **não** [starter]. A tag da receita de aprendizagem é separada da tag consultada durante o cast. [Mana25/tierII][name-config] são defaults; composição e configuração efetivas permanecem Ars-owned. Sem cooldown, canalização, dano, DamageType, projétil ou duração autônomos na classe. [Aquisição completa](../../ACQUISITION.md).

## Certificação estática individual — 25/10/2026

| Campo | Contrato e limite verificado |
|---|---|
| Identidade e versão | `ars_nouveau:glyph_name`, EffectName, Ars5.13.1, Manipulation/tierII; identidade compilada e source pinado. |
| Comportamento e causalidade | Nome de tag/caster ou null; mutação em alvo e offhand, Mob persistence e ramos skull/container/caixa separados [name-entity] [name-block]. |
| Parâmetros e caps | Nenhum augment; nome não tem scalar de potência/duração. Sem limite local de quantidade na caixa; sem truncamento/validação de texto próprios [name-value]. |
| Targeting e resultado | EntityHitResult ou bloco; caixa AABB+0,08 somente no fallback de bloco. Sem dano, projétil, TTL ou aquisição de alvo próprios. |
| Custos e aquisição | Mana25, tierII, 55XP, essência+NameTag, starter não; consulta de tag durante cast não consome a stack no caminho inspecionado. |
| Integração e autoridade | `getName` e InventoryManager são pontos reais de leitura; mudar nomes/persistência requer contrato de autorização e dedup próprio. Sem adapter RPG/Black Arcana validado. |
| Evidência e validação | `PINNED_SOURCE_PLUS_SHA_EXACT_BINARY_IDENTITY`; somente contrato estático, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`. |

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
[name-entity]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectName.java#L35-L71
[name-value]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectName.java#L73-L92
[name-block]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectName.java#L94-L124
[name-config]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectName.java#L126-L150
[find]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/item/inv/InventoryManager.java#L186-L208
[preference]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/item/inv/InventoryManager.java#L249-L290
[held-tool]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/StackUtil.java#L62-L70
[recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L114-L114
