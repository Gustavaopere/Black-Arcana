# Ars Nouveau 5.13.1 — exact SHA-equal compiled glyph and ritual ResourceLocation IDs

**✅ COUNTED_EXACT for static binary identity of 109 already counted roots (85 glyph parts + 24 rituals). ⚠️ Not loaded GlyphRegistry / RitualRegistry, casts, runtime or Survival acceptance.**

## Reproducible publisher authority

- Sibling modlist exact physical #047: `ars_nouveau-1.21.1-5.13.1.jar`, mod ID `ars_nouveau`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`. Minecraft 1.21.1, NeoForge.
- Official publisher Modrinth `qEFs5RRw`; official CurseForge project/file `401955/8721482`.
- 20,107,711 bytes; SHA-256 `99dff85e8778f7ae21dfd51cdedadf20f555a834fc757c0afe5f03c10eea96f2`.
- [Previous independent 85+24 compiled registration calls #38687523172](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38687523172) SUCCESS and [previous PR #822](https://github.com/Gustavaopere/Black-Arcana/pull/822) merged, with [post-merge CI #38688054084](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38688054084) SUCCESS.
- **[Exact 109 physical ID audit #38691889186](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38691889186) SUCCESS**: SHA gate matches physical JAR, the previously proven 85+24 `APIRegistry.setup` owner registrations, the compiled ID literals and constants, and the per-class owner→ID reference manifests.
- 12 earlier Java 21 synthetic tests and 15 new fail-closed synthetic tests passed. The first new physical run [#38691711273](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38691711273) rejected the same-class `EffectSenseMagic` constructor notation; the final audit checks its exact `new → dup → getstatic → ldc → invokespecial → putstatic` chain without weakening other constructor guards.

## Exact count and closure

| Surface | Number | Static proof |
|---|---:|---|
| Forms | 5 | `GlyphLib` constant/literal → owner constructor → static registry call |
| Effects | 67 | same, with separate `reset`, `rewind` and `wololo` literal IDs |
| Augments | 13 | same |
| Rituals | 24 | `RitualLib` constant → `getRegistryName` → `ArsNouveau.prefix` → static registration call |
| **Existing semantic roots** | **109** | **109 unique namespaced IDs, zero new roots** |

The exact 85 class→ID reference pairs are in [glyph manifest](../../../docs/qa/ars_5131_glyph_class_id_manifest.json); 24 ritual pairs in [ritual manifest](../../../docs/qa/ars_5131_ritual_class_id_manifest.json). The inspection logic is [the clean-room Java 21 audit](../../../docs/qa/ars_5131_exact_ids_binary_audit.py), and the [synthetic adversarial tests](../../../docs/qa/ars_5131_exact_ids_binary_audit_test.py). Only names, IDs and bytecode identity structure are stored. No third-party JAR, code, models, sounds, textures or other assets are committed.

The manifest also reconciles the documented 85 `ars_nouveau:*` glyph IDs in the provider README. Player-composed spell chains are combinations of these primitives, not additional counted static spells. The 24 `RitualLib` constructors are distinct from spell parts. `GlyphLib.EffectEarthshakeID` is a library constant but does **not** appear among the 85 compiled `APIRegistry.setup` registrations and is not counted.

## Safety and scope

The publisher JAR contains six copies each of `META-INF/LICENSE.txt` and `META-INF/NOTICE.txt`; the earlier auditor allows exactly this metadata duplication and rejects duplicated compiled code or other archive entries. The static result does **not** prove live registry insertion during current modpack startup, enabled configs or glyph tiers, learning/recipe acquisition, provider-controlled mana or Source, execution of any particular spell or ritual, multiplayer concurrency, reload/save/restart, or Survival. These remain ⚠️ Stage 09 provider-real acceptance. Stage 06.05 remains 🟡.

Ars Nouveau owns its spell composition/resolution, mana and Source; Black Arcana owns only its own casting/ritual/hazard/world-safety runtime. RPG Skill Tree may supply progression/perks/gates through verified contracts; no RPG adapter was implemented, licensed third-party code copied, or gameplay settlement duplicated.

## Arithmetic

109 pre-existing `COUNTED_SOURCE_PINNED` semantic identities gain `COUNTED_EXACT` **for exact compiled static class→ResourceLocation identity only**; +0 semantic roots. Frozen 39-provider campaign **33 exact / 6 conditional → 34 exact / 5 conditional**. Strict semantic minimum **1,856 global / 1,854 in scope**, final denominator unknown.
