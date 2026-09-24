# Ars Controle 1.6.16 — technical audit

Status: `SOURCE-PINNED STATIC/RUNTIME-PATH AUDIT / INSTALLED-JAR QA PENDING`

Source checkpoint: `Vonr/Ars-Controle@14c5f4770a9ec265491fb9a7ae1a60a2123dfbc0` (`ver: 1.6.16`).

## Registration architecture

The exact 1.6.16 source centralizes game/content registration in `ACRegistry` and the mod constructor calls `ACRegistry.register(bus)`. `ACRegistry.java` is byte-identical at Git-blob level to 1.6.15 (`b38959053740605768a8945ed40c012c6bef5953`), so the registered content surface did not change in this release. The closed registry surface is recorded in `REGISTRIES.md`: 4 blocks, 6 items, 3 BlockEntityTypes, 2 data components, 4 attachments, 1 creative tab and 9 Ars spell parts.

Separate capability registration occurs in the mod constructor listener and does not create additional player glyph/content registries.

## Persistence model

Provider-owned state uses two mechanisms:

1. persistent/network-synchronized item data components:
   - `ars_controle:remote_data`;
   - `ars_controle:portable_brazier`;
2. NeoForge attachments:
   - `ars_controle:relay_uuid`;
   - `ars_controle:association`;
   - `ars_controle:block_target`;
   - `ars_controle:entity_target`.

Remote state can contain `GlobalPos`, UUID, lock/selection flags, a first-corner `GlobalPos` and a display component. Relay state contains brazier `GlobalPos`, relay UUID and ritual-name string.

These serialized references are provider state only. Persistence does not make a referenced endpoint currently loaded, valid, owned or authorized for Black Arcana.

## Networking — 5 payloads, protocol registrar `1`

Client -> server:

- `ars_controle:clear_remote`;
- `ars_controle:set_remote_lock_mode`;
- `ars_controle:set_remote_selection_mode`.

Server -> client:

- `ars_controle:sync_association`;
- `ars_controle:render_block_outline`.

The three Remote C2S handlers resolve the sender on the server and mutate only when the server-side main-hand stack is the Ars Controle Remote. Lock/selection payloads carry enums; clear has no coordinate/entity payload.

`sync_association` updates the client-side attachment only when the client is in the matching dimension and the target block entity exists. `render_block_outline` is presentation feedback.

Black Arcana must not trust or reuse these payloads as its cast/target protocol.

## Spell grammar hooks

Ars Controle injects `BinaryFilterValidator` and `UnaryFilterValidator` into Ars Nouveau `StandardSpellValidator`.

Binary filters require the next two relevant parts to be filters; supported spell modifiers between first/second filter are accounted for. Unary NOT requires the next part to be a filter. Adaptive filters cannot be chained into adaptive filters; malformed structures produce provider validation errors instead of being silently interpreted.

The filters therefore extend the Ars spell grammar itself and remain within Ars cast authority.

## Mixins

Exact mixin config declares six common mixins/invokers and one client invoker:

- `AbstractRitualInvoker`;
- `AbstractRitualMixin`;
- `ComparatorBlockMixin`;
- `RitualBrazierTileMixin`;
- `RitualEventQueueMixin`;
- `StandardSpellValidatorMixin`;
- client `LevelRendererInvoker`.

The mixin plugin currently returns `true` for provider-package mixins; previously contemplated Ars-version-specific EventQueue gating is commented out. The 1.6.16 source build now targets Ars Nouveau `5.13.1.1403`, but required mixin application and assembled-pack behavior still require runtime testing.

## Remote capability delegation

Scryer's Linkage registers handlers for NeoForge block capabilities except configured blacklisted classes. It delegates to the remote provider through `BlockCapabilityCache`; it does not clone resource state.

A stack-overflow guard removes the target on recursive capability query. This is a defensive behavior, not a proof that arbitrary remote-capability graphs are safe.

## Performance/safety observations

### Warping Spell Prism

- can add a provider region ticket for the target chunk;
- default ticket lifetime parameter: 600 ticks;
- cross-dimensional projectile recreation is bounded to the one projectile hit path;
- provider Source settlement has an entity-target path divergence requiring QA.

### Scryer's Linkage

- linked block entity ticker checks target block-entity identity and updates neighboring redstone/comparator state every tick;
- capability caches expire after one minute of access and invalidate on target changes;
- many active links require representative performance QA.

### Temporal Stability Sensor

- scheduled every 10 ticks at `EXTREMELY_HIGH` tick priority;
- many deployed sensors require performance QA.

### Remote multiple selection

- exact source iterates `BlockPos.betweenClosed(firstCorner, secondCorner)`;
- no explicit volume/range ceiling is visible in the audited Remote path;
- this is a provider risk and specifically **not** a pattern Black Arcana may copy.

### Portable Brazier Relay

- relay map refresh is limited to once per 60 server ticks and scans online-player main inventories;
- active relayed ritual ticking can occur each carried-item tick;
- normal brazier ticking is suppressed while relayed, preventing the obvious duplicate tick path.

## 1.6.15 -> 1.6.16 release delta

The exact upstream compare contains six commits. No registry file changed. The only gameplay Java change is `WarpingSpellPrismBlock.java`, adapting the hit callback to the Ars Nouveau 5.13.1 API and correcting direct-block-hit direction with `Direction.getNearest(spell.getDeltaMovement())`. Other changes are the Ars dependency bump, version metadata, translations and asset optimization.

This proves registry continuity, not runtime compatibility.

## Version drift

Source build -> physical pack:

- NeoForge `21.1.217` -> `21.1.248`;
- Ars Nouveau source target `5.13.1.1403` -> installed line `5.13.1`;
- Curios `9.0.12` -> `9.5.1+1.21.1`;
- CC:Tweaked baseline `1.112.0` -> provider absent in current physical pack.

Static identities/defaults can be source-cataloged. Event/mixin/capability/network/runtime settlement behavior remains separately test-gated.

## API/adapter posture

Phase 2R discovers behavior; it does not approve a public integration API. Public Java visibility, class names, data components and attachments are not automatically supported addon contracts.

Any Black Arcana adapter remains `FAIL-CLOSED` until a specific exact-version seam is proven safe and preserves provider resource ownership, causal identity, target validation and deduplication.
