# Touch

## Identity

- Provider: Ars Nouveau
- Installed line: `5.13.1`
- Exact source pin: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`
- Type: Form / cast method
- Registry ID: `ars_nouveau:glyph_touch`
- Source class: `MethodTouch`

## Source-pinned behavior

Touch resolves the following spell effects directly against the targeted block or entity. A bare cast without a block/entity target reports failure in the exact source. Its default mana cost is **5**; the effective cost is provider-configurable.

The form also emits its provider-owned resolution particles/sound and requests a temporary fading-light presentation around the resolved target.

When invoked from a Rune caster context against an entity, the form returns Ars Nouveau's `SUCCESS_NO_EXPEND` result rather than a normal success result; that provider-specific settlement behavior must remain Ars-owned.

## Compatible augments

The exact source permits only:

- `ars_nouveau:glyph_sensitive` — extends targeting to air and fluids according to Ars Nouveau's own targeting semantics.

`MethodTouch` explicitly marks itself as a default starter glyph.

## Acquisition / learning

- Provider-generated Glyph recipe: `#minecraft:buttons`.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **yes**. When runtime config preserves this default, Touch is considered known without consuming a Glyph item.
- The generated recipe still exists; provider Glyph learning rejects the item while Touch is currently configured as a starter.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / Black Arcana consequence

Ars Nouveau owns direct Touch resolution, Rune interaction semantics, particles/lights and provider mana/config values. Black Arcana must not reinterpret a Touch cast as authority to bypass its own server targeting or `WorldEffectPolicy`; Black Arcana spells keep their canonical target validation even if an Ars bridge uses this provider method.

## Validation state

`SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / PACK RUNTIME QA PENDING`

## Mapeamento para perks — targeting real

- **Source pin:** [`MethodTouch.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/method/MethodTouch.java), Ars Nouveau 5.13.1.
- **Resolver:** `onCast` sem destino de bloco/entidade retorna `CastResolveType.FAILURE`. Overloads `onCastOnBlock` e `onCastOnEntity` passam diretamente `BlockHitResult`/`EntityHitResult` a `resolver.onResolveEffect`. **Rune:** para `SpellContext.CasterType.RUNE` em target de entidade, retorna `SUCCESS_NO_EXPEND`; isso é regra de settlement Ars, não desconto concedido por perk. **Augments:** somente Sensitive, capaz de permitir mira em ar/fluidos segundo o provider; mana default 5. **Perks:** preservar o resultado SUCCESS/FAILURE e lógica de runa; não gerar efeitos por partículas ou sound de resolução.
- **Status:** ✅ método/fonte identificado; ⛔ mutação de targeting por perk RPG não verificada. Ars controla SpellResolver, custos e cadeia de efeitos; Black Arcana só controla suas casts. Runtime/Survival: PENDING.

## Certificação técnica estática — Forms 5.13.1

**✅ 100% dos campos relevantes ao contrato estático desta Form; ⛔ hook de mutação de perk NÃO VALIDADO; ⚠️ gameplay/servidor/config do pack NÃO TESTADOS.**

| Eixo de perk | Contrato auditado / limite |
|---|---|
| Identidade e versão | `ars_nouveau:glyph_touch`, classe `MethodTouch`, versão Ars Nouveau 5.13.1; [fonte upstream em commit imutável](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/method/MethodTouch.java) e [registry compilado exato](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). |
| Comportamento e beneficiário | onCast sem alvo definido retorna FAILURE; overloads com hit de bloco/entidade passam BlockHitResult/EntityHitResult ao resolver. onCastOnEntity em contexto CasterType.RUNE retorna SUCCESS_NO_EXPEND, diferentemente da resolução padrão. |
| Parâmetros, caps, geometria e compatibilidade | Somente Sensitive é compatível; sua descrição indica suporte a ar/fluidos. Fading light, partículas e som são apresentação e não provam hit ou gasto. Target é o bloco/entidade recebido pelo overload, sem projetil próprio. |
| Alvo, dano e duração | Targeting é definido pela Form conforme os overloads anteriores. Tipo/quantidade de dano e duração de efeitos posteriores não pertencem à Form (N/A como scalar próprio). Projétil só existe como entidade própria na Form Projectile. |
| Custos, cast e aquisição | Mana-default 5, tier I, starter default sim; receita `#minecraft:buttons`, XP datagen default 27. [Aquisição 85/85](../../ACQUISITION.md). Mana real e cooldown/settlement dependem de provider/config do cast composto; não há custo autônomo por efeito resultante. |
| Boundary de integração | `SpellResolver`, targets, validação de form, custo e entidades são provider-owned Ars Nouveau. RPG Skill Tree só oferece perks/progressão por interface demonstrada, sem refazer resolver. Black Arcana controla exclusivamente seu runtime, world policy e regras de cast. Um `SpellModifierEvent` público não prova que modificar esta Form ou seu targeting seja seguro ou aceito. |
| Validação e limites | `PINNED_SOURCE_PLUS_SHA_EXACT_BINARY_IDENTITY`: source `112920ff774831f204031da75b4c4e73d3765157`; JAR `ars_nouveau-1.21.1-5.13.1.jar` SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`. ID/class do JAR comprovados; **não** comprovada equivalência completa de bytecode de métodos, configuração implantada, QA de multiplayer ou hook mutador. |

**Gates não promovidos:** `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; não alterar quantidade de magias, estágio de runtime ou sistema de casting por esta ficha. Mudança da versão ou da receita/defaults exige nova auditoria.
