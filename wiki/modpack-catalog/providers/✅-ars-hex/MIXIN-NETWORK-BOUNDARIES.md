# Ars Hex 5.0.4b — Mixin & Network Boundaries

Status: `SOURCE DECLARATIONS CLOSED / HOST RUNTIME QA OPEN`

## Mixins — 0/0

The exact `ars_hex.mixins.json` is `required: true`, Java 21 compatible, but declares:

- common `mixins`: empty;
- client `client`: empty.

Therefore Phase 2W records **0 common + 0 client Ars Hex mixins** at the release-aligned checkpoint.

This materially differs from providers such as Ars Technica: Ars Hex's main version-drift risk is event/API/library semantics, not concrete mixin-target breakage.

## Provider-owned payloads

No Ars Hex-specific custom payload registration was identified in the audited source surface. Searches for the NeoForge 1.21.1 payload idioms used by other providers (`CustomPacketPayload`, `RegisterPayloadHandlersEvent`, `PayloadRegistrar`) return no Ars-Unity registration.

Phase 2W therefore records:

- provider-owned custom payloads identified: **0**;
- no second Ars Hex networking protocol is inferred.

This does **not** mean the integrated features are network-free. Ars spell-caster state, Hexerei broom entities and host particles/rendering use their respective host/runtime networking and entity synchronization contracts. Those remain host-owned.

## Client-only surfaces

### Iron's module

Client particle registration wraps five Iron's particle providers and is reached only under `ModList.isLoaded("irons_spellbooks")`.

### Hexerei module

When Hexerei exists, client hooks include:

- particle providers;
- broom entity renderer;
- layer definitions;
- custom item renderer/client extension;
- Ars spell tooltip integration.

Because Hexerei is absent from the physical pack, these source paths should remain dormant in current runtime QA.

## Dedicated-server boundary

The provider bootstrap gates optional modules by `ModList.isLoaded`. Client-facing handlers are event methods with client-only types/annotations where applicable, while common init/post-init performs registry/event integration.

Phase 2W still requires a dedicated-server/full-pack smoke because source organization alone is not proof that no optional/client class can fail classloading with the installed dependency set.

## Black Arcana authority consequence

Black Arcana must preserve D006/D020:

- clients send bounded intent only for BA casts;
- no Ars Hex presentation or host packet becomes BA gameplay authority;
- BA must not add a parallel packet merely to replay Ars Hex damage/perk/scythe state;
- host-owned entity/particle synchronization is observed, not duplicated.
