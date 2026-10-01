# Artifacts — 13.2.5

Status: `✅ CATALOGED / EXACT PHYSICAL=PUBLISHER ARTIFACT / 49 ITEM ENTRIES / FORMAL ITEM-ABILITY COMPONENT LAYER / ZERO INDEPENDENT SEMANTIC MAGIC IDENTITIES IN CURRENT STACK / RELIQUIFIED ARTIFACTS OWNS 52 COUNTED ABILITY ROOTS / +0 STRICT`

## Current physical identity

Current sibling authority: `neoforge-rpg-skilltree@682a62c13c38215691be24361ffd303abb32dc01`.

Certified dossier:

`PROJECT-INSTRUCTIONS/modlist/Adventure and RPG + Armor, Tools, and Weapons + Cosmetic + Structures/✅-artifacts v13.2.5.md`

- JAR: `artifacts-neoforge-13.2.5.jar`;
- mod id: `artifacts`;
- runtime: `13.2.5`;
- Minecraft / loader: 1.21.1 / NeoForge;
- physical SHA-1: `fb6cd3be2d034dde369ffd7558c95c6daa44189e`;
- exact official source pin: `ochotonida/artifacts@7cf7dc42e322e13f096eea16cee17a4b400b75f7`.

## Exact publisher-artifact closure

NON-MERGE evidence PR **#493** audited CurseForge project/file **312353 / 8791899** and hard-gated the publisher artifact against the current physical fingerprint.

- audit HEAD: `a744600829646f2cd49aec541f690eff0dd392d8`;
- exact-artifact run: `36834282003` — SUCCESS;
- evidence artifact: `11148453543`;
- evidence digest: `sha256:207eabe4db1c82141868e88eb5d1fe2d736d819ac928b13db45d1d2fc856a245`;
- publisher SHA-1: `fb6cd3be2d034dde369ffd7558c95c6daa44189e`;
- publisher SHA-256: `e36a929420a0a616abdb28f5bbbdb866a426aa3bb78d1b39bc1183927c101ce6`;
- bytes: `1,086,922`.

The publisher SHA-1 exactly equals the current physical sibling SHA-1. The catalog therefore describes the exact installed 13.2.5 artifact.

See [`EXACT-13.2.5-ARTIFACT-AUDIT.md`](EXACT-13.2.5-ARTIFACT-AUDIT.md).

## Provider inventory

Exact `ModItems` exposes **49 top-level item entries**:

- 4 non-wearable/utility entries;
- 45 wearable entries across head, necklace, belt, hands, feet and generic Curio surfaces.

The exact artifact also contains a formal item-ability implementation layer under `artifacts/component/ability/**`. The audit observes **37 ability-related class files**, including support/nested classes around double jump, air swimming, death-protection teleport, Ender Pearl cost/immunity, damage absorption/immunity, post-damage effects/cooldowns, retaliation, cure effects, fluid collision, attack effects and hunger/plant-growth behavior.

See [`ITEM-ABILITY-SURFACE.md`](ITEM-ABILITY-SURFACE.md) for the complete current item inventory and semantic disposition.

## Why this provider contributes +0 independent semantic magic objects

The Black Arcana semantic ledger counts standalone spells, glyph/spell-parts, rituals/rites and **equivalent discrete supernatural action identities**. It explicitly does not count item containers, gear, attributes, statuses or downstream effects merely because they are magical in presentation or behavior.

Artifacts 13.2.5 does **not** expose a provider-owned spell/focus/action identity registry comparable to Iron's spells, Ars glyphs, Goety foci, Vampirism actions or Relics named `AbilityTemplate` roots. Its base gameplay is attached to concrete item definitions through attributes, data components, item methods and event-driven effects.

This distinction matters in the current pack because **Reliquified Artifacts 1.0.8 is installed and already cataloged**. Its canonical source audit proves that it redirects/extends **48 `artifacts:<id>` owners** into the Relics framework and closes **52 owner-scoped named ability roots**, already counted once as `COUNTED_SOURCE_PINNED`.

Counting the Artifacts item containers or their unnamed base component effects again would double-count the same current owner surface merely because two providers participate in its implementation stack.

Current semantic disposition:

- Artifacts item identities: **0 additional semantic magic identities**;
- Artifacts data-component/effect machinery: **0 additional identities**;
- Reliquified Artifacts named ability roots: remain **+52** under their existing provider catalog;
- Mimic Spawn Egg / utility food/item behavior: **+0**.

Strict semantic delta from base Artifacts: **+0**.

## Authority boundary

- **Artifacts** owns the original `artifacts:<id>` item identities, base item/data-component behavior, Mimic content and base loot/acquisition lineage.
- **Reliquified Artifacts** owns the Relics ability implementations injected for the redirected Artifact owners.
- **Relics** owns generic ability/rank/XP/cooldown framework semantics.
- **Curios** owns equip-slot lifecycle.
- Black Arcana must not create a second accessory-effect ledger or count one Artifact owner twice because the current stack layers Reliquified behavior over it.
- RPG Skill Tree retains only its own progression/contracts and does not become Artifacts runtime authority.

## Runtime QA remains separate

Catalog closure does not prove assembled-pack runtime behavior. Still fail-closed:

- Artifacts 13.2.5 + Reliquified Artifacts 1.0.8 + Relics 0.12.8 coexistence;
- exact Curios equip/unequip state under 9.5.1;
- toggle and cooldown persistence;
- death-protection exactly-once behavior;
- loot/Mimic/Quark behavior;
- movement-provider interaction;
- combat proc deduplication;
- Sophisticated Backpacks pickup interaction;
- dedicated multiplayer behavior.

These are runtime/integration gates, not open semantic-denominator questions.

## Result

**✅ Cataloged.**

Artifacts 13.2.5 is now closed as the exact current base item/ability-component provider with **49 item entries** and **+0 independent semantic magic objects** in the current stack. The effective named supernatural ability roots layered onto Artifact owners remain counted once under the already-canonical Reliquified Artifacts provider.
