# Ars Rituals on moving contraptions

State: `SOURCE-PINNED 5.4.0 / PARTIAL-COMPAT DESIGN / RUNTIME QA REQUIRED`

Release 5.4.0's changelog is `Add ritual support to contraptions`.

`RitualBehavior` reconstructs a ritual by registry id and serialized state, attaches a stand-in `RitualBrazierTile` at the moving position, supports decorative particles, consumes eligible nearby item entities while not running, obtains Source through Ars `SourceUtil`, runs `tryTick` and writes ritual state back into the movement context.

The source explicitly comments that rituals have access to a mocked tile and that some rituals not working is expected. Therefore Phase 2S records `ritual support` as a bridge family, not universal compatibility with every Ars/addon ritual.

The custom body in `RitualInteraction.handlePlayerInteraction` is commented out at the exact checkpoint, so placement/start/item-interaction behavior beyond active movement ticking is not promoted without runtime evidence.

Ritual identity/effects remain Ars-owned. Black Arcana must not duplicate them or derive proc chains from a second synthetic ritual.