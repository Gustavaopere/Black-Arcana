# Heal

- Registry ID: `ars_nouveau:glyph_heal`
- Source class: `EffectHeal`
- School: Abjuration
- Default tier: **2**
- Default mana: **50**
- Default heal config: **3.0** base + **3.0** per amplification unit
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Source-pinned behavior

Heals a living target, with randomized stats able to alter the heal amount. Healing a Player causes provider-side food exhaustion. Targets using inverted heal/harm semantics instead receive provider-owned magic damage for the same computed amount.

Compatible augments: Amplify, Dampen, Fortune, Randomize.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:abjuration_essence` + `minecraft:glistering_melon_slice` ×4 + `minecraft:golden_apple`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars Nouveau owns healing, food exhaustion, undead/inverted-heal damage and configured values. Black Arcana must not create duplicate healing settlement, damage procs or progression awards from the same provider event.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.

## Localizadores e parâmetros para Codex — fonte exata

- **Java:** [`EffectHeal.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectHeal.java) no commit `112920ff774831f204031da75b4c4e73d3765157` correspondente ao catálogo Ars 5.13.1.
- **Alvo:** `onResolveEntity` requer `LivingEntity` válida e `ServerLevel`; ignora removidos ou saúde <=0.
- **Cálculo:** `healVal = GENERIC_DOUBLE.get() + AMP_VALUE.get()*spellStats.getAmpMultiplier()`, defaults configuráveis 3.0 base e 3.0 per amplifier. `Randomize` aplica rolagem somente na branch de cura, após seleção do destino.
- **Alvo de cura invertida:** `isInvertedHealAndHarm` muda para dano de `DamageTypes.MAGIC` via `attemptDamage`; não tratar a magia como heal-only para todas as entidades.
- **Alvo player:** `causeFoodExhaustion(2.5f)` antes de `heal`; custos de fome não podem ser ignorados por perks.
- **Augments:** Amplify, Dampen, Fortune, Randomize. Hook específico para trocar amount/target ainda **não comprovado**; sem duplicar cura/dano.

**Estado:** prova estática de parâmetros por leitura de código; habilidade de mutação por hook externo não verificada. Ars controla composição, execução, mana/Source e configurações; RPG Skill Tree controla perks/Mastery/gates; Black Arcana é autoridade somente de seu runtime próprio. [Padrão universal](../../../meta/PERK-READY-TECHNICAL-STANDARD.md).
