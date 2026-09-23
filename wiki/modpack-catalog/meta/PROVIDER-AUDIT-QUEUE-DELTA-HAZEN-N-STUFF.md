# Provider Audit Queue — Hazen N Stuff 1.4.0.14 delta

Date: `2026-09-22`

This is a narrow status overlay over the historical `PROVIDER-AUDIT-QUEUE.md`. It prevails for `hazennstuff` until the current physical magic-provider queue is regenerated from the sibling's newest physical modlist.

## Current row

| Mod ID | Installed identity | Current effective audit state |
|---|---|---|
| `hazennstuff` | `hazennstuff-1.4.0.14.jar` / runtime `1.4.0.14` / physical SHA-1 `3be20bacb44c1923348ab6f61b685eec6aacfdcd` | `✅ SOURCE-PINNED SPELL CATALOG COMPLETE / 38 ACTIVE IRON'S SPELL REGISTRATIONS / 3 NON-ACTIVE LOCALIZATION ROOTS EXCLUDED / PROVIDER REGISTRY UNCONDITIONAL AT SOURCE PIN / CUSTOM SCHOOL FOCUS ROUTES + 3 SPECIAL CRAFT GATES RECONCILED / ASSEMBLED-PACK RUNTIME QA FAIL-CLOSED` |

## Evidence

Physical authority:

- sibling `neoforge-rpg-skilltree@278b427023136d7c43d85dc188d0eac1ac85ef3a`;
- certified dossier `✅-hazen-n-stuff v1.4.0.14.md`;
- current physical JAR `hazennstuff-1.4.0.14.jar`;
- mod id `hazennstuff`;
- runtime `1.4.0.14`;
- physical SHA-1 `3be20bacb44c1923348ab6f61b685eec6aacfdcd`.

Source pin:

`Hazentouvel/Hazen_N_Stuff@5fcaf39cf399609f6c1c87d14f8d4807098c9cce`

The source commit is release-correlated to 1.4.0.14 and declares that version in project metadata. Source-to-physical byte equality is not claimed.

## Semantic closure

The exact source-pinned registry contains **38 active `AbstractSpell` registrations**.

Distribution:

- Ender 1;
- Blood 2;
- Fire 6;
- Ice 2;
- Lightning 3;
- Nature 4;
- Evocation 2;
- Holy 1;
- Radiance 4;
- Shadow 4;
- Eldritch 1;
- Cosmic 4;
- Hydro 5.

`brimstone_hellblast` and `supernova` are localization-only and excluded because they are not active release-pinned registry entries. `reign_of_tyros` is also excluded: its class/localization root exists, but the exact release-pinned `registerSpell(...)` line is commented.

Semantic disposition: **+38 `COUNTED_SOURCE_PINNED`**.

## Reachability posture

The provider registry class contains no conditional-registration/config/mod-presence branch at the exact source pin.

Thirty-six registered spells inherit the host/default Iron's craftability/enabled contract at the inspected provider source level.

Three registrations inherit provider-specific `canBeCraftedBy` gates:

- Golden Shower -> Golden Shower Spellbook;
- Night's Edge Strike -> Night's Edge or True Night's Edge;
- Scorching Slash -> Raven's Bane.

The exact release packages crafting acquisition for Golden Shower Spellbook, Night's Edge and Raven's Bane.

Custom school focus routing is backed by Hazen 1.4.0.14 resources plus current HazentouveLib 1.0.9 source-correlated focus registration. Hydro uses Ace's Spell Utils focus infrastructure.

## Runtime QA still open

Catalog closure does not claim:

- physical JAR <-> source-build byte equality;
- full assembled-pack registry sync;
- deployed Iron's generic config values;
- exact runtime cast/cooldown/network behavior;
- multiplayer ownership/protection;
- provider compatibility behavior;
- numerical balance.

These remain fail-closed.

## Global accounting consequence

The strict reconstructible semantic minimum moves from **1344** to **1382**.

The historical technical denominator of 100 components predates the sibling's current 22/09 physical re-audit and did not include Hazen N Stuff as a canonical provider row. Hazen therefore closes the next known provider component, but no updated technical fraction is declared until the provider denominator is regenerated from the current physical modlist.
