# HazentouveLib 1.0.9 — evidence and provenance

## Physical authority

Sibling current physical authority:

- JAR `hazentouvelib-1.0.9.jar`;
- mod id `hazentouvelib`;
- runtime `1.0.9`;
- SHA-1 `b5d68711babb604e368b918683eb89a4d1492077`.

Physical identity remains controlled by the sibling modlist/JAR record.

## Exact source-version authority

Official repository: `Hazentouvel/HazentouveLib`.

Exact 1.0.9 checkpoint:

`641acf4e9e254f1af9f59b2eb2251ff0f1fcfc08`

Commit message: `HazentouveLib 1.0.9`.

Exact `gradle.properties`:

- `minecraft_version=1.21.1`;
- `neo_version=21.1.224`;
- `mod_id=hazentouvelib`;
- `mod_version=1.0.9`;
- `mod_license= Polyform Shield`.

Exact NeoForge metadata declares required dependencies on Minecraft, NeoForge, `irons_spellbooks` and `caelus`.

## Exact registration findings

### Schools

`HLSchoolRegistry` uses a `DeferredRegister<SchoolType>` against Iron's `SCHOOL_REGISTRY_KEY` and registers exactly:

- `hazentouvelib:radiance`;
- `hazentouvelib:shadow`;
- `hazentouvelib:cosmic`.

### Attributes

`HLAttributeRegistry` registers exactly six magic attributes: power and resistance for Radiance, Shadow and Cosmic.

### Effects

`HLEffects` registers exactly one mob effect: `hazentouvelib:hexed`.

`HLServerEvents` consumes Iron's `SpellPreCastEvent` and, for a server-side Hexed caster, applies 15% max-health damage with floor 1 using `hazentouvelib:corrupt_magic`.

### Soul Fire

`HLBlockRegistry` registers exactly one block, `hazentouvelib:soul_fire`.

`HLItemRegistry` registers seven items; the magic-relevant direct-use item is `hazentouvelib:soul_igniter`, which places/ignites Soul Fire through provider logic.

`HLDataAttachments` registers the `hazentouvelib:soul_fire` attachment backed by `SoulFireData.ATTACHMENT`. `SoulFireData` serializes burn ticks and exposes a custom payload for client synchronization.

The exact resource tree contains five provider damage-type JSONs:

- `corrupt_magic`;
- `cosmic_magic`;
- `radiance_magic`;
- `shadow_magic`;
- `soul_fire`.

### Upgrade-orb data

The exact tree contains three Iron's upgrade-orb-type JSON definitions:

- `radiance_power`;
- `shadow_power`;
- `cosmic_power`.

A `hydro_power` `ResourceKey` exists in Java, but no matching packaged data definition exists at this exact checkpoint; active registration is not claimed.

## Exact zero-spell result

Recursive exact-tree inspection shows spell-related class names because the library supplies reusable spellcasting abstractions. The bootstrap registers items, attachments, blocks, effects, particles, sounds, attributes and schools.

No concrete provider spell register is established:

- no provider `DeferredRegister<AbstractSpell>`;
- no concrete HazentouveLib spell registration list;
- no glyph/spell-part registry;
- no ritual registry.

Strict result:

- spells **0**;
- glyphs **0**;
- rituals **0**.

## Clean-room / license boundary

The exact 1.0.9 source metadata declares `Polyform Shield`. This catalog uses the public source read-only to establish factual registry names, counts, authority and interoperability boundaries.

No HazentouveLib source code, assets, models, textures, sounds or implementation are copied or adapted into Black Arcana.

Source-version correlation does not prove reproducible byte identity with the physical JAR.
