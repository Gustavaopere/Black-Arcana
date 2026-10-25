# Self

## Identity

- Provider: Ars Nouveau
- Installed line: `5.13.1`
- Exact source pin: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`
- Type: Form / cast method
- Registry ID: `ars_nouveau:glyph_self`
- Source class: `MethodSelf`

## Source-pinned behavior

Self resolves the following spell effects against the caster. The exact source consistently redirects block/entity invocation surfaces back to the invoking caster rather than the externally selected target.

Its default mana cost is **10**; the effective cost remains Ars Nouveau configuration state.

## Compatible augments

The exact source exposes **no compatible augments** for this Form.

`MethodSelf` explicitly marks itself as a default starter glyph.

## Acquisition / learning

- Provider-generated Glyph recipe: `#minecraft:wooden_pressure_plates` + `minecraft:iron_chestplate`.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **yes**. When runtime config preserves this default, Self is considered known without consuming a Glyph item.
- The generated recipe still exists; provider Glyph learning rejects the item while Self is currently configured as a starter.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / Black Arcana consequence

Ars Nouveau owns Self-form resolution and its mana/config semantics. Black Arcana self-targeted spells remain distinct Black Arcana cast definitions and still pass through canonical server authority, transactional costs, cooldowns and Arcane Danger where applicable; Ars Self must not become a shortcut around those contracts.

## Validation state

`SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / PACK RUNTIME QA PENDING`

## Mapeamento para perks — targeting real

- **Source pin:** [`MethodSelf.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/method/MethodSelf.java), Ars Nouveau 5.13.1.
- **Resolver:** `onCast`, `onCastOnBlock` e `onCastOnEntity` convertem o destino em `EntityHitResult(caster/playerIn)`, enviando `resolver.onResolveEffect` ao próprio caster — mesmo que o jogador tenha clicado outro bloco/entidade. **Mana:** default 10; starter por `defaultedStarterGlyph=true`. **Augments:** `getCompatibleAugments() = augmentSetOf()` (nenhum). **Efeitos:** emitter e sound são visuais e não confirmam resultado de cada effect da cadeia. **Perks:** mudar target self para aliado/inimigo seria alteração de contrato da Form, sem hook comprovado.
- **Status:** ✅ método/fonte identificado; ⛔ mutação de targeting por perk RPG não verificada. Ars controla SpellResolver, custos e cadeia de efeitos; Black Arcana só controla suas casts. Runtime/Survival: PENDING.

## Certificação técnica estática — Forms 5.13.1

**✅ 100% dos campos relevantes ao contrato estático desta Form; ⛔ hook de mutação de perk NÃO VALIDADO; ⚠️ gameplay/servidor/config do pack NÃO TESTADOS.**

| Eixo de perk | Contrato auditado / limite |
|---|---|
| Identidade e versão | `ars_nouveau:glyph_self`, classe `MethodSelf`, versão Ars Nouveau 5.13.1; [fonte upstream em commit imutável](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/method/MethodSelf.java) e [registry compilado exato](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). |
| Comportamento e beneficiário | Todos os caminhos onCast/onCastOnBlock/onCastOnEntity resolvem via EntityHitResult(caster/playerIn). O alvo clicado não substitui o destinatário dos efeitos. Som/partículas podem usar outra posição, sem mudar o target. |
| Parâmetros, caps, geometria e compatibilidade | Não possui augments compatíveis. Não possui range, AoE, projétil, dano ou duração próprios; efeitos posteriores são decididos pela composição Ars. |
| Alvo, dano e duração | Targeting é definido pela Form conforme os overloads anteriores. Tipo/quantidade de dano e duração de efeitos posteriores não pertencem à Form (N/A como scalar próprio). Projétil só existe como entidade própria na Form Projectile. |
| Custos, cast e aquisição | Mana-default 10, tier I, starter default sim; receita `#minecraft:wooden_pressure_plates` + `minecraft:iron_chestplate`, XP datagen default 27. [Aquisição 85/85](../../ACQUISITION.md). Mana real e cooldown/settlement dependem de provider/config do cast composto; não há custo autônomo por efeito resultante. |
| Boundary de integração | `SpellResolver`, targets, validação de form, custo e entidades são provider-owned Ars Nouveau. RPG Skill Tree só oferece perks/progressão por interface demonstrada, sem refazer resolver. Black Arcana controla exclusivamente seu runtime, world policy e regras de cast. Um `SpellModifierEvent` público não prova que modificar esta Form ou seu targeting seja seguro ou aceito. |
| Validação e limites | `PINNED_SOURCE_PLUS_SHA_EXACT_BINARY_IDENTITY`: source `112920ff774831f204031da75b4c4e73d3765157`; JAR `ars_nouveau-1.21.1-5.13.1.jar` SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`. ID/class do JAR comprovados; **não** comprovada equivalência completa de bytecode de métodos, configuração implantada, QA de multiplayer ou hook mutador. |

**Gates não promovidos:** `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; não alterar quantidade de magias, estágio de runtime ou sistema de casting por esta ficha. Mudança da versão ou da receita/defaults exige nova auditoria.
