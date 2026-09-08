# Rewind

Status: `SOURCE-PINNED 5.13.1 / TIME-MANIPULATION EFFECT`

- Registry id: `ars_nouveau:rewind`
- Display name: `Rewind`
- Default tier: `THREE`
- Default mana cost: `100`
- Exact source pin: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native behavior

`Rewind` delays continuation and rewinds compatible entities through provider-owned recorded history. The pinned source defaults to:

- entity history tracking ceiling: `60 ticks`;
- base rewind: `40 ticks`;
- Extend Time increment: `20 ticks`;
- Duration Down decrement: `10 ticks`;
- Extend Time limit: `1`;
- Duration Down limit: `5`.

For entities it requires `IRewindable`, rejects the provider rewind blacklist and rejects an entity already rewinding. The remaining spell continues through a delayed event after the rewind interval. Block-target resolution also schedules provider-owned delayed/rewind events.

The provider config explicitly warns that entities **anywhere** track rewind state and that a high tracking value is unsuitable for low-spec machines.

Compatible augments are Extend Time and Duration Down.

## Black Arcana boundary

Rewind owns temporal recording, delayed execution and restoration semantics. Black Arcana must not create a parallel history buffer for Ars entities or treat the delayed continuation as a second player cast.

Any independent Black Arcana temporal mechanic must remain bounded and must not borrow this provider state without a real API seam.

## Performance / QA

The global entity-history warning is part of the source-pinned provider contract and remains a representative-performance QA item for the 612-mod pack. Runtime acceptance is not inferred from source inspection.