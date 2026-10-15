# Ars Nouveau 5.13.1 — prepared exact-publisher class-callsite proof (NOT ID-exact)

**🟡 Physical workflow pending.** Even if the workflow passes, the class-callsite report alone **does not promote** Ars Nouveau's 109 objects to COUNTED_EXACT because class registration does not prove 109 namespaced ResourceLocation identities.

## Authority and finite scope

- Sibling physical modlist #047: ars_nouveau-1.21.1-5.13.1.jar, mod ID ars_nouveau, physical SHA-1 02782d071ee5fab3b5c4b8ced67b7e1748277dfd.
- Previous independent binary host fingerprint (Ars Additions proof [#38266741543](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38266741543)): 20,107,711 bytes, official CurseForge project/file 401955/8721482. No new binary match is inferred until the isolated workflow completes.
- Modrinth publisher 5.13.1: qEFs5RRw. The workflow allows download only if version, NeoForge/Minecraft target, literal filename and publisher SHA-1 match the physical digest, then verifies the complete downloaded file again.
- Pinned public reference [baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157](https://github.com/baileyholl/Ars-Nouveau/tree/112920ff774831f204031da75b4c4e73d3765157), APIRegistry.setup(); only type names and registration structure were used as audit references, not upstream implementation code.
- Static source-located inventory already exists: **85 glyph parts** (5 forms + 67 effects + 13 augments) and **24 ritual classes** = **109 previously counted semantic primitives**. Composed spell chains are not extra static registries.

## Probe construction

docs/qa/ars_5131_static_registry_audit.py inspects SHA-gated Java 21 bytecode with javap -c -p, searches only APIRegistry.setup(), associates every registerSpell with an INSTANCE class producer and every registerRitual with a constructed ritual class, detects omissions, additions and duplicates, and rejects conditional jumps between the registrations. It compares the observed complete class-owner sets against the pinned 85+24 manifest. No remote provider code or JAR is committed.

Nine Java 21 synthetic tests check manifest sizes, correct two-plus-two producer paths, class identity substitution, missing calls, malformed constructor relations, conditional calls, duplicate manifests and SHA-gate rejection. The test fixture is independently authored and does not require the actual Ars JAR.

## Limits and non-promotion contract

**Class identities are not registry IDs.** Before upgrading COUNTED_SOURCE_PINNED to COUNTED_EXACT, separately verify all 85 glyph ResourceLocation IDs and 24 ritual ResourceLocation IDs from compiled bytecode, including class constructor/constant paths, namespace rules, registration call reachability, and exclusions, then reconcile consumer ledgers and repeat final-head CI. A pass from this preliminary audit alone does not satisfy those criteria.

Actual class initialization, glyph learning, books/tier/cost configuration, spell-context composition, GlyphRegistry/RitualRegistry loading, mana/Source transactions, ability activation, ritual effects, Survival, multiplayer, RPG Skill Tree perks and Black Arcana provider boundaries remain ⚠️. Black Arcana owns its own runtime; Ars owns glyph/casting/mana/Source; never duplicate settlement or create a second resolver.

**Campaign unchanged until later exact-ID evidence:** 33/39 currently exact, 6/39 conditioned, strict minima 1,856 global / 1,854 scoped, delta +0, denominator unknown. Stage 06.05 remains 🟡 and Stage 09 remains the owner of release-candidate physical QA.
