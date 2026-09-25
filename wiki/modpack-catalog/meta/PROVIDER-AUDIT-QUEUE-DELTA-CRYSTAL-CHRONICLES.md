# Provider Audit Queue Delta — Crystal Chronicles 0.1.3-alpha

Date: `2026-09-23`

This narrow overlay applies to Crystal Chronicles until the shared current-provider ledgers are reconciled after concurrent catalog PRs.

## Current row

| Mod ID | Installed identity | Current effective audit state |
|---|---|---|
| `crystal_chronicles` | physical #208 / `crystal_chronicles-0.1.3-alpha.jar` / runtime `0.1.3-alpha` / SHA-1 `afdc32ab27661cd52160280dc4273d70a2d4a3d2` | ✅ `COUNTED_SOURCE_PINNED / 1 ACTIVE PROVIDER SPELL / PRISMATIC FOCUS ROUTE CATALOGED / +1 STRICT SEMANTIC / RUNTIME QA FAIL-CLOSED` |

## Physical evidence

Current sibling authority:

`neoforge-rpg-skilltree@49d9910ca0abfb9c0608c2730ab3ae8cefc59a9a`

Certified dossier:

`PROJECT-INSTRUCTIONS/modlist/Addons + Adventure and RPG + Armor, Tools, and Weapons + Dimensions + Magic/✅-crystal-chronicles v0.1.3-alpha.md`

The dossier preserves:

- physical order #208;
- `crystal_chronicles-0.1.3-alpha.jar`;
- runtime `0.1.3-alpha`;
- required physical host stack including Iron's 3.16.3;
- Alpha/WIP maturity and portal/dimension risk surface.

Physical SHA-1 is now preserved by the current sibling dossier: `afdc32ab27661cd52160280dc4273d70a2d4a3d2`. This fingerprints the installed JAR but does not prove source-build byte equivalence.

## Source evidence

Official source:

`VeroxUniverse/CrystalChronicles-NeoForge@dff00d5ebbc5c726dad010f0d4cd40201ba4fc17`

The pin:

- is dated 2026-06-30;
- bumps the project to `0.1.3-alpha`;
- is the last inspected repository commit on that release date;
- contains one `DeferredRegister<AbstractSpell>`;
- contains exactly one active provider-owned spell registration, `crystal_chronicles:prismatic_portal`.

## Closed by current evidence

- physical provider/version identity;
- source-correlated 0.1.3-alpha pin;
- exact active source registry cardinality: 1;
- exact provider spell ID;
- Prismatic school identity;
- spell rarity/level/mana/cast/cooldown signature;
- high-level portal/return semantic behavior;
- provider focus item/tag;
- provider injection of Prismatic focus into Iron's `school_focus`;
- provider recipe for the focus item;
- host-owned preset spell references excluded from Crystal Chronicles counting.

## Still open

- installed-JAR ↔ source-build byte equality;
- deployed Iron's generic spell enable/crafting config;
- live registry parity;
- Scroll Forge behavior in the assembled pack;
- portal activation exactly-once behavior;
- dimension persistence/restart;
- protection/multiplayer behavior;
- physical dependency-version coexistence;
- Alpha/WIP progression and placeholder-recipe balance.

## Semantic accounting

Provider-owned source-pinned semantic spell identities: **1**.

Strict semantic delta: **+1**.

The shared global numerator is intentionally not edited in this overlay because concurrent PRs #359 and #360 also reconcile shared catalog ledgers.
