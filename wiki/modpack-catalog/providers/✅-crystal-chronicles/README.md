# Crystal Chronicles — 0.1.3-alpha

Status: `COUNTED_SOURCE_PINNED / 1 PROVIDER-OWNED SPELL / CATALOG ✅ / ALPHA-WIP / RUNTIME QA FAIL-CLOSED`

## Current physical identity

Current sibling authority at `neoforge-rpg-skilltree@49d9910ca0abfb9c0608c2730ab3ae8cefc59a9a` preserves the certified Crystal Chronicles dossier:

- physical order: **#208**;
- JAR: `crystal_chronicles-0.1.3-alpha.jar`;
- runtime version: `0.1.3-alpha`;
- Minecraft: 1.21.1 / NeoForge;
- required provider stack in the pack: AzureLib 3.1.11, Iron's Spells 'n Spellbooks 3.16.3, Biolith 3.0.14 and Fusion 1.3.15+a.

The sibling dossier does not preserve an independent installed-JAR SHA for this row, so source-build byte equality is not claimed.

## Source pin

Official source repository:

`VeroxUniverse/CrystalChronicles-NeoForge`

Version-correlated source checkpoint:

`dff00d5ebbc5c726dad010f0d4cd40201ba4fc17`

That commit is dated 2026-06-30, is titled `Incremented version number`, and changes the project version from `0.1.2-alpha` to `0.1.3-alpha`. No later commit exists on 2026-06-30 in the inspected repository history.

The pinned `gradle.properties` declares:

- `mod_id=crystal_chronicles`;
- `mod_version=0.1.3-alpha`;
- Minecraft 1.21.1;
- source-side Iron's dependency 3.16.0;
- source-side AzureLib 3.1.8;
- source-side Biolith 3.0.11.

Because the physical pack uses newer provider versions and no physical JAR hash is available here, this catalog is `COUNTED_SOURCE_PINNED`, not `COUNTED_EXACT`.

## Exact source-pinned spell registry

The pinned `CCSpells` owns one Iron's `DeferredRegister<AbstractSpell>` under the `crystal_chronicles` namespace.

It has exactly one active registration:

- `crystal_chronicles:prismatic_portal` → `PrismaticPortalSpell`.

The registry method contains no config branch, mod-presence branch or optional registration path around that identity.

The exact English localization contains one provider-owned root spell identity:

- `spell.crystal_chronicles.prismatic_portal` → **Prismatic Portal**.

No second Crystal Chronicles spell registration is established by the inspected source pin.

## Prismatic Portal

Catalog signature:

| Field | Source-pinned value |
|---|---|
| Registry ID | `crystal_chronicles:prismatic_portal` |
| Display name | Prismatic Portal |
| School | `crystal_chronicles:prismatic` |
| Cast type | LONG |
| Cast time | 60 ticks |
| Base mana | 150 |
| Rarity | LEGENDARY |
| Max level | 1 |
| Default cooldown | 60 seconds |
| Spell power scaling | 0 / no spell-power scaling in the concrete class |

Semantic behavior:

- outside the provider's `crystal_chronicles:alpha` dimension, the cast targets a formed, inactive Bismuth portal frame and activates that portal;
- inside the Alpha dimension, the same spell returns the server player to their respawn position, falling back to the Overworld shared spawn.

The catalog records that behavior at signature level only; implementation bodies are not copied into Black Arcana.

## School and acquisition route

Crystal Chronicles registers the provider-owned school:

- `crystal_chronicles:prismatic`.

Its focus tag is:

- `crystal_chronicles:prismatic_focus`.

The exact pin populates that focus with:

- `crystal_chronicles:rainbow_bismuth_crystal`.

The exact pin also adds `#crystal_chronicles:prismatic_focus` to Iron's `irons_spellbooks:school_focus` tag.

A provider-owned smelting recipe produces `crystal_chronicles:rainbow_bismuth_crystal` from the provider's full-block Bismuth tag.

Under the same generic Iron's focus/Scroll Forge contract used by other source-pinned addons in this catalog, this closes a catalog-level focus route. Exact deployed Iron's config and live Scroll Forge behavior remain runtime QA.

## Host-owned spells embedded in gear

Crystal Chronicles equipment references several Iron's `SpellRegistry` identities through preset spell containers.

Those spell identities remain owned by Iron's and are **not** counted again under Crystal Chronicles.

Examples observed at the pin include host-owned Divine Smite, Frostwave, Flaming Strike, Poison Breath, Magic Missile, Shadow Slash, Blood Slash, Volt Strike, Chain Lightning and Throw.

Gear physicalization does not mint new semantic spell identities.

## Semantic accounting

Crystal Chronicles contributes:

- **+1 `COUNTED_SOURCE_PINNED` semantic spell identity**;
- **+0** additional identities for the Prismatic school itself;
- **+0** for provider gear containing already-owned Iron's spells;
- **+0** for portal blocks, chisel, dimension, biomes, armor, weapons or the Diffraction Ring.

Shared global semantic totals are intentionally not edited in this narrow checkpoint because concurrent catalog PRs are reconciling the same global ledgers.

## Alpha/WIP boundary

The physical dossier explicitly marks 0.1.3-alpha as WIP/Alpha.

It also records:

- placeholder equipment recipes;
- incomplete dimension content;
- worldgen/portal/progression instability risk;
- hard dependencies on Iron's, AzureLib, Biolith and Fusion;
- explicit OptiFine incompatibility in publisher documentation.

Catalog closure does not promote any of those surfaces to runtime-stable contracts.

## Runtime state — fail-closed

Still unverified in the exact assembled pack:

- source-build ↔ installed-JAR byte equivalence;
- live registry parity for `crystal_chronicles:prismatic_portal`;
- deployed generic Iron's spell enable/crafting configuration;
- live Scroll Forge reachability;
- Bismuth portal assembly/activation exactly once;
- Alpha-dimension travel and return behavior;
- restart/reconnect while inside the dimension;
- multiplayer caster attribution;
- world/protection interactions;
- dependency-version coexistence against the physical pack;
- placeholder-recipe and progression balance.

## Authority boundary

- Iron's owns the host spell registry, casting pipeline, mana, generic scroll/focus contract and its own embedded spell identities.
- Crystal Chronicles owns `crystal_chronicles:prismatic_portal`, its Prismatic school/support content, Bismuth portal state and Alpha dimension.
- Black Arcana does not duplicate provider casting or portal state.
- RPG Skill Tree remains progression/Mastery/perk authority only through verified boundaries.

## Result

**✅ Cataloged at source-pinned semantic level: 1/1 active provider-owned spell registration at the 0.1.3-alpha source pin.**

Strict semantic delta: **+1**.

Runtime/provider integration remains fail-closed until direct assembled-pack evidence exists.
