# Bubble

Status: `SOURCE-PINNED 5.13.1 / WATER CONTROL EFFECT / SEMANTICS+ACQUISITION AUDITED`

- Registry id: `ars_nouveau:glyph_bubble`
- Display name: `Bubble`
- Default mana cost: `20`
- School: Elemental Water
- Exact source pin: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native behavior

`Bubble` creates a provider-owned `BubbleEntity`. On entity targets it immediately attempts to capture the target; on block targets it creates the bubble at the hit location.

Pinned defaults:

- base lifetime constructor term: `100 ticks`;
- Extend Time contribution: `3 ticks` per provider duration multiplier unit;
- base pop damage: `5.0`;
- Amplify contribution: `2.0`;
- default mana: `20`.

Compatible augments are Extend Time, Amplify, Dampen and Duration Down.

The bubble carries owner information for non-fake casters and controls captured-entity lift/pop behavior in its own entity runtime.

## Acquisition / learning

- Provider-generated Glyph recipe: `#c:feathers` ×3 + `minecraft:water_bucket` + `#minecraft:boats` + `ars_nouveau:water_essence`.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Black Arcana boundary

Capture, lift, lifetime and pop damage are provider-owned settlement. Black Arcana must not register a second imprisonment state or apply duplicate pop damage. Any mastery/danger observation must preserve the original cast identity even when the bubble remains in-world after resolution.

## QA

Entity lifecycle behavior is source-pinned at the spell entry point; full `BubbleEntity` behavior and full-pack runtime interactions remain provider/runtime QA.

## Engenharia para perks — caminho causal individual

- **Fonte exata:** [`EffectBubble.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectBubble.java), `com.hollingsworth.arsnouveau.common.spell.effect.EffectBubble` (Ars 5.13.1).
- **Criador:** `createBubble` instancia `BubbleEntity(level,(int)(100+getDurationMultiplier()*EXTEND_TIME.getAsInt()),(float)(DAMAGE.getAsDouble()+getAmpMultiplier()*AMP_VALUE.getAsDouble()+getDamageModifier()))`; defaults 100 ticks, ExtendTime config 3, DAMAGE 5 e amp 2.
- **Alvos e owner:** ramo em bloco posiciona a bubble no hit; ramo em entidade faz spawn e `bubble.tryCapturing(target)` imediatamente. `bubble.setOwner(shooter)` só é aplicado com `isNotFakePlayer(shooter)`.
- **Perks:** dano calculado é **dano de pop da entidade Bubble**, não dano instantâneo da resolução do glyph. Duração e captura/persistência exigem ler `BubbleEntity`; evento de resolução não prova captura ou pop. Não creditar duplicadamente.
- **Estado:** ✅ assinatura/fórmula do source pin; ⚠️ config carregada, auxiliar e testes físicos pendentes. Contratos de `EffectResolveEvent.Pre` são existentes, porém o adapter RPG, clamps, causalidade e escrita externa **não** foram validados: ⛔ fail-closed até testes.
