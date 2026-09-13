# SnackPirate's Aeromancy Additions 1.2.8 — mixin and network boundaries

Status: `2 REQUIRED MIXINS / 3 PROVIDER-OWNED PAYLOAD REGISTRATIONS OBSERVED / CURRENT-HOST QA OPEN`

Exact source: `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`

## Required mixin footprint

`aeromancy.mixins.json` is `required: true`, uses Mixin `0.8`, `compatibilityLevel: JAVA_21` and `defaultRequire: 1`.

Common mixins:

- `ServerPlayerMixin`
- `ServerPacketListenerMixin`

Total: **2 required direct bindings**.

These are implementation-sensitive surfaces, not stable Black Arcana interoperability APIs. Direct runtime application against the current full pack remains an explicit QA gate.

## Provider-owned network surface

`AAPayloadHandler` registers an optional versioned `1.0.0` payload registrar with exactly three observed registrations:

- S2C `DashParticlesPacket`
- C2S `AirstepPacket`
- S2C `AASyncPlayerDataPacket`

`AirstepPacket` carries directional input and dispatches server-side to the provider's `AirstepSpell.airstepJump(...)`. The provider handler itself checks the provider-owned Airstep state: remaining jumps, active Airstepping effect and airborne state before applying movement and consuming a jump.

This evidence is used only to establish authority/boundary and direct-QA risk. Black Arcana must not recreate, proxy or double-process Airstep movement, provider attachment state or provider packet settlement.

## Black Arcana boundary

Iron's remains authority for its cast lifecycle, mana and cooldowns. Aeromancy remains authority for Wind spell-specific execution, effects/entities and its auxiliary Airstep state/networking. Black Arcana may consume only a real supported/validated integration seam when one exists.

Required mixins and provider payloads are reasons to keep assembled-pack runtime acceptance fail-closed. A source-pinned catalog identity is not proof that every mixin target, payload path or multiplayer state transition works in the current modpack.

One causal cast/action must not be processed twice across Iron's, Aeromancy and any future Black Arcana adapter.
