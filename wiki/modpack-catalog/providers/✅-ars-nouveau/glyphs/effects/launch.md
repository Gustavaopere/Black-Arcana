# Launch

- Registry ID: `ars_nouveau:glyph_launch`
- Source class: `EffectLaunch`
- School: Elemental Air
- Default tier: **1**
- Default mana: **30**
- Default vertical strength config: **0.8** base + **0.25** per amplification unit
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Source-pinned behavior

Adds upward motion to entity targets and resets their fall distance. On blocks it may convert provider-calculated blocks into enchanted falling-block entities and launch them; Sensitive disables the block-moving path.

Compatible augments: Amplify, Dampen, AOE, Sensitive, Pierce. Sensitive is limited to 1 by default.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:air_essence` + `minecraft:rabbit_hide` ×3.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars owns Launch motion and falling-block conversion. Black Arcana launch/movement remains server-authoritative, and any Black Arcana block movement must pass world-safety and bounded-work gates.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.

## Engenharia para perks — caminho causal individual

- **Source pin:** [`EffectLaunch.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectLaunch.java) do Ars 5.13.1.
- **Entity velocity:** `onResolveEntity` usa `setDeltaMovement(old.add(0,GENERIC_DOUBLE+AMP_VALUE*ampMultiplier,0))`; defaults base 0.8 e amp scalar 0.25. Sinaliza `hurtMarked` e zera `fallDistance`.
- **Block velocity:** sem Sensitive percorre `SpellUtil.calcAOEBlocks` e cria `EnchantedFallingBlock.fall`; no sucesso, soma componente vertical `(GENERIC_DOUBLE*0.6)+AMP_VALUE*ampMultiplier` (default base 0.48 + amp*0.25), distinto do valor aplicado à entidade viva; propaga ShapersFocus. Sensitive aborta esse ramo.
- **Perks:** movimento de entidade, mutação de bloco e prevenção de queda têm resultados separados; não duplicar execução de `EnchantedFallingBlock` e requerer QoS de world effects em magias Black Arcana.
- **Estado:** ✅ origem e lógica source-pinned; ⚠️ helpers, itens externos e runtime QA pendentes; ⛔ adapter de perks do RPG sem teste nem contrato para duplo settlement. Ars conserva mana, inventário e efeitos.
