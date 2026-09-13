# SnackPirate's Aeromancy Additions 1.2.8 — mixin and network boundaries

Status: `2 REQUIRED MIXINS / 3 PROVIDER-OWNED PAYLOAD REGISTRATIONS OBSERVED / CURRENT-HOST QA OPEN`

Exact source: `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`

`aeromancy.mixins.json` is required, uses Java 21 compatibility and `defaultRequire: 1`. The two common direct bindings observed are `ServerPlayerMixin` and `ServerPacketListenerMixin`.

`AAPayloadHandler` registers exactly three provider-owned payload paths at the audited pin:

- S2C `DashParticlesPacket`
- C2S `AirstepPacket`
- S2C `AASyncPlayerDataPacket`

The Airstep C2S path hands directional input to provider-owned server logic, which checks provider state before applying movement. These mixins/payloads are implementation-sensitive provider authority, not Black Arcana APIs.

Black Arcana must not recreate, proxy or double-process provider movement/state or Iron's casting, mana and cooldown settlement. Required mixins and payload behavior remain assembled-pack runtime QA gates; source-pinned catalog identity alone does not certify current multiplayer/runtime compatibility.
