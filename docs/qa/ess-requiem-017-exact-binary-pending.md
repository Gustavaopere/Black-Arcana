# Requiem 0.1.7 — compiled registry gate (independent CI pending)

State: **⚠️ COUNTED_SOURCE_PINNED — NOT COUNTED_EXACT until publisher bytes pass the installed SHA and Java 21 inspection proves entire inventory.**

## Locked physical inputs

- Provider: Ender's Spells and Stuff: Requiem, mod ID ess_requiem
- Sibling physical entry #265: ess_requiem-0.1.7.jar, NeoForge 1.21.1
- Installed SHA-1: c4648cced4f9e96527cfa4e3f5edcdcead43abb1
- Publisher: CurseForge project 1336977, file 8762149
- Source pin: EnderTheNerd/ESS-Requiem@04ab715d657368b177267a8df196c32329acf3f6
- Canonical source inventory: wiki/modpack-catalog/providers/✅-enders-spells-and-stuff-requiem/SOURCE-0.1.7-SPELL-INVENTORY.md

## Gate semantics

Java 21 workflow downloads the publisher JAR and demands its SHA-1 match the installed physical hash before calling javap.

1. Detect 55 compiled static construction registrations in GGSpellRegistry.
2. Detect three compiled static construction registrations in the DTE addon DTESpellRegistry.
3. Resolve each compiled constructed class's stored ResourceLocation ID and getSpellResource getter.
4. Compare all 58 IDs with the canonical inventory: 53 counted and five excluded implementation/AI roots.
5. Verify three DTE-specific IDs: forever_dreaming, nightmare, nightmare_scream.

Missing, unexpected, duplicate or unparsable identities, changed class construction, wrong hash or missing compiled classes fail closed. This proves classfile identity, not a live registered or usable spell.

## Scope and blockers

- DTE 1.4.4 is physically present, but conditional startup branch invocation is not confirmed.
- No direct gameplay, assembled server/client, recipe or loot, actual configuration, casting, mana/cooldown settlement, multiplayer, lifecycle, load/reload/restart or Survival tests.
- Requiem owns its abilities and effects, Iron's owns host casting/mana/cooldown, DTE owns its content. Black Arcana must not duplicate any provider-native settlement.
- RPG Skill Tree Mastery/perks integration remains without an approved bridge.
- No publisher JAR or proprietary source code is redistributed; CI retains only JSON evidence.
- Stage 06.05 remains 🟡; Stage 09 retains the physical acceptance rows.

Promotion requires exact-release Java workflow success on synchronized PR head, reconciled 39-provider matrix and consumer tests, canonical CI, merge and postmerge verification. Until then **28/39 exact / 11/39 conditional; 1,857 global / 1,855 in scope**.
