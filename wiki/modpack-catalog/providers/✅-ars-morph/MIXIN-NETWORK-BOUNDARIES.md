# Ars Morph 2.0.0 — Mixin, networking and config boundaries

Status: `SOURCE SURFACE CLOSED / RUNTIME TRANSPORT QA OPEN`

## Mixins — 0/0

`ars_morph.mixins.json` declares:

- common mixins: 0;
- client mixins: 0.

The manifest still names the mixin config, but it contains no declared target classes at the release-aligned source checkpoint.

## Provider-owned custom payloads

No Ars Morph source file/path matching a provider-owned payload/network registration surface was identified in the exact recursive tree, and no custom payload registration is present in the audited Java files.

This does not mean the feature is network-free. It delegates transport/state synchronization to host providers:

- Ars spell/entity networking remains Ars-owned;
- Identity2 morph/variant/ability networking remains Identity2-owned;
- `IdentityApi.syncBoolean(serverPlayer, "isFlying", flying)` is explicitly an Identity2 API call.

Black Arcana must not add a parallel packet merely to mirror the same provider state.

## Config boundary

`MorphConfig` constructs an empty COMMON spec, but `ArsMorph` has the call that would register that spec commented out.

The actual production setting found in source is built by `EffectMorph.buildConfig(...)`:

- key `max_hp_morph`;
- default 100;
- min 20;
- max `Integer.MAX_VALUE`.

This is part of the Ars spell-part configuration lifecycle, not an independently registered Ars Morph COMMON config proven by `MorphConfig`.

The installed/generated config path/value must be inspected before claiming the exact physical filename/location.

## Security/authority implications

- server-side Morph glyph mutation requires a real `ServerPlayer` and delegates persistence to Identity2;
- no BA client packet should be allowed to assert an Identity2 form;
- player-target morph behavior must be tested for permission/friendly-target semantics at the provider/runtime layer;
- Identity2 ability cooldown/use-duration data must remain provider-owned;
- variant synchronization must not be mirrored into a BA-owned NBT/network state.

## Runtime QA

- inspect actual physical JAR payload/mixin/config metadata;
- validate Identity2 provider synchronization after version drift;
- validate malicious/invalid client inputs through the host providers rather than inventing an Ars Morph C2S contract;
- dedicated-server boot and dimension/login synchronization.
