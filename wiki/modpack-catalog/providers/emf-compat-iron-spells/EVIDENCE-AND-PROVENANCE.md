# Evidence and provenance — EMF Compat: Iron's Spells 2.0.0

## Physical layer

Authority: latest physical modlist `/mnt/data/modlist.txt`, SHA-1 `7aaece7acbfb07ba4d0c66029042f36c50d046f0`.

Installed row:

- `emf_compat_iron_spells_1.21.1_2.0.0.jar`
- mod id `emf_compat_iron_spells`
- runtime version `2.0.0`
- SHA-1 `515b545870fce128bbf01a0ccacdd19566ed3b22`

Relevant physical hosts:

- NeoForge `21.1.248`;
- `emf_compat_core` `2.0.0`;
- `entity_model_features` `3.3.5`;
- `entity_texture_features` `7.2.1`;
- `irons_spellbooks` `1.21.1-3.16.3`.

## Exact public source layer

Publisher repository:

`https://github.com/victorkozhokin/emf-compat`

Inspected revision:

`79d730a9d02275b7d721967c75f5f22dc815d9dc`

At this revision the dedicated NeoForge 1.21.1 Iron's subproject declares exactly:

- `mod_id=emf_compat_iron_spells`;
- `mod_version=2.0.0`;
- `mod_license=GNU GPL 3.0`;
- Minecraft `1.21.1`;
- NeoForge build baseline `21.1.230`;
- Java 21.

The exact package source consists of the mod entry class plus `compat` and `mixin` packages. The audited semantic Java surface is five classes:

1. `EMFCompatIronSpellsMod`
2. `IronSpellsCompat`
3. `PlayerModelMixin`
4. `PlayerRendererMixin`
5. `EMFAnimationPauseHandlerMixin`

The mixin manifest declares exactly the three mixin classes above as client mixins.

## Build/runtime dependency evidence

Exact source build dependencies:

- EMF Compat Core project;
- EMF `3.3.2-neoforge-1.21` compile-only;
- ETF `7.2.1-neoforge-1.21` compile-only;
- Iron's `1.21.1-3.15.6-neoforge` compile-only.

Generated NeoForge metadata declares client-side required dependencies:

- Minecraft `[1.21.1,1.22)`;
- NeoForge `[21,)`;
- EMF Compat Core `[2.0.0,)`;
- Iron's `[1.21.1-3.15.0,)`;
- EMF `[3.3.2,)`.

The physical pack is at or above those declared lower bounds. This supports the intended compatibility line but does not substitute for runtime QA.

## Publisher public surface

The publisher project describes this addon as making Iron's Spells casting poses work correctly with animated EMF player models. Current public project metadata classifies it as a client addon/bug-fix and GPLv3.

Some web indexing still exposes stale 1.0.0 file-list snapshots while the physical pack and publisher source both identify 2.0.0. Therefore the catalog does not use stale search-index file tables as version authority. Physical artifact + exact official source-version metadata are the stronger current evidence layers.

## What source inspection established

Read-only source inspection was used to establish factual catalog/interoperability properties only:

- zero standalone spells and zero gameplay registry surface in this subproject;
- client-only role;
- casting-state read path from Iron's client data;
- three exact mixin targets and behaviors;
- first-person EMF condition;
- two config keys;
- `iron_spells` pose source priority 10;
- dependency/version boundaries.

No provider implementation has been copied into Black Arcana.

## License / clean-room disposition

- exact subproject metadata: `GNU GPL 3.0`;
- publisher CurseForge project metadata: GPLv3;
- no root `LICENSE` file was located at the inspected revision through the repository contents endpoint;
- this phase uses source read-only for factual cataloging and interoperability analysis;
- no code, text, textures, models, sounds or other assets are copied/adapted into Black Arcana.

Any future implementation that would reuse provider code rather than merely interoperate must independently satisfy license/notice obligations. This catalog does not grant such reuse.

## Explicit non-equivalence

`SOURCE-PINNED EXACT VERSION` means the publisher source metadata matches the installed semantic version. It does **not** mean:

- the public tree has been reproducibly built and compared byte-for-byte with the physical JAR;
- every runtime transform/mixin succeeds in the full modpack;
- the physical JAR contains no packaging-only delta;
- newer physical Iron's/EMF internals are proven compatible merely because they satisfy the declared version ranges.

Those remain runtime/pack QA boundaries.

## Provenance ledger

This inspection is also recorded in `docs/provenance/REFERENCE_LEDGER.md` before the Phase 2AK source-derived catalog constraints are promoted to canonical `main`.
