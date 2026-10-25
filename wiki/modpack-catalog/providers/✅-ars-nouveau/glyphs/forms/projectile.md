# Projectile

## Identity

- Provider: Ars Nouveau
- Installed line: `5.13.1`
- Exact source pin: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`
- Type: Form / cast method
- Registry ID: `ars_nouveau:glyph_projectile`
- Source class: `MethodProjectile`

## Source-pinned behavior

Projectile creates a spell projectile and resolves the following spell effects when that projectile reaches a target or block. Its default mana cost in the 5.13.1 source is **10**; the effective casting cost remains configuration-owned by Ars Nouveau.

The projectile count is increased by Split. Its launch velocity is derived from the spell acceleration multiplier, and the provider exposes a configurable maximum projectile lifespan with a default of **60 seconds**.

## Compatible augments

The exact source permits:

- `ars_nouveau:glyph_pierce` — additional piercing through targets/blocks;
- `ars_nouveau:glyph_split` — creates additional projectiles;
- `ars_nouveau:glyph_accelerate` — raises projectile velocity;
- `ars_nouveau:glyph_decelerate` — lowers projectile velocity;
- `ars_nouveau:glyph_sensitive` — allows collision with plants/materials that normally do not block motion.

`MethodProjectile` explicitly marks itself as a default starter glyph.

## Acquisition / learning

- Provider-generated Glyph recipe: `minecraft:fletching_table` + `minecraft:arrow`.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **yes**. When runtime config preserves this default, the player is treated as already knowing Projectile without consuming a Glyph item.
- The generated recipe still exists; the Ars Glyph-use path rejects learning while the part is currently considered a starter.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / Black Arcana consequence

Ars Nouveau owns this projectile cast method, projectile entity lifecycle, provider mana/config values and glyph compatibility. Black Arcana must not replace it with a second Ars projectile pipeline. A Black Arcana projectile spell may exist only as Black Arcana-owned content entering the canonical Black Arcana cast pipeline, with its own bounded targeting/effect contracts and a material forbidden-domain distinction.

## Validation state

`SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / PACK RUNTIME QA PENDING`

This page records source facts, not proof that the installed 612-mod pack preserves every default config value.

## Localizadores e parâmetros para Codex — fonte exata

- **Java:** [`MethodProjectile.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/method/MethodProjectile.java) no commit `112920ff774831f204031da75b4c4e73d3765157` correspondente ao catálogo Ars 5.13.1.
- **Método resolutor:** `MethodProjectile.onCast` → `summonProjectiles` → entidades `EntityProjectileSpell`, que resolvem **efeitos de glyph posteriores** quando colidem.
- **Quantidade no disparo pela entidade:** `numSplits = 1 + spellStats.getBuffCount(AugmentSplit.INSTANCE)`; velocity `max(0.1, 0.75 + spellStats.getAccMultiplier()/2)`; ângulos de yaw variam em passos alternados de 10°.
- **Diferença importante para perks:** o overload de lançamento em bloco também usa `AugmentSplit`, mas possui posicionamento/velocidade próprios. Qualquer perk de split/velocidade deve preservar origem e resolver do feitiço, não injetar cast extra após o impacto.
- **Lifespan default:** `getProjectileLifespan` busca `PROJECTILE_TTL` configurável (fallback 60 segundos); não é um alcance máximo por blocos.
- **Limites:** `getCompatibleAugments` permite Pierce, Split, Accelerate, Decelerate e Sensitive. Quantidade/velocidade são dados do `SpellStats` provider-native; nenhuma API de reescrita por RPG perk foi comprovada.

**Estado:** prova estática de parâmetros por leitura de código; habilidade de mutação por hook externo não verificada. Ars controla composição, execução, mana/Source e configurações; RPG Skill Tree controla perks/Mastery/gates; Black Arcana é autoridade somente de seu runtime próprio. [Padrão universal](../../../../meta/PERK-READY-TECHNICAL-STANDARD.md).

## Certificação técnica estática — Forms 5.13.1

**✅ 100% dos campos relevantes ao contrato estático desta Form; ⛔ hook de mutação de perk NÃO VALIDADO; ⚠️ gameplay/servidor/config do pack NÃO TESTADOS.**

| Eixo de perk | Contrato auditado / limite |
|---|---|
| Identidade e versão | `ars_nouveau:glyph_projectile`, classe `MethodProjectile`, versão Ars Nouveau 5.13.1; [fonte upstream em commit imutável](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/method/MethodProjectile.java) e [registry compilado exato](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). |
| Comportamento e beneficiário | onCast, onCastOnEntity e onCastOnBlock(UseOnContext) criam EntityProjectileSpell pelo caminho shooter. onCastOnBlock(BlockHitResult,LivingEntity,...) utiliza overload com BlockPos, posição e movimento próprios. Cada entidade compartilha o SpellResolver dos efeitos posteriores, sem representar cast adicional. |
| Parâmetros, caps, geometria e compatibilidade | No caminho shooter, n=1+count(Split), velocidade max(0.1,0.75+accMultiplier/2), yaw alternado em 10° e inaccuracy 0.8. No caminho BlockPos n=1+Split com deltaMovement (0,-0.1,0), não a mesma velocidade. TTL configurável default 60 s; não é range em blocos. Compatíveis Pierce, Split, Accelerate, Decelerate e Sensitive. |
| Alvo, dano e duração | Targeting é definido pela Form conforme os overloads anteriores. Tipo/quantidade de dano e duração de efeitos posteriores não pertencem à Form (N/A como scalar próprio). Projétil só existe como entidade própria na Form Projectile. |
| Custos, cast e aquisição | Mana-default 10, tier I, starter default sim; receita `minecraft:fletching_table` + `minecraft:arrow`, XP datagen default 27. [Aquisição 85/85](../../ACQUISITION.md). Mana real e cooldown/settlement dependem de provider/config do cast composto; não há custo autônomo por efeito resultante. |
| Boundary de integração | `SpellResolver`, targets, validação de form, custo e entidades são provider-owned Ars Nouveau. RPG Skill Tree só oferece perks/progressão por interface demonstrada, sem refazer resolver. Black Arcana controla exclusivamente seu runtime, world policy e regras de cast. Um `SpellModifierEvent` público não prova que modificar esta Form ou seu targeting seja seguro ou aceito. |
| Validação e limites | `PINNED_SOURCE_PLUS_SHA_EXACT_BINARY_IDENTITY`: source `112920ff774831f204031da75b4c4e73d3765157`; JAR `ars_nouveau-1.21.1-5.13.1.jar` SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`. ID/class do JAR comprovados; **não** comprovada equivalência completa de bytecode de métodos, configuração implantada, QA de multiplayer ou hook mutador. |

**Gates não promovidos:** `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; não alterar quantidade de magias, estágio de runtime ou sistema de casting por esta ficha. Mudança da versão ou da receita/defaults exige nova auditoria.
