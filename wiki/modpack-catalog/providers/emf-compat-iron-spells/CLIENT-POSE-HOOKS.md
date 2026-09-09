# Client pose hooks — EMF Compat: Iron's Spells 2.0.0

## Casting-state input

`IronSpellsCompat.isCasting(AbstractClientPlayer)` reads Iron's client state only:

- local player: `ClientMagicData.isCasting()`;
- remote player: `ClientMagicData.getSyncedSpellData(player).isCasting()`.

The compat consumes this state for rendering. It does not originate casts and it does not provide a server-authoritative cast result.

## Pose source

The addon registers the EMF Compat Core pose source name `iron_spells` with priority **10**.

That priority is a presentation merge priority only. It does not define Black Arcana spell priority, damage priority, proc ordering or provider authority.

## `PlayerModelMixin`

Target: Minecraft `PlayerModel`.

- mixin priority: `2500`;
- injects into `setupAnim` at `RETURN`;
- only handles `AbstractClientPlayer`;
- if disabled or the player is not casting, clears the saved `iron_spells` pose;
- while casting, saves only left/right arm snapshots;
- head/body/legs are not captured by this addon;
- when `ironspells.bodyFollowArms=true`, it also records the body base position so the casting arms can follow torso movement through the core pose system.

This is pose capture after the underlying Iron's/Player Animator casting animation. It is not spell targeting or cast validation.

## `PlayerRendererMixin`

Target: Minecraft `PlayerRenderer`.

The mixin injects twice into the first-person `renderHand(...)` path, immediately before the arm and sleeve `ModelPart.render(...)` calls. For the matching left/right arm it retrieves the saved `iron_spells` pose and applies rotation to both the arm and sleeve.

It does not cast, debit mana, alter cooldowns or send packets.

## `EMFAnimationPauseHandlerMixin`

Target: EMF `EMFAnimationPauseHandler.shouldAnimationsPause` at `RETURN`, cancellable.

Behavior:

1. only acts when EMF would otherwise pause animations;
2. ignores null/unidentified render states;
3. preserves an explicit per-entity pause already present in `EMFAnimationPauseHandler.entitiesPaused`;
4. requires an `AbstractClientPlayer`;
5. when Iron's reports that player casting, changes the return value to `false` so EMF animation continues.

This prevents Player Animator's active Iron's cast from freezing the entire EMF player animation while the arm pose is separately preserved.

## First-person vanilla-model condition

During client setup the addon registers an EMF vanilla-model condition.

It returns true only when all of these are true:

- addon enabled;
- entity is an `AbstractClientPlayer`;
- player is the local player;
- EMF Compat Core reports that player in first person;
- Iron's reports that player casting;
- Iron's `SHOW_FIRST_PERSON_ARMS` or `SHOW_FIRST_PERSON_ITEMS` client config is enabled.

This is a client rendering decision for first-person visibility.

## Config

Two booleans are registered through EMF Compat Core:

| Key | Default | Meaning |
|---|---:|---|
| `ironspells.enabled` | `true` | master switch for the Iron's EMF compatibility layer |
| `ironspells.bodyFollowArms` | `true` | body-follow arm pose mode; false selects legacy rotation-only behavior |

## Mixin manifest

`emf_compat_iron_spells.mixins.json` is required, Java 21 compatible, and contains exactly three client mixins:

- `PlayerModelMixin`
- `PlayerRendererMixin`
- `EMFAnimationPauseHandlerMixin`

No common/server mixins are declared by this addon.

## Runtime dependency boundary

Exact source metadata declares all relevant mod dependencies on side `CLIENT`:

- Minecraft `[1.21.1,1.22)`;
- NeoForge `[21,)`;
- EMF Compat Core `[2.0.0,)`;
- Iron's Spells `[1.21.1-3.15.0,)`;
- Entity Model Features `[3.3.2,)`.

The source build additionally compiles against ETF 7.2.1, but ETF is not declared as a direct dependency in this addon's NeoForge metadata. Do not invent a direct runtime dependency that the provider metadata does not declare.

## Black Arcana boundary

These hooks are presentation-only. They are not safe or meaningful hooks for Black Arcana's canonical cast pipeline.

Black Arcana must never interpret:

- a saved EMF pose as proof of a cast;
- a first-person vanilla-model condition as cast authority;
- `ClientMagicData.isCasting()` as a server-authoritative BA input;
- EMF pose priority as combat/proc priority.

If Black Arcana later needs EMF-specific visual semantics, its adapter must consume BA server-owned cast state through the existing BA presentation boundary and remain independent from this Iron's-specific client compat.
