# Ars Nouveau — Rune

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_rune`
- Display name: Rune
- School: Manipulation
- Default tier: 1
- Default mana cost: 30
- Compatible augments: Sensitive
- Default Sensitive limit: 1

## Provider-native behavior

Rune creates an Ars rune block, cancels the current spell context, creates a child context, prepends `Touch` to the remaining spell recipe and stores that resulting spell on the `RuneTile`. The rune is temporary and triggers the stored spell when a target touches it. Sensitive changes inventory ownership behavior for pickup/usage according to provider semantics.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:manipulation_essence` + `ars_nouveau:runic_chalk` + `minecraft:tripwire_hook`.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

This is a provider-owned delayed/triggered spell-execution surface. Black Arcana must not route Ars rune execution through a second Black Arcana casting pipeline or duplicate costs/effects. Black Arcana rituals/traps require their own canonical server-authoritative contracts.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectRune`).

## Dossiê de engenharia para perks — causalidade exata

- **Código versionado:** [`EffectRune.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectRune.java), `com.hollingsworth.arsnouveau.common.spell.effect.EffectRune` no Ars 5.13.1, método `onResolve`.
- **Lifecycle:** `SpellContext newContext=spellContext.makeChildContext()` e `spellContext.setCanceled(true)` transferem a cadeia para execução posterior; isso não é cancelamento global de magia por erro. **Colocação:** posição do hit (corrigida se `BlockHitResult.isInside`), exige replaceable, world bounds e `BlockUtil.destroyRespectsClaim`; coloca `RUNE_BLOCK`. **Armazenamento:** em `RuneTile` persiste UUID do jogador caster, `isTemporary=true`, cópia do child spell com `MethodTouch.INSTANCE` inserido no começo e `isSensitive`. Sensitive limit 1. **Perks:** progresso/recursos de colocação e trigger posterior exigem deduplicação e auditoria `RuneTile`; sem autorização para criar uma segunda transação no Black Arcana.
- **Limite de integração:** ✅ source pin da lógica local, ⚠️ execução auxiliares/config dependem do provider real; ⛔ hook externo de mutação não comprovado. Black Arcana só governa suas world mutations; RPG Skill Tree depende de bridge real. QA Survival PENDING.
