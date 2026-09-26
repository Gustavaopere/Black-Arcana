# Iron's Spellbooks KubeJS — 4.0.3

Status: `⚠️ PARTIAL / CURRENT PHYSICAL 4.0.3 / EXACT OFFICIAL SOURCE VERSION PIN / SCRIPTABLE IRON'S SPELL+SCHOOL FRAMEWORK / 0 FIXED BUILT-IN SPELL IDENTITIES ESTABLISHED / CURRENT PACK SCRIPT INVENTORY UNVERIFIED / FAIL-CLOSED`

## Current physical identity

Current sibling authority rechecked at `neoforge-rpg-skilltree@a0bf15c16f7e22eb42c4665bbe7a9dace8b8fda8`.

Certified dossier: `PROJECT-INSTRUCTIONS/modlist/✅-irons-spellbooks-kubejs.md`.

- JAR: `irons_spells_js-4.0.3.jar`;
- mod id: `irons_spells_js`;
- runtime: `4.0.3`;
- Minecraft / loader: 1.21.1 / NeoForge;
- physical SHA-1: `0481395c5847e2920d1425e77833bef87df63139`;
- current physical Iron's Spells: `1.21.1-3.16.3`;
- current physical KubeJS: `2101.7.2-build.377`.

The sibling dossier classifies this mod as the KubeJS bridge for creating custom Iron's spells, schools, attributes and magic items, and explicitly states that the mod adds no content by itself without scripts. That statement does not prove that the assembled pack contains no relevant scripts.

## Exact official source pin

Official repository: `sentwayfarer/irons_spells_js`.

Exact 1.21.1 / 4.0.3 source checkpoint: `f3c05a102707a87ac3b8f0d2df5d2ffa5ae5b6c7` on branch `2101`.

The pin is dated 2025-11-18. Its `gradle.properties` declares:

- `minecraftVersion=1.21.1`;
- `modId=irons_spells_js`;
- `modVersion=4.0.3`;
- `neoVersion=21.1.199`;
- Iron's source baseline `1.21.1-3.11.0`;
- KubeJS source baseline `2101.7.2-build.315`;
- license `MIT`.

This is an exact source-version pin, not a physical-JAR↔source-build byte-equivalence claim.

The exact source tree at this pin contains 49 files including 30 Java files. The only JSON path in that tree is the provider mixin configuration; no packaged data spell-definition inventory is present.

## Framework surface

Exact `IronsSpellsJSPlugin` source registers KubeJS builder types for:

- Iron's `SpellRegistry.SPELL_REGISTRY_KEY` using `CustomSpell.Builder`;
- Iron's `SchoolRegistry.SCHOOL_REGISTRY_KEY` using `SchoolTypeJSBuilder`;
- spell-related attributes;
- custom magic swords;
- custom staves;
- custom spellbooks.

The same plugin exposes Iron's spell/school/casting bindings, cast/mana/selection events, EntityJS spell-casting helpers and Alchemist Cauldron recipe schemas.

Exact `IronsSpellsJSMod` does not define a fixed gameplay spell roster. During inter-mod enqueue it iterates KubeJS `RegistryObjectStorage` for the Iron's spell registry and creates Iron's server-config entries for objects built there.

Exact `CustomSpell` is a generic script-configurable `AbstractSpell` implementation whose builder exposes resource ID, school, rarity, max level, cooldown, mana/power fields, cast type/timing, callbacks, looting/learning/crafting gates, animations and pre-cast conditions.

Together, these surfaces establish a spell-construction framework rather than a provider-owned fixed spell catalog.

## Semantic disposition

### Base addon

- fixed built-in standalone spell identities established by the base addon itself: **0**;
- fixed built-in spell-school gameplay identities established by the base addon itself: **0**;
- scriptable spell/school/item builders: **present**.

This does not mean the current modpack has zero KubeJS-defined Iron's spells.

### Current pack scripts

The current pack's script-defined semantic inventory is **UNVERIFIED**.

Repository and Project-file searches performed on 2026-09-26 did not locate the exact current instance's `kubejs/startup_scripts` or relevant `server_scripts`. Absence from those available sources is not treated as proof that the physical CurseForge instance contains no such scripts.

A KubeJS script can register a custom Iron's spell under an arbitrary namespace, so filtering only namespace `irons_spells_js` cannot close this provider.

Current disposition:

**⚠️ partial / conditioned**

Strict contribution from the base framework itself: **+0**.

Any pack-script-defined semantic objects remain outside the denominator until the exact current script set or equivalent authoritative assembled-instance provenance is audited.

## Historical assembled-instance script evidence — not current closure

Project Library logs from a physical boot on 2026-09-08 provide a bounded historical observation:

- KubeJS Startup logged `startup_scripts:main.js#2: Hello, World! (Loaded startup example script)`;
- it then logged `Loaded 1/1 KubeJS startup scripts ... with 0 errors and 0 warnings`;
- the same boot inventory reports Iron's Spellbooks KubeJS 4.0.3 and KubeJS `2101.7.2-build.374`.

This strongly indicates that **that 2026-09-08 instance** had only the default/example startup script and no observed custom Iron's spell registration script.

It does **not** close the current pack: current sibling authority now records KubeJS `2101.7.2-build.377`, and the exact current `kubejs/` directory has not been captured. Historical script absence is not propagated across a later physical pack checkpoint.

Accordingly the current script-defined inventory remains `UNVERIFIED / NOT ADDITIVE` until current-instance evidence is available.

## Closure path

See [`PACK-SCRIPT-CLOSURE-CHECKLIST.md`](PACK-SCRIPT-CLOSURE-CHECKLIST.md).

Promotion to a closed zero-semantic framework requires authoritative current-instance evidence that no relevant Iron's spell/school registration exists. If scripts do register objects, they must be enumerated, deduplicated and evaluated for effective host config and survival reachability.

## Authority boundary

- Iron's Spells owns the spell registry, casting pipeline, mana, cooldown/config settlement and host semantics.
- KubeJS owns script lifecycle and registry-builder execution.
- Iron's Spellbooks KubeJS owns the bridge/builders/events that let scripts create or observe Iron's content.
- Pack scripts, when present, own the custom definitions they declare.
- Black Arcana must not synthesize missing script definitions, mirror Iron's settlement, double-debit mana/cooldown or treat client callbacks as cast authority.
- RPG Skill Tree receives no casting/runtime authority from this bridge.

## Runtime QA remains fail-closed

Exact source 4.0.3 was built against older host baselines than the current pack: Iron's 3.11.0 vs physical 3.16.3, and KubeJS build 315 vs physical build 377. Declared ranges permitting newer hosts are not an assembled-pack PASS.

Still separate from semantic inventory closure: startup registry lifecycle, Iron's config regeneration, server-script reload, duplicate listeners/IDs, mana/cooldown exactly-once settlement, EntityJS attribution, custom item persistence and dedicated-server/client behavior.

## Result

**⚠️ Partial / conditioned.**

The 4.0.3 base addon is cataloged as a scriptable Iron's/KubeJS framework with no fixed built-in spell inventory established by the provider itself. The current modpack's script-defined Iron's semantic inventory remains open until the physical scripts or equivalent authoritative assembled-instance evidence are available.

Strict semantic delta from the base framework itself: **+0**.
