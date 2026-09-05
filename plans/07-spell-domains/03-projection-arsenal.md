# 07.03 — Projection & Arsenal

## Implemented mechanics

Stage 07.03 now provides the bounded, server-authoritative contracts for:

- Echo Armament;
- Ephemeral Tempering;
- Spectral Arsenal;
- Rift Blades;
- Oathforged Ascension point allocation and ledger seams.

Projected weapons and projectiles are ephemeral representations/handles. Black Arcana does not duplicate persistent real items, copy arbitrary item NBT, or create a parallel client-authoritative inventory.

## Frozen technical ceilings

The current hard safety ceilings are defined by `ProjectionSafetyCeilings`:

- `MAX_ACTIVE_ECHOES = 48`;
- `MAX_PROJECTILES_PER_VOLLEY = 64`;
- `MAX_RAW_ATTACK_DAMAGE = 100.0`;
- `MAX_ASCENSION_POINTS = 20`;
- `MAX_PROFILE_REGISTRY_ENTRIES = 64`;
- `MAX_PROFILE_ID_LENGTH = 64`.

These are technical ceilings, not final spell balance. Stage 08 owns progression and balance below these bounds.

## Runtime authority and safety

All 07.03 runtime settlement is server-authoritative.

- Echo Armament resolves allowlisted projected weapon profiles instead of cloning real inventory stacks.
- Ephemeral Tempering applies bounded temporary projection state rather than mutating or duplicating persistent equipment.
- Spectral Arsenal owns bounded ephemeral arsenal sessions/handles and releases their projection budget on lifecycle termination.
- Rift Blades owns bounded projectile handles with explicit lifetime, range and active-projection accounting. Handles release their budget on expiry, collision, range termination, owner logout or server shutdown.
- Rift Blades marked-strike damage passes through the canonical entity-interaction admission path and is re-authorized before settlement.
- Rift Blades gap-close is optional and independent from damage settlement. A blocked/unsafe destination fails closed for displacement without rolling back already-authorized real damage.
- Gap-close never force-loads a destination. Loaded-chunk state, world border, collision/headroom, fluids, protection admission, teleport support and vehicle state are checked and revalidated before displacement.

The historical stacked implementation depended on the later 07.04 `content/space/SafeDestinationPolicy`. That dependency is intentionally not imported here. Its small pure destination-fact checks are preserved locally in the Rift Blades adapter over already-canonical Stage 04 world-safety primitives, so 07.03 remains isolated from 07.04 Space & Displacement.

## Provider-native boundary

Iron's Spells remains the preferred active-cast/materialization host where its verified API is applicable. Black Arcana owns the bounded authority, projection profile, lifecycle and safety contracts; it does not synthesize persistent Iron's items or bypass provider authority.

Oathforged Ascension currently exposes deterministic allocation/ledger primitives only. No synthetic provider progression currency or unverified host settlement is invented. Provider-specific behavior that requires the real modpack remains part of deferred final validation unless a verified provider hook exposes the required identity and causal contract.

RPG mastery may specialize projection behavior below the frozen technical ceilings, but client presentation/input never becomes authoritative gameplay state.

## Automated evidence

The 07.03 implementation followed explicit RED→GREEN slices.

- Ephemeral Tempering: workflow `33986994360` (#972) passed JUnit, diff sanity, NeoForge build, JAR verification, 47 required GameTests and dedicated-server smoke.
- Spectral Arsenal: RED workflow #974 failed only the four new GameTests while `MinecraftSpectralArsenalRuntime` was absent; GREEN workflow `33989714645` (#976) passed the complete pipeline with 51 required GameTests and dedicated-server smoke.
- Rift Blades: RED workflow `33989972103` (#982) passed unit/build/JAR gates and failed exactly the seven new Rift Blades GameTests because `MinecraftRiftBladesRuntime` was absent. GREEN workflow `33990282195` (#984) passed the complete pipeline with all 58 required GameTests and dedicated-server smoke.
- Integrated runtime registration: workflow `33990511277` (#986) passed JUnit, diff sanity, NeoForge build, JAR verification, all 58 required GameTests and dedicated-server smoke on the complete 07.03 branch.

## Acceptance state

`IMPLEMENTED / AUTOMATED GATES GREEN / REAL-MODPACK HOST ACCEPTANCE DEFERRED`

The automated evidence validates deterministic Black Arcana contracts and NeoForge server integration. It does not convert provider-specific or real-modpack/manual host acceptance into PASS.