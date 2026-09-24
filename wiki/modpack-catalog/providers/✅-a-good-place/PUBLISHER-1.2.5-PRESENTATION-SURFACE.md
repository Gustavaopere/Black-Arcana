# A Good Place 1.21-1.2.5 — publisher-bounded presentation surface

## Evidence boundary

Current physical identity:

- `a_good_place-1.21-1.2.5-neoforge.jar`;
- mod id `a_good_place`;
- runtime `1.21-1.2.5`;
- Minecraft 1.21.1 / NeoForge.

Sibling authority:

`neoforge-rpg-skilltree@d7c99d23ef1b38fe62c86a362ec521ced8861f96`

Exact publisher binary:

- CurseForge project `1020455`;
- file `5974291`;
- `a_good_place-1.21-1.2.5-neoforge.jar`;
- Release;
- 2024-12-08;
- 1.21 + 1.21.1;
- NeoForge;
- Client environment.

Exact publisher sources artifact:

- file `5974293`;
- `a_good_place-1.21-1.2.5-neoforge-sources.jar`;
- same release date and supported versions.

The exact sources archive was not materialized into this audit environment, so this document does not claim a file-by-file source reconstruction. Public provider documentation is used to classify the exposed runtime.

## Publisher / official documentation role

The provider describes itself as a mod that adds block placement animations.

The official README describes it as client-side and Resource Pack-customizable.

The visual system includes:

| Surface | Role | Semantic magic disposition |
|---|---|---:|
| placement animation | temporary client representation of a placed block | +0 |
| Resource Pack definitions | configure visual behavior by data | +0 |
| block-state predicates | select which visual definition applies | +0 |
| scale | initial-to-final visual transform | +0 |
| translation | visual movement transform | +0 |
| rotation | visual rotation transform | +0 |
| rotation pivot | presentation pivot | +0 |
| height scale | presentation transform | +0 |
| duration | animation timing | +0 |
| curve controls | interpolation presentation | +0 |
| restrict direction | visual direction selection | +0 |
| optional sound | presentation feedback | +0 |

## 1.2.5 release-specific evidence

The exact 1.2.5 changelog states:

- improved logic for block entities;
- fixed an issue.

The sibling dossier carries this into the current pack as a regression target for:

- block entity rendering;
- duplicate/flicker presentation;
- orientation/state visuals.

These are rendering concerns, not gameplay action identities.

## Client/server boundary

The provider is published as **Client**.

The server/world placement result remains authoritative independently of the animation.

Two clients may therefore render different placement animations for the same accepted server-side placement if their Resource Pack/config state differs.

That does not constitute gameplay divergence.

## Semantic exclusion

Do not count the following as spells or equivalent magic actions:

- an animation JSON;
- a block-state predicate;
- a transform;
- a curve;
- a visual sound trigger;
- a block-entity render accommodation;
- shader/VFX composition;
- placement observation.

No provider-owned magic-action identity is established.

## Strict semantic result

- spells: 0;
- rituals/rites: 0;
- magical abilities: 0;
- equivalent discrete actions: 0.

Strict semantic delta: **+0**.

Status: **✅ zero-semantic presentation-layer closure**.
