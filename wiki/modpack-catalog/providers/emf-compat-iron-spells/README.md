# EMF Compat: Iron's Spells 'n Spellbooks 2.0.0

## Status

`SOURCE-PINNED EXACT 2.0.0 / CLIENT PRESENTATION COMPAT / 0 SPELLS / 0 CASTING AUTHORITY / 3 CLIENT MIXINS / 2 CONFIG KEYS / COMPONENT #39 CANDIDATE`

This provider is a client-side animation compatibility addon. It does not add spells, schools, mana, cooldowns, targeting, damage logic or a second casting path. Its role is to keep Iron's Spells casting arm poses visible when Entity Model Features (EMF) animates player models.

## Physical identity

- artifact: `emf_compat_iron_spells_1.21.1_2.0.0.jar`
- mod id: `emf_compat_iron_spells`
- version: `2.0.0`
- physical SHA-1: `515b545870fce128bbf01a0ccacdd19566ed3b22`
- Minecraft: `1.21.1`
- loader: NeoForge
- environment: client

Physical related providers in the same 595-entry pack:

- `emf_compat_core` `2.0.0`, SHA-1 `e22256acaaabc43d4043b119a748e8f52e27a451`;
- `entity_model_features` `3.3.5`, SHA-1 `e78060b9a01bf41b5628bd45ce5ac741f68f092c`;
- `entity_texture_features` `7.2.1`, SHA-1 `908d09263709193b918fdc9ca0d79c9d90c4a531`;
- `irons_spellbooks` `1.21.1-3.16.3`, SHA-1 `017fd8140c477f9ae602cf95594f1c23bef1d6e3`.

## Exact official source pin

`victorkozhokin/emf-compat@79d730a9d02275b7d721967c75f5f22dc815d9dc`

The exact NeoForge 1.21.1 Iron's subproject declares:

- `mod_id=emf_compat_iron_spells`
- `mod_version=2.0.0`
- `mod_license=GNU GPL 3.0`
- Java 21
- NeoForge build baseline `21.1.230`

The source build uses Iron's `1.21.1-3.15.6-neoforge` and EMF `3.3.2-neoforge-1.21`; runtime metadata requires Iron's `>=1.21.1-3.15.0`, EMF `>=3.3.2`, EMF Compat Core `>=2.0.0` and NeoForge `21.x`. The physical pack is newer on Iron's/EMF/NeoForge and exact on Core. Runtime rendering behavior on the full pack remains QA evidence, not inferred from version ranges.

## Complete semantic surface

Standalone semantic spells: **0**.

Provider-owned semantic gameplay registries: **0 observed in the exact subproject**.

Client compatibility surface:

1. `PlayerModelMixin` — captures the Iron's casting pose for the left/right arms after player animation is applied;
2. `PlayerRendererMixin` — restores saved arm rotation for first-person arm/sleeve rendering;
3. `EMFAnimationPauseHandlerMixin` — prevents EMF's generic Player Animator pause from freezing EMF animation during an Iron's cast, while respecting explicit per-entity pauses;
4. first-person EMF vanilla-model condition — only for the local player while casting and while Iron's first-person arms/items are enabled;
5. two config keys: `ironspells.enabled` and `ironspells.bodyFollowArms`;
6. source priority `10` for the `iron_spells` pose source in EMF Compat Core.

There are no provider C2S/S2C gameplay packets, resource costs, spell registration, cooldown ownership, targeting, server events or world effects in this compatibility surface.

## Authority and deduplication

- **Iron's Spells** owns casting state, spells, mana, cooldowns and synced remote casting state.
- **EMF Compat: Iron's Spells** owns only the client presentation adapter that captures/restores casting pose data around EMF animation.
- **EMF Compat Core / EMF** own the shared pose/animation framework their APIs expose.
- **Black Arcana** must not use this visual addon as a cast trigger, cast confirmation, mana hook or server authority signal.
- Black Arcana's own presentation may coexist, but it must not double-restore provider arm poses or mutate this provider's pose source.
- RPG Skill Tree receives no progression authority from this visual compatibility layer.

## Black Arcana implications

This component closes a visual compatibility unit, not a spell-content unit. It proves that the physical pack already has a provider-native solution for keeping Iron's casting arm poses visible under EMF.

No Black Arcana capability gap is created by the existence of this mod. A future BA-specific EMF presentation integration, if required, must use its own bounded client presentation contract and must not route BA casting authority through these mixins.

## Evidence boundary

Confirmed:

- exact physical version and SHA-1;
- exact official source version `2.0.0`;
- complete five-class Java package surface plus mixin config for this subproject;
- three required client mixins;
- two config keys and source priority;
- declared client-only dependencies and minimum versions;
- GPLv3/GNU GPL 3.0 publisher/source metadata.

Not claimed:

- byte-for-byte reproducibility between the public source tree and the physical JAR;
- full-modpack visual correctness with every player-animation resource pack;
- compatibility behavior outside the exact client hooks documented here;
- any spell/casting authority belonging to this addon.

See:

- [`CLIENT-POSE-HOOKS.md`](./CLIENT-POSE-HOOKS.md)
- [`EVIDENCE-AND-PROVENANCE.md`](./EVIDENCE-AND-PROVENANCE.md)
