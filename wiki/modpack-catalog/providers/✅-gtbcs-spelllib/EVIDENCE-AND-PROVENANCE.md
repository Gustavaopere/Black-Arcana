# GTBC's SpellLib 2.2.0 — evidence and provenance

## Evidence layers

### Physical authority

Current `modlist.txt` identifies:

- `gtbcs_spell_lib-2.2.0-1.21.1.jar`;
- mod id `gtbcs_spell_lib`;
- runtime version `2.2.0-1.21.1`;
- SHA-1 `36cce8ab3117e89ae992a84a566d596709db2ffe`;
- CurseForge package fingerprint `1996449855`.

This layer is authoritative for presence/version in the installed pack.

### Exact publisher release

CurseForge Project `1194714`, File `8824651` publishes `gtbcs_spell_lib-2.2.0-1.21.1.jar` for NeoForge / Minecraft 1.21.1 on 2026-09-06.

The exact 2.2.0 changelog records three added attributes:

- Healing Received;
- Damage Taken;
- Summon Health.

The project page classifies the mod as API/Library and describes it as shared code for the author's Iron's Spellbooks add-ons. It explicitly says that the library does not provide standalone gameplay on its own.

### Public API-role description

Publisher prose documents reusable infrastructure such as attributes, particle helpers, trade helpers, Curio/armor abstractions, an advanced spell base abstraction and summon checks. These descriptions prove library responsibility at a semantic level but do not establish exact Java signatures or runtime contracts for Black Arcana.

## Semantic count reasoning

The semantic-magic ledger counts provider-owned spells, glyph/spell-part primitives, rituals/rites and equivalent discrete magical player actions. It does not count attributes, developer helper classes, reusable bases, compatibility abstractions or items that only hold/imbue external spells.

GTBC's SpellLib therefore contributes **0 independent semantic magic objects** at the audited current publisher surface.

This does not mean its APIs are inert. Consumer mods may use its helpers to implement real spells and mechanics, but those identities remain owned by the consumer provider.

## License / clean-room posture

The project is All Rights Reserved. Publisher text explicitly prohibits extraction, reuse, redistribution, modification and decompilation of project code/assets and describes source as closed/private except for permissioned collaboration access.

Black Arcana posture:

- `REFERENCE_ONLY / COMPATIBILITY_TARGET / CLOSED_SOURCE ARR`;
- public factual behavior/API-role descriptions may be cataloged;
- no JAR decompilation;
- no copying/adapting code or assets;
- no inferred method/class signatures beyond publisher-named conceptual surfaces;
- provider-specific runtime/API claims remain fail-closed without an exact documented seam.

## Sources

- `https://www.curseforge.com/minecraft/mc-mods/gtbcs-spelllib`
- `https://www.curseforge.com/minecraft/mc-mods/gtbcs-spelllib/files/8824651`
