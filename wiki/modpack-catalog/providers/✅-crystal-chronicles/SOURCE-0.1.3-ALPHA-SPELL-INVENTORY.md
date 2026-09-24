# Crystal Chronicles 0.1.3-alpha — source-pinned spell inventory

## Evidence boundary

Current physical identity:

- physical order #208;
- `crystal_chronicles-0.1.3-alpha.jar`;
- runtime `0.1.3-alpha`;
- physical SHA-1 `afdc32ab27661cd52160280dc4273d70a2d4a3d2`.

Current sibling evidence:

`neoforge-rpg-skilltree@49d9910ca0abfb9c0608c2730ab3ae8cefc59a9a`

Version-correlated official source pin:

`VeroxUniverse/CrystalChronicles-NeoForge@dff00d5ebbc5c726dad010f0d4cd40201ba4fc17`

The source pin declares `mod_version=0.1.3-alpha` and is the last inspected repository commit on the 2026-06-30 release date.

The current sibling dossier preserves installed-JAR SHA-1 `afdc32ab27661cd52160280dc4273d70a2d4a3d2`. This remains `COUNTED_SOURCE_PINNED` rather than `COUNTED_EXACT` because no byte-equivalence comparison to a build from the source pin has been established.

## Active registry inventory

| # | Registry ID | Display name | School | Cast | Mana | Rarity | Max level | Cooldown | Semantic role |
|---:|---|---|---|---|---:|---|---:|---:|---|
| 1 | `crystal_chronicles:prismatic_portal` | Prismatic Portal | `crystal_chronicles:prismatic` | LONG / 60 ticks | 150 | LEGENDARY | 1 | 60 s | formed Bismuth portal activation outside Alpha; return-to-spawn from Alpha |

Active provider-owned registrations: **1**.

Semantic delta: **+1 `COUNTED_SOURCE_PINNED`**.

## Registration closure

Pinned `CCSpells` creates one `DeferredRegister<AbstractSpell>` and makes one active `SPELLS.register(...)` call.

Observed registration properties:

- namespace owner: `crystal_chronicles`;
- registration ID source: `PrismaticPortalSpell.SPELL_ID`;
- concrete class: `PrismaticPortalSpell`;
- no conditional branch in the registration method;
- no config gate in the registration method;
- no optional-mod gate in the registration method.

Pinned `PrismaticPortalSpell` does not override provider-specific `allowCrafting`, `isEnabled` or `canBeCraftedBy` behavior.

Generic Iron's deployed configuration remains an external runtime gate.

## Prismatic school

The same pin owns one SchoolRegistry entry:

- ID: `crystal_chronicles:prismatic`;
- focus: `crystal_chronicles:prismatic_focus`;
- provider attributes: Prismatic spell power and Prismatic magic resistance.

The school itself is taxonomy/support and contributes **+0** semantic spell identities.

## Catalog-level reachability

The exact pin provides:

1. `crystal_chronicles:prismatic_focus` containing `crystal_chronicles:rainbow_bismuth_crystal`;
2. an Iron's `school_focus` tag extension containing `#crystal_chronicles:prismatic_focus`;
3. a provider smelting recipe that produces `crystal_chronicles:rainbow_bismuth_crystal` from `#crystal_chronicles:bismuth/full_blocks`.

This establishes the provider side of the generic Iron's focus route at catalog level.

It does **not** prove the deployed host's generic spell config, live Scroll Forge behavior or survival balance.

## Exact semantic signature

### `crystal_chronicles:prismatic_portal`

Provider-owned action identity:

- long cast;
- fixed level cap 1;
- portal/travel utility rather than damage scaling;
- outside Alpha: requires a formed, inactive provider portal frame in cast targeting range and activates the provider portal;
- inside Alpha: returns the player to respawn, otherwise Overworld shared spawn;
- server-player/server-level guarded behavior;
- no spell-power damage/scaling contract.

Deduplication consequence:

- this is a real provider-owned portal/travel spell identity;
- it must not be collapsed into generic teleport spells merely because the endpoint is dimensional;
- portal-block state, chisel use and the spell are parts of one provider travel system, not separate spell identities.

## Host spell references excluded

The pinned item registry equips Crystal Chronicles weapons with Iron's-owned preset spells.

Observed host identities include:

- Divine Smite;
- Frostwave;
- Flaming Strike;
- Poison Breath;
- Magic Missile;
- Shadow Slash;
- Blood Slash;
- Volt Strike;
- Chain Lightning;
- Throw.

Disposition: `HOST_OWNED_PHYSICALIZATION / +0`.

They remain counted only under Iron's.

## Clean-room boundary

This inventory records factual interoperability/catalog facts:

- registration identity;
- school ownership;
- public configuration signature;
- high-level cast semantics;
- focus/tag route;
- host-spell ownership.

No provider method body, model, texture, localization prose, recipe ingredient layout or implementation formula is reused in Black Arcana.

## Result

- provider-owned active spell registrations: **1**;
- source-level conditional registration gates: **0**;
- source-level provider-specific craft/enabled overrides on the spell: **0**;
- catalog-level focus route: **present**;
- strict semantic delta: **+1**;
- assembled-pack runtime validation: **pending / fail-closed**.
