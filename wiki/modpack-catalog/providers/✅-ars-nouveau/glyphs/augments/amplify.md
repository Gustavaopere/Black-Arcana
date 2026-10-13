# Amplify

- Registry ID: `ars_nouveau:glyph_amplify`
- Source class: `AugmentAmplify`
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`
- Default tier: **1**
- Default mana: **20**

## Source-pinned behavior

Adds **+1.0** amplification. Compatible Ars Nouveau glyphs decide what amplification means; provider documentation/source examples include increased spell damage and higher Break harvest capability.

## Acquisition / learning

- Provider-generated Glyph recipe: `minecraft:diamond_pickaxe`.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Amplification is an Ars spell stat, not a universal Black Arcana damage scalar. Black Arcana power remains governed by its own caps, budgets and diminishing-return contracts.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.

## Mapeamento de perk para Codex — transformação real

- **Source pin:** [`AugmentAmplify.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/augment/AugmentAmplify.java) no Ars Nouveau 5.13.1.
- **Transformação exata:** `applyModifiers(SpellStats.Builder builder, AbstractSpellPart spellPart)` chama `builder.addAmplification(1.0)`. `getDefaultManaCost=20`, tier I. **Interpretação:** efeitos escolhem como usar `spellStats.getAmpMultiplier()`; Harm aumenta dano/Poison, Explosion aumenta intensidade e altera dano via `ANExplosion`, Break altera capacidade de harvest. **Limites:** caps são declarados por cada glyph receptor, por exemplo Harm/Explosion limit 2 e Wither limit 4; Amplify não autoriza todas as combinações e um bonus RPG genérico que supere limites não é automaticamente seguro.
- **Bridge:** `source identified / mutation hook NOT VERIFIED / provider-owned`. Não implementar segundo `SpellStats` no Black Arcana, nem usar atributos RPG sem seam verificado. Testes em modpack/Survival PENDING.
