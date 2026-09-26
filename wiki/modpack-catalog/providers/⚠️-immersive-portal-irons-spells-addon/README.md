# Immersive Portal - Iron's Spells 'n Spellbooks Addon — 1.0.1

Status: `⚠️ PARTIAL / CURRENT PHYSICAL 1.0.1 / PORTAL-SPELL BRIDGE / +0 INDEPENDENT SPELL IDENTITIES / PUBLIC SOURCE STILL 1.0.0 / RELEASE-EXACT INTERNALS + ASSEMBLED QA FAIL-CLOSED`

## Current physical identity

Current sibling authority: `neoforge-rpg-skilltree@a0bf15c16f7e22eb42c4665bbe7a9dace8b8fda8`.

Certified sibling dossier: `PROJECT-INSTRUCTIONS/modlist/✅-immersive-portal-irons-spells-n-spellbooks-addon.md`.

- JAR: `immersive_portal_irons_spells_n_spellbooks_addon-1.0.1.jar`;
- mod id: `immersive_portal_irons_spells_n_spellbooks_addon`;
- runtime: `1.0.1`;
- Minecraft / loader: 1.21.1 / NeoForge;
- physical SHA-1: `ebfd9e75b591cf3fd250dbcdd219706b6afb96f1`;
- exact official release: CurseForge File `8770439`, Release, 2026-08-30;
- current host Iron's Spells: `1.21.1-3.16.3`;
- current portal core: `immersive_portals_core` `6.0.7`, provided by Immersive Aeronautics `1.1.4` in this pack.

Physical identity is closed by the sibling/JAR audit. This dossier does not install a second Immersive Portals top-level provider.

## Provider role

The addon is a bridge between Iron's existing Portal Spell runtime and Immersive Portals. Iron's remains authority for cast admission, mana, cooldown and host spell state. Immersive Portals remains authority for portal entities, linkage and entity transfer. The addon owns the adaptation/lifecycle layer between those systems.

Publisher-facing evidence describes the feature as turning Iron's Portal Spell portals into see-through Immersive Portals and exposing portal-size configuration.

That is an interoperability surface over an existing host spell, not evidence of a new standalone spell identity.

## Official source boundary

Official repository: `AitherLight/Immersive-Portal---Iron-s-Spells-n-Spellbooks-Addon`.

Current public source head inspected: `c3ab3709b6dce124ef9e342490df58aed98f80e8`, dated 2026-08-27.

Its `gradle.properties` still declares:

- `mod_version=1.0.0`;
- Iron's `1.21.1-3.16.2`;
- Immersive Portals `6.0.7`;
- NeoForge `21.1.233`.

The installed official release is 1.0.1 and was uploaded three days later. Therefore this source is useful for architecture, but it is **not** treated as exact 1.0.1 source or byte-equivalent proof.

## Bounded source architecture — 1.0.0 only

The inspected public source contains 29 Java files and 14 declared mixins (11 common + 3 client). The bridge surface includes:

- server-side bridge/pair registry and lifecycle tracking;
- Immersive Portals portal factory/linkage support;
- Iron portal-frame and entity-portal adaptation;
- client portal overlay/render support;
- config for bridge enablement, spell-portal enablement, block-portal enablement, portal-size scale and visual overlay;
- a mixin targeting Iron's `PortalSpell` block-portal handling, invoking the bridge after the host spell finishes linking the portal frame.

The source metadata describes the mod as a compatibility addon for Iron's Portal Spell and requires `irons_spellbooks` plus the Immersive Portals core modules.

No independent provider spell-registry surface is demonstrated by this inspected source tree. Its spell-facing hook targets the existing host `PortalSpell` class.

## Semantic disposition

Independent provider-owned standalone spell identities established: **0**.

The bridge modifies/adapts behavior of an existing Iron's spell. It therefore contributes **+0 strict semantic objects** to the Black Arcana provider spell denominator.

This does not make the component irrelevant: it owns a real runtime interoperability layer around portal creation, lifecycle, transfer and presentation.

## Why the provider remains ⚠️

Do not promote this provider to a fully source-exact ✅ closure yet because:

1. installed artifact is 1.0.1 while public source still declares 1.0.0;
2. the 1.0.1 changelog only states `Fixed some issues`; exact changed internals are not published in the evidence currently available;
3. exact 1.0.1 config keys/ranges and mixin targets must not be inferred solely from 1.0.0 source;
4. the pack uses Immersive Aeronautics as the provider of `immersive_portals_core`, so assembled compatibility must be validated against that rewrite;
5. lifecycle and exactly-once portal creation are runtime QA questions, separate from semantic identity.

Therefore the catalog state is **⚠️ partial / conditioned**, with semantic contribution fixed at **+0 independent spell identities**.

## Authority and deduplication

- Iron's Spells owns cast/mana/cooldown/host spell state.
- Immersive Portals owns portal entity/linkage/teleport mechanics.
- This addon owns only the bridge between the two.
- Black Arcana must not create a second Portal Spell, a second teleport settlement path, or infer cast success from client rendering.
- A single authorized host cast must not create duplicate linked portal pairs through another Black Arcana listener.
- RPG Skill Tree receives no magic runtime authority from this compatibility addon.

## QA / remaining evidence

Required assembled checks remain fail-closed:

- dedicated server + client boot with physical 1.0.1, Iron's 3.16.3 and Immersive Aeronautics-provided core 6.0.7;
- one valid host Portal Spell cast produces the intended single portal bridge/pair;
- failed/cancelled cast leaves no partial portal state;
- no duplicate mana/cooldown settlement;
- chunk unload/reload, reconnect and restart lifecycle;
- entity transfer occurs once, without an extra teleport path;
- current physical config values and valid ranges;
- interaction with True Immersion and other portal-related mixins.

## Result

**⚠️ Partial / conditioned.**

Semantic inventory: **0 independent spells**. The addon is cataloged as a host-spell interoperability bridge; release-exact 1.0.1 internals and assembled runtime behavior remain open.
