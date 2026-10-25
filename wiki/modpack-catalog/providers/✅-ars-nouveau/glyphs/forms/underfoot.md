# Underfoot

## Identity

- Provider: Ars Nouveau
- Installed line: `5.13.1`
- Exact source pin: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`
- Type: Form / cast method
- Registry ID: `ars_nouveau:glyph_underfoot`
- Source class: `MethodUnderfoot`

## Source-pinned behavior

Underfoot resolves the following spell effects beneath the caster. In the ordinary cast/entity invocation path, Ars Nouveau first checks whether the caster is riding an entity; otherwise it searches a narrowly inflated area beneath the caster for another entity; if neither case applies, it resolves against the block below the caster.

When invoked through the direct block-use overloads, it resolves against the block below the caster.

Its default mana cost is **5**; the effective cost remains provider-configurable.

## Compatible augments

The exact source exposes **no compatible augments** for this Form.

## Acquisition / learning

- Provider-generated Glyph recipe: `minecraft:iron_boots` + `#minecraft:wooden_pressure_plates`.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned: using the crafted Glyph server-side records it in Ars player data and consumes the Glyph in survival. Runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / Black Arcana consequence

Ars Nouveau owns this under-caster target-selection behavior. Black Arcana must not reuse its nearby-entity selection as an implicit targeting contract: Black Arcana target geometry remains server-validated and bounded. The provider capability also occupies the generic "resolve magic directly beneath the caster" niche for deduplication analysis.

## Validation state

`SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / PACK RUNTIME QA PENDING`

## Mapeamento para perks — targeting real

- **Source pin:** [`MethodUnderfoot.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/method/MethodUnderfoot.java), Ars Nouveau 5.13.1.
- **Alvo em cast genérico e onCastOnEntity:** primeiro `caster.getVehicle()`; senão `world.getEntities(caster, caster.getBoundingBox().inflate(0.1,1.5,0.1))` e o primeiro da lista; se nenhum, usa `BlockHitResult` no bloco abaixo. **Divergência por overload:** `onCastOnBlock` sempre aponta ao bloco sob o caster, sem busca de entidades. **Mana:** default 5; `getCompatibleAugments()=augmentSetOf()`. **Perks:** a primeira entidade encontrada não é automaticamente alvo de combate nem critério de propriedade RPG; não reimplementar target finder sem auditoria e sem hook.
- **Status:** ✅ método/fonte identificado; ⛔ mutação de targeting por perk RPG não verificada. Ars controla SpellResolver, custos e cadeia de efeitos; Black Arcana só controla suas casts. Runtime/Survival: PENDING.

## Certificação técnica estática — Forms 5.13.1

**✅ 100% dos campos relevantes ao contrato estático desta Form; ⛔ hook de mutação de perk NÃO VALIDADO; ⚠️ gameplay/servidor/config do pack NÃO TESTADOS.**

| Eixo de perk | Contrato auditado / limite |
|---|---|
| Identidade e versão | `ars_nouveau:glyph_underfoot`, classe `MethodUnderfoot`, versão Ars Nouveau 5.13.1; [fonte upstream em commit imutável](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/method/MethodUnderfoot.java) e [registry compilado exato](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). |
| Comportamento e beneficiário | onCast/onCastOnEntity prioriza getVehicle(); caso contrário consulta entidades em AABB do caster inflada (0.1,1.5,0.1), usa a primeira retornada ou resolve no bloco abaixo do caster. onCastOnBlock em seus dois overloads usa diretamente o bloco abaixo. |
| Parâmetros, caps, geometria e compatibilidade | Sem augments compatíveis. A caixa inflada é apenas seleção espacial local, não atributo geral de alcance nem hitbox alterável. A ordem da lista de entidades não está garantida por esta classe. |
| Alvo, dano e duração | Targeting é definido pela Form conforme os overloads anteriores. Tipo/quantidade de dano e duração de efeitos posteriores não pertencem à Form (N/A como scalar próprio). Projétil só existe como entidade própria na Form Projectile. |
| Custos, cast e aquisição | Mana-default 5, tier I, starter default não; receita `minecraft:iron_boots` + `#minecraft:wooden_pressure_plates`, XP datagen default 27. [Aquisição 85/85](../../ACQUISITION.md). Mana real e cooldown/settlement dependem de provider/config do cast composto; não há custo autônomo por efeito resultante. |
| Boundary de integração | `SpellResolver`, targets, validação de form, custo e entidades são provider-owned Ars Nouveau. RPG Skill Tree só oferece perks/progressão por interface demonstrada, sem refazer resolver. Black Arcana controla exclusivamente seu runtime, world policy e regras de cast. Um `SpellModifierEvent` público não prova que modificar esta Form ou seu targeting seja seguro ou aceito. |
| Validação e limites | `PINNED_SOURCE_PLUS_SHA_EXACT_BINARY_IDENTITY`: source `112920ff774831f204031da75b4c4e73d3765157`; JAR `ars_nouveau-1.21.1-5.13.1.jar` SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`. ID/class do JAR comprovados; **não** comprovada equivalência completa de bytecode de métodos, configuração implantada, QA de multiplayer ou hook mutador. |

**Gates não promovidos:** `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; não alterar quantidade de magias, estágio de runtime ou sistema de casting por esta ficha. Mudança da versão ou da receita/defaults exige nova auditoria.
