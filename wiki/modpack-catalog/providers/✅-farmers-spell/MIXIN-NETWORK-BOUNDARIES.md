# Farmer's Spell 1.0.5.1 — Mixin and network boundaries

Status: `7 REQUIRED MIXINS / 0 PROVIDER-OWNED PAYLOAD REGISTRATIONS OBSERVED / CURRENT-HOST QA OPEN`

Exact source: `GLDYM/Farmers-Spell-n-Spellbook@b7cbb40316a9ccbbc2ce2b56b3023647261ce569`

## Required mixin footprint

`farmers_spell.mixins.json` is `required: true`, uses Mixin `0.8`, `compatibilityLevel: JAVA_21` and `defaultRequire: 1`.

Common mixins:

- `LivingEntityMixin`
- `AbstractSpellCastTimeMixin`
- `CreativeModeTabAccessor`
- `CreativeModeTabMixin`

Client mixins:

- `GluttonyArmorRendererMixin`
- `PlayerRendererMixin`
- `ReflectionModelMixin`

Total: **4 common + 3 client = 7 required direct bindings**.

These bindings are compatibility-sensitive implementation surfaces, not supported Black Arcana APIs. Their presence is a reason to keep current-host runtime acceptance fail-closed even though declared dependency ranges accept the physical versions.

## Network surface

The exact source contains `network/NetworkHandler.java`, but `registerPackets()` is empty. Targeted source search found no provider-owned `RegisterPayloadHandlersEvent`, `CustomPacketPayload`, `StreamCodec` or `PacketDistributor` registration path.

Safe catalog conclusion: **zero provider-owned payload registrations are observed at the exact source pin**.

This does not prove that every host interaction is network-free; Iron's and Minecraft retain their own networking/runtime authority. It only means this provider audit does not establish a separate Farmer's Spell payload protocol.

## Black Arcana boundary

Black Arcana must not bind directly to these mixins as a stable interoperability API. A future adapter requires a provider/host-native supported seam or a narrowly validated observation boundary. Missing or drifting hooks fail closed.

Provider spell execution remains one causal Iron's/provider-native action. Black Arcana must not duplicate projectile/effect settlement, mana use, cooldowns, scroll acquisition or status application merely because it observes the action.
