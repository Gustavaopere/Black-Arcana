# Stage 07.07 — Astral Severance avatar/viewpoint checkpoint plan

Implementation branch: `feat/stage07-07-astral-end-to-end`

Baseline: `main@ff5b99106c91723cce2a13f363f7af1336c5d5c1`.

## Scope

This checkpoint extends the already-canonical `AstralSeveranceRuntime` lifecycle with the missing bounded server-authored avatar/viewpoint and movement/control representation. It does not close the seven-spell specification gate, does not promote Stage 07.07, does not invent Stage 08 balance values, and does not create a second casting path.

Production activation remains downstream of `activateAuthorizedAstralProjection(...)`: the ordinary Stage 02 cast/channel transaction must eventually authorize Astral Severance before activation. Because the exact Astral Severance resource, cooldown, progression and final balance/config contracts are still open, this branch must not make the spell player-invocable by bypassing that gate.

The approved default interaction boundary remains non-combat and non-owning: the projection cannot cast from the astral position, attack, use/break/place blocks, open containers, move items, mount/possess entities, or become damage/proc/loot ownership authority.

## Exact platform constraints confirmed before implementation

- physical modlist: NeoForge `21.1.248`, Minecraft `1.21.1`, Java 21;
- NeoForge 1.21.1 `DeferredRegister` exposes generic `create(Registry/ResourceKey, namespace)`; the later `createEntities` convenience helper is not assumed;
- Minecraft 1.21.1 `EntityType.Builder` exposes `of`, `sized`, `noSummon`, `noSave`, `clientTrackingRange`, `updateInterval` and `build(String)`;
- NeoForge 1.21.1 exposes `EntityRenderersEvent.RegisterRenderers#registerEntityRenderer` and `MovementInputUpdateEvent` on the client event bus;
- Minecraft 1.21.1 `Input` exposes mutable `leftImpulse`, `forwardImpulse`, `jumping`, `shiftKeyDown`, and directional booleans used only as client intent.

## TDD sequence

1. RED — add deterministic tests requiring a server-owned projection pose/origin, monotonic exact-session movement intent, range/finite-value rejection, post-close rejection, and a source-level requirement that the Minecraft composition root uses a dedicated non-persistent avatar rather than an arbitrary observed entity.
2. GREEN — extend the domain lifecycle minimally so origin/pose and movement sequencing are server-owned. Movement input is normalized/bounded; client coordinates are never accepted.
3. GREEN — add a Black Arcana astral projection entity registered through the exact 1.21.1 registry API. It is no-save/no-summon, invisible through a `NoopRenderer`, non-pickable/non-attackable and has no inventory/combat/ownership behavior.
4. GREEN — make `MinecraftNoeticRuntime` spawn the avatar at the loaded living physical body after authorized lifecycle activation, keep body identity authoritative, move only the avatar through validated intent, and remove the avatar on every projection terminal path. Loaded-only/same-dimension and hard-range rules remain fail-closed; no chunk tickets or force-loading.
5. GREEN — add a dedicated bounded Astral network bridge: server→client BEGIN/END presentation carrying only server-authored projection identity/entity id, and client→server MOVE/RETURN intent carrying the exact projection identity plus bounded sequence/input. Server derives caster identity from the connection.
6. GREEN — add a physical-client Astral controller. It attaches the camera only to the server-spawned projection entity, converts movement keys to intent, suppresses those movement impulses from moving the physical body while projected, sends explicit return intent, and restores the physical camera on authoritative END/entity loss/disconnect. It does not admit projection or settle gameplay.
7. Refactor/validation — add wiring/codec/client source-contract tests, build/JAR/GameTests/dedicated-server smoke, then reconcile with latest `origin/main`, re-run exact-HEAD CI, update Stage 07.07 docs/status without marking the seven-spell gate complete, and only then merge if review/CI are green.

## Safety invariants

- server-authored projection UUID and server connection identity are both required;
- one active projection per physical caster; bounded global count;
- monotonic per-projection movement sequence; stale/replayed/foreign/post-close intent is ignored;
- client sends directional/look intent, never authoritative coordinates, range, duration, cost, cooldown or progression facts;
- same dimension and already-loaded region only; unavailable space refuses/terminates rather than force-loading;
- range is measured from the physical body/origin under the server's current state;
- body damage, final death, logout, dimension change, expiry, explicit exact-id return, avatar loss and server stop restore/clean the projection;
- no persistence/resume of astral avatar/session across logout/restart;
- no global entity/player/chunk scans and no unbounded per-tick network snapshots;
- no remote interaction/casting path is introduced by this checkpoint;
- RPG Skill Tree may later gate progression through a real contract, but never owns this runtime.

## Completion boundary

A green merge of this checkpoint may close the avatar/viewpoint/control implementation gap only. Stage 07.07 remains `IN PROGRESS` until `07-familiars-divination-specification-gate.md` closes the seven-spell authority/balance/provenance fields and any required acceptance evidence is correctly recorded under D031.