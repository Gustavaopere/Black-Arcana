# Reset

Status: `SOURCE-PINNED 5.13.1 / CONTEXT-MANIPULATION EFFECT / SEMANTICS+ACQUISITION AUDITED`

- Registry id: `ars_nouveau:reset`
- Display name: `Reset`
- Default mana cost: `0`
- Exact source pin: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native behavior

`Reset` is not a normal terminal effect. It implements Ars Nouveau's `IContextManipulator` contract and restructures the remaining `SpellContext`.

The pinned source:

- finds the next `Reset` in the remaining recipe;
- creates a cloned context containing the spell portion before that reset;
- advances the original context index past that segment;
- can clear `NEW_CONTEXT` cancellation so execution continues;
- pushes a new context;
- bypasses combination and occurrence limits for spell parts registered in `EffectReset.RESET_LIMITS`.

The class has no compatible augments and no mana cost.

## Acquisition / learning

- Provider-generated Glyph recipe: `minecraft:target`.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Black Arcana boundary

Reset belongs to Ars Nouveau's spell grammar/runtime. Its context manipulation and limit-bypass semantics must never be reimplemented as a Black Arcana cast shortcut.

A Black Arcana observer must attribute all child/context segments to the original provider cast unless a real provider hook proves another causal identity. No extra mana charge, cooldown, danger settlement or mastery award is created merely because Reset causes multiple resolution contexts.

## QA / runtime

The exact class is source-pinned to 5.13.1. Runtime/config behavior in the full pack remains separately pending.

## Engenharia para perks — caminho causal individual

- **Código exato:** [`EffectReset.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectReset.java), Ars 5.13.1.
- **Registry distinto:** `ars_nouveau:reset` (não `glyph_reset`); `EffectReset implements IContextManipulator`, custo default 0 e conjunto de augments vazio. Não é magia terminal de dano/status.
- **Segmentação:** `manipulate` obtém `context.getRemainingSpell().mutable()`, procura `indexOf(EffectReset.INSTANCE)`, cria `context.clone().withSpell(subList(0,index))`, e avança index do context original por `index`. `contextCanceled` reconhece `CancelReason.NEW_CONTEXT`, limpa cancelamento e pula até próximo Reset, permitindo continuidade.
- **Bypasses internos:** `bypassCombinationLimitsFor()` e `bypassOccurrenceLimitsFor()` retornam `EffectReset.RESET_LIMITS`, conjunto preenchido por effects como Wall/Linger; não é permissão global para ilimitadas magias do Black Arcana. `shouldPushContext` retorna true. **Perks:** multiplicação de resolvers/contextos pode multiplicar observers; preservar identidade causal e gates de receitas Ars.
- **Estado:** ✅ assinatura/source; ⚠️ integração de plugins proteção, configs e gameplay pending; ⛔ nenhum adapter RPG testado nem permissão para duplicar a cadeia causal/perk/mastery.
